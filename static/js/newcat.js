document.getElementById('refresh-cat').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/cat/');
        const html = await response.text();
        const contentBlock = document.querySelector('.cat-container > :first-child');
        const newContent = new DOMParser()
            .parseFromString(html, 'text/html')
            .querySelector('.alert, .cat-image, .error-message');

        if (contentBlock && newContent) {
            contentBlock.replaceWith(newContent);
        }

        const button = document.getElementById('refresh-cat');
        button.disabled = html.includes('disabled');
    } catch (error) {
        console.log('Ошибка при загрузке котика:', error);
    }
});

