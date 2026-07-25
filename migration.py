import psycopg2
import os

DSN = (
    f"host={os.environ.get('POSTGRES_HOST', 'localhost')} "
    f"port={os.environ.get('POSTGRES_PORT', '5432')} "
    f"dbname={os.environ.get('POSTGRES_DB', 'dgssi')} "
    f"user={os.environ.get('POSTGRES_USER', 'dgssi')} "
    f"password={os.environ.get('POSTGRES_PASSWORD', 'changeme')}"
)

def add_column():
    conn = psycopg2.connect(DSN)
    conn.autocommit = True
    try:
        with conn.cursor() as cur:
            cur.execute("ALTER TABLE non_conformites ADD COLUMN IF NOT EXISTS est_note BOOLEAN DEFAULT FALSE;")
            cur.execute("ALTER TABLE chapitres ADD COLUMN IF NOT EXISTS notes_audit TEXT;")
            cur.execute("ALTER TABLE chapitres ADD COLUMN IF NOT EXISTS notes_audit_synthese TEXT;")
            print("Columns added successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    add_column()
