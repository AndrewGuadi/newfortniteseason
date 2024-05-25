document.addEventListener('DOMContentLoaded', function() {
    // Rank buttons event listeners
    const rankButtons = document.querySelectorAll('.rank-button');
    rankButtons.forEach(button => {
        button.addEventListener('click', function() {
            const rank = this.dataset.rank;

            // Remove active class from all buttons
            rankButtons.forEach(btn => btn.classList.remove('active-rank'));

            // Add active class to the clicked button
            this.classList.add('active-rank');

            // Update weapon stats
            updateStats('stats-body-', rank);
            updateHeaders('rank-header-', rank);
        });
    });

    // Category tabs event listeners
    const categoryTabs = document.querySelectorAll('#categoryTab a');
    categoryTabs.forEach(tab => {
        tab.addEventListener('shown.bs.tab', function(event) {
            const targetId = event.target.getAttribute('href').substring(1); // e.g., 'weapons' or 'items'
            const rankButtonsContainer = document.querySelector('.btn-group');

            if (targetId === 'weapons') {
                rankButtonsContainer.style.display = 'block';
                updateStats('stats-body-', 'common'); // Reset to common on tab switch
                updateHeaders('rank-header-', 'common');
            } else if (targetId === 'items') {
                rankButtonsContainer.style.display = 'none';
                updateStats('stats-body-item-', 'common'); // Reset to common on tab switch
                updateHeaders('rank-header-item-', 'common');
            }
        });
    });

    // Function to update stats
    function updateStats(bodyPrefix, rank) {
        const tables = document.querySelectorAll(`tbody[id^="${bodyPrefix}"]`);
        tables.forEach(tbody => {
            const rows = tbody.querySelectorAll('tr');
            rows.forEach(row => {
                const selectedCell = row.querySelector(`td.${rank}`);
                const statValueCell = row.querySelector('td:nth-child(2)');
                if (selectedCell) {
                    statValueCell.textContent = selectedCell.textContent;
                    // Remove existing rank classes
                    statValueCell.classList.remove('common', 'uncommon', 'rare', 'epic', 'legendary');
                    // Add the new rank class
                    statValueCell.classList.add(rank);
                }
            });
        });
    }

    // Function to update headers
    function updateHeaders(headerPrefix, rank) {
        const headers = document.querySelectorAll(`th[id^="${headerPrefix}"]`);
        headers.forEach(header => {
            // Update header text
            header.textContent = rank.charAt(0).toUpperCase() + rank.slice(1);
            // Remove existing rank classes
            header.classList.remove('common', 'uncommon', 'rare', 'epic', 'legendary');
            // Add the new rank class
            header.classList.add(rank);
        });
    }
});
