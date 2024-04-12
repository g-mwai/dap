document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById("userCountChart").getContext("2d");

    const chart = new Chart(ctx, {
        type: "line",
        data: {
            labels: [], // Empty array for dynamic labels
            datasets: [
                {
                    label: "User Growth",
                    backgroundColor: "#79AEC8",
                    borderColor: "#417690",
                    data: []
                }
            ]
        },
        options: {
            title: {
                text: "User Growth",
                display: true
            }
        }
    });

    const startDateInput = document.getElementById('start-date');
    const endDateInput = document.getElementById('end-date');
    const applyFilterButton = document.getElementById('apply-filter');

    applyFilterButton.addEventListener('click', function () {
        const startDate = startDateInput.value;
        const endDate = endDateInput.value;

        fetchUserGrowthData(startDate, endDate);
    });

    function fetchUserGrowthData(startDate, endDate) {
        const url = `/user_count_chart/?start_date=${startDate}&end_date=${endDate}`;
        $.ajax({
            url: url,
            type: 'GET',
            success: function(response) {
                updateChart(response.labels, response.counts);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    }

    function updateChart(labels, counts) {
        chart.data.labels = labels;
        chart.data.datasets[0].data = counts;
        chart.update();
    }

    // Initial chart rendering and data fetching
    fetchUserGrowthData();
});
