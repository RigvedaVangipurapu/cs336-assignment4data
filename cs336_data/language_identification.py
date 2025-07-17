import fasttext
import resiliparse
from fastwarc import ArchiveIterator, WarcRecordType
from resiliparse import extract, parse
from resiliparse.extract import html2text
from resiliparse.parse import encoding
from resiliparse.parse.encoding import detect_encoding, bytes_to_str


model = fasttext.load_model('/Users/rigvedavangipurapu/Documents/Stanford CS336 assignment 4/lid.176.bin')


def identify_language(unicode_text: str) -> str:
    unicode_text = unicode_text.replace('\n', ' ')
    labels, prob = model.predict(unicode_text)
    lang_code = labels[0].replace('__label__', '') 
    probability = prob[0]
    return lang_code, probability


print(identify_language('¡Hola mundo! 你好世界! Bonjour le monde! こんにちは世界! مرحبا بالعالم! Γεια σου Κόσμε!'))
print(identify_language('Hello, world!'))