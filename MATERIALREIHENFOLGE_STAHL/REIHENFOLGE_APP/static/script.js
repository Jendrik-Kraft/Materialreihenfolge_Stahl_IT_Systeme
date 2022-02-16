// First Load of the WebSide
var firstTime = localStorage.getItem("first_time");

if (!firstTime) {
  // first time loaded!
  localStorage.setItem("first_time", "1");
  localStorage.setItem("Breite", "1");
  localStorage.setItem("Dicke", "1");
  localStorage.setItem("buttonText", "Zeige besten Pfad");
  localStorage.setItem("DummyText", "Zeige Dummycoils an");
  localStorage.setItem("tauschen", 0);
} else if (firstTime == 1) {
  var tol_breite = localStorage.getItem("Breite");
  var tol_dicke = localStorage.getItem("Dicke");
  reload();
  localStorage.setItem("first_time", "2");
} else if (firstTime == 2) {
  localStorage.setItem("first_time", "1");
}

function reload() {
  var tol_breite = localStorage.getItem("Breite");
  var tol_dicke = localStorage.getItem("Dicke");
  if (localStorage.getItem("buttonText") == "Zeige alle Pfade") {
    location.href =
      "http://127.0.0.1:8000/display_graph/" +
      tol_breite +
      "/" +
      tol_dicke +
      "/best_path";
  } else {
    location.href =
      "http://127.0.0.1:8000/display_graph/" + tol_breite + "/" + tol_dicke;
  }
}

function updateToleranz() {
  var tol_dicke = document.getElementById("input_dicke");
  var tol_breite = document.getElementById("input_breite");
  //if((typeof(tol_dicke) != 'undefined' && tol_dicke != null && tol_dicke != "") || (typeof(tol_breite) != 'undefined' && tol_breite != null && tol_breite != "")){

  if ( tol_dicke != null && tol_dicke.value != "" && tol_breite != null && tol_breite.value != "" ) {
    localStorage.setItem("Breite", tol_breite.value);
    localStorage.setItem("Dicke", tol_dicke.value);
    
    if (localStorage.getItem("buttonText") == "Zeige alle Pfade"){
      location.href = "http://127.0.0.1:8000/display_graph/" + tol_breite.value + "/" + tol_dicke.value + "/best_path";
    }    
    else {    
      location.href = "http://127.0.0.1:8000/display_graph/" + tol_breite.value + "/" + tol_dicke.value;
    }
  } 
  else {
    localStorage.setItem("Breite", 0);
    localStorage.setItem("Dicke", 0);
    tol_dicke.setCustomValidity("");
    tol_breite.setCustomValidity("");
    if(tol_dicke.value == ""){
      tol_dicke.setCustomValidity("Invalid field.");
    }
    if(tol_breite.value == ""){
      tol_breite.setCustomValidity("Invalid field.");
    }
  }
}
function showPath() {
  var currentText = document.getElementById("show_path").value;
  var newText = " ";
  // Change Button Text
  if (currentText == "Zeige besten Pfad") {
    //path = "/bestpath";
    newText = "Zeige alle Pfade";
    localStorage.setItem("buttonText", newText);
    //document.getElementById("show_path").value = newText;
    //location.href = "http://127.0.0.1:8000/display_graph/" + tolBreite + "/" + tolDicke + "/bestpath";
    reload();
  } else if (currentText == "Zeige alle Pfade") {
    path = "";
    newText = "Zeige besten Pfad";
    //document.getElementById("show_path").value = newText;
    localStorage.setItem("buttonText", newText);
    reload();
  }
}

function onChangeAxisButtonClick() {
  var tauschen = localStorage.getItem("tauschen");
  if (tauschen == 0) {
    localStorage.setItem("tauschen", 1);
  } else {
    localStorage.setItem("tauschen", 0);
  }
  reload();
}

function showDummys() {
  var currentText = document.getElementById("show_dummys").value;
  var newText = "";
  if (currentText == "Zeige Dummycoils an") {
    newText = "Blende Dummycoils aus";
    localStorage.setItem("DummyText", newText);
  } else {
    newText = "Zeige Dummycoils an";
    localStorage.setItem("DummyText", newText);
  }
  reload();
}

function onChangeToEditPageButtonClick() {
  location.href = "http://127.0.0.1:8000/edit_database/test";
}
