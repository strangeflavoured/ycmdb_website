//get parameters from template
var script_tag = document.getElementById('renderSubmit');
var csrf_token = script_tag.getAttribute("csrf-token");
var checkTime = script_tag.getAttribute("check-time");
var fillSubmit = script_tag.getAttribute("auto-fill");
var uploadTemplate = script_tag.getAttribute("upload-template");
var downloadCurrent = script_tag.getAttribute("download-current");
var processSubmission = script_tag.getAttribute("process-files");

//configure ajax for csrf protection
$.ajaxSetup({
	beforeSend: function(xhr, settings) {
		if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrf_token);
		}
	}
});

//custom file input workaround
$('#uploadData').change(function() {
	var file = $(this).val().replace("C:\\fakepath\\", "");
	$('#pretty-input').val(file);
});

//custom file input workaround
$('#reloadCurrent').change(function() {
	var file = $(this).val().replace("C:\\fakepath\\", "");
	$('#pretty-input-2').val(file);
});

//make medium composition table
var table = $('#medium_composition').DataTable({
	dom: "rtB",
	select: true,
	buttons: [{
        text: 'Delete selected rows',
        attr: {
        	id: 'deleteRow',
        	class: "btn btn-default"
        }
    }]
});

// react to selection of strain
$('#StrainSelected').change(function(){
	var optionSelected = $("option:selected", this);
		var valueSelected = this.value;
	$.ajax({
		url: fillSubmit,
		dataType: "json",
		type: "post",
		contentType: "application/json",
		data: JSON.stringify({"request":"strain","strain": valueSelected})
	}).done(function(response){
		//populate strain form
		if (response["strainId"]!="new"){
			$("#StrainName").val(response["strainId"]);
			$("#StrainName").prop("disabled", true);
			$("#strain_ploidity").val(response["ploidity"]);
			$("#strain_ploidity").prop("disabled", true);
			$("#strain_mating_type").val(response["matingType"]);
			$("#strain_mating_type").prop("disabled", true);
			$("#strain_mutations").val(response["mutations"]);
			$("#strain_mutations").prop("disabled", true);
			$("#strain_link").val(response["link"]);
			$("#strain_link").prop("disabled", true);
			$("#strain_comment").val(response["comment"]);
			$("#strain_comment").prop("disabled", true);					
		} else {
			$("#StrainName").val("");
			$("#StrainName").prop("disabled", false);
			$("#strain_ploidity").val("");
			$("#strain_ploidity").prop("disabled", false);
			$("#strain_mating_type").val("");
			$("#strain_mating_type").prop("disabled", false);
			$("#strain_mutations").val("");
			$("#strain_mutations").prop("disabled", false);
			$("#strain_link").val("");
			$("#strain_link").prop("disabled", false);
			$("#strain_comment").val("");
			$("#strain_comment").prop("disabled", false);
		};	
	});
});

	//react to medium selection
	$('#MediumSelected').change(function(){
	var optionSelected = $("option:selected", this);
		var valueSelected = this.value;
	$.ajax({
		url: fillSubmit,
		dataType: "json",
		type: "post",
		contentType: "application/json",
		data: JSON.stringify({"request":"medium","medium": valueSelected})
	}).done(function(response){				
		if (response["Medium_ID"]!="new"){
			$("#Medium_Name").val(response["Medium_ID"]);
			$("#Medium_Name").prop("disabled", true);
			$("#Medium_pH").val(response["pH"]);
			$("#Medium_pH").prop("disabled", true);
			$("#Medium_CompoundSelected").prop("disabled", true);
			$("#Medium_CompoundName").prop("disabled", true);
			$("#Medium_Value").prop("disabled", true);
			$("#Medium_Unit").prop("disabled", true);
			$("#Medium_CompoundPubChemID").prop("disabled", true);
			$("#addCompound").prop("disabled", true);
			table.clear();
			table.rows.add(JSON.parse(response["composition"])).draw();
			$("#Medium_provided-error").remove();
		} else {
			$("#Medium_Name").val("");
			$("#Medium_Name").prop("disabled", false);
			$("#Medium_pH").val("");
			$("#Medium_pH").prop("disabled", false);
			$("#Medium_CompoundSelected").prop("disabled", false);
			$("#Medium_CompoundName").prop("disabled", false);
			$("#Medium_Value").prop("disabled", false);
			$("#Medium_Unit").prop("disabled", false);
			$("#Medium_CompoundPubChemID").prop("disabled", false);
			$("#addCompound").prop("disabled", false);
			table.clear().draw();
		};
	});   			
});

//enable add component if Medium Compound Name is provided
$("#Medium_CompoundName").keyup(function(){
	if ($("#Medium_CompoundName").val().trim().length !=0){
		$("#addCompound").prop("disabled", false);
	};
});

//add component to composition table
$("#addCompound").click(function(){
	table.row.add( [
		$("#Medium_CompoundName").val(),
		$("#Medium_CompoundPubChemID").val(),							
		$("#Medium_Value").val(),							
		$("#Medium_Unit").val()	
	]).draw();
	$("#addCompound").prop("disabled", true);
	$("#Medium_provided-error").remove();
});

//remove selected rows from table
$("#deleteRow").click(function(){
	table.rows({selected:true}).remove().draw();
});

//get pubchem of component
$('#Medium_CompoundSelected').change(function(){
	var optionSelected = $("option:selected", this);
		var valueSelected = this.value;
	$.ajax({
		url: fillSubmit,
		dataType: "json",
		type: "post",
		contentType: "application/json",
		data: JSON.stringify({"request":"component","component": valueSelected})
	}).done(function(response){
		if (response["PubChem"]!="new"){
			$("#Medium_CompoundPubChemID").val(response["PubChem"]);
			$("#Medium_CompoundName").val(response["Component"]);
			$("#Medium_Unit").val("");
			$("#Medium_Value").val("");
			$("#Medium_CompoundPubChemID").prop("disabled", true);
			$("#Medium_CompoundName").prop("disabled", true);
		} else {
			$("#Medium_CompoundPubChemID").val("");
			$("#Medium_CompoundName").val("");
			$("#Medium_Unit").val("");
			$("#Medium_Value").val("");
			$("#Medium_CompoundPubChemID").prop("disabled", false);
			$("#Medium_CompoundName").prop("disabled", false);
		};		
	});
});

//react to selection of datatype
$('#DataTypes').change(function(){
	var optionSelected = $("option:selected", this);
		var valueSelected = this.value;
	$.ajax({
		url: fillSubmit,
		dataType: "json",
		type: "post",
		contentType: "application/json",
		data: JSON.stringify({"request":"dtype","dtype": valueSelected})
	}).done(function(response){
		$("#primary_identifier").text(response["identifier"]);
	});
});

//download correct file
$("#getTemplate").click(function(){
	var oldHref = $(this).attr("href");
	var dType = $("#DataTypes").val();
	if ($("#IsTimeResolved").val() == "true"){
		var tType = "_time_";
	} else  if ($("#IsTimeResolved").val() == "false"){
		var tType = "_";
	};				
	var vType = $("#ValueType").val();
	var filename = dType+tType+vType+".csv";
	$(this).attr("href", oldHref + "?file=" + filename);
});

//upload datatable
var uploadTable;
$("#addData").click(function(){	
	var files = $("#uploadData").prop("files");
	if (files.length>0){
		var formData = new FormData();
		formData.append("file", files[0]);
		$.ajax({
			url: uploadTemplate,
			type: 'post',
			data: formData,
			contentType: false,
			processData: false,
			cache: false
		}).done(function(response){
			uploadTable=$("#uploadedDataTable").DataTable({
				dom: "rt",
				"columns": JSON.parse(response["columns"]),
				"data": JSON.parse(response["data"])
			});
			$("#addData").prop("disabled", true);
			$("#uploadData").prop("disabled", true);
			$("#pretty-input").prop("disabled", true);
			$("#pretty-button").prop("disabled", true);
			$("#removeData").prop("disabled", false);
			$("#uploadSpan").attr("style","display: block");
			$("#uploadPanel").attr("style","display: block");
			$("#Data_provided-error").remove();
		});
	};	
});

//remove uploaded data
$("#removeData").click(function(){
	uploadTable.clear().destroy();
	$("#uploadedDataTable thead").empty();
	$("#addData").prop("disabled", false);
	$("#uploadData").prop("disabled", false);
	$("#pretty-input").prop("disabled", false);
	$("#pretty-button").prop("disabled", false);
	$("#removeData").prop("disabled", true);
	$("#uploadSpan").attr("style","display: none");
	$("#uploadPanel").attr("style","display: none");
});

//custom validation methods for hidden inputs
	//medium provided
	$.validator.addMethod("mediumProvided", function(){
		var provided = table.data().any();
		if (provided){
			$("#Medium_provided-error").remove();
		} else {
			if (! $("#Medium_provided-error").length){
				$("<label id='Medium_provided-error' class='errors' for='Medium_provided'>Please provide a medium composition.</label>").insertAfter("#Medium_provided");
			};
		};
		return provided;
	}, "Please provide a medium composition.");

	//data provided
	$.validator.addMethod("dataProvided", function(){
		var provided;
		if (typeof uploadTable !== 'undefined'){
			provided = uploadTable.data().any();
		} else {
			provided = false;
		};
		if (provided){
			$("#Data_provided-error").remove();
		} else {
			if (! $("#Data_provided-error").length){
				$("<label id='Data_provided-error' class='errors' for='Data_provided'>Please provide data to upload.</label>").insertAfter("#Data_provided");
			};					
		};
		return provided;
	}, "Please provide data to upload.");

//validate on submit		
var validator = $("form[name='submit_data']").validate({
	onsubmit: true,
	errorClass: 'errors',
	ignore: [],
	invalidHandler: function() {		
		$("#submissionErrors").text();
		$("#submissionErrors").text(validator.numberOfInvalids() + " field(s) are invalid");
		$("#submissionErrors").prop("hidden", false);
	},
	rules: {
		DataSetName: {
			required: true,
			minlength: 8
		},
		DataSetContact: {
			required: true,
			email: true
		},
		StrainName: {
			required: true,
			minlength: 4
		},
		strain_link: {
			required: false,
			url: true
		},					
		Medium_pH: {
			required: false,
			range: [0,14]
		},
		Medium_Name: {
			required: true,
			minlength: 8
		},
		Medium_provided: "mediumProvided",
		Temperature: {
			required: true,
			range: [0, 100]
		},
		GrowthRate: {
			required: false,
			number: true
		},
		MethodName: {
			required: true,
			minlength: 3
		},
		Unit: {
			required: true
		},
		Data_provided: "dataProvided",
		check_time: {
			required: true,
			remote: checkTime
		}
	},
	submitHandler: function(form, event){
		var disabled = $("form").find(':input:disabled').removeAttr('disabled');
		var formData = $("form").serializeArray();
		disabled.attr('disabled','disabled');
		var mediumComposition = jsonTable(table);
		var Data = jsonTable(uploadTable);
		var successful;	
		$.ajax({
			url: processSubmission,
			dataType: "json",
			type: "post",
			async: false,
			contentType: "application/json",
			data: JSON.stringify({"formData": formData, "mediumComposition": mediumComposition, "Data": Data}),
			error: function(){
				$("#submissionErrors").text();
				$("#submissionErrors").text("Something bad happened");
				$("#submissionErrors").prop("hidden", false);
				successful = false;
			}
		}).done(function(response){
			if (response){
				$("#submissionErrors").text();
				$("#submissionErrors").prop("hidden", true);
				successful = true;
			} else {
				$("#submissionErrors").text();
				$("#submissionErrors").text("Your data could not be submitted. Please check your data again, download your current data and contact us.");
				$("#submissionErrors").prop("hidden", false);
				successful = false;
			};
		});
		if (successful){
			form.submit();
		};
	}
});

//serialize datatable
function serializeTable(table){
	if (typeof table != "undefined"){
		if (table.data().any()){
			var series = "";
			table.columns().every(function(index) {
			    var data = this.data().toArray().toString();
				var col = $(table.column(index).header()).html();
				series += col+"="+data+"&";
			});
			series=series.slice(0,-1);
			series=series.replaceAll("/", "\u0298");
			return encodeURIComponent(series);
		} else {
			return "None";
		};
	} else {
		return "None"
	};		
};

//jsonify datatable
function jsonTable(table){
	if (typeof table != "undefined"){
		if (table.data().any()){
			var values = {};
			table.columns().every(function(index) {
			    var data = this.data().toArray();
				var col = $(table.column(index).header()).html();
				values[col]=data;
			});
			return JSON.stringify(values);
		} else {
			return "None";
		};
	} else {
		return "None"
	};		
};

//download current data
$("#getCurrent").click(function(){
	var disabled = $('form').find(':input:disabled').removeAttr('disabled');
	var formData = $('form').find('input[name!=csrf_token]').serialize();
	disabled.attr('disabled','disabled');
	formData=formData.replaceAll("/", "\u0298");
	formData=encodeURIComponent(formData);			
	var mediumData = serializeTable(table);
	var Data = serializeTable(uploadTable);
	var filename =formData+"&&"+mediumData+"&&"+Data;
	$(this).attr("href", downloadCurrent + filename);
});

//convert serialized table to json
function seriesToTable(tableString){
	var mediumData=tableString.split("&");
	var values = {};
	var columns = [];
	var nCol = mediumData.length;

	for (i=0; i<nCol; i++){
		var col = mediumData[i].split("=")[0];
		var val = mediumData[i].split("=")[1].split(",");
		values[col]=val;
		columns.push({"data": col, "title": col});
	};

	nRow=values[Object.keys(values)[0]].length;
	var data = [];
	for (i=0; i<nRow; i++){
		var dCol = {};
		for (j=0; j<nCol; j++){
			var col = Object.keys(values)[j];
			dCol[col]=values[col][i];
		};
		data.push(dCol);
	};
	return [columns, data];
};

//reupload current data
$("#addCurrent").click(function(){	
	var files=$("#reloadCurrent").prop("files");
	if (files.length>0){
		var reader = new FileReader();
		reader.readAsText(files[0]);
		reader.onload = function(e) {
		    var content = reader.result;
		    content=content.replaceAll("\u0298", "/");
		    content=content.split("&&");
		    //fill form data
		    $.each(content[0].split('&'), function (index, elem) {
			   	var vals = elem.split('=');
				$("[name='" + vals[0] + "']").val(decodeURIComponent(vals[1].replace(/\+/g, ' ')));
			});
			//fill medium content table
			if (content[1]!="None"){
				var mediumContent = seriesToTable(content[1]);
				table.clear().destroy();
				table = $('#medium_composition').DataTable({
					dom: "rtB",
					select: true,
					buttons: [{
				        text: 'Delete selected rows',
				        attr: {
				        	id: 'deleteRow',
				        	class: "btn btn-default"
				        }
				    }],
				    columns: mediumContent[0],
				    data: mediumContent[1]
				});
			};
			//fill data table
			if (content[2]!="None"){
				var dataContent = seriesToTable(content[2]);
				if (typeof uploadTable!="undefined"){
					uploadTable.clear().destroy();
					$("#uploadedDataTable thead").empty();
				};
						
				uploadTable=$("#uploadedDataTable").DataTable({
					dom: "rt",
					"columns": dataContent[0],
					"data": dataContent[1]
				});

				$("#addData").prop("disabled", true);
				$("#uploadData").prop("disabled", true);
				$("#pretty-input").prop("disabled", true);
				$("#pretty-button").prop("disabled", true);
				$("#removeData").prop("disabled", false);
				$("#uploadSpan").attr("style","display: block");
				$("#uploadPanel").attr("style","display: block");
				$("#Data_provided-error").remove();
			};			
		};		
	};	
});

//reset form
$("#clearData").click(function(){
	$("form").get(0).reset();
	window.location.reload(false); 
});