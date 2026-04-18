import re

class MatcherService:
    @staticmethod
    def get_keywords(text):
        if not text: return set()
        words = re.findall(r'\w+', text.lower())
        stopwords = {'a', 'an', 'the', 'and', 'or', 'if', 'to', 'in', 'is', 'it', 'of', 'for', 'with'}
        return {w for w in words if w not in stopwords and len(w) > 2}

    @classmethod
    def rank_incidents(cls, query, incidents, top_n=3):
        if not incidents or not query: return []
        query_keywords = cls.get_keywords(query)
        scored = []
        for inc in incidents:
            text = f"{inc.get('issue', '')} {inc.get('tags', '')}"
            overlap = query_keywords.intersection(cls.get_keywords(text))
            if overlap: scored.append((len(overlap), inc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:top_n]]

    @staticmethod
    def determine_confidence(count):
        if count >= 2: return "High"
        if count == 1: return "Medium"
        return "Low"
