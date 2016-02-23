var McqObj = {
  questions: [],
  /* `len` would be the total number of questions */
  len: 0,
  /* `curQuesIndex` is the index of current question */
  curQuesIndex: 0,
  switchNextQues: '',
  switchPrevQues: ''
};

$(document).ready(function() {
  /* Hide questions panel */
  var panel = $("#questions_panel");
  panel.hide();

  $.getJSON("/static/mcqs/mcq_dump.json", function(data) {
    console.log("MCQs downloaded.");

    McqObj.questions = data;
    McqObj.len = data.length;
    McqObj.curQuesIndex = 0;

    switchQuestion(0);
    /* 
     * - Initialize `Answers` with empty answers.
     * - Create panel buttons.
     */
    var panelButtons = "";
    for (i = 0; i < McqObj.len; i++) {
      var panelButton = '<input type="button" onclick="switchQuestion(' + String(i) + ')" value="' + String(i+1) + '"/>';
      panelButtons += panelButton;
    }
    /* Add buttons to panel */
    panel.html(panelButtons);

  }).fail(function() {
    console.log("Error occured while downloading MCQs. Try reloading page.");
  });

  $("#next_question").click(function() {
    McqObj.switchNextQues();
  });

  $("#prev_question").click(function() {
    McqObj.switchPrevQues();
  });

  McqObj.switchNextQues = function() {
    var i = McqObj.curQuesIndex;
    i = (i == McqObj.len-1) ? 0 : ++i;
    switchQuestion(i);
  };

  McqObj.switchPrevQues = function() {
    var i = McqObj.curQuesIndex;
    i = (i === 0) ? McqObj.len-1 : --i;
    switchQuestion(i);
  };

  window.switchQuestion = function switchQuestion(index) {
    var choices = "";
    var question = McqObj.questions[index];

    $("#question_no").text(question.qno);
    $("#question_text").text(question.qtext);
    
    $.each(question.choices, function(i, choice) {
      /* Highlight the choice if it has already been selected as answer */
      if (choice == Answers[question.qno]) {
        div = '<div class="choices selected" onclick="selectChoice(this)">' + choice + '</div>';
      } else {
        div = '<div class="choices" onclick="selectChoice(this)">' + choice + '</div>';
      }

      choices +=  div;
    });
    $("#choices").html(choices);

    McqObj.curQuesIndex = index;
  };

  window.selectChoice = function selectChoice(ele) {
    var selectedChoice = $(ele).text();
    var curQuesNo = String(McqObj.curQuesIndex+1);
    Answers[curQuesNo] = selectedChoice;
    /* Switch to next question */
    McqObj.switchNextQues();
  };
  
  $("#submit_all").click(function() {
    /* Check if all questions have been solved (No answer is empty) */
    var allAnswersSolved = true;
    $.each(Answers, function(qno, answer) {
      if (answer === "") {
        allAnswersSolved = false;
        return;
      }
    });

    if (allAnswersSolved === false) {
      var submitAnswers = confirm("You have not answered all questions. Would you still like to continue uploading answers?");
      /* If user cancels confirmation, don't upload answers */
      if (submitAnswers === false) {
        return;
      }
    }

    var data = Answers;
    data.csrfmiddlewaretoken = csrfmiddlewaretoken;
    $.post("/mcqs/answer/", data, function() {
      console.log("Answers uploaded.");
      alert("Answers uploaded.");
    }).fail(function() {
      console.log("Error occured while uploading answers.");
      alert("Error occured while uploading answers.");
    });
  });

  /* Toggle Questions Panel */
  $("#panel_toggle_button").click(function() {
    panel.slideToggle("slow");
  });

});