var user=null;
var treemapper = {};
var sid = null;

$(document).ready(function() {
	if(!wn.get_sid())
		$("[data-label='Add A Tree']").toggle(false);
});

treemapper = {
	current_step: "1",
	markers: [],
	render: function(start_y, start_x) {
		treemapper.map = L.map('map').setView([start_y, start_x], 13);

		L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
			maxZoom: 18,
			attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
		}).addTo(treemapper.map);
		
		treemapper.show_tree_markers();
		treemapper.map.on("zoomend", treemapper.show_tree_markers);
		treemapper.map.on("dragend", treemapper.show_tree_markers);
	},
	show_tree_markers: function() {
		// clear existing
		$.each(treemapper.markers, function(i, marker) {
			treemapper.map.removeLayer(marker);
		});
		treemapper.makers = [];

		var bounds = treemapper.map.getBounds();
		wn.call({
			method: "treemapper.doctype.tree.tree.get_trees",
			args: {
				north: bounds.getNorth(),
				south: bounds.getSouth(),
				east: bounds.getEast(),
				west: bounds.getWest()
			},
			callback: function(r) {
				$.each(r.message || [], function(i, tree) {
					treemapper.markers.push(L.marker([tree.latitude, tree.longitude]).addTo(treemapper.map)
						.bindPopup(repl("<b>%(tree_species)s</b><br />%(address_display)s", tree)));
				})
				
			}
		})
	},
	show_step: function(n) {
		if(treemapper.current_step) {
			$(".step-" + treemapper.current_step).toggle(false);
		}
		treemapper.current_step = n;
		$(".step-" + treemapper.current_step).toggle(true);
		
		$(".progress-bar").css("width", ((parseInt(n)-1) * 100 / 4) + "%")
		
		scroll(0, 0);
	},
	setup_login: function() {
		$(".splash").toggle(true);
		$(".btn-login").click(function() {
			window.location.href = "login";
		});
	},
	show_add: function() {
		$(".splash").toggle(false);
		treemapper.get_location("Checking location services on your device...", function() {
				$(".add-tree").toggle(true);
		});
	},
	get_form_values: function(id) {
		var form = {};
		$.each($("#"+id).serializeArray(), function(i, obj) {
			form[obj.name] = obj.value;
		});
		return form;
	},
	get_location: function(message, callback) {
		NProgress.start();
		try {
			wn.show_message(message, "icon-map-marker icon-spin");
			navigator.geolocation.getCurrentPosition(function(pos) {
				NProgress.done();
				if(pos) {
					callback(pos);
					wn.hide_message();
				} else {
					treemapper.no_location();
				}
			});
		} catch(e) {
			console.log(e);
			NProgress.done();
			wn.hide_message();
			treemapper.no_location();
		}
	},
	no_location: function() {
		wn.show_message("Please use a device with GPS and allow your browser to capture your location.", 
			"icon-warning-sign")
	},
	resize_image: function(reader, callback) {
		var tempImg = new Image();
		tempImg.src = reader.result;
		
		tempImg.onload = function() {
			var MAX_WIDTH = 400;
			var MAX_HEIGHT = 300;
			var tempW = tempImg.width;
			var tempH = tempImg.height;
			if (tempW > tempH) {
				if (tempW > MAX_WIDTH) {
				   tempH *= MAX_WIDTH / tempW;
				   tempW = MAX_WIDTH;
				}
			} else {
				if (tempH > MAX_HEIGHT) {
				   tempW *= MAX_HEIGHT / tempH;
				   tempH = MAX_HEIGHT;
				}
			}

			var canvas = document.createElement('canvas');
			canvas.width = tempW;
			canvas.height = tempH;
			var ctx = canvas.getContext("2d");
			ctx.drawImage(this, 0, 0, tempW, tempH);
			var dataURL = canvas.toDataURL("image/jpeg");
			callback(dataURL);
		}
	}
};