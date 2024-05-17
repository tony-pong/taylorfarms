document.addEventListener('DOMContentLoaded', function () {
    let chartData = [
        { name: 'Previous 12-24 Months', data: [] },
        { name: 'Last 12 Months', data: [] }
    ];

    function mapData(data, monthNames) {
        return monthNames.map(monthName => {
            const item = data.find(item => {
                const itemDate = new Date(item.month);
                return itemDate.toLocaleString('default', { month: 'short' }) === monthName;
            });
            return item ? item.total : null;
        });
    }
function getMonthNames(data) {
    const monthNames = data.recent_data.map(item => {
        const itemDate = new Date(item.month);
        return itemDate.toLocaleString('default', { month: 'short' });
    });
    return monthNames;
}
    function getChartOptions(chartData, monthNames) {
        let mainChartColors = {
            borderColor: document.documentElement.classList.contains('dark') ? '#374151' : '#F3F4F6',
            labelColor: document.documentElement.classList.contains('dark') ? '#9CA3AF' : '#6B7280',
            background: document.documentElement.classList.contains('dark') ? '#000000' : '#FFFFFF'
        };

        return {
            chart: {
                type: 'bar',
                height: 420,
                fontFamily: 'Inter, sans-serif',
                foreColor: mainChartColors.labelColor,
                toolbar: {
                    show: false
                },
                background: mainChartColors.background
            },

            series: chartData.map(series => ({
                name: series.name,
                data: series.data
            })),
            plotOptions: {
                bar: {
                    horizontal: false,
                    columnWidth: '55%',
                    endingShape: 'rounded'
                }
            },
            xaxis: {
                type: 'category',
                categories: monthNames
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

    async function fetchChartData(chart) {
        const selectedCommodities = Array.from(document.getElementById('commodity-filter').selectedOptions).map(opt => opt.value);
        const params = new URLSearchParams();
        if (selectedCommodities.length > 0) {
            selectedCommodities.forEach(commodity => params.append('commodity', commodity));
        }

        try {
            let response = await fetch(`/failures/rolling-yoy-data-filtered/?${params.toString()}`);
            let data = await response.json();
            console.log('Fetched data:', data); // Check if the data is fetched correctly

            const monthNames = getMonthNames(data);
            const recentDataProcessed = mapData(data.recent_data, monthNames);
            const previousDataProcessed = mapData(data.previous_data, monthNames);

            chartData = [
                { name: 'Previous 12-24 Months', data: previousDataProcessed },
                { name: 'Last 12 Months', data: recentDataProcessed }
            ];

            chart.updateOptions(getChartOptions(chartData, monthNames));
            chart.updateSeries(chartData, false);

let dropdown = document.getElementById('commodity-filter');
// Clear existing options
dropdown.innerHTML = '';

// Sort the commodities alphabetically
const sortedCommodities = data.commodities.sort();

for (let commodity of sortedCommodities) {
    if (commodity !== null) {
        let option = document.createElement('option');
        option.text = commodity;
        option.value = commodity;
        dropdown.add(option);
    }
}
        } catch (error) {
            console.error('Error loading the chart data:', error);
        }
    }

async function initializeChart() {
    const chartElement = document.getElementById('rolling-yoy-chart-filtered');
    console.log('Chart element:', chartElement); // Check if the chart element is found

    if (!chartElement) {
        console.error('Chart element not found on the page.');
        return;
    }

    const chart = new ApexCharts(chartElement, {
        chart: {
            type: 'bar',
            height: 420
        },
        series: [],
        xaxis: {
            categories: []
        }
    });

    chart.render();

    const filterForm = document.getElementById('commodity-form');
    filterForm.addEventListener('submit', function (event) {
        event.preventDefault();
        fetchChartData(chart);
    });

    const clearFilterButton = document.getElementById('clear-filter');
    clearFilterButton.addEventListener('click', function () {
        const filterElement = document.getElementById('commodity-filter');
        filterElement.selectedIndex = -1;
        fetchChartData(chart);
    });

    document.addEventListener('dark-mode', function () {
        chart.updateOptions(getChartOptions(chartData, chart.w.globals.categoryLabels));
    });

    await fetchChartData(chart);
}

    initializeChart();
});