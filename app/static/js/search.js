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

  function renderTemplate(templateSelector, data) {
    var template = $( templateSelector ).html();
    Mustache.parse(template);
    var rendered = Mustache.render(template, data);
    return rendered;
  }

  function makeListViewItems(results) {
    /** Start with the assumption that #list-results has been emptied **/
    $("#list-results").append(renderTemplate("#list-wrapper-template", {}));
    var listViewItems = $("#list-results")
      .find(".list-group");
    for(i=0; i < results.length; i++) {
      $(listViewItems).append(renderTemplate("#list-template", results[i]));
    }
    $("#list-results").append(listViewItems);
  }

  function makeGridViewItems(results) {
    $("#list-results").append(renderTemplate("#grid-wrapper-template", {}));
    var gridViewItems = $("#list-results")
      .find(".row");
    for(i=0; i < results.length; i++) {
      $(gridViewItems).append(renderTemplate("#grid-template", results[i]));
    }
    $("#list-results").append(gridViewItems);
  }

  $( "#view-grid, #view-list" ).on("click", function (event) {
    toggleActive(this);
    var results = getAllResultData();
    $("#list-results").empty();
    if ( $(this).attr("id") == "view-grid" ) {
      makeGridViewItems(results);
    } else if ( $(this).attr("id") == "view-list" ) {
      makeListViewItems(results);
    }
  });

});
