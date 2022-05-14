from typing import Set
from uuid import UUID

from easysql.EasyStruct import EasyStruct
from easysql.EasySQL import EasySQL
from easysql.drivers.SQLite import SQLite


class Artist(EasyStruct):
    _id: UUID
    _name: str
    _albums: Set[UUID]


class Album(EasyStruct):
    _id: UUID
    _name: str
    _artist: UUID
    _songs: Set[UUID]


class Song(EasyStruct):
    _id: UUID
    _name: str
    _album: UUID
    _runtime: int


DRIVER = SQLite(location="identifier.sqlite")  # creds as well

db = EasySQL(driver=DRIVER, types=[Artist, Album, Song])

# diag = db.EERDiagram()

artist = Artist("Sigrid", {})
db.create_artist(artist)

album = Album("How To Let Go", artist.get_id(), {})
db.create_album(album)
artist = db.get_artist(artist.get_id())

songs = [Song("Grow", album.get_id(), 193),
         Song("It Gets Dark", album.get_id(), 206)]
for song in songs:
    db.create_song(song)

album = db.get_album(album.get_id())
# also update stuff
