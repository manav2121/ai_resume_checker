import pdfplumber
import re
import spacy
from pdf2image import convert_from_path
import pytesseract
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# List of skills to match
skills_list = {"Python", "Java", "Machine Learning", "SQL", "AI", "Data Science", "React", "Django"}

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF, using OCR if necessary."""
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                else:
                    # If no text is extracted, use OCR
                    images = convert_from_path(pdf_path)
                    for img in images:
                        text += pytesseract.image_to_string(img) + "\n"
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return ""
    
    return text.strip()

def extract_info(text):
    """Extract email and phone number from text using regex."""
    email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    phone_pattern = r"\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}"
    
    email = re.findall(email_pattern, text)
    phone = re.findall(phone_pattern, text)

    return {
        "Email": email[0] if email else "Not found",
        "Phone": phone[0] if phone else "Not found",
    }

def extract_skills(text):
    """Extract skills from the text."""
    doc = nlp(text)
    extracted_skills = set()

    # Check for single-word skills
    for token in doc:
        if token.text in skills_list:
            extracted_skills.add(token.text)

    # Check for multi-word skills (e.g., "Machine Learning")
    for chunk in doc.noun_chunks:
        if chunk.text in skills_list:
            extracted_skills.add(chunk.text)

    return extracted_skills

def calculate_similarity(resume_text, job_description):
    """Calculate cosine similarity between a resume and a job description."""
    if not resume_text.strip():
        return 0.0  # Return 0 if the resume has no text
    
    documents = [resume_text, job_description]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)

    return cosine_similarity(tfidf_matrix[0], tfidf_matrix[1].reshape(1, -1))[0][0]

# Example job description
job_description = "Looking for a Python developer with experience in machine learning, AI, and SQL."

# List of resumes to process
resumes = ["res_ai_1.pdf", "res_ai_2.pdf", "res_ai_3.pdf"]
ranked_resumes = []

for resume in resumes:
    text = extract_text_from_pdf(resume)
    if not text.strip():
        print(f"Skipping {resume}: No text extracted!")
        continue
    
    info = extract_info(text)
    skills = extract_skills(text)
    score = calculate_similarity(text, job_description)

    ranked_resumes.append((resume, score, info, skills))

# Sort resumes by match score (highest first)
ranked_resumes.sort(key=lambda x: x[1], reverse=True)

# Display results
print("\n📌 Top Ranked Resumes:")
for resume, score, info, skills in ranked_resumes:
    print(f"\n📄 {resume}")
    print(f"   🔹 Match Score: {score:.2f}")
    print(f"   📧 Email: {info['Email']}")
    print(f"   📞 Phone: {info['Phone']}")
    print(f"   💡 Skills: {', '.join(skills) if skills else 'None found'}")
