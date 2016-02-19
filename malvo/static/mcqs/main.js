var McqObj = {
  questions: [],
  /* `len` would be the total number of questions */
  len: 0,
  curQuesIndex: 0,
  switchNextQues: '',
  switchPrevQues: ''
};

/* `Answers` contains question number as keys and answered choice as value */
var Answers = {};

$(document).ready(function() {

  $.getJSON("/static/mcqs/mcq_dump.json", function(data) {
    McqObj.questions = data;
    McqObj.len = data.length;
    McqObj.curQuesIndex = 0;
    console.log("Questions loaded.");
    switchQuestion(0);
    /* Initialize `Answers` */
    for (i = 1; i <= McqObj.len; i++) {
      Answers[String(i)] = "";
    }
    console.log(Answers);
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
    McqObj.curQuesIndex = i;
    switchQuestion(i);
  };

  McqObj.switchPrevQues = function() {
    var i = McqObj.curQuesIndex;
    i = (i === 0) ? McqObj.len-1 : --i;
    McqObj.curQuesIndex = i;
    switchQuestion(i);
  };

  function switchQuestion(index) {
    var choices = "";
    var curQues = McqObj.questions[McqObj.curQuesIndex];

    $("#question_no").text(curQues.qno);
    $("#question_text").text(curQues.qtext);
    
    $.each(curQues.choices, function(i, choice){
      var div = '<div class="choices" onclick="selectChoice(this)">' + choice + '</div>';
      choices +=  div;
    });
    $("#choices").html(choices);
  }

  window.selectChoice = function selectChoice(ele) {
    var selectedChoice = $(ele).text();
    var curQuesNo = String(McqObj.curQuesIndex + 1);
    Answers[curQuesNo] = selectedChoice;
  };
  
});