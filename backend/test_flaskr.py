import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db
from settings import DB_NAME, DB_USER, DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".
        # format('localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, 'localhost', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation
    and for expected errors.
    """
    # test pagination

    def test_get_questions_per_page(self):
        res = self.client().get("/api/v1.0/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

    def test_get_questions_per_page_wrong_url(self):
        res = self.client().get("/api/v1.0/question")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    def test_get_questions_per_page_wrong_method(self):
        res = self.client().get("/api/v1.0/questions/5")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    # test categories

    def test_get_categories(self):
        res = self.client().get("/api/v1.0/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_categories_not_found(self):
        res = self.client().get("/api/v1.0/categories/4")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    def test_get_categories_wrong_method(self):
        res = self.client().post("/api/v1.0/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    def test_get_categories_wrong_url(self):
        res = self.client().post("/api/v1.0/categuries")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    # test question

    def test_get_questions(self):
        res = self.client().get("/api/v1.0/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_get_question_wrong_url(self):
        res = self.client().get("/api/v1.0/question")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    def test_get_question_bad_request(self):
        res = self.client().get("/api/v1.0/questions/?page=1400")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 400)

    def test_get_question_wrong_method(self):
        res = self.client().post("/api/v1.0/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    # test delete question

    def test_delete_question(self):
        res = self.client().delete("/api/v1.0/questions/8")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_not_found(self):
        res = self.client().delete("/api/v1.0/questions/8000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    def test_delete_question_wrong_method(self):
        res = self.client().post("/api/v1.0/questions/6")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    def test_delete_question_wrong_url(self):
        res = self.client().delete("/api/v1.0/question/8")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    # test add question

    def test_add_question(self):
        new_question = {
            'question': 'Who is your father?',
            'answer': 'James',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post("/api/v1.0/questions", json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_question_wrong_method(self):
        new_question = {
            'question': 'Who is your father?',
            'answer': 'James',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().delete("/api/v1.0/questions", json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    def test_add_question_wrong_url(self):
        new_question = {
            'question': 'Who is your father?',
            'answer': 'James',
            'difficulty': 1,
            'category': 1
        }
        res = self.client().post("/api/v1.0/question", json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    # test search

    def test_search_question(self):
        search_term = {'searchTerm': 'Who'}
        res = self.client().post(
            "/api/v1.0/questions/search", json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data['questions']), 10)

    def test_search_question_wrong_method(self):
        search_term = {'search_term': 'What'}
        res = self.client().get(
            "/api/v1.0/questions/search", json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    def test_search_question_wrong_url(self):
        search_term = {'search_term': 'What'}
        res = self.client().post(
            "/api/v1.0/questions/saerch", json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)

    # test question by categories

    def test_questions_by_category(self):
        res = self.client().get('/api/v1.0/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertNotEqual(len(data['questions']), 0)
        self.assertEqual(data['current_category'], 'Science')

    def test_questions_by_category_wrong_method(self):
        res = self.client().post('/api/v1.0/categories/7/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 405)

    def test_questions_by_category_not_found(self):
        res = self.client().get('/api/v1.0/categories/6000/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    def test_questions_by_category_wrong_url(self):
        res = self.client().get('/api/v1.0/categores/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 404)

    # test quiz

    def test_quizzes(self):
        quiz = {
            'previous_questions': [6],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 3
            }
        }
        res = self.client().post('/api/v1.0/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['question']['category'], 3)

    def test_quizzes_wrong_method(self):
        quiz = {
            'previous_questions': [6],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 3
            }
        }
        res = self.client().get('/api/v1.0/quizzes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    def test_quizzes_wrong_url(self):
        quiz = {
            'previous_questions': [8],
            'quiz_category': {
                'type': 'Entertainment',
                'id': 3
            }
        }
        res = self.client().get('/api/v1.0/quizes', json=quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
