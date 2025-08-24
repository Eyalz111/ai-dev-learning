# text_tools.py
def count_words(text):
    """Returns the number of words in the text"""
    return len(text.split())

def shout(text):
    """Returns the text in uppercase"""
    return text.upper()

def whisper(text):
    """Returns the text in lowercase"""
    return text.lower()

# This part ONLY runs when the file is run directly!
if __name__ == "__main__":
    print("Testing count_words:", count_words("Hello world"))
    print("Testing shout:", shout("hello"))