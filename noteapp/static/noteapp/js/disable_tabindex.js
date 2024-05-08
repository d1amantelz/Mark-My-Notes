window.addEventListener('keydown', function (e) {
    if (e.keyIdentifier == 'U+0009' || e.key == 'Tab') {
        e.preventDefault();
    }
}, true);