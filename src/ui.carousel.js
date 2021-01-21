;(function( $, window, document, undefined ) {
	/**
	* @class
	* @name jQuery.ui.carousel
	* @extends jQuery.Widget
	*/
	$.widget( "ui.carousel", {

		/**
		* Options that define the behavior of the carousel.
		* @memberOf jQuery.ui.carousel.prototype
		*/
		options: {
			/**
			 * Whether or not the carousel is full-width
			 * Full-Width has arrows on bottom instead of sides
			 * and Item/Page is full width of container.
			 * @type {Boolean}
			 * @default false
			 */
			fullWidth: false,
			/**
			 * Page to start on.
			 * Not index based.
			 * @type {Number}
			 * @default 1
			 */
			startPage: 1,

			pageText: {
				/**
				 * Whether or not to show the Page x of x text.
				 * @type {boolean}
				 * @default true
				 */
				enabled: true,
				/**
				 * The text to use if pageText.enabled
				 * @type {String}
				 * @default Page
				 */
				text: "Page"
			},

			/**
			 * Which icons to use for the navigation buttons.
			 *
			 * If no icons are defined, the navigation buttons will not be rendered.
			 *
			 * @type {Object.<string, string>}
			 * @default { prev: "ion-chevron-left", next: "ion-chevron-right" }
			 */
			icons: {
				prev: "ion-chevron-left",
				next: "ion-chevron-right"
			},

			/**
			 * Callback to invoke when the page changes.
			 * @type {function(Event, Object)}
			 * @default null
			 */
			callback: null
		},

		// setup the widget
		_create: function() {
			var carouselClasses = (this.options.fullWidth) ? "ui-carousel ui-widget ui-carousel-full-width" : "ui-carousel ui-widget";
			this.element.addClass(carouselClasses);

			// the first list is the set of items to scroll through
			this.items = this.element.find( "ul" ).eq( 0 );
			this.items.addClass( "ui-carousel-items" );

			// wrap the items ul in a content div for styling and seperation
			// also utilized for placing the prev/next buttons in non full-width carousel (default)
			this.content = this.items.wrap($("<div>", {
				"class": "ui-carousel-content"
			})).parent();

			this.page = this.options.startPage - 1; // take start page and turn it into an index
			this.pageCount = this.items.children().length; // get count of total pages

			// if there's only one page, there's no need for any controls
			if ( this.pageCount > 1 ) {
				this._createNavigation(); // create the prev/next buttons
				this._refreshControls(); // update the prev/next disabled/enabled states
				this._createPageOfText(); // add the page of x text if enabled
			}

			// give the item/page UL a class
			this.items.children().addClass("ui-carousel-item");
			// give the active page/item an active class
			this.items.children().eq(this.page).addClass("ui-carousel-item-active");

			// run interaction setup
			this._super();
		},

		// create the previous and next buttons
		// bind them to the prev and next methods on click
		_createNavigation: function() {
			// create prev button
			this.prevButton = $( "<a>", {
				"href": "#",
				"class": "ui-carousel-prev"
			}).append("<i class=\"" + this.options.icons.prev + "\"></i>");
			// bind the prev button to the prev action
			this._on( this.prevButton, { click: "prev" } );

			// create next button
			this.nextButton = $( "<a>", {
				"href": "#",
				"class": "ui-carousel-next"
			}).append("<i class=\"" + this.options.icons.next + "\"></i>");
			// bind the next button to the next action
			this._on( this.nextButton, { click: "next" } );

			if (this.options.fullWidth) {
				this.controls = $("<div>", {
						"class": "ui-carousel-controls"
				}).appendTo(this.element);
				// put the prev button before the content
				this.prevButton.appendTo( this.controls );
				// put the next button after the content
				this.nextButton.appendTo( this.controls );
			} else {
				// put the prev button before the content
				this.prevButton.prependTo( this.content );
				// put the next button after the content
				this.nextButton.appendTo( this.content );
			}
		},

		// create the Page x of x text element
		_createPageOfText: function() {
			// if page text is disabled just return.
			if (!this.options.pageText.enabled) {
				return;
			}

			this.pageText = $( "<div>", {
				"href": "#",
				"class": "ui-carousel-pageoftext"
			}).append("<span></span>");

			if (this.options.fullWidth) {
				// put the page of text after the previous button
				this.prevButton.after( this.pageText );
			} else {
				//put the page of text after the content
				this.pageText.appendTo( this.element );
			}

			// setup the page of text
			this._refreshPageOfText();
		},

		// set the Page x of x text
		// to the current page and
		// set the of x to page count
		_refreshPageOfText: function() {
			// if page text is disabled just return.
			if (!this.options.pageText.enabled) {
				return;
			}

			var pageText = this.options.pageText.text + " " + (this.page + 1) + " of " + this.pageCount;

			this.pageText.find("span").text(pageText);
		},

		// Destroy the widget
		// get rid of the navigation buttons
		// remove all the classes added by the widget
		destroy: function() {
			// check to see if we have a pageText element
			// if so remove it
			if (this.pageText && this.pageText.length) {
				this.pageText.remove();
			}
			// check to see if we have a previous button
			// if so remove it
			if (this.prevButton && this.prevButton.length) {
				this.prevButton.remove();
			}
			// check to see if we have a next button
			// if so remove it
			if (this.nextButton && this.nextButton.length) {
				this.nextButton.remove();
			}
			// check to see if we have a controls element (used by full-width carousel)
			// if so remove it
			if (this.controls && this.controls.length) {
				this.controls.remove();
			}

			// get rid of the content wrapper
			this.items.unwrap();

			// remove the classes from children, items, and the carousel widget container
			this.items.children().removeClass("ui-carousel-item-active ui-carousel-item");
			this.items.removeClass( "ui-carousel-items" );
			this.element.removeClass( "ui-carousel ui-widget ui-carousel-full-width" );
		},

		/**
		 * Moves to the previous page/item.
		 * @memberof jQuery.ui.carousel.prototype
		 * @param {?Event} event The event that caused the carousel to change page/item.
		 */
		prev: function( event ) {
			// if called by a javascript event prevent the default
			if (event) {
				event.preventDefault();

				// if called by javascript event and the button is disabled
				// do nothing.
				if (this.prevButton.hasClass("disabled")) {
					return;
				}
			}

			// set the page to current page minus 1 (previous)
			// can bypass javascript event if fired directly.
			this._page( this.page - 1, event );
		},

		/**
		 * Moves to the next page/item.
		 * @memberof jQuery.ui.carousel.prototype
		 * @param {?Event} event The event that caused the carousel to change page/item.
		 */
		next: function( event ) {
			// if called by a javascript event prevent the default
			if (event) {
				event.preventDefault();

				// if called by javascript event and the button is disabled
				// do nothing.
				if (this.nextButton.hasClass("disabled")) {
					return;
				}
			}

			// set the page to current page plus 1 (next)
			// can bypass javascript event if fired directly.
			this._page( this.page + 1, event );
		},

		/**
		 * Moves to the page requested.
		 * @param  {Number} page  The page number (Not an index but actual 1 to x type number)
		 * @param  {?Event} event The event that caused the carousel to change page/item.
		 */
		goToPage: function( page, event ) {
			// goes to the requested page, since page is not index we minus 1 to get actual index
			this._page( page - 1, event );
		},

		// get the current page
		// go to the next page whether its next or prev as long as its possible (no loop support)
		// update the active child class
		// update the page x of x text
		// trigger the callback
		_page: function( page, event ) {
			var currentPage = this.page;

			// check to see if the requested page isn't below the min or above the max
			// if so go to min or max
			this.page = Math.max( 0, Math.min( this.pageCount - 1, page ) );

			// if we're moving to the same page, there's nothing to do
			if ( currentPage === this.page ) {
				return;
			}

			// remove active class from currently active item/page
			// add active class to selected page
			this.items.children().removeClass("ui-carousel-item-active").eq( this.page ).addClass("ui-carousel-item-active");

			this._refreshControls(); // enable/disable prev/next buttons
			this._refreshPageOfText(); // update the page of text

			// if defined trigger the callback event passing it pageNum and pageIndex
			if (this.options.callback) {
				this._trigger( "callback", event, { pageNum: this.page + 1, pageIndex: this.page } );
			}
		},

		// disable the prev or next button if there is no prev or next page/item.
		_refreshControls: function() {
			this.prevButton.toggleClass( "disabled", (this.page === 0) );
			this.nextButton.toggleClass( "disabled", (this.page + 1 > this.pageCount - 1 ) );
		}
	});

})( jQuery, window, document );
