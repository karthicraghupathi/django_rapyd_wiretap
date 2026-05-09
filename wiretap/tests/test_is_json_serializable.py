from datetime import datetime

from wiretap.middleware import is_json_serializable


def test_string():
    assert is_json_serializable("hello") is True


def test_integer():
    assert is_json_serializable(42) is True


def test_float():
    assert is_json_serializable(3.14) is True


def test_none():
    assert is_json_serializable(None) is True


def test_list():
    assert is_json_serializable([1, 2, 3]) is True


def test_dict():
    assert is_json_serializable({"key": "value"}) is True


def test_set_not_serializable():
    assert is_json_serializable({1, 2, 3}) is False


def test_datetime_not_serializable():
    assert is_json_serializable(datetime.now()) is False


def test_custom_object_not_serializable():
    class Unserializable:
        pass

    assert is_json_serializable(Unserializable()) is False
