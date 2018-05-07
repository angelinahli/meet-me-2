$( document ).ready( function() {
  
  /* shelving this because I don't know how to use it for now */
  var userSearchUrl = "/search_invitees/";
  
  function renderTemplate(templateSelector, data) {
    var template = $( templateSelector ).html();
    Mustache.parse(template);
    var rendered = Mustache.render(template, data);
    return rendered;
  }

  $("#search-usernames")
    .closest(".input-group")
    .next(".username-group")
    .append(renderTemplate("#invitee-template", {"name": "angelinali"}));
  var value = $("#search-usernames").val();
  $("#return-usernames").val(value + ",angelinali");

  $(".btn-invitee").on("mouseenter", function() {
    $(this)
      .find(".invitee-cancel")
      .removeClass("far")
      .addClass("fas");
  });

  $(".btn-invitee").on("mouseleave", function() {
    $(this)
      .find(".invitee-cancel")
      .removeClass("fas")
      .addClass("far");
  });

  $( "#search-usernames" ).on("input", function (event) {

  });

});
