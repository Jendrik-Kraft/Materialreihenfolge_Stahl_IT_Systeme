// First Load of the WebSide

function onChangeToMainPageButtonClick() {
    location.href =
    "http://127.0.0.1:8000/display_graph/10/10";
}

function onAddButtonClick(){
          var new_dicke = document.getElementById("input_dicke").value;
          var new_breite = document.getElementById("input_breite").value;
          const coilsTable = document.querySelector('.coilsTable'); // Find the table we created
          let coilsTableBodyRow = document.createElement('tr'); // Create the current table row
          coilsTableBodyRow.className = 'coilsTableBodyRow';
          // Lines 72-85 create the 3 column cells that will be appended to the current table row
          let coilID = document.createElement('td');
          coilID.innerText = coilsTable.rows.length;
          let coilWidth = document.createElement('td');
          coilWidth.innerText = new_breite;
          let coilHight = document.createElement('td');
          coilHight.innerText = new_dicke;
          coilsTableBodyRow.append(coilID, coilWidth, coilHight);// Append all 5 cells to the table row
          coilsTable.append(coilsTableBodyRow);// Append the current row to the scoreboard table body
}

function onSaveChangesButtonClick() {
    //var coilsTableData = document.querySelector("tbody.coilsTable-Body");
    //var tableId = document.getElementById('coilsTable').value;
    //var tBody = tableId.getElementsByTagName('tbody')[0];
    //var tableRow = [1,2,4,5];//tBody.getElementsByTagName('tr');
    //coils_list = document.getElementById('coilsTable').values.tolist();
    var coilDiv = document.querySelector(".coilsTable");
    //var tableRow = tBody.getElementsByTagName('tr');
    let test =coilDiv.innerHTML;
    test = test.replace(/td/g, '');
    test = test.replace(/class="coilsTableBodyRow"/g,'');
    test = test.replace(/thead class="coilsTableHead" contenteditable="false"/g,'');
    test = test.replace(/class="coilsTableHeaderRow"/g, '');
    test = test.replace(/class="coilsTableBody"/g, '');
    test = test.replace(/</g, '');
    test = test.replace(/>/g, '');
    test = test.replace(/tr/g, '');
    test = test.replace(/thID/g, '');
    test = test.replace(/ththWidth/g, '');
    test = test.replace(/ththHeight/g, '');
    test = test.replace(/theadtbody /g, '');
    test = test.replace(/tbody /g, '');
    test = test.replace(/th/g, '');
    test = test.replace(/\s+/g, '');
    test = test.replace(/\//g, ',');
    test = test.replace(/,,/g, ';');
    test = test.replace(/;;/g, '');
    //test.append('"');
    let tableTest = String(test);



    //array1.forEach(element => console.print(element));
    //console.log('1');
    //coils_list.forEach(element => console.log(element));
    //list_for_js = [];
    //for coil in coils_list:
        //list_for_js.append({"x": coil[1], "y": coil[2]});
    //list_for_js = json.dumps(list_for_js);
    //var tableJS = json.dumps(tableRow);
    location.href = "http://127.0.0.1:8000/edit_database/test/" + tableTest;
}

function buildTable() {
      var coilDiv = document.querySelector("div.coilTable"); // Find the scoreboard div in our html
      //scoreDiv.style.background = "green";
      var tableHeaders = ["ID","Breite", "Dicke"];
      const createCoilTable = () =>
      {
          while (coilDiv.firstChild){ coilDiv.removeChild(coilDiv.firstChild); }// Remove all children from scoreboard div (if any)
          var coilsTable = document.createElement('table'); // Create the table itself
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
          coilsTableBody.className = "coilsTableBody";
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
      // Iterates through all the objects in the scores array and appends each one to the table body
      for (const coil of coils) {
          var coilIndex = coils.indexOf(coil) + 1;// Index of score in score array for global ranking (these are already sorted in the back-end)
          appendCoils(coil); // Creates and appends each row to the table body
          }

}