import logging
import os

from faster_whisper import WhisperModel
from tqdm import tqdm

from ProjectExceptions import VideoNotFound

model: WhisperModel = None

DEFAULT_MODEL_SIZE = "tiny.en"


def load_model(model_size: str = DEFAULT_MODEL_SIZE):
    global model
    logging.info(f"Loading model {model_size}")
    model = WhisperModel(model_size, device='cuda', compute_type="float32")


def analyze(file_name: str, raw=True):
    if os.path.isfile(f"./data/{file_name}.out"):
        with open(f"./data/{file_name}.out", 'r') as out:
            summary_text = out.read()
            return summary_text
    global model
    if model is None:
        logging.info("Model not loaded, initializing...")
        load_model()
    if os.path.isfile(f"./data/{file_name}"):
        logging.info("Target file found, ")
        segments, info = model.transcribe(f"./data/{file_name}", beam_size=5)
        pl = []
        t_dur = round(info.duration, 2)
        with tqdm(total=t_dur, unit="seconds") as pbar:
            for i in segments:

                pl.append(f"{round(i.start, 4)} - {round(i.end, 4)} | {i.text}")
                segment_dur = round(i.end - i.start, 2)
                pbar.update(segment_dur)
        summary_text = "\n".join(pl)
        with open(f"./data/{file_name}.out", 'w') as out:
            out.write(summary_text)
        return summary_text
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
    res = analyze("sample3.mp4")
    with open("transcript_sample.txt", 'w') as f:
        f.write(res)
