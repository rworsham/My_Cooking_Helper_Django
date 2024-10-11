document.addEventListener('DOMContentLoaded', () => {
    const favoriteIcon = document.querySelector('.favorite span');
    const favoriteInput = document.getElementById('favorite');
    const form = document.getElementById('favoriteForm');

    favoriteIcon.addEventListener('click', () => {
        if (favoriteInput.value === 'favorite') {
            favoriteInput.value = 'un_favorite';
            favoriteIcon.classList.remove('bi-heart-fill');
            favoriteIcon.classList.add('bi-heart');
        } else {
            favoriteInput.value = 'favorite';
            favoriteIcon.classList.remove('bi-heart');
            favoriteIcon.classList.add('bi-heart-fill');
        }

        favoriteForm.submit();
    });
});