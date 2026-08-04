read_games();

function escapeHtml(str){
    if (str === undefined || str === null) return "";
    return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;");
}

function read_games(){
    $.ajax({
        url: "/game_list",
        method: "GET",
        success: function(response){
            if (response.status === false){
                showerror(response.error);
            }

            var ignore_items = ['.DS_Store'];
            var games = response.data || [];
            var items = "";

            for (var i in games){
                var game = games[i];
                if (ignore_items.includes(game)) continue;

                items +=
                    '<div class="col-lg-4 col-md-6 game-card-container">' +
                        '<div class="game-card style2 hud-frame">' +
                            '<div class="game-card-img">' +
                                '<a href="' + game.url + '">' +
                                    '<img src="' + game.background_image + '" alt="' + escapeHtml(game.name) + '" loading="lazy">' +
                                '</a>' +
                            '</div>' +
                            '<div class="game-card-details">' +
                                '<h5 class="box-title"><a href="' + game.url + '">' + escapeHtml(game.name) + '</a></h5>' +
                                '<div class="media-body">' +
                                    '<span class="game-rating"><i class="fas fa-star"></i> ' + escapeHtml(game.rating) + '</span>' +
                                    '<span class="review-count">(' + escapeHtml(game.ratings_count) + ' Review)</span>' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>';
            }

            if (!items){
                items = '<div class="empty-state">No games found. Drop a game folder into your repository to get started <span>_</span></div>';
            }

            $("#game_list_title").removeClass("display_none");
            $("#game_loading").addClass("display_none");
            $("#game_list").html(items);
        },
        error: function(){
            $("#game_loading").addClass("display_none");
            $("#game_list").html('<div class="empty-state">Could not load the game library. Check your connection and refresh.</div>');
        }
    });
}

var filterGamesTimeout;
function filterGames(){
    clearTimeout(filterGamesTimeout);
    filterGamesTimeout = setTimeout(function(){
        var searchInput = document.getElementById('searchInput').value.toLowerCase().trim();
        var gameContainers = document.querySelectorAll('.game-card-container');
        var visibleCount = 0;

        gameContainers.forEach(function(container){
            var titleEl = container.querySelector('.box-title');
            if (!titleEl) return;
            var title = titleEl.textContent.toLowerCase();
            var matches = title.includes(searchInput);
            container.style.display = matches ? '' : 'none';
            if (matches) visibleCount++;
        });
    }, 150);
}
