document.addEventListener('DOMContentLoaded', function () {
    let chartData = [];

    const colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#393b79', '#637939', '#8c6d31', '#843c39', '#7b4173', '#5254a3', '#9c9ede', '#8ca252', '#bd9e39', '#ad494a',
        '#a55194', '#6b6ecf', '#b5cf6b', '#e7ba52', '#d6616b', '#ce6dbd', '#6baed6', '#fd8d3c', '#78c679', '#e6550d'
    ];

    async function initializeChart() {
        const chartElement = document.getElementById('product-evaluation-chart');
        console.log('Chart element:', chartElement);

        if (!chartElement) {
            console.error('Chart element not found on the page.');
            return;
        }

        const chart = new ApexCharts(chartElement, getChartOptions(chartData));
        chart.render();

        await fetchChartData(chart);

        document.addEventListener('dark-mode', function () {
            chart.updateOptions(getChartOptions(chartData));
        });
    }

    async function fetchChartData(chart) {
        try {
            let response = await fetch(`/product-evaluation/product-evaluation-chart/`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            let data = await response.json();
            console.log('Fetched data:', data);
            updateChart(data);

            // Update the chart with the new fetched data
            chart.updateSeries(chartData);

        } catch (error) {
            console.error('Error loading the chart data:', error);
        }
    }

    function updateChart(data) {
        chartData = Object.keys(data).map((line, index) => {
            return {
                name: line,
                data: data[line].map(item => {
                    let date = new Date(item.month + '-01'); // Adjust to get the correct date object
                    return { x: date, y: item.fail_percentage };
                }),
                color: colors[index % colors.length]
            };
        });
    }

    function getChartOptions(chartData) {
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
            series: chartData,
            xaxis: {
                type: 'datetime',
                labels: {
                    format: 'MMM yy' // Display month and year
                },
                tickAmount: 12
            },
            yaxis: {
                labels: {
                    formatter: function (value) {
                        return value + '%';
                    }
                }
            },
            tooltip: {
                x: {
                    format: 'MMM yy' // Tooltip displays month and year
                }
            },
            grid: {
                borderColor: mainChartColors.borderColor
            },
            legend: {
                labels: {
                    colors: mainChartColors.labelColor
                }
            },
            colors: chartData.map(series => series.color) // Use the colors defined in the chartData
        };
    }

    function getLast12Months() {
        const months = [];
        const date = new Date();
        date.setMonth(date.getMonth() - 11); // Set to 11 months ago
        for (let i = 0; i < 12; i++) {
            months.push(date.toLocaleString('default', { month: 'short', year: '2-digit' }));
            date.setMonth(date.getMonth() + 1);
        }
        return months;
    }

    initializeChart();
});
