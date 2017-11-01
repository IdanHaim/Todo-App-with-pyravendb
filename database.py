from pyravendb.store.document_store import DocumentStore
from pyravendb.raven_operations.server_operations import CreateDatabaseOperation


class Database:
    @staticmethod
    def get_store(context):
        store = getattr(context.g, "store", None)
        if not store:
            urls = context.app.config["DATABASE_URLS"]
            database_name = context.app.config["DATABASE_NAME"]
            store = DocumentStore(urls=urls, database=database_name)
            store.initialize()
            context.g.store = store
        return store

    @staticmethod
    def create_database(context):
        database_name = context.app.config["DATABASE_NAME"]
        if not hasattr(context.g, database_name):
            try:
                store = Database.get_store(context)
                setattr(context.g, database_name, True)
                store.admin.server.send(CreateDatabaseOperation(database_name=database_name))
            except:
                pass
