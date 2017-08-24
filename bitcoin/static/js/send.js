var sendMoney = function() {
	walletFrom = $('#walletFrom option:selected').val();
    walletTo = $("#contactWallet").val();
    if (wallet_is_stranger == 1) {
		send_message("Sending money into the void..", "info")
		walletTo = "stranger";
	}
    amount = $("#amount").val();
    description = $("#description").val();
    $(".actions a[href$='#finish']").removeAttr('href').addClass('disabled');
    $.post('/processing', {'walletFrom': walletFrom, 'walletTo': walletTo, 'amount': amount, "description": description }, function(data, textStatus, xhr) {
    		
    		if (data.code == "200") {
    			send_message(data.result, "success")
    			
    			window.location = "/";
    		}
    		else if (data.code = "400") {
    			send_message(data.result, "danger")
    		}
    });
}

$(document).ready(function(){

    $('.single-transaction').click('click', function() {
        $("#walletTo").val($(this).find(".contactWallet").html());
        $('#f_walletTo').text($("#walletTo").val())
        $('#f_contactFirst').text($(this).find(".contactFirst").html())
        $('#f_contactLast').text($(this).find(".contactLast").html())
        adding_contact = 0;
        form.children("div").steps("next");
        form.children("div").steps("next");
    });

})