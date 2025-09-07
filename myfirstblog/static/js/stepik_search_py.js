document.addEventListener('DOMContentLoaded', function() {
    function addPaginationEventListeners() {
        const paginationLinks = document.querySelectorAll('#stepik-pagination-links-py div');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();

                const pageNumber = this.getAttribute('data-stepik');
                fetch('/stepik/python/ajax/?' + new URLSearchParams({
                    page: pageNumber
                }))
                .then(response => response.json())
                .then(data => {
                    document.getElementById('stepik-post-container').innerHTML = data.html;
                    document.getElementById('stepik-pagination-links-py').innerHTML = data.paginator;
                    addPaginationEventListeners();
                })
                .catch(error => console.error('Ошибка:', error));
            });
        });
    }

    document.body.addEventListener('click', function(event) {
        const target = event.target.closest('.pagg');

        if (target) {
            addPaginationEventListeners();
        }
    });

    addPaginationEventListeners();
});