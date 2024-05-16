// document.addEventListener('DOMContentLoaded', (event) => {
//     // Получаем элементы
//     let modal = document.getElementById("deleteModal");
//     let btn = document.getElementById("deleteNoteButton"); // Кнопка, которая открывает модальное окно
//     let confirmDelete = document.getElementById("confirmDelete"); // Кнопка подтверждения удаления
//     let cancelDelete = document.getElementById("cancelDelete"); // Кнопка отмены удаления
//
//     // Когда пользователь нажимает на кнопку удаления, открываем модальное окно
//     btn.onclick = function () {
//         modal.style.display = "block";
//         modal.setAttribute('data-note-id', this.getAttribute('data-note-id'));
//     }
//
//
//
//     // Когда пользователь нажимает на кнопку "Да", выполняем удаление
//     confirmDelete.onclick = function () {
//         let noteId = modal.getAttribute('data-note-id');
//         if (noteId) {
//             window.location.href = '/notes/' + noteId + '/delete/'; // Измените URL на ваш путь удаления
//         }
//     }
//
//     // Когда пользователь нажимает на кнопку "Нет", закрываем модальное окно
//     cancelDelete.onclick = function () {
//         modal.style.display = "none";
//     }
//
//     // Когда пользователь нажимает в любом месте за пределами модального окна, закрываем его
//     window.onclick = function (event) {
//         if (event.target === modal) {
//             modal.style.display = "none";
//         }
//     }
// });

document.addEventListener('DOMContentLoaded', (event) => {
    // Получаем модальное окно и кнопки подтверждения/отмены
    let modal = document.getElementById("deleteModal");
    let confirmDelete = document.getElementById("confirmDelete");
    let cancelDelete = document.getElementById("cancelDelete");

    // Находим все кнопки удаления по классу и добавляем обработчики событий
    document.querySelectorAll(".deleteButton").forEach(btn => {
        btn.onclick = function () {
            modal.style.display = "block";
            // Установка атрибута data-id для модального окна
            modal.setAttribute('data-id', this.getAttribute('data-id'));
            modal.setAttribute('data-type', this.getAttribute('data-type'));
        }
    });

    // Обработчик события для кнопки "Да"
    confirmDelete.onclick = function () {
        let id = modal.getAttribute('data-id');
        let type = modal.getAttribute('data-type');
        if (id && id !== 'null') {
            let path = type === 'note' ? '/notes/' : '/categories/';
            window.location.href = path + id + '/delete/';
        }
    };

    // Обработчик события для кнопки "Нет"
    cancelDelete.onclick = function () {
        modal.style.display = "none";
    };

    // Закрытие модального окна при клике вне его области
    window.onclick = function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});

