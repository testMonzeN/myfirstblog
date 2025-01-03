    function loadPage(page) {
        fetch('blog/?page=${page}')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Ошибка загрузки страницы');
                }
                return response.text();
            })
            .then(html => {
            try {
                document.getElementById('pagination-links').innerHTML = html;
            } catch (err) {
                console.log('error - ', err);
            }})
            .catch(error => {
                console.error(error);
            });
    }

loadPage(1);
