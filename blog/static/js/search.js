document.addEventListener('DOMContentLoaded', function() {
    console.log('search');
    document.body.addEventListener('click', function(event) {
        const target = event.target.closest('.pag-button');
        if (target) {
            event.preventDefault();
            const page = target.getAttribute('data-search');
            fetch('/search/ajax/?' + new URLSearchParams({
                page: page
            }))
            .then(response => response.json())
            .then(data => {
                document.getElementById('search-container').innerHTML = data.html;
                document.getElementById('search-pag-links').innerHTML = data.paginator;
            })
            .catch(error => console.error('Ошибка:', error));
        }
    });
});