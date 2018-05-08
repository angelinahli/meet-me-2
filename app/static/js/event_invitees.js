$( document ).ready( function() {
  
  /* shelving this because I don't know how to use it for now */
  var userSearchUrl = "/search_invitees/";
  var verifyUserUrl = "/is_valid_user/";
  var usersInputGroup = $("#search-usernames").closest(".input-group");
  var addedUsers = []; /* is this okay :/ */
  
  function renderTemplate(templateSelector, data) {
    var template = $( templateSelector ).html();
    Mustache.parse(template);
    var rendered = Mustache.render(template, data);
    return rendered;
  }

  function addErrorMessage(message) {
    var errorMessage = renderTemplate("#error-template", {"message": message});
    $("#username-group").append(errorMessage);
  }
  
  function makeReturnValue() {
    $("#return-usernames").val(addedUsers.join(","));
  }

  function addUser(username) {
    addedUsers.push(username);
    makeReturnValue();
  }

  function removeUser(username) {
    /* from stackoverflow */
    addedUsers.splice( $.inArray(username, addedUsers), 1 );
    makeReturnValue();
  }

  function clearSearchUsernames(clearVal) {
    if (clearVal) {
      $("#search-usernames").val("");
    }
    $(".text-error").remove();
    $(".btn-add-invitee").remove();
    $("#search-usernames").removeClass("border border-right-0");
  }

  function addUserIfValid(username, data) {
    var valid = data.valid;
    var added = $.inArray(username, addedUsers) != -1;
    /* clear any previous successful username attempts */
    clearSearchUsernames(false);
    if (added) {
      addErrorMessage("User has already been added!");
    } else if (valid) {
      /* if valid and not added */
      var button = renderTemplate("#add-invitee-template", {});
      $("#search-usernames").addClass("border border-right-0");
      usersInputGroup.append(button);
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

  $(document).on("click", ".invitee-cancel", function() {
    var btn = $(this).closest(".btn-invitee");
    var username = btn.find(".btn-username").val();
    btn.remove();
    removeUser(username);
  })

  $(document).on("click", ".btn-add-invitee", function() {
    var username = $("#search-usernames").val();
    var userButton = renderTemplate("#invitee-template", {"name": username});
    $("#username-group").append(userButton);
    addUser(username);
    clearSearchUsernames(true);
  });

  $("#search-usernames").on("input", function (event) {
    var username = $(this).val();
    $.post(
      verifyUserUrl,
      {"username": username},
      function(data) {
        addUserIfValid(username, data);
      });
  });

});
