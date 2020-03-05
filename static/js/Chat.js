var Chat = function() { };

Chat.prototype = {
	refreshTimeout: 2000,
	readyToSend: false,
	readyToGet: true,
	windowVisible: false,
	
	constructor: function() {
		alert(this);
		this.refreshTimeout = 1000;
	},
	
	refreshChannel: function(e, refresh_all) {
		var obj = e;
		
		if (obj.data)
			obj = obj.data.obj;
		//Get list of Players on Channel
		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
			url: "/chat/getPlayers",
			data: JSON.stringify({"channel": "local", "refresh_all": refresh_all}),
			dataType: "json",
			success: function (r) {
				console.log(r);
				var players = r.players;
				var i = 0;
				$(".member_list ul").empty();
				for(i=0; i<players.length; i++) {
					var s = $('#playerTpl').children().clone();
					$(s).find("strong").text(players[i].name);
					$(s).toggle();
					$(".member_list ul").append(s);
				}
				obj.refreshChannel(obj, 0);
				//console.log(pl);
			},
			error: function (message) {
				console.error("error has occured");
				console.error(message);
			}
		});
		
		if (obj.readyToGet){
		}
	},
	
	toggleChatWindow: function(e) {
		$('.chat_container').toggle();
		var obj = e;
		
		if (obj.data)
			obj = obj.data.obj;
		obj.windowVisible = !obj.windowVisible;
		
		if (obj.windowVisible) {
			//obj.refreshChannel(e);
		}
	},
	
	sendChatMessage: function(e) {
		var obj = e;
		
		if (obj.data)
			obj = obj.data.obj;
		var message = $('#chatText').val();
		//Send message to the Channel
		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
			url: "/chat/sendMessage",
			data: JSON.stringify({"channel": "local", "message": message.trim()}),
			dataType: "json",
			success: function (r) {
				console.log(r);
				$('#chatText').val('');
				obj.readyToSend = false;
				obj.readyToGet = true;
				//console.log(pl);
			},
			error: function (message) {
				console.error("error has occured");
				console.error(message);
			}
		})
	},
	
	getChatMessages: function(e) {
		var obj = e;
		
		if (obj.data)
			obj = obj.data.obj;
		//Get new messages to the Channel
		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
			url: "/chat/getMessages",
			data: JSON.stringify({"channel": "local"}),
			dataType: "json",
			success: function (r) {
				console.log(r);
				var msgs = r.result[0].messages;
				
				for(i=0; i<msgs.length; i++) {
					var s = $('#msgTpl').children().clone();
					var sb = $('#msgBodyTpl').clone();
					//console.log(msgs[i].message[1]+":"+msgs[i].message[2]);
					$(s).text(msgs[i].message[1]+": ");
					$(sb).text(msgs[i].message[2]);
					$(s).append(sb);
					$(s).toggle();
					$(".chat_area ul").append(s);
				}
				$('.chat_area').scrollTop($('.chat_area')[0].scrollHeight);

				obj.gotChatMessages(e);
			},
			error: function (message) {
				console.error("error has occured");
				console.error(message);
			}
		})
	},
	
	gotChatMessages: function(e) {
		var obj = e;
		
		if (obj.data)
			obj = obj.data.obj;
		//Clean messages
		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
			url: "/chat/gotMessages",
			data: {},
			dataType: "json",
			success: function (r) {
				console.log(r);
				if (obj.readyToSend){
					obj.readyToGet = false;
					obj.readyToSend = false;
				}
			obj.getChatMessages(e);
			},
			error: function (message) {
				console.error("error has occured");
				console.error(message);
			}
		})
	},
	
	LoadChat: function(obj) {
		$('#chatBtn').click({obj}, obj.toggleChatWindow);
		$('#chatSend').click({obj}, obj.sendChatMessage);
		$('#chatText').keyup(function(e){
			var keyCode = e.keyCode ? e.keyCode : e.which;
			if (keyCode == 13){
				obj.readyToSend = true;
				$('#chatText').val($('#chatText').val().trim());
				obj.sendChatMessage(e);
			}
		});
//		mainGame.setTimer('chat', obj.refreshChannel, 1000, obj);
		obj.refreshChannel(obj, 1)
		obj.getChatMessages(obj);
	}
}