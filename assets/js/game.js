

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


