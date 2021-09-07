from tracardi_dot_notation.dict_traverser import DictTraverser
from tracardi_dot_notation.dot_accessor import DotAccessor


def test_dot_traverser():
    template = {
        "x": {
            "a": "session@...",
            "b": {"x": [1]},
            "c": [111, 222, "profile@a"],
            "d": {"q": {"z": 11, "e": 22}}
        }
    }

    dot = DotAccessor(profile={"a": [1, 2], "b": [1, 2]}, session={"b": 2}, event={})
    t = DictTraverser(dot)
    result = t.reshape(reshape_template=template)

    assert result['x']['a'] == {'b': 2}
    assert result['x']['b'] == {'x': [1]}
    assert result['x']['c'] == [111, 222, [1, 2]]
    assert result['x']['d'] == {"q": {"z": 11, "e": 22}}
