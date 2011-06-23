var keys='';
var header_found
var username
document.onkeypress = function(e) {
    get = window.event?event:e;
    key = get.keyCode?get.keyCode:get.charCode;
    key = String.fromCharCode(key);
    if (header_found == true){
        if (username == null){
            if (key == '|'){
                username = keys
                keys = ''
            } 
        } else if (keys.length == 56){
            hash = keys
            barcode_data = username + '|' + hash
            if (window.barauth_host != undefined ){
                host = window.barauth_host
            } else if (window.location.port != 80) {
                host = window.location.hostname + ':' + window.location.port
            } else {
                host = window.location.hostname
            }
            auth_url = 'http://' + host + '/barauth/login?barcode_data=' + barcode_data
            window.location = auth_url
        }
        if (key != '|'){ 
            keys+=key;
        }
    } else {
        if (key == '#'){
            keys+=key;
        } 
        if (keys == '####'){
            header_found = true
            keys = ''
        }
    }
}
