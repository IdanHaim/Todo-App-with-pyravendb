from datetime import datetime


class Todo:
    def __init__(self, title=None, text=None):
        self.Id = None
        self.title = title
        self.text = text
        self.done = False
        self.pub_date = datetime.utcnow()
