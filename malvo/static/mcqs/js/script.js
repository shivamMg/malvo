$(document).ready(function() {
  var $timer = $("#timer");
  var $qnoPanel = $("#question-no-panel");
  var $qchPanel = $("#question-choices-panel");
  var $questionNo = $("#question-no");
  var $questionText = $("#question-text");
  var $choices = $("#choices");

  $qchPanel.hide();

  /* Start Timer */
  var timerObj = setInterval(function() {
    if (RemainingTime <= 0) {
      clearInterval(timerObj);
      $timer.text("You've run out of time. Submitted answers will not be accepted.");
      return;
    }
    changeTimer();
    RemainingTime -= 1;
  }, 1000);

  var mcqObj = {
    questions: MCQs,
    /* `curQuesIndex` is the index of current question */
    curQuesIndex: -1,
    switchNextQues: function() {
      var i = mcqObj.curQuesIndex;
      i = (i == mcqObj.questions.length-1) ? 0 : ++i;
      switchQuestion(i);
    },
    switchPrevQues: function() {
      var i = mcqObj.curQuesIndex;
      i = (i === 0) ? mcqObj.questions.length-1 : --i;
      switchQuestion(i);
    }
  };

  /* Add Question Panel Buttons */
  var panelButtons = "";
  for (var i = 0; i < mcqObj.questions.length; i++) {
    if (Answers[String(i+1)] === "" || typeof Answers[String(i+1)] === "undefined") {
      panelButton = '<span class="qno-panel-label" id="qno' + String(i+1) + '">' + String(i+1) + '</span>';
    } else {
      panelButton = '<span class="qno-panel-label answered" id="qno' + String(i+1) + '">' + String(i+1) + '</span>';
    }
    panelButtons += panelButton;
  }
  $qnoPanel.html(panelButtons);

  switchQuestion(0);

  $(document).on("click", ".qno-panel-label", function() {
    var $this = $(this);
    var qno = parseInt($this.text());
    var index = qno - 1;
    switchQuestion(index);
  });

  $("#next-question").click(function() {
    mcqObj.switchNextQues();
  });

  $("#prev-question").click(function() {
    mcqObj.switchPrevQues();
  });

  function switchQuestion(index) {
    if (index == mcqObj.curQuesIndex) {
      return;
    }

    var choices = "";
    var question = mcqObj.questions[index];

    $qchPanel.fadeOut(300, function() {
      $questionNo.text("Q " + String(question.qno));
      /* Convert Markdown text to HTML */
      var qtextHtml = showdownConverter.makeHtml(question.qtext);

      $questionText.html(qtextHtml);

      $.each(question.choices, function(i, choice) {
        /* Highlight the choice if it has already been selected as answer */
        var choiceId = "choiceno" + String(choice.no);
        var choiceText = showdownConverter.makeHtml(choice.text);
        if (choice.no == Answers[String(question.qno)] && typeof Answers[String(question.qno)] != "undefined") {
          var div = '<div class="ui segment choice answered" onclick="selectChoice(this)" id="' + choiceId + '">' + choiceText + '</div>';
        } else {
          var div = '<div class="ui segment choice" onclick="selectChoice(this)" id="' + choiceId + '">' + choiceText + '</div>';
        }

        choices +=  div;
      });
      $choices.html(choices);

      /* Apply Highlightjs */
      $("pre code").each(function(i, block) {
        hljs.highlightBlock(block);
      });
    }).fadeIn(100);

    $("#qno" + String(mcqObj.curQuesIndex + 1)).removeClass("current");
    mcqObj.curQuesIndex = index;
    $("#qno" + String(mcqObj.curQuesIndex + 1)).addClass("current");
  }

  window.selectChoice = function selectChoice(ele) {
    var selectedChoiceId = $(ele).attr("id");
    var choiceNo = parseInt(selectedChoiceId.slice("choiceno".length));
    var curQuesNo = String(mcqObj.curQuesIndex+1);
    Answers[curQuesNo] = choiceNo;
    $(ele).addClass("answered");

    /* Mark Question as answered in question-no-panel */
    $("#qno" + curQuesNo).addClass("answered");

    /* Switch to next question */
    mcqObj.switchNextQues();
  };

  $("#submit-all").click(function() {
    /* If all questions have not been solved */
    if (Object.keys(Answers).length != mcqObj.questions.length) {
      var submitAnswers = confirm("You have not answered all questions. Would you still like to continue uploading answers?");
      /* If user cancels confirmation, don't upload answers */
      if (submitAnswers === false) {
        return;
      }
    }

    var data = $.extend({}, Answers);
    data.csrfmiddlewaretoken = $.cookie("csrftoken");
    $.post("/mcqs/answer/", data, function() {
      console.log("Answers uploaded.");
      $(".ui.basic.small.modal").modal("show");
      // alert("Answers uploaded.");
    }).fail(function() {
      console.log("Error occured while uploading answers.");
      alert("Error occured while uploading answers.");
    });
  });

  function changeTimer() {
    var time = new Date(null);
    time.setSeconds(RemainingTime);
    $timer.text(time.toISOString().substr(11, 8));
  }
});
