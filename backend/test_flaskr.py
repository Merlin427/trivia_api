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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'At what racetrack did Ayrton Senna die?',
            'answer': 'Imola',
            'category': '6',
            'difficulty': 1


        }
        self.quiz_category = {
            'previous_questions':[5,9],
            'quiz_category': {
            'type': 'History',
            'id':4
            }
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)

    def test_get_questions(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['questions'][0]['id'], 5)

    def test_if_paginated(self):
        res = self.client().get('/api/questions?page=2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertEqual(len(data['categories']),6)
        self.assertEqual(data['total_questions'],19)
        self.assertEqual(len(data['questions']), 9)

    def test_if_page_out_of_range(self):
        res = self.client().get('/api/questions?page=200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['error'], 404)


    def test_delete_question(self):

        new_question = Question(question=self.new_question['question'], answer=self.new_question['answer'], \
        category=self.new_question['category'], difficulty=self.new_question['difficulty'])
        new_question.insert()
        new_question_id=new_question.id

        all_question=Question.query.all()
        self.assertEqual(len(all_question), 20)

        res = self.client().delete(f'/api/questions/{new_question_id}')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], new_question_id)



    def test_delete_question_fail(self):
        res= self.client().delete(f'/api/questions/500')
        data = json.loads(res.data)
        self.assertEqual(data['error'], 404)



    def test_post_new_question(self):

        res = self.client().post('/api/questions', json=self.new_question)
        data = json.loads(res.data)
        nq_id = data['added']
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        res = self.client().delete(f'/api/questions/{nq_id}')

    def test_post_invalid_question(self):
        invalid_q = {
            'question': '',
            'answer': '',
            'category': '2',
            'difficulty': '3'
        }
        res = self.client().post('/api/questions', json = invalid_q)
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)

    def test_get_q_by_category(self):
        res = self.client().get('/api/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

        res = self.client().post('/api/categories/50/questions')
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 200) #Status code is 200 because it successfully returned json response

    def test_question_search(self):
        res = self.client().post('/api/questions_search', json={'searchTerm': ' bOx '}) #Looking for the word 'boxer'
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 1)

    def test_play_quiz(self):
        res = self.client().post('/api/quizzes', json=self.quiz_category)
        data= json.loads(res.data.decode('utf-8'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

# Some code borrowed from Udacity Knowledge questions and answers. Modified to suit case





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
