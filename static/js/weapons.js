document.addEventListener('DOMContentLoaded', function() {
    const rankButtons = document.querySelectorAll('.rank-button');
    rankButtons.forEach(button => {
        button.addEventListener('click', function() {
            const rank = this.dataset.rank;

            // Remove active class from all buttons
            rankButtons.forEach(btn => btn.classList.remove('active-rank'));

            // Add active class to the clicked button
            this.classList.add('active-rank');

            const tables = document.querySelectorAll('tbody[id^="stats-body-"]');
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
            const headers = document.querySelectorAll('th[id^="rank-header-"]');
            headers.forEach(header => {
                // Update header text
                header.textContent = rank.charAt(0).toUpperCase() + rank.slice(1);
                // Remove existing rank classes
                header.classList.remove('common', 'uncommon', 'rare', 'epic', 'legendary');
                // Add the new rank class
                header.classList.add(rank);
            });
        });
    });
});
