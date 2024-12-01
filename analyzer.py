import logging
import os

from faster_whisper import WhisperModel
from tqdm import tqdm

from ProjectExceptions import VideoNotFound

model: WhisperModel = None

DEFAULT_MODEL_SIZE = "tiny.en"


def load_model():
    model_size = "medium"
    model = WhisperModel(model_size, device='cpu', compute_type="float32")
    return model


def analyze(file_name: str, raw=True):
    print(file_name)
    if os.path.isfile(f"./data/{file_name}.out"):
        with open(f"./data/{file_name}.out", 'r') as out:
            curr_line = out.readline()
            pl = []
            while curr_line != "":
                t1 = curr_line.split("|")
                t2 = t1[0].replace(" ", "")
                t3 = t2.split("-")
                line_info = {
                    "line_start": t3[0],
                    "line_end": t3[1],
                    "line_text": t1[1][2:]
                }
                pl.append(line_info)
                curr_line = out.readline()
            return pl
    global model
    if model is None:
        logging.info("Model not loaded, initializing...")
        load_model()
    print(f"data/{file_name}.mp4")
    print(os.path.isfile(f"./data/{file_name}.mp4"))
    if os.path.isfile(f"./data/{file_name}.mp4"):
        logging.info("Target file found, ")
        segments, info = model.transcribe(f"./data/{file_name}.mp4", beam_size=5)
        pl = []
        t_dur = round(info.duration, 2)
        with tqdm(total=t_dur, unit="seconds") as pbar:
            for i in segments:
                line = {
                    "line_start": round(i.start, 4),
                    "line_end": round(i.end, 4),
                    "line_text": i.text
                }
                pl.append(line)
                pl.append(f"{round(i.start, 4)} - {round(i.end, 4)} | {i.text}")
                segment_dur = round(i.end - i.start, 2)
                pbar.update(segment_dur)
        summary_text = "\n".join(pl)
        with open(f"./data/{file_name}.mp4.out", 'w') as out:
            out.write(summary_text)
        return pl
        # if raw:
        #     return segments
        # else:
        #     return proc(segments)
    else:
        logging.warning(f"Target file {file_name} not found")
        raise VideoNotFound("Video not found")


def proc(raw_dict) -> str:
    proc_list = []
    for i in raw_dict:
        proc_list.append(f"{i['start']:07.2f} | {i['end']:07.2f} | {i['text']}")
    return "\n".join(proc_list)


if __name__ == '__main__':
    res = analyze("Owner Snaps At Waitress For Telling The Truth ｜ Kitchen Nightmares FULL EPISODE")
    # with open("transcript_sample.txt", 'w') as f:
    #     f.write(res)
    file_name = "Gordon Baffled By 'Thin Crust Pizza' ｜ Kitchen Nightmares FULL EPISODE.mp4"
    p = f"./data/{file_name}"
    print(p)
    r = os.path.isfile(f"./data/{file_name}")
    print(r)
