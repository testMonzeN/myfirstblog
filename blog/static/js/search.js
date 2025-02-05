document.addEventListener('DOMContentLoaded', function() {
    console.log('search');
    document.body.addEventListener('click', function(event) {
        const target = event.target.closest('.pag-button');
        if (target) {
            event.preventDefault();
            const page = target.getAttribute('data-search');
            const query = document.getElementById('search_text_id').value;
            fetch('/search/ajax/?' + new URLSearchParams({
                q: query,
                page: page
            }))
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка сети');
                }
                return response.json();
            })
            .then(data => {
                document.getElementById('search-container').innerHTML = data.html;
                document.getElementById('search-pag-links').innerHTML = data.paginator;
            })
            .catch(error => {
                console.error('Ошибка:', error);
            });
        }
    });
    const searchForm = document.querySelector('form[action="{% url \'global_search\' %}"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            const query = document.getElementById('search_text_id').value;
            if (!query.trim()) {
                event.preventDefault();
                alert('Введите поисковый запрос');
                return;
            }
            window.location.href = `/search/?q=${encodeURIComponent(query)}`;
        });
    }
});