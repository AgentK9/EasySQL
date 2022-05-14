from typing import Protocol, Dict, Optional, Type, List, Any

from easysql.EasyStruct import EasyStruct


class EasySQLDriver(Protocol):
    _PLACEHOLDER: str  # the placeholder used by the database dialect

    def __init__(self, location: str, creds: Optional[Dict] = None):
        """ do initialization here (check the connection to the db, etc) """
        raise NotImplementedError(f"{type(self).__name__}.__init__ is not implemented")

    def init_tables(self, types: List[Type[EasyStruct]]):
        """ initialize tables
        (Note: this should handle if it is run multiple times, and potentially if some tables already exist) """
        raise NotImplementedError(f"{type(self).__name__}.init_tables is not implemented")

    def execute_modification(self, sql_: str, args: List[Any]):
        """ execute a modification on the database. Modifications DO NOT return anything. """
        raise NotImplementedError(f"{type(self).__name__}.execute_modification is not implemented")

    def execute_query(self, sql_: str, args: List[Any]) -> Any:  # TODO: typecast return type
        """ execute a query on the database. Queries DO return data. """
        raise NotImplementedError(f"{type(self).__name__}.execute_query is not implemented")

    @classmethod
    def _preprocess_sql(cls, sql_: str) -> str:
        return sql_.replace("%s", cls._PLACEHOLDER)
