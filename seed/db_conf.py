import asyncpg
from dotenv import load_dotenv
import os


load_dotenv()
URL = os.getenv("DATABASE_URL", None)
SCHEMA = os.getenv("SCHEMA", None)

class db_insert:
    async def initialize(self):
        self.pool = await asyncpg.create_pool(URL, timeout=30, command_timeout=5,
                                              server_settings={'search_path': SCHEMA})

        print('connected!')
        return self.pool
