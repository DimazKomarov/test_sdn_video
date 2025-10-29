from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'cities.db'}"

NOMINATIM_USER_AGENT = "Test-App/1.0 (contact@example.com)"