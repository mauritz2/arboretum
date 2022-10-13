
function highlight_path(to_highlight)
{

    dim_all_cards();

//    // Un-dim the cards that are part of the path to highlight to make it stand out
//    for (const [player, tree_dict] of Object.entries(top_paths)){
//        console.log(player)
//        for (const [tree_type, coord] of Object.entries(tree_dict[to_highlight].Path)){
//              console.log(coord)
//              var card = document.getElementById(coord);
//              card.classList.remove("highlighted_path");
//		}
//    }
};

function dim_all_cards()
{
    // :-)
    all_coords = []
    rows = 5
    columns = 10
    for (i = 0; i < rows ; i++)
    {
        console.log(i)
        for (j = 0; j < columns; j++)
      {
        i_str = i.toString();
        j_str = j.toString();
        coord =  + i_str + j_str;
          all_coords.push(coord);
      }
    }

    all_coords.forEach(function(coord){
        console.log("I'm going to read from");
        console.log(coord);
        card = document.getElementById(coord);
        card.classList.add("highlight_path");
    });
 };

// Lights up empty tiles when player is choosing where to place a card
function hover(element) {
element.setAttribute('src', '../static/css/other/blank-selected.png');
}

function unhover(element) {
  element.setAttribute('src', '../static/css/other/blank-w-border.png');
}