document.addEventListener('DOMContentLoaded', function () {
    fetch('/product-evaluation/api/product-evaluation-summary/')
        .then(response => response.json())
        .then(data => {
            const table = $('#product-evaluation-table').DataTable({
                data: data,
                columns: [
                    { data: 'asset', title: 'Asset' },
                    { data: 'most_recent_date_sampled', title: 'Most Recent Date Sampled' },
                    { data: 'pass_count', title: 'Pass Count' },
                    { data: 'fail_count', title: 'Fail Count' },
                    { data: 'daily_fail', title: 'Daily Fail' },
                    { data: 'week_range', title: 'Week Range' },
                    { data: 'week_fail', title: 'Week Fail' },
                    { data: 'month_range', title: 'Month Range' },
                    { data: 'month_fail', title: 'Month Fail' },
                    { data: 'ytd_range', title: 'YTD Range' },
                    { data: 'ytd_fail', title: 'YTD Fail' },
                    { data: 'prev_year_range', title: 'Prev Year Range' },
                    { data: 'prev_year_fail', title: 'Prev Year Fail' },
                ],
                paging: false,
                info: false,
                responsive: true,
                searching: true,
                scrollX: true,
            });

            function applyDarkModeStyles() {
                const tableContainer = document.querySelector('#product-evaluation-table');
                const tableWrapper = tableContainer.querySelector('.dataTables_wrapper');
                tableWrapper.classList.remove('bg-white');
                tableWrapper.classList.add('bg-gray-800', 'shadow-md', 'rounded', 'my-6');

                const tableElement = tableContainer.querySelector('table');
                tableElement.classList.remove('text-gray-700');
                tableElement.classList.add('text-gray-200');

                const tableHeaders = tableWrapper.querySelectorAll('thead th');
                tableHeaders.forEach(header => {
                    header.classList.remove('bg-gray-100', 'text-gray-700');
                    header.classList.add('bg-gray-700', 'text-gray-200', 'font-bold');
                });

                const tableRows = tableWrapper.querySelectorAll('tbody tr');
                tableRows.forEach(row => {
                    row.classList.remove('bg-white', 'hover:bg-gray-100');
                    row.classList.add('bg-gray-800', 'hover:bg-gray-700');
                });

                const tableCells = tableWrapper.querySelectorAll('tbody td');
                tableCells.forEach(cell => {
                    cell.classList.remove('text-gray-700');
                    cell.classList.add('text-gray-200');
                });
            }

            function applyLightModeStyles() {
                const tableContainer = document.querySelector('#product-evaluation-table');
                const tableWrapper = tableContainer.querySelector('.dataTables_wrapper');
                tableWrapper.classList.remove('bg-gray-800');
                tableWrapper.classList.add('bg-white', 'shadow-md', 'rounded', 'my-6');

                const tableElement = tableContainer.querySelector('table');
                tableElement.classList.remove('text-gray-200');
                tableElement.classList.add('text-gray-700');

                const tableHeaders = tableWrapper.querySelectorAll('thead th');
                tableHeaders.forEach(header => {
                    header.classList.remove('bg-gray-700', 'text-gray-200');
                    header.classList.add('bg-gray-100', 'text-gray-700', 'font-bold');
                });

                const tableRows = tableWrapper.querySelectorAll('tbody tr');
                tableRows.forEach(row => {
                    row.classList.remove('bg-gray-800', 'hover:bg-gray-700');
                    row.classList.add('bg-white', 'hover:bg-gray-100');
                });

                const tableCells = tableWrapper.querySelectorAll('tbody td');
                tableCells.forEach(cell => {
                    cell.classList.remove('text-gray-200');
                    cell.classList.add('text-gray-700');
                });
            }

            function updateTableStyles() {
                if (document.documentElement.classList.contains('dark')) {
                    applyDarkModeStyles();
                } else {
                    applyLightModeStyles();
                }
            }

            document.addEventListener('dark-mode', function () {
                updateTableStyles();
            });

            updateTableStyles();
        });
});