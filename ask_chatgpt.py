import json

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


def ask_gpt(transcript_file_path: str):
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
