//get parameters from template
var script_tag = document.getElementById('resultTable');
var searchFor = script_tag.getAttribute("search");
var selection = JSON.parse(script_tag.getAttribute("selection"));

//init datatable
var table=$('#results_table').DataTable({
	columnDefs: [
		{targets: selection, visible: true},
		{targets: '_all', visible: false}
		],
	dom: "<'row'<'col-sm-6'i><'col-sm-6'f>><'row'<'col-sm-4'l><'col-sm-3'B><'col-sm-5'p>>RSrt<'bottom'><'row'<'col-sm-7'><'col-sm-5'p>>",
	buttons: [
		{
			extend: "colvis",
			text: "Select Columns",
			columns: ":gt(0)"
		},
		{
            extend: 'csv',
            text: "<span title='Download CSV' class='glyphicon glyphicon-download-alt'></span>",
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

//adjust colwidth if column selection changes
$('#results_table').on('column-visibility.dt', function () {
    table.columns.adjust();
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