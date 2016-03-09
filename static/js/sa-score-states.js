"use strict";

function dashboard(id, fData){
    var barColor = 'steelblue';

    // Set colors for updates from pie chart
    function segColor(c){ return {"Dog Friendliness":"#807dba", "Food Quality":"#41ab5d"}[c]; }
    
    // Compute total for each state in the list by passing each value in list to anonymous function
    fData.forEach(function(d){d.total=d.score["Dog Friendliness"]+d.score["Food Quality"];});
    
    // Function to handle histogram
    function histoGram(fD){
        var hG={},    hGDim = {t: 60, r: 7, b: 150, l: 60};
        hGDim.w = 800 - hGDim.l - hGDim.r,
        hGDim.h = 400 - hGDim.t - hGDim.b;
            
        // Select element with passed in id and within that element,
        // create svg for histogram with following attributes
        var hGsvg = d3.select(id)
            .append("svg")
            .attr("width", hGDim.w + hGDim.l + hGDim.r)
            .attr("height", hGDim.h + hGDim.t + hGDim.b)
            .append("g")
            .attr("transform", "translate(" + hGDim.l + "," + hGDim.t + ")");

        // Create x-axis mapping with range and domain (states in this case).
        // Notation: rangeRoundBands(interval[, padding[, outerPadding]])
        var x = d3.scale.ordinal().rangeRoundBands([0, hGDim.w], 0.2)
                .domain(fD.map(function(d) { return d[0]; }));

        // Add x-axis to the histogram svg.
        hGsvg.append("g")
             .attr("class", "x axis")
             .attr("transform", "translate(0," + hGDim.h + ")")
             .call(d3.svg.axis().scale(x).orient("bottom"))
            .selectAll("text")
             .attr("font-weight", "bold")
             .attr("dx", -5)
             .attr("dy", -.1)
             .attr("transform", "rotate(-45)")
             .style("text-anchor", "end");

        // Create y-axis mapping with range (y-axis starts from top)
        // and domain (d.total).
        var y = d3.scale.linear().range([hGDim.h, 0])
                .domain([0, d3.max(fD, function(d) { return d[1]; })]);

        // Create bars (with class bar) for histogram to contain rectangles
        // and score labels.
        var bars = hGsvg.selectAll(".bar").data(fD).enter()
                .append("g").attr("class", "bar");

        // Create the rectangles.
        bars.append("rect")
            .attr("x", function(d) { return x(d[0]); }) // state
            .attr("y", function(d) { return y(d[1]); }) // total
            .attr("id", function(d) { return d[0]; }) // state
            .attr("class", "d3-location")
            .attr("width", x.rangeBand())
            .attr("height", function(d) { return hGDim.h - y(d[1]); })
            .attr('fill',barColor) // defined above
            .on("mouseover",mouseover) // mouseover is defined below.
            .on("mouseout",mouseout) // mouseout is defined below.
            .on("click",click); // click is defined below.
            
        // Create the score labels above the rectangles.
        bars.append("text").text(function(d){ return d3.format(".3f")(d[1])})
            // Set label as 1.5 x-value 
            .attr("x", function(d) { return x(d[0])+x.rangeBand()/2; })
            // Set label as 5 units above y-value
            .attr("y", function(d) { return y(d[1])-5; })
            .attr("font-size", "13px")
            .attr("text-anchor", "middle");

        function mouseover(d){  // utility function to be called on mouseover.
            // filter for selected state.
            // Filter by state and get state object
            var st = fData.filter(function(s){ return s.State == d[0];})[0],
                // From state object, get type and value
                nD = d3.keys(st.score).map(function(s){ return {type:s, score:st.score[s]};});
               
            // Update pie-chart and legend.    
            pC.update(nD);
            leg.update(nD);
        }
        
        function mouseout(d){    // utility function to be called on mouseout.
            // reset pie-chart and legend.    
            pC.update(tF);
            leg.update(tF);
        }
        
        function click() {
            var location = this.id.split(",")[0];
            window.location = '/analysis/state?location=' + location;
        }

        // create function to update the bars. This will be used by pie-chart.
        hG.update = function(nD, color){
            // Update the domain of the y-axis map to reflect change in scores.
            y.domain([0, d3.max(nD, function(d) { return d[1]; })]);
            
            // Attach the new data to the bars.
            var bars = hGsvg.selectAll(".bar").data(nD);
            
            // Transition the height and color of rectangles.
            bars.select("rect").transition().duration(500)
                .attr("y", function(d) { return y(d[1]); })
                .attr("height", function(d) { return hGDim.h - y(d[1]); })
                .attr("fill", color);

            // transition the score labels location and change value.
            bars.select("text").transition().duration(500)
                .text(function(d){ return d3.format(".3f")(d[1]); })
                .attr("y", function(d) { return y(d[1])-5; });
        };
        return hG;
    }
    
    // function to handle pieChart.
    function pieChart(pD){
        var pC ={},    pieDim = {w:250, h: 500};
        pieDim.r = Math.min(pieDim.w, pieDim.h) / 2;
        
        // create svg for pie chart.
        var piesvg = d3.select(id).append("svg")
            .attr("width", pieDim.w)
            .attr("height", pieDim.h)
            .append("g")
            .attr("transform", "translate("+pieDim.w/2+","+pieDim.h/2+")");
        
        // create function to draw the arcs of the pie slices.
        var arc = d3.svg.arc().outerRadius(pieDim.r - 10).innerRadius(0);

        // create a function to compute the pie slice angles based on key-value.
        var pie = d3.layout.pie().sort(null).value(function(d) { return d.score; });

        // Draw the pie slices.
        piesvg.selectAll("path").data(pie(pD)).enter().append("path").attr("d", arc)
            // allows change based on histogram mouseover
            .each(function(d) { this._current = d; })
            // segColor defined above
            .style("fill", function(d) { return segColor(d.data.type); })
            .on("mouseover",mouseover) // defined below
            .on("mouseout",mouseout); // defined below

        // create function to update pie-chart. This will be used by histogram.
        pC.update = function(nD){
            piesvg.selectAll("path").data(pie(nD)).transition().duration(500)
                .attrTween("d", arcTween);
        };

        // Utility function to be called on mouseover a pie slice.
        function mouseover(d){
            // call the update function of histogram with new data.
            hG.update(fData.map(function(v){
                return [v.State,v.score[d.data.type]];}),segColor(d.data.type));
        }
        //Utility function to be called on mouseout a pie slice.
        function mouseout(d){
            // call the update function of histogram with all data.
            hG.update(fData.map(function(v){
                return [v.State,v.total];}), barColor);
        }
        // Animating the pie-slice requiring a custom function which specifies
        // how the intermediate paths should be drawn.
        function arcTween(a) {
            var i = d3.interpolate(this._current, a);
            this._current = i(0);
            return function(t) { return arc(i(t)); };
        }
        return pC;
    }
    
    // function to handle legend.
    function handlelegend(lD){
        var leg = {};
            
        // create table for legend.
        var legend = d3.select(id).append("table").attr('class','legend');

        // create labels for legend.

        // create one row per segment.
        var tr = legend.append("tbody").selectAll("tr").data(lD).enter().append("tr");
        
        // create the first column for each segment.
        tr.append("td").append("svg").attr("width", '16').attr("height", '16')
            .append("rect").attr("width", '16').attr("height", '16')
            .attr("fill",function(d){ return segColor(d.type); });

        // create the second column for each segment.
        tr.append("td").text(function(d){
            return d.type;
        });

        // create the third column for each segment.
        tr.append("td").attr("class",'legendScore')
            .text(function(d){ return d3.format(".3f")(d.score);});

        // create the fourth column for each segment.
        tr.append("td").attr("class",'legendPerc')
            .text(function(d){ return getLegend(d,lD);});

        // legend.tbody.append("tr");

        // Utility function to be used to update the legend.
        leg.update = function(nD){
            // update the data attached to the row elements.
            var l = legend.select("tbody").selectAll("tr").data(nD);

            // update the scores.
            l.select(".legendScore").text(function(d){ return d3.format(".3f")(d.score);});

            // update the percentage column.
            l.select(".legendPerc").text(function(d){ return getLegend(d,nD);});
        };
        
        function getLegend(d,aD){ // Utility function to compute percentage.
            return d3.format("%")(d.score/d3.sum(aD.map(function(v){ return v.score; })));
        }

        return leg;
    }

    // calculate total scores by segment for all state.
    var tF = ['Dog Friendliness','Food Quality'].map(function(d){
        return {type:d, score: d3.sum(fData.map(function(t){ return t.score[d];}))};
    });
    
    // calculate total score by state for all segment.
    var sF = fData.map(function(d){return [d.State,d.total];});

    var hG = histoGram(sF), // create the histogram.
        pC = pieChart(tF), // create the pie-chart.
        leg= handlelegend(tF);  // create the legend.
}
