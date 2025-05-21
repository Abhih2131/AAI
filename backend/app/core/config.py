import os

class Settings:
    SUPABASE_DB_URL = os.getenv("SUPABASE_DB_URL")

settings = Settings()
