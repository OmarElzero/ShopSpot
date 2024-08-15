window.onload = function () {
    document.getElementById('preloader').style.display = 'none';
};

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.main-menu li').forEach(function(el) {
        el.addEventListener('mouseenter', function() {
            this.querySelector('.sub-menu').style.display = 'block';
        });
        el.addEventListener('mouseleave', function() {
            this.querySelector('.sub-menu').style.display = 'none';
        });
    });
});

