const API_BASE_URL = "http://localhost:5000/api";

/**
 * Generate a quiz from a Wikipedia URL
 * @param {string} url - The Wikipedia URL
 * @returns {Promise<Object>} Quiz data with questions and related topics
 */
export const generateQuiz = async (url) => {
  try {
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ url })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error generating quiz:", error);
    throw error;
  }
};

/**
 * Fetch quiz history
 * @returns {Promise<Array>} Array of quiz history items
 */
export const fetchQuizHistory = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/history`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching quiz history:", error);
    throw error;
  }
};

/**
 * Fetch a specific quiz by ID
 * @param {string|number} quizUrl - The quiz ID
 * @returns {Promise<Object>} Quiz details
 */
export const fetchQuizByUrl = async (quizUrl) => {
  try {
    const response = await fetch(`${API_BASE_URL}/quiz/${quizUrl}`);

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error fetching quiz:", error);
    throw error;
  }
};
