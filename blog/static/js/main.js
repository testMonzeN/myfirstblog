
document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('click', function(event) {
        const target = event.target.closest('.pag');
        if (target) {
            const paginationLinks = document.querySelectorAll('#pagination-links div');

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
                            document.getElementById('pagination-links').innerHTML = data.paginator;
                        })
                        })
                        .catch(error => console.error('Ошибка:', error))

                    })}})})
