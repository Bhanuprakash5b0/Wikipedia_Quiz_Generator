function Tabs({ activeTab, setActiveTab }) {
  return (
    <div className="tabs">
      <button
        className={activeTab === "generate" ? "active" : ""}
        onClick={() => setActiveTab("generate")}
      >
        Generate Quiz
      </button>

      <button
        className={activeTab === "history" ? "active" : ""}
        onClick={() => setActiveTab("history")}
      >
        Past Quizzes
      </button>
    </div>
  );
}

export default Tabs;
