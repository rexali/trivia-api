# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## ToDo Tasks
These are the files you'd want to edit in the backend:

1. *./backend/flaskr/`__init__.py`*
2. *./backend/test_flaskr.py*


One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 


2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 


3. Create an endpoint to handle GET requests for all available categories. 


4. Create an endpoint to DELETE question using a question ID. 


5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 


6. Create a POST endpoint to get questions based on category. 


7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 


8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 


9. Create error handlers for all expected errors including 400, 404, 422 and 500. 



## Review Comment to the Students

```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints

GET     '/api/v1.0/categories'
GET     '/api/v1.0/questions'
GET     '/api/v1.0/categories/<int:id>/questions'
POST    '/api/v1.0/questions'
POST    '/api/v1.0/questions/search'
POST    '/api/v1.0/quizzes'
DELETE  '/api/v1.0/questions/<int:id>'


GET '/api/v1.0/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
    {
        '1' : "Science",
        '2' : "Art",
        '3' : "Geography",
        '4' : "History",
        '5' : "Entertainment",
        '6' : "Sports"
    }

GET '/api/v1.0/question'
- Fetches a dictionary of categories, a list of questions and total number of question.

  - The dictionary of categories is with ids and its corresponding values of string of the category
  - The list of questions is with answer, category, difficulty, id, and question as keys and their values are. 
    in string, string, integer, integer and string respectively.
  - The total_question is in integer

- Request Arguments: None
- Returns: An object with multiple keys: categories, question, and total_question of key:value pairs. 
       {
        "categories": {
                "1": "Science", 
                "2": "Art", 
                "3": "Geography", 
                "4": "History", 
                "5": "Entertainment", 
                "6": "Sports"
               }, 
        "questions": [
            {
                "answer": "Lake Victoria", 
                "category": 3, 
                "difficulty": 2, 
                "id": 13, 
                "question": "What is the largest lake in Africa?"
            },
            ], 
        "success": true, 
        "total_questions": 19
       }

GET     '/api/v1.0/categories/<int:id>/questions'
- Fetches to a current category, a list of questions under the category, and number of the question in key-value pairs
  - The current_category is a key with its value in string
  - The list of dictionaries of questions with keys such as answer, category, difficulty, id, and question  with corresponding 
    values in string, string, number, number and string respectively
  - The total_questions is a key with its value in string

- Request Arguments: request with an id e.g

        {
            id:2
        }

- Return: An object with multiple keys: current_category, questions, and total_questions of key:value pairs.

        {
        "current_category": "Science", 
        "questions": [
            {
            "answer": "The Liver", 
            "category": 1, 
            "difficulty": 4, 
            "id": 20, 
            "question": "What is the heaviest organ in the human body?"
            }, 
        
        ], 
        "success": true, 
        "total_questions": 3

  POST    '/api/v1.0/questions'
  - Add a new dictionary of question with mutiple key such question, answer, difficulty and category to the database 
  - Request Arguments:  request with question, answer, difficulty and category e.g
        {
            'question':''who is this, 
            'answer':'me', 
            'difficulty':1 ,
            'category':'Art',
        }
  - Returns: An object with a single key, success, that contains a object of success: boolean key:value pair. 
        {
            'success':true
        }

POST    '/api/v1.0/questions/search'
- Fetches a list of dictionary of questions by searching with a specific term with key and its value
- Request Arguments: request with search term e.g
        {
            search_term : 'Who is'
        }
- Returns: An object with multiple keys: categories,  that contains a object of id: category_string key:value pairs e.g.
        {
            'question' : "Science",
            'total_questions' : "Art",
            'current_category' : "Geography",
        }

POST    '/api/v1.0/quizzes'
- Post a new quiz with quizz category and previous question as keys and their corresponding values
- Request Arguments: request with an object of quizz_category and previous_question e.g
        {
        'quiz_category': {
                    'type':'Entertainment',
                    'id':3
                    },
        'previous_questions':[4] 
        }
- Returns: An object with multipe keys of questions and previous_questions e.g.
        { 
        'question':{
            'answer':'Home',
            'category':'Science',
            'difficulty':2,
            'id':1,
            'question':'What is this',
            },

            'previous_questions':'How are you?
        }

DELETE  '/api/v1.0/questions/<int:id>'
- Delete a dictionary of question with mutiple key such question, answer, difficulty and category in the database 
- Request Arguments:  request with id e.g
        {
            'id':3
        }
- Returns: An object with a single key, success, that contains a object of success: boolean key:value pair. 
        {
            'success':true
        }

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
