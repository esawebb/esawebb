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
