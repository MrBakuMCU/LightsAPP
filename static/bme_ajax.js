function refreshData() {
    //alert("Calling refresh...");
    $.ajax({
        url: "/myBME",
        type: "GET",
        dataType: "json",
        success: function (data) {
            //alert("Refresh called. Result="+data.result);
            $("#sysTemp").html(data.temp);
            $("#sysHum").html(data.hum);
            $("#sysPSI").html(data.psi);
            setTimeout(refreshData, 1000);
        },
        error: function (xhr, status, err) {
            alert("Error: " + err);
        }
    });
}

$("#refresh").ready(function () {
    refreshData();
});
