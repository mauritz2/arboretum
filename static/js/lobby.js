var socket = io();
console.log("I loaded!")
socket.on('connect', function() {
    socket.emit('my event', {data: 'I\'m connected!'});
});


$(document).ready(function(){
    $('.sit_down_form').submit(function(event) {
        console.log("Standing up!")
        //var player_name = event.currentTarget[0].value;
        player_name = $("#player_name_input").val();
        socket.emit('sit_down', {player_name: player_name});
        return false;
    });
});

$(document).ready(function(){
    $("#leave_game").click(function(){
        socket.emit("stand_up")
    })

})

socket.on("new player", function(current_players){
    current_players = JSON.parse(current_players).Players;
    console.log("I am the frontend and I will now update the player list");
    console.log(current_players);

    $("#player_list").empty()

    current_players.forEach((player_name) => {
        $("#player_list").append("<li>" + player_name + "</li>");
    });
});

socket.on("message", function(message){
    console.log(message)
    showMessage(JSON.parse(message).text, JSON.parse(message).category);
});

function showMessage(text, category) {
  // Displays a message on top of the screen
  let message_div = document.getElementById("messages");
  alert_class = "alert" + "-" + category
  message_div.classList.add("alert", alert_class);
  message_div.innerHTML = text;
}


//// SocketIO socket
//// const socket = io();
//socket.on('error', (error) => console.error('SocketIO error ', error));
//// When socket connected, request for the game state
//socket.on('connect', () => socket.emit('get game', JSON.stringify({id: game_id})));
//// When receiving the game state, show it
//socket.on('game', (game, score) => Queue.enqueue(() => showState(JSON.parse(game), JSON.parse(score))));
//// When receiving info that game changed, request the game state
//socket.on('game changed', () => socket.emit('get game', JSON.stringify({id: game_id})));
//// Show alert messages
//socket.on('message', (data) => showMessage(JSON.parse(data).text, JSON.parse(data).category));
//// If game ended, show the result overlay
//socket.on('game ended', (data) => Queue.enqueue(() => showResult(JSON.parse(data))));
//// If match ended, show the result overlay
//socket.on('match ended', (data) => Queue.enqueue(() => showEnd(JSON.parse(data))));