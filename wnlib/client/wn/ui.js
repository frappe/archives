// ui widgets

wn.provide('wn.ui');
// opts { width, height, title, fields (like docfields) }

wn.ui.Dialog = Class.extend({
	init: function(opts) {
		$.extend(this, opts);
		this.wrapper = $('<div class="modal hide"></div>');
		this.header = $('<div class="modal-header">\
			<button class="close" data-dismiss="modal">×</button>\
			<h3></h3></div>').appendTo(this.wrapper);
		this.body = $('<div class="modal-body" style="min-height: 100px;"></div>').appendTo(this.wrapper);
		this.footer = $('<div class="modal-footer"></div>').appendTo(this.wrapper);		
		this.display = false;
		this.set_title(this.title);
		this.make_buttons(this.buttons);
		$(this.wrapper).modal();
	},
		
	set_title: function(txt) {
		this.header.find('h3').text(txt);
	},
	
	make_buttons: function(btn_list) {
		var me = this;
		$.each(btn_list, function(i, v) {
			var btn = $('<button class="btn">' + v.label + '</button>')
				.appendTo(me.footer)
				.click(function() { v.click(me); });
			if(i==0) {
				btn.addClass('btn-primary');
			}
		})
	},
		
	/** show the dialog */
	show: function() {
		// already live, do nothing
		if(this.display) return;

		// show it
		$(this.wrapper).modal('show');

		this.display = true;
		wn.ui.cur_dialog = this;

		// call onshow
		if(this.onshow) this.onshow(this);
	},

	hide: function() {
		// call onhide
		if(this.onhide) this.onhide(this);

		// hide
		$(this.wrapper).modal('hide');

		// flags
		this.display = false;
	}
});

wn.ui.msgprint = function(message) {
	if(!wn.ui.msgprint_dialog) {
		wn.ui.msgprint_dialog = new wn.ui.Dialog({
			title: 'Message',
			buttons: [{
				label: 'Ok',
				click: function(dialog) { dialog.hide(); }
			}],
			onhide: function(dialog) {
				dialog.body.empty();				
			}
		});
	}

	var d = wn.ui.msgprint_dialog;
	if(typeof(message)!='string')
		message = JSON.stringify(message);
	
	if(d.body.children().length) {
		d.body.append('<hr>');
	}
	d.body.append(message);
	d.show();
}

var msgprint = wn.ui.msgprint;

// parent, args, callback
wn.upload = {
	make: function(opts) {
		var id = wn.dom.set_unique_id();
		$(opts.parent).append(_.template('<iframe id="<%=id%>" name="<%=id%>" src="blank.html" \
				style="width:0px; height:0px; border:0px"></iframe>\
			<form method="POST" enctype="multipart/form-data" \
				action="<%=action%>" target="<%=id%>">\
				<input type="file" name="filedata" /><br><br>\
				<input type="submit" class="btn btn-small" value="Upload" />\
			</form>', {
				id: id,
				action: wn.request.url
			}));
	
		opts.args.cmd = 'uploadfile';
		opts.args._id = id;
			
		// add request parameters
		for(key in opts.args) {
			if(opts.args[key]) {
				$('<input type="hidden">')
					.attr('name', key)
					.attr('value', opts.args[key])
					.appendTo($(opts.parent).find('form'));				
			}
		}
		
		$('#' + id).get(0).callback = opts.callback
	},
	callback: function(id, file_id, args) {
		$('#' + id).get(0).callback(file_id, args);
	}
}

// options: doctype, callback, query (if applicable)
wn.ui.Search = Class.extend({
	init: function(opts) {
		$.extend(this, opts);
		var me = this;
		wn.model.with_doctype(this.doctype, function(r) {
			me.make();
			me.dialog.show();
			me.list.$w.find('.list-filters input[type="text"]').focus();
		});
	},
	make: function() {
		var me = this;
		this.dialog = new wn.ui.Dialog({
			title: this.doctype + ' Search',
			width: 500
		});
		this.list = new wn.ui.Listing({
			parent: $(this.dialog.body),
			appframe: this.dialog.appframe,
			new_doctype: this.doctype,
			doctype: this.doctype,
			method: 'webnotes.widgets.doclistview.get',
			show_filters: true,
			style: 'compact',
			get_args: function() {
				if(me.query) {
					me.page_length = 50; // there has to be a better way
					return {
						query: me.query
					}
				} else {
					return {
						doctype: me.doctype,
						fields: [ '`tab' + me.doctype + '`.name'],
						filters: me.list.filter_list.get_filters(),
						docstatus: ['0','1']
					}					
				}
			},
			render_row: function(parent, data) {
				$ln = $('<a style="cursor: pointer;" data-name="'+data.name+'">'
					+ data.name +'</a>')
					.appendTo(parent)
					.click(function() {
						var val = $(this).attr('data-name');
						me.dialog.hide(); 
						if(me.callback)
							me.callback(val);
						else 
							wn.set_route('Form', me.doctype, val);
					});
			}
		});
		this.list.filter_list.add_filter('name', 'like');
		this.list.run();
	}
});

// Tree object
// tree with expand on ajax
// constructor: parent, label, method (get children), args

wn.ui.Tree = Class.extend({
	init: function(args) {
		$.extend(this, args);
		this.nodes = {};
		this.$w = $('<div class="tree">').appendTo(this.parent);
		this.rootnode = new wn.ui.TreeNode({
			tree: this, 
			parent: this.$w, 
			label: this.label, 
			expandable: true
		});
		this.set_style();
	},
	set_style: function() {
		wn.dom.set_style("\
			.tree li { list-style: none; }\
			.tree ul { margin-top: 2px; }\
			.tree-link { cursor: pointer; }\
		")
	}
})

wn.ui.TreeNode = Class.extend({
	init: function(args) {
		var me = this;
		$.extend(this, args);
		this.loaded = false;
		this.expanded = false;
		this.tree.nodes[this.label] = this;
		this.$a = $('<a class="tree-link">')
			.click(function() { 
				if(me.expandable && me.tree.method && !me.loaded) {
					me.load()
				} else {
					me.selectnode();
				}
				if(me.tree.click) me.tree.click(this);
			})
			.bind('reload', function() { me.reload(); })
			.data('label', this.label)
			.appendTo(this.parent);
		
		// label with icon
		if(this.expandable) {
			this.$a.append('<i class="icon-folder-close"></i> ' + this.label);
		} else {
			this.$a.append('<i class="icon-file"></i> ' + this.label);
		}
	},
	selectnode: function() {
		// expand children
		if(this.$ul) {
			this.$ul.toggle();
			
			// open close icon
			this.$a.find('i').removeClass();
			if(this.$ul.css('display').toLowerCase()=='block') {
				this.$a.find('i').addClass('icon-folder-open');
			} else {
				this.$a.find('i').addClass('icon-folder-close');				
			}
		}
		
		// select this link
		this.tree.$w.find('a.selected')
			.removeClass('selected');
		this.$a.toggleClass('selected');
		this.expanded = !this.expanded;
	},
	reload: function() {
		if(this.expanded) {
			this.$a.click(); // collapse			
		}
		if(this.$ul) {
			this.$ul.empty();
		}
		this.load();
	},
	addnode: function(label, expandable) {
		if(!this.$ul) {
			this.$ul = $('<ul>').toggle(false).appendTo(this.parent);
		}
		return new wn.ui.TreeNode({
			tree:this.tree, 
			parent: $('<li>').appendTo(this.$ul), 
			label: label, 
			expandable: expandable
		});
	},
	load: function() {
		var me = this;
		args = $.extend(this.tree.args, {
			parent: this.label
		});

		$(me.$a).set_working();

		wn.call({
			method: this.tree.method,
			args: args,
			callback: function(r) {
				$(me.$a).done_working();

				$.each(r.message, function(i, v) {
					node = me.addnode(v.value || v, v.expandable);
					node.$a.data('node-data', v);
				});
				
				me.loaded = true;
				
				// expand
				me.selectnode();
			}
		})
	}	
});