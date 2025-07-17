import fasttext
import fastwarc
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

def detect_encoding(text: bytes) -> str:
    return resiliparse.parse.encoding.detect_encoding(text)

def extract_text(unicode_text: str) -> str:
    return resiliparse.extract.html2text.extract_plain_text(bytes_to_str(unicode_text, detect_encoding(unicode_text)))

def extract_language_from_warc(warc_file: str):
    results = dict()
    with open(warc_file, 'rb') as f:
        for i, record in enumerate(ArchiveIterator(f, WarcRecordType.response)):
            if i >= 20:
                break
            text = extract_text(record.reader.read())
            results[text[0:25]] = (record.record_id, identify_language(text))
    return results


# print(identify_language('¡Hola mundo! 你好世界! Bonjour le monde! こんにちは世界! مرحبا بالعالم! Γεια σου Κόσμε!'))
# print(identify_language('Hello, world!'))
res = extract_language_from_warc('/Users/rigvedavangipurapu/Documents/Stanford CS336 assignment 4/cs336-assignment4data/cs336_data/CC-MAIN-20250417135010-20250417165010-00065.warc.gz')
for key, value in res.items():
    print("Record ID: ",value[0], "Text: ", key)
    print("Language: ", value[1][0], "Probability: ", value[1][1])
    print('--------------------')