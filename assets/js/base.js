
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