var mymap = L.map('mapid').setView([48.5746963022463,19.5249155786772], 7);
var players = [];
var player = 1;

function init() {
  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
    maxZoom: 18,
    attribution: '',
    id: 'mapbox.streets'
  }).addTo(mymap);

  players.push(generate(0));
  players.push(generate(1));

  mymap.on('click', function(e) {
    style = players[player].style;
    players[player].distance += 0;

    $.post( "/colonise", { lat: e.latlng.lat, lng: e.latlng.lng, distance: players[player].distance }, function(data) {
      L.geoJSON(jQuery.parseJSON(data['result']), style).addTo(mymap);
      var manipulated = data['manipulated'];
      manipulated = parseInt(manipulated);
      if (manipulated > 0) {
        players[player].score += manipulated;
      }
      $(players[player].container).text(numberWithCommas(players[player].score));
      changePlayer();
    });

    $.get( "/close_villages", { lat: e.latlng.lat, lng: e.latlng.lng}, function(data) {
      for (var i in data['result']) {  
        $('#output-town-'+i).text((data['result'][i][0]));
        $('#output-population-'+i).text((data['result'][i][1]));
        $('#output-label-'+i).text((data['result'][i][2]));
        $('#output-distance-'+i).text(parseInt(parseFloat(data['result'][i][3])/1.5));
      }
    });
  });
}   

function upgrade(player) {
  players[player].distance+=5000;
  changePlayer();
}

function changePlayer() {
  player = 1 - player;
  $(".part").toggleClass( 'disabled' );
}

function generate(i) {
  return {
    style: i == 0 ? {style: {color: '#F00', weight: 0}} : {style: {color: '#00F', weight: 0}},
    score: 0,
    container: '#player_' + i,
    distance: 10000
  }
}

function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}
