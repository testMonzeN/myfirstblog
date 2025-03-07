document.getElementById('refresh-cat').addEventListener('click', function() {
    fetch('/api/cat/')
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');
            const newImg = doc.querySelector('img').outerHTML;
            document.querySelector('img').outerHTML = newImg;
        });
});