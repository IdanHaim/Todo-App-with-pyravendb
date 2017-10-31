from pyravendb.store.document_store import DocumentStore
from pyravendb.raven_operations.server_operations import CreateDatabaseOperation

database_name = "todo"
urls = ["http://localhost:8080"]


class Database:
    def __init__(self):
        self._document_store = None

    @property
    def document_store(self):
        if self._document_store is None:
            self._document_store = DocumentStore(urls=urls, database=database_name)
            self.document_store.initialize()
        self.create_database()
        return self._document_store

    def create_database(self):
        try:
            self._document_store.admin.server.send(CreateDatabaseOperation(database_name=database_name))
        except Exception:
            pass

    def close(self):
        self.document_store = None