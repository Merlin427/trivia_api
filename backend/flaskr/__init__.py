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

  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
      'success': False,
      'error': 405,
      'message': "Method not allowed"
      })

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

      categories= Category.query.all()
      if categories==0:
          abort(422)



      try:
          categories = Category.query.order_by(Category.type).all()
          formatted_categories = {category.id: category.type for category in categories}

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

 # @app.route("/api/quizzes", methods=["POST"])
 # def get_quizzes():
#      data = request.get_json()
#      previous_questions = data.get("previous_questions")
#      quiz_category = data.get("quiz_category")
#      quiz_category_id = int(quiz_category["id"])

#      question = Question.query.filter(
#            Question.id.notin_(previous_questions)
#      )

        # quiz category id is 0 if all is selected and therefore false
#      if quiz_category_id:
#            question = question.filter_by(category=quiz_category_id)

        # limit result to only one question
#      question = question.first().format()

#      return jsonify({"success": True, "question": question, }), 200
#This code is borrowed from the Udacity Knowledge base posted by Yousra A

  @app.route('/api/quizzes', methods=['POST'])
  def play_quiz():
      body = request.get_json()
      previous_questions = body.get('previous_questions',[])
      quiz_category = body.get('quiz_category',None)

      try:
          category_id= int(quiz_category['id'])
          if quiz_category:
              if quiz_category['id']==0:
                  filter_question=Question.query.all()
              else:
                  filter_question = Question.query.filter_by(category = category_id).all()

          if not filter_question:
              return abort(422)
          data=[]
          for question in filter_question:
              if question.id not in previous_questions:
                  data.append(question.format())
          if len(data) != 0:
              result = random.choice(data)
              return jsonify({
                'success':True,
                'question': result
              })
          else:
              return jsonify({
                'question': False
              })
      except:
          abort(422)


# Some code borrowed from Udacity Knowledge questions and answers. Modified to suit case

  #if __name__ == '__main__':
#      app.run()



  return app
