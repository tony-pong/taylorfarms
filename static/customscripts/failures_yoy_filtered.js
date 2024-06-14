document.addEventListener('DOMContentLoaded', function () {
    let chartData = [
        { name: 'Previous 12-24 Months', data: [] },
        { name: 'Last 12 Months', data: [] }
    ];

function getXAxisLabels() {
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const currentDate = new Date();
    const currentMonthIndex = currentDate.getMonth();
    const xAxisLabels = [];

    for (let i = 1; i <= 12; i++) {
        const index = (currentMonthIndex - i + 12) % 12;
        xAxisLabels.push(monthNames[index]);
    }

    return xAxisLabels.slice(0, -1); // Remove the last element (current month)
}
    function mapData(data) {
        return data.slice(1).map(item => item.total);
    }

    function getChartOptions(chartData, xAxisLabels) {
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
                categories: xAxisLabels
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
            console.log('Fetched data:', data);

            const xAxisLabels = getXAxisLabels();
            const recentDataProcessed = mapData(data.recent_data);
            const previousDataProcessed = mapData(data.previous_data);

            chartData = [
                { name: 'Previous 12-24 Months', data: previousDataProcessed },
                { name: 'Last 12 Months', data: recentDataProcessed }
            ];

            console.log('Chart Data:', chartData);
            console.log('X-Axis Labels:', xAxisLabels);

            chart.updateOptions(getChartOptions(chartData, xAxisLabels));
            chart.updateSeries(chartData, false);

            let dropdown = document.getElementById('commodity-filter');
            dropdown.innerHTML = '';

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
        console.log('Chart element:', chartElement);

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