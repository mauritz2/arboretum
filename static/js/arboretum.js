
function highlight_path(to_highlight)
{



    dim_all_cards();

    // Un-dim the cards that are part of the path to highlight to make it stand out
    for (const [player, tree_dict] of Object.entries(top_paths)){
        for (const [tree_type, coord] of Object.entries(tree_dict[to_highlight].Path)){
              var card = document.getElementById(coord);
              card.classList.remove("dimmed");
		}
    }
};

function dim_all_cards()
{
    // :-) :-) :-)
    // TODO - this is a very silly loop to dim all coords - refactor
    all_coords = []
    num_players = 2
    rows = 5
    columns = 10
    for (p = 1; p <= num_players; p++)
    {
        for (i = 0; i < rows ; i++)
        {
            for (j = 0; j < columns; j++)
          {
            coord_id = p.toString() + i.toString() + j.toString()
            all_coords.push(coord_id);
          }
        }
     };

    all_coords.forEach(function(coord){
        card = document.getElementById(coord);
        card.classList.add("dimmed");
    });
 };

// Lights up empty tiles when player is choosing where to place a card
function hover(element) {
element.setAttribute('src', '../static/css/other/blank-selected.png');
}

function unhover(element) {
  element.setAttribute('src', '../static/css/other/blank-w-border.png');
}