$( document ).ready( function() {
  
  /* shelving this because I don't know how to use it for now */
  var userSearchUrl = "/search_invitees/";
  var verifyUserUrl = "/is_valid_user/";
  var usersInputGroup = $("#search-usernames").closest(".input-group");
  var usernameGroup = usersInputGroup.next(".username-group")
  
  function renderTemplate(templateSelector, data) {
    var template = $( templateSelector ).html();
    Mustache.parse(template);
    var rendered = Mustache.render(template, data);
    return rendered;
  }

  function addErrorMessage(message) {
    var errorMessage = renderTemplate("#error-template", {"message": message});
    usernameGroup.append(errorMessage);
  }

  function addUserIfValid(data) {
    var valid = data.valid;
    usernameGroup.empty();
    $(".btn-add-invitee").remove();
    if (valid) {
      var button = renderTemplate("#add-invitee-template", {});
      usersInputGroup.append(button);
    } else {
      var msgText = "This username is not valid";
      var errorMsg = renderTemplate("#error-template", {"message": msgText});
      usernameGroup.append(errorMsg);
    }
  }

  $(document).on("mouseenter", ".btn-invitee", function() {
    $(this)
      .find(".invitee-cancel")
      .removeClass("far")
      .addClass("fas");
  });

  $(document).on("mouseleave", ".btn-invitee", function() {
    $(this)
      .find(".invitee-cancel")
      .removeClass("fas")
      .addClass("far");
  });

  $(".btn-add-invitee").on("click", function() {
    var username = $("#search-usernames").val();
    var userButton = renderTemplate("#invitee-template", {"name": username});
    usernameGroup.append(userButton);
    $("#search-usernames").removeAttr("value");
  });

  $("#search-usernames").on("input", function (event) {
    var username = $(this).val();
    $.post(
      verifyUserUrl,
      {"username": username},
      addUserIfValid
    );
  });

});
