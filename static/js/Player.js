var Player = function () { };

Player.prototype = {
    tokenId: null,
    Name: null,
    attributes: null,
	isLoaded: 0,

    constructor: function () {
        tokenId = "";
        Name = "";
    },

    //Callbacks
    refreshPlayerCallback: null,

    loadFromJSON: function (player, pl) {
        var plr = null;

        if (pl != null) plr = pl;
        else plr = this;

        plr.Name = player.Name;
        plr.tokenId = player.TokenID;
        plr.attributes = player.Attributes;
    },

    refreshPlayer: function (owner) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            url: "http://localhost:8081/player/getData",
            dataType: "json",
            success: function (r) {
                console.log('player/getData - ', r);
				if (Object.keys(r).length === 0 && r.constructor === Object) {
					window.location = "/player/login";
				}
				
				owner.isLoaded = 1;
				owner.data = r;
				mainGame.getMapObjects(mainGame, 1);
				owner.displayPlayerInfo(owner);
//                console.log(owner);

                // if (response != null && response.RefreshPlayerResult != null) {
                    // owner.loadFromJSON(response.RefreshPlayerResult, owner);
                    // console.log('Player : ' + owner.leaderName + ' logged in successfully.');
                // }

                // if (typeof owner.refreshPlayerCallback === "function")
                    // owner.refreshPlayerCallback();
            },
            error: function (message) {
                console.error("error has occured");
                console.error(message);
            }
        })
    },
	
	displayPlayerInfo(pl){
		$("#player_info").empty();
		$("#player_info").append(pl.data.Name+"<br />");
		$("#player_info").append("(" + pl.data.Organization.Name+")<br />");
		$("#player_info").append("X: " + pl.data.MapObject.X);
		$("#player_info").append("  |   Y: " + pl.data.MapObject.Y+"<br />");
	},

    getAttributeValue: function (a, b) {
        var attr = this.attributes.find(x=> x.AttributeType === a && x.Attribute === b);
        if (attr != null)
            return attr.Value;
        else
            return null;
    },
}