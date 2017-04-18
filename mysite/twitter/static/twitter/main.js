(function() {

    $('#message-text').keyup(function() {
        if($(this).val() !== '') {
            $('#submit-button').removeAttr('disabled');
        } else {
            $('#submit-button').attr('disabled', 'disabled');
        }
    })

})();
