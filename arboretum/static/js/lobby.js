// SOCKET LISTENERS
socket.on("redirect", (url) => navigate_to_page(JSON.parse(url)));
socket.on("update player list", (current_players) => update_players(JSON.parse(current_players)));



// JQUERY HTML BINDINGS
$(function(){
    $("#start_button").on("click", function()
    {
        console.log("Starting the game")
        socket.emit("start game");
    });
});


$(function()  {
    $('#join_game').on("click", function () {
        let player_name = $("#player_name_input").val();
        socket.emit('sit down', player_name);
        // This return false; is very important. Otherwise, the form refreshes the page
        // which makes the new player not show up on the screen.
        // This also resets the flask.request.sid for some reason which messes up how the app
        // keeps track of players.
        return false;
    });
});


$(function(){
    $("#leave_game").on("click", function(){
        socket.emit("stand up")
    });
});



// FUNCTIONS
function update_players(current_players) {
    const player_list = $("#player_list")
    player_list.empty();

    Array.from(current_players).forEach(function(player){
        console.log(player)
        let player_el = "<li>" + player + "</li>"
        player_list.append(player_el)
    });
}

function navigate_to_page(url){
    // Used to start or end the game
    console.log("I am navigating to " + url)
    window.location = url
}


