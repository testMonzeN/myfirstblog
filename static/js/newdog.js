document.getElementById('refresh-dog').addEventListener('click', async () => {
    try {
        const response = await fetch('/api/dog/');
        const html = await response.text();
        const contentBlock = document.querySelector('.dog-container > :first-child');
        const newContent = new DOMParser()
            .parseFromString(html, 'text/html')
            .querySelector('.alert, .dog-image, .error-message');

        if (contentBlock && newContent) {
            contentBlock.replaceWith(newContent);
        }

        const button = document.getElementById('refresh-dog');
        button.disabled = html.includes('disabled');
    } catch (error) {
        console.log('Ошибка при загрузке песика:', error);
    }
});