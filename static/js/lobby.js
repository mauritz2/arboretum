let socket = io();

$(function() {
    $('#join_game').click(function () {
        let player_name = $("#player_name_input").val();
        socket.emit('sit_down', {player_name: player_name});
        return false;
    });
});

$(function(){
    $("#leave_game").click(function(){
        socket.emit("stand_up")
    });
});

function update_players(current_players){
    console.log("Thanks for calling. I will update messages.")
    $("#player_list").empty();
    current_players.forEach((player_name) => {
        $("#player_list").append("<li>" + player_name + "</li>");
    });
}

function show_message(text, category) {
  // Displays a message on top of the screen
  let message_div = document.getElementById("messages");
  let alert_class = "alert" + "-" + category
  message_div.classList.add("alert", alert_class);
  message_div.innerHTML = text;
}

// Message listeners
socket.on("message", (message) => show_message(JSON.parse(message).text, JSON.parse(message).category));
socket.on("player change", (current_players) => update_players(JSON.parse(current_players).Players));
