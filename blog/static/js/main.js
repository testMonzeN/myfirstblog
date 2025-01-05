function loadPage(page) {
    fetch('blog/?page=' + page)
        .then(response => {
            if (!response.ok) {
                throw new Error('Ошибка загрузки страницы');
            }
            return response.text();
        })
        .then(html => {
            try {
                const paginationLinks = document.getElementById('pagination-links');
                if (paginationLinks) {
                    paginationLinks.innerHTML = html;
                } else {
                    console.error('нету элемента с id "pagination-links"');
                }
            } catch (err) {
                console.log('error - ', err);
            }
        })
        .catch(error => {
            console.error(error);
        });
}

document.addEventListener('DOMContentLoaded', function() {
    console.log('start')
    loadPage(1);
});