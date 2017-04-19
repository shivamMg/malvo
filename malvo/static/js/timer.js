// Expects `RemainingTime` variable to be defined
// as the number of seconds remaining
var $timer = $("#timer");
var timerObj;
changeTimer();

if (typeof LockTimer === "undefined" || !LockTimer) {
  timerObj = setInterval(function() {
    changeTimer();
    RemainingTime -= 1;
  }, 1000);
}

function changeTimer() {
  if (RemainingTime <= 0) {
    clearInterval(timerObj);
    $timer.text("You've run out of time.");
    return;
  }
  var time = new Date(null);
  time.setSeconds(RemainingTime);
  $timer.text(time.toISOString().substr(11, 8));
}
