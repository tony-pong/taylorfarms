document.addEventListener('DOMContentLoaded', function () {
    const endpoints = [
        '/failures/snapshot-shelflife-this-month/',
        '/failures/snapshot-shelflife-last-month/',
        '/failures/snapshot-shelflife-two-months-ago/'
    ];

    const elementIds = [
        'this-month-failure-snapshot-1',
        'this-month-failure-snapshot-2',
        'this-month-failure-snapshot-3'
    ];

    elementIds.forEach((id, index) => {
        fetch(endpoints[index])
            .then(response => response.json())
            .then(data => {
                // Extract data from the JSON response
                const { title, labels, counts } = data;

                // Generate options for ApexCharts
                const options = {
                    series: [
                        {
                            name: title,
                            data: counts,
                        },
                    ],
                    chart: {
                        height: 420,
                        type: 'bar', // Keep as bar but swap xaxis and yaxis below
                        fontFamily: 'Inter, sans-serif',
                    },
                    fill: {
                        type: 'gradient',
                    },
                    dataLabels: {
                        enabled: true, // Enable data labels
                    },
                    tooltip: {
                        style: {
                            fontSize: '14px',
                            fontFamily: 'Inter, sans-serif',
                        },
                    },
                    plotOptions: {
                        bar: {
                            horizontal: true, // Make the Bars horizontal
                        },
                    },
                    xaxis: {
                        categories: labels, // Treats labels as xaxis
                        labels: {
                            style: {
                                fontSize: '14px',
                                fontWeight: 500,
                            },
                        },
                    },
                    yaxis: {
                        labels: {
                            style: {
                                fontSize: '14px',
                                fontWeight: 500,
                            },
                        },
                    },
                    title: {
                        text: title,
                        align: 'center',
                        margin: 20,
                        offsetX: 0,
                        offsetY: 0,
                        floating: false,
                        style: {
                            fontSize: '18px',
                            fontWeight: 600,
                            fontFamily: 'Inter, sans-serif',
                            color: '#263238',
                        },
                    },
                };

                // Generate chart
                const chart = new ApexCharts(document.getElementById(id), options);
                chart.render();
            })
            .catch(error => console.error('Error fetching data:', error));
    });

});