function barauth(){
    $('<input style="position:absolute;left:-200%;" id="barauth_form" type="text">').prependTo('body')
    $('#barauth_form').focus()
}
$(document).ready(function() {
    $('#login').click(function(){barauth()});
});
