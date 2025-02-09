document.addEventListener('DOMContentLoaded', function() {
    function addPaginationEventListeners() {
        const paginationLinks = document.querySelectorAll('#blog-pagination-links div');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();

                const pageNumber = this.getAttribute('data-page');
                fetch('/blog/ajax/?' + new URLSearchParams({
                    page: pageNumber
                }))
                .then(response => response.json())
                .then(data => {
                    document.getElementById('post-container').innerHTML = data.html;
                    document.getElementById('blog-pagination-links').innerHTML = data.paginator;
                    addPaginationEventListeners();
                })
                .catch(error => console.error('Ошибка:', error));
            });
        });
    }

    document.body.addEventListener('click', function(event) {
        const target = event.target.closest('.blog-pag');

        if (target) {
            addPaginationEventListeners();
        }
    });

    addPaginationEventListeners();
});