class UserProfile:
    def __init__(self):
        self.emotional_state = None  
        self.situation_keywords = [] 
        self.preference_keywords = []
        self.category_preferences = {}  
        self.intensity_preference = 3 
    
    def update_from_input(self, user_input, conversation_step, keyword_extractor, sentiment_analyzer):
        """Profile update"""
        # 감정 상태 및 상황 키워드 파악
        if conversation_step == 1:
            sentiment_result = sentiment_analyzer.analyze(user_input)
            self.emotional_state = sentiment_result['dominant']
            
            extracted_keywords = keyword_extractor.extract_mood_keywords(user_input)
            self.situation_keywords = [k['value'] for k in extracted_keywords]
            
            # 선호 카테고리 유추
            self._infer_preferred_categories()
            
        # 향 선호도 파악
        elif conversation_step == 2:
            preference_keywords = keyword_extractor.extract_preference_keywords(user_input)
            
            # 카테고리 선호도 업데이트
            for pref in preference_keywords:
                category = pref['value']
                score = pref['score']
                current_score = self.category_preferences.get(category, 0)
                self.category_preferences[category] = current_score + score
            
            # 강도 선호도 감지
            self._detect_intensity_preference(user_input)
    
    def _infer_preferred_categories(self):
        """감정 상태에서 선호 카테고리 유추"""
        if self.emotional_state == 'positive':
            self._add_category_preference('CITRUS', 0.6)
            self._add_category_preference('FLORAL', 0.5)
        elif self.emotional_state == 'negative':
            self._add_category_preference('WOODY', 0.6)
            self._add_category_preference('GREEN', 0.5)
    
    def _add_category_preference(self, category, score):
        """카테고리 선호도 추가"""
        current_score = self.category_preferences.get(category, 0)
        self.category_preferences[category] = current_score + score
    
    def _detect_intensity_preference(self, text):
        """향 강도 선호도 감지"""
        text = text.lower()
        if '강한' in text or '진한' in text:
            self.intensity_preference = 5
        elif '부드러운' in text or '은은한' in text:
            self.intensity_preference = 2