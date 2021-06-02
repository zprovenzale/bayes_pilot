var padding = 150
    , width = 200 - padding
    , height = 200 - padding
    // , color = ['#a6cee3','#1f78b4']; 
    , color = ['#67a9cf','#f7f7f7', ];
    //, color = ['#f0f0f0', '#6baed6']; //'#f0f0f0'];

// var values = [.05, .1, .25, .5, .75, .9, .95];
// var charts = ['circle', 'pie', 'donut', 'triangle', 'rect'];

// values.forEach(function(value, index){
//     var container = d3.select('body')
//         .append('div');
//     container.append('h1').text(value);

//     charts.forEach(function(chart){
//         var id = chart + '_' +  index; 

//         container.append('svg')
//             .attr('id', id)
//             .attr('width', width + padding)
//             .attr('height', height + padding);
        
//         window['draw_' + chart](value, id);

//     });
    

// });
Object.defineProperty(window, 'data', {
    // data getter
    get: function() { return _data; },
    // data setter
    set: function(value) {
        _data = value;
        // update the visualization each time the data property is set by using the equal sign (e.g. data = [])
        //updateVisualization()
    }
});

console.log("in visualization.js")
loadData()


function loadData(){

    d3.csv("modules/data/list_of_words.csv",function(csv) {
        data=shuffle(csv)
        words_data=data.slice(0,21)
        data_part2=data.slice(21,)
        console.log(words_data)
    })
}

function draw_primary(condition){
    console.log("in draw primary")

    var conditions=["vis","text","vis_text"]
    condition=shuffle(conditions)[0]
    console.log("condition is ",condition)

    if (condition=="text"){
        document.getElementById("vis_image").style.display="none"
    }
    if (condition=="vis"){
        document.getElementById("text_condition").style.display="none"
    }
}

function draw_secondary() {

    console.log("in draw secondary")
    console.log(words_data)

    let svgHeight = 400;
    let svgWidth = 820;
        
    let svgContainer = d3.select("#second_task")
                        .append("svg")
                        .attr("width", svgWidth+600)
                        .attr("height", svgHeight)
                        .attr("id", "secondContainer");

    var rect= svgContainer.append("rect")
                .attr("x",0)
                .attr("y",0)
                .attr("height",160)
                .attr("width",svgWidth+100)
                .attr("fill","black")

    var cyanRect= svgContainer.append("rect")
                .attr("x",svgWidth)
                .attr("y",30)
                .attr("height",30)
                .attr("width",80)
                .attr("fill","cyan")

    var cyanScore= svgContainer.append("text")
                        .attr("id","cyanScore")
                        .attr("fill","black")
                        .attr("x",svgWidth+40)
                        .attr("y",50)
                        .text("0")

    var magentaRect= svgContainer.append("rect")
                .attr("x",svgWidth)
                .attr("y",70)
                .attr("height",30)
                .attr("width",80)
                .attr("fill","magenta")

    var magentaScore= svgContainer.append("text")
                        .attr("id","magentaScore")
                        .attr("fill","black")
                        .attr("x",svgWidth+40)
                        .attr("y",90)
                        .text("0")

    var yellowRect= svgContainer.append("rect")
                .attr("x",svgWidth)
                .attr("y",110)
                .attr("height",30)
                .attr("width",80)
                .attr("fill","yellow")

    var yellowScore= svgContainer.append("text")
                        .attr("id","yellowScore")
                        .attr("fill","black")
                        .attr("x",svgWidth+40)
                        .attr("y",130)
                        .text("0")

    let svg = svgContainer.append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .attr("id", "second_svg");

    var word=svg.selectAll(".words")
                .data(words_data)
                .enter()
                .append("text")
                .attr("class", "words")
                .attr("padding",0.5)
                .attr("fill","white")
 // Update (set the dynamic properties of the elements)
    var yCoord=40

     word.attr("x", function(d,i){
            return (i%7)*100+20
        })
        .attr("y", function(d,i){
            if (i%7==0){
                if (i!=0){
                   yCoord+=40
                   return yCoord
                }
                else{
                    return yCoord
                }
            }
            else{
                console.log(yCoord)
                return yCoord
            }
        })
        .attr("dy", ".35em")
        .attr("id",function(d){
            return d
        })
        .text(function(d) { 
            return d.word;
        })
        .on("mouseover",function(d){
            d3.select(this).style("cursor", "pointer"); 
        })
        .on("click",function(d){
            console.log("clicked")
            if (d.fruit==1){
               console.log("in fruits")
               this.setAttribute("fill","cyan")
               //update score
               var cyanScore = parseInt(d3.select("#cyanScore").text())+1
               d3.select("#cyanScore").text(cyanScore)
            }
            else{
                this.setAttribute("fill","magenta")
                //update score
               var magentaScore = parseInt(d3.select("#magentaScore").text())+1
               d3.select("#magentaScore").text(magentaScore)
            }
            this.disabled=true

        })

     word.exit().remove()

     createLineUp()

     function createLineUp(){
      //=====DRAW LINEUP====
         var lineup=data_part2.slice(0,3)
         data_part2=data_part2.slice(3,)
         //loop back to start of list
         if (lineup.length==0){
            data_part2=shuffle(words_data)
             var lineup=data_part2.slice(0,3)
             data_part2=data_part2.slice(3,)
         }
        console.log("lineup is ",lineup)



         var wordNext=svg.selectAll("#lineup")
                    .data(lineup)
                    .enter()
                    .append("text")
                    .attr("id", "lineup")
                    .attr("class", "words")
                    .attr("padding",0.5)
                    .attr("fill",function(d){
                        console.log("in here")
                        return "white"
                    })
     // Update (set the dynamic properties of the elements)
        var yCoord=40

         wordNext.attr("x", function(d,i){
                return -50
            })
            .attr("y", function(d,i){
                if (i%1==0){
                    if (i!=0){
                       yCoord+=40
                       return yCoord
                    }
                    else{
                        return yCoord
                    }
                }
                else{
                    console.log(yCoord)
                    return yCoord
                }
            })
            .attr("dy", ".35em")
            .attr("id",function(d){
                return d
            })
            .text(function(d) { 
                return d.word;
            })
            .on("mouseover",function(d){
                d3.select(this).style("cursor", "pointer"); 
            })
            .on("click",function(d){
                console.log("clicked")
                if (d.fruit==1){
                   console.log("in fruits")
                   this.setAttribute("fill","cyan")
                   //update score
                   var cyanScore = parseInt(d3.select("#cyanScore").text())+1
                   d3.select("#cyanScore").text(cyanScore)

                }
                else{
                    this.setAttribute("fill","magenta")
                    //update score
                   var magentaScore = parseInt(d3.select("#magentaScore").text())+1
                   d3.select("#magentaScore").text(magentaScore)
                }
                this.disabled=true
            })

         wordNext.exit().remove()


        setTimeout(moveWords, 4000)
     }
   
     function moveWords(){
        console.log("in move words")
        //move containers
        d3.selectAll(".words")
          .transition()
          .duration(3000)
          .attr("x", function(d,i){
                var currX= +this.getAttribute('x')
                var wordColor=this.getAttribute('fill')
                var isFruit=d.fruit
                if ((currX>svgWidth) && (isFruit==1) && (wordColor=="white")){
                    var yellowScore= parseInt(d3.select("#yellowScore").text())+1
                    d3.select("#yellowScore").text(yellowScore)
                    this.remove()
                }
                return currX + 100
          })
        //check old group


        //create new lineup
        createLineUp()
     }
}

    function shuffle(array) {
      var currentIndex = array.length, temporaryValue, randomIndex;

      // While there remain elements to shuffle...
      while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = array[currentIndex];
        array[currentIndex] = array[randomIndex];
        array[randomIndex] = temporaryValue;
      }

      return array;
    }