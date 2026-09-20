import os
import glob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ProtocolRetriever:
    def __init__(self, protocols_dir="data/protocols"):
        self.protocols = []
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Load protocols
        for filepath in glob.glob(os.path.join(protocols_dir, "*.md")):
            with open(filepath, 'r') as f:
                content = f.read()
                filename = os.path.basename(filepath)
                self.protocols.append({
                    "document_id": filename,
                    "section_title": content.split('\n')[0].replace('#', '').strip() if content else filename,
                    "text_excerpt": content
                })
                
        if self.protocols:
            texts = [p['text_excerpt'] for p in self.protocols]
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
        else:
            self.tfidf_matrix = None

    def find_protocol(self, trigger_features_text):
        """
        Returns the best matching protocol excerpt based on the trigger features.
        """
        if not self.protocols or not self.tfidf_matrix is not None:
            return None
            
        # Vectorize query
        query_vec = self.vectorizer.transform([trigger_features_text])
        
        # Calculate similarities
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        best_match_idx = similarities.argmax()
        best_score = similarities[best_match_idx]
        
        # Only return if we have a somewhat meaningful match
        if best_score > 0.05:
            return self.protocols[best_match_idx]
            
        return None

if __name__ == "__main__":
    retriever = ProtocolRetriever()
    match = retriever.find_protocol("patient has low spo2 and high respiratory rate")
    print(match['document_id'] if match else "No match")
