from storage import MusicLibrary, Playlist
from models import Song
from audio_player import AudioPlayer
from database import Database

class AppController:
    def __init__(self):
        self.library, loaded = Database.load_library()
        if not loaded or self.library.song_count == 0:
            self._seed_data()
            Database.save_library(self.library)
            
        self.user_playlists = Database.load_playlists(self.library)
        self.player = AudioPlayer(self.library)

    def _seed_data(self):
        self.library.add_song(Song(1, "Bohemian Rhapsody", "Queen", "Rock", "A Night at the Opera", 1975, "", ""))
        self.library.add_song(Song(2, "Shape of You", "Ed Sheeran", "Pop", "Divide", 2017, "", ""))
        self.library.add_song(Song(3, "Hotel California", "Eagles", "Rock", "Hotel California", 1976, "", ""))
        self.library.add_song(Song(4, "Blinding Lights", "The Weeknd", "Pop", "After Hours", 2020, "", ""))
        self.library.add_song(Song(5, "Don't Stop Me Now", "Queen", "Rock", "Jazz", 1978, "", ""))

    # Admin Actions
    def add_song(self, id, title, artist, genre, album, year, audio_path="", image_path=""):
        """
        Add song to library with validation.
        Returns (success: bool, message: str)
        """
        success, message = self.library.add_song(
            Song(id, title, artist, genre, album, year, audio_path, image_path)
        )
        if success:
            Database.save_library(self.library)
        return (success, message)

    def get_all_songs(self):
        return self.library.get_all_songs()

    def get_liked_songs(self):
        """Returns a list of all songs where is_favorite=True"""
        all_songs = self.library.get_all_songs()
        return [song for song in all_songs if song.is_favorite]

    def get_song(self, id):
        return self.library.get_song_by_id(id)

    def update_song(self, id, new_song_data):
        success = self.library.update_song(id, new_song_data)
        if success:
            for p in self.user_playlists:
                p.update_song_in_playlist(id, new_song_data)
            Database.save_library(self.library)
            Database.save_playlists(self.user_playlists) # Playlists might have name/artist updates
        return success

    def delete_song(self, id):
        success = self.library.delete_song(id)
        if success:
            for p in self.user_playlists:
                p.remove_song_by_library_id(id)
            Database.save_library(self.library)
            Database.save_playlists(self.user_playlists)
        return success

    # User Actions
    def search_song(self, keyword):
        return self.library.search_song(keyword)

    def create_playlist(self, name):
        self.user_playlists.append(Playlist(name))
        Database.save_playlists(self.user_playlists)

    def get_playlists(self):
        return self.user_playlists

    def add_to_playlist(self, playlist_idx, song_id):
        if 0 <= playlist_idx < len(self.user_playlists):
            song_node = self.library.get_song_by_id(song_id)
            if song_node:
                self.user_playlists[playlist_idx].add_song(song_node.data)
                Database.save_playlists(self.user_playlists)
                return True, "Added."
            return False, "Song ID not found."
        return False, "Invalid playlist."

    def remove_from_playlist(self, playlist_idx, song_id):
        if 0 <= playlist_idx < len(self.user_playlists):
            success = self.user_playlists[playlist_idx].remove_song(song_id)
            if success:
                Database.save_playlists(self.user_playlists)
            return success, "Removed." if success else "Song not found in playlist."
        return False, "Invalid playlist."

    def play_playlist(self, playlist_idx):
        if 0 <= playlist_idx < len(self.user_playlists):
            p = self.user_playlists[playlist_idx]
            if p.head:
                song_node = self.library.get_song_by_id(p.head.data.id)
                if song_node:
                    return self.player.play(song_node, p)
            return False, "Playlist is empty."
        return False, "Invalid playlist."

    def play_song_node(self, node):
        return self.player.play(node, None)

    def play_song_id(self, song_id):
        node = self.library.get_song_by_id(song_id)
        if node:
             return self.player.play(node)
        return False, "Song not found"

    # Player Controls
    def stop_music(self):
        return self.player.stop()

    def next_song(self):
        return self.player.next()

    def prev_song(self):
        return self.player.prev()

    def get_player_state(self):
        return {
            "is_playing": self.player.is_playing,
            "current_song": self.player.current_song
        }
