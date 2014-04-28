$(document).ready(function (){
    change_password();
})

function change_password(){
    $("#changepwd_submit").click(function (){
        form = $("form#changepwd_form");
        messenger = Messenger();

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data){
                var response = JSON.parse(data);
                if(response.status == "success"){
                    messenger.post({
                        message: "Success   ",
                        type: "success"
                    })
                    window.location.href=response.redirect
                }
                else if(response.status == "error")
                    messenger.post({
                        message: response.content,
                        type: "error"
                    })
            },
        });
        return false;
    })
}


