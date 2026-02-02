from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from config import GEMINI_API_KEY
import json
import re
from db.db import get_connection

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",  # Changed from gemini-1.0-pro
    google_api_key=GEMINI_API_KEY,
    temperature=0.4
)

quiz_prompt = PromptTemplate(
    input_variables=["title", "content"],
    template="""Create a quiz of 1 question based on the following:
Title: {title}
Content: {content}

Return ONLY valid JSON in this exact format:
{{
  "quiz": [
    {{
      "question": "Question text?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "correct_answer": 0,
      "explanation": "Explanation text"
    }}
  ],
  "related_topics": ["Topic1", "Topic2", "Topic3"]
}}

Do not include any text before or after the JSON. Return only the JSON object."""
)

# In-memory cache for quiz data
_quiz_cache = {}

def generate_quiz_from_text(title, content):
    """Generate a quiz from text using Gemini API."""
    prompt = quiz_prompt.format(
        title=title,
        content=content[:2000]  # safety limit
    )

    response = llm.invoke(prompt)
    response_text = response.content.strip()
    
    # Extract JSON from response (in case there's extra text)
    json_match = re.search(r'\{[\s\S]*\}', response_text)
    if json_match:
        response_text = json_match.group(0)
    
    try:
        parsed = json.loads(response_text)
        
        # Validate structure
        if "quiz" not in parsed or "related_topics" not in parsed:
            raise ValueError("Missing required fields in LLM response")
        
        if not isinstance(parsed["quiz"], list) or len(parsed["quiz"]) == 0:
            raise ValueError("Quiz must be a non-empty list")
        
        # Ensure all questions have required fields
        for q in parsed["quiz"]:
            if not all(k in q for k in ["question", "options", "correct_answer", "explanation"]):
                raise ValueError("Question missing required fields")
            if not isinstance(q["options"], list) or len(q["options"]) != 4:
                raise ValueError("Each question must have exactly 4 options")
            if not isinstance(q["correct_answer"], int) or not (0 <= q["correct_answer"] < 4):
                raise ValueError("Correct answer index must be 0-3")
        
        return parsed
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by LLM: {str(e)}")
    except ValueError as e:
        raise ValueError(f"LLM response validation failed: {str(e)}")

def save_quiz(data):
    """Save quiz to database and cache."""
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO quizzes (url, title, summary, quiz, related_topics)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (url) DO UPDATE SET
        title = EXCLUDED.title,
        summary = EXCLUDED.summary,
        quiz = EXCLUDED.quiz,
        related_topics = EXCLUDED.related_topics,
        updated_at = CURRENT_TIMESTAMP
    RETURNING id;
    """

    try:
        cur.execute(query, (
            data["url"],
            data["title"],
            data["summary"],
            json.dumps(data["quiz"]),  # Ensure it's JSON string
            json.dumps(data.get("related_topics", []))  # Ensure it's JSON string
        ))
        
        quiz_id = cur.fetchone()[0]
        conn.commit()
        
        # Update cache
        _quiz_cache[quiz_id] = data
        _quiz_cache[data["url"]] = data
        
        return quiz_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()

def fetch_all_quizzes():
    """Fetch all quizzes from database."""
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, url, title, created_at
            FROM quizzes
            ORDER BY created_at DESC
        """)

        rows = cur.fetchall()
        return rows
    finally:
        cur.close()
        conn.close()

def fetch_quiz_by_id(quiz_id):
    """Fetch quiz by ID and parse JSON fields."""
    # Check cache first
    if quiz_id in _quiz_cache:
        return _quiz_cache[quiz_id]
    
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, url, title, summary, quiz, related_topics
            FROM quizzes
            WHERE id = %s
        """, (quiz_id,))

        row = cur.fetchone()
        
        if not row:
            return None
        
        # Parse JSON fields
        quiz_data = {
            "id": row[0],
            "url": row[1],
            "title": row[2],
            "summary": row[3],
            "quiz": json.loads(row[4]) if isinstance(row[4], str) else row[4],
            "related_topics": json.loads(row[5]) if isinstance(row[5], str) else row[5]
        }
        
        # Cache the result
        _quiz_cache[quiz_id] = quiz_data
        
        return quiz_data
    finally:
        cur.close()
        conn.close()

def fetch_quiz_by_url(url):
    """Fetch quiz by URL for deduplication."""
    # Check cache first
    if url in _quiz_cache:
        return _quiz_cache[url]
    
    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, url, title, summary, quiz, related_topics
            FROM quizzes
            WHERE url = %s
        """, (url,))

        row = cur.fetchone()
        
        if not row:
            return None
        
        # Parse JSON fields
        quiz_data = {
            "id": row[0],
            "url": row[1],
            "title": row[2],
            "summary": row[3],
            "quiz": json.loads(row[4]) if isinstance(row[4], str) else row[4],
            "related_topics": json.loads(row[5]) if isinstance(row[5], str) else row[5]
        }
        
        # Cache the result
        _quiz_cache[url] = quiz_data
        _quiz_cache[row[0]] = quiz_data
        
        return quiz_data
    finally:
        cur.close()
        conn.close()

def clear_cache():
    """Clear the in-memory cache."""
    global _quiz_cache
    _quiz_cache = {}
