
function update_ps_address(){
    ps_ip = $("#ps_ip").val()
    $.ajax({
        url:"/update_ps_address",
        method:"POST",
        data:{ps_ip:ps_ip},
        success:function(response){
            if (response.success){
                showsuccess("PS Change Successfully")
            }else{
                showerror("Something Wrong.")
            }
        }
    })
 }
 read_ps_addresses()
 function read_ps_addresses(){
    $.ajax({
        url:"/read_ps_addresses",
        method:"GET",
        success:function(response){
            if (response.success){
                items = ""
                for(var i in response.addresses){
                    if(response.addresses[i].selected){
                        items += '<option value="'+response.addresses[i].address+'" selected>'+response.addresses[i].name+'</option>\n'
                    }else{
                        items += '<option value="'+response.addresses[i].address+'">'+response.addresses[i].name+'</option>\n'
                    }
                }
                $("#ps_ip").html(items)
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
  local_pkg_switch()
  function local_pkg_switch(){
    var isChecked = $("#local_pkg_switch").is(':checked');
    if (isChecked){
        $("#remote_repo_input_div").addClass("display_none")
        $("#local_repo_input_div").removeClass("display_none")
    }else{
        $("#local_repo_input_div").addClass("display_none")
        $("#remote_repo_input_div").removeClass("display_none")
    }
    // $.ajax({
    //     url:"/submit_game_info",
    //     method:"POST",
    //     data:{
    //         command:command,
    //         value:value},
    //     success:function(response){
    //         if(response.status){
    //             showsuccess("Game Info Successfuly Changed!")
    //         }else{
    //             showerror("Something Wrong.")
    //         }
    //     }
    // })
  }