from pymongo import MongoClient
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

client = MongoClient("your_mongodb_uri")
db = client.resume_analyzer
collection = db.resumes

def save_to_mongo(filename, analysis):
    existing_resumes = list(collection.find({}, {"text": 1}))
    vectorizer = TfidfVectorizer()
    all_texts = [resume["text"] for resume in existing_resumes] + [analysis["skills"]]
    
    if len(all_texts) > 1:
        vectors = vectorizer.fit_transform(all_texts)
        similarities = cosine_similarity(vectors[-1], vectors[:-1])
        if any(sim > 0.8 for sim in similarities[0]):
            analysis["plagiarism_detected"] = True

    collection.insert_one({"filename": filename, "analysis": analysis})
