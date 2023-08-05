from moderage import ModeRage
from moderage.experiment import Experiment

parent_meta = {
    'parent': 'blah',
}

parent_files = [
    {
        'filename': 'examples/disapproval.jpg',
        'caption': 'Poppy disapproves of this nonsense'
    },
    {
        'filename': 'examples/test.txt',
        'caption': 'This text file contains text'
    }
]

meta = {
    'some_thing': 'on the bridge'
}

def run(mr):

    # Create 10 parents
    parents = []
    for i in range(0, 10):
        parent_experiment = mr.save('test_parent', meta)
        parents.append({'metaCategory': 'test_parent', 'id': parent_experiment.id})

    experiment = mr.save('test_with_parents', meta, parents=parents, keep_originals=True)

    loaded_experiment = mr.load(experiment.id, 'test_with_parents')

    loaded_parents = loaded_experiment.load_parents()

    for parent in loaded_parents:
        assert isinstance(parent, Experiment)

    # Create 10 more parents
    moreParents = []
    for i in range(0, 10):
        parent_experiment = mr.save('test_parent', meta)
        moreParents.append({'metaCategory': 'test_parent', 'id': parent_experiment.id})

    experiment.add_parents(moreParents)

    assert experiment.parents == (parents + moreParents)

def test_with_parents_local():
    mr = ModeRage()
    assert mr._mode == 'local'
    run(mr)

def test_with_parents_server():
    mr = ModeRage('./tests/server_mrconfig.yml')
    assert mr._mode == 'server'
    run(mr)
