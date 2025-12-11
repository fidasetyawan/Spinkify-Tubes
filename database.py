import json
import os
from models import Song
from storage import MusicLibrary, Playlist

class Database:
    @staticmethod
    def save_library(library, filename="library.json"):
        data = []
        current = library.head
        while current:
            data.append(current.data.to_dict())
            current = current.next
        
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving library: {e}")
            return False

    @staticmethod
    def load_library(filename="library.json"):
        library = MusicLibrary()
        if not os.path.exists(filename):
            return library, False # Empty library, file not found
            
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    song = Song.from_dict(item)
                    library.add_song(song)
            return library, True
        except Exception as e:
            print(f"Error loading library: {e}")
            return library, False

    @staticmethod
    def save_playlists(playlists, filename="playlists.json"):
        data = []
        for p in playlists:
            p_data = {
                "name": p.name,
                "songs": [s.id for s in p.get_songs()] # Store just IDs
            }
            data.append(p_data)
            
        try:
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving playlists: {e}")
            return False

    @staticmethod
    def load_playlists(library, filename="playlists.json"):
        playlists = []
        if not os.path.exists(filename):
            return playlists
            
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                for item in data:
                    p = Playlist(item["name"])
                    for song_id in item["songs"]:
                        node = library.get_song_by_id(song_id)
                        if node:
                            p.add_song(node.data)
                    playlists.append(p)
            return playlists
        except Exception as e:
            print(f"Error loading playlists: {e}")
            return []
