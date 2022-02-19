// First Load of the WebSide

function onChangeToMainPageButtonClick() {
    location.href =
    "http://127.0.0.1:8000/display_graph/10/10";
}

function onAddButtonClick(){
          var new_dicke = document.getElementById("input_dicke").value;
          var new_breite = document.getElementById("input_breite").value;
          location.href = "http://127.0.0.1:8000/edit_database/test/" + new_breite + "/" + new_dicke;
}

function onDeleteButtonClick() {
    var delete_id = document.getElementById("input_ID").value;
    location.href = "http://127.0.0.1:8000/edit_database/test/" + delete_id;
}
function buildTable() {
      var coilDiv = document.querySelector("div.coilTable");
      var tableHeaders = ["ID","Breite", "Dicke"];
      const createCoilTable = () =>
      {
          while (coilDiv.firstChild){ coilDiv.removeChild(coilDiv.firstChild); }
          var coilsTable = document.createElement('table');
          coilsTable.className = 'coilsTable';
          let coilsTableHead = document.createElement('thead') ;
          coilsTableHead.className = 'coilsTableHead';
          let coilsTableHeaderRow = document.createElement('tr');
          coilsTableHeaderRow.className = 'coilsTableHeaderRow';

          tableHeaders.forEach(header => {
              let coilsHeader = document.createElement('th');
              coilsHeader.innerText = header;
              coilsTableHeaderRow.append(coilsHeader);
              })
          coilsTableHead.append(coilsTableHeaderRow);
          coilsTable.append(coilsTableHead);
          let coilsTableBody = document.createElement('tbody');
          coilsTableBody.className = "coilsTableBody";
          coilsTable.append(coilsTableBody);
          coilDiv.append(coilsTable);
      }

      const appendCoils = (coil) => {
          const coilsTable = document.querySelector('.coilsTable');
          let coilsTableBodyRow = document.createElement('tr');
          coilsTableBodyRow.className = 'coilsTableBodyRow';
          let coilID = document.createElement('td');
          coilID.innerText = coil[0];
          let coilWidth = document.createElement('td');
          coilWidth.innerText = coil[2];
          let coilHight = document.createElement('td');
          coilHight.innerText = coil[1];
          coilsTableBodyRow.append(coilID, coilWidth, coilHight);
          coilsTable.append(coilsTableBodyRow);
          }
      createCoilTable();
      for (const coil of coils) {
          var coilIndex = coils.indexOf(coil) + 1;
          appendCoils(coil);
          }

}