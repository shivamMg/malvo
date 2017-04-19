$(document).ready(function() {
  var $qnoPanel = $("#question-no-panel");
  var $qchPanel = $("#question-choices-panel");
  var $questionNo = $("#question-no");
  var $questionText = $("#question-text");
  var $choices = $("#choices");

  // Check for unuploaded Answers
  var localAnswers = JSON.parse(localStorage.getItem("mcqs"));
  if (localAnswers === null) {
    localStorage.setItem("mcqs", JSON.stringify(Answers));
  } else {
    // Check if localAnswers equals uploaded Answers
    var equal = true;
    // Using keys for localAnswers (it will always be >= Answers)
    var keys = Object.keys(localAnswers);
    for (var i = 0; i < keys.length; i++) {
      if (localAnswers[keys[i]] != Answers[keys[i]]) {
        equal = false;
        break;
      }
    }
    if (!equal) {
      $(".load-answers.modal")
        .modal({
          closable: false,
          onApprove: loadFromStorage,
          onDeny: loadFromAnswers,
        })
        .modal("show");
    }
  }

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

  addQuestionPanelLabels();
  // Load first question
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

  function addQuestionPanelLabels() {
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
  }

  function loadFromStorage() {
    var keys = Object.keys(localAnswers);
    for (var i = 0; i < keys.length; i++) {
      Answers[keys[i]] = localAnswers[keys[i]];
    }
    addQuestionPanelLabels();
  }

  function loadFromAnswers() {
    localStorage.setItem("mcqs", JSON.stringify(Answers));
  }

  function submitAnswers() {
    var data = $.extend({}, Answers);
    data.csrfmiddlewaretoken = $.cookie("csrftoken");
    $.post("/mcqs/answer/", data, function() {
      localStorage.removeItem("mcqs");
      $(".success-submit.modal").modal("show");
    }).fail(function() {
      alert("Error occured while uploading answers. Please try again.");
    });
  }

  window.selectChoice = function selectChoice(ele) {
    var selectedChoiceId = $(ele).attr("id");
    var choiceNo = parseInt(selectedChoiceId.slice("choiceno".length));
    var curQuesNo = String(mcqObj.curQuesIndex + 1);
    Answers[curQuesNo] = choiceNo;
    // Update local answers
    localStorage.setItem("mcqs", JSON.stringify(Answers));

    $(".choice").removeClass("answered");
    $(ele).addClass("answered");
    $("#qno" + curQuesNo).addClass("answered");

    mcqObj.switchNextQues();
  };

  $("#submit-all").click(function() {
    // If all questions have not been solved
    if (Object.keys(Answers).length != mcqObj.questions.length) {
      $(".confirm-submit.modal")
        .modal({
          onApprove: submitAnswers
        })
        .modal("show");
      return;
    }
    submitAnswers();
  });
});
