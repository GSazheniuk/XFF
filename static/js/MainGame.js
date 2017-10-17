var mGame = function () { };

mGame.prototype = {
    intervalIds: {},
    refreshTimeout: 5000,

    constructor: function () {
        refreshTimeout = 5000;
    },

    //Callbacks
    refreshWorldTimeCallback: null,

    setTimer: function (intervalId, delegate, interval, owner) {
        if (this.intervalIds[intervalId] != null) {
            window.clearInterval(this.intervalIds[intervalId]);
            this.intervalIds[intervalId] = null;
        }

        this.intervalIds[intervalId] = window.setInterval(delegate, interval, owner);
    },

    refreshWorldTime: function (w) {
        $.ajax({
            type: "POST",
            contentType: "application/json; charset=utf-8",
            url: "http://localhost:8001/HOOService/GetWorldState",
            data: JSON.stringify({ }),
            dataType: "json",
            success: function (response) {
                console.log(response);

                if (response != null && response.GetWorldStateResult != null) {
                    var res = JSON.parse(response.GetWorldStateResult);
                    //console.log(response.GetWorldStateResult);
                    //console.log(res);

                    //console.log(w);

                    w.WorldPeriod = res.Period;
                    w.WorldTick = res.Tick;
                    w.WorldTurn = res.Turn;

                    if (typeof w.refreshWorldTimeCallback === "function")
                        w.refreshWorldTimeCallback();
                }
            },
            error: function (message) {
                console.error("error has occured");
                console.error(message);
            }
        })
    },

    LoadMain: function () {
		p.refreshPlayer(this);
    }
}