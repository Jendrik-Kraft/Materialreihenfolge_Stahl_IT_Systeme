// First Load of the WebSide

function onChangeToMainPageButtonClick() {
    location.href =
    "http://127.0.0.1:8000/display_graph/10/10";
}

function buildTable() {
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
          coilID.innerText = coil[0];
          let coilWidth = document.createElement('td');
          coilWidth.innerText = coil[2];
          let coilHight = document.createElement('td');
          coilHight.innerText = coil[1];
          scoreboardTableBodyRow.append(coilID, coilWidth, coilHight);// Append all 5 cells to the table row
          scoreboardTable.append(scoreboardTableBodyRow);// Append the current row to the scoreboard table body
          }
      //var coils = {{ coils|safe }} ;
      //var coils=coils;
      createScoreboardTable();// Clears scoreboard div if it has any children nodes, creates & appends the table
      // Iterates through all the objects in the scores array and appends each one to the table body

      for (const coil of coils) {
          var coilIndex = coils.indexOf(coil) + 1;// Index of score in score array for global ranking (these are already sorted in the back-end)
          appendScores(coil); // Creates and appends each row to the table body
          }

}