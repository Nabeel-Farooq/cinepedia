
$( document ).ready(function() {

$.typeahead({
    input: '.js-typeahead-game_v1',
    minLength: 1,
    maxItem: 0,
    maxItemPerGroup: 16,
    order: "asc",
    hint: true,
    group: true,
    maxItemPerGroup: 5,
    dropdownFilter: "all",
    source: {
        Film: {
          ajax: {
                url: "/_all.json",
                dataType: "json",
                path: "data.films"
            }
        },
        Serie: {
            ajax: {
                url: "/_all.json",
                dataType: "json",
                path: "data.series"
            }
        },
	Anime: {
            ajax: {
                url: "/_all.json",
                dataType: "json",
                path: "data.animes"
            }
        },
	Jeu: {
            ajax: {
                url: "/_all.json",
                dataType: "json",
                path: "data.jeux"
            }
        },


    },
    callback: {
        onNavigateBefore: function (node, query, event) {
            if (~[38,40].indexOf(event.keyCode)) {
                event.preventInputChange = true;
            }
        },
        onClick: function (node, a, item, event) {
            window.open(
                    "/category/" + item.group.toLowerCase() + "/" +
                    item.slug
            ,"_self");
        },
        onMouseEnter: function (node, a, item, event) {
            if (!$(a).find(".popover")[0]) {
 
                $(a).append(
                    $("<div/>", {
                        "class": "popover fade right in",
                        "html": $("<div/>", {
                            "class": "popover-content",
                            "html": $("<img/>", {
                                "src": item.img
                            })
                        }).prepend($("<div/>", {
                            "class": "arrow"
                        }))
                    })
                );
 
            } else {
                $(a).find(".popover").removeClass("out").addClass("in");
            }
        },
        onMouseLeave: function (node, a, item, event) {
            $(a).find(".popover").removeClass("in").addClass("out");
        }
    }
});

});

