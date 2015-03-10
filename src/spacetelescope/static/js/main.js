// Mobile menu

$(document).ready(function() {
	$('.menu-trigger').click(function(){
		$('.level0').toggleClass('open-menu');
		return false;
	});

	$('.mobile-children').click(function(event){
		$(this).parent().find('ul:first').toggleClass('open-menu');
		return false;
	});
});


// Menu

$(document).ready(function() {

	var hoverDelay = 300;
	var hoverInID;
	var hoverOutID;

	function activateMenu() {
		var $mainmenu = $('.mainmenu-aim');
		var $menu = $('.submenu-aim');

		$mainmenu.menuAim({
			activate: activateMainSubmenu,
			deactivate: deactivateMainSubmenu,
			exitMenu: exitMainMenu,
			tolerance: 100,
			submenuDirection: 'below'
		});

		$menu.menuAim({
			activate: activateSubmenu,
			deactivate: deactivateSubmenu,
			exitMenu: exitMenu,
			submenuSelector: '.submenu'
		});

		// Set top content margin on pages with at least one level1
		// submenu selected
		if ($('.level1.current').length !== 0) {
			$('#content').css('margin-top', '125px');
			$('#eso-side-logo div.affix').css('top', '145px');
		}

		// Set initial menu height
		setMenuHeight('selected', 'li.current-leaf ul');
	}

	function activateMainSubmenu(row) {
		hoverInID = setTimeout(function() {
			$(row).addClass('hover');
			if ($('.level0 > li.hover').not(row).length) {
				// Another top level menu is still open so we disable
				// the menu animations
				$(row).addClass('hover-notransition');
				$('.level0 > li.hover').not(row).removeClass('hover');
			}

			// Set the max-height of the .level1 based on the height of
			// the children ul (only for the default page menu)
			if ($(row).hasClass('current')) {
				var level1Current = $(row).find('.level1');
				var height = level1Current.children('ul').css('height');
				level1Current.css('max-height', height);
			}
			
		}, hoverDelay);

		setMenuHeight('selected', 'li.current-leaf ul');
	}

	function deactivateMainSubmenu(row) {
		clearTimeout(hoverInID);
		setMenuHeight('selected', 'li.current-leaf ul');

		// Reset level1 max-height
		$('.level1').css('max-height', '');
	}

	function exitMainMenu(submenu) {
		// If the highlighted menu is the current one we remove the hover
		// class straight to use the default css "hover out" animation
		if ($('.level0 > li.hover.current').length)
			$('.level0 > li.hover').removeClass('hover');
		else {
			hoverOutID = setTimeout(function() {
				$('.level0 > li.hover').removeClass('hover');
			}, hoverDelay);
		}

		$('.level0 > li.hover-notransition').removeClass('hover-notransition');

		return true;
	}

	function deactivateMenu() {
		var $menu = $('.submenu-aim').data('jquery.menuAim');

		if ($menu)
		{
			$menu.reset();
			$menu.destroy();
		}

		setMenuHeight('current-hover', 'li.hover > ul');
	}

	function activateSubmenu(row) {
		var $row = $(row),
			$submenu = $row.children('.sublevel'),
			$parent_menu = $row.parents('ul.submenu-aim');
			

		$parent_menu.find('.current .sublevel').addClass('hover');
		$parent_menu.addClass('current-hover');

		$row.addClass('hover');

		setMenuHeight('current-hover', 'li.hover > ul');

		// Show the submenu
		$submenu.css({
			display: 'block'
		});

		// Update the parent level1
		$submenu.closest('.level1').css('overflow', 'visible');
	}

	function deactivateSubmenu(row) {
		var $row = $(row),
			$parent_menu = $row.closest('ul.submenu-aim');

		$parent_menu.find('.current .sublevel').removeClass('hover');
		$parent_menu.removeClass('current-hover');
		$row.removeClass('hover');

		// Hide the submenu and remove the row's highlighted look
		$row.children('.sublevel').css('display', '');
		$row.closest('.level1').css('overflow', 'hidden');

		setMenuHeight('selected', 'li.current-leaf > ul');
	}

	function exitMenu(submenu) {
		var row = $(submenu.activeRow);
		deactivateSubmenu(row);
		return true;
	}

	// Close menu if click anywhere else
	$(document).on('click', function(event){
		if (!$(event.target).closest('.mainmenu-aim').length) {
			$('.sublevel').css('display', '');
			$('li.hover').removeClass('hover');
		}
	});

	enquire.register("screen and (min-width: 1025px)", {
		match: activateMenu,
		unmatch: deactivateMenu
	}, true);
});

function setMenuHeight(selector, leafSelector) {
	var height = 0;
	var leafChildren = 0;
	var maxChildren = 0;
	var menu = $('.main-menu ul.' + selector).first();

	while (menu.length > 0) {
		var nChildren = menu.children('li').length;
		if (nChildren > maxChildren)
			maxChildren = nChildren;

		if (menu.find('ul.' + selector).first().length)
			menu = menu.find('ul.' + selector).first();
		else
			break;
	}

	// Check if we are at a currently highlighted row, or a current-leaf with
	// children
	leafChildren = menu.find(leafSelector).children('li').length;
	if (leafChildren > maxChildren)
		maxChildren = leafChildren;

	$('.main-menu ul.' + selector).css('height', 25 * maxChildren + 30);
	if ($('.level0 > li.current.hover .level1').length) {
		$('.level0 > li.current.hover .level1').css('max-height', 25 * maxChildren + 30); 
	}
}

$(document).ready(function() {
	level1 = $('li.current > .level1-wrapper > div > ul');
	liCount = level1.children('li').length;
	$('li.submenu.current > div > ul').each(function (idx, elm) {
		current = $(elm).children('li').length;
		if (current > liCount)
			liCount = current;
	});
	console.log(liCount);
	level1.css('height', liCount * 25 + 30);
	$('.level0 > li').hover(function() {
	});
});


// // Prepare PR carousel
// $(document).ready(function(){
	// $('#pr-carousel').slick({
		// infinite: true,
		// lazyLoad: 'progressive',
		// prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		// nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>',
		// autoplay: true,
		// autoplaySpeed: 10000
	// });
// });

// // Prepare Ann carousel
// $(document).ready(function(){
	// $('#ann-carousel').slick({
		// infinite: false,
		// lazyLoad: 'ondemand',
		// slidesToShow: 4,
		// slidesToScroll: 4,
		// responsive: [
			// {
				// breakpoint: 970,
				// settings: {
					// slidesToShow: 3,
					// slidesToScroll: 3
				// }
			// },
			// {
				// breakpoint: 750,
				// settings: {
					// slidesToShow: 2,
					// slidesToScroll: 2
				// }
			// },
			// {
				// breakpoint: 600,
				// settings: {
					// slidesToShow: 1,
					// slidesToScroll: 1
				// }
			// }
		// ],
		// prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		// nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>'
	// });
// });


// // Prepare POTW carousel
// $(document).ready(function(){
	// $('#potw-carousel').slick({
		// infinite: false,
		// lazyLoad: 'ondemand',
		// prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		// nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>'
	// });
// });


// // Prepare ESOCast carousel
// // $(document).ready(function(){
	// // $('#esocast-carousel').slick({
		// // infinite: false,
		// // lazyLoad: 'progressive',
		// // prevArrow: '<button type="button" class="slide-prev"><span class="fa
		// // fa-angle-left"></span</button>',
		// // nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>'
	// // });
// // });


// // Prepare Highlights carousel
// $(document).ready(function(){
	// $('#highlight-carousel').slick({
		// infinite: true,
		// lazyLoad: 'ondemand',
		// autoplay: true,
		// prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		// nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>'
	// });
// });


// // Prepare Top100 frontpage carousel
// $(document).ready(function(){
	// $('#top100-frontpage-carousel').slick({
		// infinite: false,
		// lazyLoad: 'ondemand',
		// prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		// nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>'
	// });
// });

// // Prepare Top100 dedicated carousel
// $(document).ready(function(){
	// $('#top100-carousel').slick({
		// infinite: true,
		// lazyLoad: 'ondemand',
		// prevArrow: '<button type="button" class="slide-prev"><span class="fa fa-angle-left"></span</button>',
		// nextArrow: '<button type="button" class="slide-next"><span class="fa fa-angle-right"></span></button>'
	// });
// });


// function top100Fullscreen() {
	// var elem = document.getElementById('top100-carousel-wrapper');
	// if (elem.requestFullscreen) {
		// elem.requestFullscreen();
	// } else if (elem.msRequestFullscreen) {
		// elem.msRequestFullscreen();
	// } else if (elem.mozRequestFullScreen) {
		// elem.mozRequestFullScreen();
	// } else if (elem.webkitRequestFullscreen) {
		// elem.webkitRequestFullscreen();
	// }
// }


// // Show/Hide ESO logo
// $(document).scroll(function() {
	// if ($(document).scrollTop() > 180) {
		// $('#frontpage-side-logo').css('display', 'block');
	// } else
		// $('#frontpage-side-logo').css('display', 'none');
// });


// Prepare Pop-ups (previously shadowbox):
$(document).ready(function(){
	$('.archive-image.popup').each(function() {
			$(this).magnificPopup({
			type: 'image',
			delegate: 'a.popup',
			gallery: {
				enabled: true,
				preload: [1, 1]
			},
			mainClass: 'mfp-fade'
		});
	});

	$('.archive-image.popup-ajax').each(function() {
			$(this).magnificPopup({
			type: 'ajax',
			delegate: 'a.popup',
			closeBtnInside: true,
			mainClass: 'mfp-fade'
		});
	});
});


function setupVideoPlayer(video_id) {
	jwplayer.key="EAjAk7x879BjeiN54i9pMZjIrVJMCTtZFFMcmY2yiTI=";



	// Replace '-' by '_' in video_id if any:
	video_id = video_id.replace(/-/g, '_', 'g');

	var config = window['config_' + video_id];                             

	// Check if we have a playlist defined:
	if (typeof playlist !== 'undefined') {
		config.playlist = playlist;

		if (typeof listbar !== 'undefined') {
			config.listbar = listbar;
		} else {
			config.listbar = {
				position: "right",
				size: 240
			};
		}
	}

	jwplayer('videoplayer-' + video_id).setup( config );       
}


// Configure video players
$(document).ready(function(){
	jwplayer.key="EAjAk7x879BjeiN54i9pMZjIrVJMCTtZFFMcmY2yiTI=";

	$('.video-thumbnail').each(function(){
		var parent = $(this);
		$(this).find('.fa-play').click(function() {
			var id = parent.children().first().attr('id').replace('videoplayer-', '');
			var config = window['config_' + id];
			jwplayer('videoplayer-' + id).setup( config );
			parent.addClass('playing');
			jwplayer('videoplayer-' + id).play();
		});
	});

	// Check if some videos have been embedded with embedvideos_from_id
	// if (typeof djp_videos !== 'undefined') {
		// $.each(djp_videos, function(index, video_id) {
			// console.log(video_id);
			// setupVideoPlayer(video_id);
		// });
	// }
});


// Show/hide main search box
$('#searchbox-button').click(function(){
	$('.languages-dropdown').removeClass('active');
	$('#searchbox-dropdown').toggleClass('active');
	return false;
});

// Close main search box if click anywhere else
$(document).on('click', function(event){
	if (!$(event.target).closest('#searchbox-dropdown').length) {
		$('#searchbox-dropdown').removeClass('active');
	}
});


// images comparisons
$(window).load(function() {
	$('#before_after_container').beforeAfter( {
		animateIntro : true,
	    introDelay : 1000,
	    introDuration : 500,
	    showFullLinks : false,
	    imagePath : '/public/archives/app/media/beforeafter/',
	    enableKeyboard : true
	});
});


function setWebcamTimestamp(selector, timestampPath) {
	$(selector + ':first').load(timestampPath, function(result) {
		var timestamp = $(selector + ':first').text().replace('\n', '');

		// Get the time difference in second between now and the pano timestamp:
		// We remove " CEST" from the string as javascript doesn't know how to
		// handle it and assume we're in local TZ anyway
		var timediff = (new Date - new Date(timestamp.replace(/ CES?T/, ''))) / 1000;

		// If more than 62 minutes we add a "not live" message
		var div = $(selector).parent('.webcam-timestamp').next('.webcam-live, .webcam-nolive');
		if (timediff > 3720) {
			div.text('Last image before nightfall');
			div.addClass('webcam-nolive');
			div.removeClass('webcam-live');

		} else {
			div.text('LIVE');
			div.addClass('webcam-live');
			div.removeClass('webcam-nolive');
		}

		// Set timestamp to all others .pano-timestamp
		$(selector).text(timestamp);

		// Add "webcam" to pano-timestamp within .webcam-wrapper
		$('.webcam-wrapper .pano-timestamp').text('Webcam | ' + timestamp);
	});
}


// Update Paranal panorama 'Live' in pages if any
// $(document).ready(function() {
	// if ($('.pano-timestamp').length) {
		// setWebcamTimestamp('.pano-timestamp', '/public/archives/static/pano/latest/timestamp.txt');
	// }
	// if ($('.hqcam-timestamp').length) {
		// setWebcamTimestamp('.hqcam-timestamp', '/public/archives/static/hqcam/timestamp.txt');
	// }
// });


// Load tooltips if any
$("[data-toggle='tooltip']").tooltip();


$(".image-list-300").justifiedGallery({
		rowHeight: 300,
		margins: 8,
		captions: false,
		sizeRangeSuffixes: {'lt100':'',
		'lt240':'',
		'lt320':'',
		'lt500':'',
		'lt640':'',
		'lt1024':''}
});

$(".image-list-200").justifiedGallery({
		rowHeight: 200,
		margins: 8,
		captions: false,
		sizeRangeSuffixes: {'lt100':'',
		'lt240':'',
		'lt320':'',
		'lt500':'',
		'lt640':'',
		'lt1024':''}
});

$(".image-list-150").justifiedGallery({
		rowHeight: 150,
		margins: 8,
		captions: false,
		sizeRangeSuffixes: {'lt100':'',
		'lt240':'',
		'lt320':'',
		'lt500':'',
		'lt640':'',
		'lt1024':''}
});


// Setup Masonry on archive list page
$(window).load(function() {
	if ($('.archive-list').length) {
		$('.archive-list').each(function() {
			var msnry = new Masonry(this, {
				itemSelector: '.item', 
				columnWidth: '.item',
				transitionDuration: 0
			});
		});
	}
});
