document.addEventListener('DOMContentLoaded', function() {
    const today = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };

    const currentDayElement = document.getElementById('day-0');
    if (currentDayElement) {
        currentDayElement.textContent = today.toLocaleDateString('en-US', options);
    }

    for (let i = 1; i <= 6; i++) {
        const nextDay = new Date(today);
        nextDay.setDate(today.getDate() + i);
        const dayElement = document.getElementById(`day-${i}`);
        if (dayElement) {
            dayElement.textContent = nextDay.toLocaleDateString('en-US', options);
        }
    }
});