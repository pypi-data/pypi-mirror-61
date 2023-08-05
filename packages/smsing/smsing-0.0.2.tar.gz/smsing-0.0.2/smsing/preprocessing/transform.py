from typing import List
from nltk.stem import SnowballStemmer


def lemmatize(text: str, model, allowed_postags: List[str] = None) -> str:
    return " ".join(
        [
            token.lemma_
            for token in model(text)
            if (allowed_postags is None or token.pos_ in allowed_postags)
            if (token.lemma_ != "-PRON-")
        ]
    ).strip()


def stem(text: str, language: str = "english") -> str:
    return " ".join([SnowballStemmer().stem(word) for word in text.split()]).strip()


def to_lowercase(text: str) -> str:
    return text.lower()

