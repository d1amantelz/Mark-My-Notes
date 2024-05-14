window.addEventListener('load', (event) => {
    document.querySelectorAll('pre code').forEach((block) => {
        // Создаем div-обертку
        const wrapper = document.createElement('div');
        wrapper.style.maxWidth = '800px';
        wrapper.style.position = 'relative';
        wrapper.style.zIndex = '10';

        // Создаем div для кнопки копирования
        const div = document.createElement('div');
        div.className = 'copy-container';
        div.style.position = 'absolute';
        div.style.right = '0';
        div.style.zIndex = '9';
        div.style.top = '0';

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

        // Добавляем div в обертку
        wrapper.appendChild(div);

        // Заменяем блок кода на обертку
        block.parentNode.replaceChild(wrapper, block);

        // Добавляем блок кода в обертку
        wrapper.appendChild(block);

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
