import spacy
import nltk
from nltk.tokenize import word_tokenize
from collections import Counter
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob  # Alternative for grammar checking

nlp = spacy.load("en_core_web_sm")

# Job-related keywords
JOB_KEYWORDS = {"python", "flask", "data science", "machine learning", "AI", "NLP"}

def extract_skills(text):
    words = word_tokenize(text.lower())
    found_skills = {word for word in words if word in JOB_KEYWORDS}
    return list(found_skills)

def extract_experience(text):
    experience_years = re.findall(r"(\d+)\s*years?", text, re.IGNORECASE)
    return int(experience_years[0]) if experience_years else 0

def calculate_relevance(text):
    job_description = "Looking for a Python developer with Flask experience and AI skills."
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([job_description, text])
    return cosine_similarity(vectors[0], vectors[1])[0][0]

# Alternative grammar checking using TextBlob
def check_grammar(text):
    blob = TextBlob(text)
    errors = sum(1 for sentence in blob.sentences if sentence.correct() == False)
    return errors, []  # TextBlob doesn't provide detailed messages

def analyze_resume(text):
    skills = extract_skills(text)
    experience = extract_experience(text)
    relevance_score = calculate_relevance(text)
    grammar_errors, grammar_suggestions = check_grammar(text)

    return {
        "skills": skills,
        "experience": experience,
        "relevance_score": round(relevance_score * 100, 2),
        "grammar_errors": grammar_errors,
        "grammar_suggestions": grammar_suggestions,
    }
