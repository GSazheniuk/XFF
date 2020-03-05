var Bunker = function () { };

Bunker.prototype = {
    id: null,
    Name: null,
    avail_recruits: null,
	isLoaded: 0,

    constructor: function () {
        id = "";
        Name = "";
    },
    getData: function (bunker_id) {
        owner = this;
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "/bunker/getData",
            data: JSON.stringify({"bunker_id": bunker_id}),
            dataType: "json",
            success: function (r) {
                console.log('bunker/getData - ', r);
				owner.isLoaded = 1;
				owner.data = r;
				displayBunkerInfo(owner);
            },
            error: function (message) {
                console.error("error has occurred");
                console.error(message);
            }
        })
    },
}