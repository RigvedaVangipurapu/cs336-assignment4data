# =============================================================================
# IMPORTS
# =============================================================================
import fasttext
import fastwarc
import resiliparse
from fastwarc import ArchiveIterator, WarcRecordType
from resiliparse import extract, parse
from resiliparse.extract import html2text
from resiliparse.parse import encoding
from resiliparse.parse.encoding import detect_encoding, bytes_to_str
import nltk
from nltk.tokenize import word_tokenize

# Download required NLTK data
nltk.download('punkt')
nltk.download('punkt_tab')


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def has_alpha(s: str) -> bool:
    """
    Check if a string contains at least one alphabetic character.
    
    Args:
        s: Input string to check
        
    Returns:
        True if string contains at least one alphabetic character, False otherwise
    """
    return any(c.isalpha() for c in s)


def less_than_50_non_symbol_words(unicode_text: str) -> bool:
    """
    Check if the text has fewer than 50 words containing alphabetic characters.
    
    Args:
        unicode_text: Input text to analyze
        
    Returns:
        True if fewer than 50 words have alphabetic characters, False otherwise
    """
    words = word_tokenize(unicode_text)
    non_symbol_words = [word for word in words if has_alpha(word)]
    return len(non_symbol_words) < 50


# =============================================================================
# MAIN QUALITY FILTER FUNCTION
# =============================================================================

def gopher_quality_filter(unicode_text: str) -> bool:
    """
    Apply Gopher quality filtering criteria to determine if text meets quality standards.
    
    Quality criteria:
    1. Must have 50-100,000 words
    2. Average word length must be 3-10 characters
    3. No more than 30% of lines can end with ellipsis
    4. Must have at least 50 non-symbol words
    5. At least 80% of words must contain alphabetic characters
    
    Args:
        unicode_text: Input text to filter
        
    Returns:
        True if text passes all quality criteria, False otherwise
    """
    
    # =====================================================================
    # CRITERION 1: Check ellipsis usage (must be done before text normalization)
    # =====================================================================
    lines = unicode_text.split('\n')
    count_ellipses = 0
    for line in lines:
        line = line.strip() 
        if line.endswith('...'):
            count_ellipses += 1

    if count_ellipses / len(lines) > 0.3:
        print("count_ellipses / len(lines) > 0.3", count_ellipses / len(lines))
        return False

    # =====================================================================
    # TEXT NORMALIZATION
    # =====================================================================
    # Convert to lowercase and normalize whitespace for word processing
    unicode_text = unicode_text.lower()
    unicode_text = unicode_text.replace('\n', ' ')
    unicode_text = unicode_text.replace('\r', ' ')
    unicode_text = unicode_text.replace('\t', ' ')
    unicode_text = ' '.join(unicode_text.split())  # Remove extra whitespace but keep single spaces

    # =====================================================================
    # CRITERION 2: Word count check (50-100,000 words)
    # =====================================================================
    num_words = len(word_tokenize(unicode_text))

    if num_words < 50 or num_words > 100000:
        print("num_words < 50 or num_words > 100000", num_words)
        return False

    # =====================================================================
    # CRITERION 3: Average word length check (3-10 characters)
    # =====================================================================
    mean_word_length = sum(len(word) for word in word_tokenize(unicode_text)) / num_words

    if mean_word_length < 3 or mean_word_length > 10:
        print("mean_word_length < 3 or mean_word_length > 10", mean_word_length)
        return False

    # =====================================================================
    # CRITERION 4: Non-symbol word count check (at least 50)
    # =====================================================================
    if less_than_50_non_symbol_words(unicode_text):
        print("less_than_50_non_symbol_words")
        return False

    # =====================================================================
    # CRITERION 5: Alphabetic character percentage check (at least 80%)
    # =====================================================================
    count_alpha = 0
    for word in word_tokenize(unicode_text):
        if has_alpha(word):
            count_alpha += 1

    if count_alpha / num_words < 0.8:
        print("count_alpha / num_words < 0.8", count_alpha / num_words)
        return False

    # =====================================================================
    # ALL CRITERIA PASSED
    # =====================================================================
    return True


# Test cases for gopher_quality_filter function
if __name__ == "__main__":
    print("Running test cases for gopher_quality_filter...")
    
    # Test 1: Valid text
    print("\nTest 1: Valid text")
    valid_text = """
    This is a well-written article about machine learning and artificial intelligence. 
    The content is informative and educational, providing valuable insights into 
    the field of computer science. Machine learning algorithms have revolutionized 
    how we approach data analysis and pattern recognition.
    """
    result = gopher_quality_filter(valid_text)
    print(f"Valid text result: {result} (expected: True)")
    
    # Test 2: Too short text
    print("\nTest 2: Too short text")
    short_text = "This is too short."
    result = gopher_quality_filter(short_text)
    print(f"Short text result: {result} (expected: False)")
    
    # Test 3: Too long text
    print("\nTest 3: Too long text")
    long_text = "This is a sentence. " * 50000  # ~100,000 words
    result = gopher_quality_filter(long_text)
    print(f"Long text result: {result} (expected: False)")
    
    # Test 4: Short words
    print("\nTest 4: Short words")
    short_words = "a b c d e f g h i j " * 10  # Average length ~1
    result = gopher_quality_filter(short_words)
    print(f"Short words result: {result} (expected: False)")
    
    # # Test 5: Long words
    # print("\nTest 5: Long words")
    # long_words = "extraordinarily extraordinarily extraordinarily extraordinarily " * 25
    # result = gopher_quality_filter(long_words)
    # print(f"Long words result: {result} (expected: False)")
    
    # # Test 6: Too many ellipses
    # print("\nTest 6: Too many ellipses")
    # ellipses_text = "This line ends with ellipsis...\n" * 40
    # ellipses_text += "This is a normal line.\n" * 10
    # result = gopher_quality_filter(ellipses_text)
    # print(f"Ellipses text result: {result} (expected: False)")
    
    # # Test 7: Few alphabetic words
    # print("\nTest 7: Few alphabetic words")
    # mixed_text = "123 456 789 012 345 " * 8  # 80% numbers
    # mixed_text += "word word word word word"  # 20% words
    # result = gopher_quality_filter(mixed_text)
    # print(f"Mixed text result: {result} (expected: False)")
    
    # # Test 8: Less than 50 non-symbol words
    # print("\nTest 8: Less than 50 non-symbol words")
    # short_non_symbol = "This is a short text with only a few words."
    # result = less_than_50_non_symbol_words(short_non_symbol)
    # print(f"Short non-symbol result: {result} (expected: True)")
    
    # # Test 9: Exactly 50 words
    # print("\nTest 9: Exactly 50 words")
    # exactly_50 = "word " * 50
    # result = less_than_50_non_symbol_words(exactly_50)
    # print(f"Exactly 50 words result: {result} (expected: False)")
    
    # # Test 10: Edge case - exactly 10 words
    # print("\nTest 10: Edge case - exactly 10 words")
    # exactly_10 = "one two three four five six seven eight nine ten"
    # result = gopher_quality_filter(exactly_10)
    # print(f"Exactly 10 words result: {result} (expected: True)")
    
    # print("\nAll test cases completed!")

    print(gopher_quality_filter("the with " * 100))

    numbers = ["2831823829", "(283)-182-3829", "(283) 182 3829", "283-182-3829"]
    for number in numbers:
        test_string = f"Feel free to contact me at {number} if you have any questions."
        print(gopher_quality_filter(test_string))