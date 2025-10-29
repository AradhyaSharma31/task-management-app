import psycopg2

DB_NAME = "task_management"
DB_USER = "postgres"
DB_PASSWORD = "$DatA_BasE26"
DB_HOST = "localhost"
DB_PORT = "5432"

def get_connection():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    return conn

def init_db():
    conn = None
    cur = None
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        # First check if table exists and has all columns
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='tasks'
        """)
        existing_columns = [row[0] for row in cur.fetchall()]
        
        if not existing_columns:
            # Table doesn't exist, create it
            cur.execute("""
                CREATE TABLE tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    status VARCHAR(10) DEFAULT 'pending',
                    due_date DATE,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            print("Tasks table created.")
        else:
            # Table exists, check for missing columns
            required_columns = ['id', 'title', 'description', 'status', 'due_date', 'created_at']
            for column in required_columns:
                if column not in existing_columns:
                    if column == 'created_at':
                        cur.execute("ALTER TABLE tasks ADD COLUMN created_at TIMESTAMP DEFAULT NOW()")
                        print(f"Added missing column: {column}")
        
        conn.commit()
        print("Database initialized and ready.")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        if conn:
            conn.rollback()
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()