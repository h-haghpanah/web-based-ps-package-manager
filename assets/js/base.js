function update_ps_address(){
    var ps_ip = $("#ps_ip").val();
    $.ajax({
        url: "/update_ps_address",
        method: "POST",
        data: { ps_ip: ps_ip },
        success: function(response){
            if (response.success){
                showsuccess("PS Change Successfully");
            } else {
                showerror("Something Wrong.");
            }
        },
        error: function(){
            showerror("Could not reach the server.");
        }
    });
}

read_ps_addresses();
function read_ps_addresses(){
    $.ajax({
        url: "/read_ps_addresses",
        method: "GET",
        success: function(response){
            if (response.success){
                var items = "";
                if (!response.addresses || !response.addresses.length){
                    $("#ps_ip").html('<option value="">No console configured</option>');
                    return;
                }
                for (var i in response.addresses){
                    var addr = response.addresses[i];
                    items += '<option value="' + addr.address + '"' + (addr.selected ? ' selected' : '') + '>' + addr.name + '</option>\n';
                }
                $("#ps_ip").html(items);
            } else {
                showerror("Something Wrong.");
            }
        }
    });
}

function showerror(msg){
    Swal.mixin({
        toast: true,
        position: 'top-start',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    }).fire({ icon: 'error', title: msg });
}

function showsuccess(msg){
    Swal.mixin({
        toast: true,
        position: 'top-start',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true
    }).fire({ icon: 'success', title: msg });
}

local_pkg_switch();
function local_pkg_switch(){
    var isChecked = $("#local_pkg_switch").is(':checked');
    if (isChecked){
        $("#remote_repo_input_div").addClass("display_none");
        $("#local_ip_address_div").removeClass("display_none");
    } else {
        $("#local_ip_address_div").addClass("display_none");
        $("#remote_repo_input_div").removeClass("display_none");
    }
}

rawg_api_switch();
function rawg_api_switch(){
    var isChecked = $("#rawg_api_switch").is(':checked');
    if (isChecked){
        $("#rawg_api_key").prop("disabled", false).attr("placeholder", "Ex: fdsferc54fdsf45a3745643agdd55f").removeClass("disabled_background_dark_red");
    } else {
        $("#rawg_api_key").prop("disabled", true).attr("placeholder", "Disabled").addClass("disabled_background_dark_red");
    }
}

function submit_config(){
    var local_pkg_enabled = $("#local_pkg_switch").is(':checked');
    var local_ip_address = $("#local_ip_address").val();
    var remote_repository_address = $("#remote_repository_address").val();
    var rawg_api_enabled = $("#rawg_api_switch").is(':checked');
    var rawg_api_key = $("#rawg_api_key").val();
    var repository_type;
    if ($("#repo_type_ps4").is(':checked')){
        repository_type = "ps4";
    } else if ($("#repo_type_ps5").is(':checked')){
        repository_type = "ps5";
    } else {
        repository_type = "ps";
    }
    var web_title = $("#web_title").val();
    var ps_ip_addresses = $("#ps_ip_addresses").val();

    $.ajax({
        url: "/submit_config",
        method: "POST",
        data: {
            local_pkg_enabled: local_pkg_enabled,
            local_ip_address: local_ip_address,
            remote_repository_address: remote_repository_address,
            rawg_api_enabled: rawg_api_enabled,
            rawg_api_key: rawg_api_key,
            repository_type: repository_type,
            web_title: web_title,
            ps_ip_addresses: ps_ip_addresses
        },
        success: function(response){
            if (response.status){
                $(".close").click();
                showsuccess("Config Successfuly Changed!");
                read_ps_addresses();
            } else {
                showerror("Something Wrong.");
            }
        }
    });
}

read_config();
function read_config(){
    $.ajax({
        url: "/read_config",
        method: "GET",
        success: function(response){
            if (!response.status){
                showerror("Something Wrong.");
                return;
            }
            var data = response.data;
            if (data.local_pkg_enabled){
                $('#local_pkg_switch').prop('checked', true);
                $("#remote_repo_input_div").addClass("display_none");
                $("#local_ip_address_div").removeClass("display_none");
            } else {
                $('#local_pkg_switch').prop('checked', false);
                $("#local_ip_address_div").addClass("display_none");
                $("#remote_repo_input_div").removeClass("display_none");
            }
            $("#remote_repository_address").val(data.remote_web_server_address);
            $("#local_ip_address").val(data.local_system_ip_address);

            if (data.rawg_api_enabled){
                $('#rawg_api_switch').prop('checked', true);
                $("#rawg_api_key").prop("disabled", false).attr("placeholder", "Ex: fdsferc54fdsf45a3745643agdd55f").removeClass("disabled_background_dark_red");
            } else {
                $('#rawg_api_switch').prop('checked', false);
                $("#rawg_api_key").prop("disabled", true).attr("placeholder", "Disabled").addClass("disabled_background_dark_red");
            }
            $("#rawg_api_key").val(data.rawg_api_key);

            if (data.repository_type === "ps4"){
                $('#repo_type_ps4').prop('checked', true);
            } else if (data.repository_type === "ps5"){
                $('#repo_type_ps5').prop('checked', true);
            }

            $("#web_title").val(data.web_title);
            $("#ps_ip_addresses").html(data.ps_addresses);
        }
    });
}
