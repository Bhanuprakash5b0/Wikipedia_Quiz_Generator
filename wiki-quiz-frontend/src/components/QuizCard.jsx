function QuizCard({ data, questionId = 0, selected, onAnswer }) {
  const options = Array.isArray(data.options) ? data.options : [];
  const correctOption =
    typeof data.answer === "string" ? data.answer : options[data.correct_answer];

  return (
    <div className="card">
      <h4>{data.question}</h4>

      <div className="options">
        {options.map((opt, i) => (
          <label key={i} className="option-label">
            <input
              type="radio"
              name={`question-${questionId}`}
              value={opt}
              checked={selected === opt}
              onChange={() => onAnswer && onAnswer(opt)}
            />
            <span>{opt}</span>
          </label>
        ))}
      </div>

      <p>
        <strong>Difficulty:</strong> {data.difficulty || "N/A"}
      </p>

      {selected && (
        <>
          <p className={selected === correctOption ? "correct" : "incorrect"}>
            <strong>
              {selected === correctOption ? "✓ Correct!" : "✗ Incorrect"}
            </strong>
          </p>

          <p className="explanation">
            <strong>Correct Answer:</strong> {correctOption}
          </p>

          {data.explanation && (
            <p className="explanation">
              <strong>Explanation:</strong> {data.explanation}
            </p>
          )}
        </>
      )}
    </div>
  );
}

export default QuizCard;
