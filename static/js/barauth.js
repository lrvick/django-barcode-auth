function barauth(){
    $('<input name="barcode_data" style="position:absolute;left:-200%;" id="barauth_input" type="text">').prependTo('#barauth_form')
    $('#barauth_input').focus()
    $('#barauth_input').keyup(function(e) {
        if(e.keyCode == 13) {
            e.preventDefault();
            $.post("/", $("#barauth_form").serialize());
        }
    });
}
$(document).ready(function() {
    barauth()
});
