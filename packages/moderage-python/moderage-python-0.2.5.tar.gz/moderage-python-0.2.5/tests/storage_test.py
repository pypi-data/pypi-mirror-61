import uuid
from io import BufferedReader

from moderage import ModeRage
from moderage.experiment import Experiment

# Experimental Data such as accuracy, metrics, hyperparameters, anything important
meta = {
    'text_data': 'Hello there this is some text data',
    'numeric_data': 6,
    'list_data': [0, 1, 2, 3],
    'dict_data': {
        'key1': 1,
        'key2': [1, 2, 3],
        'key3': 'text within dict data'
    }
}

# Any files associated with the experiment
files = [
    {
        'filename': 'examples/disapproval.jpg',
        'caption': 'Poppy disapproves of this nonsense'
    },
    {
        'file': 'examples/test.txt',
        'filename': 'text_text.txt',
        'caption': 'This text file contains text'
    }
]

# The Id and metaCategory of an experiment or dataset that this dataset is dependent on
parents = [{
    'id': str(uuid.uuid4()),
    'metaCategory': 'test'
}]


def assert_experiment(experiment, load=True):
    assert isinstance(experiment, Experiment)

    assert experiment.id is not None
    assert experiment.meta is not None
    assert experiment.parents is not None
    assert experiment.files is not None
    assert experiment.metaCategory is not None

    assert experiment.started_timestamp is not None
    assert experiment.ended_timestamp is not None

    assert len(experiment.parents) == 1
    assert len(experiment.files) == 2

    if load:
        file1 = experiment.get_file('disapproval.jpg')
        file2 = experiment.get_file('text_text.txt')

        assert isinstance(file1, BufferedReader)
        assert isinstance(file2, BufferedReader)

    file_info1 = experiment.get_file_info('disapproval.jpg')
    file_info2 = experiment.get_file_info('text_text.txt')

    assert 'error' not in file_info1, file_info1['error']
    assert file_info1['filename'] == 'disapproval.jpg'
    assert file_info1['caption'] == 'Poppy disapproves of this nonsense'
    assert file_info1['location'] is not None
    assert file_info1['contentType'] == 'image/jpeg'
    assert file_info1['success']

    assert 'error' not in file_info2, file_info2['error']
    assert file_info2['filename'] == 'text_text.txt'
    assert file_info2['caption'] == 'This text file contains text'
    assert file_info2['location'] is not None
    assert file_info2['contentType'] == 'text/plain'
    assert file_info2['success']


def run(mr):
    """
    Save and experiment and then load it and check that the load and save give back consistent results
    """

    # SAVE
    save_result = mr.save('test_category', meta, parents=parents, files=files, keep_originals=True)
    assert_experiment(save_result, load=False)

    # LOAD
    loaded_experiment = mr.load(save_result.id, 'test_category', lazy_file_download=True)
    assert_experiment(loaded_experiment)

    return loaded_experiment


def test_save_and_load_no_config():
    """
    If there is no config file loaded, moderage will use the local cache to store using tinydb
    """
    run(ModeRage())


def test_save_and_load_local():
    """
    We have a config that tells us to use a different local cache directory, but still cache locally
    """
    run(ModeRage('./tests/local_mrconfig.yml'))


def test_save_and_load_server():
    """
    We set up a moderage server connection and cache (test not work if there is no moderage server started on localhost 8118
    """
    run(ModeRage('./tests/server_mrconfig.yml'))


def test_save_with_git():
    """
    Local server that automatically commits and tags for this particular experiment,
    A tag should also be created on save.
    """
    loaded_experiment = run(ModeRage('./tests/local_mrconfig_git.yml'))

    assert loaded_experiment.git_tag is not None
