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


/* Simple JavaScript Inheritance
 * By John Resig http://ejohn.org/
 * MIT Licensed.
 */
// Inspired by base2 and Prototype

(function(){
	var initializing = false, fnTest = /xyz/.test(function(){xyz;}) ? /\b_super\b/ : /.*/;
	// The base Class implementation (does nothing)
	this.Class = function(){};
	
	// Create a new Class that inherits from this class
	Class.extend = function(prop) {
		var _super = this.prototype;
		
		// Instantiate a base class (but only create the instance,
		// don't run the init constructor)
		initializing = true;
		var prototype = new this();
		initializing = false;
		
		// Copy the properties over onto the new prototype
		for (var name in prop) {
			// Check if we're overwriting an existing function
			prototype[name] = typeof prop[name] == "function" && 
				typeof _super[name] == "function" && fnTest.test(prop[name]) ?
				(function(name, fn){
					return function() {
						var tmp = this._super;
						
						// Add a new ._super() method that is the same method
						// but on the super-class
						this._super = _super[name];
						
						// The method only need to be bound temporarily, so we
						// remove it when we're done executing
						var ret = fn.apply(this, arguments);				
						this._super = tmp;
						
						return ret;
					};
				})(name, prop[name]) :
				prop[name];
		}
		
		// The dummy class constructor
		function Class() {
			// All construction is actually done in the init method
			if ( !initializing && this.init )
				this.init.apply(this, arguments);
		}
		
		// Populate our constructed prototype object
		Class.prototype = prototype;
		
		// Enforce the constructor to be what we expect
		Class.prototype.constructor = Class;

		// add bindable events
		Class.prototype._observers = {};
		Class.prototype.on = function(event_name, handle) {
			if(!this._observers[event_name]) {
				this._observers[event_name] = [];
			}
			_.get_or_set(this._observers, event_name, []).push(handle);
		}
		Class.prototype.trigger = function(event_name) {
			var args = [];
			if(arguments.lengths > 1) args = arguments.splice(1);
			var observer_list = this._observers[event_name] || [];
			for(var i=0;i< observer_list.length; i++) {
				observer_list[i].apply(this, args);
			}
		}

		// And make this class extendable
		Class.extend = arguments.callee;
		
		return Class;
	};
})();

// create namespace
// usage: wn.provide('a.b.c');
if(!window.wn)wn = {}
wn.provide = function(namespace) {
	var nsl = namespace.split('.');
	var l = nsl.length;
	var parent = window;
	for(var i=0; i<l; i++) {
		var n = nsl[i];
		if(!parent[n]) {
			parent[n] = {}
		}
		parent = parent[n];
	}
}

// make console for IE
if(!window.console) { var console = { log: function(txt) { } }; };

// misc utilities
wn.utils = {
	id_count: 0,
	by_id: function(id) {
		return document.getElementById(id);
	},
	set_unique_id: function(ele) {
		var id = 'unique-' + wn.dom.id_count;
		if(ele)
			ele.setAttribute('id', id);
		wn.dom.id_count++;
		return id;
	},
	eval: function(txt) {
		if(!txt) return;
		var el = document.createElement('script');
		el.appendChild(document.createTextNode(txt));
		// execute the script globally
		document.getElementsByTagName('head')[0].appendChild(el);
	},
	set_style: function(txt) {
		if(!txt) return;
		var se = document.createElement('style');
		se.type = "text/css";
		if (se.styleSheet) {
			se.styleSheet.cssText = txt;
		} else {
			se.appendChild(document.createTextNode(txt));
		}
		document.getElementsByTagName('head')[0].appendChild(se);	
	},
	set_box_shadow: function(ele, spread) {
		$(ele).css('-moz-box-shadow', '0px 0px '+ spread +'px rgba(0,0,0,0.3);')
		$(ele).css('-webkit-box-shadow', '0px 0px '+ spread +'px rgba(0,0,0,0.3);')
		$(ele).css('-box-shadow', '0px 0px '+ spread +'px rgba(0,0,0,0.3);')

	},	
	image_placeholder: function(dim, txt) {
		function getsinglecol() {
			return Math.min(Math.round(Math.random() * 9) * Math.round(Math.random() * 1) + 3, 9)
		}
		function getcol() {
			return '' + getsinglecol() + getsinglecol() + getsinglecol();
		}
		args = {
			width: Math.round(flt(dim) * 0.7) + 'px',
			height: Math.round(flt(dim) * 0.7) + 'px',
			padding: Math.round(flt(dim) * 0.15) + 'px',
			'font-size': Math.round(flt(dim) * 0.6) + 'px',
			col1: getcol(),
			col2: getcol(),
			letter: letter.substr(0,1).toUpperCase()
		}
		return _.template('<div style="\
			height: <%=height%>; \
			width: <%=width%>; \
			font-size: <%=font-size%>; \
			color: #fff; \
			text-align: center; \
			padding: <%=padding%>; \
			background: -moz-linear-gradient(top,  #<%=col1%> 0%, #<%=col2%> 99%); /* FF3.6+ */\
			background: -webkit-gradient(linear, left top, left bottom, color-stop(0%,#<%=col1%>), color-stop(99%,#<%=col2%>)); /* Chrome,Safari4+ */\
			background: -webkit-linear-gradient(top,  #<%=col1%> 0%,#<%=col2%> 99%); /* Chrome10+,Safari5.1+ */\
			background: -o-linear-gradient(top,  #<%=col1%> 0%,#<%=col2%> 99%); /* Opera 11.10+ */\
			background: -ms-linear-gradient(top,  #<%=col1%> 0%,#<%=col2%> 99%); /* IE10+ */\
			background: linear-gradient(top,  #<%=col1%> 0%,#<%=col2%> 99%); /* W3C */\
			filter: progid:DXImageTransform.Microsoft.gradient( startColorstr=\'#<%=col1%>\', endColorstr=\'#<%=col2%>\',GradientType=0 ); /* IE6-9 */\
			"><%=letter%></div>', args);
	},
	markdown: function(txt) {
		if(!wn.md2html) {
			wn.require('js/lib/utils/showdown.min.js');
			wn.md2html = new Showdown.converter();
		}
		return wn.md2html.makeHtml(txt);
	},
	get_cookie: function(c) {
		var clist = (document.cookie+'').split(';');
		var cookies = {};
		for(var i=0;i<clist.length;i++) {
			var tmp = clist[i].split('=');
			cookies[$.trim(tmp[0])] = $.trim(tmp[1]);
		}
		return cookies[c];
	}
	
};

// jquery extensions
(function($) {
	$.fn.add_options = function(options_list) {
		// create options
		for(var i=0; i<options_list.length; i++) {
			var v = options_list[i];
			value = v.value || v;
			label = v.label || v;
			$('<option>').html(label).attr('value', value).appendTo(this);
		}
		// select the first option
		$(this).val(options_list[0].value || options_list[0]);
	}
	$.fn.set_working = function() {
		var ele = this.get(0);
		$(ele).attr('disabled', 'disabled');
		if(ele.loading_img) { 
			$(ele.loading_img).toggle(true);
		} else {
			ele.loading_img = $('<img src="js/lib/wn/img/button-load.gif" \
				style="margin-left: 4px; margin-bottom: -2px; display: inline;" />')
				.insertAfter(ele);
		}		
	}
	$.fn.done_working = function() {
		var ele = this.get(0);
		$(ele).attr('disabled', null);
		if(typeof ele.loading_img != 'undefined') { 
			$(ele.loading_img).toggle(false); 
		};
	}
})(jQuery);


// underscore extensions
$.extend(_, {
	get_or_set: function(obj, key, val) {
		if(typeof obj[key] === 'undefined')
			obj[key] = val;
		return obj[key];
	}
});

wn.loaded_modules = [];
wn.require = function(items, reload) {
	if(typeof items === "string") {
		items = [items];
	}
	var l = items.length;

	for(var i=0; i< l; i++) {
		var src = items[i];
		if(_.contains(wn.loaded_modules, src)) {
			continue;
		}
		$.ajax({
			url: t,
			data: reload && {
				q: Math.floor(Math.random()*1000)
			},
			dataType: 'text',
			success: function(txt) {
				var extn = src.split('.').splice(-1)[0];
				if(extn=='js') {
					wn.dom.eval(txt);
				} else if(extn=='css') {
					wn.dom.set_style(txt);
				}
				wn.loaded_modules.push(src);
			},
			async: false
		});
	}
}

wn.provide('wn.lib');
wn.lib.import_slickgrid = function() {
	wn.require('js/lib/slickgrid/slick.grid.css');
	wn.require('js/lib/slickgrid/slick-default-theme.css');
	wn.require('js/lib/slickgrid/jquery.event.drag.min.js');
	wn.require('js/lib/slickgrid/slick.core.js');
	wn.require('js/lib/slickgrid/slick.grid.js');
	wn.dom.set_style('.slick-cell { font-size: 12px; }');
};

