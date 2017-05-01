(function() {

    (function() {
        var url = window.location;
        
        $('ul.nav-pills a').filter(function() {
             return this.href == url;
        }).parent().addClass('active');
        autoRefresh(url);
    })()


    $('input.message-text').keyup(function() {
        var tweet_id = $(this).data('tweet-id');
        var elem = '#reply-submit-button-' + tweet_id;
        if($(this).val() !== '') {
            $(elem).removeAttr('disabled');
        } else {
            $(elem).attr('disabled', 'disabled');
        }
    })

    $('.reply-icon').click(function() {
        var tweet_id = $(this).data('tweet-id');
        var reply_input = '#reply-input-' + tweet_id;
        $(reply_input).toggle();
    })

    function autoRefresh(url){
       if (url.pathname === '/') {
            setTimeout(function(){
               window.location.reload(1);
            }, 60000);
       }
    }

})();
