wn.provide('mailnext');

wn.pages['mailbox'].on('load', function() {
	var wrapper = this.wrapper; 
	wrapper.appframe = new wn.ui.AppFrame($(wrapper).find('.appframe-area'));
	wrapper.appframe.add_button('Refresh', function() { 
		// hard refresh - get mails from server
		mailnext.mailbox.run(
			$(mailnext.page).find('.mail-service.selected').data('service-name'), true) 
	}, 'icon-refresh');
	wrapper.appframe.add_button('Settings', function() {
		wn.views.formview.show('Mail Account', wn.boot.profile.name);
	}, 'icon-cog');
	wrapper.appframe.$titlebar.find('.appframe-title').html('Mailbox');
	
	mailnext.page = wrapper;
	mailnext.mailbox = new mailnext.MailBox();
	mailnext.mailbox.setup();
});

mailnext.MailBox = Class.extend({
	init: function() {
		// pass
	},
	setup: function() {
		var me = this;

		this.make_list();
		
		// non service mails
		var s = new mailnext.MailService('Mails');
		s.select();
		
		// service mailbox
		$.each(wn.boot.mail_services, function(i, v) {
			new mailnext.MailService(v)
		});		
	},
	make_list: function() {
		var me = this;
		this.listing = new wn.ui.Listing({
			no_toolbar: true,
			parent: $(mailnext.page).find('.list-area'),
			get_args: function(opts) {
				var args = {
					service_name: $(mailnext.page).find('.mail-service.selected').data('service-name')
				}
				if(opts && opts.hard_refresh) 
					args.hard_refresh = 1;
				return args;
			},
			method:'mail.page.mailbox.mailbox.get_mails',
			render_row: function(parent, data) { me.render_message(parent, data)}
		});
	},
	run: function(service, hard_refresh) {
		$(mailnext.page).find('h2').html(service);
		if(hard_refresh) {
			this.listing.run({
				hard_refresh: true
			});
		} else {
			this.listing.run();
		}
	},
	render_message: function(parent, data) {
		$(_.template('<div><b><%=subject%></b></div><p>From: <%=from%> | <%=date%></p>', data))
			.appendTo(parent);
	}
});

mailnext.MailService = Class.extend({
	init: function(name) {
		this.name = name;
		var me = this;

		this.$link = $(_.template('<a class="mail-service">\
			<%=name%></a>', {name: name}))
			.data('service-name', name)
			.click(function() {
				me.select()
			}).appendTo($('<p>').appendTo($(mailnext.page).find('.layout-side-section')));

	},
	select: function() {
		$(mailnext.page).find('.mail-service.selected').removeClass('selected');
		this.$link.addClass('selected');
		mailnext.mailbox.run(this.name);
	}
})
