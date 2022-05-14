from typing import List, Callable, Type, Any

from easysql.EasySQLDriver import EasySQLDriver
from easysql.EasyStruct import EasyStruct


class EasySQL:
    _driver: EasySQLDriver

    def __init__(self, driver: EasySQLDriver, types: List[Type[EasyStruct]]):
        self._driver = driver
        # table init
        self._driver.init_tables(types)

        # data method init
        for typ in types:
            typname = typ.__name__
            # creator
            setattr(self, "create_" + typname.lower(), self._create_func_factory(typ))
            # getter
            setattr(self, "get_" + typname.lower(), self._get_func_factory(typ))
            # updater
            setattr(self, "update_" + typname.lower(), self._update_func_factory(typ))
            # deleter
            setattr(self, "delete_" + typname.lower(), self._delete_func_factory(typ))

    def _create_func_factory(self, t: Type[EasyStruct]) -> Callable[[EasyStruct, Any], None]:
        def creator(obj: t, self=self):
            table = t.__name__.lower()
            sql = f"INSERT INTO {table} ({', '.join(a.lstrip('_') for a in t.get_non_relational_attrs())}) " \
                  f"VALUES ({', '.join(['%s'] * len(t.get_non_relational_attrs()))})"
            args = [getattr(obj, 'get_' + a.lstrip('_'))() for a in t.get_non_relational_attrs()]
            self._driver.execute_modification(sql, args)

        return creator

    def _update_func_factory(self, t: Type[EasyStruct]) -> Callable[[EasyStruct, Any], None]:
        def updater(obj: t, self=self):
            table = t.__name__.lower()
            sql = f"UPDATE {table} SET (" + \
                  ', '.join([f"{a.lstrip('_')} = %s" for a in t.get_non_relational_attrs() if a != '_id']) + \
                  f" WHERE id = %s"
            args = [getattr(obj, 'get_' + a.lstrip('_'))() for a in t.get_non_relational_attrs() if a != '_id'] + \
                   [obj.get_id()]
            self._driver.execute_modification(sql, args)

        return updater

    def _delete_func_factory(self, t: Type[EasyStruct]) -> Callable[[EasyStruct, Any], None]:
        def deleter(obj: t, self=self):
            table = t.__name__.lower()
            sql = f"DELETE FROM {table} WHERE id = %s"
            args = [obj.get_id()]
            self._driver.execute_modification(sql, args)

        return deleter

    def _get_func_factory(self, t: Type[EasyStruct]) -> Callable[[Any, Any], EasyStruct]:
        def getter(id_: Any, self=self):
            table = t.__name__.lower()
            sql = f"SELECT * FROM {table} WHERE id = %s"
            args = [id_]
            for raw in self._driver.execute_query(sql, args):
                return t(**{a: raw[i] for i, a in enumerate(t.get_non_relational_attrs())})

        return getter
