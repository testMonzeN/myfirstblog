document.addEventListener('DOMContentLoaded', function() {
    function addPaginationEventListeners() {
        const paginationLinks = document.querySelectorAll('#stepik-pagination-links-js div');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();

                const pageNumber = this.getAttribute('data-stepik-js');
                fetch('/stepik/js/ajax/?' + new URLSearchParams({
                    page: pageNumber
                }))
                .then(response => response.json())
                .then(data => {
                    document.getElementById('js-stepik-post-container').innerHTML = data.html;
                    document.getElementById('stepik-pagination-links-js').innerHTML = data.paginator;
                    addPaginationEventListeners();
                })
                .catch(error => console.error('Ошибка:', error));
            });
        });
    }

    document.body.addEventListener('click', function(event) {
        const target = event.target.closest('.stepik-pag-js');

        if (target) {
            addPaginationEventListeners();
        }
    });

    addPaginationEventListeners();
});