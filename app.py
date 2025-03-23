import json
from perfume_bot.models.fragrance import Fragrance
from perfume_bot.models.mood_blend import MoodBlend
from perfume_bot.nlp.keyword_extractor import KeywordExtractor
from perfume_bot.nlp.sentiment_analyzer import SentimentAnalyzer
from perfume_bot.recommendation.recommendation_engine import RecommendationEngine
from perfume_bot.conversation.conversation_manager import ConversationManager

def load_data():
    # 향수 정보 로드
    with open('data/fragrances.json', 'r', encoding='utf-8') as f:
        fragrances_data = json.load(f)
    
    fragrances = []
    for data in fragrances_data:
        fragrance = Fragrance(
            data['id'],
            data['name'],
            data['categories'],
            data['notes'],
            data['description'],
            data['mood_tags']
        )
        fragrances.append(fragrance)
    
    # 기분별 블렌드 로드
    with open('data/mood_blends.json', 'r', encoding='utf-8') as f:
        mood_blends_data = json.load(f)
    
    mood_blends = []
    for data in mood_blends_data:
        mood_blend = MoodBlend(
            data['id'],
            data['mood_name'],
            data['description'],
            data['composition'],
            data['effect'],
            data['keywords'],
            data['sentiment_scores']
        )
        mood_blends.append(mood_blend)
    
    return fragrances, mood_blends

def main():
    """Application Main"""
    print("System Started")
    
    # 데이터 로드
    fragrances, mood_blends = load_data()
    print(f"Loaded perfume #: {len(fragrances)}, Blends: {len(mood_blends)}개")
    
    # 컴포넌트 초기화
    keyword_extractor = KeywordExtractor()
    sentiment_analyzer = SentimentAnalyzer()
    recommendation_engine = RecommendationEngine(fragrances, mood_blends)
    
    # 대화 관리자 생성
    conversation_manager = ConversationManager(
        keyword_extractor,
        sentiment_analyzer,
        recommendation_engine
    )
    
    # 대화 시작
    print("\n" + conversation_manager.process_message(""))
    
    # 대화 루프
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["end", "quit", "exit"]:
            print("Chatbot: 좋은 하루 되세요!")
            break
        
        response = conversation_manager.process_message(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()