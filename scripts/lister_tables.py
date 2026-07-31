import sys; sys.path.insert(0,'src')
from dgssi_platform.infrastructure.database.session import SessionLocal
from sqlalchemy import text
session = SessionLocal()
q = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name"
result = session.execute(text(q))
print("Tables existantes:")
for r in result:
    print(" -", r[0])
session.close()
