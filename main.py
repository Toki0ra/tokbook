import sqlite3

from kivy.lang import Builder
from kivymd.app import MDApp


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "BlueGray"

        conn = sqlite3.connect('first_db.db')
        c = conn.cursor()

        c.execute("""CREATE TABLE if not exists books
			(name TEXT, author TEXT, genre TEXT, year INTEGER);
            """)

        conn.commit()
        conn.close()

        return Builder.load_file('kivy_style.kv')

    def submit(self):
        name = self.root.ids.name_input.text
        author = self.root.ids.author_input.text
        genre = self.root.ids.genre_input.text
        year = self.root.ids.year_input.text

        if name != '' and author != '' and genre != '' and year.isdecimal():
            conn = sqlite3.connect('first_db.db')

            c = conn.cursor()
            sql_command = "INSERT INTO books (name, author, genre, year) VALUES {0}"
            year = int(year)

            values = (name, author, genre, year)

            c.execute(sql_command.format(str(values)))

            self.root.ids.word_label.text = f'{self.root.ids.name_input.text} Added'

            self.root.ids.name_input.text = ''
            self.root.ids.author_input.text = ''
            self.root.ids.genre_input.text = ''
            self.root.ids.year_input.text = ''

            conn.commit()
            conn.close()
        else:
            self.root.ids.word_label.text = 'Incorrect data, please, try again'

    def show_records(self):
        conn = sqlite3.connect('first_db.db')

        c = conn.cursor()
        c.execute("SELECT * FROM books")
        records = c.fetchall()

        self.root.ids.word_label.text = ''
        res_str = ''
        for record in records:
            res_str += (" ".join(map(str, record)) + '\n')
        self.root.ids.word_label.text += res_str

        # Commit our changes
        conn.commit()

        # Close our connection
        conn.close()


MainApp().run()
