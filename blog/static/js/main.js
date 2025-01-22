document.addEventListener('DOMContentLoaded', function() {
    const paginationLinks = document.querySelectorAll('#pagination-links div');
    console.log('start');

    paginationLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();

            const pageNumber = this.getAttribute('data-page');
            fetch('/blog/ajax_page/?' + new URLSearchParams({
                page: pageNumber
            }))
            .then(response => response.json())
            .then(data => {
                document.getElementById('post-container').innerHTML = data.html;
                console.log(data.pagination.page_next)
            })
            .catch(error => console.error('Ошибка:', error));
        });
    });
});
