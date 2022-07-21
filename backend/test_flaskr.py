from encodings import search_function
import os
from typing_extensions import Self
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','postgres','localhost', self.database_name)

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
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test pagination

    def test_paginate_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))

    def test_questions_page_error(self):
        res = self.client().get("/questions?page=0")
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertNotEqual(data["success"], True)

    def test_bad_request_error(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertNotEqual(data["success"], True)
        self.assertTrue(data["error"],False)

    # test categories

    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_get_categories_error(self):
        res = self.client().delete("/categories")
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    # test question

    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["categories"]))
        self.assertTrue(len(data["questions"]))
    
    def test_get_question_error(self):
        res = self.client().delete("/question")
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)
    
    # test delete question

    def test_delete_question(self):
        res = self.client().delete("/questions/2")
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)

    def test_delete_question(self):
        res = self.client().post("/questions/2")
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)


   # test add question
    def test_add_question(self):
        new_question = {
            'question':'Who is your father?',
            'answer':'James',
            'difficulty':1,
            'category':1
        }
        res = self.client().post("/questions",json = new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)

    def test_add_question(self):
        new_question = {
            'question':'Who is your father?',
            'answer':'James',
            'difficulty':1,
            'category':1
        }
        res = self.client().get("/questions",json = new_question)
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)

    # test search

    def test_search_question(self):
        search_term = {'search_term':'What is your father name?'}
        res = self.client().post("/search",json = search_term )
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertEqual(len(data['questions']),10)

    def test_search_question(self):
        search_term = {'search_term':'What is your father name?'}
        res = self.client().get("/search",json = search_term )
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["error"], 405)
        
    # test question by categories

    def test_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertNotEqual(len(data['questions']),0)
        self.assertEqual(data['current_category'], 'Science')

    def test_questions_by_category_error(self):
        res = self.client().post('/categories/1/questions')
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertTrue(data["success"], False)
        self.assertTrue(data["error"], 405)
    
    # test quiz
    
    def test_quiz(self):
        quiz = {
            'previous_questions':[13],
            'quiz_category':{
                'type':'Entertainment',
                'id':3
            }
        }
        res = self.client().post('/quiz', json = quiz)
        data = json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['question']['category'], '3')

    def test_quiz(self):
        quiz = {
            'previous_questions':[13],
            'quiz_category':{
                'type':'Entertainment',
                'id':3
            }
        }
        res = self.client().get('/quiz', json = quiz)
        data = json.loads(res.data)
        self.assertNotEqual(res.status_code,200)
        self.assertTrue(data["success"], False)
        self.assertTrue(data["error"], 405)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()