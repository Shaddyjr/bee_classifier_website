'use strict';

( function ( document)
{
    const form = document.querySelector('form');
    const input = form.querySelector( 'input[type="file"]' );
    input.addEventListener( 'change', function( e )
    {
        form.submit();
    });

}( document));
