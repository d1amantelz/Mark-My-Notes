document.addEventListener('DOMContentLoaded', function () {
    var saveIcon = document.querySelector(".note-panel img[src$='save.svg']");
    saveIcon.addEventListener('click', function (e) {
        e.preventDefault();
        var submitButton = document.querySelector("button[type='submit']");
        submitButton.click();
    });
});