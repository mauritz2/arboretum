
function highlight_path(player, tree_type)
{

    dim_all_cards();

    // Un-dim the cards that are part of the path to highlight to make it stand out
    //for (const [player, tree_dict] of Object.entries(top_paths)){
        for (const [tree, coord] of Object.entries(top_paths[player][tree_type].Path)){
              var card = document.getElementById(coord);
              card.classList.remove("dimmed");
        }
}

function dim_all_cards()
{
    // TODO -re-write now that we can't rely on Player 1 and Player 2 names anymore
    // :-) :-) :-)
    // TODO - this is a very silly loop to dim all coords - refactor
    // To fix this JS needs to know what IDs exist - so we don't have to generate them through hard coding here
    // Either we could pass a list of coords, or the configs to the game. This might be useful anyways if the UI knows the num of players
    // that could support multiple UIs depending on game size. But would be work to set that up.
    // A better approach would be to be able to access the children of the board parent div and apply the class
    // That seems like the best approach
    all_coords = []
    num_players = 2
    rows = 6
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
     }

    console.log(all_coords)

    all_coords.forEach(function(coord){
        card = document.getElementById(coord);
        card.classList.add("dimmed");
    });
 }
