google.load("visualization", "1", {packages:["corechart"]});
google.setOnLoadCallback(processCharts);

function processCharts() {
  charts = $('.wordChart')

  charts.each(function() {    
    
    var json_data = JSON.parse($(this).html())
    var data = google.visualization.arrayToDataTable(json_data);    
    var article_source = $(this).attr('data-articlesource')
    var article_title = $(this).attr('data-articletitle')
    
    var options = {
      legend: 'none',
      pieSliceText: 'label',
      title: article_source + " - " + article_title,
      pieStartAngle: 120,      
    };

    var article_id = $(this).attr('data-articleid')
    var chart = new google.visualization.PieChart(document.getElementById(article_id));
    chart.draw(data, options);
    
  });

}