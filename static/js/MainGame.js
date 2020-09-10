var mGame = function () { };

mGame.prototype = {
    constructor: function () {
    },
	
	getMapObjects: function (refresh_all) {
		var obj = this;

		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
			url: "/map/getObjects",
			data: JSON.stringify({"refresh_all": refresh_all}),
			dataType: "json",
			success: function (r) {
			    //console.log(r);
				$("#event_log").empty();
				r = r.objects;
				map.draw_objects(r);
				total_ops = 0;
				for(var obj_id in r) {
				    console.log(obj_id);
				    if (r[obj_id].objType > 0) {
				        total_ops++;
                        var s = '<li class="ufo" id="' + r[obj_id].id + '">'
                        s += r[obj_id].name + ' - ';
                        s += r[obj_id].point.Lat + ' : ';
                        s += r[obj_id].point.Long + ' - ';
//                        s += (distance(p.data.MapObject.X, p.data.MapObject.Y, r[obj_id].X, r[obj_id].Y) / 1000).toFixed(3);
                        s += ' miles away. ';
                        s += '- ' + enums.UfoStatuses[r[obj_id].status];
                        s += ' <span class="approach">&gt;&gt;</span>'
                        s += '</li>';
                        $("#event_log").append(s);
					}
				    if (r[obj_id].objType == 0) {
				        continue;
                        var s = '<li class="bunker" id="' + r[obj_id].id + '">'
                        s += r[obj_id].name + ' - ';
                        s += r[obj_id].X + ' : ';
                        s += r[obj_id].Y + ' - ';
//                        s += (distance(p.data.MapObject.X, p.data.MapObject.Y, r[obj_id].X, r[obj_id].Y) / 1000).toFixed(3);
                        s += ' miles away. ';
                        s += ' <span class="approach">&gt;&gt;</span>'
                        s += '</li>';
                        $("#event_log").append(s);
					}
				}
				$("#opsnum").text(total_ops);
                $(".ufo .approach").click(function(e){
                    $.ajax({
                        type: "POST",
                        contentType: "application/json; charset=utf-8",
                        url: "/attack_site",
                        data: JSON.stringify({"site_id": $(this.parentElement).attr("id")}),
                        dataType: "json",
            			success: function (r) {
            			    console.log("attack result: ", r)
            			    location.href = "/attack_site"
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