from models import SongNode, PlaylistNode

class MusicLibrary:
    def __init__(self):
        self.head = None
        self.tail = None
        self.song_count = 0

    def is_duplicate(self, song):
        """
        Check if song already exists in library.
        Returns (True, reason) if duplicate, (False, None) if not.
        """
        current = self.head
        while current:
            # Check by ID
            if current.data.id == song.id:
                return (True, f"Song with ID {song.id} already exists")
            
            # Check by title + artist (case-insensitive)
            if (current.data.title.lower() == song.title.lower() and 
                current.data.artist.lower() == song.artist.lower()):
                return (True, f"Song '{song.title}' by '{song.artist}' already exists")
            
            current = current.next
        
        return (False, None)
    
    def add_song(self, song):
        """
        Add song to library if not duplicate.
        Returns (True, "Success") if added, (False, reason) if duplicate.
        """
        # Check for duplicates
        is_dup, reason = self.is_duplicate(song)
        if is_dup:
            return (False, reason)
        
        # Add song
        new_node = SongNode(song)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.song_count += 1
        return (True, "Song added successfully")

    def delete_song(self, id):
        if not self.head:
            return False

        current = self.head
        while current:
            if current.data.id == id:
                if current == self.head and current == self.tail:
                    self.head = self.tail = None
                elif current == self.head:
                    self.head = self.head.next
                    self.head.prev = None
                elif current == self.tail:
                    self.tail = self.tail.prev
                    self.tail.next = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                
                self.song_count -= 1
                return True
            current = current.next
        return False

    def update_song(self, id, new_details):
        node = self.get_song_by_id(id)
        if node:
            node.data = new_details
            return True
        return False

    def search_song(self, keyword):
        current = self.head
        keyword = keyword.lower()
        while current:
            if keyword in current.data.title.lower() or keyword in current.data.artist.lower():
                return current
            current = current.next
        return None

    def get_song_by_id(self, id):
        current = self.head
        while current:
            if current.data.id == id:
                return current
            current = current.next
        return None

    def get_all_songs(self):
        songs = []
        current = self.head
        while current:
            songs.append(current.data)
            current = current.next
        return songs

    def find_next_similar(self, current_node):
        if not current_node:
            return self.head
        
        # 1. Try to find same artist forward
        temp = current_node.next
        while temp:
            if temp.data.artist == current_node.data.artist:
                return temp
            temp = temp.next
            
        # 2. Try to find same genre forward
        temp = current_node.next
        while temp:
            if temp.data.genre == current_node.data.genre:
                return temp
            temp = temp.next
            
        # 3. Fallback to next song
        if current_node.next:
            return current_node.next
            
        # 4. Loop to head?
        return self.head
    
    def find_prev_similar(self, current_node):
        """
        Find previous similar song based on priority:
        1. Same artist (backward traversal)
        2. Same genre (backward traversal)
        3. Fallback to previous node
        4. If at head, loop to tail
        
        Symmetric to find_next_similar but traverses backward.
        """
        if not current_node:
            return self.tail
        
        # 1. Try to find same artist backward
        temp = current_node.prev
        while temp:
            if temp.data.artist == current_node.data.artist:
                return temp
            temp = temp.prev
            
        # 2. Try to find same genre backward
        temp = current_node.prev
        while temp:
            if temp.data.genre == current_node.data.genre:
                return temp
            temp = temp.prev
            
        # 3. Fallback to previous song
        if current_node.prev:
            return current_node.prev
            
        # 4. Loop to tail if at head
        return self.tail

class Playlist:
    def __init__(self, name):
        self.name = name
        self.head = None
        self.tail = None

    def add_song(self, song):
        new_node = PlaylistNode(song)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def remove_song(self, song_id):
        if not self.head:
            return False

        if self.head.data.id == song_id:
            self.head = self.head.next
            if not self.head:
                self.tail = None
            return True

        current = self.head
        while current.next:
            if current.next.data.id == song_id:
                current.next = current.next.next
                if not current.next:
                    self.tail = current
                return True
            current = current.next
        return False

    def get_songs(self):
        songs = []
        current = self.head
        while current:
            songs.append(current.data)
            current = current.next
        return songs

    def update_song_in_playlist(self, id, new_details):
        current = self.head
        while current:
            if current.data.id == id:
                current.data = new_details
            current = current.next

    def remove_song_by_library_id(self, id):
        # Remove all occurrences
        while self.head and self.head.data.id == id:
            self.head = self.head.next
        
        if not self.head:
            self.tail = None
            return

        current = self.head
        while current.next:
            if current.next.data.id == id:
                current.next = current.next.next
                if not current.next:
                    self.tail = current
            else:
                current = current.next
