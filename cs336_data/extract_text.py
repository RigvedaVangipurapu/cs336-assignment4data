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
    return resiliparse.extract.html2text.extract_plain_text(unicode_text)



text1 = b'\xff\xfeH\x00e\x00l\x00l\x00o\x00 \x00W\x00o\x00r\x00l\x00d\x00'
text2 = b'\n<!DOCTYPE html>\n<html lang="en">\n<head>\n  <meta charset="UTF-8">\n  <title>UTF-8 Demo</title>\n</head>\n<body>\n  <h1>Welcome! \xf0\x9f\x8e\x89</h1>\n  <p>This page supports UTF-8 characters like:</p>\n  <ul>\n    <li>Emojis: \xf0\x9f\x98\x80 \xf0\x9f\x91\x8d \xe2\x9d\xa4\xef\xb8\x8f</li>\n    <li>Currency symbols: \xe2\x82\xac \xc2\xa5 \xe2\x82\xb9</li>\n    <li>Math symbols: \xe2\x88\x91 \xe2\x88\x9e \xe2\x89\x88</li>\n    <li>Non-Latin text: \xe3\x81\x93\xe3\x82\x93\xe3\x81\xab\xe3\x81\xa1\xe3\x81\xaf, \xe0\xa4\xa8\xe0\xa4\xae\xe0\xa4\xb8\xe0\xa5\x8d\xe0\xa4\xa4\xe0\xa5\x87, \xd9\x85\xd8\xb1\xd8\xad\xd8\xa8\xd8\xa7</li>\n  </ul>\n</body>\n</html>\n'


print(detect_encoding(text2))
plaintext1 = bytes_to_str(text2, detect_encoding(text2))
print(plaintext1)

print(extract_text(plaintext1))

