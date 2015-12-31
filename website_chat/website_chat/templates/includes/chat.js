
// check agent status

var chat = {};
chat.gravatars = {};
chat.chats = {};

frappe.ready(function() {
	chat.$sidebar = $(".page-sidebar").html('<div class="sidebar-item"></div>');
	chat.$messages = $(".chat-messages");
	chat.set_agent_status();
	chat.bind_events();
	if(getCookie("user_id")) {
		$("#client-email").val(getCookie("user_id"))
	}
	if(getCookie("full_name")) {
		$("#client-name").val(getCookie("full_name"))
	}
	frappe.require("/assets/frappe/js/lib/md5.min.js");

	if(Notification) {
		if(Notification.permission!=="granted") {
			if(Notification.permission!=="denied") {
				Notification.requestPermission(function(permission) {
					Notification.permission = permission;
				})
			}
		}
	}
});

chat.bind_events = function() {
	chat.welcome();
	chat.send_message();
	chat.setup_feedback();
	chat.setup_end_chat();
	chat.setup_agent_status();
	setTimeout(chat.sync, 2000);
}

chat.sound = new Audio("/assets/website_chat/ding.mp3");

chat.set_agent_status = function() {
	$.ajax({
		url:"api/method/website_chat.templates.pages.chat.get_agent_status",
		statusCode: {
			200: function(data) {
				data = data.message;
				if(data.active_sessions) {
					chat.sender = "Agent";
					chat.sender_id = getCookie("user_id");
					chat.set_sessions(data.active_sessions);
					chat.my_status = data.my_status;
					chat.set_agent_status_btn();
				} else {
					chat.agent_status = data.agent_status;
					chat.sender = "Client";
					if(data.agent_status=="active") {
						$(".chat-status").html('<div class="alert alert-success">\
							Agents online. Please enter your name and email to start a session.</div>')
					} else {
						$(".chat-status").html('<div class="alert alert-warning">\
							Agents offline. Please enter your name, email and question. \
								Our agents will get back to you as soon as possible.</div>')
					}
				}
			}
		}
	})
}

chat.welcome = function() {
	$("#chat-start").on("click", function() {
		var name = $("#client-name").val();
		var email = $("#client-email").val();
		var question = $("#client-question").val();
		if(name && email && question) {
			$.ajax({
				type:"POST",
				url: "api/resource/Website Chat Sesssion",
				data: {
					doclist: JSON.stringify([
						{
							"doctype":"Website Chat Session",
							"client_name": name,
							"client_email_id": email,
							"client_question": question,
							"status": (chat.agent_status==="active" ? "New" : "Lost")
						}
					])
				},
				statusCode: {
					200: function(data) {
						if(chat.agent_status==="active") {
							chat.chatid = data.doclist[0].name;
							chat.chat_session = data.doclist[0];
							chat.client_name = name,
							chat.sender_id = email,
							chat.start();
							chat.add_message({
								sender: "Client",
								message: question,
								name: ""
							})
						} else {
							$(".page-content").html('<div class="alert alert-success">\
								Thank you for your message, we will get back to you \
								as soon as possible.</div>');
						}
					}
				}
			})
		} else {
			frappe.msgprint("All fields are required!")
		}
		return false;
	});
	
}

chat.start = function() {
	$("[data-chatid]").removeClass("active");
	$("[data-chatid='"+chat.chatid+"']").addClass("active");
	$(".chat-welcome, .end-chat").addClass("hide");
	$(".chat-sessions").removeClass("hide");
	chat.$messages.empty();
	chat.message_ids = [];
	$(".btn-end-chat").prop("disabled", false);
	$("#chat-input").prop("disabled", false).focus();
	if(!$(".btn-end-chat").length) {
		$('<button class="pull-right btn btn-primary btn-end-chat">End Chat</button>').
			prependTo(".page-header .container:first").
			on("click", function() {
				$(this).prop("disabled", true);
				$.ajax({
					url:"/api/method/website_chat.templates.pages.chat.end_chat",
					type:"POST",
					data: {chatid: chat.chatid}
				});
			});
	}
}


chat.send_message = function(chatid, question) {
	$("#chat-send-message").on("click", function() {
		var message = $("#chat-input").val();
		if(message) {
			$.ajax({
				type:"POST",
				url: "api/resource/Website Chat Message",
				data: {
					doclist: JSON.stringify([
						{
							"doctype":"Website Chat Message",
							"parent": chat.chatid,
							"parenttype": "Website Chat Session",
							"parentfield": "website_chat_messages",
							"message": message,
							"owner": chat.sender_id,
							"sender": chat.sender || "Client"
						}
					])
				},
				statusCode: {
					200: function(data) {
						chat.add_message(data.doclist[0]);
					}
				}
			})
		}
	})
}


chat.get_gravatar = function(email_id) {
	if(!chat.gravatars[email_id]) {
		chat.gravatars[email_id] = "https://secure.gravatar.com/avatar/" + md5(email_id)
	}
	return chat.gravatars[email_id];
}
chat.add_message = function(message, no_animation) {
	if(message.name) {
		if(chat.message_ids.indexOf(message.name)!==-1) {
			// duplicate
			return;
		}
		chat.message_ids.push(message.name);
	}
	if(!message.owner) {
		message.owner = chat.chat_session.client_email_id;
	}
	if(message.sender==="Client") {
		message.alert_class = "warning";
		message.avatar = chat.get_gravatar(chat.chat_session.client_email_id);
	} else {
		message.alert_class = "info";
		message.avatar = chat.get_gravatar(message.owner);
	}
	message.time = comment_when(message.creation || new Date());

	var div = $(repl('<div class="chat-message alert alert-%(alert_class)s media">\
		<a class="pull-left">\
			<img class="media-object" src="%(avatar)s" style="width: 32px; border-radius: 4px;">\
		</a>\
	    <div class="media-body">\
			%(message)s\
			<p class="text-muted small">%(time)s</p>\
		</div>\
	</div>', message)).appendTo(chat.$messages);
	
	if(no_animation) {
		chat.$messages.scrollTop(chat.$messages[0].scrollHeight);
	} else {
		chat.$messages.animate({ scrollTop: chat.$messages[0].scrollHeight}, 1000);
	}
	
	$("#chat-input").val("").focus();
	chat.last_message_id = message.name;
	
	chat.notify("New Message: " + message.message);
}


chat.set_sync_timeout = function() {
	if(!chat.timeout) {
		chat.timeout = setTimeout(function() { chat.sync() }, 3000);
	}
}

chat.sync = function() {
	chat.timeout = false;
	if(frappe.get_pathname()!=="chat" 
		|| (!chat.sender)
		|| (chat.chat_session && chat.chat_session.status === "Ended" && chat.sender==="Client")
		|| (!chat.chatid && chat.sender==="Client"))  {
			chat.set_sync_timeout();
			return;
	}
	$.ajax({
		url:"/api/method/website_chat.templates.pages.chat.get_latest",
		data: {
			chatid: chat.chatid || "no-chat",
			last_message_id: chat.last_message_id || "",
			sender: chat.sender
		},
		statusCode: {
			200: function(data) {
				data = data.message;
				
				if(data.status==="Ended") {
					chat.end_chat();
				}
				
				$.each(data.messages || [], function(i, d) {
					chat.add_message(d);
				});
				
				if(chat.sender==="Agent") {
					chat.set_sessions(data.active_sessions);
				}
			}
		}
	}).always(function() {
		chat.set_sync_timeout();
	});
}

chat.sync_messages = function() {
	chat.$messages.html('<div class="alert alert-info">Loading...</div>')
	$.ajax({
		url:"api/resource/Website Chat Session/" + chat.chatid,
		statusCode: {
			200: function(data) {
				chat.$messages.empty();
				chat.chat_session = data.doclist[0];
				if(chat.sender==="Agent") {
					$(".chatting-with").html(repl("Client: %(client_name)s (%(client_email_id)s)",
						chat.chat_session));
				}
				chat.add_message({
					sender:"Client",
					message: chat.chat_session.client_question,
					name:""
				}, true);
				$.each(data.doclist, function(i, d) {
					if(d.doctype==="Website Chat Message") {
						chat.add_message(d, true);
					}
				});
			}
		}
	});
}

chat.set_sessions = function(active_sessions) {
	chat.$sidebar.empty();
	
	if(active_sessions.length) {
		$.each(active_sessions, function(i, d) {
			var $item = $('<div class="sidebar-item"></div>').appendTo(chat.$sidebar);
			var $a = $('<a>'+d.client_name+'</a>')
				.appendTo($item)
				.attr("data-chatid", d.name)
			if(d.name===chat.chatid) {
				$a.addClass("active");
			} else {
				$a.on("click", function() {
					chat.chatid = $(this).attr("data-chatid");
					chat.start();
					chat.sync_messages();
				});
			}
			if(d.status==="New") {
				if(!chat.chats[d.name]) {
					chat.notify("New Chat: " + d.client_name + " > " + d.question);
				}
				$a.css({"color": "green"});
			}
			if(d.status==="Waiting" || d.status==="New") {
				$a.html(d.client_name + ' <i class="icon-volume-up blink text-danger"></i>');
			}
			
			chat.chats[d.name] = d;
		});
	
		// start latest
		if(!chat.chatid) {
			chat.chatid = active_sessions[0].name;
			chat.start();
			chat.sync_messages();
		}
	} else {
		var $item = $('<div class="sidebar-item">No Active Sessions</div>')
			.appendTo(chat.$sidebar);
		$(".chat-welcome").addClass("hide");
	}
}

chat.setup_agent_status = function() {
	$(".btn-agent-status").on("click", function() {
		$.ajax({
			url:"/api/method/website_chat.templates.pages.chat.set_agent_status",
			type: "POST",
			data: {
				my_status: chat.my_status
			},
			statusCode: {
				200: function(data) {
					chat.my_status = data.message;
					chat.set_agent_status_btn();
				}
			}
		})
	})
}

chat.set_agent_status_btn = function() {
	$(".btn-agent-status").removeClass("hide");
	if(chat.my_status==="Active") {
		$(".btn-agent-status").html("Go Offline").
			removeClass("btn-default").addClass("btn-success");
	} else {
		$(".btn-agent-status").html("Go Online").
			removeClass("btn-success").addClass("btn-default");
	}
}

chat.setup_end_chat = function() {
	$(".btn-end-chat")
		.on("click", function() {
			$(this).prop("disabled", true);
			$.ajax({
				url:"/api/method/website_chat.templates.pages.chat.end_chat",
				type:"POST",
				data: {chatid: chat.chatid}
			});
		});
}

chat.end_chat = function() {
	$(".end-chat").removeClass("hide");
	$("#chat-input").prop("disabled", true);
	$(".chat-feedback")
		.toggle(chat.sender==="Client")
	chat.chat_session.status="Ended";
}


chat.setup_feedback = function() {
	$(".chat-feedback").val("0").on("change", function() {
		var feedback = parseInt($(this).val());
		$.ajax({
			url:"/api/method/website_chat.templates.pages.chat.set_feedback",
			type:"POST",
			data: {
				chatid: chat.chatid,
				feedback: $(this).val()
			},
			statusCode: {
				200: function(data) {
					if(feedback < 3) {
						frappe.msgprint("Thank you for leaving feedback. Sorry this session did not work for you. We will get back to you as soon as possible.");
					} else if(feedback < 5) {
						frappe.msgprint("Thank you for leaving feedback. We will review this session and see where we can improve.");
					} else {
						frappe.msgprint("Thank you for leaving feedback! This will help us keep going.");
					}
					$(".chat-feedback").remove();
				}
			}
		})
	});	
}

chat.notify = function(message) {
	if(!document.hasFocus()) {
		 if(Notification.permission==="granted") {
			new Notification(message);
		 }
		 chat.sound.play();
		 chat.sound.currentTime = 0;
	}
}