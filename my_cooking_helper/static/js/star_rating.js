document.addEventListener('DOMContentLoaded', () => {
    const stars = document.querySelectorAll('.star-rating span');
    const ratingInput = document.getElementById('rating-score');
    const form = document.querySelector('form');

    stars.forEach(star => {
        star.addEventListener('click', () => {
            const rating = parseInt(star.getAttribute('data-value'));
            ratingInput.value = rating;

            stars.forEach((s, index) => {
                if (index < rating) {
                    s.classList.remove('fa-regular');
                    s.classList.add('fa', 'fa-star', 'checked');
                } else {
                    s.classList.remove('fa', 'fa-star', 'checked');
                    s.classList.add('fa-regular', 'fa-star');
                }
            });

            form.submit();
        });
    });
});