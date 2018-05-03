$( document ).ready( function() {
 
  function toggleActive ( selector ) {
    if ( !$(selector).hasClass("active") ) {
      $( "#view-grid, #view-list" ).toggleClass("active");
    }
  }
 
  function getResultData( selector ) {
    return {
      "imageUrl": $(selector).find("#user-image").attr("src"),
      "userUrl": $(selector).find("#user-full-name").attr("href"),
      "name": $(selector).find("#user-full-name").text(),
      "username": $(selector).find("#user-username").text()
    };
  }

  function getAllResultData () {
    var results = [];
    $(".list-result").each(
      function () {
        results.push( getResultData(this) );
      });
    return results;
  }

  function makeListViewItem (result) {
    var template = $( "#list-template" ).html();
    Mustache.parse(template);
    var rendered = Mustache.render(template, result);
    return rendered;
  }

  function appendListViewItems (results) {
    for(i=0; i < results.length; i++) {
      $("#list-results").append( makeListViewItem(results[i]) );
    }
  }

  $( "#view-grid, #view-list" ).on("click", function (event) {
    toggleActive(this);
    var results = getAllResultData();
    $("#list-results").empty();
    if ( $(this).attr("id") == "view-grid" ) {
    } else if ( $(this).attr("id") == "view-list" ) {
      appendListViewItems (results);
    }
  });

});
