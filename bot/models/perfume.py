class Fragrance:
    def __init__(self, id, name, categories, notes, description, mood_tags):
        self.id = id
        self.name = name
        self.categories = categories 
        self.notes = notes  
        self.description = description
        self.mood_tags = mood_tags  
    
    def __str__(self):
        return f"Fragrance({self.name}, {', '.join(self.categories)})"