var mGame = function () { };

mGame.prototype = {
    constructor: function () {
    },
	
	getMapObjects: function (e, refresh_all) {
		var obj = e;

		$.ajax({
			type: "POST",
            contentType: "application/json; charset=utf-8",
			url: "http://localhost:8081/map/getObjects",
			data: JSON.stringify({"refresh_all": refresh_all}),
			dataType: "json",
			success: function (r) {
				console.log(r);
				$("#map_holder").empty();
				for(var obj_id in r) {
					var s = '<li class="ufo" id="' + obj_id + '">'
					s += r[obj_id].objType + ' - ';
					s += r[obj_id].X + ' : ';
					s += r[obj_id].Y + ' - ';
					s += (distance(p.data.MapObject.X, p.data.MapObject.Y, r[obj_id].X, r[obj_id].Y) / 1000).toFixed(3);
					s += ' miles away. ';
					s += '<span class="approach">&gt;&gt;</span>'
					s += '</li>';
					$("#map_holder").append(s);
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
				obj.getMapObjects(obj, 1 - refresh_all);
				//console.log(pl);
			},
			error: function (message) {
				console.error("error has occurred");
				console.error(message);
			}
		});
	},

    LoadMain: function () {
		p.refreshPlayer(p);
    }
}