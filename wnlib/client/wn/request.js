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

// My HTTP Request

wn.provide('wn.request');
wn.request.url = 'server.cgi';

// call execute serverside request
wn.request.prepare = function(opts) {
	// btn indicator
	if(opts.btn) $(opts.btn).set_working();
	
	// no cmd?
	if(!opts.args._method) {
		console.log(opts)
		throw "No method specified";
	}
}

wn.request.cleanup = function(opts, r) {
	// stop button indicator
	if(opts.btn) $(opts.btn).done_working();

	// session expired?
	if(wn.boot && wn.boot.sid && wn.get_cookie('sid') != wn.boot.sid) { 
		if(!wn.app.logged_out) {
			msgprint('Session Expired. Logging you out');
			wn.app.logout();			
		}
		return;
	}
	
	// show messages
	if(r.messages) $.each(r.messages, function(i, v) { msgprint(v); });
	
	// show errors
	if(r.errors) $.each(r.errors, function(i, v) { console.log(v); });
	
	// 403 (forbidden)
	if(r['403']) {
		wn.container.change_to('403');
	}
}

wn.request.call = function(opts) {
	wn.request.prepare(opts);
	
	$.ajax({
		url: opts.url || wn.request.url,
		data: opts.args,
		type: opts.type || 'POST',
		dataType: opts.dataType || 'json',
		success: function(r, xhr) {
			wn.request.cleanup(opts, r);
			opts.success(r, xhr.responseText);
		},
		error: function(xhr, textStatus) {
			wn.request.cleanup(opts, {});
			msgprint('Unable to complete request: ' + textStatus)
			if(opts.error)opts.error(xhr)
		}
	})
}

// generic server call (call page, object)
wn.call = function(opts) {
	args = {};
	if(typeof opts == 'object') {
		// all arguments passed as dict
		args.args = $.extend({}, opts.args)		
		if(opts.method) {
			args.args._method = opts.method;
		}
		args.success = opts.success || opts.callback;
		args.error = opts.error;
		args.btn = opts.btn;
	} else if(typeof opts=='string') {
		
		// wn.call('method', ..)
		args = {args:{}};
		args.args._method = arguments[0];
		if(typeof arguments[1]=='object') {
			// wn.call('method', {}, success)
			args.args.extend(arguments[1]);
			args.success = arguments[2];
		} else {
			// wn.call('method', success)
			args.success = arguments[1];
		}
	}

	wn.request.call(args);
}

wn.request.get = function(opts) {
	wn.call($.extend(opts, {type:"GET"}));
}

wn.request.post = function(opts) {
	wn.call($.extend(opts, {type:"POST"}));
}
