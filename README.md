# Django-Barcode-Auth #
  
  [[http://github.com/lrvick/django-barcode-auth]]

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

## Usage / Installation ##

  1. Add django-barcode-auth to INSTALLED_APPS

  2. Ensure your login template is including jquery, and barauth.js

        <head>
          ...
          <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
          <script type="text/javascript" src="{{ STATIC_URL }}js/barauth.js"></script>
          ...
        </head>

  3. Stick an empty form with the id 'barauth_form' and a csrf_token somewhere in your template.

        <form id="barauth_form" method="POST" action="">
          {% csrf_token %}
        </form>

  When loaded this will create and focus a hidden form field.
  
  Most barcode scanners emulate keyboard entry followed by enter.

  The form will auto-submit on enter. If the string from the barcode was correct, 
  the user will be logged in as usual and you are free to use user.is_authenticated 
  as usual

  The app also includes a signal that will auto-generate a barcode on new user creation
  You can determine its location using the included barcode_hash filter like so: 
    
    {% load barcode_auth %}
    {{ STATIC_ROOT }}/img/barcodes/{{ user.username|barcode_hash }}.png 
  
## Notes ##
    
  Use at your own risk. You may be eaten by a grue.

  Questions/Comments? Please check us out on IRC via irc://udderweb.com/#uw
