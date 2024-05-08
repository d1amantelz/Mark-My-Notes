function popNotification() {
    var message = document.createElement('div');
    message.innerText = 'Текст скопирован';
    message.style.position = 'fixed';
    message.style.top = '30px';
    message.style.left = '50%';
    message.style.fontWeight = "bold";
    message.style.transform = 'translateX(-50%)';
    message.style.padding = '15px';
    message.style.backgroundColor = '#3a3a3a';
    message.style.color = '#d7d7d7';
    message.style.border = '1px solid #fdbf2d'
    message.style.borderRadius = '15px';
    message.style.transition = 'opacity 0.5s';
    message.style.opacity = '1';
    message.style.zIndex = '10';

    // Добавление сообщения на страницу
    document.body.appendChild(message);

    // Удаление сообщения через 2 секунды с анимацией
    setTimeout(function () {
        message.style.opacity = '0';
        setTimeout(function () {
            document.body.removeChild(message);
        }, 500);
    }, 1000);
}

function copy_to_clipboard() {
    // Копирование текста
    document.querySelector("textarea").select();
    document.execCommand('copy');
    window.getSelection().removeAllRanges();
    popNotification();
}