function test1(){

	alert("test");
}

function add_to_my_link(id){

	var form = document.createElement("form");
	form.setAttribute("method", "post");
	form.setAttribute("action", "addlink");
	var field = document.createElement("input"); 
	field.setAttribute("type", "hidden");
	field.setAttribute("name", "follow_lid");
	field.setAttribute("value", id);
	form.appendChild(field);
	document.body.appendChild(form);
	form.submit();

}