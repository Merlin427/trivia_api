import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  def paginate_questions(request, questions_list):
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE

      questions = [question.format() for question in questions_list]
      paginated_questions = questions[start:end]
      return paginated_questions

  def get_category_list():
      categories = {}
      for category in Category.query.all():
          categories[category.id]= category.type

      return categories


  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET POST PATCH, DELETE, OPTIONS')
      return response


  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error': 400,
        'message': "Bad request"
      })

  @app.errorhandler(404)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': "Not found"
      })

  @app.errorhandler(422)
  def bad_request(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': "Unprocessable entity"
      })

  @app.route('/api/categories', methods=['GET'])
  def get_categories():
      try:

          categories = Category.query.all()
          formatted_categories = [category.format() for category in categories]

          return jsonify({
            'success':True,
            'categories': formatted_categories

          })
      except:
          abort(500)


  @app.route('/api/questions', methods=['GET'])
  def get_questions():

      questions_list = Question.query.all()
      paginated_questions=paginate_questions(request, questions_list)

      categories = Category.query.order_by(Category.type).all()

      if len(paginated_questions) == 0:
          abort(404)

      return jsonify({
      'success': True,
      'questions': paginated_questions,
      'total_questions': len(questions_list),
      'categories': get_category_list(),
      'current_category': None

      })

  @app.route('/api/questions/<int:q_id>', methods=['DELETE'])
  def delete_question(q_id):
      question = Question.query.get(q_id)

      if not question:
          abort(404)

      else:
          try:
              question.delete()

              return jsonify({

                'success': True,
                'deleted': q_id

              })
          except:
              abort(422)




  @app.route('/api/questions', methods=['POST'])
  def post_question():
      body = request.get_json()

      if (body['question'].strip()=="") or (body['answer'].strip()==""):
          abort(400)
      try:
          new_question = Question(question=body['question'].strip(), answer=body['answer'].strip(),\
          category=body['category'], difficulty=body['difficulty'])
          new_question.insert()

      except:
          abort(422)

      return jsonify({
        'success':True,
        'added': new_question.id
      })

  @app.route('/api/questions_search', methods=['POST'])
  def search_question():
      body = request.get_json()

      if 'searchTerm' in body:
          search_term = body['searchTerm'].strip()

          questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

          results = [q.format() for q in questions]

          return jsonify({
            'success':True,
            'questions': results
          })

  @app.route('/api/categories/<int:category_id>/questions')
  def get_by_category(category_id):
      questions = Question.query.filter_by(category=str(category_id)).all()

      questions_list = paginate_questions(request, questions)
      if len(questions_list)==0:
          abort(404)

      return jsonify({
        'success':True,
        'questions': questions_list,
        'total_questions': len(questions),
        'categories': Category.query.get(category_id).format(),
        'current_category': category_id


      })



  #'''
  #@TODO:
  #Create a GET endpoint to get questions based on category.

  #TEST: In the "List" tab / main screen, clicking on one of the
  #categories in the left column will cause only questions of that
  #category to be shown.



  #@TODO:
  #Create a POST endpoint to get questions to play the quiz.
  #This endpoint should take category and previous question parameters
  #and return a random questions within the given category,
  #if provided, and that is not one of the previous questions.

  #TEST: In the "Play" tab, after a user selects "All" or a category,
  #one question at a time is displayed, the user is allowed to answer
  #and shown whether they were correct or not.
  #'''



  return app
