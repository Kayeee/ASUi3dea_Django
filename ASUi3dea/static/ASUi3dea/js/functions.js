
//save new inverter name when exit editing of Name text
$("#invert_name").focusout(function() {
    console.log($(this).text())

     $.ajax({
        type: "POST",
        url: "http://52.87.223.187:8000/ASUi3dea/" + inverter + "/change_invert_name/",
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
     url: "http://52.87.223.187:8000/ASUi3dea/" + inverter + "/update/",
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



//multi selector
(function() {
"use strict";

var supportsMultiple = self.HTMLInputElement && "valueLow" in HTMLInputElement.prototype;

var descriptor = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value");

self.multirange = function(input) {
	if (supportsMultiple || input.classList.contains("multirange")) {
		return;
	}

	var values = input.getAttribute("value").split(",");
	var min = +input.min || 0;
	var max = +input.max || 100;
	var ghost = input.cloneNode();

	input.classList.add("multirange", "original");
	ghost.classList.add("multirange", "ghost");

	input.value = values[0] || min + (max - min) / 2;
	ghost.value = values[1] || min + (max - min) / 2;

	input.parentNode.insertBefore(ghost, input.nextSibling);

	Object.defineProperty(input, "originalValue", descriptor.get ? descriptor : {
		// Fuck you Safari >:(
		get: function() { return this.value; },
		set: function(v) { this.value = v; }
	});

	Object.defineProperties(input, {
		valueLow: {
			get: function() { return Math.min(this.originalValue, ghost.value); },
			set: function(v) { this.originalValue = v; },
			enumerable: true
		},
		valueHigh: {
			get: function() { return Math.max(this.originalValue, ghost.value); },
			set: function(v) { ghost.value = v; },
			enumerable: true
		}
	});

	if (descriptor.get) {
		// Again, fuck you Safari
		Object.defineProperty(input, "value", {
			get: function() { return this.valueLow + "," + this.valueHigh; },
			set: function(v) {
				var values = v.split(",");
				this.valueLow = values[0];
				this.valueHigh = values[1];
			},
			enumerable: true
		});
	}

	function update() {
		ghost.style.setProperty("--low", 100 * ((input.valueLow - min) / (max - min)) + 1 + "%");
		ghost.style.setProperty("--high", 100 * ((input.valueHigh - min) / (max - min)) - 1 + "%");
	}

	input.addEventListener("input", update);
	ghost.addEventListener("input", update);

	update();
}

multirange.init = function() {
	Array.from(document.querySelectorAll("input[type=range][multiple]:not(.multirange)")).forEach(multirange);
}

if (document.readyState == "loading") {
	document.addEventListener("DOMContentLoaded", multirange.init);
}
else {
	multirange.init();
}

})();
