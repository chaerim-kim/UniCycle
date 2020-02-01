$("#cash_received").on("input", function(){
  var paid = $(this).val();
  var price = $("#price").text();

  $("#change").text("Change Due: £" + parseFloat(paid - price).toFixed(2));
})
