document.addEventListener('keydown', function (event) {
    if (event.ctrlKey && event.key === 's') {
        event.preventDefault();
        let submitButton = document.querySelector("button[type='submit']");
        if (submitButton) {
            submitButton.click();
        }
    }
});
