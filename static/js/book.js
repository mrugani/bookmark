
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

function follow(id1, id2){

	url = "follow?id1="+id1+"&id2="+id2;
	ajax(url, [], null)
	el = document.getElementById(id2);
	el.innerHTML = "UNFOLLOW"
	el.className = "btn btn-warning btn-sm"
	el.onclick = function () { unfollow(id1, id2) };
}

function unfollow(id1, id2){

	url = "unfollow?id1="+id1+"&id2="+id2;
	ajax(url, [], null)
	el = document.getElementById(id2);
	//alert(el.class)
	el.innerHTML = "FOLLOW"
	el.className = "btn btn-success btn-sm"
	el.onclick = function () { follow(id1, id2) };
}