class MoodBlend:
    def __init__(self, id, mood_name, description, composition, effect, keywords, sentiment_scores):
        self.id = id
        self.mood_name = mood_name  
        self.description = description
        self.composition = composition
        self.effect = effect  
        self.keywords = keywords 
        self.sentiment_scores = sentiment_scores  
    
    def __str__(self):
        return f"MoodBlend({self.mood_name}: {self.description})"