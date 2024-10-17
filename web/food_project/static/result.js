document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    
    // URL에서 전달된 예측 결과 가져오기
    const classNames = JSON.parse(decodeURIComponent(urlParams.get('class_names')));  // class_names로 가져오기
    const predictions = JSON.parse(decodeURIComponent(urlParams.get('predictions')));
    const imagePath = urlParams.get('image_path');
    
    const canvas = document.getElementById('predictionCanvas');
    const ctx = canvas.getContext('2d');
    const img = new Image();

    // 바운딩 박스 색상을 다르게 설정할 수 있는 색상 배열
    const colors = ['#FF5100', '#005AEB', '#1FA51F', '#FFD000', '#FF5A89', '#9747FF'];
    img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);

        // 예측된 바운딩 박스 그리기 (각각 다른 색상 적용)
        predictions.forEach((pred, index) => {
            const color = colors[index % colors.length];  // 색상 배열에서 순차적으로 선택
            ctx.strokeStyle = color;
            ctx.lineWidth = 2;
            ctx.strokeRect(
                pred.bbox[0], 
                pred.bbox[1], 
                pred.bbox[2] - pred.bbox[0], 
                pred.bbox[3] - pred.bbox[1]
            );

            // 바운딩 박스 위에 예측된 음식 이름 표시
            ctx.fillStyle = color;  // 텍스트 색상도 동일하게
            ctx.font = "bold 20px Arial";
            ctx.fillText(
                classNames[index],  // 예측된 음식 이름
                pred.bbox[0],  // 바운딩 박스의 왼쪽 위에 텍스트 표시
                pred.bbox[1] - 10  // 바운딩 박스 위에 여백을 주고 텍스트 표시
            );

            // 예상된 이름 및 버튼 박스 생성
            createRecipeButton(classNames[index], color);
        });
    };

    // 이미지 경로 설정
    img.src = `/static/${imagePath}`;
});

function createRecipeButton(className, color) {
    const buttonContainer = document.getElementById('buttonContainer');

    // 버튼 생성
    const recipeButton = document.createElement('button');
    recipeButton.textContent = `${className}의 레시피 보기`;
    recipeButton.style.backgroundColor = color;
    recipeButton.style.color = 'white';
    recipeButton.style.border = 'none';
    recipeButton.style.padding = '10px';
    recipeButton.style.cursor = 'pointer';
    recipeButton.style.borderRadius = '30px';  // 둥근 모서리
    recipeButton.style.marginBottom = '10px';

    // 버튼 클릭 이벤트 (레시피 페이지로 이동 - 실제 레시피로 연결)
    recipeButton.addEventListener('click', function() {
        window.location.href = `/recipe?food_name=${className}`;  // className을 food_name 파라미터로 넘김
    });

    // 전체 컨테이너에 추가
    buttonContainer.appendChild(recipeButton);
}