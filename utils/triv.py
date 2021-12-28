from typing import List
import aiohttp
from faker import Faker
from random import shuffle
from html import unescape
from typing import Union

_API = 'https://opentdb.com/api.php?amount=1&type=multiple'
chrome = Faker().chrome

class Triv:
    __slots__ = (
        'category',
        'type',
        'difficulty',
        'question',
        'correct_answer',
        'answers',
        'time',
    )
    __DIFFICULTY = {
        'hard': 10,
        'medium': 12,
        'easy': 15,
    }
    def __init__(self,
                category: str, 
                q_type: str, 
                difficulty: str, 
                question: str,
                correct_answer: str, 
                incorrect_answers: List[str]):
        self.category = category
        self.type = q_type
        self.difficulty = difficulty
        self.question = question
        self.correct_answer = correct_answer
        self.time = self.__DIFFICULTY[self.difficulty]
        self.answers = [correct_answer, *incorrect_answers]
        shuffle(self.answers)

async def get_trivia() -> Union[Triv, None]:
    user_agent = chrome(version_from=80, version_to=86, build_from=4100, build_to=4200)
    async with aiohttp.ClientSession() as session:
        async with session.get(_API, headers={'User-agent': user_agent}) as res:
            json = await res.json()

    if json['response_code'] != 0:
        return None
    json = json['results'][0]

    clean_q = unescape(json['question'])
    clean_ans = unescape(json['correct_answer'])
    clean_inc_ans = [unescape(s) for s in json['incorrect_answers']]
    return Triv(
        json['category'],
        json['type'],
        json['difficulty'],
        clean_q,
        clean_ans,
        clean_inc_ans,
    )
