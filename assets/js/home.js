
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

                items += '<div class="row gy-4">\n'+
                '<div class="col-lg-4 col-md-6">\n'+
                '<div class="game-card style2">\n'+
                '<div class="game-card-img">\n'+
                '<a href="'+response[i].url+'"><img src="'+response[i].background_image+'" alt="game image"></a>\n'+
                '</div>\n'+
                '<div class="game-card-details">\n'+
                '<div class="media-left">\n'+
                '<h3 class="box-title"><a href="'+response[i].url+'">'+response[i].name+'</a></h3>\n'+
                '</div>\n'+
                '<div class="media-body"><span class="game-rating"><i class="fas fa-star"></i> 4.8</span> <span class="review-count">(2.6k Review)</span></div>\n'+
                '</div>\n'+
                '</div>\n'+
                '</div>\n'+
                '</div>\n'

            }
            }
            $("#game_list").html(items)
        }
    })
 }

