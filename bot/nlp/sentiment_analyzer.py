class SentimentAnalyzer:
    def __init__(self):
        # 간단한 사전 기반 감정 분석을 위한 감정 어휘 목록
        self.positive_words = ["좋아", "행복", "기쁨", "즐거움", "설렘", "신남", "좋은"]
        self.negative_words = ["우울", "슬픔", "힘들어", "화가남", "스트레스", "불안", "짜증"]
    
    def analyze(self, text):
        """텍스트의 감정 분석"""
        normalized_text = text.lower()
        
        # 감정 점수 계산
        positive_score = 0
        negative_score = 0
        
        for word in self.positive_words:
            if word in normalized_text:
                positive_score += 1
        
        for word in self.negative_words:
            if word in normalized_text:
                negative_score += 1
        
        # 주요 감정 및 점수 결정
        total_score = positive_score + negative_score
        
        if total_score == 0:
            return {
                'dominant': 'neutral',
                'scores': {
                    'positive': 0,
                    'negative': 0,
                    'neutral': 1.0
                },
                'suggested_moods': ["생각 정리가 필요한 밤", "새 출발을 앞둔 날"]
            }
        
        positive_ratio = positive_score / total_score
        negative_ratio = negative_score / total_score
        
        if positive_score > negative_score:
            return {
                'dominant': 'positive',
                'scores': {
                    'positive': positive_ratio,
                    'negative': negative_ratio,
                    'neutral': 0
                },
                'suggested_moods': ["기쁜 날", "데이트 전날", "여행 떠나기 전날"]
            }
        else:
            return {
                'dominant': 'negative',
                'scores': {
                    'positive': positive_ratio,
                    'negative': negative_ratio,
                    'neutral': 0
                },
                'suggested_moods': ["우울한 날", "상사에게 혼난 날", "스트레스 받을 때"]
            }