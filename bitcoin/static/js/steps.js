var form = $("#send-form");
var wallet_is_stranger = 0;
var adding_contact = 1;


form.children("div").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "none",
    onStepChanging: function (event, currentIndex, newIndex)
    {
        if (currentIndex > newIndex)
        {
            return true;
        }
        if(currentIndex == 0) {
            amount = $("#amount").val();
            if (amount <= 0) {
                send_message("error! No amount set", "danger")
                return false;
            }
            else {
                description = $("#description").val();
                amount = parseFloat($("#amount").val());
                amount_usd = parseFloat($("#amount-usd").val());
                $('#f_description').text(description);
                $('#f_amount_to').text(amount);
                $('#f_amount_to_usd').text(amount_usd);
                $('#f_amount').text(amount.toFixed(5));
                $('#f_amount_usd').text(amount_usd);
            }

        }
        

        if(currentIndex == 1) {
            walletTo = $("#walletTo").val();
            walletFrom = $('#walletFrom option:selected').val();
            if (walletTo == walletFrom) {
                send_message("Can't send to yourself!", "danger")
                return false;
            }
            $.post('/checkwallet', {"walletTo": walletTo}, function(data, textStatus, xhr) {
                if (data.result == "known") {
                    send_message("Wallet is registered. No fee!", "success");
                    $("#fee").text("0")
                    wallet_is_stranger = 0;
                }
                else {
                    send_message("Wallet not on platform, adding fee", "info");
                    console.log(data.result);
                    fee = 0.001
                    $("#fee").text(fee);
                    amount = parseFloat($("#amount").val());
                    amount_with_fee = amount * (1 - fee)
                    $('#f_amount_to').text(amount_with_fee.toFixed(5))
                    $('#f_amount_to_usd').text(parseFloat($("#amount-usd").val())* (1 - fee))
                    wallet_is_stranger = 1;
                }  
            });

            $("#contactWallet").val(walletTo);
            return true;

        }
        if(currentIndex == 2 && adding_contact == 1) {
            contactFirst = $("#contactFirst").val();
            contactLast = $("#contactLast").val();
            if (contactFirst.length == 0 || contactLast.length == 0) {
                send_message("Please enter First and Last Name", "danger");
                return false;
            }
            contactEmail = $('#contactEmail').val();
            contactWallet = $('#contactWallet').val();
            $("#walletTo").val($(this).find(".contactWallet").html());
            $('#f_walletTo').text(contactWallet)
            $('#f_contactFirst').text(contactFirst)
            $('#f_contactLast').text(contactLast)
            $.post('/createcontact', {"first_name": contactFirst, "last_name": contactLast, "email": contactEmail, "wallet": contactWallet}, function(data, textStatus, xhr) {
                if (data.code == "200") {
                    send_message(data.result, "success")
                    return true;
                }
                else if (data.code = "401") {
                    send_message(data.error, "danger")
                    return false;
                }
            });
            return true;



            
        }
        else {
            return true;   
        }


    },
    onStepChanged: function (event, currentIndex, priorIndex)
    {
        if (currentIndex === 2 && priorIndex === 3)
        {
            form.children("div").steps("previous");
        }

        if (currentIndex === 3)
        {

        }

    },
    onFinishing: function (event, currentIndex)
    {
        if ( $('#acceptTerms').is(':checked') ) {
            $('#acceptContainer').removeClass()
            sendMoney(); 
            return true;
        } 
        else {
            $('#acceptContainer').addClass('bg-danger')
            return false;  
        }

    },
    onFinished: function (event, currentIndex)
    {

    }
});

$("#example-basic").steps({
    headerTag: "h3",
    bodyTag: "section",
    transitionEffect: "slideLeft",
    autoFocus: true,
    onStepChanging: function (event, currentIndex, newIndex)
    {
        if (currentIndex > newIndex)
        {
            return true;
        }
        if(currentIndex == 0) {
            amount = $("#amount").val();
            if (amount <= 0) {
                send_message("error! No amount set", "danger")
                return false;
            }
            else {
                amount = $("#amount").val();
                amount_usd = $('#amount-usd').val();
                description = $("#description").val();
                $('#f_amount').add('#requested-bc-amount').text(amount)
                $('#requested-bc-amount-usd').text(amount_usd);
                $('#f_description').add('#requested-bc-description').text(description)
                return true;
            }

        }
    }
});