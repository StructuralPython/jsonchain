from jsonchain import load_json, dump_json, extract_keys, flatten_tree
import pathlib

here = pathlib.Path.cwd()
if here.name != "tests" and here.name == "jsonchain":
    here = here / "tests"


def test_load_json():
    a_dict = load_json(here / "a.json")
    assert a_dict['aa'] == 1
    assert a_dict['ab'] == 2
    assert a_dict['bc'] == 3


def test_extract_keys():
    a_dict = load_json(here / "a.json")
    loks = extract_keys(a_dict, key_name="group")
    assert loks == [
        {"group": "aa"},
        {"group": "ab"},
        {"group": "bc"}
    ]
    loks_a = extract_keys(a_dict, key_name="group", include_startswith="a")
    assert loks_a == [
        {"group": "aa"},
        {"group": "ab"}
    ]
    loks_b = extract_keys(a_dict, key_name="group", exclude_startswith="b")
    assert loks_b == [
        {"group": "aa"},
        {"group": "ab"},
    ]
    

def test_flatten_tree():
    tree = {
        "a": {
            "A": {
                1: {
                    "opta": 1,
                    "optb": 2,
                    "optc": 3,
                },
                2: {
                    "opta": 10,
                    "optb": 20,
                    "optc": 30,
                },
            },
            "B": {
                1: {
                    "opta": 21,
                    "optb": 22,
                    "optc": 23,
                },
                2: {
                    "opta": 210,
                    "optb": 220,
                    "optc": 230,
                }
            },
            "C": {
                1: {
                    "opta": 31,
                    "optb": 32,
                    "optc": 33,
                },
                2: {
                    "opta": 310,
                    "optb": 320,
                    "optc": 330,
                }
            }
        }
    }
    flat = [
        {"member": "a", "force": "A", "case": 1, "opta": 1, "optb": 2, "optc": 3},
        {"member": "a", "force": "A", "case": 2, "opta": 10, "optb": 20, "optc": 30},
        {"member": "a", "force": "B", "case": 1, "opta": 21, "optb": 22, "optc": 23},
        {"member": "a", "force": "B", "case": 2, "opta": 210, "optb": 220, "optc": 230},
        {"member": "a", "force": "C", "case": 1, "opta": 31, "optb": 32, "optc": 33},
        {"member": "a", "force": "C", "case": 2, "opta": 310, "optb": 320, "optc": 330},
    ]
    flattened = flatten_tree(tree, level_labels=['member', 'force', 'case'])
    assert flattened == flat