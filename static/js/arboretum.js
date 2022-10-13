
function highlight_path(to_highlight)
{

    remove_all_highlights();

    // Un-dim the cards that are part of the path to highlight to make it stand out
    for (const [player, tree_dict] of Object.entries(top_paths)){
        console.log(player)
        for (const [tree_type, coord] of Object.entries(tree_dict[to_highlight].Path)){
              console.log(coord)
              var card = document.getElementById(coord);
              card.classList.remove("highlighted_path");
		}
    }
}

function remove_all_highlights()
{
    // Dim all cards
    // TODO - this is a very inefficient way of removing highlight by looping through everything
    // TODO - has to exist a better way of reference JSON elements in JS than nesting loops
    for (const [player, tree_dict] of Object.entries(top_paths)){
        for (const [tree_type, tree_dict_2] of Object.entries(tree_dict)){
              for (const [tree, score_array] of Object.entries(tree_dict_2))
              {
                if(score_array.length > 0){

                    score_array.forEach(function(coord)
                    {
                        var card = document.getElementById(coord);
                        card.classList.add("highlighted_path");
                    })
              }
		}
    }
}
}

// Lights up empty tiles when player is choosing where to place a card
function hover(element) {
element.setAttribute('src', '../static/css/other/blank-selected.png');
}

function unhover(element) {
  element.setAttribute('src', '../static/css/other/blank-w-border.png');
}