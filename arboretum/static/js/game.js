// Move the HTML bindings to one func

// Globals
const socket = io(); // to emit events and listen for events
const my_uid = getCookie("player_uid") // the player user ID (e.g. 123)
const blank_card_name = "blank-w-border" // the filename for the blank card png

// SOCKET EVENT LISTENERS
socket.on("message", (message) => show_message(JSON.parse(message)["text"], JSON.parse(message)["category"]));
socket.on("update hand", (cards_on_hand) => update_hand(JSON.parse(cards_on_hand)));
socket.on("update board state", (board_state) => update_board_state(JSON.parse(board_state)));

// JQUERY EVENT LISTENERS
$(function(){
    // $function() is needed since otherwise the event listener is applied before the page completely load. This leads
    // to that the button doesn't do anything.
    $("#draw_button").on("click",function () {
        socket.emit("draw card");
    });
});

$(document).on("submit", ".choose_coord_btn", function (event) {
    // The submit event is applied to $(document) since the board gets dynamically re-created. Therefore, the
    // on() has to be applied to something that doesn't get deleted, i.e. the document. Same explanation applies to all
    // event listeners on dynamic content in this file
    event.preventDefault();
    socket.emit("choose coords", event.currentTarget[0].value);
});

$(document).on("submit", ".card_to_play", function (event){
    event.preventDefault();
    socket.emit("choose card to play", event.currentTarget[0].value);
});

$(document).on("submit", ".discard_btn_container", function (event){
    event.preventDefault();
    socket.emit("discard card", event.currentTarget[0].value);
});

$(document).on("submit", ".draw_discard_form", function(event) {
    event.preventDefault();
    socket.emit("draw from discard", event.currentTarget[0].value);
});

// BOARD STATE UPDATE FUNCTIONS
function update_board_state(game_state){
    // This is the main function that manages the board state update

    // Get data from the game state
    let game_phase = game_state["game_phase"];
    let cur_player_uid = game_state["current_player_id"]["uid"];
    let cur_player_name = game_state["current_player_id"]["player_name"];
    let player_boards = game_state["player_boards"];
    let num_cards_in_deck = game_state["num_cards_in_deck"];
    let uid_to_player_map = game_state["uid_to_player_map"];


    // Update game phase player message
    update_game_status_heading(cur_player_name, game_phase);

    // Update boards
    $("#side_board_container").empty();
    for (const board_uid of Object.keys(player_boards)) {
        if(board_uid === cur_player_uid){
            // Create this board as the main board on the screen
            update_main_board(player_boards[board_uid], game_phase, cur_player_uid, cur_player_name);
        }
        else {
            let board_owner_name = uid_to_player_map[board_uid]
            // Create these boards as the smaller boards on the screen
            update_side_board(player_boards[board_uid], board_owner_name);
        }
    }

    // Update amount of cards remaining in deck
    update_cards_left(num_cards_in_deck);

    // Update discard piles
    let top_discard_cards = game_state["top_discard_cards"];
    update_discard(top_discard_cards, cur_player_uid, game_phase);

    // Show/hide buttons based on game state - this has to happen after hand and discard pile updates - otherwise not all elements will exist yet
    toggle_buttons(game_phase, cur_player_uid, num_cards_in_deck);

}

function update_game_status_heading(current_player_name, game_phase) {
        // Sets the player message to show who's currently playing and what they're currently doing
        $("#main_board_title").text(current_player_name + " is currently in the " + game_phase.toLowerCase() + " phase");
}

function update_side_board(board_data, board_owner_name){
    let side_board_el = $("#side_board_container");

    // Creating HTML elements like this is used a lot in this file. It's the best way I found to create elements,
    // using something like React would make this a lot clearer
    let side_board = "";
    side_board += "<p><small>" + board_owner_name + "'s board" + "</small></p>";
    side_board += '<table class="table-condensed">';

    for (const row of board_data.values()){
        side_board += '<tr>';
        for (const card of row.values()){
            side_board += '<td>';
             if (card != null) {
                side_board += '<img class="card_on_mini_board zoom-larger" src="../static/css/playing_cards/' + card + '.png">';
             }
             else {
                 side_board += '<img class="card_on_mini_board dimmed" src="../static/css/playing_cards/' + blank_card_name + '.png">';
             }
            side_board += '</td>';
        }
        side_board += '</tr>';
    }
    side_board += '</table>';
    side_board_el.append(side_board);
}

function toggle_buttons(game_phase, cur_player_uid, num_cards_in_deck){
    // Toggles which buttons to show depending on game phase (e.g. draw button is only visible during the draw phase)

    // Play card button
    if (cur_player_uid === my_uid && game_phase === "Choose Card"){
        $(".card_to_play").removeClass("hide");
    }
    else{
        $(".card_to_play").addClass("hide");
    }

    // Discard card button
    if(cur_player_uid === my_uid && game_phase === "Choose Discard"){
        $(".discard_btn_container").removeClass("hide");
    }
    else{
        $(".discard_btn_container").addClass("hide");
    }

    // Draw card button
    if(cur_player_uid === my_uid && game_phase === "Draw" && num_cards_in_deck > 0){
        $("#draw_button_container").removeClass("hide");
    }
    else{
        $("#draw_button_container").addClass("hide");
    }
}

function update_main_board(board_data, game_phase, current_player_uid){
    // Update the main board layout

    let main_board_el = $("#main_board");
    main_board_el.empty();

    for (const [row_index, row] of board_data.entries()) {
        let main_board = '<tr>';
        for (const [col_index, card] of row.entries()) {
            main_board += "";
            main_board += '<td>';
            if (card != null) {
                main_board += '<img class="card_on_board zoom" id="' + row_index + col_index + '" src="../static/css/playing_cards/' + card + '.png">';
            }
            else {
                if (game_phase === "Choose Coords" && current_player_uid === my_uid)  {
                    main_board += '<form class="choose_coord_btn">';
                    main_board += '<input name="coords" type="hidden" value="' + row_index + col_index + '">';
                    main_board += '<input class="card_on_board blank_choose_coord" src="../static/css/playing_cards/' + blank_card_name + '.png" type="image">';
                    main_board += '</form>';
                }
                else {
                    main_board += '<form>';
                    main_board += '<input disabled class="card_on_board dimmed" id="' + row_index + col_index + '"  src="../static/css/other/' + blank_card_name + '.png" type="image">';
                    main_board += '</form>';
                }
            }
            main_board += '</td>';
        }
        main_board += '</tr>';
        main_board += '</tr>';
        main_board_el.append(main_board);
    }
}

function update_hand(cards_on_hand) {
    let player_hand_el = $("#player_hand_div");
    player_hand_el.empty();

    // Append a first col outside the loop because we need an offset-1 only on the first col
    player_hand_el.append('<div class="col-1 offset-1"></div>');

    // This class combo center-aligns the buttons, the button overlays: d-flex justify-content-center text-center
    cards_on_hand.forEach(function (card) {
        let player_hand = "";
        player_hand += "<div class='col-1 d-flex justify-player_hand-center text-center'>";
        player_hand += "<div class='overlay-button-container'>";
        player_hand += "<img class='card_on_hand' src='../static/css/playing_cards/" + card + ".png'>";
        player_hand += "<form class='card_to_play hide'>";
        player_hand += "<input name='card_name' type='hidden' value='" + card + "'>";
        player_hand += "<input type='submit' class='btn btn-dark' value='Play card'>";
        player_hand += "</form>";
        player_hand += "<form class='discard_btn_container hide'>";
        player_hand += "<input name='card_name' type='hidden' value='" + card + "'>";
        player_hand += "<input type='submit' class='btn btn-dark' value='Discard card'>";
        player_hand += "</form>";
        player_hand += "</div>";
        player_hand += "</div>";
        player_hand_el.append(player_hand);
    });
}

function update_cards_left(cards_left){
    // Update the remaining cards text next to the deck
    $("#cards_left").text("Deck (" + cards_left + " cards)");
}

function update_discard(top_discard_cards, cur_player_uid, game_phase) {
    // Update the top discard cards
    let discard_el = $("#discard_div");
    discard_el.empty();

    Object.entries(top_discard_cards).forEach(([player, card]) => {
        let discard = "";
        discard += '<div class="row">';
        discard += '<div class="col-12 d-flex justify-discard-center text-center">';
        discard += '<p><small>' + player + "'s discard" + '</small></p>';
        discard+= '</div>';
        discard+= '</div>';
        discard+= '<div class ="row">';
        discard+= '<div class="col-12 d-flex justify-discard-center text-center">';
        discard += '<div class="overlay-button-container">';

        if(card === null){
            discard += '<img class="card_on_hand dimmed" src="../static/css/playing_cards/' + blank_card_name + '.png">';
        }
        else {
            discard += '<img class="card_on_hand" src="../static/css/playing_cards/' + card + '.png">';
        }
        discard += '<form class="draw_discard_form ';

        if (cur_player_uid !== my_uid || game_phase !== "Draw" || card === null){
            // We need to add the hide class when we don't want the draw button to show on the discard pile.
            // I.e. we want the above to result to true if:
            // (1) It's not our turn to play, OR (2) it's not turn to draw, OR (3) the deck is empty.
            // Would be better with a separate function to addClass("hide") after creation, but for that to work each
            // discard would need its own ID. Right now can only reference all buttons with class .draw_discard_form.
            // But not all piles will be empty at the same time. Therefore, keeping this logic on creation of the discard element.
            discard += 'hide';
        }
        discard += '">';
        discard += '<input name="discard_owner" type="hidden" value="'+ player +'">';
        discard += '<input class="btn btn-dark" type="submit" value="Draw card">';
        discard += '</form>';
        discard += '</div>';
        discard += '</div>';
        $("#discard_div").append(discard);

    });
}

// UTILITY FUNCTIONS
function show_message(text, category) {
    // Displays a message on top of the screen
    let message_div = document.getElementById("messages");
    let alert_class = "alert" + "-" + category
    message_div.classList.add("alert", alert_class);
    message_div.innerHTML = text;
}

function getCookie(cname) {
  let cookies = ` ${document.cookie}`.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i].split("=");
    if (cookie[0] === ` ${cname}`) {
      return cookie[1];
    }
  }
  return "";
}
