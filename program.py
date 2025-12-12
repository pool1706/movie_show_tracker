import datetime

# ==========================================
# 1. DECORATORS & CLOSURES (Advanced Concepts)
# ==========================================

# [DECORATOR] - Used to automatically print a log message when a function runs
def log_activity(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n[LOG {timestamp}] Running action: {func.__name__}...")
        result = func(*args, **kwargs)
        print("[LOG] Action complete.")
        return result
    return wrapper

# [CLOSURE] - A function that builds a custom filter function
# You call it like: my_filter = make_genre_filter("Sci-Fi")
# Then use my_filter(movie) to check if it matches.
def make_genre_filter(target_genre):
    def filter_func(entry):
        # This inner function "remembers" target_genre from the outer function
        return entry.genre.lower() == target_genre.lower()
    return filter_func


# ==========================================
# 2. THE BLUEPRINTS (Classes & Inheritance)
# ==========================================

# [PARENT CLASS] - Holds data shared by both Movies and Series
class MediaEntry:
    # [CLASS VARIABLE] - Shared by ALL instances to count total items
    total_entries = 0

    def __init__(self, title, genre, rating, review_text):
        self.title = title
        self.genre = genre
        self.review_text = review_text
        # We assign to self.rating, which triggers the Property Setter below
        self.rating = rating 
        
        MediaEntry.total_entries += 1

    # [PROPERTY] - The "Bouncer" that guards the rating
    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not (0 <= value <= 10):
            raise ValueError(f"Rating for '{self.title}' must be between 0 and 10!")
        self._rating = value

    # [DUNDER METHOD] - String representation for users
    def __str__(self):
        return f"[{self.rating}/10] {self.title} ({self.genre})"

    # [DUNDER METHOD] - String representation for developers/debugging
    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.title}>"


# [CHILD CLASS] - Inherits from MediaEntry
class MovieEntry(MediaEntry):
    def __init__(self, title, genre, rating, review_text):
        super().__init__(title, genre, rating, review_text)
        # Movies don't need extra data, so __init__ is simple

    def __str__(self):
        return f"🎬 MOVIE:  {super().__str__()}"


# [CHILD CLASS] - Inherits from MediaEntry but adds Season/Episode
class SeriesEntry(MediaEntry):
    def __init__(self, title, genre, rating, review_text, season, episode=None):
        super().__init__(title, genre, rating, review_text)
        self.season = season
        self.episode = episode

    def __str__(self):
        base_str = super().__str__()
        if self.episode:
            return f"📺 SERIES: {base_str} - S{self.season} E{self.episode}"
        return f"📺 SERIES: {base_str} - Season {self.season} Review"


# ==========================================
# 3. THE MANAGER (The Logbook System)
# ==========================================

class MediaLogbook:
    def __init__(self):
        # The list that holds all objects
        self.entries = []

    # [DECORATOR USE] - We tag this method so it logs automatically
    @log_activity
    def add_entry(self, entry_object):
        self.entries.append(entry_object)
        print(f"Successfully added: {entry_object.title}")

    def find_entry_index(self, title_to_find):
        """Helper function to find the index 'n' of a movie."""
        for n in range(len(self.entries)):
            if self.entries[n].title.lower() == title_to_find.lower():
                return n
        return -1 # Not found

    @log_activity
    def edit_entry(self, title):
        index = self.find_entry_index(title)
        
        if index == -1:
            print(f"❌ Could not find '{title}' in your logbook.")
            return

        entry = self.entries[index]
        print(f"Found: {entry}")
        print("What would you like to update?")
        print("1. Rating")
        print("2. Review Text")
        
        choice = input("Choice: ")
        
        if choice == "1":
            try:
                new_rating = float(input("New Rating (0-10): "))
                # This automatically calls the @property setter "Bouncer" again!
                entry.rating = new_rating 
                print("✅ Rating updated!")
            except ValueError as e:
                print(f"❌ Error: {e}")
        
        elif choice == "2":
            new_text = input("New Review: ")
            entry.review_text = new_text
            print("✅ Review updated!")

    def show_all(self):
        print(f"\n--- YOUR LOGBOOK ({MediaEntry.total_entries} Total) ---")
        if not self.entries:
            print("Logbook is empty.")
        else:
            for entry in self.entries:
                print(entry) # Calls __str__ automatically
        print("-----------------------------------")

    def filter_by_genre(self, genre):
        print(f"\n--- Searching for {genre} ---")
        # [CLOSURE USE] - Create a custom filter function for this genre
        my_filter = make_genre_filter(genre)
        
        found = False
        for entry in self.entries:
            # We use the closure function here
            if my_filter(entry): 
                print(entry)
                found = True
        
        if not found:
            print("No matches found.")


# ==========================================
# 4. MAIN PROGRAM LOOP
# ==========================================

if __name__ == "__main__":
    logbook = MediaLogbook()

    while True:
        print("\n=== 🎥 MY WATCH LOG ===")
        print("1. Add Movie")
        print("2. Add Series/Episode")
        print("3. View All")
        print("4. Edit an Entry")
        print("5. Filter by Genre")
        print("q. Quit")
        
        choice = input("Select: ")

        if choice == "1":
            try:
                t = input("Title: ")
                g = input("Genre: ")
                r = float(input("Rating (0-10): "))
                txt = input("Review: ")
                # Create Instance
                m = MovieEntry(t, g, r, txt)
                # Add to logbook
                logbook.add_entry(m)
            except ValueError as e:
                print(f"❌ Failed to add: {e}")

        elif choice == "2":
            try:
                t = input("Title: ")
                g = input("Genre: ")
                r = float(input("Rating (0-10): "))
                txt = input("Review: ")
                s = input("Season #: ")
                e_num = input("Episode # (Enter to skip): ")
                
                # Create Instance (Handle optional episode)
                if e_num.strip() == "":
                    s_entry = SeriesEntry(t, g, r, txt, s)
                else:
                    s_entry = SeriesEntry(t, g, r, txt, s, e_num)
                
                logbook.add_entry(s_entry)
            except ValueError as e:
                print(f"❌ Failed to add: {e}")

        elif choice == "3":
            logbook.show_all()

        elif choice == "4":
            search_title = input("Enter title to edit: ")
            logbook.edit_entry(search_title)

        elif choice == "5":
            g = input("Enter genre to search (e.g., Sci-Fi): ")
            logbook.filter_by_genre(g)

        elif choice == "q":
            print("Goodbye!")
            break