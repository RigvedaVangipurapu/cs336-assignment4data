import re
import fastwarc
import resiliparse
from fastwarc import ArchiveIterator, WarcRecordType
from resiliparse import extract, parse
from resiliparse.extract import html2text
from resiliparse.parse import encoding
from resiliparse.parse.encoding import detect_encoding, bytes_to_str

def mask_emails(text: str) -> str:
    replaced_text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '|||EMAIL_ADDRESS|||', text)
    num_replacements = len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
    return (replaced_text, num_replacements)

def mask_phone_numbers(text: str) -> str:
    # Match +X-XXX-XXX-XXXX or XXX-XXX-XXXX
    replaced_numbers =  re.sub(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b', '|||PHONE_NUMBER|||', text)
    num_replacements = len(re.findall(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}\b', text))
    return (replaced_numbers, num_replacements)

def mask_ip_addresses(text: str) -> str:
    replaced_ip = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '|||IP_ADDRESS|||', text)
    num_replacements = len(re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text))
    return (replaced_ip, num_replacements)


def detect_encoding(text: bytes) -> str:
    return resiliparse.parse.encoding.detect_encoding(text)

def extract_text(unicode_text: str) -> str:
    return resiliparse.extract.html2text.extract_plain_text(bytes_to_str(unicode_text, detect_encoding(unicode_text)))

def mask_pii_from_warc(warc_file: str):
    results = dict()
    with open(warc_file, 'rb') as f:
        for i, record in enumerate(ArchiveIterator(f, WarcRecordType.response)):
            if i >= 100:
                break
            text = extract_text(record.reader.read())
            masked_text, _ = mask_emails(text)
            masked_text, _ = mask_phone_numbers(masked_text)
            masked_text, _ = mask_ip_addresses(masked_text)
            if masked_text != text:
                results[text[0:25]] = (record.record_id, masked_text[0:25])
    return results

# print(mask_emails('Hello, my email is test@example.com and my friend\'s email is friend@domain.co.in'))
# print(mask_phone_numbers('My phone number is 123-456-7890'))
# print(mask_ip_addresses('My IP address is 192.168.1.1'))

res = mask_pii_from_warc(r'/Users/rigvedavangipurapu/Documents/Stanford CS336 assignment 4/cs336-assignment4data/cs336_data/CC-MAIN-20250417135010-20250417165010-00065.warc.gz')
for key, value in res.items():
    print("Record ID: ",value[0], "Text: ", key)
    print("Masked Text: ", value[1])
    print('--------------------')