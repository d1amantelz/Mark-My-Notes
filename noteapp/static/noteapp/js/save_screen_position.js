function resize(textarea) {
    var scrollLeft = window.pageXOffset ||
        (document.documentElement || document.body.parentNode || document.body).scrollTop;

    var scrollTop = window.pageYOffset ||
        (document.documentElement || document.body.parentNode || document.body).scrollTop;

    textarea.style.height = "auto";
    textarea.style.height = textarea.scrollHeight + 'px';

    window.scrollTo(scrollLeft, scrollTop);
}

var textarea = document.querySelector(".note-text");

// Обновление высоты при вводе
textarea.addEventListener("input", function () {
    resize(this);
});

// Отключение плавной прокрутки при фокусе
textarea.addEventListener("focus", function () {
    document.documentElement.style.scrollBehavior = 'auto';
});

// Включение плавной прокрутки при потере фокуса
textarea.addEventListener("blur", function () {
    document.documentElement.style.scrollBehavior = 'smooth';
});

// Инициализация высоты при загрузке страницы
window.addEventListener("DOMContentLoaded", function () {
    resize(textarea);
});
