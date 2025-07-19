import logging
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("app.log")
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


def get_logger():
    return logger


BASE_DIR = Path(__file__).parent.parent


class AuthJWTSettings(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 150


class BackendSettings(BaseModel):
    host: str = "localhost"
    port: int = 8000


class DatabaseSettings(BaseModel):
    driver: str = "sqlite+aiosqlite"
    user: str = ""
    password: str = ""
    host: str = ""
    port: str = ""
    dbname: str = "database.db"

    @property
    def database_url(self) -> str:
        if "sqlite" in self.driver:
            return f"{self.driver}:///{self.dbname}"
        else:
            return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"


class NoteRulesSettings(BaseModel):
    title_max_lenght: int = 256
    body_max_lenght: int = 65536


class MongoSettings(BaseModel):
    login: str = "root"
    password: str = "example"
    host: str = "localhost"
    port: int = 27017

    @property
    def mongo_uri(self) -> str:
        return f"mongodb://{self.login}:{self.password}@{self.host}:{self.port}"


class DevSettings(BaseSettings):
    auth_jwt: AuthJWTSettings = AuthJWTSettings()
    db: DatabaseSettings = DatabaseSettings()
    backend: BackendSettings = BackendSettings()
    note_rules: NoteRulesSettings = NoteRulesSettings()
    mongo: MongoSettings = MongoSettings()


class ProdSettings(BaseSettings): ...


settings = DevSettings()
