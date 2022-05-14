import sqlite3
from inspect import getmembers
from typing import List, Type, Any, Iterator
from uuid import UUID

from easysql.EasyStruct import EasyStruct
from easysql.EasySQLDriver import EasySQLDriver


class SQLite(EasySQLDriver):
    _PLACEHOLDER = "?"

    def __init__(self, location: str):
        super().__init__(location)
        self._location = location

    def get_cursor(self) -> sqlite3.Cursor:
        with sqlite3.connect(self._location) as con:
            return con.cursor()

    @staticmethod
    def _init_table(cur: sqlite3.Cursor, typ: Type[EasyStruct]):
        members = getmembers(typ)
        attributes = {k: v for k, v in members[0][1].items() if not k[:3] == '___'}

        cols = []
        for k, v in attributes.items():
            col = k.lstrip('_') + ' '
            if v == str:
                col += "TEXT"
            elif v == UUID:
                col += "UUID"
            elif v == int:
                col += "REAL"
            cols.append(col)

        sql_ = f"CREATE TABLE IF NOT EXISTS {typ.__name__.lower()} ({', '.join(cols)})"
        cur.execute(sql_, [])

    def init_tables(self, types: List[Type[EasyStruct]]):
        cur = self.get_cursor()
        for t in types:
            self._init_table(cur, t)

    def execute_modification(self, sql_: str, args: List[Any]):
        sql_ = self._preprocess_sql(sql_)
        cur = self.get_cursor()
        cur.execute(sql_, args)

    def execute_query(self, sql_: str, args: List[Any]) -> Iterator[Any]:
        sql_ = self._preprocess_sql(sql_)
        cur = self.get_cursor()
        for raw in cur.execute(sql_, args):
            yield raw

