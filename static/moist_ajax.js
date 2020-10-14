function refreshData() {
  //alert("Calling refresh...");
  $.ajax({
    url: "/moist",
    type: "GET",
    dataType: "json",
    success: function(data) {
      //alert("Refresh called. Result="+data.result);
      $("#Moist").html(data.moist);

      setTimeout(refreshData, 1000);
    },
    error: function(xhr, status, err) {
      alert("Error: " + err);
    }
  });
}

$("#refresh").ready(function() {
    refreshData();
  });
