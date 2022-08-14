from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import Category, Question
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#  pagination of the question
def get_questions_per_page(request, selection):
    # get initial page value from the rquest
    page = request.args.get('page', 1, type=int)
    # get number of questions on a page
    begin = (page - 1) * QUESTIONS_PER_PAGE
    # get  number of question for next page
    next = begin + QUESTIONS_PER_PAGE
    # get all the question from given current question in db
    questions = [question.format() for question in selection]
    # get the list of page questions
    page_questions = questions[begin:next]
    # return the current question
    return page_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample
    route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # @app.route("/")
    # def hello_world():

    #   return "Hello World!"

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_rquest(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization, True')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, DELETE, PATCH, OPTIONS')

        return response
    '''
    @TODO: Create an endpoint to handle GET requests for all
    available categories
    '''
    @app.route('/api/v1.0/categories')
    def get_categories():
        # let us get all categories
        cats = Category.query.all()
        # let create dict to hold the list of categories
        cat_dict = {}
        # loop thru each of the categories
        for cat in cats:
            # add each category id and its type to the dictionary
            cat_dict[cat.id] = cat.type
            # return the json of categories

        return jsonify({'success': True, 'categories': cat_dict})

    '''
    @TODO:Create an endpoint to handle GET requests for questions,
    including get_questions_per_page (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    TEST: At this point, when you start the application
    you should see que stions and categories generated,
    ten questions per page and get_questions_per_page at the bottom of
    the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''
    @app.route('/api/v1.0/questions')
    def get_questions():
        try:
            # let us get all questions
            questions = Question.query.order_by(Question.id).all()
            # get total number of questions
            total_questions = len(questions)
            # get questions in a page
            current_questions = get_questions_per_page(request, questions)
            # if page not found
            if (len(current_questions) == 0):
                abort(404)
            # get all categories
            categories = Category.query.all()
            # create empty categories dictionary
            categories_dict = {}
            # loop thru the categories
            for category in categories:
                # create dictionary to hold the list
                categories_dict[category.id] = category.type

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': total_questions,
                'categories': categories_dict,
                'current_category': categories_dict,
            })

        except Exception as e:
            print(e)
            abort(400)

    '''
    @TODO: Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.'''
    @app.route('/api/v1.0/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            # get a question with the given id
            question = Question.query.filter_by(id=id).one_or_none()

            # check if the question is empty
            if question is None:
                # then stop operation
                abort(404)

            # delete the question that matched the id
            try:
                # delete now
                question.delete()
                # get the remaining question after deletion fro the db
                remaining_question = Question.query.order_by(Question.id).all()
            except Exception as e:
                print(e)
            # get the questions to be displayed currentyly on the page
            current_questions = get_questions_per_page(
                request, remaining_question)

            return jsonify({
                'success': True,
                'question': current_questions,
                'total_questions': len(remaining_question)
            })

        except Exception as e:
            print(e)
            abort(404)

    '''
    @TODO: Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.
    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end
    of the last page of the questions list in the "List" tab.
    '''
    @app.route('/api/v1.0/questions', methods=['POST'])
    def add_question():
        # get the post data from the form and convert to json
        form_data = request.get_json()
        # get individaual properties or form field: questio,answer,
        # category and difficulty
        question = form_data.get('question')
        answer = form_data.get('answer')
        category = form_data.get('category')
        difficulty = form_data.get('difficulty')
        # try to create the question object
        try:
            # create now
            question = Question(question=question, answer=answer,
                                category=category, difficulty=difficulty)
            # add data to db
            question.insert()
            # get resulting questions to update the client
            resulting_questions = Question.query.order_by(Question.id).all()
            # get question to be on the first page
            current_questions = get_questions_per_page(
                request, resulting_questions)

            return jsonify({
                'success': True,
                'question_id': question.id,
                'questions': current_questions,
                'total_questions': len(resulting_questions)
            })
        except Exception as e:
            print(e)
            abort(404)

    '''
    @TODO: Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term is
    a substring of the question.
    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/api/v1.0/questions/search', methods=['POST'])
    def search_questions():
        # get the form data from the request
        form_data = request.get_json()
        # get searched term  from the form data
        search_term = form_data.get('searchTerm')
        # query the db for the questions that match with this:
        # questions = Question.query.filter(Question.question.
        # contains(search_term)).all() or below code line
        questions = Question.query.filter(Question.question.like(
            '%s%s%s' % ('%', search_term, '%'))).all()
        # check question found
        if questions:
            # get the initial page questions
            current_questions = get_questions_per_page(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
            })

        else:
            abort(404)

    '''
    @TODO: Create a GET endpoint to get questions based on category.
    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/api/v1.0/categories/<int:id>/questions')
    def questions_by_category(id):
        # get a category by its id
        category = Category.query.filter_by(id=id).one_or_none()
        # check if category is present
        if category:
            # get all the questions with the given id if not empty
            category_questions = Question.query.filter_by(category=id).all()
            # get the initial page questions
            initial_questions = get_questions_per_page(
                request, category_questions)

            return jsonify({
                'success': True,
                'questions': initial_questions,
                'total_questions': len(category_questions),
                'current_category': category.type
            })
        # if not category found
        else:
            abort(404)

    '''@TODO: Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    @app.route('/api/v1.0/quizzes', methods=['POST'])
    def quiz():
        # get post data from the form
        form_data = request.get_json()
        # get the catgory of the quiz from the form
        quiz_category = form_data.get('quiz_category')
        # get the previous questions from the form
        previous_questions = form_data.get('previous_question')

        try:
            # check that quiz category is 0
            if quiz_category['id'] == 0:
                # get all the questions if true
                questions = Question.query.all()
            else:
                # get all the questions non-zero id
                questions = Question.query.filter_by(
                    category=quiz_category['id']).all()
            # get random number betw zero and total questions
            random_number = random.randint(0, len(questions))
            # get the next questions randomly using random number
            next_question = questions[random_number]

            return jsonify({
                'success': True,
                'question': {
                    'answer': next_question.answer,
                    'category': next_question.category,
                    'difficulty': next_question.difficulty,
                    'id': next_question.id,
                    'question': next_question.question,
                },
                'previous_questions': previous_questions
            })

        except Exception as e:
            print(e)
            abort(404)

    '''
    @TODO: Create error handlers for all expected errors
    including 404 and 422.
    '''

    # error handlers for 400: Bad request
    @app.errorhandler(400)
    def bad_request(error):

        return jsonify({
            'success': False,
            'error': 400,
            'message': "Bad request"
        })

    # error handlers for 404: Page not found
    @app.errorhandler(404)
    def page_not_found(error):

        return jsonify({
            'success': False,
            'error': 404,
            'message': "Page not found"
        })

    # error handlers for 405: Method not allowed
    @app.errorhandler(405)
    def method_not_allowed(error):

        return jsonify({
            'success': False,
            'error': 405,
            'message': "Method not allowed"
        })

    # error handlers for 500: Internal server error
    @app.errorhandler(500)
    def internal_server_error(error):

        return jsonify({
            'success': False,
            'error': 500,
            'message': "Internal server error"
        })

    # error handlers for 422: Unable to process
    @app.errorhandler(422)
    def unable_to_process(error):

        return jsonify({
            'success': False,
            'error': 422,
            'message': "Unable to process"
        })

    return app
