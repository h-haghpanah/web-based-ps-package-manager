

function pkg_list(game_path,folder){
    $.ajax({
        url:"/pkg_list/"+game_path+"/"+folder,
        method:"GET",
        success:function(response){
            console.log(response)
            items = ''
            ignore_items = ['.DS_Store']
            for(var i in response){
                if (ignore_items.includes(response[i])){


                }
                else{

                items += '<a href="/send_pkg/'+response[i].path+'/'+response[i].pkg+'">'+response[i].pkg+'</a>'

            }
            }
            if(folder == "Install"){
                $("#installModal_content").html(items)
            }else if(folder == "Update"){
                $("#updateModal_content").html(items)
            }else if(folder == "DLC"){
                $("#dlcModal_content").html(items)
            }
            
        }
    })
 }

