
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
        $("#local_ip_address_div").removeClass("display_none")
    }else{
        $("#local_ip_address_div").addClass("display_none")
        $("#remote_repo_input_div").removeClass("display_none")
    }
  }
  rawg_api_switch()
  function rawg_api_switch() {
    var isChecked = $("#rawg_api_switch").is(':checked');
    if (isChecked){
        $("#rawg_api_key").prop("disabled", false).attr("placeholder", "Ex: fdsferc54fdsf45a3745643agdd55f").removeClass("disabled_background_dark_red");
    } else {
        $("#rawg_api_key").prop("disabled", true).attr("placeholder", "Disabled").addClass("disabled_background_dark_red");
    }
}

function submit_config() {
    local_pkg_enabled = $("#local_pkg_switch").is(':checked')
    local_ip_address = $("#local_ip_address").val()
    remote_repository_address = $("#remote_repository_address").val()
    rawg_api_enabled = $("#rawg_api_switch").is(':checked')
    rawg_api_key = $("#rawg_api_key").val()
    if($("#repo_type_ps4").is(':checked')){
        repository_type = "ps4"
    }else if($("#repo_type_ps5").is(':checked')){
        repository_type = "ps5"
    }else{
        repository_type = "ps"
    }
    web_title = $("#web_title").val()
    ps_ip_addresses = $("#ps_ip_addresses").val()
    $.ajax({
        url:"/submit_config",
        method:"POST",
        data:{
            local_pkg_enabled:local_pkg_enabled,
            local_ip_address:local_ip_address,
            remote_repository_address:remote_repository_address,
            rawg_api_enabled:rawg_api_enabled,
            rawg_api_key:rawg_api_key,
            repository_type:repository_type,
            web_title:web_title,
            ps_ip_addresses:ps_ip_addresses},
        success:function(response){
            if(response.status){
                $(".close").click()
                showsuccess("Config Successfuly Changed!")
            }else{
                showerror("Something Wrong.")
            }
        }
    })
}
read_config()
function read_config() {
    $.ajax({
        url:"/read_config",
        method:"GET",
        success:function(response){
            if(response.status){
                if(response.data.local_pkg_enabled){
                    $('#local_pkg_switch').prop('checked', true);
                    $("#remote_repo_input_div").addClass("display_none")
                    $("#local_ip_address_div").removeClass("display_none")
                }else{
                    $('#local_pkg_switch').prop('checked', false);
                    $("#local_ip_address_div").addClass("display_none")
                    $("#remote_repo_input_div").removeClass("display_none")
                }
                $("#remote_repository_address").val(response.data.remote_web_server_address)
                $("#local_ip_address").val(response.data.local_system_ip_address)
                if(response.data.rawg_api_enabled){
                    $('#rawg_api_switch').prop('checked', true);
                    $("#rawg_api_key").prop("disabled", false).attr("placeholder", "Ex: fdsferc54fdsf45a3745643agdd55f").removeClass("disabled_background_dark_red");
                }else{
                    $('#rawg_api_switch').prop('checked', false);
                    $("#rawg_api_key").prop("disabled", true).attr("placeholder", "Disabled").addClass("disabled_background_dark_red");
                }
                $("#rawg_api_key").val(response.data.rawg_api_key)
                if(response.data.repository_type == "ps4"){
                    $('#repo_type_ps4').prop('checked', true);
                }else if (response.data.repository_type == "ps5"){
                    $('#repo_type_ps5').prop('checked', true);
                }else {
                    $('#repo_type_mixed').prop('checked', true);
                }
                $("#web_title").val(response.data.web_title)
                $("#ps_ip_addresses").html(response.data.ps_addresses)
            }else{
                showerror("Something Wrong.")
            }
        }
    })
}