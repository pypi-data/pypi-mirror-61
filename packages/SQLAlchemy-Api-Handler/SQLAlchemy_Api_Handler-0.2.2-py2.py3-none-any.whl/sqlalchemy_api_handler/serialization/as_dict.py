from collections import OrderedDict
from functools import singledispatch
from typing import Iterable, Set, List
from sqlalchemy.orm.collections import InstrumentedList

from sqlalchemy_api_handler.api_handler import ApiHandler
from sqlalchemy_api_handler.serialization.serialize import serialize

@singledispatch
def as_dict(value, column=None, includes: Iterable = ()):
    return serialize(value, column=column)

@as_dict.register(InstrumentedList)
def as_dict_for_intrumented_list(objs, column=None, includes: Iterable = ()):
    not_deleted_objs = filter(lambda x: not x.is_soft_deleted(), objs)
    return [as_dict(obj, includes=includes) for obj in not_deleted_objs]

@as_dict.register(ApiHandler)
def as_dict_for_api_handler(obj, column=None, includes: Iterable = None):
    result = OrderedDict()

    if includes is None:
        if hasattr(obj.__class__, '__as_dict_includes__'):
            includes = obj.__class__.__as_dict_includes__
        else:
            includes = ()

    for key in _keys_to_serialize(obj, includes):
        value = getattr(obj, key)
        columns = obj.__table__.columns._data
        column = columns.get(key)
        result[key] = as_dict(value, column=column)

    for join in _joins_to_serialize(includes):
        key = join['key']
        sub_includes = join.get('includes', set())
        value = getattr(obj, key)
        result[key] = as_dict(value, includes=sub_includes)

    return result

def _joins_to_serialize(includes: Iterable) -> List[dict]:
    dict_joins = filter(lambda a: isinstance(a, dict), includes)
    return list(dict_joins)


def _keys_to_serialize(obj, includes: Iterable) -> Set[str]:
    obj_attributes = obj.__mapper__.c.keys()
    return set(obj_attributes).union(_included_properties(includes)) - _excluded_keys(includes)


def _included_properties(includes: Iterable) -> Set[str]:
    string_keys = filter(lambda a: isinstance(a, str), includes)
    included_keys = filter(lambda a: not a.startswith('-'), string_keys)
    return set(included_keys)


def _excluded_keys(includes):
    string_keys = filter(lambda a: isinstance(a, str), includes)
    excluded_keys = filter(lambda a: a.startswith('-'), string_keys)
    cleaned_keys = map(lambda a: a[1:], excluded_keys)
    return set(cleaned_keys)
