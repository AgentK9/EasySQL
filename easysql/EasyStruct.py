from inspect import getmembers
from typing import List, Any
from uuid import uuid4, UUID


class EasyStruct(object):
    _id: Any

    def __init__(self, *args, **kwargs):
        members = getmembers(self)
        sub_attributes = {k: v for k, v in members[0][1].items() if not k[:3] == '___'}
        # anything with three underscores ('___') is an attr of this superclass, and not what we want
        # TODO: relational attributes

        # id initialization
        if '_id' not in sub_attributes.keys():  # TODO: non-permission-controlled attributes?
            raise AttributeError("No _id attribute")
        if 'id' in kwargs.keys():
            self._id = kwargs["id"]
        else:
            if sub_attributes['_id'] == UUID:
                self._id = uuid4()  # TODO: other id types
            else:
                raise AttributeError("No id provided")
                # TODO: able to provide id generation for non-uuids (and overloads?)

        # attribute initialization
        attr_num = 0
        non_id_attrs = list(sub_attributes.keys())
        non_id_attrs.remove('_id')
        # positional args
        for arg in args:
            # type handling
            if attr_num >= len(non_id_attrs):
                raise AttributeError("Malformed Constructor")
            attr_name = non_id_attrs[attr_num]
            if type(arg) != sub_attributes[attr_name]:
                raise TypeError(f"{self.__name__}.{attr_name} is not of type {sub_attributes[attr_name].__name__}")
            setattr(self, non_id_attrs[attr_num], arg)
            attr_num += 1
        # keyword args
        for key in kwargs.keys():
            if key == 'id':
                continue  # already handled id
            # check that the class definition matches the constructor
            if key not in sub_attributes.keys():
                raise AttributeError("Cannot handle non-defined sub_attributes ")
            # type handling
            if type(kwargs[key]) != sub_attributes[key]:
                raise TypeError(f"{self.__name__}.{key} is not of type {sub_attributes[key].__name__}")
            setattr(self, key, kwargs[key])
            attr_num += 1
        # check that we have the args we need
        if len(non_id_attrs) != attr_num:
            raise AttributeError("Bad sub_attributes passed or malformed class")

        # setter/getter initialization
        # TODO: allow for attributes to be immutable
        # NOTE: keys cannot be private because of how sql works. Maybe look into that in the future?
        immutable = ['_id']  # id is immutable, period
        for key in sub_attributes.keys():
            if key not in immutable:
                # setter
                setattr(self, 'set_' + key.lstrip('_'), lambda a: setattr(self, key, a))
            # getter
            setattr(self, 'get_' + key.lstrip('_'), lambda: getattr(self, key))

    @classmethod
    def get_non_relational_attrs(cls) -> List[str]:
        members = getmembers(cls)
        sub_attributes = {k: v for k, v in members[0][1].items() if not k[:3] == '___'}
        # anything with three underscores ('___') is an attr of this superclass, and not what we want
        return list(sub_attributes.keys())

    def get_id(self) -> Any:
        return self._id
