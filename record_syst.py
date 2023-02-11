import sqlite3
from datetime import datetime
from tkinter import *

# Record data in the database
class RecordSystem(object):
    def __init__(self):
        self.conn = sqlite3.connect('scoresheet.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            name TEXT,
            score INTEGER
        )
        ''')

    # Enters scores and names into the database
    def enter_score(self, name: str, val: int):
        self.cursor.execute(f"""
        INSERT INTO scores VALUES
        ('{name}', '{val}')
        """)
        self.conn.commit()

    # Gets scores and names from database
    def get_scores(self):
        self.cursor.execute('''
        SELECT * FROM scores ORDER BY score DESC LIMIT 10;
        ''')
        return self.cursor.fetchall()

# Using tkinter to show up the text box
class TextBox:
    def __init__(self, score):
        self.root = Tk()
        self.records = RecordSystem()  # Record system to record player name and score
        self.entry = Entry(self.root, width=50, borderwidth=5)  # Tkinter root
        self.add_btn = Button(command=self.update_info, text='ENTER')  # Set up the button on the screen
        self.player_score = score

    # Takes second element in list to sort out the data on the score screen
    def takeSecond(self, elem):
        return elem[1]

    # Drawing the text box
    def enter_info(self):
        self.root.title('Enter Name')
        self.entry.grid(row=1, column=0, columnspan=3)
        self.add_btn.grid(row=2, column=1)
        self.root.mainloop()

    def update_info(self):
        name = self.entry.get()  # Get the name from the text box
        # Sets the record name and score
        self.records.enter_score(name, self.player_score)
        self.root.destroy()  # Exits
