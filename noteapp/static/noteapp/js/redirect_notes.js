document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll(".note-row");

    rows.forEach((row) => {
        const url = row.dataset.url;
        if (url) {
            row.addEventListener("click", function () {
                window.location = url;
            });
        }
    });
});
