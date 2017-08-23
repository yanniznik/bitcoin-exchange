$(document).ready(function(){
	current_amount = parseFloat($("#wallet_amount").text());
	rate = parseFloat($("#rate").text());
	wallet_worth = current_amount * rate;
	$("#worth").text(wallet_worth.toFixed(2))
})


var send_message = function(message, type) {
    $("#exception_handler").removeClass().addClass("bg-" + type).text(message);
    $("#exception_handler").slideDown("fast")
    setTimeout(function() {
        $("#exception_handler").slideUp("fast")
    },2500)
}
