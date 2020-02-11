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

        owner = this;
        Promise.all([
            d3.json("/static/Data/countries-110m.json"),
            d3.json("/static/Data/places.json"),
        ]).then(function(files) {
            owner.render(files[0], files[1]);
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

        owner = this;
        this.loaded = true;

        d3.timer(function (t){
//            moon.attr("d", path(circle.center([-t / 60, 0])()));
//            if (t % 10000 < 1000){
                owner.projection.rotate([-t / 600, 0, 0]);
                owner.svg.selectAll("path").attr("d", owner.path);
                owner.svg.selectAll(".ufo").attr("d", function(d) {return map.path(d3.geoCircle().center([d.point.Lat, d.point.Long]).radius(d.R)());});
                owner.svg.selectAll(".bunker-filter")
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
//            }
        });
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
            if (objects[o].objType < 20){
                ufos.push(objects[o]);
            }
            if (objects[o].objType == 1000){
                bunkers.push(objects[o]);
            }
        }

        if (!this.loaded)
            return;

        var circle = this.svg.selectAll(".ufo")
            .data(ufos, function(d) { return d.id; });
        circle.exit().remove();
        circle.enter()
          .append("path")
            .attr("class", "ufo")
            .attr("d", function(d) {return map.path(d3.geoCircle().center([d.point.Lat, d.point.Long]).radius(d.R)());});

        var tri = this.svg.selectAll(".bunker-filter")
            .data(bunkers, function(d) { return d.id; });
        tri.exit().remove();
        tri.enter()
          .append("path")
            .attr("class", "bunker-filter")
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

    },

    draw_ufo: function(d){
        return map.path()
    },
}