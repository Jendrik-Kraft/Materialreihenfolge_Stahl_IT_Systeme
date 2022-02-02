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

// Get Toleranzes and Store in LocalStorage
function updateToleranz() {
  var tol_dicke = document.getElementById("input_dicke").value;
  var tol_breite = document.getElementById("input_breite").value;
  if((typeof(tol_dicke) != 'undefined' && tol_dicke != null) || (typeof(tol_breite) != 'undefined' && tol_breite != null)){
    localStorage.setItem("Breite", tol_breite);
    localStorage.setItem("Dicke", tol_dicke);
    location.href =
    "http://127.0.0.1:8000/display_graph/" + tol_breite + "/" + tol_dicke;
  }
  else {
    localStorage.setItem("Breite", 0);
    localStorage.setItem("Dicke", 0);
    location.href =
    "http://127.0.0.1:8000/display_graph/0/0";
  }
}

function showPath() {
  var currentText = document.getElementById("show_path").value;
  var newText = " ";
  var tolBreite = localStorage.getItem("Breite");
  var tolDicke = localStorage.getItem("Dicke");
   
  // Change Button Text
  if(currentText == "Zeige besten Pfad"){
    //path = "/bestpath";
    newText = "Zeige alle Pfade";
    localStorage.setItem("buttonText", newText);
    //document.getElementById("show_path").value = newText;
    //location.href = "http://127.0.0.1:8000/display_graph/" + tolBreite + "/" + tolDicke + "/bestpath";
    location.href = "http://127.0.0.1:8000/display_graph/" + tolBreite + "/" + tolDicke;
  }
  else if(currentText == "Zeige alle Pfade"){
    path = "";
    newText = "Zeige besten Pfad";
    //document.getElementById("show_path").value = newText;
    localStorage.setItem("buttonText", newText);
    location.href = "http://127.0.0.1:8000/display_graph/" + tolBreite + "/" + tolDicke;
  }
  
}

function onChangeAxisButtonClick() {
  var coils = coils
  var xAchse_Name = "Breite";
      var yAchse_Name = "Dicke";

}
