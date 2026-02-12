import psycopg2
from config import DATABASE_URL

def init_db():
    """Initialize the database schema."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable not set")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Create quizzes table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS quizzes (
                url VARCHAR(500) PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                summary TEXT,
                quiz JSONB NOT NULL,
                related_topics JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_quizzes_url ON quizzes(url);
        """)

        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_quizzes_created_at ON quizzes(created_at DESC);
        """)

        conn.commit()
        cur.close()
        conn.close()

        print("✓ Database initialized successfully!")
        print("✓ Created 'quizzes' table with indexes")

    except psycopg2.Error as e:
        print(f"✗ Database error: {e}")
        raise
    except Exception as e:
        print(f"✗ Error: {e}")
        raise


if __name__ == "__main__":
    init_db()
