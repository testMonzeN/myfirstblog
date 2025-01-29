document.addEventListener('DOMContentLoaded', function() {
    console.log('search');
    document.body.addEventListener('click', function(event) {
        const target = event.target.closest('.search_btn');
        if (target) {
            event.preventDefault();
            const text = document.getElementById("search_text_id").value;
            fetch('/search/ajax/?' + new URLSearchParams({
                 q: text
                    }))
                   .then(response => response.json())
                        .then(data => {
                            document.getElementById('search_text_id').value = '';
                            document.getElementById('post-container').innerHTML = data.html;
                            document.getElementById('pagination-links').innerHTML = data.paginator;
                        })
                        .catch(error => console.error('Ошибка:', error))




                    }}
    )}
)