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

wn.provide('wn.model');
wn.provide('wn.docs');
wn.provide('wn.doclists');

wn.model = {
	no_value_type: ['Section Break', 'Column Break', 'HTML', 'Table', 
 	'Button', 'Image'],

	new_names: {},

	with_doctype: function(doctype, callback) {
		if(wn.model.has('DocType', doctype)) {
			callback();
		} else {
			wn.call({
				method:'webnotes.model.doctype.get',
				args: {
					doctype: doctype
				},
				callback: function(r) {
					wn.model.sync(r.docs);
					callback(r);
				}
			});
		}
	},
	with_doc: function(doctype, name, callback) {
		if(!name) name = doctype; // single type
		if(wn.model.has(doctype, name)) {
			callback(name);
		} else {
			wn.call({
				method:'webnotes.model.doclist.get',
				args: {
					doctype: doctype,
					name: name
				},
				callback: function(r) {
					wn.model.sync(r.docs);
					callback(name, r);
				}
			});
		}
	},
	can_delete: function(doctype) {
		if(!doctype) return false;
		return wn.model.get('DocType', doctype).get('allow_trash') && 
			wn.boot.profile.can_cancel.indexOf(doctype)!=-1;
	},
	sync: function(doclist) {
		for(var i=0, len=doclist.length; i<len; i++) {
			var doc = doclist[i];
			if(doc.parent) {
				var doclistobj = wn.doclists[doc.parenttype][doc.parent];
				doclistobj.add(doc);
			} else {
				new wn.model.DocList([doc]);
			}
		}
	},
	// return doclist
	get: function(dt, dn) {
		return wn.doclists[dt] && wn.doclists[dt][dn];
	},
	has: function(dt, dn) {
		if(wn.doclists[dt] && wn.doclists[dt][dn]) return true;
		else return false;
	},
	get_value: function(dt, dn, fieldname) {
		var doc = wn.model.get(dt, dn);
		if(doc) return doc.get(fieldname);
		else return null;
	},
	set_value: function(dt, dn, fieldname, value) {
		wn.model.get(dt, dn).doc.set(fieldname, value);
	},
	remove: function(dt, dn) {
		delete wn.doclists[dt][dn];
	},
	// naming style for onchange events
	event_name: function(dt, dn) {
		return 'change-'+dt.replace(/ /g, '_')+'-' + dn.replace(/ /g, '_');
	}
}

// document (row) wrapper
wn.model.Document = Class.extend({
	init: function(fields) {
		this.fields = fields;
	},
	get: function(key, ifnull) {
		return this.fields[key] || ifnull;
	},
	set: function(key, val) {
		this.fields[key] = val;
		$(document).trigger(wn.model.event_name(this.get('doctype'), this.get('name')), [key, val]);
	}
});

// doclist (collection) wrapper
wn.model.DocList = Class.extend({
	init: function(doclist) {
		this.doclist = [];
		if(doclist) {
			for(var i=0, len=doclist.length; i<len; i++) {
				this.add(doclist[i]);
			}
		}
	},
	setup: function(doc) {
		// first doc, setup and add to dicts
		this.doc = doc;
		this.doctype = doc.get('doctype');
		this.name = doc.get('name');
		wn.provide('wn.doclists.' + this.doctype);
		wn.doclists[this.doctype][this.name] = this;
	},
	add: function(doc) {
		if(!(doc instanceof wn.model.Document)) {
			var doc = new wn.model.Document(doc);
		}
		this.doclist.push(doc);
		if(this.doclist.length==1) {
			this.setup(doc);
		}
	},
	// usage:
	// doclist.each(doctype, filters, fn)
	// doclist.each(filters/doctype, fn);
	// doclist.each(fn);
	//
	// example:
	// doclist.each({"doctype":"DocField", "fieldtype":"Table"}, function(d) {})
	// doclist.each('DocField', function(d) { })
	each: function() {
		if(typeof arguments[0]=='function') {
			var fn = arguments[0];
			$.each(this.doclist, function(i, doc) { fn(doc); })
		} else if(typeof arguments[1]=='function') {
			var fn = arguments[1];
			if(typeof arguments[0]=='string') {
				$.each(this.get({doctype:arguments[0]}), function(i, doc) { fn(doc); });				
			} else {
				$.each(this.get(arguments[0]), function(i, doc) { fn(doc); });				
			}
		} else {
			var fn = arguments[2];
			$.each(this.get(arguments[0], arguments[1]), function(i, doc) { fn(doc); });
		}
	},
	// usage:
	// doclist.get(doctype, filters) => filtered doclist
	// doclist.get(filters) => filtered doclist
	// doclist.get(fieldname) => value of main doc
	get: function() {
		var me = this;
		if(typeof arguments[0]=='string' && typeof arguments[1]=='object') {
			var filters = arguments[1];
			filters.doctype = arguments[0];
		} else if(typeof arguments[0]=='object') {
			var filters = arguments[0];
		} else {
			return this.doc.get(arguments[0], arguments[1]);
		}
		return $.map(this.doclist, function(d) { return me.match(filters, d) });
	},
	get_value: function(key, def) {
		return this.doc.get(key, def);
	},
	match: function(filters, doc) {
		for(key in filters) {
			if(doc.get(key)!=filters[key]) {
				return null;
			}
		}
		return doc;
	},
	// save doclist
	save: function(docstatus, callback) {
		var me = this;
		wn.call({
			method: 'webnotes.model.doclist.save',
			args: {
				docs: this.doclist
			},
			callback: function(r) {
				// reset the doclist
				delete me.doclist;
				me.doclist = r.docs;
				if(me.doclist[0].get('name')!=me.name) {
					me.rename();
				}
			}
		});
	},
	rename: function() {
		this.name = this.doclist[0].get('name');
	}
});