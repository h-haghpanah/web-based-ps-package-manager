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

repo_type_switch();
function repo_type_switch(){
    if ($("#repo_type_ps5").is(':checked')){
        $("#ps5_send_method_div").removeClass("display_none");
    } else {
        $("#ps5_send_method_div").addClass("display_none");
    }
    receiver_discovery_visibility();
}

$(document).on("change", "input[name=ps5_send_method_options]", receiver_discovery_visibility);

function get_ps5_send_method(){
    if ($("#ps5_send_method_receiver").is(':checked')){
        return "loopayeh-pkg_receiver";
    }
    return "haghpanah-ps5_file_downloader";
}

function receiver_monitor_visibility(repository_type, ps5_send_method){
    if (repository_type === "ps5" && ps5_send_method === "loopayeh-pkg_receiver"){
        $("#receiver_monitor_btn_div").removeClass("display_none");
    } else {
        $("#receiver_monitor_btn_div").addClass("display_none");
    }
}

function receiver_discovery_visibility(){
    if ($("#repo_type_ps5").is(':checked') && $("#ps5_send_method_receiver").is(':checked')){
        $("#receiver_discover_div").removeClass("display_none");
    } else {
        $("#receiver_discover_div").addClass("display_none");
    }
}

function discover_receivers(){
    var btn = $("#receiver_discover_btn");
    btn.prop("disabled", true).text("Scanning...");
    $.ajax({
        url: "/receiver_discover",
        method: "GET",
        success: function(response){
            btn.prop("disabled", false).text("Scan Network");
            if (!response.status || !response.addresses.length){
                showerror("No console answered.");
                return;
            }
            var current = $("#ps_ip_addresses").val();
            var lines = current ? current.split("\n") : [];
            var added = 0;
            for (var i in response.addresses){
                var ip = response.addresses[i];
                if (current.indexOf(ip) !== -1) continue;
                lines.push("ps5-" + ip.split(".").pop() + "=" + ip);
                added++;
            }
            $("#ps_ip_addresses").val(lines.join("\n").replace(/^\n+/, ""));
            showsuccess(added ? added + " console(s) found" : "Already listed");
        },
        error: function(){
            btn.prop("disabled", false).text("Scan Network");
            showerror("Could not reach the server.");
        }
    });
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
    var ps5_send_method = get_ps5_send_method();

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
            ps5_send_method: ps5_send_method,
            web_title: web_title,
            ps_ip_addresses: ps_ip_addresses
        },
        success: function(response){
            if (response.status){
                $(".close").click();
                showsuccess("Config Successfuly Changed!");
                read_ps_addresses();
                receiver_monitor_visibility(repository_type, ps5_send_method);
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

            if (data.ps5_send_method === "loopayeh-pkg_receiver"){
                $('#ps5_send_method_receiver').prop('checked', true);
            } else {
                $('#ps5_send_method_downloader').prop('checked', true);
            }
            repo_type_switch();
            receiver_monitor_visibility(data.repository_type, data.ps5_send_method);

            $("#web_title").val(data.web_title);
            $("#ps_ip_addresses").html(data.ps_addresses);
        }
    });
}

var receiver_monitor_timer = null;
var receiver_paused = false;
var receiver_samples = {};

function open_receiver_monitor(){
    $("#receiverDownloadsModal").modal("show");
    refresh_receiver_downloads();
    if (receiver_monitor_timer){
        clearInterval(receiver_monitor_timer);
    }
    receiver_monitor_timer = setInterval(refresh_receiver_downloads, 2000);
}

$(document).on("hidden.bs.modal", "#receiverDownloadsModal", function(){
    clearInterval(receiver_monitor_timer);
    receiver_monitor_timer = null;
    receiver_samples = {};
});

function human_size(bytes){
    if (!bytes || bytes < 0) return "0 B";
    var units = ["B", "KB", "MB", "GB", "TB"];
    var i = 0;
    while (bytes >= 1024 && i < units.length - 1){
        bytes = bytes / 1024;
        i++;
    }
    return bytes.toFixed(i === 0 ? 0 : 1) + " " + units[i];
}

function human_eta(seconds){
    if (!isFinite(seconds) || seconds <= 0) return "";
    var h = Math.floor(seconds / 3600);
    var m = Math.floor((seconds % 3600) / 60);
    var sec = Math.floor(seconds % 60);
    if (h) return h + "h " + m + "m";
    if (m) return m + "m " + sec + "s";
    return sec + "s";
}

// speed is not reported by the receiver, it comes from the delta between two polls
function transfer_rate(item){
    var now = Date.now();
    var previous = receiver_samples[item.file];
    receiver_samples[item.file] = { bytes: item.downloaded, at: now };
    if (!previous || item.downloaded <= previous.bytes) return "";
    var speed = (item.downloaded - previous.bytes) / ((now - previous.at) / 1000);
    if (speed <= 0) return "";
    var text = human_size(speed) + "/s";
    if (item.total > 0){
        var eta = human_eta((item.total - item.downloaded) / speed);
        if (eta) text += " - " + eta + " left";
    }
    return text;
}

function render_receiver_meta(data){
    var meta = [];
    if (data.build) meta.push("build " + data.build);
    if (data.pc_age >= 0 && data.pc_age < 15){
        meta.push("PC " + data.pc_ip);
    } else {
        meta.push("PC not detected");
    }
    if (data.truncated) meta.push("listing truncated");
    $("#receiver_meta").text(meta.join(" - "));
}

function refresh_receiver_downloads(){
    $.ajax({
        url: "/receiver_downloads",
        method: "GET",
        success: function(response){
            if (!response.status){
                $("#receiver_state").text("");
                $("#receiver_meta").text("");
                $("#receiver_pause_btn").addClass("display_none");
                $("#receiver_downloads_content").html('<p class="text-muted mb-0">' + (response.error || "Unavailable.") + '</p>');
                return;
            }
            var data = response.data;
            $("#receiver_state").text(data.busy ? "Busy - " + data.active + " active" : "Idle");
            render_receiver_meta(data);

            receiver_paused = data.paused;
            if (data.pulling){
                $("#receiver_pause_btn").removeClass("display_none").text(data.paused ? "Resume" : "Pause");
            } else {
                $("#receiver_pause_btn").addClass("display_none");
            }

            if (!data.downloads.length){
                $("#receiver_downloads_content").html('<p class="text-muted mb-0">No transfers yet.</p>');
                return;
            }
            var items = "";
            for (var i in data.downloads){
                var item = data.downloads[i];
                var percent = item.percent === null ? 0 : item.percent;
                var label = item.percent === null ? "" : percent + "%";
                var meta = [];
                if (item.total > 0){
                    meta.push(human_size(item.downloaded) + " / " + human_size(item.total));
                }
                meta.push(item.state);
                if (item.state === "downloading"){
                    var rate = transfer_rate(item);
                    if (rate) meta.push(rate);
                }
                items +=
                    '<div class="receiver_download">' +
                        '<div class="receiver_download_head">' +
                            '<span class="receiver_download_name">' + item.file + '</span>' +
                            '<span class="receiver_download_percent">' + label + '</span>' +
                        '</div>' +
                        '<div class="receiver_progress"><div class="receiver_progress_bar receiver_' + item.state + '" style="width:' + percent + '%"></div></div>' +
                        '<div class="receiver_download_meta">' + meta.join(" &middot; ") + '</div>' +
                    '</div>';
            }
            $("#receiver_downloads_content").html(items);
        },
        error: function(){
            $("#receiver_downloads_content").html('<p class="text-muted mb-0">Could not reach the server.</p>');
        }
    });
}

function toggle_receiver_pause(){
    $.ajax({
        url: "/receiver_pause",
        method: "POST",
        data: { paused: receiver_paused ? "false" : "true" },
        success: function(response){
            if (!response.status){
                showerror("Something Wrong.");
                return;
            }
            refresh_receiver_downloads();
        }
    });
}

function clear_finished_receiver_downloads(){
    $.ajax({
        url: "/receiver_clear_finished",
        method: "POST",
        success: function(){
            refresh_receiver_downloads();
        }
    });
}
