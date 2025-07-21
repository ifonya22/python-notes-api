from app.database.repositories.mongo.notes import MongoDBNoteRepositoryImpl
from app.database.repositories.mongo.users import MongoDBUserRepositoryImpl
from app.database.repositories.sql.notes import SQLNoteRepositoryImpl
from app.database.repositories.sql.users import SQLUserRepositoryImpl


class RepositoryDBFactory:
    def __init__(self, sql_session, mongo_db):
        self.sql_session = sql_session
        self.mongo_db = mongo_db

    def get_sql_user_repository(self) -> SQLUserRepositoryImpl:
        return SQLUserRepositoryImpl(self.sql_session)

    def get_sql_note_repository(self) -> SQLNoteRepositoryImpl:
        raise NotImplementedError()
        # return SQLNoteRepository(self.sql_session)

    def get_mongo_user_repository(self) -> MongoDBUserRepositoryImpl:
        raise NotImplementedError()
        # return MongoDBUserRepository(self.mongo_db["users"])

    def get_mongo_note_repository(self) -> MongoDBNoteRepositoryImpl:
        return MongoDBNoteRepositoryImpl(self.mongo_db["notes"])
