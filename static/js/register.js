$(document).ready(function (){
    register();
})

function register(){
    $("#register_submit").click(function (){
        form = $("form#register_form");
        messenger = Messenger();

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            success: function (data){
                var response = JSON.parse(data);
                if(response.status == "success"){
                    messenger.post({
                        message: "Register success",
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


