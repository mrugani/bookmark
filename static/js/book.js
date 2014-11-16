
function test(){

	alert("test");
}

function delete_link(id){

	r=confirm('Are you sure you want to delete this link?');
	if(r==true) {

		url = "delete?id="+id;
		ajax(url, [], null)
		el=document.getElementById(id);
		el.parentNode.removeChild(el);
	}
}

function update_link(id){

	/*var form = "<form method='post' action=addlink>\n";
	form += "<input type='hidden' name='" + "link" + "' value='" +id + "'></input>\n";
	form += "</form>"*/
	//alert(form);	
	var form = document.createElement("form");
	form.setAttribute("method", "post");
	form.setAttribute("action", "addlink");
	var field = document.createElement("input"); 
	field.setAttribute("type", "hidden");
	field.setAttribute("name", "id");
	field.setAttribute("value", id);
	form.appendChild(field);
	document.body.appendChild(form);
	form.submit();
}