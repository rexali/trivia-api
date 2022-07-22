from crypt import methods
from email.errors import NonASCIILocalPartDefect
from logging import exception
import os
from unicodedata import category
from webbrowser import get
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import Category, Question, db
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request,selection):
  page = request.args.get('page',1,type=int)
  # start = 1 if (page <= 0) else (page - 1) * QUESTIONS_PER_PAGE
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection ]
  current_questions = questions[start:end]
  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins":"*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_rquest(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type, Authorization, True')
    response.headers.add('Access-Control-Allow-Methods','GET, POST, DELETE, PATCH, OPTIONS')

    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    # get categories
    categories = Category.query.all()
    categories_dict={}
    for category in categories:
      # create dictionary to hold the list
      categories_dict[category.id]= category.type

    return jsonify({'success':True,'categories':categories_dict})

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 


  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_questions():
    try:
      # get all questions
      questions = Question.query.order_by(Question.id).all()
      # get total number of questions
      total_questions = len(questions)
      # get questions in a page (10q)
      current_questions = paginate_questions(request,questions)
      # if page not found
      if(len(current_questions)==0):
        abort(404)
      # get all categories
      categories = Category.query.all()
      # create empty categories dictionary
      categories_dict={}
      # loop thru the categories
      for category in categories:
        # create dictionary to hold the list
        categories_dict[category.id]= category.type

      return jsonify({
        'success':True,
        'questions':current_questions,
        'total_questions':total_questions,
        'categories':categories_dict,
        # 'current_category':category.type
      })

    except Exception as e:
      print(e)
      abort(400)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:id>', methods=['DELETE'])
  def delete_question(id):
    try:
      question = Question.query.filter_by(id=id).one_or_none()
      # check if there is question
      if question is None:
        abort(404)
      question.delete()
      remaining_question = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request,remaining_question)
      return jsonify({
        'success':True,
        'question':current_questions,
        'total_questions':len(remaining_question)
      })

    except Exception as e:
      print(e)
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/question', methods=['POST'])
  def add_question():
    # get the questions from the form
    body = request.get_json()
    # get individaual properties
    question = body.get('question',None)
    answer = body.get('answer', None)
    category = body,get('category', None)
    difficulty = body.get('difficulty', None)

    try:
      # create question object
      question = Question(question=question,answer=answer,category=category, difficulty=difficulty)
      # add data to db
      question.delete()
      # send current questions to update the client 
      selection = Question.query.order_by(Question.id).all()
      current_questions = paginate_questions(request,selection)
      return jsonify({
        'success': True,
        'question_id':question.id,
        'questions':current_questions,
        'total_questions':len(selection)
      })
    except Exception as e:
      print(e)
      abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/search', methods=['POST'])
  def search_questions():
    # get post data
    body = body.get_json()
    # get searched term 
    search_term = body.get('search_term')
    # query the db for the questions that match
    questions = Question.query.filter('%'+search_term+'%').all()
    # check question found
    if questions:
      current_questions = paginate_questions(request,questions)
      
      return jsonify({
        'sucess':True,
        'questions':current_questions,
        'total_questions':len(questions)
      })
    else:
      abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:num>/questions')
  def questions_by_category(num):
    # get category by id
    category = Category.query.filter_by(id = num).one_or_none()
    # check if category is present
    if category:
      # get all the questions in the categories
      questions_in_category = Question.query.filter_by(category = num).all()
      current_questions = paginate_questions(request, questions_in_category)
      return jsonify({
        'success':True,
        'questions':current_questions,
        'total_questions':len(questions_in_category),
        'current_category':category.type
      })
    # if not category found
    else:
      abort(404)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes',methods=['POST'])
  def quiz():
    # get post data
    body = request.get_json()
    # get the properties
    quiz_category = body.get('quiz_category')
    previous_question = body.get('previous_question')

    try:
      # check
      if quiz_category['id']==0:
        questions_query = Question.query.all()
      else:
        questions_query = Question.query.filter_by(category=quiz_category['id']).all()
      
      random_index= random.randint(0,len(questions_query))
      next_question = questions_query[random_index]

      return jsonify({
        'success':True,
        'question':{
          'answer':next_question.answer,
          'category':next_question.category,
          'difficulty':next_question.difficulty,
          'id':next_question.id,
          'question':next_question.question,
        },
        'previous_question':previous_question
      })

    except Exception as e:
      print(e)
      abort(404)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success':False,
      'error':400,
      'message':"Bad request"
    })

  @app.errorhandler(404)
  def page_not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message':"Page not found"
    })

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success':False,
      'error':405,
      'message':"Method not allowed"
    })

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      'success':False,
      'error':500,
      'message':"Internal server error"
    })

  @app.errorhandler(422)
  def unable_to_process(error):
    return jsonify({
      'success':False,
      'error':422,
      'message':"Unable to process"
    })


  
  return app

    