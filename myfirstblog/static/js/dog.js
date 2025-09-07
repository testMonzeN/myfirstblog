document.addEventListener('DOMContentLoaded', function() {
    function setupDogPagination() {
        const paginationLinks = document.querySelectorAll('.dog-pag-button');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                const pageNumber = this.getAttribute('data-page');
                loadDogPage(pageNumber);
            });
        });
    }

    async function loadDogPage(page) {
        try {
            const response = await fetch(`/animals/dog_hist/ajax/?page=${page}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) throw new Error(`Error: ${response.status}`);

            const data = await response.json();

            if (data.html) {
                document.getElementById('dog-images').innerHTML = data.html;
            }
            if (data.paginator) {
                document.getElementById('dog-pagination').innerHTML = data.paginator;
            }

            setupDogPagination();

        } catch (error) {
            console.error('Dog error:', error);
            alert('Failed to load dogs. Please try again.');
        }
    }

    document.body.addEventListener('click', function(event) {
        if (event.target.closest('.dog-pag')) {
            setupDogPagination();
        }
    });

    setupDogPagination();
});