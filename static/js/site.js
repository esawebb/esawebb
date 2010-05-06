/*
# spacetelescope.org
# Copyright 2009-2010 ESO, ESA/Hubble, IAU
#
# Authors:
#   Lars Holm Nielsen <lnielsen@eso.org>
#   Luis Clara Gomes <lcgomes@eso.org>
#
*/

/* 
 * External link decorator 
 */
(function($) {
    $.fn.extend({
        extlink: function () {
            $("a", this).filter(function (i) {
                return (($(this).attr("target") == '_blank') && $(this).contents('img').size()==0);
            }).each(function () {
                $(this).addClass("extlink")
            });
        }
    });
})(jQuery);


$(document).ready(function () {
    $(this).extlink();
});


/* onFocus/onBlur events for search fields */
function searchbox_focus( box, text ) {
	if( box.value == text ){
		box.value='';
		box.className = box.className + '_ready';
	}
}

function searchbox_blur( box, text ) {
	if( box.value == '' ){
		box.value=text;
		box.className = box.className.split('_ready',1)[0];
	}
}


        
/* feature rotator */

$(".rotator").hover(
          function () {
              $(".fbut").fadeIn();
              
          }, 
          function () {
             $(".fbut").fadeOut();
          }
        )
        
$('.feature-fade').removeClass("init_hide")

$('.rotator .items' ).
            cycle({ 
                fx:    'fade', 
                timeout: 4000,
                speed:  1000,
                pause:  1,
                next:   '.fbut_right', 
                prev:   '.fbut_left',
                pager: '#feat-nav'
            });;

$('.fbut').fadeOut(0);
$('.fbut').removeClass('init_hide');