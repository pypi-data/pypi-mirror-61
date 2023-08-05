// Floating AJAX: basic functions for loading content.

const floating_ajax = {
    ajaxGetRequest: function(
        preloader,
        url,
        container,
        data_type='JSON',
        main=null,
        data={},
        icon=null,
        text='',
        error_icon=null,
        error_text=null,
        template_var='template') {

        // the basic function for loading content with an ajax GET request.

        const container_object = $(container); // The container into which the content will be loaded.

        // AJAX options.
        const ajax_parameters = {
            url: url,
            type: 'GET',
            data: data,
            dataType: data_type,
        };

        // upon completion of AJAX, the preloader object executes callback functions.
        preloader.preloaderMessage(container, $.ajax(ajax_parameters), function (response, message) {
            // message - object of the message displayed on the screen (preloader object)
            // can be used to manipulate messages.

            data_type === 'JSON' ?
                container_object.empty().append(response[template_var]) :
                container_object.empty().append(response);

            // call callback functions.
            if(main) {
                main(response, container, message);
            }

        }, icon, text, error_icon, error_text);
    },

    ajaxPostRequest: function(
        preloader,
        url,
        container,
        data_type='JSON',
        main=null,
        data={},
        icon=null,
        text='',
        error_icon=null,
        error_text=null) {

        // basic function for sending POST requests via ajax.

        // AJAX options.
        const ajax_parameters = {
            url: url,
            type: 'POST',
            data: data,
            dataType: data_type,
        };

        preloader.preloaderMessage(container, $.ajax(ajax_parameters), function (response, message) {
            // message - object of the message displayed on the screen (preloader object)
            // can be used to manipulate messages.

            // call callback functions.
            if (main) {
                main(response, container, message);
            }

        }, icon, text, error_icon, error_text);
    },

    gText: function(text, exprForReplace=/_/g, replaceBy=' ') {
        // remove under underscore from text string.
        let result = null;

        if (text) {
            result = text.toString().replace(exprForReplace, replaceBy);
        }

        return result;
    }
};


let ajax_loader = undefined;
FloatingAjaxLoader = function () {
    // ajax loader service with GUI messages support.

    const self = this;

    ajax_loader = self;

    this.preloader = null;

    this.loader_button_selector = '[data-ajax-load-type]';
    this.post_button_selector = '[data-ajax-post-type]';
    this.csrf_token_selector = '[name="csrfmiddlewaretoken"]';
    this.loader_events = 'click';

    this.container_data_attr = 'ajaxContainer';
    this.url_data_attr = 'ajaxUrl';
    this.data_type_data_attr = 'ajaxDataType';
    this.post_icon_data_attr = 'ajaxPostIcon';
    this.post_error_icon_data_attr = 'ajaxPostErrorIcon';
    this.post_success_icon_data_attr = 'ajaxPostSuccessIcon';
    this.post_text_data_attr = 'ajaxPostText';
    this.post_error_text_data_attr = 'ajaxPostErrorText';
    this.loader_icon_data_attr = 'ajaxLoaderIcon';
    this.loader_error_icon_data_attr = 'ajaxLoaderErrorIcon';
    this.loader_text_data_attr = 'ajaxLoaderText';
    this.loader_error_text_data_attr = 'ajaxLoaderErrorText';
    this.load_type_data_attr = 'ajaxLoadType';
    this.post_type_data_attr = 'ajaxPostType';
    this.form_data_attr = 'ajaxForm';
    this.request_data_data_attr = 'ajaxData';
    this.reload_content_data_attr = 'ajaxReloadContent';
    this.template_variable_data_attr = 'ajaxTemplateVariable';

    this.post_icon = '/assets/img/grid.svg';
    this.post_succes_icon = '/assets/img/check-mark.svg';
    this.post_error_icon = '/assets/img/error.svg';
    this.post_text = 'Отправка...';
    this.post_error_text = 'Не удалось отправить данные.';
    this.loader_icon = '/assets/img/circle.svg';
    this.loader_error_icon = '/assets/img/error-gears.svg';
    this.loader_text = 'Загрузка...';
    this.loader_error_text = 'Ошибка на сервере, либо страница не была найдена :(';

    // callbacks

    this.mainCallback = function (response, container, message) {};
    this.prepareGETDataCallback = function (data, load_type, data_options) {return data;};
    this.runOperationsBeforeGETRequestCallback = function (container, load_type, data_options) {};
    this.preparePOSTDataCallback = function (form_obj, data, post_type, data_options) {return data;};
    this.preparePostCallback = function (form_obj, data, post_type, data_options) {};

    this.baseRequest = function (data_options, type='GET') {
        // basic method for executing queries.

        const container = $(data_options[self.container_data_attr]);
        const url = data_options[self.url_data_attr];
        const data_type = data_options[self.data_type_data_attr] || 'JSON';
        const loader_icon = data_options[self.loader_icon_data_attr] || self.loader_icon;
        const loader_error_icon = data_options[self.loader_error_icon_data_attr] || self.loader_error_icon;
        const loader_text = floating_ajax.gText(data_options[self.loader_text_data_attr]) || self.loader_text;
        const loader_error_text = floating_ajax.gText(data_options[self.loader_error_text_data_attr]) || self.loader_error_text;
        const post_icon = data_options[self.post_icon_data_attr] || self.post_icon;
        const post_error_icon = data_options[self.post_error_icon_data_attr] || self.post_error_icon;
        const post_text = floating_ajax.gText(data_options[self.post_text_data_attr]) || self.post_text;
        const post_error_text = floating_ajax.gText(data_options[self.post_error_text_data_attr]) || self.post_error_text;
        const reload_content = data_options[self.reload_content_data_attr];
        const template_variable = data_options[self.template_variable_data_attr] || 'template';

        const container_content_length = container.text().trim().length;

        if (((container_content_length !== 0 && reload_content) || container_content_length === 0) && type === 'GET') {
            let data = data_options[self.request_data_data_attr] || prepareGETData(data_options);
            // performing operations before a request.
            runOperationsBeforeGETRequest(data_options);
            // make request.
            floating_ajax.ajaxGetRequest(
                self.preloader,
                url,
                container,
                data_type,
                self.mainCallback,  // response, container, message
                data,
                loader_icon,
                loader_text,
                loader_error_icon,
                loader_error_text,
                template_variable);
        } else if (type === 'POST') {
            const data = preparePOSTData(data_options);
            const callback = getPostCallback(data, data_options);
            // make request.
            floating_ajax.ajaxPostRequest(
                self.preloader,
                url,
                container,
                data_type,
                callback,  // response, container, message
                data,
                post_icon,
                post_text,
                post_error_icon,
                post_error_text,
            );
        }
    };

    this.initSignals = function () {
        $(document).on(self.loader_events, self.loader_button_selector, function (event) {
            self.baseRequest($(this).data(), 'GET');
            event.preventDefault();
        });
        $(document).on(self.loader_events, self.post_button_selector, function (event) {
            self.baseRequest($(this).data(), 'POST');
            event.preventDefault();
        });
    };

    this.standardPOSTMessage = function(data_options, type, text, callback, timeout=300) {
        const container = $(data_options[self.container_data_attr]);
        const show_effect = 'slow';
        let icon = '';

        if (type === 'success') {
            icon = data_options[self.post_success_icon_data_attr] || self.post_succes_icon;
        } else {
            icon = data_options[self.post_error_icon_data_attr] || self.post_error_icon;
        }

        self.preloader.showTimeOutMessage(
            container,
            icon,
            text,
            timeout,
            show_effect,
            callback
        )
    };

    function prepareGETData (data_options) {
        // Function for preparing GET parameters for the function 'baseRequest()'.

        const load_type = data_options[self.load_type_data_attr];
        let data = {};

        return self.prepareGETDataCallback(data, load_type, data_options);
    }

    function runOperationsBeforeGETRequest (data_options) {
        // Function to perform additional operations when performing content downloads.

        const load_type = data_options[self.load_type_data_attr];
        const container = $(data_options[self.container_data_attr]);

        self.runOperationsBeforeGETRequestCallback(container, load_type, data_options);
    }

    function preparePOSTData (data_options) {
        // Function for preparing POST parameters for the function 'baseRequest()'.

        const form_obj = $(data_options[self.form_data_attr]);
        const post_type = data_options[self.post_type_data_attr];
        let data = {'csrfmiddlewaretoken': $(self.csrf_token_selector).val()};

        return self.preparePOSTDataCallback(form_obj, data, post_type, data_options);
    }

     function getPostCallback (data, data_options) {
        const form_obj = $(data_options[self.form_data_attr]);
        const post_type = data_options[self.post_type_data_attr];

        // callback must return a function, args: response, container, message
        return self.preparePostCallback(form_obj, data, post_type, data_options)
     }
};


let floating_full_screen_messenger = undefined;
function Messages(){
    // service for displaying messages to the user about any operations.

    this.fullScreen = function () {
        // message - fill the screen (specified block) by timer.

        const self = this;
        floating_full_screen_messenger = self;

        this.background = 'rgba(98, 117, 239, 0.4)';
        this.background_z_index = '100';
        this.background_font_color = 'white';
        this.background_style =
            'position: absolute;' +
            'display: flex;' +
            'align-items: center;' +
            'justify-content: center;' +
            'top: 0;' +
            'left: 0;' +
            'right: 0;' +
            'bottom: 0;' +
            'z-index: '+ self.background_z_index +' ;' +
            'text-align: center;' +
            'color: '+ self.background_font_color +';' +
            'background: '+ self.background + ';';

        this.preloader_img_width = '4rem';
        this.preloader_img_height = '4rem';
        this.preloader_img_style = 'width: '+ self.preloader_img_width +';height: '+ self.preloader_img_height +';';

        this.preloader_wrapper_style =
            'display: block;' +
            'padding: 0 auto;' +
            // 'position: fixed;' +
            // 'top: 50%;' +
            // 'left: 50%;' +
            // 'transform: translate(-50%, -50%);' +
            'text-align: center;';

        this.message_style = 'font-size: 4rem%;margin-top: 0.5rem;color: white;';
        this.tip_style = 'font-size: 0.7rem;color: white;';
        this.tip_indent_style = {'margin-top': '1rem'};
        this.return_button_style =
            'margin-top: 0.5rem;' +
            'padding: 0.5rem;' +
            'border-radius: 0.2rem;' +
            'border: 1px solid white;' +
            'color: white;';

        this.return_button_text = 'Вернуться';
        this.blur_style =  {'filter': 'blur(0.5rem)', '-webkit-filter': 'blur(0.5rem)'};

        this.message_container_class = 'js-full-screen-message';
        this.message_img_container_class = 'js-full-screen-message-img';
        this.message_text_container_class = 'js-full-screen-message-text';
        this.tip_message_container_class = 'js-full-screen-tip-message-text';
        this.return_button_class = 'js-return-btn';
        this.blur_container_class = 'js-blur';

        this.message = (
            $('<div/>', {
                class: self.message_container_class,
                style: self.background_style
            }).append(
                $('<div/>',{
                    class: self.message_img_container_class,
                    style: self.preloader_wrapper_style
                }).append(
                    $('<img>', {
                        style: self.preloader_img_style,
                        src: ''
                    })
                ).append(
                    $('<div/>',{
                        class: self.message_text_container_class,
                        style: self.message_style
                    })
                ).append(
                    $('<div/>',{
                        class: self.tip_message_container_class,
                        style: self.tip_style
                    })
                )
            )
        );

        this.return_button = (
            $('<button/>',{
                class: self.return_button_class,
                style: self.return_button_style,
                html: self.return_button_text
            })
        );

        this.showTimeOutMessage = function(
            container,
            icon='',
            text='',
            time_out=600,
            animation='slow',
            callback=null) {

            // Method for displaying a timeout message.

            let msg_container = $(container);

            self.message.find('.' + self.message_text_container_class).text(text);
            self.message.find('img').attr('src', icon);

            msg_container.append(self.message).fadeIn(animation);
            setBlur(msg_container);

            $.when(
                setTimeout(function() {
                    setBlur(msg_container, '');
                    self.message.remove();
                }, time_out)
            ).done(function (){
                if(callback){
                    setTimeout(function() {
                        callback(msg_container);
                    }, time_out)
                }
            })
        };

        this.preloaderMessage = function (
            container,
            main,
            done,
            icon='',
            text='',
            icon_on_fail='',
            text_on_fail='',
            animation='slow',
            timeOut=200) {

            // Method for displaying a message on completion of operations in the main callback and execution
            // of operations in the done callback.

            let msg_container = $(container);

            self.message.find('.' + self.message_text_container_class).text(text);
            self.message.find('img').attr('src', icon);

            msg_container.append(self.message).fadeIn(animation);
            setBlur(msg_container);

            setTimeout(function () {
                $.when(main).done(function (response){
                    self.message.remove();
                    done(response);
                }).fail(function (response){
                    self.addSimpleMessage(container, icon_on_fail, text_on_fail, animation)
                })
            }, timeOut);
        };

        this.addSimpleMessage = function (
            container,
            icon='',
            text='',
            animation='slow') {

            let msg_container = $(container);

            self.message.find('.' + self.message_img_container_class).append(self.return_button);
            self.message.find('.' + self.message_text_container_class).text(text);
            self.message.find('img').attr('src', icon);
            msg_container.append(self.message).fadeIn(animation);

            setBlur(msg_container);

            self.return_button.click(function () {
                setBlur(msg_container, '');
                self.message.remove();
            })
        };

        this.setTipMessage = function (text) {
            // Method for setting tooltip text to message.

            self.message.find('.' + self.tip_message_container_class).css(self.tip_indent_style).text(text);
        };

        function setBlur(parent_container, value=self.blur_style) {
            // Function to add container style blur.

            parent_container.find('.' + self.blur_container_class).css(value);
        }
    };
}