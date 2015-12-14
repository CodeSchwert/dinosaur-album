/*!
 * catalogue.js - Udacity Project 3
 *
 * Nik Ho, 2015
 *
 * JavaScript script to take JSON responses from the Flask application and use
 * the results to render 'item cards'. The script uses the new Bootstrap v4
 * card class to style the output.
 *
 * There is repetition in the code, and it could be refactored to be more DRY.
 * It was mostly done this way to play around with Bootstrap v4, JQuery & AJX.
 *
 * License:  MIT
 */
$(window).load(function () {

    // Load recent items for on the Home tab
    "use strict";
    var categoryId = "home";
    $.get("/catalogue/" + categoryId, function (data) {

        var cardId = "#cards_" + categoryId;

        $.each(data.CategoryItems, function (k, v) {

            var cardName = "#card_" + categoryId + "_" + v.id;

            // Check if the card exists
            if ($(cardName).length === 0) {

                // Add the card if it doesn't exist
                $(cardId).append('<div class="card" id="' + 'card_' + categoryId + '_' + v.id + '">');
                $(cardName).append('<a href="/catalogue/' + v.category + '/items/' + v.id + '/"><img class="card-img-top" src="' + v.image + '" alt="' + v.caption + '" width=300></a>');
                $(cardName).append('<div class="card-block">');
                $(cardName).find('.card-block').append('<h4 class="card-title">' + v.name + '</h4>');
                $(cardName).find('.card-block').append('<p class="card-text">' + v.description + '</p>');
                $(cardName).find('.card-block').append('<a href="/catalogue/' + v.category + '/items/' + v.id + '/" class="btn btn-primary">Details</a>');

            };

        });

        $.getScript('/static/js/holder.min.js', function () {

            var cardNameCreate = "#card_" + categoryId + "_create";
            // Check if the card exists
            if ($(cardNameCreate).length === 0) {

                // Render the 'Add' card to the pack
                $(cardId).append('<div class="card" id="' + 'card_' + categoryId + '_create' + '">');
                $(cardNameCreate).append('<a href="/catalogue/0/items/new/"><img class="card-img-top" src="holder.js/300x200?text=Add Dinosaur!" alt=""></a>');
                $(cardNameCreate).append('<div class="card-block">');
                $(cardNameCreate).find('.card-block').append('<h4 class="card-title"></h4>');
                $(cardNameCreate).find('.card-block').append('<p class="card-text"></p>');
                $(cardNameCreate).find('.card-block').append('<a href="/catalogue/0/items/new/" class="btn btn-primary"><i class="fa fa-plus-circle fa-lg"></i></a>');

            }

        });

    })

    $(".nav-link").click(function () {

        // Get the Category Id from the element
        var categoryId = $(this).attr("id");

        // AJAX request to endpoint for Category Item JSON info
        $.get("/catalogue/" + categoryId, function (data) {

            var cardId = "#cards_" + categoryId;

            $.each(data.CategoryItems, function (k, v) {

                var cardName = "#card_" + categoryId + "_" + v.id;

                // Check if the card exists
                if ($(cardName).length === 0) {
                    // Add the card if it doesn't exist

                    //alert(v.description);
                    $(cardId).append('<div class="card" id="' + 'card_' + categoryId + '_' + v.id + '">');
                    $(cardName).append('<a href="/catalogue/' + categoryId + '/items/' + v.id + '/"><img class="card-img-top" src="' + v.image + '" alt="' + v.caption + '" width=300></a>');
                    $(cardName).append('<div class="card-block">');
                    $(cardName).find('.card-block').append('<h4 class="card-title">' + v.name + '</h4>');
                    $(cardName).find('.card-block').append('<p class="card-text">' + v.description + '</p>');
                    $(cardName).find('.card-block').append('<a href="/catalogue/' + categoryId + '/items/' + v.id + '/" class="btn btn-primary">Details</a>');

                };

            });


            //Load holder JS
            $.getScript('/static/js/holder.min.js', function () {

                var cardNameCreate = "#card_" + categoryId + "_create";
                // Check if the card exists
                if ($(cardNameCreate).length === 0) {
                    // Render the 'Add' card to the pack
                    $(cardId).append('<div class="card" id="' + 'card_' + categoryId + '_create' + '">');
                    $(cardNameCreate).append('<a href="/catalogue/' + categoryId + '/items/new/"><img class="card-img-top" src="holder.js/300x200?text=Add Dinosaur!" alt=""></a>');
                    $(cardNameCreate).append('<div class="card-block">');
                    $(cardNameCreate).find('.card-block').append('<h4 class="card-title"></h4>');
                    $(cardNameCreate).find('.card-block').append('<p class="card-text"></p>');
                    $(cardNameCreate).find('.card-block').append('<a href="/catalogue/' + categoryId + '/items/new/" class="btn btn-primary"><i class="fa fa-plus-circle fa-lg"></i></a>');

                }

            });

        })

    });

});
