import re
from collections import Counter

import nltk
import pymorphy2

# Load NLTK data
download_dir = 'services/tags/nltk_data'
nltk.data.path.append(download_dir)

nltk.download('punkt', download_dir=download_dir)
nltk.download('stopwords', download_dir=download_dir)
nltk.download('wordnet', download_dir=download_dir)
nltk.download('punkt_tab', download_dir=download_dir)

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Settings
stop_words_en = set(stopwords.words('english'))
stop_words_ru = set(stopwords.words('russian'))

lemmatizer_en = WordNetLemmatizer()
morph_ru = pymorphy2.MorphAnalyzer()


def clean_text(text: str) -> str:
    """Cleaning text: lowercasing, removing punctuation."""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def tokenize_text(text: str) -> list:
    """Tokenize text and remove stop words."""
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t not in stop_words_en and t not in stop_words_ru]
    return tokens


def lemmatize_tokens(tokens: list) -> list:
    """Lemmatize tokens for both English and Russian."""
    lemmas = []
    for t in tokens:
        # English words
        if re.match(r'^[a-z]+$', t):
            lemmas.append(lemmatizer_en.lemmatize(t))
        # Russian words
        else:
            lemmas.append(morph_ru.parse(t)[0].normal_form)
    return lemmas


def extract_tags(tokens: list, top_n=10) -> list:
    """Get the most common tokens as tags."""
    counter = Counter(tokens)
    most_common = counter.most_common(top_n)
    return [tag for tag, freq in most_common]


def generate_tags(text: str, top_n=10) -> list:
    """Full pipeline to generate tags from text."""
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    lemmas = lemmatize_tokens(tokens)
    tags = extract_tags(lemmas, top_n=top_n)
    return tags
