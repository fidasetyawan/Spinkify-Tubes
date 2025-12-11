import pygame
import os

class AudioPlayer:
    def __init__(self, library):
        self.library = library
        self.current_song = None
        self.is_playing = False
        self.current_playlist_context = None # If playing from playlist
        
        # Initialize Pygame Mixer
        try:
            pygame.mixer.init()
        except Exception as e:
            print(f"Error initializing mixer: {e}")

    def play(self, song_node, context=None):
        if not song_node: return False, "No song provided."
        
        # Stop current if playing
        if self.is_playing:
            self.stop()

        self.current_song = song_node
        self.current_playlist_context = context
        
        audio_path = song_node.data.audio_path
        if audio_path and os.path.exists(audio_path):
            try:
                pygame.mixer.music.load(audio_path)
                pygame.mixer.music.play()
                self.is_playing = True
                return True, "Playing."
            except Exception as e:
                print(f"Error playing audio: {e}")
                self.is_playing = False
                return False, f"Error: {e}"
        else:
            # Fallback for UI simulation only if no path
            self.is_playing = True 
            return False, "Audio file not found. Playing in demo mode."

    def stop(self):
        if self.is_playing:
            try:
                pygame.mixer.music.stop()
            except: pass
            self.is_playing = False
            return True
        return False

    def next(self):
        if not self.current_song:
            return None, "No song selected."

        if self.current_playlist_context:
            # Playlist Context
            p_node = self.current_playlist_context.head
            while p_node:
                if p_node.data.id == self.current_song.data.id:
                    if p_node.next:
                        # Find library node for next song
                        lib_node = self.library.get_song_by_id(p_node.next.data.id)
                        if lib_node:
                            self.play(lib_node, self.current_playlist_context)
                            return lib_node, None
                        else:
                            return None, "Error: Song not found in library."
                    else:
                        return None, "End of playlist."
                p_node = p_node.next
        else:
            # Library Context - Smart Shuffle
            next_node = self.library.find_next_similar(self.current_song)
            if next_node:
                self.play(next_node, None)
                return next_node, None
            else:
                return None, "No similar songs found."
        return None, "Error finding next song."

    def prev(self):
        if not self.current_song:
            return None, "No song selected."

        if self.current_playlist_context:
            # Playlist Context - Prev
            p_node = self.current_playlist_context.head
            prev = None
            while p_node:
                if p_node.data.id == self.current_song.data.id:
                    if prev:
                        lib_node = self.library.get_song_by_id(prev.data.id)
                        if lib_node:
                            self.play(lib_node, self.current_playlist_context)
                            return lib_node, None
                    else:
                        return None, "Start of playlist."
                    return None, "Error."
                prev = p_node
                p_node = p_node.next
        else:
            # Library Context - Smart Prev (symmetric to Smart Next)
            prev_node = self.library.find_prev_similar(self.current_song)
            if prev_node:
                self.play(prev_node, None)
                return prev_node, None
            else:
                return None, "No similar songs found."
        return None, "Error finding prev song."
