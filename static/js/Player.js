var Player = function () { };

Player.prototype = {
    tokenId: null,
    Name: null,
    attributes: null,
    Organization: null,
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
        plr.Organization = player.Organization;
    },

    refreshPlayer: function () {
        owner = this;
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
				displayPlayerInfo(owner);
//                console.log(owner);

                // if (response != null && response.RefreshPlayerResult != null) {
                    // owner.loadFromJSON(response.RefreshPlayerResult, owner);
                    // console.log('Player : ' + owner.leaderName + ' logged in successfully.');
                // }

                 if (typeof owner.refreshPlayerCallback === "function")
                     owner.refreshPlayerCallback();
            },
            error: function (message) {
                console.error("error has occurred");
                console.error(message);
            }
        })
    },

    addSkillToQueue: function (skill){
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "http://localhost:8081/player/addSkill",
            data: JSON.stringify({"skill_name": skill}),
            dataType: "json",
            success: function (r) {
                p.refreshPlayer();
            },
            error: function (message) {
                console.error("addSkillToQueue error has occurred");
                console.error(message);
            }
        })
    },

    recruitSoldier: function (ids){
        recruit_id = ids.split(":")[0];
        bunker_id = ids.split(":")[1];
        console.log(ids);
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "http://localhost:8081/bunker/recruitSoldier",
            data: JSON.stringify({"recruit_id": parseInt(recruit_id), "bunker_id": parseInt(bunker_id)}),
            dataType: "json",
            success: function (r) {
                recruitSoldier(recruit_id);
            },
            error: function (message) {
                console.error("recruitSoldier error has occurred");
                console.error(message);
            }
        })
    },

    getAttributeValue: function (a, b) {
        var attr = this.attributes.find(x=> x.AttributeType === a && x.Attribute === b);
        if (attr != null)
            return attr.Value;
        else
            return null;
    },
}