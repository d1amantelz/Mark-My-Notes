// Ваш JavaScript-файл
window.addEventListener('load', (event) => {
    document.querySelectorAll('pre code').forEach((block) => {
        // Создаем div
        const div = document.createElement('div');
        div.className = 'copy-container';

        // Создаем кнопку копирования
        const button = document.createElement('button');
        button.className = 'copy-button';

        // Создаем изображение для кнопки
        const img = document.createElement('img');
        img.src = window.copyIconPath; // Используйте глобальную переменную
        img.alt = 'Копировать';

        // Добавляем изображение в кнопку
        button.appendChild(img);

        // Добавляем кнопку в div
        div.appendChild(button);

        // Добавляем div в code
        block.appendChild(div);

        // Добавляем функциональность копирования
        button.addEventListener('click', () => {
            const code = block.textContent;
            navigator.clipboard.writeText(code);
            img.src = window.saveIconPath; // Используйте глобальную переменную
            img.alt = 'Скопировано!';
            setTimeout(() => {
                img.src = window.copyIconPath; // Возвращаем иконку copy.svg
                img.alt = 'Копировать';
            }, 4000);
        });
    });
});
