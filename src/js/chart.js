import Chart from "chart.js/auto";

document.addEventListener("DOMContentLoaded", () => {
  const chartElement = document.getElementById("chart");
  const chartDataElement = document.getElementById("chart-data");

  if (chartElement && chartDataElement) {
    var chart = new Chart(document.getElementById("chart"), {
      type: "pie",
      data: JSON.parse(document.getElementById("chart-data").textContent),
      options: {
        responsive: true,
      },
      plugins: {
        legend: {
          display: true,
          position: "left",
        },
      },
    });
  }
});
