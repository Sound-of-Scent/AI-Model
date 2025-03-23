import re
from perfume_bot.nlp.dict.mood_keywords import MOOD_KEYWORDS
from perfume_bot.nlp.dict.category_keywords import CATEGORY_KEYWORDS

class KeywordExtractor:
    def __init__(self):
        self.mood_keywords = MOOD_KEYWORDS
        self.category_keywords = CATEGORY_KEYWORDS
    
    def extract_mood_keywords(self, text):
        """감정/상황 관련 키워드 추출"""
        normalized_text = self._normalize_text(text)
        extracted_keywords = []
        
        # 각 무드 타입에 대해 키워드 매칭
        for mood_type, keywords in self.mood_keywords.items():
            for keyword in keywords:
                if keyword in normalized_text:
                    confidence = self._calculate_confidence(normalized_text, keyword)
                    extracted_keywords.append({
                        'type': 'mood',
                        'value': mood_type,
                        'keyword': keyword,
                        'score': confidence
                    })
        
        # 점수 기준 정렬
        return sorted(extracted_keywords, key=lambda k: k['score'], reverse=True)
    
    def extract_preference_keywords(self, text):
        """향 선호도 관련 키워드 추출"""
        normalized_text = self._normalize_text(text)
        extracted_keywords = []
        
        # 각 카테고리에 대해 키워드 매칭
        for category, keywords in self.category_keywords.items():
            for keyword in keywords:
                if keyword in normalized_text:
                    confidence = self._calculate_confidence(normalized_text, keyword)
                    extracted_keywords.append({
                        'type': 'preference',
                        'value': category,
                        'keyword': keyword,
                        'score': confidence
                    })
        
        # 점수 기준 정렬
        return sorted(extracted_keywords, key=lambda k: k['score'], reverse=True)
    
    def _normalize_text(self, text):
        """텍스트 정규화"""
        return text.lower().replace('  ', ' ')
    
    def _calculate_confidence(self, text, keyword):
        """키워드 신뢰도 계산"""
        # 키워드 위치 기반 신뢰도 (앞에 있을수록 중요도 상승)
        position = text.find(keyword) / len(text) if len(text) > 0 else 0
        position_factor = 1 - position
        
        # 키워드 길이 기반 신뢰도 (길수록 중요도 상승)
        length_factor = len(keyword) / 10
        
        return 0.5 + position_factor * 0.3 + length_factor * 0.2