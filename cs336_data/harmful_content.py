import fasttext
import fastwarc
import resiliparse
from fastwarc import ArchiveIterator, WarcRecordType
from resiliparse import extract, parse
from resiliparse.extract import html2text
from resiliparse.parse import encoding
from resiliparse.parse.encoding import detect_encoding, bytes_to_str


model_hatespeech = fasttext.load_model('/Users/rigvedavangipurapu/Documents/Stanford CS336 assignment 4/jigsaw_fasttext_bigrams_hatespeech_final.bin')
model_offensive = fasttext.load_model('/Users/rigvedavangipurapu/Documents/Stanford CS336 assignment 4/jigsaw_fasttext_bigrams_nsfw_final.bin')

def identify_hatespeech(unicode_text: str) -> str:
    labels, prob = model_hatespeech.predict(unicode_text)
    return labels[0].replace('__label__', ''), prob[0]

def identify_nsfw(unicode_text: str) -> str:
    labels, prob = model_offensive.predict(unicode_text)
    return labels[0].replace('__label__', ''), prob[0]

print(identify_hatespeech("I hate you"))
print(identify_nsfw("Love you")) 