
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
                items += '<a href="'+response[i].url+'">\n'+
                '<div class="col-xl-3 col-sm-6 col-md-4 col-6">\n'+
                '<div class="card rounded text-white bg-dark" style="width: 18rem;">\n'+
                '<img class="card-img-top" src="'+response[i].background_image+'">\n'+
                '<div class="card-body">\n'+
                  '<p class="card-text">'+response[i].name+'</p>\n'+
                '</div>\n'+
                '</div>\n'+
                '</div>\n'+
                '</a>\n'

            }
            }
            $("#game_list").html(items)
        }
    })
 }

