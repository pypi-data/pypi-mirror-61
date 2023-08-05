import logging
from datetime import datetime
from pathlib import Path

import magic
import yaml
import re

from moderage.clients import LocalClient, ServerClient


class ModeRage():

    def __init__(self, config_data=None):

        self._server_config_defaults = {
            'host': 'http://localhost',
            'port': '8118',
        }

        self._local_config_defaults = {

        }

        self._logger = logging.getLogger("Mode Rage client")
        self._logger.info(f'Attempting to load Mode Rage config')

        # By default assume that the experiment has started now
        self._started = datetime.now()

        if isinstance(config_data, dict):
            self._mode, self._config = self._load_config(config_dict=config_data)
        else:
            self._mode, self._config = self._load_config(config_filename=config_data)

        cache_location = self._config['cache_location']
        if not cache_location.exists():
            cache_location.mkdir()

        self._logger.debug(f'Cache location: [{str(cache_location)}]')

        if self._mode == 'server':
            host = self._config['server']['host']
            port = self._config['server']['port']
            self._client = ServerClient(host, port, cache_location, self)

            if not self._client.check():
                self._logger.warning(f'Server not found, defaulting to local cache. host: [{host}:{port}]')
                self._mode = 'local'

        # Will save and load from local cache and use tinydb for file lookup
        if self._mode == 'local':
            self._client = LocalClient(cache_location, self)

        if self._git_snapshot_enabled():

            # Snapshots the current code onto a branch starting with 'mr-snapshot-{timestamp}'
            from git import Repo
            self._repo = Repo()
            self._logger.debug("Git integration enabled, repo will be snapshotted")
            # Create branch with mr_shapshot_{timestamp}

            formatted_date_time = re.sub('[/:]', '', self._started.strftime('%x%X'))
            self._snapshot_start_tag = f'mr_snapshot_{formatted_date_time}_start'

            current_branch = self._repo.active_branch

            changes_to_track = len(self._repo.index.diff(None)) > 0

            if changes_to_track:
                self._repo.git.add(u=True)
                self._repo.git.commit('-m', f'Snapshot {self._snapshot_start_tag}')
                self._repo.remote().push(current_branch)
            tag = self._repo.create_tag(self._snapshot_start_tag)
            self._repo.remote().push(tag)

            self._logger.debug(f'Created snapshot of current code on branch {self._snapshot_start_tag}')

    def _git_snapshot_enabled(self):
        return 'git' in self._config and 'snapshot' in self._config['git'] and self._config['git']['snapshot']

    def _get_git_remote(self):
        if 'remote' in self._config['git']:
            return self._config['git']['remote']
        else:
            return next(self._repo.remote().urls)

    def get_config(self):
        return self._config

    def _default_config_key_if_empty(self, config, key, default):
        if key not in config:
            config[key] = default
        return config

    def _load_config(self, config_dict=None, config_filename=None):
        """
        Looks for .mrconfig in local directory and loads settings if present
        """

        local_defaults = {
            'cache_location': Path.home().joinpath('.moderage')
        }

        # Use default config location if none is available
        if not config_filename and not config_dict:
            config_filename = './.mrconfig'

        if config_dict is not None:
            config = config_dict
        else:
            try:
                with open(config_filename, 'r') as config_file:
                    config = yaml.safe_load(config_file)
            except IOError as e:
                self._logger.info('Cannot load .mrconfig file. Using defaults.', e)
                return 'local', local_defaults

        mode = config['mode']
        del config['mode']

        config = self._default_config_key_if_empty(config, 'cache_location', local_defaults['cache_location'])

        config['cache_location'] = Path(config['cache_location'])

        # expand any tilde '~' characters to full directory
        config['cache_location'] = config['cache_location'].expanduser()

        if mode == 'server':
            config = self._default_config_key_if_empty(config, 'server', self._server_config_defaults)
            return 'server', config
        elif mode == 'local':
            config = self._default_config_key_if_empty(config, 'local', self._local_config_defaults)
            return 'local', config

    def save(self, meta_category, meta, parents=None, files=None, keep_originals=False):
        """
        :param parents: list of objects containing the id and category of experiments that this experiment relies on

        for example:

        {
            "id": "05c0581c-7ece-4cad-a26f-0e415ea1b01d",
            "metaCategory": "grid_world"
        }

        :param meta_category: A category name for this experiment, or this dataset
        :param meta: meta information for this experiment or dataset
        :param files: A list of files and metadata associated with this experiment or dataset

        Files must be in the following format:

        [
            "filename": "./path/to/my/file.xyz",
            "caption": "This is a description of my file"
        ]

        :return:
        """

        self._logger.info(f'Saving data to category [{meta_category}]')

        if files is not None:
            files = [self._process_file_info(file) for file in files]

        ended = datetime.now()
        started_timestamp = int(self._started.timestamp()*1000)
        ended_timestamp = int(ended.timestamp()*1000)

        git_tag = None
        if self._git_snapshot_enabled():
            remote_url = self._get_git_remote()

            url_parts = re.match('git@(?P<domain>.*):(?P<path>.*)\.git', remote_url)
            domain = url_parts.group('domain')
            path = url_parts.group('path')

            if 'gitlab.com' in domain:
                git_tag = f'https://{domain}/{path}/-/tags/{self._snapshot_start_tag}'
            elif 'github.com' in domain:
                git_tag = f'https://{domain}/{path}/tree/{self._snapshot_start_tag}'

        saved_experiment = self._client.save(
            meta_category,
            meta,
            started_timestamp,
            ended_timestamp,
            git_tag=git_tag,
            parents=parents,
            files=files,
            keep_originals=keep_originals)

        if self._git_snapshot_enabled():
            formatted_date_time = re.sub('[/:]', '', ended.strftime('%x%X'))
            snapshot_end_tag = f'mr_snapshot_{formatted_date_time}_end_{saved_experiment.id}'

            ended_tag = self._repo.create_tag(snapshot_end_tag)
            self._repo.remote().push(ended_tag)

        return saved_experiment

    def add_parents(self, id, meta_category, parents):
        """

        :param id:
        :param meta_category:
        :param parents:
        :return:
        """

        self._logger.info(f'Adding parents to data experiment [{id}] in category [{meta_category}]')

        return self._client.add_parents(id, meta_category, parents)

    def add_files(self, id, meta_category, files, keep_originals=False):
        """

        :param id:
        :param meta_category:
        :param files:
        :return:
        """

        self._logger.info(f'Adding files to data experiment [{id}] in category [{meta_category}]')

        if files is not None:
            files = [self._process_file_info(file) for file in files]

        return self._client.add_files(id, meta_category, files, keep_originals=keep_originals)

    def download_file(self, file_info, cached_filename):
        return self._client.download_file(file_info, cached_filename)

    def load(self, id, meta_category, lazy_file_download=True):
        """
        Load an experiment
        :param id: the id of the experiment
        :param meta_category: the category of the experiment
        :param lazy_file_download: if 'True' will not download files until 'Experiment.get_file' is used
        """

        self._logger.info(f'Loading data with id [{id}] in category [{meta_category}]')

        return self._client.load(id, meta_category, lazy_file_download)

    def _process_file_info(self, file):
        """
        Get the mime type of the file
        :param file:
        :return:
        """

        local_filename = file['file'] if 'file' in file else file['filename']

        file['contentType'] = magic.from_file(local_filename, True)

        return file
