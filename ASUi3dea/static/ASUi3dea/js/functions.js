
//save new inverter name when exit editing of Name text
$("#invert_name").focusout(function() {
    console.log($(this).text())

     $.ajax({
        type: "POST",
        url: "http://127.0.0.1:8000/ASUi3dea/" + inverter + "/change_invert_name/",
        dataType: "json",
        data: {
          inverter: inverter,
          newName: $(this).text(),
          csrfmiddlewaretoken: csrfToken
        },
        success: function (data) {
          //Do nothing
        },
        error: function () {
         alert("Inverter not found");
        }
    });
});


$("#update-button").click(function() {
  console.log("updating database...")

  addUpdateLoader()

  $.ajax({
     type: "GET",
     url: "http://127.0.0.1:8000/ASUi3dea/" + inverter + "/update/",
     dataType: "json",
     data: {
       csrfmiddlewaretoken: csrfToken
     },
     success: function (data) {
       drawAllGraphs()
       removeUpdateLoader()
     },
     error: function (data) {
      alert(data["responseText"])
      removeUpdateLoader()
     }
 });
});


function addUpdateLoader() {

  $("#options-content").append('<div id="update-loader" class="loader"></div>')
}


function removeUpdateLoader(){

  $("#options-content").find("#update-loader").remove()
}
