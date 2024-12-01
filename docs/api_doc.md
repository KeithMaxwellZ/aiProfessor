# Upload Video (Submit Video Link)

Submit and download the target Youtube Video

**URL** : `/upload`

**Method** : `POST`

**Data example** All fields must be sent.

```json
{
    "link": "https://www.youtube.com/watch?v=Onf7AKGHBzg"
}
```

## Success Response

**Code** : `200 OK`

**Content examples**

Return the name of the video file, located at ./data/{file_name}.mp4

```json
{
    "file_name": "sample3"
}
```

## Notes

* No verification on backend

<br>
<br>  
<br>  

# Get Transcript

Submit and download the target Youtube Video

**URL** : `/transcript`

**Method** : `POST`

**Data example** All fields must be sent.

```json
{
    "raw": "False"
}
```

## Success Response

**Code** : `200 OK`

**Content examples**

Contains each line with corresponding starting and ending time.

```json
[
    {
        "line_start": "0.0",
        "line_end": "8.0",
        "line_text": "Hello, my name is Jeff Messier. I'm a professor in electrical and software engineering in the Schulick School of Engineering at the University of Calgary.\n"
    },
    {
        "line_start": "8.0",
        "line_end": "19.0",
        "line_text": "And this is the introduction to my lecture series on computer organization, computer architecture.\n"
    },
    ...
    ...
]
```

## Notes

* Data doesn't do anything at this moment as it was some depreciated codes, but just leave it there to make it works.  

<br>
<br>  
<br>  

# Get Summary

Submit and download the target Youtube Video

**URL** : `/summary`

**Method** : `Get`


## Success Response

**Code** : `200 OK`

**Content examples**

Contains summary of each topic, along with one key frame for this img and the starting/ending time of this topic.

```json
[
    {
        "main_topic": " Introduction to Course",
        "time_start": "0.0",
        "time_end": "101.0",
        "key_frame_img": [
            "frames/sample3_0.0 .png"
        ],
        "subtopics": [
            " Overview of the instructor and course subject.",
            " Focus on computer organization and architecture at the second-year undergraduate level.",
            " Course designed to bridge the gap between basic logic gates and software."
        ]
    },
    {
        "main_topic": " User Perspective and Interaction with Computers",
        "time_start": "140.0",
        "time_end": "546.0",
        "key_frame_img": [
            "frames/sample3_140.0 .png"
        ],
        "subtopics": [
            " Emphasis on the user's perspective of computer interaction.",
            " Discussion of various computing devices: personal computers, smartphones, and cars.",
            " Introduction of input-output (I-O) devices as the primary way users interact with their computers."
        ]
    },
    ...
    ...
]
```

## Notes

* N/A


<br>
<br>  
<br>  

# Get Quiz

Submit and download the target Youtube Video

**URL** : `/quiz`

**Method** : `Get`


## Success Response

**Code** : `200 OK`

**Content examples**

Contains the quiz questions for the whole video with their answers and the time when they are suppose to show up.

```json
[
    {
        "timestamp": 101.0,
        "type": "true_false",
        "question": "This lecture series on computer organization and architecture is intended for first-year undergraduate students.",
        "correct_answer": "False"
    },
    {
        "timestamp": 546.0,
        "type": "true_false",
        "question": "The user's perspective on computers primarily focuses on the hardware and internal components rather than the interaction with input/output devices.",
        "correct_answer": "False"
    },
    ...
    ...
]
```

## Notes

* N/A