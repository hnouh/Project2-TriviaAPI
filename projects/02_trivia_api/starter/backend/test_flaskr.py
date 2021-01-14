import os
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
        self.database_path = "postgresql://{}@{}/{}".format('postgres:Ar648898','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            
            self.new_question= {
                "question":"Give one of top 10 questions asked on Google?",
                "answer":"how to draw?",
                "category":"5",
                "difficulty":"3"
            }
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # get questions
    def test_get_paginated_questions(self):
        res= self.client().get('/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['categories']))

    def test_404_sent_requesting_beyond_valid_page(self):
        res=self.client().get('/questions?page=1000', json={'difficulty':3})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'], 'resource not found')
    
    # delete question
    def test_delete_question(self):
        res= self.client().delete('/questions/5')
        data=json.loads(res.data)

        question=Question.query.filter(Question.id==5).one_or_none()

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['deleted'],5)
        self.assertTrue(len(data['questions']))
        self.assertEqual(question,None)

    def test_422_if_question_does_not_exist(self):
        res=self.client().delete('/questions/200')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'unprocessable')
    
    # create questions
    def test_create_new_question(self):
        res= self.client().post('/questions',json=self.new_question)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_405_if_question_creation_not_allowed(self):
        res=self.client().post('/questions/200', json=self.new_question)
        data=json.loads(res.data)

        self.assertEqual(res.status_code,405)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'method not allowed')

    # search questions
    def test_search_question(self):
        res= self.client().post('/searchQuestions',json={'searchTerm':"name"})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(len(data['questions']))

    def test_404_if_question_search_not_allowed(self):
        res=self.client().post('/searchQuestions/200', json={'searchTerm':'box'})
        data=json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'], 'resource not found')

    # get questions for specific category
    def test_get_category_questions(self):
        res= self.client().get('/categories/2/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions'])) 

    def test_422_sent_requesting_invalid_category_questions(self):
        res=self.client().get('/categories/200/questions')
        data=json.loads(res.data)

        self.assertEqual(res.status_code,422)
        self.assertEqual(data['success'],False)
        self.assertTrue(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()