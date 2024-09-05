document.addEventListener('DOMContentLoaded', function() {
    var menuToggle = document.getElementById('menu-toggle');
    var sidebar = document.getElementById('sidebar');
    var mainContent = document.getElementById('main-content');

    if (menuToggle) {
        menuToggle.addEventListener('click', function() {
            if (sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                mainContent.classList.remove('shift');
            } else {
                sidebar.classList.add('open');
                mainContent.classList.add('shift');
            }
        });
    }

    var shiftDiv = document.getElementById('menu-toggle');

    if (shiftDiv) {
        shiftDiv.addEventListener('click', function() {
            var viewportWidth = window.innerWidth;

            if (viewportWidth < 1000) {
                this.classList.toggle('shifted');
            }
        });
    }
});