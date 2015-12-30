// Explorer widget
//  - page
//  - title
//  - doctype_list
wn.views.Explorer = wn.views.FrameContent.extend({
	init: function(opts) {
		var me = this;
		this._super({
			title: opts.title,
			wrapper: opts.page.content
		});
		this.make_doctype_list(opts.doctype_list);
	},
	make_doctype_list: function(doctype_list) {
		var me = this;
		$ul = $('<ul>').appendTo(this.$side);
		$.each(doctype_list, function(i, v) {
			$a = $('<a>')
				.text(v)
				.css('cursor', 'pointer')
				.data('doctype', v)
				.click(function() {
					me.show($(this).data('doctype'));
					return false;
				}).appendTo($('<li>').appendTo($ul));
		});
	},
	show: function(doctype) {
		$(this.$main).empty();
		$('<h1>').text(doctype).appendTo(this.$main);
		this.$loading = $('<div class="help">Loading...</div>').appendTo(this.$main);
	}
});