import requests
import json


def get_questions(text):
    # change to env variable
    url = 'localhost:4000/api/'
    res = requests.put(url, data=text)
    data = json.loads(res)
    return data["questions"]


def format_response(text):
    """ 
    {
    "statement": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket.",
    "questions": [
        {
            "Question": "What is Sachin Ramesh Tendulkar's career?",
            "Answer": "cricketer",
            "id": 1,
            "context": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team."
        },
        {
            "Question": "Where is Sachin Ramesh Tendulkar from?",
            "Answer": "india",
            "id": 2,
            "context": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team."
        },
        {
            "Question": "What is the best cricketer?",
            "Answer": "batsmen",
            "id": 3,
            "context": "He is widely regarded as one of the greatest batsmen in the history of cricket."
        }
    ]

    }
 """
    return 0
