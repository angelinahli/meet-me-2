$("#delete").click( function() {
  return confirm("Are you sure?\nThis action cannot be undone!");
});
// $("#delete").on("click", function () {
//   return $.confirm({
//     title: "Are you sure?",
//     content: "This action is permanent and will delete all data associated with your account!",
//     buttons: {
//       ok: {
//         btnClass: "btn-danger"
//       },
//       cancel: {
//         btnClass: "btn-primary"
//       }
//     }
//   });
// });