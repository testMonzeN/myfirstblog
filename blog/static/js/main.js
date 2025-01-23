document.addEventListener('DOMContentLoaded', function() {
    console.log('start');
    const paginationLinks = document.querySelectorAll('#pagination-links div');
    console.log('connect with paginationLinks');

    paginationLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            console.log('click');
            event.preventDefault();

            const pageNumber = this.getAttribute('data-page');
            fetch('/blog/ajax_page/?' + new URLSearchParams({
                page: pageNumber
            }))

            .then(response => response.json())
                .then(data => {
                    document.getElementById('post-container').innerHTML = data.html;
                    document.getElementById('pagination-links').innerHTML = data.paginator;
                    console.log('data update!');
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });
});