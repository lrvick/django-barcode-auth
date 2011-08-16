# Django-Barcode-Auth #
  
  <http://github.com/lrvick/django-barcode-auth>

## About ##

  A system that lets you use any barcode scanner that emulates a
  keyboard (most of them do) and use it to log-in a user via 
  django's auth system.
    
  Ideal for touch-screen kiosk deployments, cash registers, people
  who want to feel like James Bond when they log in to their blog, etc.

  Also has hooks to generate barcodes for all users, that can 
  be obtained and printed from an admin interface.

## Current Features ##
 
  * Includes a signal so barcodes are generated on regular user creation
  * Easy template to generate/verify hashes from barcodes
  * Invisibly login when a barcode is scanned via jQuery
  * Can be included and used as a standard django authentication backend
  * Supports printing cards to CR80 sized card printers

## Usage / Installation ##

  1. Add django-barcode-auth to INSTALLED_APPS

  2. Ensure your login template is including jquery, and barauth.js

        <head>
            ...
            <script type="text/javascript" src="{{ STATIC_URL }}js/barauth.js"></script>
            ...
        </head>

  3. Optionally provide a host to post the logins to (if different from server including barauth.js)    

        <script>
            var window.barauth_host = 'myhost.com'
        </script>

  When loaded this will remain in the background looking for keyboard input
  that matches the specific pattern encoded into the barcodes barauth generates.
  
  Most barcode scanners emulate keyboard entry, thus when the string is seen by
  the script, it will automatically try to use it to login that user.

  This also means you can log in at any time from any page, which is useful
  in a kiosk scenario where people can come and go at any time.

  The app also includes a signal that will auto-generate a barcode on new user creation
  You can determine its location using the included barcode_hash filter like so: 
    
    {% load barcode_auth %}
    {{ STATIC_ROOT }}/img/barcodes/{{ user.username|barcode_hash }}.png 
  
  Additionally if the variable PRINT_CARDS is set in settings.py, barauth will
  print a CR80 sized card to the default printer.

  You can explicitly set the printer with the PRINTER variable.

  Example settings.py:
    
    PRINT_CARDS = 1
    PRINTER = 'card_printer' 

### Manual use with GET ###

  To manually log-in, you need only to format a GET request.

  Log-in's GET's should be formatted as follows:

    ?barcode_data=USER_ID|BARCODE_HASH

  By default, if login is sucessful it will 301 redirect back to the referring URL, 
  with a GET request attached.

  If login is invalid it will return a GET of: 
 
    ?login=true&email=user@example.com&full_name=First%20Last

  If successful:

    ?login=false

  Example using curl and a valid user_id/hash for the user John Doe:

    curl -sI "http://localhost/barauth/login?barcode_data=65|162112bb5765fb28fd153255d7694dc213665a5972cd06ce2c92e2ee" --referer http://mysite.com | grep Location

  Output:

    Location: http://mysite.com?login=true&email=john@doe.com&full_name=John%20Doe

  If this was in fact not a valid user it would return:

    Location: http://mysite.com?login=false


## Notes ##
    
  Use at your own risk. You may be eaten by a grue.

  Questions/Comments? Please check us out on IRC via irc://udderweb.com/#uw
