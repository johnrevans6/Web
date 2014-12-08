$(document).ready(function(){

    namespace = '/service'; 

    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('event', {data: 'Connected!'});
    });
    
    socket.on('response', function(msg) {
        $('#log').append('<br>Received #' + msg.count + ': ' + msg.data);
    });       
  
    $('form#send').submit(function(event) {
        socket.emit('broadcast event', {data: $('#broadcast_data').val(),language: $('.btn:first-child').text()});
        return false;
    });                             
});