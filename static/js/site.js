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

/*shadowbox */

$(document).ready( function(){
	var options = {
		assetURL: MEDIA_URL + "djangoplicity/shadowbox3/",
		handleLgImages: "resize",
		players : ["img","html","flv","qt","wmp"],
    };
    Shadowbox.init(options);	


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