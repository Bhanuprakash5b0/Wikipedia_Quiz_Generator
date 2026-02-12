import { useState, useEffect } from "react";
import QuizModal from "./QuizModal";
import {fetchQuizByUrl, fetchQuizHistory} from "../api/quizApi.js";

function HistoryTable() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedQuiz, setSelectedQuiz] = useState(null);
  const [showModal, setShowModal] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      
      const data = await fetchQuizHistory();
      setHistory(data);
      setError(null);
    } catch (err) {
      setError(err.message);
      setHistory([]);
    } finally {
      setLoading(false);
    }
  };

  const handleDetails = async (quizSummary) => {
    try {
      setLoading(true);

      const full = await fetchQuizByUrl(quizSummary.url);

      // Ensure quiz fields are JSON-parsed for older responses
      if (typeof full.quiz === "string") full.quiz = JSON.parse(full.quiz);
      if (typeof full.related_topics === "string")
        full.related_topics = JSON.parse(full.related_topics);

      setSelectedQuiz(full);
      setShowModal(true);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <p>Loading history...</p>;
  if (error) return <p className="error">Error: {error}</p>;
  if (history.length === 0) return <p>No quizzes generated yet.</p>;

  return (
    <>
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>URL</th>
            <th>Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {history.map((quiz) => (
            <tr key={quiz.url}>
              <td>{quiz.title}</td>
              <td>
                <a href={quiz.url} target="_blank" rel="noopener noreferrer">
                  View
                </a>
              </td>
              <td>{new Date(quiz.created_at).toLocaleString()}</td>
              <td>
                <button onClick={() => handleDetails(quiz)}>Details</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {showModal && selectedQuiz && (
        <QuizModal quiz={selectedQuiz} onClose={() => setShowModal(false)} />
      )}
    </>
  );
}

export default HistoryTable;
