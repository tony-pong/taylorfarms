document.addEventListener('DOMContentLoaded', function () {
    async function initializeChart() {
        const chartElement = document.getElementById('rolling-yoy-chart');
        console.log('Chart element:', chartElement);

        if (!chartElement) {
            console.error('Chart element not found on the page.');
            return;
        }

        const chart = new ApexCharts(chartElement, getChartOptions());
        chart.render();
        await fetchChartData(chart);

        // init again when toggling dark mode
        document.addEventListener('dark-mode', function () {
            chart.updateOptions(getChartOptions());
        });
    }

    async function fetchChartData(chart) {
        try {
            let response = await fetch(`/failures/rolling-yoy-data/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            let data = await response.json();
            console.log('Fetched data:', data);
            processChartData(chart, data);
        } catch (error) {
            console.error('Error loading the chart data:', error);
        }
    }


function processChartData(chart, data) {
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth(); // 0-indexed
    const currentYear = currentDate.getFullYear();

    console.log('Current Month:', currentMonth, 'Current Year:', currentYear);

    // Filter the data to exclude the current month and year for both recent and previous data
    const recentDataFiltered = filterData(data.recent_data, currentMonth, currentYear);
    const previousDataFiltered = filterData(data.previous_data, currentMonth, currentYear);

    console.log('Filtered Recent Data:', recentDataFiltered);
    console.log('Filtered Previous Data:', previousDataFiltered);

    updateChart(chart, recentDataFiltered, previousDataFiltered);
}

function filterData(data, currentMonth, currentYear) {
    // Filter out the current month and year
    const filteredData = data.filter(item => {
        const date = new Date(item.month);
        return !(date.getMonth() === currentMonth && date.getFullYear() === currentYear);
    }).slice(1); // Remove the first element (current month)

    console.log('Filtered Data (excluding current month and year):', filteredData);

    return filteredData;
}

function updateChart(chart, recentData, previousData) {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

    const currentDate = new Date();
    const currentMonth = currentDate.getMonth(); // 0-indexed

    // Since we want our months reversed, we'll start from the current month and rotate back
    const xaxisLabels = [];
    for(let i=0; i < 12; i++) {
        const index = (currentMonth - i + 12) % 12; // +12 to ensure we're getting a positive index
        xaxisLabels.push(monthNames[index]);
    }

    console.log('X-Axis Labels:', xaxisLabels);

    chart.updateOptions({
        xaxis: {
            categories: xaxisLabels
        }
    });

    chart.updateSeries([
        { name: 'Previous 12-24 Months', data: previousData.map(item => item.total) },
        { name: 'Last 12 Months', data: recentData.map(item => item.total) }
    ]);
}function updateChart(chart, recentData, previousData) {
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

        const currentDate = new Date();
        let currentMonth = currentDate.getMonth(); // 0-indexed
        currentMonth--; // subtract 1 to start from the previous month

        // Since we want our months reversed, we'll start from the current month and rotate back
        const xaxisLabels = [];
        for(let i=0; i < 12; i++) {
            const index = (currentMonth - i + 12) % 12; // +12 to ensure we're getting a positive index
            xaxisLabels.push(monthNames[index]);
        }

        console.log('X-Axis Labels:', xaxisLabels);

        chart.updateOptions({
            xaxis: {
                categories: xaxisLabels
            }
        });

        chart.updateSeries([
            { name: 'Previous 12-24 Months', data: previousData.map(item => item.total) },
            { name: 'Last 12 Months', data: recentData.map(item => item.total) }
        ]);
    }

    function getChartOptions() {
        let mainChartColors = {};

        if (document.documentElement.classList.contains('dark')) {
            mainChartColors = {
                borderColor: '#374151',
                labelColor: '#9CA3AF',
                background: '#000000'
            };
        } else {
            mainChartColors = {
                borderColor: '#F3F4F6',
                labelColor: '#6B7280',
                background: '#FFFFFF'
            };
        }

        return {
            chart: {
                type: 'line',
                height: 420,
                fontFamily: 'Inter, sans-serif',
                foreColor: mainChartColors.labelColor,
                toolbar: {
                    show: false
                },
                background: mainChartColors.background
            },
            series: [
                { name: 'Previous 12-24 Months', data: [] },
                { name: 'Last 12 Months', data: [] }
            ],
            xaxis: {
                type: 'category',
                categories: [] // Will be set dynamically
            },
            yaxis: {
                labels: {
                    formatter: function (value) {
                        return value + ' failures';
                    }
                }
            },
            tooltip: {
                x: {
                    format: 'MMM'
                }
            },
            grid: {
                borderColor: mainChartColors.borderColor
            },
            legend: {
                labels: {
                    colors: mainChartColors.labelColor
                }
            }
        };
    }

    initializeChart();
});