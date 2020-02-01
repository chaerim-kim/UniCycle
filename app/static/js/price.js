
function checkChanged(){

  var daysPrice = document.getField("Select Days for Hire:").value;

  if (daysPrice=="1 Day") event.value = "£2.5";
  else if (daysPrice=="2 Days") event.value = "£4.9";
  else if (daysPrice=="3 Days") event.value = "£7.3";
  else if (daysPrice=="4 Days") event.value = "£9.7";
  else if (daysPrice=="5 Days") event.value = "£12.1";
  else if (daysPrice=="6 Days") event.value = "£14.5";
  else if (daysPrice=="7 Days") event.value = "£16.9";


  else event.value = "";
}

$(function(){
  $("#HirePeriod").on("change", function(event){

    var i;
    for (i = 0; i < 8; ++i) {
      var temp1 = "#" + i + "-days";
      $(temp1).hide();
    }

    var id = $("#HirePeriod :selected").val() + "-days";
    var id2 = "#" + id;
    $(id2).toggle();
    $(id2).removeClass("d-none");
  })

  $(id2).addClass("d-none");
})

$(document).ready($(".d-none").hide());
