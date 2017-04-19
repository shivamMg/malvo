$(document).ready(function() {
  /* Initialize Showdown MDtoHTML Converter */
  var showdownConverter = new showdown.Converter();

  $(".markdown").each(function(i, ele) {
    var md = $(ele).text();
    var html = showdownConverter.makeHtml(md);
    $(ele).html(html);
  });
});
