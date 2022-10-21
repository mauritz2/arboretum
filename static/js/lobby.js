let socket = io();
// let is_current_player = null;
// let game_phase = null;

function join_game(player_name){
        socket.emit('sit_down', {player_name: player_name});
}


$(function()  {
    $('#join_game').click(function call_join_game () {
        let player_name = $("#player_name_input").val();
        join_game(player_name);
        // This return false; is very important. Otherwise, the form refreshes the page
        // which makes the new player not show up on the screen.
        // This also resets the flask.request.sid for some reason which messes up how the app
        // keeps track of players.
        return false;
    });
});


$(function(){
    $("#leave_game").click(function(){
        socket.emit("stand_up")
    });
});

function update_players(current_players) {
    $("#player_list").empty();

    $.each(current_players, function (i, item) {
        let player_id = item["player_id"]
        let player_name = item["player_name"]
        $("#player_list").append("<li>" + player_id + " - " + player_name + "</li>");
    });
}

function show_message(text, category) {
  // Displays a message on top of the screen
  let message_div = document.getElementById("messages");
  let alert_class = "alert" + "-" + category
  message_div.classList.add("alert", alert_class);
  message_div.innerHTML = text;
}

// function update_current_player(player_name){
//     current_player = player_name;
//     console.log("Within update_cur-player" + current_player)
// }

function update_game_phase(g_phase, is_cur_player){
    //console.log(game_phase_dict)
    console.log("Updating game phase to " + g_phase)
    console.log("Updating is current player to " + is_cur_player)
    
    game_phase = g_phase
    is_current_player = is_cur_player
    
    //socket.emit("get current player")

    console.log(is_cur_player)
    console.log(typeof(is_cur_player))



    // Draw button
    if(is_current_player === true && game_phase === "Draw"){
        console.log("Showing draw button")
        $("#draw_button_container").removeClass("hide_button");
    }
    else{
        console.log("Hiding draw button")
        $("#draw_button_container").addClass("hide_button");
    }

    $(".card_to_play").submit(function (event){
        console.log("Playing card" + event.currentTarget[0].value)
        let card_to_play = event.currentTarget[0].value
        socket.emit("choose card to play", card_to_play);
    });
}

function update_hand(cards_on_hand) {
    console.log(cards_on_hand)

    $("#player_hand_div").empty();

    cards_on_hand.forEach(function (card) {

        $("#player_hand_div").append("" +
            "<div class='col-1'>" +
            "<div class='overlay-button-container'>" +
            "<img class='card_on_hand' src='../static/css/playing_cards/" + card + ".png'>" +
            "<form class='card_to_play hide_button'>" +
            "<input name='card_name' type='hidden' value='" + card + "'>" +
            "<input type='submit' class='btn btn-dark' value='Play card'>" +
            "</form>" +
            "<form class='discard_btn hide_button'>" +
            "<input name='card_name' type='hidden' value='" + card + "'>" +
            "<input type='submit' class='btn btn-dark' value='Discard card'>" +
            "</form>" +
            "</div>" +
            "</div>")


    });

    // TODO - verify again if these truly have to be nested in this func. Can't they be outside?
    $(".card_to_play").submit(function (event){
        // Add prevent default back once board is generated through sockerio
        //event.preventDefault();
        console.log("Playing card" + event.currentTarget[0].value)
        let card_to_play = event.currentTarget[0].value
        socket.emit("choose card to play", card_to_play);
    });

    $(".discard_btn").on("submit", function (event){
        event.preventDefault();
        console.log("Discarding card" + event.currentTarget[0].value)
        let card_to_discard = event.currentTarget[0].value
        socket.emit("discard card", card_to_discard);
    });
}

function update_cards_left(cards_left){
    $("#cards_left").text(cards_left + " cards remain");
}

function update_discard(top_discard_cards) {
    console.log(top_discard_cards)

    $("#discard_div").empty();

    Object.entries(top_discard_cards).forEach(([player, card]) => {

        if(card == null){
            // TODO - blank-w border currently exists in two folders- refactor into tiles and cards
            card = "blank-w-border"
        };

        $("#discard_div").append("" +
            '<p class="mb-0 mt-3"><strong>Discard pile</strong></p>' +
            '<p><small>' + player + '</small></p>' +
            '<div class="overlay-button-container">' +
            '<img class="card_on_hand" src="../static/css/playing_cards/' + card + '.png">' +
            '<form class="draw_discard_btn hide_button">' +
            '<input name="discard_owner" type="hidden" value="'+ player +'">' +
            '<input class="btn btn-dark" type="submit" value="Draw card">' +
            '</form>' +
            '</div>')
    });
}

function update_board_state(game_state){
    console.log(game_state);
    console.log(game_state["game_phase"]);
    console.log(game_state["is_current_player"]);
    console.log(game_state["num_cards_in_deck"]);

    // Update the global state variables
    game_phase = game_state["game_phase"];
    is_current_player = game_state["is_current_player"];

    // Update amount of cards remaining
    update_cards_left(game_state["num_cards_in_deck"]);

    // Update discard piles
    update_discard(game_state["top_discard_cards"]);


    // Show/hide buttons based on game state - this has to happen last - otherwise not all elements will exist yet
    toggle_buttons(game_phase, is_current_player);



    // Show/hide buttons

    // Helper function to call all funcs to update the game state
    // A large helper func is used as opposed to one emit per board item to make the code simpler to troubleshoot

    // Update the game phase
    // Update the current player

    // Update player hands
    // Update remaining cards in hand
    // Update top discard decks


    // Assign bindings to elements that didn't exist before (?)
}

function toggle_buttons(game_phase, is_current_player){
    console.log("Evaluating what buttons to show")

    // Draw button!
    if (is_current_player === true && game_phase === "Choose Card"){
        console.log("Showing play button")
        $(".card_to_play").removeClass("hide_button");
    }
    else{
        $(".card_to_play").addClass("hide_button");
    }

    // Discard button
    if(is_current_player === true && game_phase === "Choose Discard"){
        console.log("Showing discard button")
        $(".discard_btn").removeClass("hide_button");
    }
    else{
        $(".discard_btn").addClass("hide_button");
    }

    // Draw button
    if(is_current_player === true && game_phase === "Draw"){
        console.log("Showing draw button")
        $("#draw_button_container").removeClass("hide_button");
        $(".draw_discard_btn").removeClass("hide_button");
    }
    else{
        console.log("Hiding draw button")
        $("#draw_button_container").addClass("hide_button");
        $(".draw_discard_btn").addClass("hide_button");
    }
}


// JQUERY HTML BINDINGS

$(function(){
    $("#draw_button").on("click",function ()
    {
        console.log("Drawing button was clicked!")
        socket.emit("draw card")
    });
});



// SOCKET LISTENERS
socket.on("message", (message) => show_message(JSON.parse(message).text, JSON.parse(message).category));
socket.on("update player list", (current_players) => update_players(JSON.parse(current_players)));
// socket.on("update current player", (current_player) => update_current_player(JSON.parse(current_player)));
socket.on("update hand", (cards_on_hand) => update_hand(JSON.parse(cards_on_hand)));
// socket.on("update game phase", (game_phase_dict) => update_game_phase(JSON.parse(game_phase_dict).game_phase, JSON.parse(game_phase_dict).is_current_player));
// socket.on("update cards left", (cards_left) => update_cards_left(JSON.parse(cards_left)));
socket.on("update board state", (board_state) => update_board_state(JSON.parse(board_state)));




        // if(current_player === true && game_phase == "Choose Card"){
        //     $(".button_placeholder").append(""+
        //             "<form class='card_to_play'>" +
        //             "<input name='card_name' type='hidden' value='" + card + "'>" +
        //             "<input type='submit' class='btn btn-dark' value='Play card'>" +
        //             "</form>"
        //     )
        //     )        $("#player_hand_div").append("" +
        //     "<div class='col-1'>" +
        //     "<div class='overlay-button-container'>" +
        //     "<img class='card_on_hand' src='../static/css/playing_cards/" + card + ".png'>" +
        //     "<div class='button_placeholder'>" +
        //     "</div>" +
        //     "</div>" +
        //     "</div>")
        //
        //
        // if(current_player === true && game_phase == "Choose Card"){
        //     $(".button_placeholder").append(""+
        //             "<form class='card_to_play'>" +
        //             "<input name='card_name' type='hidden' value='" + card + "'>" +
        //             "<input type='submit' class='btn btn-dark' value='Play card'>" +
        //             "</form>"
        //     )
        //}

        // if(current_player === true && game_phase == "Choose Discard"){
        //     console.log("Time to discard")
        //     $(".button_placeholder").append(""+
        //             "<form action='/discard_card' method='post'>" +
        //             "<input name='card_name' type='hidden' value='" + card + "'>" +
        //             "<input type='submit' class='btn btn-dark' value='Discard card'>" +
        //             "</form>")
        // }