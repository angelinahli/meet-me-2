$(function() {
  $("#startdate").datetimepicker({
    format: "L"
  });
});
$(function() {
  $("#enddate").datetimepicker({
    format: "L",
    useCurrent: false
  });
});

$(function() {
  $("#starttime").datetimepicker({
    format: "LT"
  });
});
$(function() {
  $("#endtime").datetimepicker({
    format: "LT"
  });
});

$("#startdate").on("change.datetimepicker",
  function (e) {
    $("#enddate").datetimepicker("minDate", e.date);
  }
);
$("#enddate").on("change.datetimepicker",
  function (e) {
    $("#startdate").datetimepicker("maxDate", e.date);
  }
);