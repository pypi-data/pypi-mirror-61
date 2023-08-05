// Floating Windows JS handler
// Set trigger:
// <button type="button" class="js-floating_window_open"
//         data-floating-window="#w1"
//         data-floating-window-title="Title"
//         data-floating-window-show-footer="true"
//         data-floating-window-set-background="body"          background parent container (bcg of popups is ignoring)
//         data-floating-window-z-index="200"                  set this attr to set windows hierarchy
//         data-floating-window-hide-on-outside-click="true"   popup
//         data-floating-window-position="40px,50px">
//    Trigger
// </button>
// for several windows with background on same page, which can display in same time, you must specify
// data-floating-window-z-index attribute for background and window correct display.

let floating_windows = {};  // here you can access any created window.
FloatingWindows = function () {
    const self = this;

    let sequence = new Set();
    this.start_z_index = 100;  // set custom value for correct background applying.

    this.window_data_attr = 'floating-window';
    this.hidden_class = 'hidden-floating';
    this.position_data_opt_attr = 'floatingWindowPosition';
    this.title_data_opt_attr = 'floatingWindowTitle';
    this.show_footer_data_opt_attr = 'floatingWindowShowFooter';
    this.hide_on_outside_click_data_opt_attr = 'floatingWindowHideOnOutsideClick';
    this.z_index_data_opt_attr = 'floatingWindowZIndex';
    this.window_trigger_events = 'click';
    this.open_window_class = 'open';
    this.window_opened_event = 'floating-window:opened';
    this.window_closed_event = 'floating-window:closed';
    this.prevent_events_for_trigger = false;
    this.set_background_to_data_opt_attr = 'floatingWindowSetBackground';

    this.attach_windows_to = 'body';
    this.window_html_source_class = 'js-floating_window_source';
    this.window_close_button_selector = '.js-floating_window_close';
    this.window_trigger_selector = '.js-floating_window_open';
    this.windows_footer_selector = '.js-window_footer';
    this.window_header_selector = '.js-window_header';
    this.windows_body_selector = '.js-window_body';
    this.windows_header_title_selector = '.js-window_header_title';
    this.outside_click_bind_class = 'js-close_on_outside_click';
    this.background_source_selector = '.js-floating_background_source';

    this.window_get_param = 'fw';
    this.set_ids_to_url_data_attr = 'floatingWindowSetToUrl';
    this.push_events_to_history_data_attr = 'floatingWindowPushToHistory';

    this.initWindows = function (...windows_ids) {
        // main initialization method
        self.createWindows(...windows_ids);
        self.initSignals();
    };

    this.createWindows = function (...windows_ids) {
        // clone window object and add it as new to page with specified id.

        $.each(windows_ids, function (index, window_id) {
            let new_window = $('#' + window_id);

            floating_windows[window_id] = self;

            // if window is not on the page - clone and prepare default window reference from page.
            // if window is on the page (custom window) - only bind events for it.
            if (!new_window.length) {
                new_window = $('.' + self.window_html_source_class).clone();
                new_window.attr('id', window_id);
                self.addObjectToPage(new_window);
                self.setWindowDataAttr(new_window);
            }
            new_window.removeClass(self.window_html_source_class);
            self.bindEvents(window_id);
        });
    };

    this.setWindowPosition = function (window_id, options) {
        // setup window position - data-floating-window-position attr on trigger.
        // top,left,bottom,right
        const window = $('#' + window_id);
        let position = options[self.position_data_opt_attr];

        if (position) {
            position = position.split(',');
            if (position.length >= 1) {
                window.css({'top': position[0]})
            }
            if (position.length >= 2) {
                window.css({'left': position[1]})
            }
            if (position.length >= 3) {
                window.css({'bottom': position[2]})
            }
            if (position.length === 4) {
                window.css({'right': position[3]})
            }
        }
    };

    this.bindOutsideClick = function (window_id, options) {
        // bind this event on window open.
        const window = $('#' + window_id);

        // set class for handling outside click event for popup windows.
        if (options[self.hide_on_outside_click_data_opt_attr]){
            window.addClass(self.outside_click_bind_class);
        } else {
            window.removeClass(self.outside_click_bind_class);
        }
    };

    this.bindEvents = function (window_id) {
        const window = $('#' + window_id);

        // check for click on free space for hiding popup windows.
        $(self.attach_windows_to).click(function(event){
            if (window.hasClass(self.outside_click_bind_class) && window.has(event.target).length === 0) {
                self.closeWindow(window_id, {});
            }
        });

        // other.
    };

    this.addObjectToPage = function (object_to_add) {
        $(self.attach_windows_to).append(object_to_add);
    };

    this.setWindowDataAttr = function (window) {
        const window_id = window.attr('id');
        window.find('[' + 'data-' + self.window_data_attr + '=""]').attr('data-' + self.window_data_attr, window_id);
    };

    this.addWindowToUrl = function (window_id, options) {
        /*
        Method for adding related parameters to the address bar when opening a window.
        */

        if (options[self.set_ids_to_url_data_attr]) {
            const new_url = updateUrl(window.location.href, self.window_get_param + '=' + window_id);
            window.history.replaceState(window.location.href, '', new_url);
            if (options[self.push_events_to_history_data_attr]) {
                window.history.pushState(null, '', new_url);
            }
        }
    };

    this.removeWindowFromUrl = function (window_id) {
        /*
        Method for removing related parameters from the address bar when closing a window.
        */
        const url = new URL(window.location.href);
        const windows_id_from_url = url.searchParams.getAll(self.window_get_param);

        if (windows_id_from_url.includes(window_id.toString())) {
            const new_url = updateUrl(window.location.href, self.window_get_param + '=' + window_id, null);
            window.history.replaceState(window.location.href, '', new_url);
        }
    };

    this.openWindow = function (window_id, options={}) {
        const window = $('#' + window_id);
        const window_footer = window.find(self.windows_footer_selector);
        const window_header_title = window.find(self.windows_header_title_selector);
        const show_footer = options[self.show_footer_data_opt_attr];
        const title = options[self.title_data_opt_attr] || '';

        if (!window.hasClass(self.open_window_class)) {
            self.bindOutsideClick(window_id, options);
            show_footer ?
                window_footer.removeClass(self.hidden_class) :
                window_footer.addClass(self.hidden_class);
            window_header_title.html(prepareText(title));
            window.addClass(self.open_window_class);
            window.removeClass(self.hidden_class);
            window.css({'z-index': options[self.z_index_data_opt_attr] || self.start_z_index});

            // add window_id to array determine the sequence of open events.
            addToSequence(window_id, options);
            self.setWindowPosition(window_id, options);
            // add window to url as get-parameter
            self.addWindowToUrl(window_id, options);
            // trigger event on window open.
            $(document).trigger(self.window_opened_event, [window_id, options]);
        }
    };

    this.closeWindow = function (window_id, options) {
        const window = $('#' + window_id);

        if (window.hasClass(self.open_window_class)) {
            window.removeClass(self.open_window_class);
            window.addClass(self.hidden_class);

            // remove window_id from sequence.
            removeFromSequence(window_id, options);
            // remove window from url as get-parameter
            self.removeWindowFromUrl(window_id);
            // trigger event on window close.
            $(document).trigger(self.window_closed_event, [window_id, options]);
        }
    };

    this.toggleWindow = function (window_id, options={}) {
        const window = $('#' + window_id);

        window.hasClass(self.open_window_class) ?
            self.closeWindow(window_id, options) :
            self.openWindow(window_id, options);
    };

    this.initSignals = function () {
        /*
        The main method for initializing window's interaction signals.
        */

        self.openWindowsByUrlParams();
        $(document).on(self.window_trigger_events, self.window_trigger_selector, function (event) {
            const window_id = $(this).data(self.window_data_attr);
            const options = $(this).data();

            self.toggleWindow(window_id, options);

            // prevent other scripts execution if needed.
            if (self.prevent_events_for_trigger)
                event.stopPropagation();

            event.preventDefault();
        });
        $(document).on(self.window_trigger_events, self.window_close_button_selector, function (event) {
            const window_id = $(this).data(self.window_data_attr);
            const options = $(this).data();

            self.closeWindow(window_id, options);
            event.preventDefault();
        });
    };

    this.hideBackground = function () {
        const background = getBackground();
        background.addClass(self.hidden_class);
    };

    this.showBackground = function (options) {
        /*
        Method to control the display of background dimming.
        */

        const background = getBackground();
        // clone exist background and add to container specified in trigger by data-floating-window-set-background
        // attribute, then delete cloned background object.
        const new_background = background.clone();
        const container = $(options[self.set_background_to_data_opt_attr] || self.attach_windows_to);

        // set background to specified container.
        container.append(new_background);
        new_background.removeClass(self.hidden_class);
        background.remove();
    };

    this.setBackgroundZIndexForWindow = function (window_id) {
        /*
        Method to set the correct index of dimming on the screen according to the position of the windows.
        */

        const background = $(self.background_source_selector);
        const window = $('#' + window_id);
        const window_z_index = window.css('z-index') || self.start_z_index;

        // check window z-index and set background index as window z-index - 1 .
        background.css({'z-index': window_z_index - 1});
    };

    this.openWindowsByUrlParams = function () {
        /*
        Method for opening windows according to the parameters in the address bar.
        */

        const url = new URL(window.location.href);
        const windows_id_from_url = url.searchParams.getAll(self.window_get_param);

        // open windows in the sequence specified in url.
        for (let index in windows_id_from_url) {
            const window_id = windows_id_from_url[index];
            const options_source =
                $(self.window_trigger_selector + '[data-' + self.window_data_attr + '="' + window_id + '"]');

            if (options_source.length) {
                self.openWindow(window_id, options_source.data());
            }
        }
    };

    function addToSequence(window_id, options) {
        /*
        Function for tracking open windows and controlling background dimming in case of multiple
        overlapping windows.
        */

        const window = $('#' + window_id);

        // adding to array for determine the sequence of window (with background) open events.
        // check window has not outside click property - we must ignore popup windows.
        if (options[self.set_background_to_data_opt_attr] && !window.hasClass(self.outside_click_bind_class)) {
            sequence.add(window_id.toString());
            self.setBackgroundZIndexForWindow(window_id);
            self.showBackground(options);
        }
    }

    function removeFromSequence(window_id, options) {
        /*
        Function for tracking open windows and controlling background dimming in case of multiple
        overlapping windows.
        */

        sequence.delete(window_id.toString());

        if (sequence.size !== 0) {
            // set background z-index for last window after deletion of the current window.
            const previous_window_id = Array.from(sequence).pop();

            self.setBackgroundZIndexForWindow(previous_window_id);
            self.showBackground(options);
        } else {
            // hide background if sequence is empty.
            self.hideBackground();
        }
    }

    function getBackground() {
        return $(self.background_source_selector);
    }

    function updateUrl(url, param, update_value){
        /*
        Function for setting parameters in the address bar for tracking opened windows.
        */

        // check # position.
        let hash_index = url.indexOf("#") | 0;
        if (hash_index === -1)
            hash_index = url.length | 0;

        // get url string parts and save # - parameters substring.
        let urls = url.substring(0, hash_index).split('?');
        let base_url = urls[0];
        let parameters = '';
        let new_parameters = [];

        // get all GET - parameters after ?.
        if (urls.length > 1)
            parameters = urls[1];

        // get valid URI.
        if (update_value)
            update_value = encodeURI(update_value);

        // parse exist parameters and search for parameters to update or delete.
        if (parameters) {
            parameters = parameters.split('&');
            for (let k in parameters) {
                const key_val = parameters[k];
                let new_param = key_val;

                // update exist parameter by new value.
                if (update_value && key_val === param) {
                    const ekey = key_val.split('=')[0];
                    new_param = ekey + '=' + update_value;
                }
                // skip parameters with null value and save other parameters.
                if (!(update_value || key_val === param)) {
                    new_parameters.push(new_param)
                }
            }
        }

        // if there was no such parameter before - add it to url.
        if (new_parameters.indexOf(param) < 0 && update_value === undefined) {
            new_parameters.push(param);
        }
        // final assembly.
        let final_url = base_url;
        if (new_parameters.length > 0) {
            final_url += '?' + new_parameters.join('&');
        }

        return final_url + url.substring(hash_index);
    }

    function prepareText(text, exprForReplace=/_/g, replaceBy=' ') {
        /*
        Function for removing underscore or any other substring from string.
        */

        let result = null;
        if (text) {
            result = text.toString().replace(exprForReplace, replaceBy);
        }
        return result;
    }
};
