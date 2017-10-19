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
					var s = '<li>'+JSON.stringify(r[obj_id])+'</li>';
					$("#map_holder").append(s);
				}
				obj.getMapObjects(obj, 1 - refresh_all);
				//console.log(pl);
			},
			error: function (message) {
				console.error("error has occured");
				console.error(message);
			}
		});
	},

    LoadMain: function () {
		p.refreshPlayer(this);
    }
}