const imageUpload = document.getElementById('imageUpload');
const imagePreviewContainer = document.getElementById('imagePreviewContainer');
const imagePreview = document.getElementById('imagePreview');
const searchIcon = document.getElementById('searchIcon');

// 이미지 미리보기
imageUpload.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreviewContainer.style.display = 'block';  // 미리보기 표시
        };
        reader.readAsDataURL(file);
    }
});

// 이미지 삭제
function removeImage() {
    imagePreview.src = '';
    imagePreviewContainer.style.display = 'none';
    imageUpload.value = '';  // 파일 입력 초기화
}

// 서버로 이미지 전송
searchIcon.addEventListener('click', function() {
    const file = imageUpload.files[0];
    if (!file) {
        alert('이미지를 선택해 주세요.');
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    // 서버로 이미지를 전송하고 JSON 응답을 받아옴
    fetch('/predict', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // 예측된 class_names와 바운딩 박스들을 JSON 문자열로 변환하여 URL에 추가
            const classNames = JSON.stringify(data.class_names);
            const predictions = JSON.stringify(data.predictions);

            // result 페이지로 이동하면서 예측된 데이터와 이미지 경로를 URL 파라미터로 전달
            window.location.href = `/result?class_names=${encodeURIComponent(classNames)}&predictions=${encodeURIComponent(predictions)}&image_path=${data.image_path}`;
        } else {
            alert('예측에 실패했습니다.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('예측에 실패했습니다.');
    });
});
