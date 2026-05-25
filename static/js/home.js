document.addEventListener('DOMContentLoaded', function () {
    const vehiclesContainer = document.getElementById('vehiclesContainer');
    const searchInput = document.getElementById('searchInput');
    const brandFilter = document.getElementById('brandFilter');
    const descFilter = document.getElementById('descFilter');
    const sortSelect = document.getElementById('sortSelect');
    const toggleViewBtn = document.getElementById('toggleViewBtn');
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');

    sortSelect.value = 'alphabetical';
    filterAndSortVehicles();

    function filterAndSortVehicles() {
        const searchTerm = searchInput.value.toLowerCase();
        const brandTerm = brandFilter.value.toLowerCase();
        const descTerm = descFilter.value.toLowerCase();
        const sortValue = sortSelect.value;

        let vehicles = Array.from(vehiclesContainer.getElementsByClassName('vehicle-card'));

        // Filter vehicles
        vehicles.forEach(vehicle => {
            const brand = vehicle.getAttribute('data-brand').toLowerCase();
            const description = vehicle.getAttribute('data-description').toLowerCase();
            const model = vehicle.getAttribute('data-model').toLowerCase();

            const matchesSearch = model.includes(searchTerm) || description.includes(searchTerm);
            const matchesBrand = (brandTerm === 'all' || brand === brandTerm);
            const matchesDesc = (descTerm === 'all' || description === descTerm);

            if (matchesSearch && matchesBrand && matchesDesc) {
                vehicle.style.display = '';
                // Reset fade-in class for re-animation
                vehicle.classList.remove('fade-in');
                // Trigger reflow
                void vehicle.offsetWidth;
                // Re-add fade-in class
                requestAnimationFrame(() => {
                    vehicle.classList.add('fade-in');
                });
            } else {
                vehicle.style.display = 'none';
            }
        });

        // Sort vehicles
        vehicles = vehicles.filter(v => v.style.display !== 'none');

        vehicles.sort((a, b) => {
            if (sortValue === 'alphabetical') {
                const brandComparison = a.getAttribute('data-brand').localeCompare(b.getAttribute('data-brand'));
                if (brandComparison === 0) {
                    return a.getAttribute('data-model').localeCompare(b.getAttribute('data-model'));
                }
                return brandComparison;
            } else if (sortValue === 'price_asc') {
                return parseFloat(a.getAttribute('data-price')) - parseFloat(b.getAttribute('data-price'));
            } else if (sortValue === 'price_desc') {
                return parseFloat(b.getAttribute('data-price')) - parseFloat(a.getAttribute('data-price'));
            }
        });

        // Append sorted vehicles back to container
        vehicles.forEach(vehicle => vehiclesContainer.appendChild(vehicle));
    }

    // Event listeners for filters and sorting
    searchInput.addEventListener('input', filterAndSortVehicles);
    brandFilter.addEventListener('change', filterAndSortVehicles);
    descFilter.addEventListener('change', filterAndSortVehicles);
    sortSelect.addEventListener('change', filterAndSortVehicles);

    // Toggle grid/list view
    toggleViewBtn.addEventListener('click', function () {
        if (vehiclesContainer.classList.contains('grid-view')) {
            vehiclesContainer.classList.remove('grid-view');
            vehiclesContainer.classList.add('list-view');
            toggleViewBtn.textContent = 'Switch to Grid View';
        } else {
            vehiclesContainer.classList.remove('list-view');
            vehiclesContainer.classList.add('grid-view');
            toggleViewBtn.textContent = 'Switch to List View';
        }
    });

    // Reset filters and search
    resetFiltersBtn.addEventListener('click', function () {
        searchInput.value = '';
        brandFilter.value = 'all';
        descFilter.value = 'all';
        sortSelect.value = 'alphabetical';
        filterAndSortVehicles();
    });

});