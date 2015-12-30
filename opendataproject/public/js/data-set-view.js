var DataSetViewer = Class.extend({
	init: function() {
		if(localStorage && !localStorage.rated) {
			localStorage.rated = {};
		}
		this.wrapper = $("#datasetgrid");
		this.columns = [
			{id: "title", name: "Title", field: "title", width: 400},
			{id: "row_count", name: "Row Count", field: "row_count"},
			{id: "rating", name: "Rating", field: "rating", formatter: 
				function formatter(row, cell, value, columnDef, dataContext) {
					var rating = parseFloat(value || 0);
					var html = "";
					for(var i=1; i<6; i++) {
						if(rating >= 1) {
							html += '<i class="icon-star"></i>';
						} else if (rating >= 0.5) {
							html += '<i class="icon-star-half-empty"></i>';
						} else {
							html += '<i class="icon-star-empty"></i>';
						}
						rating = rating - 1;
					}
					return html;
				}
			}
		];
		this.options = {
			enableCellNavigation: true,
			enableColumnReorder: false,
			syncColumnCellResize: true,
			forceFitColumns: true,
			rerenderOnResize: true,
			showHeaderRow: true,
			headerRowHeight: 30,
			explicitInitialization: true
		};
		this.make_id_map();
	},
	make_id_map: function() {
		this.data_by_id = {};
		for(var i=0, j=datasets.length; i<j; i++) {
			this.data_by_id[datasets[i].id] = datasets[i];
		}
	},
	make: function() {
		var me = this;
		this.columnFilters = {};
		this.make_dataview();
		this.grid = new Slick.Grid("#datasetgrid", this.dataView, this.columns, this.options);
		this.grid.setSelectionModel(new Slick.RowSelectionModel({selectActiveRow: false}));
		// this.grid.registerPlugin(this.checkboxSelector);
		// this.grid.setSelectedRows(this.conf.selected_rowids);

		this.grid.onClick.subscribe(function (e) {
			var cell = me.grid.getCellFromEvent(e);
			me.set_route(me.grid.getDataItem(cell.row).id);
			e.stopPropagation();
		});
		
		$(this.grid.getHeaderRow()).delegate(":input", "change keyup", function (e) {
			var columnId = $(this).data("columnId");
			if (columnId != null) {
				me.columnFilters[columnId] = $.trim($(this).val());
				me.dataView.refresh();
			}
		});
		
		this.grid.onHeaderRowCellRendered.subscribe(function(e, args) {
			$(args.node).empty();
			$("<input type='text'>")
				.data("columnId", args.column.id)
				.val(me.columnFilters[args.column.id])
				.appendTo(args.node);
		});
		this.grid.init();
		
		this.show();
		this.resize();
	},
	
	make_dataview: function() {
		// initialize the model
		this.dataView = new Slick.Data.DataView({ inlineFilters: true });
		this.dataView.beginUpdate();
		this.dataView.setItems(datasets);
		this.dataView.setFilter(this.inline_filter);
		this.dataView.endUpdate();
		
		var me = this;
		this.dataView.onRowCountChanged.subscribe(function (e, args) {
			me.grid.updateRowCount();
			me.grid.render();
		});

		this.dataView.onRowsChanged.subscribe(function (e, args) {
			me.grid.invalidateRows(args.rows);
			me.grid.render();
		});
	},
	
	inline_filter: function (item) {
		var me = window.data_set_viewer;
		for (var columnId in me.columnFilters) {
			if (columnId !== undefined && me.columnFilters[columnId] !== "") {
				var c = me.grid.getColumns()[me.grid.getColumnIndex(columnId)];
				if(!(c.field==="title" && item[c.field].toLowerCase().indexOf(me.columnFilters[columnId])!==-1)) {
					return false;
				}
			}
		}
		return true;
	},
	
	resize: function() {
		if(this.chart_view) {
			this.chart_view.resize();
		} else {
			this.resize_data_set_grid();
		}
		
	},
	
	resize_data_set_grid: function() {
		var width = $(window).width();
		this.columns[0].width = parseInt(width * 0.8);
		this.columns[1].width = parseInt(width * 0.1);
		this.columns[1].width = parseInt(width * 0.1);
		this.wrapper.css("height", $(window).height()-52).css("width", width);
		this.grid.resizeCanvas();
	},
	
	show: function() {
		this.chart_view = null;
		$(".navbar-brand").html("<i class='icon-home'></i> OpenDataProject.in");
		$('[data-for-chart=1]').toggle(false);
		$('[data-for-list=1]').toggle(true);
		this.resize_data_set_grid();
	},
	
	show_chart: function(route) {
		var d = this.data_by_id[route];
		// var d = this.grid.getData()[route];
		wn.call({
			method: "opendataproject.doctype.data_set.data_set.get_settings",
			args: {name: d.id},
			callback: function(r) {
				this.chart_view = new ChartBuilder({
					url: "app/data/" + d.raw_filename,
					title: d.title,
					name: d.id,
					_dataset: d,
					conf: r.message
				});
			}
		})
	},
	
	set_route: function(route) {
		window.location.hash = route;		
	},
	
	set_view_from_route: function() {
		var route = window.location.hash.slice(1);
		if(route==="home" || !route) {
			this.show();
		} else {
			this.show_chart(route);
		}
	}
})