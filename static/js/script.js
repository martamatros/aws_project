

$( document ).ready(function() {
  $("select").imagepicker()
});

$("img").on("click", function() {
  $("select").data('picker').sync_picker_with_select();
});
