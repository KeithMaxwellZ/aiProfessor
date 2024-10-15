# sumy.
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

# Bert
from summarizer import Summarizer

# bart.
from transformers import BartTokenizer, BartForConditionalGeneration

# t5.
from transformers import T5Tokenizer, T5ForConditionalGeneration


# handling input text as global.
with open('transcript_sample.txt', 'r', encoding='utf-8') as file:
    input_text = file.read()
        
def sumy():
    # Parse the input text
    parser = PlaintextParser.from_string(input_text, Tokenizer("english"))

    # Create an LSA summarizer
    summarizer = LsaSummarizer()

    # Generate the summary
    summary = summarizer(parser.document, sentences_count=30)  # You can adjust the number of sentences in the summary

    # Output the summary
    print("Original Text:")
    print(input_text)
    print("\nSummary:")
    for sentence in summary:
        print(sentence)


def bert():
    # Create a BERT extractive summarizer
    summarizer = Summarizer()

    # Generate the summary
    summary = summarizer(input_text, min_length=50, max_length=150)  # You can adjust the min_length and max_length parameters

    # Output the summary
    print("Original Text:")
    print(input_text)
    print("\nSummary:")
    print(summary)

def bart():
    # Load pre-trained BART model and tokenizer
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    # Tokenize and summarize the input text using BART
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=100, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)

    # Decode and output the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Original Text:")
    print(input_text)
    print("\nSummary:")
    print(summary)

def t5():
    # Load pre-trained T5 model and tokenizer
    model_name = "t5-small"
    tokenizer = T5Tokenizer.from_pretrained(model_name)
    model = T5ForConditionalGeneration.from_pretrained(model_name)

    # Tokenize and summarize the input text using T5
    inputs = tokenizer.encode("summarize: " + input_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=1500, min_length=1000, length_penalty=2.0, num_beams=10, early_stopping=True)

    # Decode and output the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    print("Original Text:")
    print(input_text)
    print("\nSummary:")
    print(summary)


# sumy()
# bert()
t5()
