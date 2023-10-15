

function pkg_list(game_path,folder){
    $.ajax({
        url:"/pkg_list/"+game_path+"/"+folder,
        method:"GET",
        success:function(response){
            items = '<div class="d-grid gap-2">'
            ignore_items = ['.DS_Store']
            console.log(response)
            for(var i in response){
                console.log(i)
                if (ignore_items.includes(response[i])){

                }
                else{
                    items += '<button type="button" onclick="send_pkg('+"'"+'/send_pkg/'+response[i].path+'/'+response[i].pkg+"'"+')"  class="btn btn-dark">'+response[i].pkg+'</button>'
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


function send_pkg(path){
    $.ajax({
        url:path,
        method:"GET",
        success:function(response){
            if(response.success){
                showsuccess("Package Sent Successfully.")
            }else{
                showerror("Something Wrong.")
            }
        }
    })
}


function showerror(msg){
    const Toast = Swal.mixin({
      toast: true,
      position: 'top-start',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
    });
    
    Toast.fire({
      icon: 'error',
      title: msg
    })
  }
  
  function showsuccess(msg){
    const Toast = Swal.mixin({
      toast: true,
      position: 'top-start',
      showConfirmButton: false,
      timer: 3000,
      timerProgressBar: true,
    });
    
    Toast.fire({
      icon: 'success',
      title: msg
    })
  }