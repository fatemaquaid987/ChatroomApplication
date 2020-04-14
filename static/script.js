
var timeoutID;
var timeout = 1000;


function setup() {
	document.getElementById("postButton").addEventListener("click", makePost, true);

	timeoutID = window.setTimeout(poller, timeout);
}

function makePost() {

    
    if(document.getElementById("messageText").value != '')
	{var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	
	var message = document.getElementById("messageText").value;
	var user = "{{user_name}}";
	
	var row = [message, user];
	httpRequest.onreadystatechange = function() { handlePost(httpRequest, row) };
	
	httpRequest.open("POST", "/new_message");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');

	var data;
	var id = {{chatroom.chatroom_id|safe}};
	data = "message=" + message + "&chatroom="+ id.toString();
	httpRequest.send(data);}
}

function handlePost(httpRequest, row) {
	//alert("handling");
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		//alert(httpRequest.status);
		if (httpRequest.status === 200) {
			
			//alert("done")
			addMessage(row);
			clearInput();
			
		} else {
			
			alert("This Chatroom has been deleted! Kindly press back button to go to your profile and select a new chatroom");
			window.location.replace("/profile/{{user_name}}");
		}
	}
	/*else
	{
		alert(httpRequest.readyState);
	}*/
}

function poller() {
	var httpRequest = new XMLHttpRequest();

	if (!httpRequest) {
		alert('Giving up :( Cannot create an XMLHTTP instance');
		return false;
	}

	httpRequest.onreadystatechange = function() { handlePoll(httpRequest) };
	httpRequest.open("POST", "/items");
	httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
	var data;
	var id = {{chatroom.chatroom_id|safe}};
	data = "chatroom="+ id.toString();
	httpRequest.send(data);
}

function handlePoll(httpRequest) {
	if (httpRequest.readyState === XMLHttpRequest.DONE) {
		if (httpRequest.status === 200) {
			var tab = document.getElementById("messageBoard");
			tab.innerHTML ="";
			var rows = JSON.parse(httpRequest.responseText);
			if(rows)
			{for (var i = 0; i < rows.length; i++) {
				addMessage(rows[i]);
			}}
			
			timeoutID = window.setTimeout(poller, timeout);
			
		} else {
			alert("There was a problem with the poll request.  you'll need to refresh the page to recieve updates again!");
			
		}
	}
}

function clearInput() {

	document.getElementById("messageText").value = "";
}

function addMessage(row) {
	var messageBoard = document.getElementById("messageBoard");
	var newRow   = messageBoard.insertRow();
	var newCell1, newText1, newCell2, newText2;
    if (row[1] == "{{user_name}}")
    {
        newCell1  = newRow.insertCell();
        newCell1.setAttribute("id", "my_message", 0);
		newText1  = document.createTextNode(row[0]);
		newCell1.appendChild(newText1);

		newCell2  = newRow.insertCell();
		newCell2.setAttribute("id", "username", 0);
		newText2  = document.createTextNode(row[1]);
		newCell2.appendChild(newText2);

    }
    else
    {

	    newCell1  = newRow.insertCell();
		newText1  = document.createTextNode(row[0]);
		newCell1.appendChild(newText1);

		newCell2  = newRow.insertCell();
		newCell2.setAttribute("id", "username", 0);
		newText2  = document.createTextNode(row[1]);
		newCell2.appendChild(newText2);
    }
	
	
	
}

window.addEventListener("load", setup, true);

