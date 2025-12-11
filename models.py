class Song:
    def __init__(self, id, title, artist, genre, album, year, audio_path="", image_path="", is_favorite=False):
        self.id = id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.album = album
        self.year = year
        self.audio_path = audio_path
        self.image_path = image_path
        self.is_favorite = is_favorite

    def __str__(self):
        return f"{self.title} - {self.artist}"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "album": self.album,
            "year": self.year,
            "audio_path": self.audio_path,
            "image_path": self.image_path,
            "is_favorite": self.is_favorite
        }

    @staticmethod
    def from_dict(data):
        return Song(
            data["id"],
            data["title"],
            data["artist"],
            data["genre"],
            data["album"],
            data["year"],
            data.get("audio_path", ""),
            data.get("image_path", ""),
            data.get("is_favorite", False)
        )

class SongNode:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class PlaylistNode:
    def __init__(self, data):
        self.data = data
        self.next = None
