from enum import Enum
from perfume_bot.models.user_profile import UserProfile
from perfume_bot.conversation.response_generator import ResponseGenerator

class DialogState(Enum):
    GREETING = 0
    MOOD_INQUIRY = 1
    PREFERENCE_INQUIRY = 2
    RECOMMENDATION = 3
    FAREWELL = 4

class ConversationManager:
    def __init__(self, keyword_extractor, sentiment_analyzer, recommendation_engine):
        self.keyword_extractor = keyword_extractor
        self.sentiment_analyzer = sentiment_analyzer
        self.recommendation_engine = recommendation_engine
        self.response_generator = ResponseGenerator()
        
        self.state = DialogState.GREETING
        self.user_profile = UserProfile()
        self.conversation_count = 0
        self.recommended_blend = None
    
    def process_message(self, user_message):
        """사용자 메시지 처리 및 응답 생성"""
        self.conversation_count += 1
        
        # 현재 상태에 따른 처리
        if self.state == DialogState.GREETING:
            # 첫 인사 후 감정/상황 파악 질문으로 전환
            self.state = DialogState.MOOD_INQUIRY
            return self.response_generator.generate_greeting()
            
        elif self.state == DialogState.MOOD_INQUIRY:
            # 첫 번째 대화: 감정/상황 파악
            self.user_profile.update_from_input(
                user_message, 
                1, 
                self.keyword_extractor, 
                self.sentiment_analyzer
            )
            
            # 다음 단계: 선호도 파악
            self.state = DialogState.PREFERENCE_INQUIRY
            return self.response_generator.generate_preference_inquiry(self.user_profile)
            
        elif self.state == DialogState.PREFERENCE_INQUIRY:
            # 두 번째 대화: 선호도 파악
            self.user_profile.update_from_input(
                user_message, 
                2, 
                self.keyword_extractor, 
                self.sentiment_analyzer
            )
            
            # 추천 엔진으로 블렌드 추천
            recommended_blends = self.recommendation_engine.recommend(self.user_profile)
            self.recommended_blend = recommended_blends[0] if recommended_blends else None
            
            # 다음 단계: 추천 제공
            self.state = DialogState.RECOMMENDATION
            return self.response_generator.generate_recommendation(self.recommended_blend, self.user_profile)
            
        elif self.state == DialogState.RECOMMENDATION:
            # 이미 추천을 제공했으므로 마무리
            self.state = DialogState.FAREWELL
            return self.response_generator.generate_farewell()
            
        else:
            # 대화 종료 상태
            return self.response_generator.generate_farewell()