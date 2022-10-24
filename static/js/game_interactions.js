let socket = io();
let my_uid = getCookie("player_uid")
const blank_card_name = "blank-w-border"


// SOCKET LISTENERS
socket.on("message", (message) => show_message(JSON.parse(message).text, JSON.parse(message).category));
socket.on("update hand", (cards_on_hand) => update_hand(JSON.parse(cards_on_hand)));
socket.on("update board state", (board_state) => update_board_state(JSON.parse(board_state)));
socket.on("end game", (url) => navigate_to_page(JSON.parse(url)));


// JQUERY HTML element bindings

$(function(){
    $("#draw_button").on("click",function ()
    {
        console.log("Drawing button was clicked!");
        socket.emit("draw card");
    });
});

// FUNCTIONS
function update_board_state(game_state){
    console.log(game_state)
    console.log("Game phase " + game_state["game_phase"]);
    console.log("Current player ID " + game_state["current_player_id"]["uid"]);
    console.log("Num cards in deck " + game_state["num_cards_in_deck"]["player_name"]);
    console.log("Player boards " + game_state["player_boards"])

    // Update the global state variables
    game_phase = game_state["game_phase"];
    let cur_player_uid = game_state["current_player_id"]["uid"];
    let cur_player_name = game_state["current_player_id"]["player_name"]

    // Update boards
    let player_boards = game_state["player_boards"]

    $("#side_board_container").empty();

    for (const board_uid of Object.keys(player_boards))
    {

        if(board_uid === cur_player_uid){
            update_main_board(player_boards[board_uid], cur_player_uid, cur_player_name);
        }
        else {
            console.log("Updating side board!")
            update_side_boards(player_boards[board_uid], cur_player_uid, cur_player_name);
        }
    }

    // current_player_board = game_state["player_boards"][cur_player_uid]

    // Update amount of cards remaining
    let num_cards_in_deck = game_state["num_cards_in_deck"]
    update_cards_left(num_cards_in_deck);

    // Update discard piles
    let top_discard_cards = game_state["top_discard_cards"]
    update_discard(top_discard_cards, cur_player_uid);

    // Show/hide buttons based on game state - this has to happen after hand and discard pile updates - otherwise not all elements will exist yet
    toggle_buttons(game_phase, cur_player_uid, num_cards_in_deck);

}

function update_side_boards(side_board, current_player_uid, current_player_name) {
    let side_board_el = $("#side_board_container");

    let content = ""
    content += "<p><strong>" + current_player_name + "'s board" + "</strong></p>"
    content += '<table className="table-sm">'

    for( const [row_index, row] of side_board.entries()){
        content += '<tr>'

        for (const [col_index, card] of row.entries(row)){
            content += '<td>'

             if (card != null) {
                content += '<img class="card_on_mini_board zoom-larger" src="../static/css/playing_cards/' + card + '.png">'
            } else {
                 content += '<img class="card_on_mini_board blank" src="../static/css/playing_cards/' + blank_card_name + '.png">'

             }
            content += '</td>'
        }
        content += '</tr>'
    }

    content += '</table>'
    side_board_el.append(content);
}


function toggle_buttons(game_phase, cur_player_uid, num_cards_in_deck){
    console.log("Evaluating what buttons to show");
    console.log("The cur UID is " + cur_player_uid);

    // Play button
    if (cur_player_uid === my_uid && game_phase === "Choose Card"){
        console.log("Showing play button")
        $(".card_to_play").removeClass("hide_button");
    }
    else{
        $(".card_to_play").addClass("hide_button");
    }

    // Discard button
    if(cur_player_uid === my_uid && game_phase === "Choose Discard"){
        console.log("Showing discard button")
        $(".discard_btn").removeClass("hide_button");
    }
    else{
        $(".discard_btn").addClass("hide_button");
    }

    console.log("The amount of cards in the deck is " + num_cards_in_deck)
    console.log((cur_player_uid === my_uid && game_phase === "Draw") && num_cards_in_deck > 0)
    // Draw button
    if((cur_player_uid === my_uid && game_phase === "Draw") && num_cards_in_deck > 0){
        // TODO - only show this if there's more than 0 card sin the discard piles and draw deck!
        // Reduce the height of the discard piles so they don't push down the cards too much
        // Replace the cards on hand and cards on board with em things?
        console.log("Showing draw button")
        $("#draw_button_container").removeClass("hide_button");
        //$(".draw_discard_btn").removeClass("hide_button");
    }
    else{
        console.log("Hiding draw button")
        $("#draw_button_container").addClass("hide_button");
        //$(".draw_discard_btn").addClass("hide_button");
    }
}

function getCookie(cname) {
  let cookies = ` ${document.cookie}`.split(";");
  let val = "";
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].split("=");
    if (cookie[0] == ` ${cname}`) {
      return cookie[1];
    }
  }
  return "";
}

function update_main_board(main_board, current_player_uid, current_player_name) {

    $("#main_board_title").text("Current player's board (" + current_player_name + ")")

    let board = $("#main_board")
    board.empty();

    for (const [row_index, row] of main_board.entries()) {
        let content = '<tr>'
        for (const [col_index, card] of row.entries()) {
            content += "";
            content += '<td>'

            let card_name = card

            if (card_name != null) {
                content += '<img class="card_on_board zoom" id="' + row_index + col_index + '" src="../static/css/playing_cards/' + card_name + '.png">'
            } else {

                if (game_phase === "Choose Coords" && current_player_uid === my_uid)  {
                    content += '<form class="choose_coord_btn">'
                    content += '<input name="coords" type="hidden" value="' + row_index + col_index + '">'
                    content += '<input class="card_on_board blank_choose_coord" src="../static/css/playing_cards/' + blank_card_name + '.png" type="image">'
                    content += '</form>'
                } else {
                    content += '<form>'
                    content += '<input disabled class="card_on_board blank" id="' + row_index + col_index + '"  src="../static/css/other/' + blank_card_name + '.png" type="image">'
                    content += '</form>'
                }
            }
            content += '</td>'
        }
        content += '</tr>'
        content += '</tr>'
        board.append(content)
    }

    $(".choose_coord_btn").on("submit", function (event){
    event.preventDefault();
    console.log("Choosing coords: " + event.currentTarget[0].value)
    let coords_to_place_card = event.currentTarget[0].value
    socket.emit("choose coords", coords_to_place_card);
    });


}

function show_message(text, category) {
  // Displays a message on top of the screen
  let message_div = document.getElementById("messages");
  let alert_class = "alert" + "-" + category
  message_div.classList.add("alert", alert_class);
  message_div.innerHTML = text;
}

function update_hand(cards_on_hand) {
    console.log(cards_on_hand)

    $("#player_hand_div").empty();

    cards_on_hand.forEach(function (card) {

    // TODO - verify again if these truly have to be nested in this func. Can't they be outside?

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

    $(".card_to_play").on("submit", function (event){
        event.preventDefault();
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

function update_discard(top_discard_cards, cur_player_uid) {
    console.log(top_discard_cards)

    $("#discard_div").empty();

    Object.entries(top_discard_cards).forEach(([player, card]) => {

        let content = ""
        content += '<p class="mb-0 mt-3"><strong>Discard pile</strong></p>'
        // Replace here with the actual player's name
        content += '<p><small>' + player + '</small></p>'
        content += '<div class="overlay-button-container">'

        if(card === null)
        {
            content += '<img class="card_on_hand blank" src="../static/css/playing_cards/' + blank_card_name + '.png">'
        }
        else
        {
            content += '<img class="card_on_hand" src="../static/css/playing_cards/' + card + '.png">'
        }
        content += '<form class="draw_discard_btn '

        // # TODO - update this and all element creations
        if (cur_player_uid !== my_uid || game_phase !== "Draw" || card === null) {
            // Unless the current player UID === my_uid
            // TODO - refactor!
            // Adding hide_buttons hides the button
            // There are three scenarios where we want to add this call (i.e. hide it)
            // When it's not your turn we want it to be true: !(cur_player_uid !== my_uid)
            // When it's not the draw phase we want it to be true (ie. !(game_phase !== "Draw")
            content += 'hide_button'
        }
        content += '">'
        content += '<input name="discard_owner" type="hidden" value="'+ player +'">'
        content += '<input class="btn btn-dark" type="submit" value="Draw card">'
        content += '</form>'
        content += '</div>'

        $("#discard_div").append(content)

    });

    // TODO - rename to consistent naming, e.g. btn is not a btn, it's a form
    // TODO - split js into separate files so it makes sense
    $(".draw_discard_btn").on("submit", function(event) {
        event.preventDefault();
        let player_to_draw_from = event.currentTarget[0].value;
        console.log("Drawing from discard: " + player_to_draw_from);
        socket.emit("draw from discard", player_to_draw_from);
    });
}
