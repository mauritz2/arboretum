let socket = io();
let current_player = null;
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
        console.log(item)
        console.log(item["player_id"])
        console.log(item["player_name"])
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

function update_current_player(player_name){
    current_player = player_name;
    console.log("Within update_cur-player" + current_player)
}

function update_game_phase(g_phase){
    console.log("Updating game phase!")
    game_phase = g_phase
}

function update_hand(cards_on_hand) {
    console.log("The current player value is " + current_player);
    console.log("The current game phase is " + game_phase);

    cards_on_hand.forEach(function (card) {
        $("#player_hand_div").append("" +
            "<div class='col-1'>" +
            "<div class='overlay-button-container'>" +
            "<img class='card_on_hand' src='../static/css/playing_cards/" + card + ".png'>" +
            "<div class='button_placeholder'>" +
            "</div>" +
            "</div>" +
            "</div>")


        if(current_player === true && game_phase == "Choose Card"){
            $(".button_placeholder").append(""+
                    "<form action='/choose_card_to_play' method='post'>" +
                    "<input name='card_name' type='hidden' value='" + card + "'>" +
                    "<input type='submit' class='btn btn-dark' value='Play card'>" +
                    "</form>"
            )
        }
        else if(current_player === true && game_phase == "Choose Discard"){
            console.log("Time to discard")
            $(".button_placeholder").append(""+
                    "<form action='/discard_card' method='post'>" +
                    "<input name='card_name' type='hidden' value='" + card + "'>" +
                    "<input type='submit' class='btn btn-dark' value='Discard card'>" +
                    "</form>")
        }

        else if(current_player === true && game_phase == "Draw"){
            console.log("Time to draw")
            $("#draw_button_placeholder").append("<input class='btn btn-dark' type='submit' value='Draw card'>")
        }
    })
}

function update_cards_left(cards_left){
    $("#cards_left").text(cards_left + " cards remain");
}


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
socket.on("update current player", (current_player) => update_current_player(JSON.parse(current_player)));
socket.on("update hand", (cards_on_hand) => update_hand(JSON.parse(cards_on_hand)));
socket.on("update game phase", (game_phase) => update_game_phase(JSON.parse(game_phase)));
socket.on("update cards left", (cards_left) => update_cards_left(JSON.parse(cards_left)));


/* Planning

// Display hands
Loop through the player ID and send each players and to their respective SIDs (no broadcast)

// Display play/discard buttons
1. Emit the current player SID
2. In front-end, check if the SID is the same as in "let session = {{ session | json }}
3. If it is, check what button to display (discard, draw)
4. If it's not, remove those buttons to make sure they're not displayed

// Display discard top cards
1. On discard, emit the latest graveyard cards
2. Listen for graveyard updates and refresh the graveyard piles with JS

// Play a card
1. From front-end emit play card event including the SID of the player + the card to play
2. Backend listens, changes the game state to choose cord etc.
x. Very similar with discard. Essentially replace the existing decorators with with the socketio.on decorators

*/