import { useState } from "react";
import QuizCard from "./QuizCard";
import { generateQuiz } from "../api/quizApi";

function normalizeQuizArray(arr) {
  return arr.map((q) => {
    const options = q.options || [];
    let answerStr = q.answer || null;
    if (q.correct_answer !== undefined && Number.isInteger(q.correct_answer)) {
      answerStr = options[q.correct_answer] || null;
    }
    return {
      ...q,
      options,
      answer: answerStr,
      difficulty: q.difficulty || "Medium"
    };
  });
}

function GenerateQuiz() {
  const [url, setUrl] = useState("");
  const [quizData, setQuizData] = useState(null);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleGenerate = async () => {
    if (!url.trim()) {
      setError("Please enter a Wikipedia URL");
      return;
    }

    if (!url.includes("wikipedia.org")) {
      setError("Please enter a valid Wikipedia URL (wikipedia.org)");
      return;
    }

    setLoading(true);
    setError(null);
    setQuizData(null);
    setAnswers({});

    try {
      const data = await generateQuiz(url);
      if (data.error) throw new Error(data.error || "LLM returned an error");
      const normalized = {
        ...data,
        quiz: normalizeQuizArray(Array.isArray(data.quiz) ? data.quiz : [])
      };
      setQuizData(normalized);
    } catch (err) {
      setError(err.message || "Failed to generate quiz");
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (qIndex, option) => {
    setAnswers((prev) => ({ ...prev, [qIndex]: option }));
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleGenerate();
  };

  return (
    <div className="generate-quiz-container">
      <div className="input-section">
        <input
          type="text"
          placeholder="Paste Wikipedia article URL (e.g., https://en.wikipedia.org/wiki/Alan_Turing)"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={loading}
        />
        <button onClick={handleGenerate} disabled={loading}>
          {loading ? "Generating..." : "Generate Quiz"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}
      {loading && <p className="loading">Generating quiz...</p>}

      {quizData && (
        <div className="quiz-section">
          <h2>{quizData.title}</h2>
          <p className="summary">{quizData.summary}</p>

          <div className="questions">
            <h3>Questions</h3>
            {quizData.quiz.length > 0 ? (
              quizData.quiz.map((q, index) => (
                <QuizCard
                  key={index}
                  questionId={index}
                  data={q}
                  selected={answers[index]}
                  onAnswer={(opt) => handleAnswer(index, opt)}
                />
              ))
            ) : (
              <p>No questions returned from the generator.</p>
            )}
          </div>

          {quizData.related_topics && Object.entries(quizData.related_topics).length > 0 && (
            <div className="related-section">
              <h3>Related Topics</h3>
              <ul className="topics-list">
                {Object.entries(quizData.related_topics).map(([topic, url],i) => (
                  <li key={i}><a href={url} target="_blank" rel="noopener noreferrer">
                    {topic}</a></li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default GenerateQuiz;
