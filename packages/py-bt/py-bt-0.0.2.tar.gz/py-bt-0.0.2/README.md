# Behaviour Tree

[WIP]

PyPi: https://pypi.org/project/py-bt/

Tree structure made up of Composite and Leaf nodes.

Leaf nodes are where the behaviour happens, for example an "action" or "test".

Composite nodes can be of 2 types:
* Sequence
* Selector

Sequence nodes return the first failed child node. Similar to the ALL operator.

Selector nodes return the first successful child node. Similar to the OR operator.

## Dependencies

Tested on:
* Python 3.8.1
* Python 3.7.5

## Usage

Install:

```bash
pip install py-bt
```

Define a python module for you behaviour tasks (actions & tests). Tasks must return True or False
depending on whether they succeed or fail. Tasks functions receive `data` and `blackboard` args.
`data` is the input data to the tree execution and `blackboard` is a key value store where
information can be shared between nodes. For example:

```python
def choose_food(data, blackboard):
    if data["lunchbox"]:
        blackboard["choice"] = random.choice(data["lunchbox"])
        return True
    return False

def eat(data, blackboard):
    print(f"Eating {blackboard['choice']}")
    return True
```

Then, define your desired tree model in JSON or YAML format. For example:

```json
{
  "type": "sequence",
  "tasks_path": "path.to.tasks.module",
  "children": [
    {
      "task": "choose_food"
    },
    {
      "task": "eat"
    }
  ]
}
```

Then initialise and execute a behaviour tree object with some input data:

```python
from bt.behaviour_tree import BehaviourTree

data = {
    "lunchbox": ["apple", "orange", "pear"]
}

tree = BehaviourTree("/path/to/tree/model.json")
tree.load()

tree.execute(data)
```

## Example Models

Some example models can be found under the `/models` directory.

For example `/models/football/attacker.json` contains a behaviour tree for how a attacking player in a
football simulator might behave.


## Tests

```
pip install -r requirements.txt
pytest
flake8
```

[TODO: CI Build]

[TODO: Docker build]


## Upload to PyPi

```bash
python3 setup.py sdist bdist_wheel
twine upload dist/*
```
