import re

class MatcherService:
    @staticmethod
    def get_keywords(text):
        """Extract meaningful keywords from text."""
        if not text:
            return set()
        # Lowercase, remove non-alphanumeric, and split
        words = re.findall(r'\w+', text.lower())
        # Filter out common short words (basic stopwords)
        stopwords = {'a', 'an', 'the', 'and', 'or', 'if', 'to', 'in', 'is', 'it', 'of', 'for', 'with'}
        return {w for w in words if w not in stopwords and len(w) > 2}

    @staticmethod
    def calculate_score(query_keywords, doc_text):
        """Calculate overlap score between query keywords and document text."""
        if not doc_text:
            return 0
        doc_keywords = MatcherService.get_keywords(doc_text)
        overlap = query_keywords.intersection(doc_keywords)
        return len(overlap)

    @staticmethod
    def rank_incidents(query, incidents, top_n=3):
        """Rank incidents based on keyword overlap and return top N."""
        if not incidents or not query:
            return []
        
        query_keywords = MatcherService.get_keywords(query)
        scored_incidents = []
        
        for inc in incidents:
            # Match against issue description mainly
            score = MatcherService.calculate_score(query_keywords, inc.get('issue', ''))
            if score > 0:
                scored_incidents.append((score, inc))
        
        # Sort by score descending
        scored_incidents.sort(key=lambda x: x[0], reverse=True)
        
        # Return only the incident objects
        return [item[1] for item in scored_incidents[:top_n]]

    @staticmethod
    def determine_confidence(matches_count):
        """Determine confidence level based on match count."""
        if matches_count >= 2:
            return "High"
        elif matches_count == 1:
            return "Medium"
        else:
            return "Low"
