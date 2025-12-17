import datetime

# decorator to log time and action name
def log_activity(func):
    def wrapper(*args, **kwargs):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"\n[LOG {timestamp}] Running action: {func.__name__}...")
        result = func(*args, **kwargs)
        print("[LOG] Action complete.")
        return result
    return wrapper

# closure-based genre filter
def make_genre_filter(target_genre):
    def filter_func(entry):
        return entry.genre.lower() == target_genre.lower()
    return filter_func


class MediaEntry:
    total_entries = 0  # shared counter

    def __init__(self, title, review_text, genre, rating):
        self.title = title
        self.review_text = review_text
        self.genre = genre
        self._rating = None
        self.rating = rating  # goes through setter
        MediaEntry.total_entries += 1

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not (0 <= value <= 10):
            raise ValueError("Invalid rating , rating must be from 0 to 10")
        self._rating = value

    def __str__(self):
        return f"Title :{self.title} | Genre : {self.genre} | Rating : {self.rating}"

    def __repr__(self):
        return f"MovieEntry({self.title} , {self.genre} , {self.rating})"


class MovieEntry(MediaEntry):
    def __init__(self, title, review_text, genre, rating):
        super().__init__(title, review_text, genre, rating)

    def __str__(self):
        return f"MOVIE: {super().__str__()}"


class ShowEntry(MediaEntry):
    def __init__(self, title, genre, rating, show_review=None, episode_number=None, season_number=None, season_review=None, episode_review=None):
        super().__init__(title, None, genre, rating)
        self.show_review = show_review
        self.episode_number = episode_number
        self.season_number = season_number
        self.episode_review = episode_review
        self.season_review = season_review

    def __str__(self):
        base_str = super().__str__()
        if self.episode_number is not None:
            return f"SERIES : {base_str} | SEASON NUMBER : {self.season_number} | EPISODE NUMBER : {self.episode_number}"
        elif self.season_review is not None:
            return f"SERIES : {base_str} | SEASON NUMBER : {self.season_number}"
        return f"SERIES : {base_str}"


class Manager:
    def __init__(self):
        self.entries = []  # stores all media objects

    @log_activity
    def addentry(self, entry):
        self.entries.append(entry)
        print(f"Succesfully added {entry.title}")

    def find_index(self, title_to_find):
        for i in range(len(self.entries)):
            if self.entries[i].title.lower() == title_to_find.lower():
                return i
        return -1

    @log_activity
    def edit_entry(self, title):
        index = self.find_index(title)
        if index == -1:
            print("entered title is invalid")
            return

        entry = self.entries[index]
        print(f" title found :  {entry}")

        k = int(input("ENTER 1 to edit the title \n ENTER 2 to the rating \n ENTER 3 to edit the genre \n ENTER 4 to edit the review text \n "))

        if k == 1:
            entry.title = input("Enter the edit for the title")

        elif k == 2:
            try:
                entry.rating = int(input("Enter the new rating : "))
            except ValueError as e:
                print(f"Error : {e}")

        elif k == 3:
            entry.genre = input("Enter the new genre")

        elif k == 4:
            entry.review_text = input("Enter the new review")

    def showall(self):
        print("------------------------------------")
        print(f"Total {MediaEntry.total_entries} entries")
        if not self.entries:
            print("list is empty")
        else:
            for entry in self.entries:
                print(entry)
        print("--------------------------------------")

    def filter_by_genre(self, genre):
        filter_func = make_genre_filter(genre)
        found = False
        for entry in self.entries:
            if filter_func(entry):
                print(f"{entry}\n")
                found = True
        if not found:
            print("movie with entered genre not found")


if __name__ == "__main__":
    logbook = Manager()

    while True:
        print("\n=== ----MY WATCH LOG---- ===")
        print("1. Add Movie")
        print("2. Add TV show")
        print("3. View All")
        print("4. Edit an Entry")
        print("5. Filter by Genre")
        print("q. Quit")

        choice = input("Select: ")

        if choice == "1":
            try:
                t = input("Title : ")
                g = input("Genre : ")
                r = float(input("Rating (0-10): "))
                txt = input("Review text : ")
                logbook.addentry(MovieEntry(t, txt, g, r))
            except ValueError as e:
                print(f"Failed to add : {e}")

        elif choice == "2":
            try:
                t = input("Title : ")
                g = input("Genre: ")
                r = float(input("Rating (0-10): "))
                s_no = input("Season number (ENTER = full show) : ")

                if s_no.strip() == "":
                    so = ShowEntry(t, g, r, show_review=input("SHOW REVIEW : "))
                else:
                    e_no = input("Episode number (ENTER = season review) : ")
                    if e_no.strip() == "":
                        so = ShowEntry(t, g, r, season_number=s_no, season_review=input("SEASON REVIEW : "))
                    else:
                        so = ShowEntry(t, g, r, season_number=s_no, episode_number=e_no, episode_review=input("EPISODE REVIEW : "))

                logbook.addentry(so)
            except ValueError as e:
                print(f"Failed to add : {e}")

        elif choice == "3":
            logbook.showall()

        elif choice == "4":
            logbook.edit_entry(input("Enter title to edit : "))

        elif choice == "5":
            logbook.filter_by_genre(input("Enter genre : "))

        elif choice == "q":
            break
