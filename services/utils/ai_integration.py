import logging
from typing import List, Dict, Any
from django.conf import settings
from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import numpy as np

logger = logging.getLogger(__name__)

# Example configuration for AI models
AI_MODELS = {
    'text_classification': 'distilbert-base-uncased-finetuned-sst-2-english',
    'question_answering': 'distilbert-base-cased-distilled-squad',
    'summarization': 'sshleifer/distilbart-cnn-12-6'
}

class AIHandler:
    def __init__(self):
        self.text_classifier = pipeline('sentiment-analysis', model=AI_MODELS['text_classification'])
        self.qa_model = pipeline('question-answering', model=AI_MODELS['question_answering'])
        self.summarizer = pipeline('summarization', model=AI_MODELS['summarization'])
        self.tfidf_vectorizer = TfidfVectorizer()

    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classify the sentiment of the given text.
        """
        try:
            result = self.text_classifier(text)[0]
            return {
                'label': result['label'],
                'score': result['score']
            }
        except Exception as e:
            logger.error(f"Error classifying text: {e}")
            raise AIIntegrationException("Failed to classify text.")

    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on the given context.
        """
        try:
            result = self.qa_model(question=question, context=context)
            return result['answer']
        except Exception as e:
            logger.error(f"Error answering question: {e}")
            raise AIIntegrationException("Failed to answer question.")

    def summarize_text(self, text: str, max_length: int = 130) -> str:
        """
        Summarize the given text.
        """
        try:
            summary = self.summarizer(text, max_length=max_length, min_length=30, do_sample=False)[0]
            return summary['summary_text']
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            raise AIIntegrationException("Failed to summarize text.")

    def recommend_courses(self, user_profile: str, courses: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Recommend courses based on the user profile using TF-IDF vectorization.
        """
        try:
            course_descriptions = [course['description'] for course in courses]
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(course_descriptions)
            user_vector = self.tfidf_vectorizer.transform([user_profile])
            cosine_similarities = linear_kernel(user_vector, tfidf_matrix).flatten()
            related_course_indices = cosine_similarities.argsort()[-5:][::-1]
            
            recommendations = [
                {
                    'course_id': courses[i]['course_id'],
                    'course_name': courses[i]['course_name'],
                    'score': cosine_similarities[i]
                }
                for i in related_course_indices
            ]
            return recommendations
        except Exception as e:
            logger.error(f"Error recommending courses: {e}")
            raise AIIntegrationException("Failed to recommend courses.")
    
    def perform_text_analytics(self, text: str) -> Dict[str, Any]:
        """
        Perform multiple text analytics tasks on the given text.
        """
        try:
            sentiment = self.classify_text(text)
            summary = self.summarize_text(text)
            return {
                'sentiment': sentiment,
                'summary': summary
            }
        except Exception as e:
            logger.error(f"Error performing text analytics: {e}")
            raise AIIntegrationException("Failed to perform text analytics.")

class AIIntegrationException(Exception):
    """
    Custom exception for AI Integration errors.
    """
    pass

# Example usage:
# ai_handler = AIHandler()
# sentiment = ai_handler.classify_text("This is a great course!")
# print(sentiment)
