
    const ctx = document.getElementById('racingChart').getContext('2d');
    const monthlyCtx = document.getElementById('monthlyChart').getContext('2d');

    const baseColors = [
        'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)',
        'rgba(255, 206, 86, 0.6)', 'rgba(75, 192, 192, 0.6)',
        'rgba(153, 102, 255, 0.6)', 'rgba(255, 159, 64, 0.6)'
    ];
    let labelColors = {};

    function getLabelColor(label) {
        if (!labelColors[label]) {
            labelColors[label] = baseColors[Object.keys(labelColors).length % baseColors.length];
        }
        return labelColors[label];
    }

    const racingChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: '',
                data: [],
                backgroundColor: [],
                borderColor: [],
                borderWidth: 1
            }]
        },
        options: createChartOptions('Cumulative Failures shown by Month and Year:')
    });

    const monthlyChart = new Chart(monthlyCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: '',
                data: [],
                backgroundColor: [],
                borderColor: [],
                borderWidth: 1
            }]
        },
        options: createChartOptions('Monthly Failures shown by Month and Year:')
    });

    function createChartOptions(titleText) {
        return {
            responsive: true,
            indexAxis: 'y',
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return numberWithCommas(value);
                        }
                    }
                }
            },
            elements: {
                bar: {
                    tension: 0.4
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: titleText,
                    font: {
                        size: 28
                    },
                    position: 'top',
                    align: 'start'
                },
                legend: {
                    display: false
                }
            },
            animation: {
                duration: 2000
            }
        };
    }

    function numberWithCommas(value) {
        return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    }

    let cumulativeMonthIndex = 0;
    let monthlyMonthIndex = 0;
    let cumulativeData = {};
    let monthlyData = {};
    let isCumulativeAnimating = true;
    let isMonthlyAnimating = true;

    function fetchData() {
        fetch('/failures/racing-chart-data/')
            .then(response => response.json())
            .then(data => {
                if (isCumulativeAnimating) updateChart(data, 'cumulative');
                if (isMonthlyAnimating) updateChart(data, 'monthly');
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    }

    function updateChart(data, chartType) {
        let index = chartType === 'cumulative' ? cumulativeMonthIndex : monthlyMonthIndex;
        if (index < data.length) {
            let chart = chartType === 'cumulative' ? racingChart : monthlyChart;
            let dataStorage = chartType === 'cumulative' ? cumulativeData : monthlyData;

            // Reset monthly data storage each time for non-cumulative display
            if (chartType === 'monthly') dataStorage = {};

            let labelData = [];
            data[index].labels.forEach((label, i) => {
                if (!dataStorage.hasOwnProperty(label)) dataStorage[label] = 0;
                dataStorage[label] += data[index].values[i];
                labelData.push({ label: label, value: dataStorage[label], color: getLabelColor(label) });
            });

            // Sort and slice the top 20 results
            labelData.sort((a, b) => b.value - a.value);
            labelData = labelData.slice(0, 20);

            chart.data.labels = labelData.map(item => item.label);
            chart.data.datasets[0].data = labelData.map(item => item.value);
            chart.data.datasets[0].backgroundColor = labelData.map(item => item.color);
            chart.data.datasets[0].borderColor = labelData.map(item => item.color.replace('0.6', '1'));

            chart.options.plugins.title.text = chartType.charAt(0).toUpperCase() + chartType.slice(1) + ' Failures shown by Month and Year: ' + data[index].yearMonth;
            chart.update();

            if (chartType === 'cumulative') {
                cumulativeMonthIndex++;
            } else {
                monthlyMonthIndex++;
            }

            setTimeout(() => {
                if ((chartType === 'cumulative' && isCumulativeAnimating) || (chartType === 'monthly' && isMonthlyAnimating)) {
                    updateChart(data, chartType);
                }
            }, 3000);
        } else {
            if (chartType === 'cumulative') {
                isCumulativeAnimating = false;
                document.getElementById('cumulativeToggleButton').innerText = 'Start Animation';
            } else {
                isMonthlyAnimating = false;
                document.getElementById('monthlyToggleButton').innerText = 'Start Animation';
            }
        }
    }

    function toggleAnimation(chartType) {
        if (chartType === 'cumulative') {
            isCumulativeAnimating = !isCumulativeAnimating;
            document.getElementById('cumulativeToggleButton').innerText = isCumulativeAnimating ? 'Stop Animation' : 'Start Animation';
            if (isCumulativeAnimating) fetchData();
        } else {
            isMonthlyAnimating = !isMonthlyAnimating;
            document.getElementById('monthlyToggleButton').innerText = isMonthlyAnimating ? 'Stop Animation' : 'Start Animation';
            if (isMonthlyAnimating) fetchData();
        }
    }

    function goBackOneStep(chartType) {
        if (chartType === 'cumulative') {
            cumulativeMonthIndex = Math.max(0, cumulativeMonthIndex - 1);
        } else {
            monthlyMonthIndex = Math.max(0, monthlyMonthIndex - 1);
        }
        fetchData();
    }

    document.getElementById('cumulativeToggleButton').addEventListener('click', () => toggleAnimation('cumulative'));
    document.getElementById('cumulativeBackButton').addEventListener('click', () => goBackOneStep('cumulative'));
    document.getElementById('cumulativeReloadButton').addEventListener('click', () => {
        cumulativeMonthIndex = 0;  // Reset the index for cumulative chart
        cumulativeData = {};       // Reset the data storage for cumulative chart
        isCumulativeAnimating = true; // Ensure animation is enabled
        fetchData();               // Fetch and display the updated data
    });

    document.getElementById('monthlyToggleButton').addEventListener('click', () => toggleAnimation('monthly'));
    document.getElementById('monthlyBackButton').addEventListener('click', () => goBackOneStep('monthly'));
    document.getElementById('monthlyReloadButton').addEventListener('click', () => {
        monthlyMonthIndex = 0;     // Reset the index for monthly chart
        monthlyData = {};          // Reset the data storage for monthly chart
        isMonthlyAnimating = true; // Ensure animation is enabled
        fetchData();               // Fetch and display the updated data
    });

    // Initialize both charts
    fetchData(); // Start both charts automatically on load
