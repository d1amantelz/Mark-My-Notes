window.onload = function () {
    // Вычисление ширины note-panel
    var notePanel = document.querySelector('.note-panel');
    var icons = notePanel.querySelectorAll('a');
    var iconWidth = 44;
    var totalWidth = icons.length * iconWidth;
    notePanel.style.width = totalWidth + 'px';

    // Плавное появление note-panel через 1 секунду
    setTimeout(function () {
        notePanel.style.visibility = 'visible';
        notePanel.style.opacity = '1';
    }, 600);
};
