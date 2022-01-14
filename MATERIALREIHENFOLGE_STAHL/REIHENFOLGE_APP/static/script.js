// First Load of the WebSide
var firstTime = localStorage.getItem("first_time");
if (!firstTime) {
  // first time loaded!
  localStorage.setItem("first_time", "1");
  localStorage.setItem("Breite", "10");
  localStorage.setItem("Dicke", "10");
} else {
  location.href =
    "http://127.0.0.1:8000/display_graph/" + tol_breite + "/" + tol_dicke;
}

// Get Toleranzes and Store in LocalStorage
function updateToleranz() {
  var tol_dicke = document.getElementById("input_dicke").value;
  var tol_breite = document.getElementById("input_breite").value;
  localStorage.setItem("Breite", tol_breite);
  localStorage.setItem("Dicke", tol_dicke);
  location.href =
    "http://127.0.0.1:8000/display_graph/" + tol_breite + "/" + tol_dicke;
}

function onChangeAxisButtonClick() {
  var coils = coils
  var xAchse_Name = "Breite";
      var yAchse_Name = "Dicke";
  
}
