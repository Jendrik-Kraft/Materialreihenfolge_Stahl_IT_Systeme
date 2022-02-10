// First Load of the WebSide

function onChangeToMainPageButtonClick() {
    location.href =
    "http://127.0.0.1:8000/display_graph/10/10";
}

function onSaveChangesButtonClick() {
    var coilsTableData = document.querySelector("tbody.coilsTable-Body");
    var tableId = document.getElementById('coilsTable');
    var tBody = tableId.getElementsByTagName('tbody')[0];
    var tableRow = tBody.getElementsByTagName('tr');
}

function buildTable() {
      var coilDiv = document.querySelector("div.coilTable"); // Find the scoreboard div in our html
      //scoreDiv.style.background = "green";
      var tableHeaders = ["ID","Width", "Height"];
      const createCoilTable = () =>
      {
          while (coilDiv.firstChild){ coilDiv.removeChild(coilDiv.firstChild); }// Remove all children from scoreboard div (if any)
          let coilsTable = document.createElement('table'); // Create the table itself
          coilsTable.className = 'coilsTable';
          let coilsTableHead = document.createElement('thead') ;// Creates the table header group element
          coilsTableHead.className = 'coilsTableHead';
          let coilsTableHeaderRow = document.createElement('tr');// Creates the row that will contain the headers
          coilsTableHeaderRow.className = 'coilsTableHeaderRow';
          // Will iterate over all the strings in the tableHeader array and will append the header cells to the table header row
          tableHeaders.forEach(header => {
              let coilsHeader = document.createElement('th'); // Creates the current header cell during a specific iteration
              coilsHeader.innerText = header;
              coilsTableHeaderRow.append(coilsHeader); // Appends the current header cell to the header row
              })
          coilsTableHead.append(coilsTableHeaderRow); // Appends the header row to the table header group element
          coilsTable.append(coilsTableHead);
          let coilsTableBody = document.createElement('tbody');// Creates the table body group element
          coilsTableBody.className = "coilsTable-Body";
          coilsTable.append(coilsTableBody); // Appends the table body group element to the table
          coilDiv.append(coilsTable); // Appends the table to the scoreboard div
      }

      const appendCoils = (coil) => {
          const coilsTable = document.querySelector('.coilsTable'); // Find the table we created
          let coilsTableBodyRow = document.createElement('tr'); // Create the current table row
          coilsTableBodyRow.className = 'coilsTableBodyRow';
          // Lines 72-85 create the 5 column cells that will be appended to the current table row
          let coilID = document.createElement('td');
          coilID.innerText = coil[0];
          let coilWidth = document.createElement('td');
          coilWidth.innerText = coil[2];
          let coilHight = document.createElement('td');
          coilHight.innerText = coil[1];
          coilsTableBodyRow.append(coilID, coilWidth, coilHight);// Append all 5 cells to the table row
          coilsTable.append(coilsTableBodyRow);// Append the current row to the scoreboard table body
          }
      //var coils = {{ coils|safe }} ;
      //var coils=coils;
      createCoilTable();// Clears scoreboard div if it has any children nodes, creates & appends the table
      coilDiv.setAttribute("contenteditable", true);
      var coilsTableHead = document.querySelector("thead.coilsTableHead");
      coilsTableHead.setAttribute("contenteditable", false);
      // Iterates through all the objects in the scores array and appends each one to the table body

      for (const coil of coils) {
          var coilIndex = coils.indexOf(coil) + 1;// Index of score in score array for global ranking (these are already sorted in the back-end)
          appendCoils(coil); // Creates and appends each row to the table body
          }

}