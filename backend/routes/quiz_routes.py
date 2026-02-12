from flask import Blueprint, request, jsonify
from services.scraper import scrape_wikipedia
from services.llm_service import generate_quiz_from_text
from db.quiz_repo import save_quiz, fetch_all_quizzes, fetch_quiz_by_url
from init_cache import cache

quiz_bp = Blueprint("quiz", __name__)

def generate_cache_key():
    body=request.get_json()
    return body.get("url")

@quiz_bp.route("/generate", methods=["POST"])

def generate_quiz():
    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Scrape article
    cached_text=cache.get(url)
    if(cached_text):
        return jsonify(cached_text)
    
    article = scrape_wikipedia(url)
    if not article:
        return jsonify({"error": "Failed to scrape Wikipedia article"}), 400

    try:
        llm_output = generate_quiz_from_text(
            article["title"],
            article["content"]
        )
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"LLM generation error: {e}\n{tb}")
        return jsonify({
            "error": "LLM generation failed",
            "detail": str(e),
            "traceback": tb
        }), 500

    # Build response
    response = {
        "url": url,
        "title": article["title"],
        "summary": article["summary"],
        "quiz": llm_output["quiz"],
        "related_topics": llm_output["related_topics"]
    }
    cache.set(url,response,timeout=120)
    # Save to database
    try:
        save_quiz(response)
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"Warning: Could not save quiz to database: {e}\n{tb}")
    cache.delete("history_cache")

    return jsonify(response)

@quiz_bp.route("/history", methods=["GET"])

def quiz_history():
    res=cache.get("history_cache")
    if res:
        return jsonify(res)
    try:
        quizzes = fetch_all_quizzes()

        result = []
        for q in quizzes:
            result.append({
                "url": q[0],
                "title": q[1],
                "created_at": q[2]
            })
        cache.set("history_cache",result,timeout=120)
        return jsonify(result),200
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"Error fetching history: {e}\n{tb}")
        return jsonify({"error": "Failed to fetch history", "detail": str(e), "traceback": tb}), 500


@quiz_bp.route("/quiz/<string:quiz_url>", methods=["GET"])
def get_quiz_details(quiz_url):
    try:
        quiz = fetch_quiz_by_url(quiz_url)
        if not quiz:
            return jsonify({"error": "Quiz not found"}), 404

        return jsonify({
            "url": quiz[0],
            "title": quiz[1],
            "summary": quiz[2],
            "quiz": quiz[3],
            "related_topics": quiz[4]
        })
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print(f"Error fetching quiz: {e}\n{tb}")
        return jsonify({"error": "Failed to fetch quiz", "detail": str(e), "traceback": tb}), 500
#generate_quiz()