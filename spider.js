
var candidate = {'trump': words_trump, 'clinton': words_clinton}

for (person in candidate) {
    person = person
    console.log('rendering ' + person + 's words!');
    words = candidate[person]
    align = ''
    if (person === 'trump') {
        align = 'left';
    }
    else {
        align = 'right';
    }
    var color = d3.scale.linear()
            var color = d3.scale.linear()
                .domain([0,5,20,35,50,60,65,70,80,90,100])
                .range(["#0806B7", "#555CC1", "#848FC7", "#A3B2CC", "#999", "#888", "#777", "#666", "#555", "#444", "#333", "#222"]);

    d3.layout.cloud().size([600, 700])
            .words(words)
            .rotate(0)
            .fontSize(function(d) { return d.size; })
            .on("end", draw)
            .start();

    function draw(words) {
        d3.select("body").select('div.' + person).append("svg")
                .attr("width", 650)
                .attr("height", 750)
                .attr("class", "wordcloud")
                .append("g")
                // without the transform, words words would get cutoff to the left and top, they would
                // appear outside of the SVG area
                .attr("transform", "translate(200,300)")
                .selectAll("text")
                .data(words)
                .enter().append("text")
                .style("font-size", function(d) { return d.size + "px"; })
                .style("fill", function(d, i) { return color(i); })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .text(function(d) { return d.text; });
    }

}