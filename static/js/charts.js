const data = {
    labels: serverData[0],
    datasets: [{
        label: 'Item 0 Price',
        backgroundColor: 'rgb(255, 99, 132)',
        borderColor: 'rgb(255, 99, 132)',
        data: serverData[1],
    }]
};

const config = {
    type: 'line',
    data,
    options: {}
};

var chart = new Chart(
    document.getElementById('chart'),
    config
);