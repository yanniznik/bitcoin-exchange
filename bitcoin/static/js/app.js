$(document).ready(function(){
	current_amount = parseFloat($("#wallet_amount").text());
	rate = parseFloat($("#rate").text());
	wallet_worth = current_amount * rate;
	$("#worth").text(wallet_worth.toFixed(2))

	var current_wallet = $("#wallet_address").text()

	$(".transactionFrom").each(function( index ) {
		if ($(this).text() == current_wallet) {
			$(this).closest(".single-transaction").addClass('moneyout');
			$(".moneyout").each(function(index) {
				$(this).find(".sign").text('-')
			});
		}
});
	
})




var send_message = function(message, type) {
    $("#exception_handler").removeClass().addClass("bg-" + type).text(message);
    $("#exception_handler").slideDown("fast")
    setTimeout(function() {
        $("#exception_handler").slideUp("fast")
    },2500)
}
