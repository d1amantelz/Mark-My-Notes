document.addEventListener('DOMContentLoaded', function () {
    var saveLink = document.querySelector(".note-panel .save-link");
    saveLink.addEventListener('click', function (e) {
        e.preventDefault();
        var submitButton = document.querySelector("button[type='submit']");
        submitButton.click();
    });
});