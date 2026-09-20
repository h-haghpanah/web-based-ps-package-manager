function escapeAttr(str){
    if (str === undefined || str === null) return "";
    return String(str).replace(/'/g, "\\'");
}

function pkg_list(game_path, folder){
    var targetId =
        folder.toLowerCase() === "install" ? "installModal_content" :
        folder.toLowerCase() === "update"  ? "updateModal_content"  :
        folder.toLowerCase() === "dlc"     ? "dlcModal_content"     : null;

    if (!targetId) return;

    $("#" + targetId).html('<p class="text-muted">Loading packages...</p>');

    $.ajax({
        url: "/pkg_list/" + game_path + "/" + folder,
        method: "GET",
        success: function(response){
            var ignore_items = ['.DS_Store'];
            var items = '<div class="d-grid gap-2">';
            var count = 0;

            for (var i in response){
                var entry = response[i];
                if (!entry || !entry.pkg || ignore_items.includes(entry.pkg)) continue;

                var btnId = "pkg_btn_" + i;
                items +=
                    '<button type="button" id="' + btnId + '" ' +
                    'onclick="send_pkg(\'/send_pkg/' + entry.path + '/' + entry.pkg + '\',\'' + btnId + '\')" ' +
                    'class="btn btn-dark">' + entry.pkg + '</button>';
                count++;
            }
            items += '</div>';

            if (!count){
                items = '<p class="text-muted mb-0">No packages found in this folder.</p>';
            }

            $("#" + targetId).html(items);
        },
        error: function(){
            $("#" + targetId).html('<p class="text-muted mb-0">Could not load packages.</p>');
        }
    });
}

function send_pkg(path, pkg_btn_id){
    $("#" + pkg_btn_id).prop("disabled", true);
    $.ajax({
        url: path,
        method: "GET",
        success: function(response){
            $("#" + pkg_btn_id).prop("disabled", false);
            if (response.success){
                showsuccess("Package Sent Successfully.");
            } else {
                showerror(response.error || "Something Wrong.");
            }
        },
        error: function(){
            $("#" + pkg_btn_id).prop("disabled", false);
            showerror("Could not reach the console.");
        }
    });
}

function submit_game_info(){
    var pathname = window.location.pathname;
    var segments = pathname.split('/');
    var game_xml_name = segments.pop() + ".xml";

    var title = $("#modal_game_title").val();
    var genres = $("#modal_game_genres").val();
    var platforms = $("#modal_game_platforms").val();
    var released = $("#modal_game_released").val();
    var image = $("#modal_game_image").val();
    var description = $("#modal_game_description").val();
    var updated = $("#modal_game_updated").val();
    var rating = $("#modal_game_rating").val();
    var ratings_count = $("#modal_game_ratings_count").val();
    var metacritic = $("#modal_game_metacritic").val();

    $.ajax({
        url: "/submit_game_info",
        method: "POST",
        data: {
            game_xml_name: game_xml_name,
            title: title,
            genres: genres,
            platforms: platforms,
            released: released,
            image: image,
            description: description,
            updated: updated,
            rating: rating,
            ratings_count: ratings_count,
            metacritic: metacritic
        },
        success: function(response){
            if (response.status){
                $("#game_background_name").html(title);
                $('#game_background_image').attr('src', image);
                $("#game_genres").html(genres);
                $("#game_platforms").html(platforms);
                $("#game_released").html(released);
                $("#game_updated").html(updated);
                $("#game_rating").html(response.data.rating);
                $("#game_ratings_count").html(response.data.ratings_count);
                $("#game_metacritic").html(metacritic);
                $("#game_description").html(description);
                $(".close").click();
                showsuccess("Game Info Successfuly Changed!");
            } else {
                showerror("Something Wrong.");
            }
        }
    });
}

function reload_rawg_game_info_alert(){
    var swalWithBootstrapButtons = Swal.mixin({
        customClass: {
            confirmButton: 'btn btn-success me-2',
            cancelButton: 'btn btn-danger ms-2'
        },
        buttonsStyling: false,
        background: '#101217',
        color: '#f2f3f5'
    });

    swalWithBootstrapButtons.fire({
        title: 'Reload game info with RAWG API',
        text: "You are about to reload game info from the RAWG API. Please confirm your choice.",
        icon: 'info',
        showCancelButton: true,
        confirmButtonText: 'Reload',
        cancelButtonText: 'Cancel',
        reverseButtons: true,
        html:
            '<div class="alert_input">' +
                '<div class="form-check">' +
                    '<input class="form-check-input" type="radio" name="reloadOption" id="reloadOption1" value="withTitle" checked>' +
                    '<label class="form-check-label font-size-12" for="reloadOption1">Reload with input title</label>' +
                '</div>' +
                '<div class="form-check">' +
                    '<input class="form-check-input" type="radio" name="reloadOption" id="reloadOption2" value="withDirectory">' +
                    '<label class="form-check-label font-size-12" for="reloadOption2">Reload with game directory</label>' +
                '</div>' +
            '</div>',
        preConfirm: function(){
            var selectedOption = document.querySelector('input[name="reloadOption"]:checked');
            if (selectedOption){
                return selectedOption.value;
            } else {
                Swal.showValidationMessage('You need to choose how to reload the game info');
            }
        }
    }).then(function(result){
        if (result.isConfirmed){
            reload_rawg_game_info(result.value);
            swalWithBootstrapButtons.fire(
                'Reload Submitted!',
                'The game info reload has been successfully submitted!',
                'success'
            );
        }
    });
}

function reload_rawg_game_info(reload_option){
    var title = $("#modal_game_title").val();
    var description = $("#modal_game_description").val();
    var pathname = window.location.pathname;
    var segments = pathname.split('/');
    var directory_name = segments.pop();

    $.ajax({
        url: "/reload_rawg_game_info",
        method: "POST",
        data: {
            reload_option: reload_option,
            title: title,
            description: description,
            directory_name: directory_name
        },
        success: function(response){
            if (!response.status){
                showerror(response.error);
            }
        },
        error: function(){
            showerror("Could not reach the server.");
        }
    });
}
