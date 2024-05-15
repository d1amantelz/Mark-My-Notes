document.addEventListener('DOMContentLoaded', function () {
    let saveLink = document.querySelector(".note-panel .save-link");
    if (saveLink) {
        saveLink.addEventListener('click', function (e) {
            e.preventDefault();
            let submitButton = document.querySelector("button[type='submit']");
            if (submitButton) {
                submitButton.click();
            }
        });
    }
});