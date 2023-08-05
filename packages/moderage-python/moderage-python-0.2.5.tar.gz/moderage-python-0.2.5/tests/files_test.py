from moderage import ModeRage


files1 = [
    {
        'file': 'examples/disapproval.jpg',
        'filename': 'poppy.jpg',
        'caption': 'Poppy disapproves of this nonsense'
    },
    {
        'filename': 'examples/test.txt',
        'caption': 'This text file contains text'
    }
]

files2 = [
    {
        'file': 'examples/disapproval2.jpg',
        'filename': 'disapproval_2.jpg',
        'caption': 'Poppy disapproves of this nonsense2'
    },
    {
        'filename': 'examples/test2.txt',
        'caption': 'This text file contains text2'
    }
]

meta = {
    'some_thing': 'on the bridge'
}

def run(mr):

    experiment = mr.save('test_with_files', meta, files=files1, keep_originals=True)

    assert len(experiment.files) == 2

    experiment.add_files(files2, keep_originals=True)

    assert len(experiment.files) == 4

def test_with_files_local():
    mr = ModeRage()
    assert mr._mode == 'local'
    run(mr)

def test_with_files_server():
    mr = ModeRage('./tests/server_mrconfig.yml')
    assert mr._mode == 'server'
    run(mr)

def test_with_files_server_config_dict():

    config_dict = {
        'mode': 'server',
        'cache_location': '~/.moderage',
        'server': {
            'host': 'http://localhost',
            'port': 8118
        }
    }

    mr = ModeRage(config_data=config_dict)
    assert mr._mode == 'server'
    run(mr)