$.extend(cur_frm.cscript, {
	onload_post_render: function(doc) {
		cur_frm.cscript.email_service(doc);
	},
	email_service: function(doc) {
		if(doc.email_service == 'Other') {
			$(cur_frm.fields_dict.server_section.row.wrapper).toggle(true);
		} else {
			$(cur_frm.fields_dict.server_section.row.wrapper).toggle(false);	
		}
	}
});
