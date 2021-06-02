    let svgHeight = 400;
    let svgWidth = screen.width;
        
    let svg = d3.select("#second_task")
	.append("svg")
	.attr("width", svgWidth)
	.attr("height", svgHeight)
	.attr("id", "second_svg");


	let rect=d3.rect()
				.attr("height",svgHeight)
				.attr("width",svgWidth)
				.attr("fill","navy")
