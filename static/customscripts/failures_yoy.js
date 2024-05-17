document.addEventListener('DOMContentLoaded', function () {
    let chartData = [
        { name: 'Previous 12-24 Months', data: [] },
        { name: 'Last 12 Months', data: [] }
    ];

    async function initializeChart() {
        const chartElement = document.getElementById('rolling-yoy-chart');
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
            let response = await fetch(`/failures/rolling-yoy-data/`);
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
        const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        let recentDataProcessed = mapData(data.recent_data, monthNames);
        let previousDataProcessed = mapData(data.previous_data, monthNames);

        if (recentDataProcessed.length === 0 || previousDataProcessed.length === 0) {
            console.error('Data missing for one or both series:', { recentDataProcessed, previousDataProcessed });
        }

        chartData = [
            { name: 'Previous 12-24 Months', data: previousDataProcessed },
            { name: 'Last 12 Months', data: recentDataProcessed }
        ];
    }

    function mapData(data, monthNames) {
        return data.map(item => {
            let date = new Date(item.month);
            return { x: monthNames[date.getMonth()], y: item.total };
        });
    }

    function getChartOptions(chartData) {
        let mainChartColors = {}

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
            }
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
                type: 'category',
                categories: getLast12Months()
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

    function getLast12Months() {
        const months = [];
        const date = new Date();
        date.setMonth(date.getMonth() - 11); // Set to 11 months ago
        for (let i = 0; i < 12; i++) {
            months.push(date.toLocaleString('default', { month: 'short' }));
            date.setMonth(date.getMonth() + 1);
        }
        return months;
    }

    initializeChart();
});