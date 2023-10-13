
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
                // items += '<div class="col-xl-3 col-sm-6 col-md-4 col-6">\n'+
                //   '<div class="card">\n'+
                //     '<div class="card-content">\n'+
                //       '<div class="card-body">\n'+
                //         '<p style="text-align: center;" class="title hwhite">'+response[i].replace(/_/g, ' ')+'</p>\n'+
                //         '<div class="media d-flex">\n'+
                //         '<div class="align-self-center">\n'+
                //             '<img src="../assets/images/icons/pkg.png" alt="" class="shabnam icon-image">\n'+
                //           '</div>\n'+
                //           '<div class="media-body text-right align-self-center list_img">\n'+
                //             '<a class="btn btn-success btn-download" href="../programs/archive/winrar.exe">View</a>\n'+
                //           '</div>\n'+
                //         '</div>\n'+
                //       '</div>\n'+
                //     '</div>\n'+
                //   '</div>\n'+
                // '</div>\n'
                items += '<a href="card-link-1.html">\n'+
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

