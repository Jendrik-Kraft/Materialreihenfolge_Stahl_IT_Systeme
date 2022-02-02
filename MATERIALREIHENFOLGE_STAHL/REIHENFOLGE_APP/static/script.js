// First Load of the WebSide
var firstTime = localStorage.getItem("first_time");
if (!firstTime) {
  // first time loaded!
  localStorage.setItem("first_time", "1");
  localStorage.setItem("Breite", "10");
  localStorage.setItem("Dicke", "10");
  localStorage.setItem("buttonText", "Zeige besten Pfad");
} else {
  location.href =
    "http://127.0.0.1:8000/display_graph/" + tol_breite + "/" + tol_dicke;
}

function updateToleranz() {
  var tol_dicke = document.getElementById("input_dicke");
  var tol_breite = document.getElementById("input_breite");
  //if((typeof(tol_dicke) != 'undefined' && tol_dicke != null && tol_dicke != "") || (typeof(tol_breite) != 'undefined' && tol_breite != null && tol_breite != "")){
  if (
    tol_dicke != null &&
    tol_dicke.value != "" &&
    tol_breite != null &&
    tol_breite.value != ""
  ) {
    localStorage.setItem("Breite", tol_breite.value);
    localStorage.setItem("Dicke", tol_dicke.value);
    location.href =
      "http://127.0.0.1:8000/display_graph/" +
      tol_breite.value +
      "/" +
      tol_dicke.value;
  } else {
    localStorage.setItem("Breite", 0);
    localStorage.setItem("Dicke", 0);
    location.href = "http://127.0.0.1:8000/display_graph/0/0";
  }
}
function showPath() {
  var currentText = document.getElementById("show_path").value;
  var newText = " ";
  var tolBreite = localStorage.getItem("Breite");
  var tolDicke = localStorage.getItem("Dicke");

  // Change Button Text
  if (currentText == "Zeige besten Pfad") {
    //path = "/bestpath";
    newText = "Zeige alle Pfade";
    localStorage.setItem("buttonText", newText);
    //document.getElementById("show_path").value = newText;
    //location.href = "http://127.0.0.1:8000/display_graph/" + tolBreite + "/" + tolDicke + "/bestpath";
    location.href =
      "http://127.0.0.1:8000/display_graph/" + tolBreite + "/" + tolDicke;
  } else if (currentText == "Zeige alle Pfade") {
    path = "";
    newText = "Zeige besten Pfad";
    //document.getElementById("show_path").value = newText;
    localStorage.setItem("buttonText", newText);
    location.href =
      "http://127.0.0.1:8000/display_graph/" + tolBreite + "/" + tolDicke;
  }
}

function onChangeAxisButtonClick() {
  var coils = coils
  var xAchse_Name = "Breite";
      var yAchse_Name = "Dicke";

}
