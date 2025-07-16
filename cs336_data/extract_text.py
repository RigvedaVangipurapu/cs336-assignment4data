import fastwarc
import resiliparse
from fastwarc import ArchiveIterator, WarcRecordType
from resiliparse import extract, parse
from resiliparse.extract import html2text
from resiliparse.parse import encoding
from resiliparse.parse.encoding import detect_encoding, bytes_to_str



def detect_encoding(text: bytes) -> str:
    return resiliparse.parse.encoding.detect_encoding(text)

def extract_text(unicode_text: str) -> str:
    return resiliparse.extract.html2text.extract_plain_text(bytes_to_str(unicode_text, detect_encoding(unicode_text)))

def extract_text_from_warc(warc_file: str) -> str:
    i = 0
    with open(warc_file, 'rb') as f:
        for record in ArchiveIterator(f, WarcRecordType.response):
            text = extract_text(record.reader.read())
            return(text)


extract_text_from_warc(r'/Users/rigvedavangipurapu/Documents/Stanford CS336 assignment 4/cs336-assignment4data/cs336_data/CC-MAIN-20250417135010-20250417165010-00065.warc.gz')