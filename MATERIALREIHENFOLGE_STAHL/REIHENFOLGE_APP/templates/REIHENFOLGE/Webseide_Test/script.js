var beispiel = [
  { x: 3, y: 950 },
  { x: 5, y: 250 },
  { x: 2, y: 750 },
  { x: 4, y: 250 },
  { x: 4, y: 150 },
  { x: 2, y: 650 },
  { x: 3, y: 500 },
  { x: 1, y: 500 },
  { x: 1, y: 700 },
  { x: 3, y: 800 },
  { x: 4, y: 400 },
  { x: 5, y: 700 },
  { x: 1, y: 450 },
  { x: 3, y: 850 },
  { x: 3, y: 850 },
  { x: 1, y: 300 },
  { x: 2, y: 650 },
  { x: 1, y: 600 },
  { x: 4, y: 550 },
  { x: 2, y: 900 },
  { x: 3, y: 300 },
  { x: 1, y: 350 },
  { x: 4, y: 150 },
  { x: 2, y: 950 },
  { x: 4, y: 650 },
  { x: 4, y: 500 },
  { x: 4, y: 650 },
  { x: 3, y: 550 },
  { x: 1, y: 650 },
  { x: 2, y: 550 },
  { x: 5, y: 750 },
  { x: 1, y: 550 },
  { x: 5, y: 1000 },
  { x: 3, y: 250 },
  { x: 5, y: 150 },
  { x: 1, y: 150 },
  { x: 3, y: 100 },
  { x: 1, y: 450 },
  { x: 5, y: 450 },
  { x: 1, y: 400 },
  { x: 4, y: 800 },
  { x: 5, y: 650 },
  { x: 5, y: 800 },
  { x: 1, y: 950 },
  { x: 2, y: 1000 },
  { x: 2, y: 200 },
  { x: 5, y: 150 },
  { x: 3, y: 700 },
  { x: 5, y: 100 },
  { x: 1, y: 550 },
];
var xyValues = [
  //Punkte in Graph
  { x: 55, y: 20 },
  { x: 60, y: 10 },
  { x: 56, y: 15 },
  { x: 54, y: 16 },
  { x: 55, y: 11 },
  { x: 59, y: 13 },
];

var xyValues_connect = [
  { x: 54, y: 16 }, //Linie von diesem Punkt
  { x: 55, y: 20 }, //zu diesesm Punkt
  { x: null, y: null }, //trennung für die nächste Linie
  { x: 55, y: 20 },
  { x: 55, y: 11 },
  { x: null, y: null },
  { x: 55, y: 11 },
  { x: 56, y: 15 },
  { x: null, y: null },
  { x: 59, y: 13 },
  { x: 60, y: 10 },
  { x: null, y: null },
  { x: 54, y: 16 },
  { x: 55, y: 11 },
  { x: null, y: null },
  { x: 55, y: 20 },
  { x: 56, y: 15 },
  { x: null, y: null },
  { x: 56, y: 15 },
  { x: 54, y: 16 },
];
var xAchse_Name = "Dicke";
var yAchse_Name = "Breite";
var xValues = [54, 55, 55, 56, 59, 60];
var yValues = [16, 11, 20, 15, 13, 10];
// var yValues2 = [16, 20, 11, 15, 13, 10];
var ypunkt1_1 = [
  { x: 55, y: 11 },
  { x: 54, y: 16 },
];
var ypunkt1_2 = [16, 20];

new Chart("myChart", {
  data: {
    datasets: [
      {
        type: "scatter",
        pointRadius: 4,
        pointBackgroundColor: "rgb(0,0,255)",
        data: beispiel,
      },
      /*{
        type: "line",
        backgroundColor: "rgba(0,0,0,1.0)",
        borderColor: "rgba(0,0,0,1)",
        data: beispiel,
      },*/
      /* {
              type: "line",
              backgroundColor: "rgba(255,0,0,1.0)",S
              borderColor: "rgba(255,0,0,1)",
              data: ypunkt1_2,
            }, */
    ],
    labels: xValues,
  },
  options: {
    plugins: {
      legend: false,
    },
    scales: {
      x: {
        ticks: { min: 40, max: 160 },
        title: {
          display: true,
          text: xAchse_Name,
        },
      },
      y: {
        ticks: { min: 6, max: 16 },
        title: {
          display: true,
          text: yAchse_Name,
        },
      },
    },
  },
});
