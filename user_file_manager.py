import os
from datetime import datetime


class UserFileManager():
    def __init__(self):
        self.root_dir = os.path.dirname(__file__)

        self.history_dir = os.path.join(self.root_dir, "History")
        if not os.path.exists(self.history_dir):
            os.mkdir(self.history_dir)

        current_date = datetime.now().strftime('%Y-%m-%d-%H.%M.%S')
        self.dir = os.path.join(self.history_dir, f"Game-{current_date}")
        os.mkdir(self.dir)

    def update_history_text(self, player_name, text):
        self.file_dir = f"{self.dir}/{player_name}.txt"
        with open(self.file_dir, mode='a') as file:
            file.write(text + '\n')
