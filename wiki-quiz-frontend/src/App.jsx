import { useState } from "react";
import Tabs from "./components/Tabs";
import GenerateQuiz from "./components/GeneratorQuiz";
import HistoryTable from "./components/HistoryTable";
import "./App.css";

function App() {
  const [activeTab, setActiveTab] = useState("generate");

  return (
    <div className="container">
      <h1>Wikipedia Quiz Generator</h1>

      <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />

      {activeTab === "generate" && <GenerateQuiz />}
      {activeTab === "history" && <HistoryTable />}
    </div>
  );
}

export default App;
