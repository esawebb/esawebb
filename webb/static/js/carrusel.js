// Prepare PR carousel
$(document).ready(function(){
	$('#pr-carousel').slick({
		infinite: true,
		lazyLoad: 'progressive',
		prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>',
		autoplay: true,
		autoplaySpeed: 10000
	});
});