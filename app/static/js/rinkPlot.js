var RINK_HELPERS = {
    toolTipText: function(d){
        var shotStr = "";
        var P1 = d["P1"];
        var P2 = d["P2"];
        var P3 = d["P3"];
        var shotFeature = d["shot.feature"];
        switch(d["etype"]){
            case "MISS":
                shotStr = RINK_HELPERS.missText(P1, "", shotFeature);
                break;
            case "BLOCK":
                shotStr = RINK_HELPERS.blockedText(P1, P2, "", shotFeature);
                break;
            case "SHOT":
                shotStr = RINK_HELPERS.shotText(P1, "", shotFeature);
                break;
            case "GOAL":
                shotStr = RINK_HELPERS.goalText(P1, P2, P3, "", shotFeature);
                break;
        }
        var timeStr = "Period: " + d["period"] + " | " + "Time: " + RINK_HELPERS.secondsToMS(d["seconds"], d["period"]);
        return shotStr + "<br>" + timeStr + "<br>Distance: " + RINK_HELPERS.adjDistanceRnd(d["adjusted.distance"]) + " ft.";
    },

    titleText: function(team){
        return team + " Shot Attempts";
    },

    blockedText: function(shotBy, blockedBy, shotType, shotFeature){
        return "BLOCKED SHOT " + RINK_HELPERS.featureText(shotFeature) + "by <b>" + shotBy + "</b><br>Blocked by <b>" + blockedBy + "</b>";
    },

    goalText: function(shotBy, primaryAssist, secondaryAssist, shotType, shotFeature){
        return "GOAL " + RINK_HELPERS.featureText(shotFeature) + "by <b>" + shotBy + "</b><br>A1: " + primaryAssist + "<br>A2: " + secondaryAssist;
    },

    missText: function(shotBy, shotType, shotFeature){
        return "MISS " + RINK_HELPERS.featureText(shotFeature) + "by <b>" + shotBy + "</b>";
    },

    shotText: function(shotBy, shotType, shotFeature){
        return "SHOT " + RINK_HELPERS.featureText(shotFeature) + "by <b>" + shotBy + "</b>";
    },

    featureText: function(shotFeature){
        if (shotFeature.indexOf("rush") >= 0){
            return "(rush) ";
        }
        else if (shotFeature.indexOf("reb") >= 0) {
            return "(rebound) ";
        }
        else{
            return "";
        }
    },

    secondsToMS: function(seconds, period){
        var secondsIntoPeriod = Math.round(seconds - ((period - 1) * 60 * 20));
        var minutesIntoPeriod = Math.floor(secondsIntoPeriod / 60);
        var secondsCalc = secondsIntoPeriod - (minutesIntoPeriod * 60);
        var secondsStr;
        if(secondsCalc < 10){
            secondsStr =  "0" + String(secondsCalc);
        }
        else{
            secondsStr = String(secondsCalc);
        }
        return String(minutesIntoPeriod) + ":" + secondsStr;
    },

    adjDistanceRnd: function(distance){
        return Math.round(100 * distance)/100;
    }
};

var RINK_MAP = function RinkMap(config){

    // all distances are in FT
    var RINK_CONFIG =
    {
        RINK_LENGTH: 200,
        RINK_WIDTH: 85,
        BLUE_LINE_WIDTH: 1,
        BOARDS_RADIUS: 28,
        RED_TO_BOARDS: 11,
        RED_TO_FACEOFF: 20,
        FACEOFF_RADIUS: 15,
        FACEOFF_DOT_RADIUS: 1,
        ZONE_LINE_WIDTH: (2/12),
        CREASE_RADIUS: 6,
        ZONE_LENGTH: 75,
        ZONE_TO_NEUTRAL_DOT: 5,
        CENTER_TO_NEUTRAL_DOT: 22,
        REF_CREASE_RADIUS: 10,
        CREASE_HEIGHT: 4,
        FACEOFF_HOR_LENGTH: 3,
        FACEOFF_VER_LENGTH: 4,
        FACEOFF_HOR_DIST_CEN: 2,
        FACEOFF_VER_DIST_CEN: (9/12),
        FACEOFF_OUT_MARK_LENGTH: 2,
        FACEOFF_OUT_MARK_DIST_BW: 5 + (7/12),
        TRAPEZOID_TOP: 22,
        TRAPEZOID_BOTTOM: 28
    }

    var RINK_COLOR =
    {
        BLUE_LINE: "blue",
        RINK_FILL: "white",
        GOAL_FILL: "lightblue"
    }

    var p =
    {
        chartsize: {width: 500, height: 500},
        margins:  {top: 30, bottom: 5, left: 10, right: 10},
        danger: [{x1: -9.11, y1: 89.1},
            {x1: -22.1, y1: 68.9}, {x1: -22.1, y1: 53.9},
            {x1: -9.11, y1: 53.9}, {x1: -9.11, y1: 43.9},
            {x1: 9.11, y1: 43.9}, {x1: 9.11, y1: 53.9},
            {x1: 22.1, y1: 53.9}, {x1: 22.1, y1: 68.9},
            {x1: 9.11, y1: 89.1}, {x1: -9.11, y1: 89.1},
            {x1: -9.11, y1: 68.9}, {x1: 9.11, y1: 68.9},
            {x1: 9.11, y1: 89.1}, {x1: -9.11, y1: 89.1}]
    }

    if (config !== "undefined"){
        for (var property in config){
            p[property] = config[property];
        }
    }

    var rinkScale = p.desiredWidth / RINK_CONFIG.RINK_WIDTH;

    for (var param in RINK_CONFIG){
        RINK_CONFIG[param] = rinkScale * RINK_CONFIG[param];
    }

    // CREATE CHART
    function chart() {

        function rinkLine(x, group, type){
            group
                .append("rect")
                .attr("x", x)
                .attr("y", 0)
                .attr("width", RINK_CONFIG.BLUE_LINE_WIDTH)
                .attr("height", RINK_CONFIG.RINK_WIDTH)
                .attr("class", type);
        }

        function rinkOutLine(group){

            group
                .append("path")
                .attr("d", rounded_rect(0,0, RINK_CONFIG.RINK_LENGTH *0.5, RINK_CONFIG.RINK_WIDTH, RINK_CONFIG.BOARDS_RADIUS, true, false, true, false))
                .attr("class", "rink-face")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                // when clicking on rink face, set tooltip back to no opacity
                .on("click", function(d){
                  toolTipDiv.style("opacity", 0);
                });

        }

        // From stackOverflow http://stackoverflow.com/questions/12115691/svg-d3-js-rounded-corner-on-one-corner-of-a-rectangle
        // r -> radius, tl/tr/bl/br - top left/bottom right TRUE/FALSE for posessing rounded corner
        function rounded_rect(x, y, w, h, r, tl, tr, bl, br) {
            var retval;
            retval  = "M" + (x + r) + "," + y;
            retval += "h" + (w - 2*r);
            if (tr) { retval += "a" + r + "," + r + " 0 0 1 " + r + "," + r; }
            else { retval += "h" + r; retval += "v" + r; }
            retval += "v" + (h - 2*r);
            if (br) { retval += "a" + r + "," + r + " 0 0 1 " + -r + "," + r; }
            else { retval += "v" + r; retval += "h" + -r; }
            retval += "h" + (2*r - w);
            if (bl) { retval += "a" + r + "," + r + " 0 0 1 " + -r + "," + -r; }
            else { retval += "h" + -r; retval += "v" + -r; }
            retval += "v" + (2*r - h);
            if (tl) { retval += "a" + r + "," + r + " 0 0 1 " + r + "," + -r; }
            else { retval += "v" + -r; retval += "h" + r; }
            retval += "z";
            return retval;
        }

        // Create goal crease with center at point (x,y) and width d
        function goalCrease(xPos, group){

            var creaseData = [  {"x": xPos, "y": (RINK_CONFIG.RINK_WIDTH/2 ) - RINK_CONFIG.CREASE_HEIGHT , "type": "M"},
                                {"x": xPos + RINK_CONFIG.CREASE_HEIGHT, "y":(RINK_CONFIG.RINK_WIDTH/2 ) - RINK_CONFIG.CREASE_HEIGHT, "type": "L"},
                                {"x": xPos + RINK_CONFIG.CREASE_HEIGHT, "y": (RINK_CONFIG.RINK_WIDTH/2 ) + RINK_CONFIG.CREASE_HEIGHT, "type": "A", "radius": RINK_CONFIG.CREASE_RADIUS},
                                {"x": xPos, "y": (RINK_CONFIG.RINK_WIDTH/2 ) + RINK_CONFIG.CREASE_HEIGHT, "type": "L"}];

            var creaseFunction = function(input){
                var dStr = "";
                for (var i=0; i < input.length; i++){
                    if (input[i]["type"] === "M" || input[i]["type"] === "L"){
                        dStr += input[i]["type"] + input[i]["x"] + "," + input[i]["y"];
                    }
                    else if (input[i]["type"] === "A"){
                        dStr += input[i]["type"] + input[i]["radius"] + "," + input[i]["radius"] + ",0,0,1," + input[i]["x"] + "," + input[i]["y"];
                    }
                }
                return dStr;
            }

            group
                .append("path")
                .attr("d", creaseFunction(creaseData))
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("class", "goal-crease");
        }

        // Create red-line at xPos to scale
        function redLine(x, group){
            var yDistance = RINK_CONFIG.BOARDS_RADIUS - Math.sqrt((2 * RINK_CONFIG.RED_TO_BOARDS * RINK_CONFIG.BOARDS_RADIUS) - (RINK_CONFIG.RED_TO_BOARDS * RINK_CONFIG.RED_TO_BOARDS));
            group
                .append("rect")
                .attr("x", x)
                .attr("y", yDistance)
                .attr("width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("height", RINK_CONFIG.RINK_WIDTH - 2 * yDistance)
                .attr("class", "red-line");
        }

        function faceOffDot(x,y, group){
            group
                .append("circle")
                .attr("cx", x)
                .attr("cy", y)
                .attr("r", RINK_CONFIG.FACEOFF_DOT_RADIUS)
                .attr("class", "red-line");
        }

        // Create face-off circule with radius r at point (x,y)
        function faceOffCircle(x, y, group){
            var faceOff = group.append("g")
              .attr("class", "faceoff");


            // outer face-off circle
            faceOff.append("circle")
                .attr("cx", x)
                .attr("cy", y)
                .attr("r", RINK_CONFIG.FACEOFF_RADIUS)
                .style("fill", RINK_COLOR.RINK_FILL)
                .attr("class", "red-faceoff")
                .style("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH);

            // face-off dot
            faceOff
                .append("circle")
                .attr("cx", x)
                .attr("cy", y)
                .attr("r", RINK_CONFIG.FACEOFF_DOT_RADIUS)
                .attr("class", "red-line");

            // Function/data to create four face-off markers
            var faceOffLineFunction = d3.svg.line()
                .x(function(d) {return RINK_CONFIG.FACEOFF_HOR_DIST_CEN + d.x; })
                .y(function(d) {return RINK_CONFIG.FACEOFF_VER_DIST_CEN + d.y; })
                .interpolate("linear");
            var faceOffLineData = [ {"x": RINK_CONFIG.FACEOFF_VER_LENGTH, "y": 0} ,{"x": 0, "y": 0},{"x": 0, "y": RINK_CONFIG.FACEOFF_HOR_LENGTH}];

            // Create four markers, each translated appropriately off-of (x,y)
            faceOff
                .append("path")
                .attr("d", faceOffLineFunction(faceOffLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + x + " , " + y + ")scale(-1, -1)");
            faceOff
                .append("path")
                .attr("d", faceOffLineFunction(faceOffLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + x + " , " + y + ")scale(1,-1)");
            faceOff
                .append("path")
                .attr("d", faceOffLineFunction(faceOffLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + x + " , " + y + ")");
            faceOff
                .append("path")
                .attr("d", faceOffLineFunction(faceOffLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + x + " , " + y + ")scale(-1, 1)");

            // Create two hash on outside of circle (each side)
            // Function/data to create outside line markers
            var outsideLineFunction = d3.svg.line()
                .x(function(d) {return  d.x; })
                .y(function(d) {return  d.y; })
                .interpolate("linear");
            var xStartOutsideLine = 0.5 * RINK_CONFIG.FACEOFF_OUT_MARK_DIST_BW * Math.tan(Math.acos(0.5 * RINK_CONFIG.FACEOFF_OUT_MARK_DIST_BW/RINK_CONFIG.FACEOFF_RADIUS));
            var outsideLineData = [ {"x": 0, "y": xStartOutsideLine} ,{"x": 0, "y": xStartOutsideLine + RINK_CONFIG.FACEOFF_OUT_MARK_LENGTH}];
            faceOff
                .append("path")
                .attr("d", outsideLineFunction(outsideLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + (x - 0.5 * RINK_CONFIG.FACEOFF_OUT_MARK_DIST_BW) + " , " + y + ")");
            faceOff
                .append("path")
                .attr("d", outsideLineFunction(outsideLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + (x + 0.5 * RINK_CONFIG.FACEOFF_OUT_MARK_DIST_BW) + " , " + y + ")");
             faceOff
                .append("path")
                .attr("d", outsideLineFunction(outsideLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + (x + 0.5 * RINK_CONFIG.FACEOFF_OUT_MARK_DIST_BW) + " , " + y + "), scale(1,-1)");
            faceOff
                .append("path")
                .attr("d", outsideLineFunction(outsideLineData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + (x - 0.5 * RINK_CONFIG.FACEOFF_OUT_MARK_DIST_BW) + " , " + y + "), scale(1,-1)");

        }

        function trapezoid(xPos, group){

            var trapezoidFunction = d3.svg.line()
                .x(function(d) {return RINK_CONFIG.RED_TO_BOARDS + d.x; })
                .y(function(d) {return (0.5 * (RINK_CONFIG.RINK_WIDTH - RINK_CONFIG.CENTER_TO_NEUTRAL_DOT)) + d.y; })
                .interpolate("linear");

            var trapezoidData = [ {"x": -1 * RINK_CONFIG.RED_TO_BOARDS, "y": -0.5 * (RINK_CONFIG.TRAPEZOID_BOTTOM - RINK_CONFIG.TRAPEZOID_TOP)} ,{"x":0 , "y": 0}];

            group
                .append("path")
                .attr("d", trapezoidFunction(trapezoidData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "translate(" + xPos + " ,0)");
            group
                .append("path")
                .attr("d", trapezoidFunction(trapezoidData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none")
                .attr("transform", "scale(1,-1),translate(" + xPos + "," + (-1 * RINK_CONFIG.RINK_WIDTH) + ")");
        }

        function neutralCircle(x, y, group){

            var circleData = [  {"x": x, "y": y - RINK_CONFIG.FACEOFF_RADIUS, "type": "M"},
                            {"x": x, "y": y + RINK_CONFIG.FACEOFF_RADIUS, "type": "A", "radius": RINK_CONFIG.FACEOFF_RADIUS, "dir": 0}];

            group
                .append("path")
                .attr("d", dStringCreator(circleData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none");
        }

        var dStringCreator = function(input){
            var dStr = "";
            for (var i=0; i < input.length; i++){
                if (input[i]["type"] === "M" || input[i]["type"] === "L"){
                    dStr += input[i]["type"] + input[i]["x"] + " " + input[i]["y"];
                }
                else if (input[i]["type"] === "A"){
                    dStr += input[i]["type"] + input[i]["radius"] + "," + input[i]["radius"] + ",0,0," + input[i]["dir"] + "," + input[i]["x"] + "," + input[i]["y"];
                }
                else{
                    "neither";
                }
            }
            return dStr;
        }

        function refereeCrease(xPos, group){
            var creaseData = [  {"x": xPos - RINK_CONFIG.REF_CREASE_RADIUS, "y": RINK_CONFIG.RINK_WIDTH, "type": "M"},
                                {"x": xPos, "y": RINK_CONFIG.RINK_WIDTH - RINK_CONFIG.REF_CREASE_RADIUS, "type": "A", "radius": RINK_CONFIG.REF_CREASE_RADIUS, "dir": 1}];

            group
                .append("path")
                .attr("d", dStringCreator(creaseData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .attr("fill", "none");
        }

        function dangerZones(zoneCoords, group){
            var dangerZoneGroup = group.append("g").attr("class","danger-zone");
            var dangerData = [];

            dangerData[0] = {"type": "M", "x": (0.5 * RINK_CONFIG.RINK_LENGTH - zoneCoords[0]["y1"] * rinkScale), "y": (0.5 * RINK_CONFIG.RINK_WIDTH +zoneCoords[0]["x1"] * rinkScale)};

            var i = 1;
            for (coord in zoneCoords){
                dangerData[i] = {};
                dangerData[i]["x"] = 0.5 * RINK_CONFIG.RINK_LENGTH - zoneCoords[coord]["y1"] * rinkScale;
                dangerData[i]["y"] = 0.5 * RINK_CONFIG.RINK_WIDTH +zoneCoords[coord]["x1"] * rinkScale;
                dangerData[i]["type"] = "L";
                i++;
            }

            dangerZoneGroup
                .append("path")
                .attr("d", dStringCreator(dangerData))
                .attr("class", "red-faceoff")
                .attr("stroke-width", RINK_CONFIG.ZONE_LINE_WIDTH)
                .style("stroke-dasharray", "10,10")
                .attr("fill", "none");
        }

        function waterMark(xPos, yPos, group){
            var waterMarkText = "war-on-ice.com";
            group
                .append("text")
                .style("fill", "lightgray")
                .style("font-size", "18px")
                .style("text-anchor", "middle")
                .style("alignment-baseline", "middle")
                .attr("transform", "translate(" + xPos +"," + yPos + ") rotate(90)")
                .text(waterMarkText);
        }

        function addTitle(xPos, yPos, title, group){
            group
                .append("text")
                .style("fill", "black")
                .style("font-size", "20px")
                .style("font-weight", "strong")
                .style("text-anchor", "middle")
                .style("alignment-baseline", "middle")
                .attr("transform", "translate(" + xPos +"," + yPos + ")")
                .text(title);
        }

        var zones = p.parent.append("g").attr("class", "zones");
        // RINK CONFIGURATON -- BOTH ZONES
        var zone1 = zones.append("g")
                      .attr("class", "zone1");
        var zone1Elements = zone1.append("g").attr("class", "rinkElements");

        rinkOutLine(zone1Elements);
        rinkLine(0.5 * RINK_CONFIG.RINK_LENGTH, zone1Elements, "center-line"); // center line

        // o-zone (left)
        rinkLine(RINK_CONFIG.ZONE_LENGTH, zone1Elements, "blue-line");
        faceOffCircle(RINK_CONFIG.RED_TO_BOARDS + RINK_CONFIG.RED_TO_FACEOFF, RINK_CONFIG.RINK_WIDTH/2 - RINK_CONFIG.CENTER_TO_NEUTRAL_DOT, zone1Elements);
        faceOffCircle(RINK_CONFIG.RED_TO_BOARDS + RINK_CONFIG.RED_TO_FACEOFF, RINK_CONFIG.RINK_WIDTH/2 + RINK_CONFIG.CENTER_TO_NEUTRAL_DOT, zone1Elements)

        redLine(RINK_CONFIG.RED_TO_BOARDS, zone1Elements);
        trapezoid(0, zone1Elements);
        goalCrease(RINK_CONFIG.RED_TO_BOARDS, zone1Elements);

        // neutral-zone (left)
        faceOffDot(RINK_CONFIG.ZONE_LENGTH + RINK_CONFIG.ZONE_TO_NEUTRAL_DOT, (RINK_CONFIG.RINK_WIDTH/2 - RINK_CONFIG.CENTER_TO_NEUTRAL_DOT), zone1Elements);
        faceOffDot(RINK_CONFIG.ZONE_LENGTH + RINK_CONFIG.ZONE_TO_NEUTRAL_DOT, (RINK_CONFIG.RINK_WIDTH/2 + RINK_CONFIG.CENTER_TO_NEUTRAL_DOT), zone1Elements);

        refereeCrease(0.5 * RINK_CONFIG.RINK_LENGTH, zone1Elements);
        neutralCircle(0.5 * RINK_CONFIG.RINK_LENGTH, 0.5 * RINK_CONFIG.RINK_WIDTH, zone1Elements);
        dangerZones(p.danger, zone1Elements)

        waterMark(RINK_CONFIG.RED_TO_BOARDS /2, RINK_CONFIG.RINK_WIDTH/2, zone1Elements);
        addTitle(RINK_CONFIG.RINK_WIDTH/2, p.margins.top/2, p.chartTitle, p.parent)

        // if full rink, generate zone2.
        if (p.fullRink){
            zoneName = "zone2";
            var zone2 = zones.append("g")
                .attr("class", zoneName);

            rinkOutLine(zone2);
            rinkLine(0.5 * RINK_CONFIG.RINK_LENGTH, zone2, "center-line"); // center line

            rinkLine(RINK_CONFIG.ZONE_LENGTH, zone2, "blue-line");
            faceOffCircle(RINK_CONFIG.RED_TO_BOARDS + RINK_CONFIG.RED_TO_FACEOFF, RINK_CONFIG.RINK_WIDTH/2 - RINK_CONFIG.CENTER_TO_NEUTRAL_DOT, zone2);
            faceOffCircle(RINK_CONFIG.RED_TO_BOARDS + RINK_CONFIG.RED_TO_FACEOFF, RINK_CONFIG.RINK_WIDTH/2 + RINK_CONFIG.CENTER_TO_NEUTRAL_DOT, zone2)
            goalCrease(RINK_CONFIG.RED_TO_BOARDS, zone2);
            redLine(RINK_CONFIG.RED_TO_BOARDS, zone2);
            trapezoid(0, zone2);

            faceOffDot(RINK_CONFIG.ZONE_LENGTH + RINK_CONFIG.ZONE_TO_NEUTRAL_DOT, (RINK_CONFIG.RINK_WIDTH/2 - RINK_CONFIG.CENTER_TO_NEUTRAL_DOT), zone2);
            faceOffDot(RINK_CONFIG.ZONE_LENGTH + RINK_CONFIG.ZONE_TO_NEUTRAL_DOT, (RINK_CONFIG.RINK_WIDTH/2 + RINK_CONFIG.CENTER_TO_NEUTRAL_DOT), zone2);

            refereeCrease(0.5 * RINK_CONFIG.RINK_LENGTH, zone2);
            neutralCircle(0.5 * RINK_CONFIG.RINK_LENGTH, 0.5 * RINK_CONFIG.RINK_WIDTH, zone2);
            waterMark(RINK_CONFIG.RED_TO_BOARDS /2, RINK_CONFIG.RINK_WIDTH/2, zone2);
        }

        // // Define 'div' for tooltips
        var toolTipDiv = d3.select("body")
            .append("div")
            .style("position", "absolute")
            .style("z-index", "10")
            .style("visibility", "hidden")
            .style("border-radius", 3)
            .attr("class", "tooltip-inner")
            .text("a simple tooltip");

        // For each shot attempt, create g element which we will append circle and text to.
        var shotNodes = p.parent.selectAll(".zone1").append("g")
                            .attr("class", "shotEvents")
                            .selectAll("text")
                            .data(p.data)
                            .enter()
                            .append("g");

        var shotX = function(d) {
                      return (0.5 * RINK_CONFIG.RINK_LENGTH - d["newxc"] * rinkScale);
                    };

        var shotY = function(d) {
                      return (0.5 * RINK_CONFIG.RINK_WIDTH + d["newyc"] * rinkScale);
                    };

        var shotClass = function(d){
                          var shotFeature = d["shot.feature"];
                          var shotType = d["etype"];
                          if (shotFeature.indexOf("rush") >= 0){
                            shotFeature = " rush";
                          }
                          else if ( shotFeature.indexOf("reb") >= 0){
                            shotFeature = " reb";
                          }
                          else{
                            shotFeature = "";
                          }
                          return d["etype"] + shotFeature;
                        };
        shotNodes.append("circle")
            .attr("r", 10)
            .attr("cx", shotX)
            .attr("cy", shotY)
            .attr("class", function(d) { return d["etype"] + " outer"});

        shotNodes.append("text")
            .attr("x", shotX)
            .attr("y", shotY)
            .attr("class", shotClass)
            .text(function(d) { return d["etype"][0];})
            .attr("transform", function(d) {  return "rotate(90," +(0.5 * RINK_CONFIG.RINK_LENGTH - d["newxc"] * rinkScale) + "," + (0.5 * RINK_CONFIG.RINK_WIDTH + d["newyc"] * rinkScale) +  ")"})
            .on("mouseover", function(d){
               d3.select(this)
                  .classed("select-sa", true);
                toolTipDiv.html(p.toolTipValue(d))
                  .style("left", ((d3.event.pageX) + 10) + "px")
                  .style("top", (d3.event.pageY) + "px")
                  .style("opacity", 1);
                p.parent.style("cursor", "pointer");
                toolTipDiv.style("visibility", "visible")
            })
            .on("mouseout", function(d){
                toolTipDiv.style("opacity", 0);
                p.parent.style("cursor", "crosshair");
                d3.select(this)
                  .classed("select-sa", false);
                toolTipDiv.style("visibility", "hidden")
            });

        // if horizontal, rotate second zone.
        if (p.horizontal){
            p.parent.selectAll(".zone2")
                .attr("transform", "rotate(180," +  RINK_CONFIG.RINK_LENGTH / 4 + "," +  RINK_CONFIG.RINK_WIDTH / 2 + ")translate(" + (-1 * RINK_CONFIG.RINK_LENGTH / 2) + ",0)" );
        }
        // if vertical, rotate both zones.
        else{
            p.parent.selectAll(".zone1")
                .attr("transform", "rotate(-90," +  RINK_CONFIG.RINK_LENGTH / 4 + "," +  RINK_CONFIG.RINK_WIDTH / 2 + ")translate(" + (-1*((RINK_CONFIG.RINK_LENGTH /2) - (RINK_CONFIG.RINK_WIDTH))) +"," + (-1 * p.margins.top) + ")");
                // .attr("transform", "rotate(-90," +  RINK_CONFIG.RINK_LENGTH / 4 + "," +  RINK_CONFIG.RINK_WIDTH / 2 + ")translate(" + (-1*((RINK_CONFIG.RINK_LENGTH /2) - (RINK_CONFIG.RINK_WIDTH)) - p.margins.top + p.margins.bottom) +"," + (0) + ")");
            p.parent.selectAll(".zone2")
                .attr("transform", "rotate(-90," +  RINK_CONFIG.RINK_LENGTH / 4 + "," +  RINK_CONFIG.RINK_WIDTH / 2 + ")translate(0," + ( RINK_CONFIG.RINK_WIDTH * 1.25) + ")");
        }

        function zoomHandler() {
          p.parent.select(".zones").attr("transform", "translate(" + d3.event.translate + ")scale(" + d3.event.scale + ")");
        }

        var zoomListener = d3.behavior.zoom()
          .scaleExtent([1, 5])
          .on("zoom", zoomHandler);

        zoomListener(p.parent);
        p.parent.attr("class", "shotPlot")
            .attr("width", RINK_CONFIG.RINK_WIDTH + p.margins.left + p.margins.right)
            .attr("height", (RINK_CONFIG.RINK_LENGTH/2) + p.margins.top + p.margins.bottom);
    }
    return chart;
};