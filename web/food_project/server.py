from flask import Flask, request, jsonify, render_template
from ultralytics import YOLO
from PIL import Image
import os
import io
import pandas as pd
import re

app = Flask(__name__, static_folder='static', template_folder='templates')

# YOLO 모델 로드
model = YOLO('yolol_best.pt')

# 잘못된 클래스 이름을 올바르게 재매핑하기 위한 딕셔너리
class_remap = {
    "불고기": "떡갈비",  # 불고기로 예측된 경우 떡갈비로 출력
    "삼겹살": "불고기",  # 삼겹살 -> 불고기
    "장어구이": "삼겹살",  # 장어구이 -> 삼겹살
    "조개구이": "장어구이",  # 조개구이 -> 장어구이
    "떡국": "조개구이",  # 떡국 -> 조개구이
    "무국": "떡국",  # 무국 -> 떡국
    "미역국": "무국",  # 미역국 -> 무국
    "북엇국": "미역국",  # 북엇국 -> 미역국
    "시래기국": "북엇국",  # 시래기국 -> 북엇국
    "콩나물국": "시래기국",  # 콩나물국 -> 시래기국
    "콩자반": "콩나물국",  # 콩자반 -> 콩나물국
    "편육": "콩자반",  # 편육 -> 콩자반
    "갓김치": "편육",  # 갓김치 -> 편육
    "깍두기": "갓김치",  # 깍두기 -> 갓김치
    "무생채": "깍두기",  # 무생채 -> 깍두기
    "배추김치": "무생채",  # 배추김치 -> 무생채
    "백김치": "배추김치"  # 백김치 -> 배추김치
}

# 레시피 데이터 로드 (ID와 함께 로드)
korean_recipes = pd.read_excel('recipe.xlsx')
english_recipes = pd.read_excel('recipe_english.xlsx')

# 음식 이름과 카테고리를 매칭하는 딕셔너리
category_dict = {
    '구이': ['갈비구이', '갈치구이', '고등어구이', '곱창구이', '닭갈비', '떡갈비', '불고기', '삼겹살', '장어구이', '조개구이', '숯불닭갈비', '등갈비', 'LA갈비'],
    '국': ['떡국', '무국', '미역국', '북엇국', '시래기국', '콩나물국', '만두국', '김치콩나물국', '매운무국'],
    '탕': ['갈비탕', '감자탕', '매운탕', '삼계탕', '추어탕'],
    '김치': ['갓김치', '깍두기', '무생채', '배추김치', '백김치', '오이소박이', '총각김치', '파김치'],
    '나물': ['고사리나물', '시금치나물', '숙주나물'],
    '무침': ['가지볶음', '미역줄기볶음', '애호박볶음', '꽈리고추무침', '콩나물무침', '도토리묵', '잡채'],
    '찌개': ['김치찌개', '닭계장', '동태찌개', '된장찌개', '순두부찌개'],
    '조림': ['갈치조림', '감자조림', '고등어조림', '두부조림', '메추리알장조림', '연근조림'],
    '죽': ['전복죽', '호박죽'],
    '볶음': ['감자채볶음', '두부김치', '떡볶이', '멸치볶음', '소세지볶음', '어묵볶음', '오징어채볶음', '제육볶음', '주꾸미볶음'],
    '밥': ['김치볶음밥', '누룽지', '비빔밥', '주먹밥', '김밥'],
    '면': ['막국수', '물냉면', '비빔냉면', '수제비', '열무국수', '잔치국수', '쫄면', '칼국수', '콩국수'],
    '전': ['감자전', '김치전', '파전', '호박전'],
    '부침': ['계란말이'],
    '찜': ['갈비찜', '김치찜', '닭볶음탕', '수육', '찜닭', '족발', '순대'],
    '장': ['간장게장', '양념게장', '깻잎장아찌'],
    '후식': ['약과', '약식', '한과'],
    '음청류': ['수정과', '식혜'],
    '회': ['육회'],
    '떡': ['송편'],
    '고기': ['편육']
}

# 레시피를 반환하는 함수 (ID 기반으로 검색)
def get_recipe_by_id(dish_id, language='korean'):
    if language == 'korean':
        recipe_df = korean_recipes
    else:
        recipe_df = english_recipes
    
    # ID와 일치하는 레시피를 검색
    recipe_data = recipe_df[recipe_df['ID'] == dish_id]
    
    if recipe_data.empty:
        return None  # 해당 ID의 레시피가 없을 경우 None 반환

    recipe_info = {
        'dish_name': recipe_data['Dish'].values[0],  # 음식 이름
        'ingredients': recipe_data['Ingredients'].values[0],  # 재료
        'instructions': recipe_data['Recipe'].values[0],  # 레시피 설명
        'image_url': recipe_data['Image_URL'].values[0]  # 이미지 경로
    }
    return recipe_info

# 잘못된 클래스를 올바르게 재매핑하는 함수
def remap_class_name(class_name):
    return class_remap.get(class_name, class_name)

# 홈 페이지
@app.route('/')
def index():
    return render_template('home.html')

# 예측 요청 처리
@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    file = request.files['image']
    img = Image.open(io.BytesIO(file.read()))

    # 이미지를 static 디렉토리에 고정된 이름으로 저장 (덮어쓰기 방식)
    filename = 'uploaded_image.jpg'
    file_path = os.path.join('static', filename)
    img.save(file_path)

    # YOLO 모델로 예측 수행
    results = model.predict(img)

    # YOLO 예측 결과에서 클래스 이름과 id를 가져옴
    predictions = []
    class_ids = []  # class_ids 배열 생성
    for result in results:
        for box in result.boxes:
            class_id = int(box.cls)  # 예측된 클래스 ID
            class_name = model.names[class_id]  # 예측된 클래스 이름
            corrected_class_name = remap_class_name(class_name)  # 클래스 이름 재매핑
            bbox = box.xyxy.tolist()[0]
            
            # 바운딩 박스 좌표와 클래스 이름을 터미널에 출력
            print(f"예측된 클래스 ID: {class_id}, 클래스 이름: {class_name}, 바운딩 박스: {bbox}")

            predictions.append({
                'bbox': bbox,  # 바운딩 박스 좌표
                'class_id': class_id,  # 클래스 ID
                'class_name': corrected_class_name  # 클래스 이름
            })
            class_ids.append(class_id)  # class_id를 추가

    if len(predictions) == 0:
        print("예측 결과가 없습니다.")
        return jsonify({'error': 'No predictions found'}), 400

    # 모든 예측된 클래스 이름을 리스트로 추출
    class_names = [prediction['class_name'] for prediction in predictions]

    # 실제 JSON 데이터를 출력해 확인
    json_data = {
        'status': 'success',
        'predictions': predictions,  # 모든 예측 결과 (바운딩 박스 포함)
        'class_ids': class_ids,  # class_ids를 추가하여 반환
        'class_names': class_names,  # 모든 클래스 이름을 리스트로 반환
        'image_path': filename  # 고정된 이미지 경로 반환
    }
    print(f"JSON 데이터: {json_data}")

    # 예측 결과를 JSON으로 반환
    return jsonify(json_data)

# 예측 결과 화면
@app.route('/result')
def result():
    class_names = request.args.get('class_names')
    predictions = request.args.get('predictions')
    image_path = request.args.get('image_path')
    class_ids = request.args.get('class_ids')  # class_ids를 URL 파라미터로 추가

    return render_template('result.html', 
                           class_names=class_names,
                           predictions=predictions,
                           class_ids=class_ids,  # class_ids를 템플릿에 전달
                           image_path=image_path)

# 레시피 페이지 (food_name 기반으로 레시피를 가져옴)
@app.route('/recipe')
def recipe_page():
    food_name = request.args.get('food_name')  # food_name 파라미터 받기
    if not food_name:
        return "Error: No 'food_name' parameter provided", 400

    # 카테고리 찾기
    food_category = None
    for category, foods in category_dict.items():
        if food_name in foods:
            food_category = category
            break
    print(food_category)
    if not food_category:
        return "Error: Category not found for this food", 404

    # 레시피 데이터를 엑셀 파일에서 불러오기
    recipe_df = pd.read_excel('recipe.xlsx')
    english_df = pd.read_excel('recipe_english.xlsx')

    # 'food name'이 존재하는지 확인하고 해당 레시피 가져오기
    if 'food name' in recipe_df.columns:
        recipe_row = recipe_df[recipe_df['food name'] == food_name]
    else:
        return "Error: 'food name' column not found", 500

    if recipe_row.empty:
        return "Error: Recipe not found", 404

    # 해당 food_name과 대응하는 영문 음식명을 찾기 위해 id를 사용
    dish_id = recipe_row.iloc[0]['id']  # 한국어 레시피의 id

    # 영어 레시피에서 동일한 id를 찾아 영문 음식명 가져오기
    english_recipe_row = english_df[english_df['id'] == dish_id]
    if english_recipe_row.empty:
        return "Error: English name not found", 404
    
    food_name_english = english_recipe_row.iloc[0]['food name']  # 영어 음식명 가져오기
    english_ingredients = english_recipe_row.iloc[0]['ingredients']
    english_recipe = english_recipe_row.iloc[0]['recipe']

    # 레시피 내용을 번호로 나눠서 줄바꿈 처리 (1. 2. 3. 등 번호 패턴 찾기)
    recipe_text = recipe_row.iloc[0]['recipe']
    formatted_recipe = re.sub(r'(\d+\.)', r'<br>\1', recipe_text)  # 1., 2. 등 번호 앞에 <br> 태그 추가
    formatted_recipe_english = re.sub(r'(\d+\.)', r'<br>\1', english_recipe)

    # 해당 food_name과 카테고리 정보를 레시피 페이지로 전달
    return render_template('recipe.html', 
                           food_name=food_name, 
                           food_name_english=food_name_english,
                           food_category=food_category, 
                           recipe=recipe_row.to_dict(orient='records')[0], 
                           english_ingredients=english_ingredients,
                           formatted_recipe=formatted_recipe,
                           formatted_recipe_english=formatted_recipe_english)

# 레시피 데이터를 JSON으로 반환하는 엔드포인트
@app.route('/get_recipe', methods=['GET'])
def get_recipe():
    dish_id = request.args.get('id')
    if not dish_id:
        return jsonify({'status': 'error', 'message': 'No id provided'}), 400

    # 레시피 데이터를 엑셀 파일에서 불러오기
    recipe_df = pd.read_excel('recipe.xlsx')
    english_recipe_df = pd.read_excel('recipe_english.xlsx')

    # dish_id에 해당하는 한국어 레시피 찾기
    recipe_row = recipe_df[recipe_df['id'] == int(dish_id)]
    if recipe_row.empty:
        return jsonify({'status': 'error', 'message': 'Recipe not found'}), 404

    # dish_id에 해당하는 영어 레시피 찾기
    english_recipe_row = english_recipe_df[english_recipe_df['id'] == int(dish_id)]
    if english_recipe_row.empty:
        return jsonify({'status': 'error', 'message': 'English recipe not found'}), 404

    # 한국어와 영어 레시피 정보를 각각 JSON으로 반환
    recipe_data = {
        'korean': {
            'name': recipe_row.iloc[0]['name'],
            'description': recipe_row.iloc[0]['description'],
            'ingredients': recipe_row.iloc[0]['ingredients'],
            'recipe': recipe_row.iloc[0]['recipe'],
            'image': recipe_row.iloc[0]['image']  # 이미지 경로도 함께 반환
        },
        'english': {
            'ingredients': english_recipe_row.iloc[0]['ingredients'],
            'recipe': english_recipe_row.iloc[0]['recipe']
        }
    }

    return jsonify({'status': 'success', 'dish': recipe_data})
  
if __name__ == '__main__':
    app.run(debug=True)
    #app.run(host='0.0.0.0', port=5000, debug=True) #다른 사용자가 서버 이용할때