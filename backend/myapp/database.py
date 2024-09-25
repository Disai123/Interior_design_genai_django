from django.db import connection

class SQLiteDB:
    def __init__(self):
        # No need to create a connection manually
        pass

    def create_tables(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_quota (
                    email TEXT PRIMARY KEY,
                    count INTEGER DEFAULT 0
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS email_images (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT,
                    image_url TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(email) REFERENCES user_quota(email)
                )
            ''')

    def add_image_record(self, email, image_url):
        with connection.cursor() as cursor:
            # Check the count of images for the user
            cursor.execute('SELECT COUNT(*) FROM email_images WHERE email=?', [email])
            count = cursor.fetchone()[0]
            if count >= 5:
                return False  # Limit exceeded

            # Insert the new image record
            cursor.execute('INSERT INTO email_images (email, image_url) VALUES (?, ?)', [email, image_url])
            return True

    def update_quota(self, email):
        with connection.cursor() as cursor:
            cursor.execute('INSERT OR IGNORE INTO user_quota (email, count) VALUES (?, 0)', [email])
            cursor.execute('UPDATE user_quota SET count = count + 1 WHERE email=?', [email])

    def get_last_5_images(self, email):
        self.cursor.execute('SELECT image_url FROM email_images WHERE email=? ORDER BY timestamp DESC LIMIT 5', (email,))
        rows = self.cursor.fetchall()
        return [row[0] for row in rows]
