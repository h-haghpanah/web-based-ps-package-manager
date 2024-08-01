
read_games()
function read_games(){
    
    $.ajax({
        url:"/game_list",
        method:"GET",
        success:function(response){
            items = ''
            ignore_items = ['.DS_Store']
            for(var i in response){
                if (ignore_items.includes(response[i])){


                }
                else{

                items += '<div class="col-lg-4 col-md-6 mb-20 game-card-container">\n'+
                '<div class="game-card style2">\n'+
                '<div class="game-card-img">\n'+
                '<a href="'+response[i].url+'"><img style="max-height: 185px;max-width: fit-content;" src="'+response[i].background_image+'" alt="game image"></a>\n'+
                '</div>\n'+
                '<div class="game-card-details">\n'+
                '<div class="media-left">\n'+
                '<h5 class="box-title"><a href="'+response[i].url+'">'+response[i].name+'</a></h5>\n'+
                '</div>\n'+
                '<div class="media-body"><span class="game-rating"><i class="fas fa-star"></i> '+response[i].rating+'</span> <span class="review-count">('+response[i].ratings_count+' Review)</span></div>\n'+
                '</div>\n'+
                '</div>\n'+
                '</div>\n'

            }
            }
            $("#game_list_title").removeClass("display_none")
            $("#game_loading").addClass("display_none")
            $("#game_list").html(items)
        }
    })
 }

 function filterGames() {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const gameContainers = document.querySelectorAll('.game-card-container');

    gameContainers.forEach(container => {
        const title = container.querySelector('.box-title').textContent.toLowerCase();
        if (title.includes(searchInput)) {
            container.style.display = 'block';
        } else {
            container.style.display = 'none';
        }
    });
}