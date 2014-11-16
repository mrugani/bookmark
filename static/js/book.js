
function test(){

	alert("test");
}

function delete_link(id){

	r=confirm('Are you sure you want to delete this link?');
	if(r==true) {
		ajax("{{=URL('default', 'delete', vars={'id':id})}}", [], null);
		el=document.getElementById(id);
		el.parentNode.removeChild(el);
	}
}