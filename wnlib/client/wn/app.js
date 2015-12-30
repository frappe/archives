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

wn.Application = Class.extend({
	init: function() {
		var me = this;
		if(window.app) {
			wn.call({
				method: 'wn.app.startup',
				callback: function(r, rt) {
					wn.provide('wn.boot');
					wn.boot = r.boot;
					if(wn.boot.profile.name=='Guest') {
						window.location = 'index.html';
						return;
					}
					me.startup();
				}
			})
		} else {
			// clear sid cookie
			//document.cookie = "sid=Guest;expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/"
			this.startup();
		}
	},
	startup: function() {
		// load boot info
		this.load_bootinfo();

		// page container
		this.make_page_container();

		// favicon
		this.set_favicon();

		// trigger app startup
		$(document).trigger('startup');
		
		if(wn.boot) {
			// route to home page
			wn.route();	
		}
				
		$(document).trigger('app_ready');
	},
	load_bootinfo: function() {
		if(wn.boot) {
			//wn.model.sync(wn.boot.docs);
			this.set_globals();	
		} else {
			this.set_as_guest();
		}
	},
	set_globals: function() {
		// for backward compatibility
		user = wn.boot.profile.name;
	},
	set_as_guest: function() {
		// for backward compatibility
		user = 'Guest';
	},
	make_page_container: function() {
		wn.container = new wn.views.Container();
	},
	logout: function() {
		var me = this;
		me.logged_out = true;
		wn.call({
			method:'logout',
			callback: function(r) {
				if(r.exc) {
					console.log(r.exc);
				}
				me.redirect_to_login();
			}
		})
	},
	redirect_to_login: function() {
		window.location.href = 'index.html';
	},
	set_favicon: function() {
		var link = $('link[type="image/x-icon"]').remove().attr("href");
		var favicon ='\
			<link rel="shortcut icon" href="' + link + '" type="image/x-icon"> \
			<link rel="icon" href="' + link + '" type="image/x-icon">'

		$(favicon).appendTo('head');
	}
});


// route urls to their virtual pages

// re-route map (for rename)
wn.re_route = {
	
}
wn.route = function() {
	if(wn.re_route[window.location.hash]) {
		window.location.hash = wn.re_route[window.location.hash];
	}

	wn._cur_route = window.location.hash;

	var page_name = wn.get_route_str();
	
	if(wn.contents[page_name]) {  // loaded
		wn.container.change_to(page_name);
		return;
	}
	
	var route = wn.get_route();	
	
	if(!route[0]) route[0] = wn.boot && wn.boot.home_page || 'Explorer';
 	
	switch (route[0]) {
		case "List":
			wn.views.doclistview.show(route[1]);
			break;
		case "Form":
			if(route.length>3) {
				route[2] = route.splice(2).join('/');
			}
			wn.views.formview.show(route[1], route[2]);
			break;
		case "Report":
			wn.views.reportview.show();
			break;
		default:
			wn.container.show(route[0])
	}
}

wn.get_route = function(route) {
	// route for web
	if(!wn.boot) {
		return [window.page_name];
	}
	
	// for app
	return $.map(wn.get_route_str(route).split('/'), 
		function(r) { return decodeURIComponent(r); });	
}

wn.get_route_str = function(route) {
	if(!route)
		route = window.location.hash;

	if(route.substr(0,1)=='#') route = route.substr(1);
	if(route.substr(0,1)=='!') route = route.substr(1);
	return route;	
}

wn.set_route = function() {
	route = $.map(arguments, function(a) { return encodeURIComponent(a) }).join('/');
	window.location.hash = route;
	
	// Set favicon (app.js)
	wn.app.set_favicon();
}

wn._cur_route = null;

// misc user functions

wn.user_info = function(uid) {
	var def = {
		'fullname':uid, 
		'image': 'images/lib/ui/no_img_m.gif'
	}
	if(!wn.boot.user_info) return def
	if(!wn.boot.user_info[uid]) return def
	if(!wn.boot.user_info[uid].fullname)
		wn.boot.user_info[uid].fullname = uid;
	if(!wn.boot.user_info[uid].image)
		wn.boot.user_info[uid].image = def.image;
	return wn.boot.user_info[uid];
}

wn.provide('wn.user');

$.extend(wn.user, {
	name: (wn.boot ? wn.boot.profile.name : 'Guest'),
	has_role: function(rl) {
		if(typeof rl=='string') 
			rl = [rl];
		for(var i in rl) {
			if((wn.boot ? wn.boot.profile.roles : ['Guest']).indexOf(rl[i])!=-1)
				return true;
		}
	},
	is_report_manager: function() {
		return wn.user.has_role(['Administrator', 'System Manager', 'Report Manager']);
	}
})

// wn.session_alive is true if user shows mouse movement in 30 seconds

wn.session_alive = true;
$(document).bind('mousemove', function() {
	wn.session_alive = true;
	if(wn.session_alive_timeout) 
		clearTimeout(wn.session_alive_timeout);
	wn.session_alive_timeout = setTimeout('wn.session_alive=false;', 30000);
})

$(window).bind('hashchange', function() {
	if(location.hash==wn._cur_route)
		return;	
	wn.route();
});


/* start the application */
$(document).ready(function() {
	wn.provide('wn.app');
	$.extend(wn.app, new wn.Application());
});