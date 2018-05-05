/* shelved until I learn a bit more */
$( document ).ready( function() {

  var userSearchUrl = "/search_invitees/";
  
  function renderTemplate(templateSelector, data) {
    var template = $( templateSelector ).html();
    Mustache.parse(template);
    var rendered = Mustache.render(template, data);
    return rendered;
  }

  $( "#search-usernames" )
    .on("input", function (event) {
      var query = $(this).val();
      $.get(
        userSearchUrl,
        {"query": query},
        function (data) {
          console.log(data);
        }
      );

  });

});
