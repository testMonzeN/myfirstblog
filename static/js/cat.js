document.addEventListener('DOMContentLoaded', function() {
    function setupCatPagination() {
        const paginationLinks = document.querySelectorAll('.cat-pag-button');
        paginationLinks.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                const pageNumber = this.getAttribute('data-page');
                loadCatPage(pageNumber);
            });
        });
    }

    async function loadCatPage(page) {
        try {
            const response = await fetch(`/api/cat_hist/ajax/?page=${page}`, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) throw new Error(`Error: ${response.status}`);

            const data = await response.json();

            if (data.html) {
                document.getElementById('cat-images').innerHTML = data.html;
            }
            if (data.paginator) {
                document.getElementById('cat-pagination').innerHTML = data.paginator;
            }

            setupCatPagination();

        } catch (error) {
            console.error('Cat error:', error);
            alert('Failed to load cats. Please try again.');
        }
    }

    document.body.addEventListener('click', function(event) {
        if (event.target.closest('.cat-pag')) {
            setupCatPagination();
        }
    });

    setupCatPagination();
});