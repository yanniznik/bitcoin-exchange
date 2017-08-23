$(document).ready(function(){
	$("#amount").keyup(function(event) {
		rate = parseFloat($("#rate").text());
		bitcoin_amount = parseFloat($(this).val());
		converted_amount = bitcoin_amount * rate
		$('#amount-usd').val(converted_amount.toFixed(5));
	});
	$("#amount-usd").keyup(function(event) {
		rate = parseFloat($("#rate").text());
		bitcoin_amount = parseFloat($(this).val());
		converted_amount = bitcoin_amount / rate
		$('#amount').val(converted_amount.toFixed(5));
	});
})
