document.addEventListener("DOMContentLoaded", function () {
    const admonitions = document.querySelectorAll(".admonition");

    admonitions.forEach(admonition => {
        const secondClass = Array.from(admonition.classList).find(cls => cls !== "admonition");
        const icon = getIconForClass(secondClass);
        const text = getTextForClass(secondClass);

        if (icon && text) {
            const iconElement = document.createElement("i");
            iconElement.classList.add("material-icons");
            iconElement.textContent = icon;

            const textNode = document.createTextNode(`${text}`);

            const wrapper = document.createElement("span");
            wrapper.appendChild(iconElement);
            wrapper.appendChild(textNode);

            admonition.insertBefore(wrapper, admonition.firstChild);
        }
    });

    function getIconForClass(className) {
        switch (className) {
            case "note":
                return "info";
            case "attention":
                return "warning";
            case "danger":
                return "error";
            case "important":
                return "priority_high";
            case "tip":
                return "lightbulb";
            default:
                return null;
        }
    }

    function getTextForClass(className) {
        switch (className) {
            case "note":
                return "Примечание";
            case "attention":
                return "Внимание";
            case "danger":
                return "Опасно";
            case "important":
                return "Важно";
            case "tip":
                return "Совет";
            default:
                return null;
        }
    }
});