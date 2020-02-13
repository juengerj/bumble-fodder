


// function addSubreddit() {
    // gotSubreddit = document.getElementById("getSubreddit").value;
    // console.log(gotSubreddit);
// }

// function deleteSubreddit() {
    
// }

// function submitGet() {
    // var req = new XMLHttpRequest();
	// req.open("GET", "http://flip3.engr.oregonstate.edu:4799/", true);

	// req.addEventListener('load',function(){
		// if(req.status >= 200 && req.status < 400){
				// var getResponse = JSON.parse(req.responseText);
				// if (getResponse.length > 0) {
					// initiateTable();
					// updateTable(getResponse);
					// hasTable = 1;
				// }
		// } else {
			// console.log("Error in network request: " + req.statusText);
		// }
	// });

	// req.send(null);
	// event.preventDefault();
// }

function removeElement(id) {
    getObject = document.getElementById(id);
    getObject.parentNode.removeChild(getObject);
}

