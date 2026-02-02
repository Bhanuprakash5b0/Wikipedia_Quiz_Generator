import json
from db.db import get_connection



def save_quiz(data):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO quizzes (url, title, summary, quiz, related_topics)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (url) DO NOTHING
    """

    cur.execute(query, (
        data["url"],
        data["title"],
        data["summary"],
        json.dumps(data["quiz"]),
        json.dumps(data["related_topics"])
    ))

    conn.commit()
    cur.close()
    conn.close()

def fetch_all_quizzes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, url, title, created_at
        FROM quizzes
        ORDER BY created_at DESC
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
def fetch_quiz_by_id(quiz_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT url, title, summary, quiz, related_topics
        FROM quizzes
        WHERE id = %s
    """, (quiz_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    return row
