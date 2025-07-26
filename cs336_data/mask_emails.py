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
    original_text = text
    # Normalize spaces: replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Debug: print normalized text
    print(f"DEBUG - Normalized text: '{text}'")
    
    # Track number of replacements
    num_replacements = 0
    
    # Pattern 1: Basic 10-digit numbers (1234567890)
    pattern1 = r'\b\d{10}\b'
    new_text = re.sub(pattern1, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern1, text))
        text = new_text
    
    # Pattern 2: Numbers with dashes (123-456-7890)
    pattern2 = r'\b\d{3}-\d{3}-\d{4}\b'
    new_text = re.sub(pattern2, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern2, text))
        text = new_text
    
    # Pattern 3: Numbers with parentheses and dashes ((123) 456-7890)
    pattern3 = r'\(\d{3}\) \d{3}-\d{4}'
    new_text = re.sub(pattern3, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern3, text))
        text = new_text
    
    # Pattern 4: Numbers with parentheses and spaces ((123) 456 7890)
    pattern4 = r'\(\d{3}\) \d{3} \d{4}'
    new_text = re.sub(pattern4, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        print(f"DEBUG - Pattern 4 matched: {len(re.findall(pattern4, text))} matches")
        num_replacements += len(re.findall(pattern4, text))
        text = new_text
    
    # Pattern 5: Numbers with dots (123.456.7890)
    pattern5 = r'\b\d{3}\.\d{3}\.\d{4}\b'
    new_text = re.sub(pattern5, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern5, text))
        text = new_text
    
    # Pattern 6: Numbers with spaces (123 456 7890)
    pattern6 = r'\b\d{3} \d{3} \d{4}\b'
    new_text = re.sub(pattern6, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern6, text))
        text = new_text
    
    # Pattern 7: Mixed separators (123 456-7890)
    pattern7 = r'\b\d{3} \d{3}-\d{4}\b'
    new_text = re.sub(pattern7, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern7, text))
        text = new_text
    
    # Pattern 8: With country code (+1 123-456-7890)
    pattern8 = r'\b\+1 \d{3}-\d{3}-\d{4}\b'
    new_text = re.sub(pattern8, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern8, text))
        text = new_text
    
    # Pattern 9: With country code and parentheses (+1 (123) 456-7890)
    pattern9 = r'\+1 \(\d{3}\) \d{3}-\d{4}'
    new_text = re.sub(pattern9, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern9, text))
        text = new_text
    
    # Pattern 10: Edge case - no space after closing paren ((123)456-7890)
    pattern10 = r'\(\d{3}\)\d{3}-\d{4}'
    new_text = re.sub(pattern10, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        num_replacements += len(re.findall(pattern10, text))
        text = new_text
    
    # Pattern 11: Parentheses with dash immediately after ((123)-456-7890)
    pattern11 = r'\(\d{3}\)-\d{3}-\d{4}'
    new_text = re.sub(pattern11, '|||PHONE_NUMBER|||', text)
    if new_text != text:
        print(f"DEBUG - Pattern 11 matched: {len(re.findall(pattern11, text))} matches")
        num_replacements += len(re.findall(pattern11, text))
        text = new_text
    
    return (text, num_replacements)


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

numbers = ["2831823829", "(283)-182-3829", "(283) 182 3829", "283-182-3829"]
for number in numbers:
    test_string = f"Feel free to contact me at {number} if you have any questions."
    print(mask_phone_numbers(test_string))
    print('--------------------')
    print( "Feel free to contact me at |||PHONE_NUMBER||| if you have any questions.")