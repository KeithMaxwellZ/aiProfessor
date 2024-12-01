import json
import random
import re
from pprint import pprint
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


def generateSummary(transcript_file_path: str, raw=True):
    content = ("Summarize the following transcript from a lecture with bulletin points "
               "and reference to timestamps using the following format, "
               "skip segments with length less than 60 seconds  \n"
               "** {start time} - {end time}: {main topic}**\n"
               "- {subtopic 1}\n"
               "- {subtopic 2}\n"
               "- {subtopic 3}\n")
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
    if raw:
        return c.message.content
    else:
        res = []
        pl = {
            "main_topic": "",
            "time_start": "",
            "time_end": "",
            "subtopics": []
        }
        ctx = c.message.content
        for i in ctx.splitlines():
            print(i)
            if i is None or len(i) == 0:
                if pl is not None:
                    res.append(pl)
                    pl = {
                        "main_topic": "",
                        "time_start": "",
                        "time_end": "",
                        "subtopics": []
                    }
            elif i.startswith("**"):
                temp = i.replace("*", "")
                segments = temp.split(":")
                times = segments[0].split("-")
                pl["time_start"] = times[0]
                pl["time_end"] = times[1]
                pl["main_topic"] = segments[1]
            else:
                pl["subtopics"].append(i[1:])

        with open(f"{transcript_file_path}.sum", "w") as fl:
            json.dump(res, fl, indent=4)
        return res




def generate_multiple_choice(summary: str, num_questions: int = 5) -> List[Dict]:
    questions = []
    # Implementation for multiple choice questions
    # This is a placeholder - you'd need to implement actual question generation logic
    for i in range(num_questions):
        question = {
            "type": "multiple_choice",
            "question": f"Multiple choice question {i + 1} based on the summary",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A"
        }
        questions.append(question)
    return questions


def generate_true_false(target_file: str) -> List[Dict]:
    trc_file = f"./data/{target_file}.out"
    summary_file = f"./data/{target_file}.out.sum"
    with open(summary_file, "r") as f:
        summary = json.load(f)
    trc = []
    with open(trc_file, "r") as f:
        t = f.readline()
        while t != "":
            print(t)
            temp1 = t.split("|")
            temp2 = temp1[0].split("-")
            trc.append((float(temp2[0]), float(temp2[1]), temp1[1]))
            t = f.readline()
    # Implementation for true/false questions
    questions = []
    for entry in summary:
        t_end = float(entry["time_end"])
        t_start = float(entry["time_start"])
        if t_end - t_start > 30:
            pl = []
            for l in trc:
                if t_start < l[0] < t_end:
                    pl.append(l[2])
            proc = '\n'.join(pl)
            content = (f"Generate a True/False question about the topic based on the following transcript "
                       f"in the following format: Format: **Question** -> --Answer--\n "
                       f"Transcript: \n {proc}")
            gpt_res = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professor in an University"},
                    {
                        "role": "user",
                        "content": content
                    }
                ]
            )

            try:
                expr = r"\*\*(.*)\*\* -> --(.*)--"
                match_res = re.search(expr, str(gpt_res.choices[0].message.content))

                question = {
                    "timestamp": t_end,
                    "type": "true_false",
                    "question": match_res.group(1),
                    "correct_answer": match_res.group(2)
                }
                questions.append(question)
            except:
                continue

    return questions


def generate_fill_in_blank(summary: str, num_questions: int = 5) -> List[Dict]:
    questions = []
    # Implementation for fill-in-the-blank questions
    for i in range(num_questions):
        question = {
            "type": "fill_in_blank",
            "question": f"Fill in the blank question {i + 1} based on the summary: ____",
            "correct_answer": "Answer"
        }
        questions.append(question)
    return questions


def generate_quiz(summary: str, num_multiple_choice: int = 3, num_true_false: int = 3, num_fill_in_blank: int = 3) -> \
List[Dict]:
    quiz = []
    quiz.extend(generate_multiple_choice(summary, num_multiple_choice))
    quiz.extend(generate_true_false(summary, num_true_false))
    quiz.extend(generate_fill_in_blank(summary, num_fill_in_blank))
    random.shuffle(quiz)
    return quiz


if __name__ == '__main__':
    tf_quiz = generate_true_false("sample3.mp4")
    print(tf_quiz)
