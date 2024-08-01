

function pkg_list(game_path,folder){
    
    $.ajax({
        url:"/pkg_list/"+game_path+"/"+folder,
        method:"GET",
        success:function(response){
            items = '<div class="d-grid gap-2">'
            ignore_items = ['.DS_Store']
            for(var i in response){
                if (ignore_items.includes(response[i])){

                }
                else{
                    items += '<button type="button" id="pkg_btn_'+i+'" onclick="send_pkg('+"'"+'/send_pkg/'+response[i].path+'/'+response[i].pkg+"'"+','+"'"+'pkg_btn_'+i+"'"+')"  class="btn btn-dark">'+response[i].pkg+'</button>'
                // items += '<button class="btn btn-secondary" href="/send_pkg/'+response[i].path+'/'+response[i].pkg+'">'+response[i].pkg+'</button>'
                }

            }
            items += "</div>"
            if(folder.toLowerCase() == "install"){
                $("#installModal_content").html(items)
            }else if(folder.toLowerCase() == "update"){
                $("#updateModal_content").html(items)
            }else if(folder.toLowerCase() == "dlc"){
                $("#dlcModal_content").html(items)
            }
            
        }
    })
 }


function send_pkg(path,pkg_btn_id){
    $("#"+pkg_btn_id).prop("disabled",true)
    $.ajax({
        url:path,
        method:"GET",
        success:function(response){
            $("#"+pkg_btn_id).prop("disabled",false)
            if(response.success){
                showsuccess("Package Sent Successfully.")
            }else{
                showerror("Something Wrong.")
            }
        }
    })
}

function submit_game_info(){
    pathname = window.location.pathname;
    segments = pathname.split('/');
    game_xml_name = segments.pop() + ".xml";
    title = $("#modal_game_title").val()
    genres = $("#modal_game_genres").val()
    platforms = $("#modal_game_platforms").val()
    released = $("#modal_game_released").val()
    image = $("#modal_game_image").val()
    description = $("#modal_game_description").val()
    updated = $("#modal_game_updated").val()
    rating = $("#modal_game_rating").val()
    ratings_count = $("#modal_game_ratings_count").val()
    metacritic = $("#modal_game_metacritic").val()
    $.ajax({
        url:"/submit_game_info",
        method:"POST",
        data:{
            game_xml_name:game_xml_name,
            title:title,
            genres:genres,
            platforms:platforms,
            released:released,
            image:image,
            description:description,
            updated:updated,
            rating:rating,
            ratings_count:ratings_count,
            metacritic:metacritic},
        success:function(response){
            if(response.status){
                $("#game_background_name").html(title)
                $('#game_background_image').attr('src', image);
                $("#game_genres").html(genres)
                $("#game_platforms").html(platforms)
                $("#game_released").html(released)
                $("#game_updated").html(updated)
                $("#game_rating").html(response.data.rating)
                $("#game_ratings_count").html(response.data.ratings_count)
                $("#game_metacritic").html(metacritic)
                $("#game_description").html(description)
                $(".close").click()
                showsuccess("Game Info Successfuly Changed!")
            }else{
                showerror("Something Wrong.")
            }
        }
    })
}


