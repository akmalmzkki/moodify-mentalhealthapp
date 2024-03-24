// for scrolling messages
function scrollToBottom() {
    var div = $("#upperid");
    div.scrollTop(div.prop("scrollHeight"));
}

scrollToBottom();

$("#userinputform").submit(function(event) {
    event.preventDefault();
    formsubmitted();
});

// sending request to python server
const formsubmitted = async () => {
    let userinput = $('#userinput').val();
    let sendbtn = $('#sendbtn');
    let userinputarea = $('#userinput');
    let upperdiv = $('#upperid');

    upperdiv.append(
        `<div class="message">
            <div class="usermessagediv">
                <div class="usermessage">
                    ${userinput}
                </div>
            </div>
        </div>`
    );

    sendbtn.prop('disabled', true);
    userinputarea.prop('disabled', true);
    scrollToBottom();
    $('#userinput').val("");
    $('#userinput').attr('placeholder', "Wait . . .");

    $.ajax({
        url: "/chat",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ 
            data: userinput
        }),
        success: function(json) {
            $('#userinput').attr('placeholder', "Your message...");

            if (json.response) {
                let message = json.message.toString();

                upperdiv.append(
                    `<div class="message">
                        <div class="appmessagediv">
                            <div class="appmessage" id="temp">
                                
                            </div>
                        </div>
                    </div>`
                );
                
                let temp = $('#temp');
                let index = 0;

                function displayNextLetter() {
                    scrollToBottom();
                    if (index < message.length) {
                        temp.append(message[index]);
                        index++;
                        setTimeout(displayNextLetter, 10);
                    } else {
                        temp.removeAttr('id');
                        sendbtn.prop('disabled', false);
                        userinputarea.prop('disabled', false);
                    }
                }

                displayNextLetter();
                scrollToBottom();
            } else {
                let message = json.message;
                upperdiv.append(
                    `<div class="message">
                        <div class="appmessagediv">
                            <div class="appmessage" style="border: 1px solid red;">
                                ${message}
                            </div>
                        </div>
                    </div>`
                );
                sendbtn.prop('disabled', false);
                userinputarea.prop('disabled', false);
            }
            scrollToBottom();
        },
        error: function(xhr, textStatus, errorThrown) {
            console.error("Error occurred while sending request:", errorThrown);
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: errorThrown,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'OK'
            });
        }
    });
};
