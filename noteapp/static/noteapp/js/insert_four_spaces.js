document.querySelector('textarea').addEventListener('keydown', function (e) {
    if (e.key == 'Tab') {
        e.preventDefault();
        var start = this.selectionStart;
        var end = this.selectionEnd;

        // вставляем 4 пробела
        this.value = this.value.substring(0, start) +
            "    " + this.value.substring(end);

        // перемещаем курсор
        this.selectionStart =
            this.selectionEnd = start + 4;
    }
});