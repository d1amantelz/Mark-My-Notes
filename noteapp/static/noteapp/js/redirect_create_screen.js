document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll(".create-block");

    rows.forEach((row) => {
        const link = row.querySelector("a");
        if (link) {
            row.addEventListener("click", function () {
                window.location = link.href;
            });
        }
    });
});