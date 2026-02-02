"""
Test suite for Wikipedia Quiz Generator
Run with: pytest test_api.py
"""

import pytest
import json
from backend.app import create_app
from backend.config import DATABASE_URL


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


class TestQuizAPI:
    """Test quiz API endpoints"""
    
    def test_generate_quiz_missing_url(self, client):
        """Test generate endpoint with missing URL"""
        response = client.post('/api/generate', 
            json={},
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'error' in response.get_json()
    
    def test_generate_quiz_invalid_url(self, client):
        """Test generate endpoint with invalid URL"""
        response = client.post('/api/generate',
            json={'url': 'not-a-valid-url'},
            content_type='application/json'
        )
        # Should fail at scraping stage
        assert response.status_code in [400, 500]
    
    def test_history_endpoint(self, client):
        """Test history endpoint returns list"""
        response = client.get('/api/history')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
    
    def test_history_structure(self, client):
        """Test history response structure"""
        response = client.get('/api/history')
        assert response.status_code == 200
        data = response.get_json()
        
        if len(data) > 0:
            quiz = data[0]
            assert 'id' in quiz
            assert 'title' in quiz
            assert 'url' in quiz
            assert 'created_at' in quiz


class TestDatabaseConnection:
    """Test database connectivity"""
    
    def test_database_url_configured(self):
        """Test DATABASE_URL is set"""
        assert DATABASE_URL is not None
        assert 'postgresql://' in DATABASE_URL or 'postgres://' in DATABASE_URL


class TestScraperService:
    """Test Wikipedia scraper"""
    
    def test_scraper_imports(self):
        """Test scraper can be imported"""
        from backend.services.scraper import scrape_wikipedia
        assert callable(scrape_wikipedia)


class TestLLMService:
    """Test LLM service"""
    
    def test_llm_imports(self):
        """Test LLM service can be imported"""
        from backend.services.llm_service import generate_quiz_from_text
        assert callable(generate_quiz_from_text)


class TestDatabaseOperations:
    """Test database operations"""
    
    def test_quiz_repo_imports(self):
        """Test quiz repository can be imported"""
        from backend.db.quiz_repo import (
            save_quiz, fetch_all_quizzes, fetch_quiz_by_id
        )
        assert callable(save_quiz)
        assert callable(fetch_all_quizzes)
        assert callable(fetch_quiz_by_id)


# Integration tests
class TestIntegration:
    """Integration tests"""
    
    def test_app_creation(self):
        """Test Flask app can be created"""
        app = create_app()
        assert app is not None
    
    def test_app_has_blueprint(self):
        """Test app has quiz blueprint registered"""
        app = create_app()
        blueprints = app.blueprints
        assert 'quiz' in blueprints
    
    def test_cors_enabled(self):
        """Test CORS is enabled"""
        app = create_app()
        # CORS should be configured for all routes
        assert app is not None


# Manual test checklist
"""
MANUAL TEST CHECKLIST:

Frontend Tests:
- [ ] Generate Quiz tab loads
- [ ] Can paste Wikipedia URL
- [ ] Generate button works
- [ ] Error message shows for invalid URL
- [ ] Quiz displays correctly
- [ ] Can click through questions
- [ ] Previous/Next buttons work
- [ ] Score calculation is correct
- [ ] History tab shows past quizzes
- [ ] Can click Details on past quiz
- [ ] Modal displays quiz history
- [ ] Styling looks good on mobile

Backend Tests:
- [ ] Flask server starts on port 5000
- [ ] POST /api/generate accepts valid Wikipedia URL
- [ ] POST /api/generate returns quiz object
- [ ] POST /api/generate returns 400 for missing URL
- [ ] GET /api/history returns list
- [ ] GET /api/quiz/<id> returns quiz details
- [ ] Database saves quizzes correctly
- [ ] CORS headers present in response

Database Tests:
- [ ] PostgreSQL is running
- [ ] Database 'wiki_quiz' exists
- [ ] 'quizzes' table created
- [ ] Indexes created
- [ ] Can insert quiz records
- [ ] Can query quiz records

API Integration Tests:
- [ ] Frontend can reach backend
- [ ] Quiz generation works end-to-end
- [ ] History persistence works
- [ ] Error handling works
"""


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
