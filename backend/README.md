# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
If you do not have PostgrSQL installed, install this first (https://www.postgresql.org/download/). From within the
With Postgres running, first create the database 'trivia' by running 'postgres=# create database trivia;',
now restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Documentation


### GET '/api/categories'


- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a list of objects of id: category_string key:value pairs.


##### Example: 'curl http://localhost:5000/api/categories'



{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    }
  ],
  "success": true
}

### GET '/api/questions?page=1'


- Fetches the questions to be displayed on page requested.
- Paginates the response to limit questions to 10 per page.
- Request arguments:'page' = Page number requested
- The response body is as follows:

 "categories": A dictionary of categories with 'id' and 'type'

 "current_category": null

 "questions": A list of formatted question objects.

 "success": True (Indicates a successful request)

 "total_questions": The total number of questions.


#### Example: 'curl http://localhost:5000/api/questions?page=1'



{
  "categories": {
    "1": "Science",
    "2": "Art",
    ....
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, ....

  ],
  "success": true,
  "total_questions": 19
}

### DELETE '/api/questions/<int:q_id>'


- Deletes a question from the database.
- Request arguments: question_id
- If the delete is successful, this returns a 'success' status along with the deleted question id


#### Example: 'curl -X DELETE http://localhost:5000/api/questions/25'

{
  "deleted": 25,
  "success": true
}

### POST '/api/questions'


- Allows the user to post a new question.
- Request arguments: the question data is sent via 'application/json' type.
- If successful a 'success' status along with the id of the new question is returned
- Request body:

question: The question

answer: The answer

difficulty: Dropdown menu with difficulty ratings from 1-5

category: Dropdown menu with category types

#### Example: "curl -X POST http://localhost:5000/api/questions -H "Content-Type: application/json" -d '{"question": "At which racetrack did Ayrton Senna die?", "answer": "Imola", "category": "6", "difficulty": 1}'"

{
  "added": 26,
  "success": true
}


### POST '/api/questions_search'


- Fetches questions using partial, (case-insensitive) string matching based on a search term.
- Request body: search term
- If successful, the request returns a 'success' status, along with all of the questions based on the search term.


#### Example: "curl -X POST http://localhost:5000/api/questions_search -H "Content-Type: application/json" -d '{"searchTerm": "SennA"}'"



{
  "questions": [
    {
      "answer": "Imola",
      "category": 6,
      "difficulty": 1,
      "id": 26,
      "question": "At which racetrack did Ayrton Senna die?"
    }
  ],
  "success": true
}


### GET '/api/categories/<int:category_id>/questions'


- Fetches all of the questions of a particular category.
- Request arguments: category_id
- If successful, the request returns a 'success' status, the number of questions in that category, along with all the questions of the chosen category.


#### Example: 'curl http://localhost:5000/api/categories/2/questions'


{
  "categories": {
    "id": 2,
    "type": "Art"
  },
  "current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}


### POST '/api/quizzes'

- Starts a new Trivia Game.
- If no category is selected, it returns a random question (that has not been asked) from all the available questions.
- If a category is selected, it returns a random question (that has not been asked) from the available questions in that category.
- Request arguments: category_id, previous_questions
- If successful a 'success' status is returned, along with a random question.
- Once 5 questions have been returned, or there are no more available questions in a given category, the API will return a 'success' status, but with no question. This will let the react front end know the game is over.



#### Example: "curl -d '{"previous_questions": [2],"quiz_category": {"type":"Geography","id": "2"}}' -H 'Content-Type: application/json' -X POST http://127.0.0.1:5000/api/quizzes"


{
  "question": {
    "answer": "Scarab",
    "category": 3,
    "difficulty": 4,
    "id": 24,
    "question": "Which dung beetle was worshipped by the ancient Egyptians?"
  },
  "success": true
}



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python3 test_flaskr.py
```
