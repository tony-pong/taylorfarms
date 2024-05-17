document.addEventListener('DOMContentLoaded', function () {
    const chartElement = document.getElementById('chart');
    let chart;

function initChart(data) {
    if (!data.records || data.records.length === 0) {
        console.error("No data available to display.");
        chartElement.innerHTML = "<p style='color: red;'>No data available to display.</p>"; // Show a red message if no data
        return;
    }

        const isDarkMode = document.body.classList.contains('dark');
        const totalHeight = data.records.length * 30; // Ensuring each bar has at least 30px for visibility

        const options = {
            series: [{
                name: 'Total',
                data: data.records.map(item => item.total)
            }],
            chart: {
                type: 'bar',
                height: Math.max(totalHeight, 550), // Adaptive height with a minimum
                orientation: 'horizontal',
                parentHeightOffset: 0,
                toolbar: {
                    show: false
                },
                background: isDarkMode ? '#333' : '#fff',
                foreColor: isDarkMode ? '#ccc' : '#333',
            },
            plotOptions: {
                bar: {
                    horizontal: true,
                    barHeight: '100%', // Full height for bars within their categories
                    distributed: true,
                }
            },
            colors: ['#FF4560', '#00E396', '#008FFB', '#FEB019', '#775DD0'], // Modern color palette
            dataLabels: {
                enabled: false
            },
            xaxis: {
                categories: data.records.map(item => item.item_number_description),
            },
            yaxis: {
                title: {
                    text: 'Total',
                }
            },
            tooltip: {
                theme: isDarkMode ? 'dark' : 'light'
            },
            legend: {
                show: false // No legend required
            }
        };

        if (chart) {
            chart.updateOptions(options);
        } else {
            chart = new ApexCharts(chartElement, options);
            chart.render();
        }
    }

    function populateDropdowns(usernames, commodities, customers) {
        const usernameSelect = document.getElementById('user_name_filter');
        const commoditySelect = document.getElementById('commodity_filter');
        const customerSelect = document.getElementById('customer_filter');

        // Clear existing options and add "All" option
        usernameSelect.innerHTML = '<option value="all">All Supervisors</option>';
        commoditySelect.innerHTML = '<option value="all">All Commodities</option>';
        customerSelect.innerHTML = '<option value="all">All Customers</option>';

        usernames.forEach(function(username) {
            usernameSelect.innerHTML += `<option value="${username}">${username}</option>`;
        });

        commodities.forEach(function(commodity) {
            commoditySelect.innerHTML += `<option value="${commodity}">${commodity}</option>`;
        });

        customers.forEach(function(customer) {
            customerSelect.innerHTML += `<option value="${customer}">${customer}</option>`;
        });
    }

    function fetchData() {
        const url = new URL('/failures/ajax-filter-data/', window.location.origin);
        appendFilterParams(url);

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                initChart(data);
                populateDropdowns(data.usernames, data.commodities, data.customers);
                setDatePickerLimits(data.earliest_date, data.latest_date);
            })
            .catch(error => console.error('Error:', error));
    }

    function appendFilterParams(url) {
        const dateStart = document.getElementById('date_start').value;
        const dateEnd = document.getElementById('date_end').value;
        const userSelect = document.getElementById('user_name_filter');
        const commoditySelect = document.getElementById('commodity_filter');
        const customerSelect = document.getElementById('customer_filter');

        if (dateStart) url.searchParams.append('date_start', dateStart);
        if (dateEnd) url.searchParams.append('date_end', dateEnd);

        if (userSelect.value !== 'all') {
            Array.from(userSelect.selectedOptions).forEach(option => {
                url.searchParams.append('user_name', option.value);
            });
        }

        if (commoditySelect.value !== 'all') {
            Array.from(commoditySelect.selectedOptions).forEach(option => {
                url.searchParams.append('commodity', option.value);
            });
        }

        if (customerSelect.value !== 'all') {
            Array.from(customerSelect.selectedOptions).forEach(option => {
                url.searchParams.append('customer', option.value);
            });
        }
    }

    function setDatePickerLimits(earliest, latest) {
        document.getElementById('date_start').min = earliest;
        document.getElementById('date_start').max = latest;
        document.getElementById('date_end').min = earliest;
        document.getElementById('date_end').max = latest;
    }

    document.getElementById('apply_filters').addEventListener('click', fetchData);

document.getElementById('clear_filters').addEventListener('click', function () {
    document.getElementById('date_start').value = '';
    document.getElementById('date_end').value = '';
    document.getElementById('user_name_filter').selectedIndex = 0;  // Reset to "All"
    document.getElementById('commodity_filter').selectedIndex = 0;  // Reset to "All"
    document.getElementById('customer_filter').selectedIndex = 0;  // Reset to "All"

    // Clear any existing messages from the chart element and show a temporary message
    chartElement.innerHTML = "<p style='color: red;'>Filters cleared. Loading data...</p>";

    // Use setTimeout to delay the fetchData function call by 3000 milliseconds (3 seconds)
    setTimeout(function() {
        fetchData(); // Fetch unfiltered data after a delay
    }, 7000);
});



    fetchData(); // Initial fetch to load the chart with default (unfiltered) data
});