var mGame = function () { };

mGame.prototype = {
    constructor: function () {
    },
	
	getMapObjects: function (refresh_all) {
		var obj = this;

		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
			url: "http://localhost:8081/map/getObjects",
			data: JSON.stringify({"refresh_all": refresh_all}),
			dataType: "json",
			success: function (r) {
				console.log(r);
				$("#event_log").empty();
				map.draw_objects(r);
				for(var obj_id in r) {
					var s = '<li class="ufo" id="' + obj_id + '">'
					s += r[obj_id].objType + ' - ';
					s += r[obj_id].X + ' : ';
					s += r[obj_id].Y + ' - ';
					s += (distance(p.data.MapObject.X, p.data.MapObject.Y, r[obj_id].X, r[obj_id].Y) / 1000).toFixed(3);
					s += ' miles away. ';
					s += '- ' + enums.UfoStatuses[r[obj_id].status];
					s += ' <span class="approach">&gt;&gt;</span>'
					s += '</li>';
					$("#event_log").append(s);
				}
                $(".ufo .approach").click(function(e){
                    $.ajax({
                        type: "POST",
                        contentType: "application/json; charset=utf-8",
                        url: "http://localhost:8081/map/approachObject",
                        data: JSON.stringify({"object_id": $(this.parentElement).attr("id")}),
                        dataType: "json",
            			success: function (r) {
            			    console.log("approachObject result: ", r)
                        },
                        error: function (message) {
                            console.error("approachObject error has occurred");
                            console.error(message);
                        }
                    })
                });
				obj.getMapObjects(0);
				//console.log(pl);
			},
			error: function (message) {
				console.error("error has occurred");
				console.error(message);
			}
		});
	},

    LoadMain: function () {
		map.init_map();
    }
}