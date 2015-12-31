// TODO
// 1. Type selection based on first 10 rows
// 1. Option to select Header Row
// 1. Transposer - Slick Grid should change
// 1. Save settings

$(document).ready(function() {
	window.chart_builder = new ChartBuilder({
		url: "wb-india.csv",
		title: "World Bank - India"
	});
	
	$(window).on("resize", function() {
		window.chart_builder.set_chart_width();
		window.chart_builder.render_chart();
	});
});

var ChartBuilder = Class.extend({
	init: function(opts) {
		// opts = {
		// 	url: "wb-india.csv"
		// 	
		// }
		$.extend(this, opts);
		this.set_title(this.title);
		this.make_conf_editor();
		this.get_csv(this.url);
	},
	
	set_title: function(title) {
		if(!title) title = "Chart Builder";
		$("head title").text(title);
		$(".navbar-brand").text(title);
	},
	
	make_conf_editor: function() {
		var me = this;
		this.conf_editor = $('<div class="modal" style="overflow: auto;" tabindex="-1">\
			<div class="modal-dialog">\
				<div class="modal-content">\
					<div class="modal-header">\
						<a type="button" class="close"\
							data-dismiss="modal" aria-hidden="true">&times;</a>\
						<h4 class="modal-title">Edit Settings</h4>\
					</div>\
					<div class="modal-body ui-front">\
					<div class="row">\
					    <div class="col-md-6" style="">\
					        <div class="form-group" style="position: static;">\
					            <label for="chart-type">Chart Type</label>\
					            <select class="form-control" id="chart-type">\
									<option value="Line">Line</option>\
								    <option value="Bar">Bar</option>\
								    <option value="Radar">Radar</option>\
								</select>\
					            <p class="help-block">One of Line, Bar, Radar</p>\
					        </div>\
					        <div class="form-group">\
					            <label for="start-column">First Column</label>\
					            <select class="form-control" id="start-column"></select>\
					            <p class="help-block">First column to plot data</p>\
					        </div>\
					        <div class="form-group" style="padding-right: 20px; position: static;">\
					            <button type="button" class="btn btn-default close-conf-editor">Close</button>\
					        </div>\
					    </div>\
					    <div class="col-md-6" style="">\
					        <div class="form-group">\
					            <label for="legend-column">Legend</label>\
					            <select class="form-control" id="legend-column"></select>\
					            <p class="help-block">Column which describes the data</p>\
					        </div>\
					        <div class="form-group">\
					            <label for="end-column">Last Column</label>\
					            <select class="form-control" id="end-column"></select>\
					            <p class="help-block">Last column to plot data</p>\
					        </div>\
					    </div>\
					</div>\
					</div>\
				</div>\
			</div>\
			</div>')
			.appendTo(window.document.body);
			
		$("#chart-builder-edit").on("click", function() {
			me.conf_editor.show();
		});
		
		// TODO fix this bug
		this.conf_editor.find(".close, .close-conf-editor").on("click", function() {
			me.conf_editor.hide();
		});
		
		this.chart_select = this.conf_editor.find("#chart-type")
			.on("change", function() { me.render_chart(); });
		this.start_select = this.conf_editor.find("#start-column")
			.on("change", function() { me.render_chart(); });
		this.end_select = this.conf_editor.find("#end-column")
			.on("change", function() { me.render_chart(); });
		this.legend_select = this.conf_editor.find("#legend-column")
			.on("change", function() { me.render_legend(); });
	},
	
	get_csv: function(url) {
		var me = this;
		$.get(url, function(data) {
			me.data = CSVToArray(data);
			me.set_conf();
			me.render_grid();
			me.set_column_selects();
			me.set_chart_width();
			me.render_chart();
		});
	},
	
	set_conf: function(conf) {
		if(!conf) {
			conf = {
				head_rowid: 0,
				selected_rowids: [0, 1, 2],
				start_colid: 0,
				end_colid: 0,
				legend_colid: 0,
				chart_type: "Line"
			};
		}
		this.conf = conf;
		if(this.conf.chart_type) this.chart_select.val(this.conf.chart_type)
	},
	
	get_conf: function() {
		return this.conf;
	},
	
	render_grid: function(data) {
		var me = this;
		if(!data) data = this.data;
		this.set_columns();
		this.set_objlist();
		
		var options = {
			enableCellNavigation: true,
			enableColumnReorder: false
		};
		
		this.checkboxSelector = new Slick.CheckboxSelectColumn({
	      cssClass: "slick-cell-checkboxsel"
	    });
		var columns = [this.checkboxSelector.getColumnDefinition()].concat(this.columns);
		this.grid = new Slick.Grid("#slickgrid", this.objlist, columns, options);
		this.grid.setSelectionModel(new Slick.RowSelectionModel({selectActiveRow: false}));
		this.grid.registerPlugin(this.checkboxSelector);
		this.grid.setSelectedRows(this.conf.selected_rowids);
		this.grid.getSelectionModel().onSelectedRangesChanged.subscribe(function() {
			me.render_chart();
		});
		
		this.grid_data = this.grid.getData();
	},
	
	set_columns: function() {
		this.columns = [];
		var head_row = this.data[this.conf.head_rowid];
		for(var i=0, len=head_row.length; i < len; i++) {
			var name = head_row[i];
			var id = name.toLowerCase().replace(/ /g, "_");
			this.columns.push({id: id, name: name, field: id});
		}
	},
	
	set_objlist: function() {
		this.objlist = [];
		for(var ri=(this.conf.head_rowid + 1), rlen=this.data.length; ri<rlen; ri++) {
			var row = {rgb: this.random_rgb().join(",")};
			for(var ci=0, clen=this.columns.length; ci < clen; ci++) {
				var val = this.data[ri][ci];
				row[this.columns[ci].field] = val;
				
				// TODO better type identifications
				if(val && !isNaN(val)) this.columns[ci].type = "number";
			}
			this.objlist.push(row);
		}
	},
	
	random_rgb: function() {
		var r = Math.floor(Math.random() * 256),
	        g = Math.floor(Math.random() * 256),
	        b = Math.floor(Math.random() * 256);
		return [r, g, b];
	},
	
	set_column_selects: function() {
		var me = this;
		var start_colid, end_colid;
		for(var i=0, l=this.columns.length; i<l; i++) {
			var name = this.columns[i].name;
			this.start_select.append('<option value="'+i+'">'+name+'</option>');
			if(this.columns[i].type==="number") {
				end_colid = i;
				start_colid = ((i-10) >= 0) ? (i-10) : 0;
			} else {
				this.legend_select.append('<option value="'+i+'">'+name+'</option>');
			}
		}
		this.end_select.html(this.start_select.html());
		this.start_select.val(this.conf.start_colid || start_colid);
		this.end_select.val(this.conf.end_colid || end_colid);
		if(this.conf.legend_colid) this.legend_select.val(this.conf.legend_colid);
	},
	
	set_chart_width: function() {
		var $chart = $("#chart");
		$chart.attr("width", $chart.parent().width());
	},
	
	render_chart: function(opts) {
		if(!this.grid) return;
		if(!opts) opts = {animationSteps: 20};
		this.set_chart_data();
		var context = document.getElementById("chart").getContext("2d");
		this.conf.chart_type = this.chart_select.val();
		this.chart = new Chart(context)[this.conf.chart_type](this.chart_data, opts);
		this.render_legend();
		this.set_grid_height();
	},
	
	set_chart_data: function() {
		var me = this;
		this.conf.start_colid = parseFloat(me.start_select.val() || 0);
		this.conf.end_colid = parseFloat(me.end_select.val() || 0);
		var columns = $.map(this.columns, function(col, i) { 
			return (i >=me.conf.start_colid  && i<=me.conf.end_colid) ? col.field : null;
		});
		this.conf.selected_rowids = this.grid.getSelectedRows();
		var datasets = $.map(this.conf.selected_rowids, function(rowid) {
			var row = [];
			for(var i=0, l=columns.length; i<l; i++) {
				row.push(parseFloat(me.grid_data[rowid][columns[i]] || 0));
			}
			var rgb = me.grid_data[rowid].rgb;
			return {
				fillColor: "rgba("+rgb+",0.5)",
				strokeColor : "rgba("+rgb+",1)",
				pointColor : "rgba("+rgb+",1)",
				pointStrokeColor : "#fff",
				data : row
			};
		});
		
		this.chart_data = {
			labels : columns,
			datasets : datasets
		};
	},
	
	render_legend: function() {
		var me = this;
		this.conf.legend_colid = parseFloat(this.legend_select.val() || 0);
		var legend_field = this.columns[this.conf.legend_colid].field;
		var $legend = $("#legend").empty();
		$.each(this.grid.getSelectedRows(), function(i, rowid) {
			var row = me.grid_data[rowid];
			$legend.append('<div class="row">\
					<div class="legend-circle" style="background-color: rgba('+row.rgb+',0.5); \
						border: 2px solid rgb('+row.rgb+')"></div>\
					<span>'+row[legend_field]+'</span>\
				</div>');
		});
	},
	
	set_grid_height: function() {
		var chart_height = $("#chart").parent().height();
		var window_height = $(window).height() - 50;
		if(window_height > chart_height) chart_height = window_height;

		$("#slickgrid").css("height", chart_height).attr("height", chart_height);
		this.grid.resizeCanvas();
	}
});