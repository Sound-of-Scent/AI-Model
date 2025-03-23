from perfume_bot.recommendation.scoring import calculate_category_match_score

class RecommendationEngine:
    def __init__(self, fragrances, mood_blends):
        self.fragrances = fragrances
        self.mood_blends = mood_blends
    
    def recommend(self, user_profile, limit=1):
        """사용자 프로필 기반 향수 블렌드 추천"""
        # 1. 후보 블렌드 선택
        candidates = []
        
        # 상황 키워드 기반 필터링
        if user_profile.situation_keywords:
            for blend in self.mood_blends:
                # 키워드 교집합 확인
                if any(k in blend.keywords for k in user_profile.situation_keywords):
                    candidates.append(blend)
        
        # 후보가 없으면 감정 상태 기반 선택
        if not candidates:
            for blend in self.mood_blends:
                if user_profile.emotional_state == 'positive' and blend.sentiment_scores['positive'] > 0.6:
                    candidates.append(blend)
                elif user_profile.emotional_state == 'negative' and blend.sentiment_scores['negative'] > 0.6:
                    candidates.append(blend)
                elif user_profile.emotional_state == 'neutral' and blend.sentiment_scores['neutral'] > 0.4:
                    candidates.append(blend)
        
        # 후보가 없으면 모든 블렌드 사용
        if not candidates:
            candidates = self.mood_blends
        
        # 2. 각 후보 블렌드에 대한 점수 계산
        scored_candidates = []
        for blend in candidates:
            # 카테고리 일치 점수 계산
            match_score = calculate_category_match_score(
                blend, 
                self.fragrances, 
                user_profile.category_preferences
            )
            
            # 감정 일치 점수 계산
            if user_profile.emotional_state:
                emotion_match = blend.sentiment_scores.get(user_profile.emotional_state, 0)
            else:
                emotion_match = 0.5
            
            # 최종 점수 계산 (카테고리 일치 70%, 감정 일치 30%)
            final_score = match_score * 0.7 + emotion_match * 0.3
            
            scored_candidates.append((blend, final_score))
        
        # 3. 점수 기준 정렬 및 상위 N개 선택
        scored_candidates.sort(key=lambda x: x[1], reverse=True)
        return [blend for blend, _ in scored_candidates[:limit]]