function highlight_path(player, tree_type){
    dim_all_cards();

    // Un-dim the cards that are part of the path to highlight to make it stand out
    for (const coord of Object.values(top_paths[player][tree_type].Path)){
          var card = document.getElementById(coord);
          card.classList.remove("dimmed");
    }
}

function dim_all_cards() {
    $(".card_on_board").addClass("dimmed");
}