import sqlite3

class StephenKingMovieDatabase:
    def __init__(self):
        # Establish a connection with the SQLite database
        self.connection = sqlite3.connect("stephen_king_adaptations.db")
        self.cursor = self.connection.cursor()

        # Create the table in the database if it doesn't exist
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                            movieID TEXT PRIMARY KEY,
                            movieName TEXT,
                            movieYear INTEGER,
                            imdbRating REAL
                        )''')
        self.connection.commit()

    def populate_database_from_file(self):
        # Read the file and copy its content to a list
        with open("stephen_king_adaptations.txt", "r") as file:
            stephen_king_adaptations_list = file.readlines()

        # Insert the content from the list into the table, ignoring duplicates
        for line in stephen_king_adaptations_list:
            movie_data = line.strip().split(",")
            try:
                self.cursor.execute('''INSERT OR IGNORE INTO stephen_king_adaptations_table (movieID, movieName, movieYear, imdbRating)
                                      VALUES (?, ?, ?, ?)''', movie_data)
            except sqlite3.IntegrityError:
                pass

        self.connection.commit()

    def search_movies(self):
        while True:
            print("\nOptions:")
            print("1. Search by movie name")
            print("2. Search by movie year")
            print("3. Search by movie rating")
            print("4. STOP")

            option = input("Enter an option: ")

            if option == "1":
                movie_name = input("Enter the name of the movie: ")
                self.cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?''', (movie_name,))
                result = self.cursor.fetchone()

                if result:
                    print("Movie details:")
                    print(f"Movie Name: {result[1]}")
                    print(f"Movie Year: {result[2]}")
                    print(f"IMDB Rating: {result[3]}")
                else:
                    print("No such movie exists in our database.")

            elif option == "2":
                movie_year = input("Enter the year: ")
                self.cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?''', (movie_year,))
                results = self.cursor.fetchall()

                if results:
                    print("Movies released in that year:")
                    for result in results:
                        print(f"Movie Name: {result[1]}")
                        print(f"Movie Year: {result[2]}")
                        print(f"IMDB Rating: {result[3]}")
                else:
                    print("No movies were found for that year in our database.")

            elif option == "3":
                rating_limit = input("Enter the minimum rating: ")
                self.cursor.execute('''SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?''', (rating_limit,))
                results = self.cursor.fetchall()

                if results:
                    print("Movies with Rating >= ", rating_limit)
                    for result in results:
                        print(f"Movie Name: {result[1]}")
                        print(f"Movie Year: {result[2]}")
                        print(f"IMDB Rating: {result[3]}")
                else:
                    print("No movies at or above that rating were found in the database.")

            elif option == "4":
                break

    def close_database(self):
        # Close the connection to the database
        self.connection.close()

if __name__ == "__main__":
    database = StephenKingMovieDatabase()
    database.populate_database_from_file()
    database.search_movies()
    database.close_database()
