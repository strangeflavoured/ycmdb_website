//get parameters from template
var script_tag = document.getElementById('resultTable');
var searchFor = script_tag.getAttribute("search");

//init datatable
var table=$('#results_table').DataTable({
	dom: "<'row'<'col-sm-6'i><'col-sm-6'f>><'row'<'col-sm-6'l><'col-sm-6'p>>RSrt<'bottom'><'row'<'col-sm-6'B><'col-sm-6'p>>",
	buttons: [
		{
            extend: 'csv',
            text: "<span class='glyphicon glyphicon-download-alt'></span>",
            modifier :{
            	selected: true
            }
        }],
	colReorder: true,
	fixedHeader: {
		header: true,
		footer: true
	},
	keys: true,
	paging: true,
	responsive: true,
	rowReorder: true,
	filter: true,
	searching: true,
	scrollX: true,
	select: true,
	autoWidth: true
});

//customise search filter
$("#results_table_filter > label").html("<label><input id='search_input' type='search' class='form-control input' placeholder='Search' aria-controls='meta_table'></label>");

$("#results_table_filter input[type=search]").on("keyup", function(){
	table.search(this.value).draw();
});			

//search datatable
if (searchFor!=""){
	$("#search_input").val(searchFor);
	table.search(searchLoad).draw();
};