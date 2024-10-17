import json
import random
from typing import List, Dict

from openai import OpenAI
from openai.types.chat.chat_completion import Choice

with open("info.json") as f:
    tres = json.load(f)
key = tres["gpt-key"]
client = OpenAI(
    api_key=key,
    organization="org-abSUbwS8ofIBUQbREDwFHMhf",
    project="proj_kd6CuSBkuv00acr6easmItye"
)

def generateSummary(transcript_file_path: str):
    content = "Summarize the following transcript from a lecture with bulletin points and reference to timestamps: \n"
    with open(transcript_file_path, 'r') as f:
        t = f.read()
    content += t
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a professor in an University"},
            {
                "role": "user",
                "content": content
            }
        ]
    )

    c: Choice = res.choices[0]
    print(c.message.content)

    return c.message.content


def generate_multiple_choice(summary: str, num_questions: int = 5) -> List[Dict]:
    questions = []
    # Implementation for multiple choice questions
    # This is a placeholder - you'd need to implement actual question generation logic
    for i in range(num_questions):
        question = {
            "type": "multiple_choice",
            "question": f"Multiple choice question {i+1} based on the summary",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A"
        }
        questions.append(question)
    return questions

def generate_true_false(summary: str, num_questions: int = 5) -> List[Dict]:
    questions = []
    # Implementation for true/false questions
    for i in range(num_questions):
        question = {
            "type": "true_false",
            "question": f"True/False question {i+1} based on the summary",
            "correct_answer": random.choice([True, False])
        }
        questions.append(question)
    return questions

def generate_fill_in_blank(summary: str, num_questions: int = 5) -> List[Dict]:
    questions = []
    # Implementation for fill-in-the-blank questions
    for i in range(num_questions):
        question = {
            "type": "fill_in_blank",
            "question": f"Fill in the blank question {i+1} based on the summary: ____",
            "correct_answer": "Answer"
        }
        questions.append(question)
    return questions

def generate_quiz(summary: str, num_multiple_choice: int = 3, num_true_false: int = 3, num_fill_in_blank: int = 3) -> List[Dict]:
    quiz = []
    quiz.extend(generate_multiple_choice(summary, num_multiple_choice))
    quiz.extend(generate_true_false(summary, num_true_false))
    quiz.extend(generate_fill_in_blank(summary, num_fill_in_blank))
    random.shuffle(quiz)
    return quiz