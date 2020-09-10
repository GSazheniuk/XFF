var mapProto = function(){
//    this.canvas = $('#map_canvas')[0];
//    this.canvas_context = this.canvas.getContext('2d');
}

mapProto.prototype = {
    constructor: function(){
    },

    init_map: function(){
        $('#map_holder').show();
        this.loaded = false;
        var world, land, borders, countries;
        this.sphere = ({type: "Sphere"});
        this.tilt = 0;
        this.height = 720;
        this.width = 720;

        this.svg = {};

        this.projection = d3.geoOrthographic().fitExtent([[50, 50], [this.width - 50, this.height - 50]], this.sphere);
        this.path = d3.geoPath(this.projection);
        this.circle = d3.geoCircle();

        this.zoom = d3.zoom()
            .scaleExtent([0.5, 2])
            //.scale(this.projection.scale())
            //.translate([0,0])               // not linked directly to projection
            .on("zoom", this.redraw);

        this.svg = d3.select("#map_holder").append("svg").attr("width", this.width).attr("height", this.height)
            .attr("viewBox", "0 0 700 700");
        var defs = this.svg.append("defs");
        var filter = defs.append("filter")
            .attr("id","glow");
        filter.append("feGaussianBlur")
            .attr("stdDeviation","12.5")
            .attr("result","coloredBlur");
        var feMerge = filter.append("feMerge");
        feMerge.append("feMergeNode")
            .attr("in","coloredBlur");
        feMerge.append("feMergeNode")
            .attr("in","SourceGraphic");

        var filter2 = defs.append("filter")
            .attr("id","glow-bunker");
        filter2.append("feGaussianBlur")
            .attr("stdDeviation","2.5")
            .attr("result","coloredBlur");
        var feMerge2 = filter2.append("feMerge");
        feMerge2.append("feMergeNode")
            .attr("in","coloredBlur");
        feMerge2.append("feMergeNode")
            .attr("in","SourceGraphic");

        map = this;
        Promise.all([
            d3.json("/static/Data/countries-110m.json"),
            d3.json("/static/Data/places.json"),
        ]).then(function(files) {
            map.render(files[0], files[1]);
        });
    },
    render: function(world, places) {
        land = topojson.feature(world, world.objects.land);
        borders = topojson.mesh(world, world.objects.countries, (a, b) => a !== b);
        countries = topojson.feature(world, world.objects.countries).features;

        this.svg.selectAll('globe-filter')
            .data([this.sphere])
            .enter()
          .append('path')
            .attr('class', 'globe-filter')
            .attr('d', this.path);

        this.svg.selectAll('globe')
            .data([this.sphere])
            .enter()
          .append('path')
            .attr('class', 'globe')
            .attr('d', this.path);

        this.drawGraticule();

        this.svg.selectAll('country')
            .data(countries)
            .enter()
          .append('path')
            .attr('class', 'country')
            .attr('d', this.path)
            .style('stroke', "#fff");

        moon = this.svg.selectAll('moon')
                .data([this.circle])
                .enter()
              .append("path")
                .attr("fill", "#333333")
                .attr("opacity", 0.95);

        this.svg.append("g").attr("class","points")
            .selectAll("text").data(places.features)
          .enter().append("path")
            .attr("class", "point")
            .attr("d", this.path);

        this.svg.append("g").attr("class","labels")
            .selectAll("text").data(places.features)
          .enter().append("text")
          .attr("class", "label")
          .text(function(d) { return d.properties.name });

        this.svg.append("g").attr("class","points")
            .selectAll("text").data(places.features)
          .enter().append("path")
            .attr("class", "point")
            .attr("d", this.path);

        this.svg.append("g").attr("class","labels")
            .selectAll("text").data(places.features)
          .enter().append("text")
          .attr("class", "label")
          .text(function(d) { return d.properties.name });

        var f = false;

        this.path.pointRadius(function(d,i){
            if (d.type == "Feature")
                return 1;
            else
                return 2;
        });

        this.def_scale = this.projection.scale();
        this.loaded = true;
        this.svg.call(this.zoom);

        d3.timer(function (t){
//            moon.attr("d", path(circle.center([-t / 60, 0])()));
//            if (t % 10000 < 1000){
                map.projection.rotate([-t / 600, 0, 0]);
                map.redraw();
//            }
        });
    },
    redraw: function(){
        if (d3.event) {
            var scale = d3.event.transform.k,
                t = d3.event.translate;
            map.projection.scale(map.def_scale*scale);
//            console.log(d3.event);
            map.slast = scale;
            return;
        }
        map.svg.selectAll("path").attr("d", map.path);
        map.svg.selectAll(".ufo").attr("d", map.draw_ufo);
        map.svg.selectAll(".ufo-atk-zone").attr("d", map.draw_ufo_atk_zone);
        map.svg.selectAll(".ufo-atk-range").attr("d", map.draw_ufo_atk_zone);
        map.svg.selectAll(".bunker-filter")
            .attr("transform", function(d) { return "translate(" + map.projection([d.point.Lat, d.point.Long]) + ")"; })
            .attr("d", function(d) {return d3.symbol().size(20).type(d3.symbolTriangle)();})
            .attr("opacity", function(d) {
                var geoangle = d3.geoDistance(
                            [d.point.Lat, d.point.Long],
                            [-map.projection.rotate()[0], map.projection.rotate()[1]]
                        );
                if (geoangle > 1.57079632679490)
                {
                    return "0";
                } else {
                    return "1.0";
                }
            });
        map.svg.selectAll(".bunker-scan-zone").attr("d", map.draw_ufo_atk_zone);
        map.svg.selectAll(".bunker-scan-range").attr("d", map.draw_ufo_atk_zone);
    },
    drawGraticule: function() {
        const graticule = d3.geoGraticule()
            .step([10, 10]);

        this.svg.append("path")
            .datum(graticule)
            .attr("class", "graticule")
            .attr("d", this.path);
    },

    draw_objects: function(objects){
        ufos = [];
        bunkers = [];
        for (var o in objects){
            console.log(o);
            if (objects[o].objType == 1){
                ufos.push(objects[o]);
            }
            if (objects[o].objType == 0){
                objects[o].R = 7;
                bunkers.push(objects[o]);
            }
        }

        if (!this.loaded)
            return;

        this.draw_ufos(ufos);
        this.draw_bunkers(bunkers);
    },

    draw_ufos: function(ufos){
        var circle = this.svg.selectAll(".ufo")
            .data(ufos, function(d) { return d.id; });
        circle.exit().remove();
        circle.enter()
          .append("path")
            .attr("class", "ufo")
            .attr("d", map.draw_ufo);

        var circle = this.svg.selectAll(".ufo-atk-zone")
            .data(ufos, function(d) { return d.id; });
        circle.exit().remove();
        circle.enter()
          .append("path")
            .attr("class", "ufo-atk-zone")
            .attr("d", map.draw_ufo_atk_zone);

        var circle = this.svg.selectAll(".ufo-atk-range")
            .data(ufos, function(d) { return d.id; });
        circle.exit().remove();
        circle.enter()
          .append("path")
            .attr("class", "ufo-atk-range")
            .attr("d", map.draw_ufo_atk_zone);
    },

    draw_bunkers: function(bunkers){
        var tri = this.svg.selectAll(".bunker-filter")
            .data(bunkers, function(d) { return d.id; });
        tri.exit().remove();
        tri.enter()
          .append("path")
            .attr("class", "bunker-filter")
            .attr("transform", function(d) { return "translate(" + map.projection([d.point.Lat, d.point.Long]) + ")"; })
            .attr("d", function(d) {return map.path(d3.symbol().size(20).type(d3.symbolTriangle)());})
            .attr("opacity", function(d) {
                var geoangle = d3.geoDistance(
                            [d.point.Lat, d.point.Long],
                            [-map.projection.rotate()[0], map.projection.rotate()[1]]
                        );
                if (geoangle > 1.57079632679490)
                {
                    return "0";
                } else {
                    return "1.0";
                }
            });
        var tri = this.svg.selectAll(".bunker-scan-zone")
            .data(bunkers, function(d) { return d.id; });
        tri.exit().remove();
        tri.enter()
          .append("path")
            .attr("class", "bunker-scan-zone")
            .attr("d", map.draw_ufo_atk_zone);

        var tri = this.svg.selectAll(".bunker-scan-range")
            .data(bunkers, function(d) { return d.id; });
        tri.exit().remove();
        tri.enter()
          .append("path")
            .attr("class", "bunker-scan-range")
            .attr("d", map.draw_ufo_atk_zone);
    },

    draw_ufo: function(d) {return map.path(d3.geoCircle().center([d.point.Lat, d.point.Long]).radius(0.5)());},
    draw_ufo_atk_zone: function(d) {return map.path(d3.geoCircle().center([d.point.Lat, d.point.Long]).radius(d.R)());},
}