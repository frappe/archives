// TODO
// 1. Type selection based on first 10 rows
// 1. Option to select Header Row
// 1. Transposer - Slick Grid should change
// 1. Save settings

var ChartBuilder = Class.extend({
	init: function(opts) {
		// opts = {
		// 	url: "wb-india.csv"
		// 	
		// }
		var me = this;
		$.extend(this, opts);
				
		if(typeof this.conf.selected_rows==="string")
			this.conf.selected_rows = JSON.parse(this.conf.selected_rows)
		
		$("#chart, #slickgrid").empty();
		$("#chart-builder-edit")
			.unbind("click")
			.on("click", function() { me.make_conf_editor(); return false;});

		$("#dataset-discuss")
			.unbind("click")
			.on("click", function() { me.show_discussion(); return false;});

		$("#dataset-download")
			.unbind("click")
			.on("click", function() { window.open(me._dataset.url); return false; });

		$("#dataset-help")
			.unbind("click")
			.on("click", function() { wn.msgprint(me._dataset.description); return false;});
			
		$("#navbar-rating")
			.unbind("click")
			.on("click", function() { me.rate_me(); return false;});


		$('[data-for-chart=1]').toggle(true);
		$('[data-for-list=1]').toggle(false);

		this.show_rating();
		this.set_title(this.title);
		this.get_csv(this.url);
	},
	
	set_title: function(title) {
		if(!title) title = "Title Not Set";
		$("#dataset-title").text(title);
		
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
									<option value="Pie">Pie</option>\
								</select>\
					            <p class="help-block">One of Line, Bar, Radar</p>\
					        </div>\
					        <div class="form-group">\
					            <label for="start-column">First Column</label>\
					            <select class="form-control" id="start-column"></select>\
					            <p class="help-block">First column to plot data</p>\
					        </div>\
					        <div class="form-group">\
					            <label for="head-row">Head Row</label>\
					            <select class="form-control" id="head-row"></select>\
					            <p class="help-block">Row that labels the data</p>\
					        </div>\
					        <div class="form-group" style="padding-right: 20px; position: static;">\
					            <button type="button" class="btn btn-default close-conf-editor">Close</button>\
					            <button type="button" class="btn btn-success save-conf-editor">Save</button>\
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
							<label>\
							    <input type="checkbox" id="transpose"> <span>Transpose</span>\
							</label>\
					    </div>\
					</div>\
					</div>\
				</div>\
			</div>\
			</div>')
			.appendTo(window.document.body);
			
		// TODO fix this bug
		this.conf_editor.find(".close, .close-conf-editor").on("click", function() {
			me.conf_editor.remove();
		});
				
		this.chart_type_select = this.conf_editor.find("#chart-type")
			.on("change", function() {
				me.conf.chart_type = $(this).val();
				me.legend_select.prop("disabled", me.conf.chart_type === "Pie");
				me.render_chart(); 
			});
		
		this.first_column_select = this.conf_editor.find("#start-column")
			.on("change", function() { 
				me.conf.first_column = parseInt($(this).val() || 0);
				me.render_chart(); 
			});
		
		this.last_column_select = this.conf_editor.find("#end-column")
			.on("change", function() { 
				me.conf.last_column = parseInt($(this).val() || 0);
				me.render_chart(); 
			});
		
		this.legend_select = this.conf_editor.find("#legend-column")
			.on("change", function() { 
				me.conf.legend = parseInt($(this).val() || 0);
				me.render_legend(); 
			});
		
		this.head_row_select = this.conf_editor.find("#head-row")
			.on("change", function() { 
				me.conf.head_row = parseInt($(this).val() || 0);
				me.render_grid();
				me.render_chart();
			});
			
		this.transpose_check = this.conf_editor.find("#transpose")
			.on("click", function() {
				me.conf.transpose = !!$(this).prop("checked");
				me.render_grid();
				me.set_column_selects();
				me.render_chart();
			});
		
		this.conf_editor.find(".save-conf-editor").click(function() {
			me.conf.name = me.name;
			me.conf.transpose = me.conf.transpose ? 1 : 0;
			wn.call({
				type: "POST",
				method: "opendataproject.doctype.data_set.data_set.public_save",
				args: me.conf,
				callback: function(r) {
					me.conf_editor.remove();
					if(r.exc) {
						wn.msgprint("There were errors.");
						console.log(r.exc);
					} else {
						wn.msgprint("Settings Saved.")
					}
				}
			})
		})
		
		this.set_column_selects();
		
		this.conf_editor.show();
	},
	
	show_discussion: function() {
		$.get("discuss", {name:this.name}, function(data) {
			wn.get_modal("Discuss This Dataset", data).modal("show");
		});
		return false;
	},
	
	show_rating: function() {
		var rating = this._dataset.rating || 0;
		for(var i=1; i<6; i++) {
			var $star = $("[data-rating='" + i + "']");
			if(rating >= 1) {
				$star.removeClass().addClass("icon-star");
			} else if (rating >= 0.5) {
				$star.removeClass().addClass("icon-star-half-empty");
			} else {
				$star.removeClass().addClass("icon-star-empty");
			}
			rating = rating - 1;
		}
	},
	
	rate_me: function() {
		var me = this;
		if(localStorage && localStorage["rated_" + me.name]) {
			wn.msgprint("You have already rated this dataset!");
		} else {
			var m = wn.get_modal("Rate This Data Set", '<p class="text-muted">5 best, 1 worst</p>\
				<ul class="rate-me"></ul>');
			for(var i=1; i<6; i++) {
				$a = $("<a>").appendTo($("<li>").appendTo(m.find(".rate-me"))).attr("data-rating", i);
				for(var j=1; j<=i; j++) {
					$('<i class="icon-star"></i>').appendTo($a);
				}
				for(var j=i+1; j<6; j++) {
					$('<i class="icon-star-empty"></i>').appendTo($a);
				}
			}
			m.modal("show");
			
			m.find("[data-rating]").click(function() {
				m.modal("hide");
				wn.call({
					type:"POST",
					method: "opendataproject.doctype.data_set.data_set.set_rating",
					args: {
						name: me.name,
						rating: $(this).attr("data-rating")
					},
					callback: function(r) {
						me._dataset.rating = parseInt(r.message);
						me.show_rating();
						localStorage["rated_" + me.name]= 1;
					}
				});
			})
		}
		return false;
	},
	
	get_csv: function(url) {
		var me = this;
		$.get(url, function(data) {
			if(data[0]=="-") {
				data = data.split("}\n-----\n").slice(-1)[0]
			}
			me.original_data = CSVToArray(data);
			me.set_conf();
			me.render_grid();
			me.set_start_last_column();
			me.set_chart_width();
			me.render_chart();
		});
	},
	
	set_conf: function() {
		var me = this;
		if(!this.conf) this.conf = {};

		$.each({
				head_row: 0,
				selected_rows: [0, 1, 2],
				first_column: 0,
				last_column: 0,
				legend: 0,
				chart_type: "Line",
				transpose: 0
			}, function(k, v) {
				if(me.conf[k]==null) {
					me.conf[k] = v
				}
			});
	},
	
	get_conf: function() {
		return this.conf;
	},
	
	render_grid: function() {
		var me = this;
		this.transpose();
		this.set_columns();
		this.set_objlist();
		
		this.checkboxSelector = new Slick.CheckboxSelectColumn({
	      cssClass: "slick-cell-checkboxsel"
	    });
		var columns = [this.checkboxSelector.getColumnDefinition()].concat(this.columns);
		
		var options = {
			enableCellNavigation: true,
			enableColumnReorder: false
		};

		this.grid = new Slick.Grid("#slickgrid", this.objlist, columns, options);
		this.grid.setSelectionModel(new Slick.RowSelectionModel({selectActiveRow: false}));
		this.grid.registerPlugin(this.checkboxSelector);
		this.grid.setSelectedRows(this.conf.selected_rows);
		this.grid.getSelectionModel().onSelectedRangesChanged.subscribe(function() {
			me.render_chart();
		});
		
		this.grid_data = this.grid.getData();
	},
	
	set_columns: function() {
		this.columns = [];
		
		var head_row = this.data[this.conf.head_row];
		for(var i=0, len=head_row.length; i < len; i++) {
			var name = head_row[i];
			var id = (name || "Column " + i).toLowerCase().replace(/ /g, "_");
			this.columns.push({id: id, name: name, field: id});
		}
	},
	
	set_objlist: function() {
		this.objlist = [];
		for(var ri=(this.conf.head_row + 1), rlen=this.data.length; ri<rlen; ri++) {
			var row = {};
			for(var ci=0, clen=this.columns.length; ci < clen; ci++) {
				var val = this.data[ri][ci];
				row[this.columns[ci].field] = val;
				
				if(ci===this.conf.legend) row["rgb"] = this.get_rgb(val).join(",");
				
				// TODO better type identifications
				if(val && !isNaN(val)) this.columns[ci].type = "number";
			}
			this.objlist.push(row);
		}
	},
	
	set_start_last_column: function() {
		if(this.conf.first_column || this.conf.last_column) return;
		var first_column, last_column, legend;
		for(var i=0, l=this.columns.length; i<l; i++) {
			if(this.columns[i].type==="number") {
				last_column = i;
				if(first_column==null) first_column = i;
			} else {
				if(legend==null) legend = i;
			}
		}
		first_column = ((last_column-first_column) > 10) ? (last_column-10) : first_column;
		this.conf.first_column = first_column;
		this.conf.last_column = last_column;
		if(!this.conf.legend) this.conf.legend = legend;
	},
	
	set_column_selects: function() {
		var me = this;
		var first_column, last_column;
		this.first_column_select.empty();
		this.last_column_select.empty();
		this.legend_select.empty();
		for(var i=0, l=this.columns.length; i<l; i++) {
			var name = this.columns[i].name;
			this.first_column_select.append('<option value="'+i+'">'+name+'</option>');
			if(this.columns[i].type!=="number"){
				this.legend_select.append('<option value="'+i+'">'+name+'</option>');
			}
		}
		this.last_column_select.html(this.first_column_select.html());
		this.first_column_select.val(this.conf.first_column);
		this.last_column_select.val(this.conf.last_column);

		if(this.conf.legend) {this.legend_select.val(this.conf.legend);}
		if(this.conf.chart_type) this.chart_type_select.val(this.conf.chart_type);
		this.transpose_check.prop("checked", !!this.conf.transpose);
		
		var l = this.data.length;
		if(l > 10) l = 10;
		this.head_row_select.empty();
		for(var i=0; i<l; i++) {
			this.head_row_select.append('<option value="'+i+'">'+this.data[i].join(", ")+'</option>');
		}
		this.head_row_select.val(this.conf.head_row);
		
		// reverse set values so that if not found in select, it sets correct value in conf
		this.conf.legend = parseInt(this.legend_select.val() || 0);
	},
	
	set_chart_width: function() {
		var $chart = $("#chart");
		$chart.attr("width", $chart.parent().width());
	},

	resize: function() {
		this.set_chart_width();
		this.render_chart();
	},
	
	render_chart: function(opts) {
		if(!this.grid) return;
		if(!opts) opts = {animationSteps: 20};
		this.set_chart_data();
		var context = document.getElementById("chart").getContext("2d");
		this.chart = new Chart(context)[this.conf.chart_type](this.chart_data, opts);
		this.render_legend();
		this.set_grid_height();
	},
	
	set_chart_data: function() {
		var me = this;
		var columns = $.map(this.columns, function(col, i) { 
			return (i>=me.conf.first_column  && i<=me.conf.last_column) ? col : null;
		});
		this.conf.selected_rows = this.grid.getSelectedRows();
		
		if(this.conf.chart_type === "Pie") {
			var row = this.grid_data[this.conf.selected_rows[0]];
			var dataset = $.map(columns, function(col) {
				var rgb = me.get_rgb(col.field).join(",");
				return {
					value: parseFloat(row[col.field] || 0),
					color: "rgba("+rgb+", 0.5)",
					name: col.name,
					rgb: rgb
				}
			});
			this.chart_data = dataset;
		} else {
			var datasets = $.map(this.conf.selected_rows, function(rowid) {
				var row = [];
				var data_row = me.grid_data[rowid];
				if(!data_row) return null;
				
				for(var i=0, l=columns.length; i<l; i++) {
					row.push(parseFloat(data_row[columns[i].field] || 0));
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
				labels : $.map(columns, function(v) { return v.name; }),
				datasets : datasets
			};
		}
	},
	
	render_legend: function() {
		var me = this;
		var $legend = $("#legend").empty();
		
		if(this.conf.chart_type === "Pie") {
			$.each(this.chart_data, function(i, d) {
				$legend.append('<div class="row">\
						<div class="legend-circle" style="background-color: rgba('+d.rgb+',0.5); \
							border: 2px solid '+d.color+'"></div>\
						<span>'+d.name+'</span>\
					</div>');
			});
		} else {
			var legend_field = this.columns[this.conf.legend].field;
			
			$.each(this.grid.getSelectedRows(), function(i, rowid) {
				var row = me.grid_data[rowid];
				if(!row) return;
				
				$legend.append('<div class="row">\
						<div class="legend-circle" style="background-color: rgba('+row.rgb+',0.5); \
							border: 2px solid rgb('+row.rgb+')"></div>\
						<span>'+row[legend_field]+'</span>\
					</div>');
			});
		}
	},
	
	set_grid_height: function() {
		var chart_height = $("#chart").parent().height();
		var window_height = $(window).height() - 50;
		if(window_height > chart_height) chart_height = window_height;

		$("#slickgrid").css("height", chart_height).attr("height", chart_height);
		this.grid.resizeCanvas();
	},
	
	transpose: function() {
		this.data = [].concat(this.original_data);
		if(this.conf.transpose) {
			this.data = this._transpose(this.data);
		}
	},

	_transpose: function(a) {
	    return Object.keys(a[0]).map(function (c) {
	        return a.map(function (r) {
	            return r[c];
	        });
	    });
	},
	
	get_rgb: function(str) {
		if(!str) str = new Date() + "";
		
		// str to hash
		for (var i = 0, hash = 0; i < str.length; hash = str.charCodeAt(i++) + ((hash << 5) - hash));

		// int/hash to hex
		for (var i = 0, colour = "#"; i < 3; colour += ("00" + ((hash >> i++ * 8) & 0xFF).toString(16)).slice(-2));

		return this.hex_to_rgb(colour);
	},
	
	hex_to_rgb: function(hex) {
		function hexToR(h) {return parseInt((cutHex(h)).substring(0,2),16)}
		function hexToG(h) {return parseInt((cutHex(h)).substring(2,4),16)}
		function hexToB(h) {return parseInt((cutHex(h)).substring(4,6),16)}
		function cutHex(h) {return (h.charAt(0)=="#") ? h.substring(1,7):h}
		
		return [hexToR(hex), hexToG(hex), hexToB(hex)];
	}
});