// SOCKET EVENT LISTENERS
socket.on("redirect", (url) => navigate_to_page(JSON.parse(url)));
socket.on("update player list", (current_players) => update_players(JSON.parse(current_players)));

// JQUERY EVENT LISTENERS
$(function(){
    $("#start_button").on("click", function(){
        event.preventDefault()
        socket.emit("start game");
    });
});

$(function(){
    $('#join_game').on("click", function (){
        event.preventDefault()
        let player_name = $("#player_name_input").val();
        socket.emit('sit down', player_name);
    });
});

$(function(){
    $("#leave_game").on("click", function(){
        event.preventDefault()
        socket.emit("stand up");
    });
});

// FUNCTIONS
function update_players(current_players){
    let player_list = $("#player_list");
    player_list.empty();

    Array.from(current_players).forEach(function(player){
        let player_el = "<li>" + player + "</li>";
        player_list.append(player_el);
    });
}

function navigate_to_page(url){
    // Used to start and end the game by navigating to the start and game over URls when needed
    window.location = url;
}


