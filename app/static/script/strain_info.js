//get parameters from template
var script_tag = document.getElementById('strainInfo');
var csrf_token = script_tag.getAttribute("csrf-token");
var selected_id = script_tag.getAttribute("selected-id");
var redirect_url = script_tag.getAttribute("redirect-url");

//configure ajax for csrf protection
 $.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});		

//mark current closest ancestor	
$(document).ready(function(){
	var textId ="#"+ selected_id;
	var textX=$(textId).attr("x");
	var textY=$(textId).attr("y");
	var textWidth=$(textId)[0].getBBox().width;
	var textHeight=$(textId)[0].getBBox().height;
	$("#rect4895").attr("x", String(textX-4));
	$("#rect4895").attr("y", String(textY-12));
	$("#rect4895").attr("width", String(textWidth+8));
	$("#rect4895").attr("height", String(textHeight+4));
});

//open tab with new strain on click
$(document).on("click", ".svg", function(event){
	var clickedStrain = $("#"+event.target.id).text();
	$.ajax({
		url: redirect_url,
		dataType: "json",
		type: "post",
		contentType: "application/json",
		data: JSON.stringify({"strain": clickedStrain})
	}).done(function(response){
		if (response["url"]!=false){
			window.open(response["url"], "_blank")
		};
	});
});