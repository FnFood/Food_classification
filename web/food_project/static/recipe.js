document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    const dishId = urlParams.get('id');

    if (!dishId) {
        alert('Error: No id parameter provided');
        return;
    }

    // 레시피 데이터를 서버에서 가져오기
    fetch(`/get_recipe?id=${dishId}`)
        .then(response => response.json())
        .then(data => {
            // 데이터를 받아서 레시피 페이지에 표시
            if (data.status === 'success') {
                document.getElementById('dishName').textContent = data.dish.name;
                document.getElementById('dishDescription').textContent = data.dish.description;
                document.getElementById('ingredients').textContent = data.dish.ingredients;
                document.getElementById('recipeSteps').textContent = data.dish.recipe;
                document.getElementById('dishImage').src = `/static/images/${data.dish.image}`;
            } else {
                alert('레시피를 불러오는 데 실패했습니다.');
            }
        })
        .catch(error => {
            console.error('Error fetching recipe:', error);
            alert('레시피를 불러오는 도중 문제가 발생했습니다.');
        });
});
