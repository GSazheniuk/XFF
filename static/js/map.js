var mapProto = function(){
    this.canvas = $('#map_canvas')[0];
    this.canvas_context = this.canvas.getContext('2d');
}

mapProto.prototype = {
    constructor: function(){
    },

    init_map: function(){
        $('#map_holder').show();
    },

    draw_objects: function(map_objects){
        this.canvas_context.clearRect(0, 0, 500, 500);
        for (var o_id in map_objects){
            o = map_objects[o_id];
            this.draw_ufo(o);
        }
    },

    draw_ufo: function(o){
        ctx = this.canvas_context;
        var grd = ctx.createRadialGradient(o.X / 2000, o.Y / 2000, 0, o.X / 2000, o.Y / 2000, o.R);
        if (o.objType == 20) {grd.addColorStop(0, "green");}
        if (o.objType < 20) {grd.addColorStop(0, "red");}
        if (o.objType == 1000) {grd.addColorStop(0, "grey");}
        grd.addColorStop(0.8, "silver");
        grd.addColorStop(1, "white");
        ctx.beginPath();
        ctx.arc(o.X / 2000, o.Y / 2000, o.R, 0, 2*Math.PI);
        ctx.stroke();
        ctx.fillStyle = grd;
        ctx.fill();
    },
}