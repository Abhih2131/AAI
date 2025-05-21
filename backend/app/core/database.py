from databases import Database
from .config import settings

database = Database(settings.SUPABASE_DB_URL)
