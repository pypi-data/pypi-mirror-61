import json
import os
import re
import requests
from requests_toolbelt import MultipartEncoderMonitor, MultipartEncoder
from tqdm import tqdm

from moderage.clients.client import ModeRageClient
from moderage.experiment import Experiment


class ServerClient(ModeRageClient):

    def __init__(self, host, port, cache_location, mr_service):
        super().__init__("ServerClient", cache_location, mr_service)
        self._root_url = f'{host}:{port}'
        self._experiment_base_url = f'{self._root_url}/v0/experiment'

    def check(self):
        try:
            response = requests.get(f'{self._root_url}/health')

            if response.status_code == 200:
                return True
            else:
                self._logger.debug(f'Server check responded with [{response.status_code}]')
                return False
        except requests.exceptions.ConnectionError:
            self._logger.debug(f'Could not connect to server at [{self._root_url}]')
            return False

    def save(self, meta_category, meta, started_timestamp, ended_timestamp, git_tag=None, parents=None, files=None, keep_originals=False):
        """
        Save using moderage server
        """

        parents = [{'id': str(p['id']), 'metaCategory': p['metaCategory']} for p in
                   parents] if parents is not None else []

        create_request = {
            'metaCategory': meta_category,

            'startedTimestamp': started_timestamp,
            'endedTimestamp': ended_timestamp,
            'gitTag': git_tag,

            'meta': meta,
            'parents': parents
        }

        create_response = requests.post(f'{self._experiment_base_url}/create', json=create_request)

        assert create_response.status_code == 201, create_response.json()

        experiment_json = create_response.json()

        id = experiment_json['id']

        if files is not None:
            experiment_json = self._upload_files(id, meta_category, files, keep_originals)

        experiment_cache_location = self._get_experiment_cache_location(id, meta_category)

        return Experiment(experiment_json, self._mr_service, experiment_cache_location)

    def load(self, id, meta_category, lazy_file_download=True):
        """
        Load from moderage server
        """

        get_response = requests.get(f'{self._experiment_base_url}/{meta_category}/{id}')
        assert get_response.status_code == 200, get_response.json()
        experiment = get_response.json()

        experiment_file_location = self._cache_location.joinpath(meta_category, id)

        if not experiment_file_location.exists():
            experiment_file_location.mkdir(parents=True)

        self._logger.info(f'[{len(experiment["files"])}] files found')

        # download the files from their uris
        for file_info in experiment['files']:

            cached_filename = experiment_file_location.joinpath(file_info['id'])

            # If we have not cached the file already, download it and move it to the cache directory
            cached = cached_filename.exists()

            if lazy_file_download:
                file_info['downloaded'] = cached
            else:
                cached_filename = experiment_file_location.joinpath(file_info['id'])

                # If we have not cached the file already, download it and move it to the cache directory
                if not cached:
                    self._logger.info(f'Downloading file: [{file_info["filename"]}]')
                    self.download_file(file_info, str(cached_filename))
                else:
                    self._logger.info(f'File found in cache: [{file_info["filename"]}]')

                file_info['downloaded'] = True

        experiment_cache_location = self._get_experiment_cache_location(id, meta_category)

        return Experiment(experiment, self._mr_service, experiment_cache_location)

    def download_file(self, file_info, cached_filename):

        location = file_info['location']
        startswith = location.startswith('https://s3.amazonaws.com')
        if startswith:
            import boto3
            # Download the file
            s3 = boto3.client('s3')

            m = re.search(r'https://s3.amazonaws.com/(?P<bucket>\w+)/(?P<key>.+)', location)

            bucket = m.group('bucket')
            key = m.group('key')

            file_size = s3.head_object(Bucket=bucket, Key=key)['ContentLength']

            with(tqdm(total=file_size, ncols=100, unit="bytes", bar_format="{l_bar}{bar}|")) as progress_bar:

                # Callback for progress to be output by tqdm progress bar
                def _download_progress(chunk):
                    progress_bar.update(chunk)

                s3.download_file(bucket, key, cached_filename, Callback=_download_progress)

        elif location.startswith('http'):

            # Download the file
            with requests.get(location) as r:
                with open(cached_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)

    def add_parents(self, id, meta_category, parents):

        add_parents_request = {'parents': parents}

        upload_response = requests.post(
            f'{self._experiment_base_url}/{meta_category}/{id}/addParents',
            json=add_parents_request,
        )

        assert upload_response.status_code == 200, upload_response.json()

        experiment_json = upload_response.json()

        experiment_cache_location = self._get_experiment_cache_location(id, meta_category)

        return Experiment(experiment_json, self._mr_service, experiment_cache_location)

    def add_files(self, id, meta_category, files, keep_originals=False):
        upload_response = self._upload_files(id, meta_category, files, keep_originals)

        experiment_cache_location = self._get_experiment_cache_location(id, meta_category)

        return Experiment(upload_response, self._mr_service, experiment_cache_location)

    def _upload_files(self, id, meta_category, files, keep_originals):

        file_info_list = []

        multipart_payload = []

        for file in files:
            file_info = dict.copy(file)

            local_filename, uploaded_filename = self._process_filenames(file)
            file_info['filename'] = uploaded_filename

            multipart_payload.append(('files', (uploaded_filename, open(local_filename, 'rb'))))
            file_info_list.append(file_info)

        file_info_payload = {
            'files': file_info_list
        }

        multipart_payload.append(('file_metadata', (None, json.dumps(file_info_payload))))
        multipart_encoder = MultipartEncoder(multipart_payload)

        self._logger.info(f'Experiment saved with id [{id}]')
        self._logger.info(f'Uploading [{len(files)}] files to experiment [{id}]')

        # Set up a progress bar for upload progress
        with(tqdm(total=multipart_encoder.len, ncols=100, unit="bytes", bar_format="{l_bar}{bar}|")) as progress_bar:
            last_bytes_read = 0

            # Callback for progress to be output by tqdm progress bar
            def _upload_progress(monitor):
                nonlocal last_bytes_read
                progress_diff = monitor.bytes_read - last_bytes_read
                progress_bar.update(progress_diff)
                last_bytes_read = monitor.bytes_read

            multipart_monitor = MultipartEncoderMonitor(multipart_encoder, _upload_progress)

            upload_response = requests.post(
                f'{self._experiment_base_url}/{meta_category}/{id}/addFiles',
                data=multipart_monitor,
                headers={'Content-Type': multipart_encoder.content_type}
            )

        assert upload_response.status_code == 200, upload_response.json()

        # Remove the files that were just uploaded
        if not keep_originals:
            for file in files:
                local_filename, uploaded_filename = self._process_filenames(file)
                os.remove(local_filename)

        return upload_response.json()
