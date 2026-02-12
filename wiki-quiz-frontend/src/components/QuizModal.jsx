import { useState } from "react";
import QuizCard from "./QuizCard";

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
      difficulty: q.difficulty || q.level || "N/A"
    };
  });
}

function QuizModal({ quiz, onClose }) {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [userAnswers, setUserAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);

  if (!quiz) return null;

  const quizDataRaw = typeof quiz.quiz === "string" ? JSON.parse(quiz.quiz) : quiz.quiz;
  const relatedTopics =
    typeof quiz.related_topics === "string"
      ? JSON.parse(quiz.related_topics)
      : quiz.related_topics || {};

  const quizData = normalizeQuizArray(Array.isArray(quizDataRaw) ? quizDataRaw : []);

  const currentQuiz = quizData[currentQuestion];

  const handleAnswer = (selectedOption) => {
    setUserAnswers({
      ...userAnswers,
      [currentQuestion]: selectedOption
    });
  };

  const handleNext = () => {
    if (currentQuestion < quizData.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    } else {
      setShowResults(true);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleReset = () => {
    setCurrentQuestion(0);
    setUserAnswers({});
    setShowResults(false);
  };

  const calculateScore = () => {
    let correct = 0;
    quizData.forEach((q, index) => {
      if (userAnswers[index] === q.answer) correct++;
    });
    return Math.round((correct / quizData.length) * 100);
  };

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-btn" onClick={onClose}>
          &times;
        </button>

        {!showResults ? (
          <>
            <h2>{quiz.title}</h2>
            <p className="quiz-progress">
              Question {currentQuestion + 1} of {quizData.length}
            </p>

            <QuizCard
              questionId={currentQuestion}
              data={currentQuiz}
              selected={userAnswers[currentQuestion]}
              onAnswer={handleAnswer}
            />

            <div className="quiz-actions">
              <button onClick={handlePrevious} disabled={currentQuestion === 0}>
                Previous
              </button>
              <button onClick={handleNext}>
                {currentQuestion === quizData.length - 1 ? "Finish" : "Next"}
              </button>
            </div>
          </>
        ) : (
          <>
            <h2>Quiz Results</h2>
            <div className="results">
              <h3>Your Score: {calculateScore()}%</h3>
              <p>
                Correct Answers:{" "}
                {quizData.filter((q, i) => userAnswers[i] === q.answer).length} /{" "}
                {quizData.length}
              </p>

              <h3>Related Topics</h3>
              <ul>
                {relatedTopics.map((topic, i) => (
                  <li key={i}>{topic}</li>
                ))}
              </ul>

              <button onClick={handleReset}>Retake Quiz</button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}

export default QuizModal;
