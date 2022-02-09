// First Load of the WebSide
var firstTime = localStorage.getItem("first_time");

if (!firstTime) {
  // first time loaded!
  localStorage.setItem("first_time", "1");
  localStorage.setItem("Breite", "0");
  localStorage.setItem("Dicke", "0");
  localStorage.setItem("buttonText", "Zeige besten Pfad");
  localStorage.setItem("tauschen", 0);
} else if (firstTime == 1) {
  var tol_breite = localStorage.getItem("Breite");
  var tol_dicke = localStorage.getItem("Dicke");
  location.href =
    "http://127.0.0.1:8000/display_graph/" + tol_breite + "/" + tol_dicke;
  localStorage.setItem("first_time", "2");
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
    tol_dicke.setCustomValidity("");
    tol_breite.setCustomValidity("");
    if (tol_dicke.value == "") {
      tol_dicke.setCustomValidity("Invalid field.");
    }
    if (tol_breite.value == "") {
      tol_breite.setCustomValidity("Invalid field.");
    }
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
      "http://127.0.0.1:8000/display_graph/" +
      tolBreite +
      "/" +
      tolDicke +
      "/best_path";
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
  var tauschen = localStorage.getItem("tauschen");
  if (tauschen == 0) {
    localStorage.setItem("tauschen", 1);
  } else {
    localStorage.setItem("tauschen", 0);
  }
  location.href =
    "http://127.0.0.1:8000/display_graph/" +
    localStorage.getItem("Breite") +
    "/" +
    localStorage.getItem("Dicke");
}


function onChangeToMainPageButtonClick() {
    location.href =
    "http://127.0.0.1:8000/display_graph/10/10";
}

function onChangeToEditPageButtonClick() {
    location.href =
    "http://127.0.0.1:8000/edit_database/test";
}

function onTestButtonClick() {
      var scoreDiv = document.querySelector("div.scoreboard"); // Find the scoreboard div in our html
      //scoreDiv.style.background = "green";
      var tableHeaders = ["ID","Width", "Height"];
      const createScoreboardTable = () =>
      {
          while (scoreDiv.firstChild){ scoreDiv.removeChild(scoreDiv.firstChild); }// Remove all children from scoreboard div (if any)
          let scoreboardTable = document.createElement('table'); // Create the table itself
          scoreboardTable.className = 'scoreboardTable';
          let scoreboardTableHead = document.createElement('thead') ;// Creates the table header group element
          scoreboardTableHead.className = 'scoreboardTableHead';
          let scoreboardTableHeaderRow = document.createElement('tr');// Creates the row that will contain the headers
          scoreboardTableHeaderRow.className = 'scoreboardTableHeaderRow';
          // Will iterate over all the strings in the tableHeader array and will append the header cells to the table header row
          tableHeaders.forEach(header => {
              let scoreHeader = document.createElement('th'); // Creates the current header cell during a specific iteration
              scoreHeader.innerText = header;
              scoreboardTableHeaderRow.append(scoreHeader); // Appends the current header cell to the header row
              })
          scoreboardTableHead.append(scoreboardTableHeaderRow); // Appends the header row to the table header group element
          scoreboardTable.append(scoreboardTableHead);
          let scoreboardTableBody = document.createElement('tbody');// Creates the table body group element
          scoreboardTableBody.className = "scoreboardTable-Body";
          scoreboardTable.append(scoreboardTableBody); // Appends the table body group element to the table
          scoreDiv.append(scoreboardTable); // Appends the table to the scoreboard div
      }

      const appendScores = (coil) => {
          const scoreboardTable = document.querySelector('.scoreboardTable'); // Find the table we created
          let scoreboardTableBodyRow = document.createElement('tr'); // Create the current table row
          scoreboardTableBodyRow.className = 'scoreboardTableBodyRow';
          // Lines 72-85 create the 5 column cells that will be appended to the current table row
          let coilID = document.createElement('td');
          coilID.innerText = coilIndex;
          let coilWidth = document.createElement('td');
          coilWidth.innerText = JSON.stringify(coil);
          let coilHight = document.createElement('td');
          coilHight.innerText = JSON.stringify(coil);
          scoreboardTableBodyRow.append(coilID, coilWidth, coilHight);// Append all 5 cells to the table row
          scoreboardTable.append(scoreboardTableBodyRow);// Append the current row to the scoreboard table body
          }
      //var coils = {{ coils|safe }} ;
      //var coils=coils;
      createScoreboardTable() ;// Clears scoreboard div if it has any children nodes, creates & appends the table
      // Iterates through all the objects in the scores array and appends each one to the table body

      for (const coil of coils) {
          var coilIndex = coils.indexOf(coil) + 1;// Index of score in score array for global ranking (these are already sorted in the back-end)
          appendScores(coil); // Creates and appends each row to the table body
          }

}