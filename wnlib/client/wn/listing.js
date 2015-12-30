// Copyright (c) 2012 Web Notes Technologies Pvt Ltd (http://erpnext.com)
// 
// MIT License (MIT)
// 
// Permission is hereby granted, free of charge, to any person obtaining a 
// copy of this software and associated documentation files (the "Software"), 
// to deal in the Software without restriction, including without limitation 
// the rights to use, copy, modify, merge, publish, distribute, sublicense, 
// and/or sell copies of the Software, and to permit persons to whom the 
// Software is furnished to do so, subject to the following conditions:
// 
// The above copyright notice and this permission notice shall be included in 
// all copies or substantial portions of the Software.
// 
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
// INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
// PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
// CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
// OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
// 

// new re-factored Listing object
// uses FieldGroup for rendering filters
// removed rarely used functionality
//
// opts:
//   parent

//   method (method to call on server)
//   args (additional args to method)
//   get_args (method to return args as dict)

//   show_filters [false]
//   doctype
//   filter_fields (if given, this list is rendered, else built from doctype)

//   query or get_query (will be deprecated)
//   query_max
//   buttons_in_frame

//   no_result_message ("No result")

//   style: compact

//   page_length (20)
//   hide_refresh (False)
//   no_toolbar
//   new_doctype
//   [function] render_row(parent, data)
//   [function] onrun
//   no_loading (no ajax indicator)

wn.provide('wn.ui');
wn.ui.Listing = Class.extend({
	init: function(opts) {
		this.opts = opts || {};
		this.page_length = 20;
		this.start = 0;
		this.data = [];
		if(opts) {
			this.make();
		}
	},
	prepare_opts: function() {
		if(this.opts.new_doctype) {
			if(wn.boot.profile.can_read.indexOf(this.opts.new_doctype)==-1) {
				this.opts.new_doctype = null;
			} else {
				this.opts.new_doctype = this.opts.new_doctype;
			}
		}
		_.get_or_set(this.opts, 'no_result_message', 'Nothing to show.');
		_.get_or_set(this.opts, 'title', '');
		_.get_or_set(this.opts, 'method', 'wn.model.get_list');

		if(!this.opts.no_result_message) {
			this.opts.no_result_message = 'Nothing to show'
		}
	},
	make: function(opts) {
		if(opts) {
			this.opts = opts;
		}
		this.prepare_opts();
		$.extend(this, this.opts);
		
		$(this.parent).html(_.template('\
			<div class="wnlist">\
				<h3 class="title hide"><%=title%></h3>\
				\
				<div class="list-filters hide">\
					<div class="show_filters well">\
						<div class="filter_area"></div>\
						<div class="clear">\
							<button class="btn btn-small add-filter-btn">\
								<i class="icon-plus"></i> Add Filter</button>\
						</div>\
					</div>\
				</div>\
				\
				<div style="margin-bottom:9px" class="list-toolbar-wrapper">\
					<div class="list-toolbar" style="display:inline-block; margin-right: 10px;">\
					</div>\
					<div style="display:inline-block; width: 24px; margin-left: 4px">\
						<img src="images/lib/ui/button-load.gif" \
						class="img-load"/></div>\
				</div><div style="clear:both"></div>\
				\
				<div class="no-result help hide">\
					<%=no_result_message%>\
				</div>\
				\
				<div class="result">\
					<div class="result-list"></div>\
				</div>\
				\
				<div class="paging-button">\
					<button class="btn btn-small btn-more hide">More...</div>\
				</div>\
			</div>\
		', this.opts));
		this.$w = $(this.parent).find('.wnlist');
		this.set_events();
		
		if(this.appframe) {
			this.$w.find('.list-toolbar-wrapper').toggle(false);
		} 
		
		if(this.show_filters) {
			this.make_filters();			
		}
	},
	add_button: function(label, click, icon) {
		if(this.appframe) {
			return this.appframe.add_button(label, click, icon)
		} else {
			$button = $('<button class="btn btn-small"></button>')
				.appendTo(this.$w.find('.list-toolbar'))
			if(icon) {
				$('<i>').addClass(icon).appendTo($button);
			}
			$button.html(label).click(click);
			return $button
		}
	},
	show_view: function($btn, $div, $btn_unsel, $div_unsel) {
		$btn_unsel.removeClass('btn-info');
		$btn_unsel.find('i').removeClass('icon-white');
		$div_unsel.toggle(false);

		$btn.addClass('btn-info');
		$btn.find('i').addClass('icon-white');
		$div.toggle(true);
	},
	set_events: function() {
		var me = this;
	
		// next page
		this.$w.find('.btn-more').click(function() {
			me.run({append: true });
		});
		
		// title
		if(this.title) {
			this.$w.find('h3').html(this.title).toggle(true);
		}
	
		// hide-refresh
		if(!(this.hide_refresh || this.no_refresh)) {
			this.add_button('Refresh', function() {
				me.run();
			}, 'icon-refresh');
		}
				
		// new
		if(this.new_doctype) {
			this.add_button('New ' + this.new_doctype, function() {
				newdoc(me.new_doctype);
			}, 'icon-plus');
		} 
		
		// hide-filter
		if(me.show_filters) {
			this.add_button('Show Filters', function() {
				me.filter_list.show_filters();
			}, 'icon-search').addClass('btn-filter');
		}
		
		if(me.no_toolbar || me.hide_toolbar) {
			me.$w.find('.list-toolbar-wrapper').toggle(false);
		}
	},

	make_filters: function() {
		this.filter_list = new wn.ui.FilterList({
			listobj: this, 
			$parent: this.$w.find('.list-filters').toggle(true),
			doctype: this.doctype,
			filter_fields: this.filter_fields
		});
		if(this.style=='compact') {
			this.$w.find('.show_filters').addClass('compact');
		}
	},

	clear: function() {
		this.data = [];
		this.$w.find('.result-list').empty();
		this.$w.find('.result').toggle(true);
		this.$w.find('.no-result').toggle(false);
		this.start = 0;
	},
	run: function(args) {
		me.set_working(true);
		wn.call({
			method: this.opts.method,
			args: this.get_call_args(args),
			callback: function(r) { 
				me.set_working(false);
				me.render_results(r) 
			},
			no_spinner: this.opts.no_loading
		});
	},
	set_working: function(flag) {
		this.$w.find('.img-load').toggle(flag);
	},
	get_call_args: function(opts) {
		// load query
		var args = {
			limit_start: this.start,
			page_length: this.page_length
		}
		
		// append user-defined arguments
		if(this.args)
			$.extend(args, this.args)

		if(this.get_args) {
			$.extend(args, this.get_args(opts));
		}
		return args;		
	},
	render_results: function(r) {
		if(this.start==0) this.clear();
		
		this.$w.find('.btn-more').toggle(false);

		if(r.message) r.values = r.message;

		if(r.values && r.values.length) {
			this.data = this.data.concat(r.values);
			this.render_list(r.values);
			this.update_paging(r.values);
		} else {
			if(this.start==0) {
				this.$w.find('.result').toggle(false);
				this.$w.find('.no-result').toggle(true);
			}
		}
		
		// callbacks
		if(this.callback) this.callback(r);
	},

	render_list: function(values) {		
		var m = Math.min(values.length, this.page_length);
		
		// render the rows
		for(var i=0; i < m; i++) {
			this.render_row(this.add_row(), values[i], this, i);
		}
	},
	update_paging: function(values) {
		if(values.length >= this.page_length) {
			this.$w.find('.btn-more').toggle(true);			
			this.start += this.page_length;
		}
	},
	add_row: function() {
		return $('<div class="list-row">').appendTo(this.$w.find('.result-list')).get(0);
	},
	refresh: function() { 
		this.run(); 
	},
	add_limits: function() {
		this.query += ' LIMIT ' + this.start + ',' + (this.page_length+1);
	}
});

wn.ui.FilterList = Class.extend({
	init: function(opts) {
		$.extend(this, opts);
		this.filters = [];
		this.$w = this.$parent;
		this.set_events();
	},
	set_events: function() {
		var me = this;
		// show filters
		this.$w.find('.add-filter-btn').bind('click', function() {
			me.add_filter();
		});
			
	},
	
	show_filters: function() {
		this.$w.find('.show_filters').toggle();
		if(!this.filters.length)
			this.add_filter();
	},
	
	add_filter: function(fieldname, condition, value) {
		this.filters.push(new wn.ui.Filter({
			flist: this,
			fieldname: fieldname,
			condition: condition,
			value: value
		}));
		
		// list must be expanded
		if(fieldname) {
			this.$w.find('.show_filters').toggle(true);
		}
	},
	
	get_filters: function() {
		// get filter values as dict
		var values = [];
		$.each(this.filters, function(i, f) {
			if(f.field)
				values.push(f.get_value());
		})
		return values;
	},
	
	// remove hidden filters
	update_filters: function() {
		var fl = [];
		$.each(this.filters, function(i, f) {
			if(f.field) fl.push(f);
		})
		this.filters = fl;
	},
	
	get_filter: function(fieldname) {
		for(var i in this.filters) {
			if(this.filters[i].field.docfield.fieldname==fieldname)
				return this.filters[i];
		}
	}
});

wn.ui.Filter = Class.extend({
	init: function(opts) {
		$.extend(this, opts);

		this.doctype = this.flist.doctype;
		this.make();
		this.make_select();
		this.set_events();
	},
	make: function() {
		this.flist.$w.find('.filter_area').append('<div class="list_filter">\
		<span class="fieldname_select_area"></span>\
		<select class="condition">\
			<option value="=">Equals</option>\
			<option value="like">Like</option>\
			<option value=">=">Greater or equals</option>\
			<option value="<=">Less or equals</option>\
			<option value=">">Greater than</option>\
			<option value="<">Less than</option>\
			<option value="in">In</option>\
			<option value="!=">Not equals</option>\
		</select>\
		<span class="filter_field"></span>\
		<a class="close">&times;</a>\
		</div>');
		this.$w = this.flist.$w.find('.list_filter:last-child');
	},
	make_select: function() {
		this.fieldselect = new wn.ui.FieldSelect(this.$w.find('.fieldname_select_area'), 
			this.doctype, this.filter_fields);
	},
	set_events: function() {
		var me = this;
		
		// render fields		
		this.fieldselect.$select.bind('change', function() {
			me.set_field(this.value);
		});

		this.$w.find('a.close').bind('click', function() { 
			me.$w.css('display','none');
			var value = me.field.get();
			me.field = null;
			if(!me.flist.get_filters().length) {
				me.flist.$w.find('.set_filters').toggle(true);
				me.flist.$w.find('.show_filters').toggle(false);
			}
			if(value) {
				me.flist.listobj.run();
			}
			me.flist.update_filters();
			return false;
		});

		// add help for "in" codition
		me.$w.find('.condition').change(function() {
			if($(this).val()=='in') {
				me.set_field(me.field.docfield.fieldname, 'Data');
				me.field.help_block('values separated by comma');
			} else {
				me.set_field(me.field.docfield.fieldname);				
			}
		});
		
		// set the field
		if(me.fieldname) {
			// presents given (could be via tags!)
			this.set_values(me.fieldname, me.condition, me.value);
		} else {
			me.set_field('name');
		}	

	},
	
	set_values: function(fieldname, condition, value) {
		// presents given (could be via tags!)
		this.set_field(fieldname);
		if(condition) this.$w.find('.condition').val(condition).change();
		if(value) this.field.set(value)
		
	},
	
	set_field: function(fieldname, fieldtype) {
		var me = this;
		
		// set in fieldname (again)
		var cur = me.field ? {
			fieldname: me.field.docfield.fieldname,
			fieldtype: me.field.docfield.fieldtype
		} : {}

		var df = me.fieldselect.fields_by_name[fieldname];
		if(!df) {
			console.log('Filter: unable to select ' + fieldname);
		}
		this.set_fieldtype(df, fieldtype);
			
		// called when condition is changed, 
		// don't change if all is well
		if(me.field && cur.fieldname == fieldname && df.fieldtype == cur.fieldtype) {
			return;
		}
		
		// clear field area and make field
		me.fieldselect.$select.val(fieldname);
		var field_area = me.$w.find('.filter_field').empty().get(0);
		f = wn.ui.make_control({docfield: df, parent:field_area, no_label: true});		
		f.docfield.single_select = 1;
		me.field = f;
		me.field.$w.css('float','left');
		me.field.$input.addClass('input-medium');
		
		this.set_default_condition(df, fieldtype);
		
		$(me.field.$w).find(':input').keydown(function(ev) {
			if(ev.which==13) {
				me.flist.listobj.run();
			}
		})
	},
	
	set_fieldtype: function(df, fieldtype) {
		// reset
		if(df.original_type)
			df.fieldtype = df.original_type;
		else
			df.original_type = df.fieldtype;
			
		df.description = ''; df.reqd = 0;
		
		// given
		if(fieldtype) {
			df.fieldtype = fieldtype;
			return;
		} 
		
		// scrub
		if(df.fieldtype=='Check') {
			df.fieldtype='Select';
			df.options='No\nYes';
		} else if(['Text','Text Editor','Code','Link'].indexOf(df.fieldtype)!=-1) {
			df.fieldtype = 'Data';				
		}
	},
	
	set_default_condition: function(df, fieldtype) {
		if(!fieldtype) {
			// set as "like" for data fields
			if(df.fieldtype=='Data') {
				this.$w.find('.condition').val('like');
			} else {
				this.$w.find('.condition').val('=');
			}			
		}		
	},
	
	get_value: function() {
		var me = this;
		var val = me.field.get();
		var cond = me.$w.find('.condition').val();
		
		if(me.field.docfield.original_type == 'Check') {
			val = (val=='Yes' ? 1 :0);
		}
		
		if(cond=='like') {
			val = val + '%';
		}
		
		return [me.fieldselect.$select.find('option:selected').attr('table'), 
			me.field.docfield.fieldname, me.$w.find('.condition').val(), val==null ? '' : val];
	}

});

// <select> widget with all fields of a doctype as options
wn.ui.FieldSelect = Class.extend({
	init: function(parent, doctype, filter_fields, with_blank) {
		this.doctype = doctype;
		this.fields_by_name = {};
		this.with_blank = with_blank;
		this.$select = $('<select>').appendTo(parent);
		if(filter_fields) {
			for(var i in filter_fields)
				this.add_field_option(this.filter_fields[i])
		} else {
			this.build_options();
		}
	},
	build_options: function() {
		var me = this;
		me.table_fields = [];
		var std_filters = [
			{fieldname:'name', fieldtype:'Data', label:'ID', parent:me.doctype},
			{fieldname:'modified', fieldtype:'Date', label:'Last Modified', parent:me.doctype},
			{fieldname:'owner', fieldtype:'Data', label:'Created By', parent:me.doctype},
			{fieldname:'creation', fieldtype:'Date', label:'Created On', parent:me.doctype},
			{fieldname:'_user_tags', fieldtype:'Data', label:'Tags', parent:me.doctype}
		];
		
		// blank
		if(this.with_blank) {
			this.$select.append($('<option>', {
				value: ''
			}).text(''));
		}

		// main table
		$.each(std_filters.concat(wn.model.get('DocType', me.doctype).get({doctype:'DocField'})), 
			function(i, df) {
				me.add_field_option(df);
			});

		// child tables
		$.each(me.table_fields, function(i,table_df) {
			if(table_df.options) {
				$.each(wn.model.get('DocType', table_df.options).get({doctype:'DocField'}), 
				function(i, df) {
					me.add_field_option(df);
				});
			}
		});
	},

	add_field_option: function(df) {
		var me = this;
		if(me.doctype && df.parent==me.doctype) {
			var label = df.label;
			var table = me.doctype;
			if(df.fieldtype=='Table') me.table_fields.push(df);					
		} else {
			var label = df.label + ' (' + df.parent + ')';
			var table = df.parent;
		}
		if(!_.contains(wn.model.no_value_type, df.fieldtype) && 
			!me.fields_by_name[df.fieldname]) {
			this.$select.append($('<option>', {
				value: df.fieldname,
				table: table
			}).text(label));
			me.fields_by_name[df.fieldname] = df;						
		}
	}
})