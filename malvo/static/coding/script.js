$(document).ready(function() {
  var $timer = $("#timer");
  /* Initialize Showdown MDtoHTML Converter */
  var showdownConverter = new showdown.Converter();
  /* Initialize Timer */
  changeTimer();
  /* Start Timer */
  timeObj = setInterval(function() {
    if (RemainingTime <= 0) {
      clearInterval(timeObj);
      $timer.text("You've run out of time. Submitted answers will not be accepted.");
      return;
    }
    changeTimer();
    RemainingTime -= 1;
  }, 1000);

  $(".markdown").each(function(i, ele) {
    var md = $(ele).text();
    var html = showdownConverter.makeHtml(md);
    $(ele).html(html);
  });

  function changeTimer() {
    var time = new Date(null);
    time.setSeconds(RemainingTime);
    $timer.text(time.toISOString().substr(11, 8));
  }
});
