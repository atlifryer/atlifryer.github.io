(function(){
	var $carouselElem = $("#carousel-test");
	module( "Carousel", {
		setup: function(){
		},
		teardown: function(){
		}
	});

	test( "Setup with No Controls [Only 1 Page/Item]", function(){
		var $carouselSetupTest = $carouselElem.clone().attr('id', 'testSetup').appendTo('#qunit-fixture');
		$carouselSetupTest.find('ul').html('<li>1 Item</li>');
		$carouselSetupTest.carousel();

		equal($carouselSetupTest.hasClass('ui-carousel'), true, "Carousel has ui-carousel class");
		equal($carouselSetupTest.hasClass('ui-widget'), true, "Carousel has ui-widget class");
		equal($carouselSetupTest.find('.ui-carousel-content').length, 1, "Carousel Content Wrapper exists");
		equal($carouselSetupTest.find( ".ui-carousel-content > ul" ).eq( 0 ).hasClass('ui-carousel-items'), true, "Carousel UL has ui-carousel-items class");
		equal($carouselSetupTest.find( ".ui-carousel-content > ul li:first" ).hasClass('ui-carousel-item-active'), true, "Carousel first Item/Page has active class");
		equal($carouselSetupTest.find('.ui-carousel-prev').length, 0, "Carousel has no Prev Control");
		equal($carouselSetupTest.find('.ui-carousel-next').length, 0, "Carousel has no Next Control");
		equal($carouselSetupTest.find('.ui-carousel-pageoftext').length, 0, "Page of text doesn't exist");
	});

	test( "Setup with Controls [More than 1 Page/Item]", function(){
		var $carouselControlsTest = $carouselElem.clone().attr('id', 'testControls').appendTo('#qunit-fixture');
		$carouselControlsTest.carousel();

		equal($carouselControlsTest.hasClass('ui-carousel'), true, "Carousel has ui-carousel class");
		equal($carouselControlsTest.hasClass('ui-widget'), true, "Carousel has ui-widget class");
		equal($carouselControlsTest.find('.ui-carousel-content').length, 1, "Carousel Content Wrapper exists");
		equal($carouselControlsTest.find( ".ui-carousel-content > ul" ).eq( 0 ).hasClass('ui-carousel-items'), true, "Carousel UL has ui-carousel-items class");
		equal($carouselControlsTest.find( ".ui-carousel-content > ul li:first" ).hasClass('ui-carousel-item-active'), true, "Carousel first Item/Page has active class");
		equal($carouselControlsTest.find('.ui-carousel-prev').length, 1, "Carousel has Prev Control");
		equal($carouselControlsTest.find('.ui-carousel-prev').hasClass('disabled'), true, "Carousel Prev Control has disabled class");
		equal($carouselControlsTest.find('.ui-carousel-next').length, 1, "Carousel has Next Control");
		equal($carouselControlsTest.find('.ui-carousel-pageoftext').length, 1, "Page of text does exist");
	});

	test( "Destroy", function(){
		var $carouselDestroyTest = $carouselElem.clone().attr('id', 'testDestroy').appendTo('#qunit-fixture');
		$carouselDestroyTest.carousel();
		$carouselDestroyTest.carousel('destroy');

		equal($carouselDestroyTest.hasClass('ui-carousel'), false, "Carousel doesn't have ui-carousel class");
		equal($carouselDestroyTest.hasClass('ui-widget'), false, "Carousel doesn't have ui-widget class");
		equal($carouselDestroyTest.find('.ui-carousel-content').length, 0, "Carousel Content Wrapper doesn't exist");
		equal($carouselDestroyTest.find( "ul" ).eq( 0 ).hasClass('ui-carousel-items'), false, "Carousel UL doesn't have ui-carousel-items class");
		equal($carouselDestroyTest.find('.ui-carousel-item-active').length, false, "Carousel Item/Page doesn't have active class");
		equal($carouselDestroyTest.find('.ui-carousel-prev').length, 0, "Carousel has no Prev Control");
		equal($carouselDestroyTest.find('.ui-carousel-next').length, 0, "Carousel has no Next Control");
		equal($carouselDestroyTest.find('.ui-carousel-pageoftext').length, 0, "Page of text doesn't exist");
	});

	test( "Option Full Width", function(){
		var $carouselOptionFullWidthTest = $carouselElem.clone().attr('id', 'testOptionFullWidth').appendTo('#qunit-fixture');
		$carouselOptionFullWidthTest.carousel({
			fullWidth: true
		});

		equal($carouselOptionFullWidthTest.hasClass("ui-carousel-full-width"), true, "Carousel has ui-carousel-full-width class");
		equal($carouselOptionFullWidthTest.find(".ui-carousel-controls").length, 1, "Carousel controls element exists");
		equal($carouselOptionFullWidthTest.find(".ui-carousel-controls").find(".ui-carousel-prev").length, 1, "Carousel prev button is inside controls element");
		equal($carouselOptionFullWidthTest.find(".ui-carousel-controls").find(".ui-carousel-next").length, 1, "Carousel next button is inside controls element");
		equal($carouselOptionFullWidthTest.find(".ui-carousel-controls").find(".ui-carousel-pageoftext").length, 1, "Carousel page of text element is inside controls element");
	});

	test( "Option Full Width Destroy", function(){
		var $carouselOptionFullWidthDestroyTest = $carouselElem.clone().attr('id', 'testOptionFullWidthDestroy').appendTo('#qunit-fixture');
		$carouselOptionFullWidthDestroyTest.carousel({
			fullWidth: true
		});
		$carouselOptionFullWidthDestroyTest.carousel('destroy');

		equal($carouselOptionFullWidthDestroyTest.hasClass('ui-carousel'), false, "Carousel doesn't have ui-carousel class");
		equal($carouselOptionFullWidthDestroyTest.hasClass('ui-widget'), false, "Carousel doesn't have ui-widget class");
		equal($carouselOptionFullWidthDestroyTest.hasClass("ui-carousel-full-width"), false, "Carousel doesn't have ui-carousel-full-width class");
		equal($carouselOptionFullWidthDestroyTest.find('.ui-carousel-content').length, 0, "Carousel Content Wrapper doesn't exist");
		equal($carouselOptionFullWidthDestroyTest.find(".ui-carousel-controls").length, 0, "Carousel controls element doesn't exists");
		equal($carouselOptionFullWidthDestroyTest.find( "ul" ).eq( 0 ).hasClass('ui-carousel-items'), false, "Carousel UL doesn't have ui-carousel-items class");
		equal($carouselOptionFullWidthDestroyTest.find('.ui-carousel-item-active').length, false, "Carousel Item/Page doesn't have active class");
		equal($carouselOptionFullWidthDestroyTest.find('.ui-carousel-prev').length, 0, "Carousel has no Prev Control");
		equal($carouselOptionFullWidthDestroyTest.find('.ui-carousel-next').length, 0, "Carousel has no Next Control");
		equal($carouselOptionFullWidthDestroyTest.find('.ui-carousel-pageoftext').length, 0, "Page of text doesn't exist");
	});

	test( "Control Prev Disabled", function(){
		var $carouselPrevDisabledTest = $carouselElem.clone().attr('id', 'testControlPrevDisabled').appendTo('#qunit-fixture');
		$carouselPrevDisabledTest.carousel();
		$carouselPrevDisabledTest.carousel('next'); // 2nd page (1)
		$carouselPrevDisabledTest.carousel('prev'); // 1st page (0)

		equal($carouselPrevDisabledTest.find('.ui-carousel-prev').hasClass('disabled'), true, "Carousel Prev Control has disabled class");
	});

	test( "Control Prev", function(){
		var $carouselControlPrevTest = $carouselElem.clone().attr('id', 'testControlPrev').appendTo('#qunit-fixture');
		$carouselControlPrevTest.carousel();
		$carouselControlPrevTest.carousel('next'); // 2nd page (1)
		$carouselControlPrevTest.carousel('next'); // 3rd page (2)
		$carouselControlPrevTest.carousel('next'); // 4th page (3)
		$carouselControlPrevTest.carousel('prev'); // 3rd page (2)

		equal($carouselControlPrevTest.find('.ui-carousel-item-active').index(), 2, "Previous (3nd) Page is Active");
	});

	test( "Control Prev [UI Event]", function(){
		var $carouselPrevEventTest = $carouselElem.clone().attr('id', 'testControlPrevEvent').appendTo('#qunit-fixture');
		$carouselPrevEventTest.carousel();
		$carouselPrevEventTest.carousel('next'); // 2nd page (1)
		$carouselPrevEventTest.find('.ui-carousel-prev').trigger('click'); // 1st page (0)

		equal($carouselPrevEventTest.find('.ui-carousel-item-active').index(), 0, "Previous (1st) Page is Active");
	});

	test( "Control Prev Disabled [UI Event]", function(){
		var $carouselPrevEventDisabledTest = $carouselElem.clone().attr('id', 'testControlPrevEventDisabled').appendTo('#qunit-fixture');
		$carouselPrevEventDisabledTest.carousel({startPage: 2});
		$carouselPrevEventDisabledTest.find('.ui-carousel-prev').addClass('disabled');
		$carouselPrevEventDisabledTest.find('.ui-carousel-prev').trigger('click'); // 1st page (0)

		equal($carouselPrevEventDisabledTest.find('.ui-carousel-item-active').index(), 1, "(2nd) Page is Active");
	});

	test( "Control Next", function(){
		var $carouselControlNextTest = $carouselElem.clone().attr('id', 'testControlNext').appendTo('#qunit-fixture');
		$carouselControlNextTest.carousel();
		$carouselControlNextTest.carousel('next'); // 2nd page (1)

		equal($carouselControlNextTest.find('.ui-carousel-item-active').index(), 1, "Next (2nd) Page is Active");
	});

	test( "Control Next [UI Event]", function(){
		var $carouselControlNextEventTest = $carouselElem.clone().attr('id', 'testControlNextEvent').appendTo('#qunit-fixture');
		$carouselControlNextEventTest.carousel();
		$carouselControlNextEventTest.find('.ui-carousel-next').trigger('click'); // 2nd page (1)

		equal($carouselControlNextEventTest.find('.ui-carousel-item-active').index(), 1, "Next (2nd) Page is Active");
	});

	test( "Control Next Disabled [UI Event]", function(){
		var $carouselControlNextEventDisabledTest = $carouselElem.clone().attr('id', 'testControlNextEventDisabled').appendTo('#qunit-fixture');
		$carouselControlNextEventDisabledTest.carousel();
		$carouselControlNextEventDisabledTest.find('.ui-carousel-next').addClass('disabled');
		$carouselControlNextEventDisabledTest.find('.ui-carousel-next').trigger('click'); // 2nd page (1)

		equal($carouselControlNextEventDisabledTest.find('.ui-carousel-item-active').index(), 0, "(1nd) Page is Active");
	});

	test( "Control Next Disabled", function(){
		var $carouselNextDisabledTest = $carouselElem.clone().attr('id', 'testControlNextDisabled').appendTo('#qunit-fixture');
		$carouselNextDisabledTest.carousel();
		$carouselNextDisabledTest.carousel('next'); // 2nd page (1)
		$carouselNextDisabledTest.carousel('next'); // 3rd page (2)
		$carouselNextDisabledTest.carousel('next'); // 4th page (3)
		$carouselNextDisabledTest.carousel('next'); // 5th page (4)

		equal($carouselNextDisabledTest.find('.ui-carousel-next').hasClass('disabled'), true, "Carousel Next Control has disabled class");
	});

	test( "Go To Page Method", function(){
		var $carouseltestGoToPageTest = $carouselElem.clone().attr('id', 'testGoToPage').appendTo('#qunit-fixture');
		$carouseltestGoToPageTest.carousel();
		$carouseltestGoToPageTest.carousel('goToPage', 2); // 2nd page (1)

		equal($carouseltestGoToPageTest.find('.ui-carousel-item-active').index(), 1, "Next (2nd) Page is Active");
	});

	test( "Go To Page Method [Same Page]", function(){
		var $carouseltestGoToPageSameTest = $carouselElem.clone().attr('id', 'testGoToPageSame').appendTo('#qunit-fixture');
		$carouseltestGoToPageSameTest.carousel({startPage: 2});
		$carouseltestGoToPageSameTest.carousel('goToPage', 2); // 2nd page (1)

		equal($carouseltestGoToPageSameTest.find('.ui-carousel-item-active').index(), 1, "Next (2nd) Page is Active");
	});

	test( "Go To Page Method [Page below min]", function(){
		var $carouseltestGoToPageMinTest = $carouselElem.clone().attr('id', 'testGoToPageMin').appendTo('#qunit-fixture');
		$carouseltestGoToPageMinTest.carousel();
		$carouseltestGoToPageMinTest.carousel('goToPage', -10);

		equal($carouseltestGoToPageMinTest.find('.ui-carousel-item-active').index(), 0, "(1st) Page is Active");
	});

	test( "Go To Page Method [Page above max]", function(){
		var $carouseltestGoToPageMaxTest = $carouselElem.clone().attr('id', 'testGoToPageMax').appendTo('#qunit-fixture');
		$carouseltestGoToPageMaxTest.carousel();
		$carouseltestGoToPageMaxTest.carousel('goToPage', 100);

		equal($carouseltestGoToPageMaxTest.find('.ui-carousel-item-active').index(), 4, "(5th) Page is Active");
	});

	test( "After Slide Event", function(){
		var callback = sinon.spy();
		var pageIndex = null;
		var pageNum = null;
		var $carouselAfterSlideEventTest = $carouselElem.clone().attr('id', 'testAfterSlideEvent').appendTo('#qunit-fixture');
		$carouselAfterSlideEventTest.carousel({ callback: function(event, object){  pageNum = object.pageNum; pageIndex = object.pageIndex; callback(); } });
		$carouselAfterSlideEventTest.carousel('next'); // 2nd page (1)

		ok(callback.called, "Spy Called after slide event");
		equal(pageNum, 2, "Page Number returned in callback is 2");
		equal(pageIndex, 1, "Page Index returned in callback is 1");
	});

	test( "Paging Text Default", function(){
		var $carouselPageTextDefaultTest = $carouselElem.clone().attr('id', 'testPageTextDefault').appendTo('#qunit-fixture');
		$carouselPageTextDefaultTest.carousel();

		equal($carouselPageTextDefaultTest.find('.ui-carousel-pageoftext').length, 1, "Page of text exists");
		equal($carouselPageTextDefaultTest.find('.ui-carousel-pageoftext').text(), "Page 1 of 5", "Page of text is 'Page x of x'");
	});

	test( "Paging Text Option", function(){
		var $carouselPageTextOptionTest = $carouselElem.clone().attr('id', 'testPageTextOption').appendTo('#qunit-fixture');
		$carouselPageTextOptionTest.carousel({ pageText: { text: 'Weekly Ad' } });

		equal($carouselPageTextOptionTest.find('.ui-carousel-pageoftext').text(), "Weekly Ad 1 of 5", "Page of text is 'Weekly Ad x of x'");
	});

	test( "Page Text Disabled" , function(){
		var $carouselPageTextDisabledTest = $carouselElem.clone().attr('id', 'testPageTextDisabled').appendTo('#qunit-fixture');
		$carouselPageTextDisabledTest.carousel({ pageText: { enabled: false } });
		$carouselPageTextDisabledTest.carousel('goToPage', 2); // 2nd page (1)

		equal($carouselPageTextDisabledTest.find('.ui-carousel-pageoftext').length, 0, "Page of text does not exist");
	});

	test( "Default Arrow Classes", function(){
		var $carouselDefaultArrowsTest = $carouselElem.clone().attr('id', 'testDefaultArrows').appendTo('#qunit-fixture');
		$carouselDefaultArrowsTest.carousel();

		equal($carouselDefaultArrowsTest.find('.ui-carousel-prev i').hasClass('ion-chevron-left'), true, "Prev Arrow Icon Class is ion-chevron-left");
		equal($carouselDefaultArrowsTest.find('.ui-carousel-next i').hasClass('ion-chevron-right'), true, "Next Arrow Icon Class is ion-chevron-right");
	});

	test( "Optional Arrow Classes", function(){
		var $carouselOptionArrowsTest = $carouselElem.clone().attr('id', 'testOptionArrows').appendTo('#qunit-fixture');
		$carouselOptionArrowsTest.carousel({
			icons: {
				prev: "icon-arrow-left-test",
                next: "icon-arrow-right-test"
			}
		});

		equal($carouselOptionArrowsTest.find('.ui-carousel-prev i').hasClass('icon-arrow-left-test'), true, "Prev Arrow Icon Class is icon-arrow-left-test");
		equal($carouselOptionArrowsTest.find('.ui-carousel-next i').hasClass('icon-arrow-right-test'), true, "Next Arrow Icon Class is icon-arrow-right-test");
	});

	test( "Default Starting Page", function(){
		var $carouselDefaultStartPageTest = $carouselElem.clone().attr('id', 'testDefaultStartPage').appendTo('#qunit-fixture');
		$carouselDefaultStartPageTest.carousel({
			startPage: 1
		});

		equal($carouselDefaultStartPageTest.find('.ui-carousel-item-active').index(), 0, "(1st) Page is Active on initiation.");
	});

	test( "Option Starting Page", function(){
		var $carouselOptionStartPageTest = $carouselElem.clone().attr('id', 'testOptionStartPage').appendTo('#qunit-fixture');
		$carouselOptionStartPageTest.carousel({
			startPage: 3
		});

		equal($carouselOptionStartPageTest.find('.ui-carousel-item-active').index(), 2, "(3nd) Page is Active on initiation.");
	});
}());