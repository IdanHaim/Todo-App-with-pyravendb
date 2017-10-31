from datetime import datetime
from pyravendb.tools.utils import Utils


class Todo:
    def __init__(self, title=None, text=None, pub_date=None, complete_date=None):
        self.Id = None
        self.title = title
        self.text = text
        self.done = False
        if not pub_date:
            self.pub_date = datetime.utcnow()
        else:
            self.pub_date = Utils.string_to_datetime(pub_date)

        if complete_date:
            complete_date = Utils.string_to_datetime(complete_date)
        self.complete_date = complete_date
