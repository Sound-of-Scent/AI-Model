def calculate_category_match_score(blend, fragrances, preferred_categories):
    """카테고리 일치 점수 계산"""
    if not preferred_categories:
        return 0.5  # 선호도 정보 없을 경우 중간 점수
    
    total_score = 0
    total_weight = 0
    
    # 블렌드의 각 구성 요소 검사
    for component in blend.composition:
        # 해당 향수 정보 찾기
        fragrance = next((f for f in fragrances if f.id == component['fragrance_id']), None)
        
        if fragrance:
            # 카테고리 일치 여부 확인
            match_score = 0
            for category in fragrance.categories:
                if category in preferred_categories:
                    # 해당 카테고리의 선호도 점수 반영
                    match_score += preferred_categories[category]
            
            # 구성 비율만큼 가중치 적용
            weight = component['percentage'] / 100
            total_score += match_score * weight
            total_weight += weight
    
    # 정규화된 점수 반환
    return total_score / total_weight if total_weight > 0 else 0