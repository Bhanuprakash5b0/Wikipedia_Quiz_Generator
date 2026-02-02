# Wikipedia Quiz Generator

A full-stack application that generates interactive quizzes from Wikipedia articles using AI (Google Gemini). Built with React frontend and Flask backend.

## Features

- 📚 **Generate Quizzes**: Input any Wikipedia URL to automatically generate multiple-choice questions
- 🤖 **AI-Powered**: Uses Google Gemini API to create quiz questions and explanations
- 💾 **Quiz History**: Stores all generated quizzes in PostgreSQL database
- 🎯 **Interactive Quiz Mode**: Play quizzes with immediate feedback and scoring
- 📊 **Related Topics**: Suggests related topics for further learning
- 🎨 **Modern UI**: Responsive design with smooth interactions

## Project Structure

```
Wiki_Quiz/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py              # Configuration (loads .env)
│   ├── init_db.py             # Database initialization script
│   ├── requirements.txt        # Python dependencies
│   ├── db/
│   │   ├── db.py              # Database connection
│   │   └── quiz_repo.py        # Quiz CRUD operations
│   ├── routes/
│   │   └── quiz_routes.py      # API endpoints
│   └── services/
│       ├── scraper.py         # Wikipedia scraper
│       └── llm_service.py      # Gemini AI service
│
├── wiki-quiz-frontend/
│   ├── package.json            # Node.js dependencies
│   ├── public/
│   │   └── index.html          # HTML entry point
│   └── src/
│       ├── App.jsx             # Main component
│       ├── index.js            # React entry point
│       ├── api/
│       │   └── quizApi.js       # API client utilities
│       ├── components/
│       │   ├── GeneratorQuiz.jsx    # Quiz generator form
│       │   ├── HistoryTable.jsx     # Quiz history display
│       │   ├── QuizCard.jsx         # Individual quiz question
│       │   ├── QuizModal.jsx        # Quiz modal/dialog
│       │   └── Tabs.jsx             # Tab navigation
│       └── styles/
│           └── main.css         # Global styles
│
└── .env.example               # Environment variables template
```

## Prerequisites

- **Python 3.8+**
- **Node.js 14+**
- **PostgreSQL 12+**
- **Google Gemini API Key** (free tier available)

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cp ../.env.example .env
```

Edit `.env` with your credentials:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/wiki_quiz
GEMINI_API_KEY=your_api_key_from_makersuite_google_com
```

### 3. Initialize Database

```bash
python init_db.py
```

This creates the `quizzes` table and necessary indexes in PostgreSQL.

### 4. Run Backend Server

```bash
python app.py
```

The backend will run on `http://localhost:5000`

## Frontend Setup

### 1. Install Node Dependencies

```bash
cd wiki-quiz-frontend
npm install
```

### 2. Configure API URL (Optional)

By default, the frontend connects to `http://localhost:5000/api`. If you need to change this, update the `API_BASE_URL` in `src/api/quizApi.js`.

### 3. Run Frontend Development Server

```bash
npm start
```

The frontend will open at `http://localhost:3000`

## API Endpoints

### Generate Quiz
- **POST** `/api/generate`
- **Body**: `{ "url": "https://en.wikipedia.org/wiki/..." }`
- **Response**: Quiz object with questions, answers, and related topics

### Get Quiz History
- **GET** `/api/history`
- **Response**: Array of quiz objects (id, title, url, created_at)

### Get Quiz Details
- **GET** `/api/quiz/<id>`
- **Response**: Full quiz object with all questions

## Database Schema

### Quizzes Table

```sql
CREATE TABLE quizzes (
    id SERIAL PRIMARY KEY,
    url VARCHAR(500) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    summary TEXT,
    quiz JSONB NOT NULL,                    -- Array of questions
    related_topics JSONB,                   -- Array of topic strings
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## Troubleshooting

### Backend Issues

**LLM Generation Failed**
- Ensure `GEMINI_API_KEY` is set correctly in `.env`
- Check API usage limits at makersuite.google.com
- Verify internet connection

**Database Connection Error**
- Verify PostgreSQL is running
- Check `DATABASE_URL` format in `.env`
- Ensure database exists: `createdb wiki_quiz`

**Wikipedia Scraper Issues**
- Verify the URL is a valid Wikipedia article URL
- Check your internet connection
- Some articles may have different HTML structures

### Frontend Issues

**CORS Errors**
- Backend CORS is enabled for all origins
- Ensure backend is running on port 5000
- Check browser console for specific errors

**API Connection Fails**
- Verify backend is running
- Check `API_BASE_URL` in `quizApi.js`
- Use browser DevTools Network tab to inspect requests

## Environment Variables

### Required (.env file)

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/wiki_quiz

# API Keys
GEMINI_API_KEY=your_api_key
```

### Optional

```env
# Flask
FLASK_ENV=development
FLASK_DEBUG=True

# Frontend
REACT_APP_API_URL=http://localhost:5000/api
```

## Sample Quiz Response Format

```json
{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Mathison Turing was an English mathematician...",
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": [
        "Harvard University",
        "Cambridge University",
        "Oxford University",
        "Princeton University"
      ],
      "answer": "Cambridge University",
      "difficulty": "easy",
      "explanation": "Alan Turing studied mathematics at Cambridge University."
    }
  ],
  "related_topics": ["Cryptography", "Enigma Machine", "Computer Science"]
}
```

## Performance Tips

- **Database**: Use indexes for faster queries (already created in init_db.py)
- **Caching**: The app stores quizzes, preventing duplicate scraping
- **API Rate Limiting**: Monitor Gemini API usage to avoid quota limits
- **Frontend**: React optimizes re-renders automatically

## Development Workflow

1. **Backend Development**: Make changes to `backend/` files
2. **Frontend Development**: Make changes to `wiki-quiz-frontend/src/` files
3. **Testing**: Test API endpoints with curl, Postman, or browser DevTools
4. **Database Changes**: Update schema and run `init_db.py` again

## Known Limitations

- Wikipedia articles only (no custom text input)
- Requires active internet connection
- Gemini API has rate limits
- Some Wikipedia articles may have unusual formatting

## Future Enhancements

- [ ] User authentication and profiles
- [ ] Quiz difficulty levels
- [ ] User statistics and progress tracking
- [ ] Multiple language support
- [ ] Export quiz as PDF
- [ ] Leaderboard/competition mode
- [ ] Custom question creation
- [ ] Advanced search and filtering

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
1. Check this README
2. Review the troubleshooting section
3. Check existing GitHub issues
4. Open a new issue with detailed description

## Credits

- **Flask**: Web framework
- **React**: Frontend framework
- **LangChain**: LLM orchestration
- **Google Gemini**: AI model
- **PostgreSQL**: Database
- **BeautifulSoup**: Web scraping

---

**Made with ❤️ for Wikipedia lovers and quiz enthusiasts**
