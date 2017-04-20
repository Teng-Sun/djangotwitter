(function() {

    $('input.message-text').keyup(function() {
        var coun = $(this).data('coun');
        var elem = '#reply-submit-button-' + coun;
        if($(this).val() !== '') {
            $(elem).removeAttr('disabled');
        } else {
            $(elem).attr('disabled', 'disabled');
        }
    })

    $('.reply-icon').click(function() {
        var counter = $(this).data('counter');
        var reply_input = '#reply-input-' + counter;
        $(reply_input).toggle();
    })

})();
