//get parameters from template
var script_tag = document.getElementById('mediumInfo');
var csrf_token = script_tag.getAttribute("csrf-token");

//define function ro replace URL parameter
var replaceUrlParam = function(url, paramName, paramValue){
    if (paramValue == null) {
        paramValue = '';
    }
    var pattern = new RegExp('\\b('+paramName+'=).*?(&|#|$)');
    if (url.search(pattern)>=0) {
        return url.replace(pattern,'$1' + paramValue + '$2');
    }
    url = url.replace(/[?#]$/,'');
    return url + (url.indexOf('?')>0 ? '&' : '?') + paramName + '=' + paramValue;
};

//configure ajax for csrf protection
var csrf_token = csrf_token;
 $.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});	

$('#medium_composition').DataTable({				
	dom: "rt<'bottom'><'row'<'col-sm-6'B><'col-sm-6'>>",
	buttons: [
		{
            extend: 'csv',
            text: "<span class='glyphicon glyphicon-download-alt'></span>"
        }],
});

//react to selected compound		
$('#compound').change(function(){
	var URLparameter = window.location.href.split("#")[0];
	var optionSelected = $("option:selected", this);
		var valueSelected = this.value;
		var newURL = replaceUrlParam(URLparameter, "compound", valueSelected)+"#medium_plot"
		window.location.href = newURL;   			
});