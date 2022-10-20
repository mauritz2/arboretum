let socket = io();
let is_current_player = null;
let game_phase = null;

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
            "<form class='discard_btn hide_button' method='post' action='/discard_card'>" +
            "<input name='card_name' type='hidden' value='" + card + "'>" +
            "<input type='submit' class='btn btn-dark' value='Discard card'>" +
            "</form>" +
            "</div>" +
            "</div>")

    })
    // console.log("Evaluating what buttons to show")
    // // Draw button!
    // if (current_player == true && game_phase === "Choose Card"){
    //     console.log("Showing play button")
    //     $(".card_to_play").removeClass("hide_button");
    // }
    // else{
    //     $(".card_to_play").addClass("hide_button");
    // }
    //
    // // Discard button
    // if(current_player === true && game_phase === "Choose Discard"){
    //     console.log("Showing discard button")
    //     $(".discard_btn").removeClass("hide_button");
    // }
    // else{
    //     $(".discard_btn").addClass("hide_button");
    // }
    //
    // // Draw button
    // if(current_player === true && game_phase === "Draw"){
    //     console.log("Showing draw button")
    //     $("#draw_button_container").removeClass("hide_button");
    // }
    // else{
    //     console.log("Hiding draw button")
    //     $("#draw_button_container").addClass("hide_button");
    // }
    //
    console.log("Evaluating what buttons to show with input as below")
    console.log("The current player value is " + is_current_player);
    console.log("The current game phase is " + game_phase);

    // Draw button!
    // TODO - not sure why these have to be in here, doesn't make sense to me - but they are most stable here
    if (is_current_player == true && game_phase === "Choose Card"){
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



    $(".card_to_play").submit(function (event){
        console.log("Playing card" + event.currentTarget[0].value)
        let card_to_play = event.currentTarget[0].value
        socket.emit("choose card to play", card_to_play);
    });
}

function update_cards_left(cards_left){
    $("#cards_left").text(cards_left + " cards remain");
}

$(function(){
    $("#draw_button").on("click",function ()
    {
        console.log("Drawing button was clicked!")
        socket.emit("draw card")
    });
});


// Used only for generating test data

// function random(min,max) {
//     return Math.floor((Math.random())*(max-min+1))+min;
// }

// io.on('connection', socket => {
//     console.log(socket.id)
// })

// socket.prependAny(() => {
//     console.log("Hand changing :-)")
//     socket.emit("hand change");
// });

// $(function(){
//     let names = ["Tom Bomb", "Frodo Bag", "G"];
//     join_game(names[random(0,2)]);
//     //socket.emit("draw_card")
// })

// Known times the SID refreshes
// 1. On page refresh

// End of test data generation functions

// Message listeners
socket.on("message", (message) => show_message(JSON.parse(message).text, JSON.parse(message).category));
socket.on("update player list", (current_players) => update_players(JSON.parse(current_players)));
//socket.on("update current player", (current_player) => update_current_player(JSON.parse(current_player)));
socket.on("update hand", (cards_on_hand) => update_hand(JSON.parse(cards_on_hand)));
socket.on("update game phase", (game_phase_dict) => update_game_phase(JSON.parse(game_phase_dict).game_phase, JSON.parse(game_phase_dict).is_current_player));
socket.on("update cards left", (cards_left) => update_cards_left(JSON.parse(cards_left)));


/* Planning

// Display hands
Loop through the player ID and send each player their respective SIDs (no broadcast)

// Display play/discard buttons
1. Emit the current player SID
2. In front-end, check if the SID is the same as in "let session = {{ session | json }}"
3. If it is, check what button to display (discard, draw)
4. If it's not, remove those buttons to make sure they're not displayed

// Display discard top cards
1. On discard, emit the latest graveyard cards
2. Listen for graveyard updates and refresh the graveyard piles with JS

// Play a card
1. From front-end emit play card event including the SID of the player + the card to play
2. Backend listens, changes the game state to choose cord etc.
x. Very similar with discard. Essentially replace the existing decorators with the socketio.on decorators

*/


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