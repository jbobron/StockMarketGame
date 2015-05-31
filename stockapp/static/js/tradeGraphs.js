queue()
    .defer(d3.json, "/trade")
    // .defer(d3.json, "static/geojson/us-states.json")
    .await(makeGraphs);

function makeGraphs(error, projectsJson, statesJson) {
  //Clean projectsJson data
  var dataArray = document.getElementById('data').innerText;
  // var jsonObj= {};
  // for(var i = 0; i < dataArray.length; i++){
  //   jsonObj[i] = JSON.parse("[" + i + "]");
  //   // jsonObj[key] = dataArray[key];
  // }
  // var date = new Date();
  var temp = '{"High":456, "Low":456, "Volume":45600, "Date":"2015-05-22"}'
  var data = covertToJson(dataArray)
  var stockData = JSON.parse(data);

  console.log("hello", stockData);
  console.log(typeof(stockData))
  var dateFormat = d3.time.format("%Y-%m-%d");

  stockData.forEach(function(d) {
    // if(d['Date'].slice(0,4) === "2015") console.log(d["Date"])
    d["Date"] = dateFormat.parse(d["Date"]);
    // console.log(d["Date"])
    // console.log(d);
    // console.log('HEEEL')
  });

  // //Create a Crossfilter instance
  var ndx = crossfilter(stockData);

  // //Define Dimensions
  var dateDim = ndx.dimension(function(d) { return d["Date"]; });
  // var highDim = ndx.dimension(function(d) { return d["High"]; });
  // var lowDim = ndx.dimension(function(d) { return d["Low"]; });
  var openDim = ndx.dimension(function(d) { return d["Open"]; });
  // var closeDim = ndx.dimension(function(d) { return d["Close"]; });
  var volDim = ndx.dimension(function(d) { return d["Volume"]/1000000; });
  var numVolumeByDate = dateDim.group().reduceSum(function(d) { return d['Volume']/1000000; });
  var numOpenByDate = dateDim.group().reduceSum(function(d) { return d['Open']; });

  var all = ndx.groupAll();

  var temp = dateDim.bottom(100);
  var minDate = dateDim.bottom(1)[0]["Date"];
  var i = 0;
  // console.log("MinDate",minDate, "temp", temp)
  while(minDate < temp){
    minDate = temp[i]["Date"];

    i++;
  }
  var maxDate = dateDim.top(1)[0]["Date"];

  console.log(minDate);
  console.log(maxDate);

  //   //Charts
  // var priceChart = dc.barChart("#price-chart");
  var openChart = dc.barChart("#open-chart");
  // // var resourceTypeChart = dc.rowChart("#resource-type-row-chart");
  // // var povertyLevelChart = dc.rowChart("#poverty-level-row-chart");
  // // var usChart = dc.geoChoroplethChart("#us-chart");
  // // var numberProjectsND = dc.numberDisplay("#number-projects-nd");
  // // var totalDonationsND = dc.numberDisplay("#total-donations-nd");

  // // numberProjectsND
  // //   .formatNumber(d3.format("d"))
  // //   .valueAccessor(function(d){return d; })
  // //   .group(all);

  // // totalDonationsND
  // //   .formatNumber(d3.format("d"))
  // //   .valueAccessor(function(d){return d; })
  // //   .group(totalDonations)
  // //   .formatNumber(d3.format(".3s"));

  // priceChart
  //   .width(500)
  //   .height(160)
  //   .margins({top: 10, right: 50, bottom: 30, left: 50})
  //   .dimension(dateDim)
  //   .group(numVolumeByDate)  //change
  //   .transitionDuration(500)
  //   .x(d3.time.scale().domain([minDate, maxDate]))
  //   .elasticY(true)
  //   // .xAxisLabel("Year")
  // //   .yAxis().ticks(4);

  openChart
    .width(1000)
    .height(160)
    .margins({top: 10, right: 50, bottom: 30, left: 50})
    .dimension(dateDim)
    .group(numOpenByDate)  //change
    .transitionDuration(500)
    .x(d3.time.scale().domain([minDate, maxDate]))
    .elasticY(true)
    .xAxisLabel("Year")
    .yAxis().ticks(4);

  // // resourceTypeChart
  // //       .width(300)
  // //       .height(250)
  // //       .dimension(resourceTypeDim)
  // //       .group(numProjectsByResourceType)
  // //       .xAxis().ticks(4);

  // // povertyLevelChart
  // //   .width(300)
  // //   .height(250)
  // //       .dimension(povertyLevelDim)
  // //       .group(numProjectsByPovertyLevel)
  // //       .xAxis().ticks(4);


  // // usChart.width(1000)
  // //   .height(330)
  // //   .dimension(stateDim)
  // //   .group(totalDonationsByState)
  // //   .colors(["#E2F2FF", "#C4E4FF", "#9ED2FF", "#81C5FF", "#6BBAFF", "#51AEFF", "#36A2FF", "#1E96FF", "#0089FF", "#0061B5"])
  // //   .colorDomain([0, max_state])
  // //   .overlayGeoJson(statesJson["features"], "state", function (d) {
  // //     return d.properties.name;
  // //   })
  // //   .projection(d3.geo.albersUsa()
  // //           .scale(600)
  // //           .translate([340, 150]))
  // //   .title(function (p) {
  // //     return "State: " + p["key"] + "\n" + "Total Donations: " + Math.round(p["value"]) + " $";
  // //   });

    dc.renderAll();

};



function covertToJson(data){
  return data.replace(/\'/g, "\"");
}

