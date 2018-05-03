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

  function makeListViewItem (results) {
    var template = $( "#list-template" ).html();
    Mustache.parse(template);
    var rendered = Mustache.render(template, results);
    return rendered;
  }

  $( "#view-grid" ).on("click", function (event) {
    toggleActive(this);
    var results = getAllResultData();
    console.log(results[0]);
    console.log(makeListViewItem(results[0]));
  });

  $( "#view-list" ).on("click", function (event) {
    toggleActive(this);
		var results = getAllResultData();
  });

});
