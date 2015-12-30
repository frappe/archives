// page container
wn.provide('wn.views');
wn.provide('wn.contents');

wn.views.Container = Class.extend({
	init: function() {
		this.content = null; // current page
	},
	add_page: function(label) {
		return new wn.views.Content(label);
	},
	change_to: function(label) {
		if(this.content && this.content.label == label) {
			return;
		}
		
		this.content && this.content.hide();
		
		if(wn.contents[label]) {
			wn.contents[label].show();
			this.content = wn.contents[label];			
		} else {
			this.show('404');
		}
	},

	show: function(label, callback) {
		var me = this;
		if(wn.contents[label]) {
			me.change_to(label);
			callback && callback();
		} else {
			var fname = '_' + label.replace(/ /g, '_').toLowerCase() + '.html';
			$(me.add_page(label).content).load(fname, function(response, status) {
				if(status=='error') {
					me.show('404');
				} else {
					me.change_to(label); 
					callback && callback();					
				}
			});
		}
	}
});

wn.views.Content = Class.extend({
	init: function(label) {
		this.label = label;
		this.content = $('<div class="content"></div>')
			.attr('id', "page-" + label.replace(/ /g, '_'))
			.appendTo('#page_container').get(0);
		wn.contents[label] = this;
	},
	show: function() {
		$(this.content).toggle(true).fadeIn();
		document.title = this.title || this.label;
		scroll(0,0);
	},
	hide: function() {
		$(this.content).toggle(false).trigger('hide');
	}
});

// Frame Content: to be embedded inside Content
// --------------------------------------------
// title
// parent
// single_column (if no sidebar)

wn.views.FrameContent = Class.extend({
	init: function(opts) {
		$.extend(this, opts);
		this.make_layout(opts);
		this.make_title_bar(opts);
	},
	make_layout: function(opts) {
		this.$content = $(this.wrapper);
		if(this.single_column) {
			this.$content.html('<div class="layout-wrapper">\
				<div class="layout-head"></div>\
				<div class="layout-pane layout-main"></div>\
			</div>');
			this.$main = this.$content.find('.layout-main');		
		} else {
			this.$content.html('<div class="layout-wrapper">\
				<div class="layout-head"></div>\
				<div class="row">\
					<div class="span9">\
						<div class="layout-pane layout-main"></div>\
					</div>\
					<div class="span3">\
						<div class="layout-pane"></div>\
					</div>\
				</div>\
				<div class="clear"></div>\
			</div>');		
			this.$main = this.$content.find('.layout-main');
			this.$side = this.$content.find('.layout-pane:last');
		}
	},
	make_title_bar: function(opts) {
		this.buttons = {};		
		this.$titlebar = $('<div class="frame-titlebar frame-titlebar-gradient">\
			<div class="frame-title"></span>\
			<span class="close">&times;</span>\
		</div>').appendTo(this.$content.find('.layout-head'));

		this.$titlebar.find('.close').click(function() {
			window.history.back();
		})
		
		this.set_title(this.title || this.label);
	},
	set_title: function(txt) {
		this.$titlebar.find('.frame-title').html(txt);
	},
	add_button: function(label, click, icon) {
		if(!this.$toolbar)
			this.$toolbar = $('<div class="frame-toolbar"></div>').insertAfter(this.$titlebar);

		args = { label: label, icon:'' };
		if(icon) {
			args.icon = '<i class="'+icon+'"></i>';
		}
		this.buttons[label] = $(_.template('<button class="btn btn-small">\
			<%=icon%> <%=label%></button>', args))
			.click(click)
			.appendTo(this.$toolbar);
		return this.buttons[label];
	},
	clear_buttons: function() {
		this.$toolbar && this.$toolbar.empty();
	}	
})