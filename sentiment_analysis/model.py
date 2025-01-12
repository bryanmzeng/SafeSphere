from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import pipeline
from keybert import KeyBERT

app = Flask(__name__)
CORS(app)

class ReviewAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="distilbert-base-uncased-finetuned-sst-2-english",
            return_all_scores=True
        )
        self.key_phrase_extractor = KeyBERT('distilbert-base-nli-mean-tokens')
    
    def analyze_review(self, review_text):
        sentiment_results = self.sentiment_analyzer(review_text)[0]
        sentiment_scores = {score['label']: score['score'] for score in sentiment_results}
        
        sentiment = 'POSITIVE' if sentiment_scores['POSITIVE'] > sentiment_scores['NEGATIVE'] else 'NEGATIVE'
        confidence = max(sentiment_scores.values())
        
        key_points = self.key_phrase_extractor.extract_keywords(
            review_text,
            keyphrase_ngram_range=(1, 3),
            stop_words='english',
            use_maxsum=True,
            nr_candidates=20,
            top_n=3
        )
        
        return {
            'sentiment': sentiment,
            'confidence': confidence,
            'key_points': [{'phrase': phrase, 'relevance': score} for phrase, score in key_points]
        }

analyzer = ReviewAnalyzer()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    review_text = data.get('text', '')
    
    if not review_text:
        return jsonify({'error': 'No text provided'}), 400
        
    try:
        results = analyzer.analyze_review(review_text)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)