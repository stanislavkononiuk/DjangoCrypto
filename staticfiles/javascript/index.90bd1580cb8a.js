$(document).ready(function () {
  $("#myTable").DataTable({
    columnDefs: [{ type: "natural", targets: "_all" }],
    order: [[3, "desc"]],
  });
});
