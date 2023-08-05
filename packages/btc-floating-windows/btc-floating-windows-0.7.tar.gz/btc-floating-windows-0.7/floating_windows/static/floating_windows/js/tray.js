// Tray Window JS handler.

let trays = {};
Tray = function (tray_id, max_items=10) {
    const self = this;
    trays[tray_id] = self;

    const tray = $(tray_id);
    const tray_header = tray.find('.js-tray_header');
    const tray_body = tray.find('.js-tray_body');
    const tray_body_col = tray.find('.js-tray_body_col');
    const tray_footer = tray.find('.js-tray_footer');
    const tray_header_title = tray.find('.js-tray_header_title');
    const resources = tray.find('.js-tray_resources');

    this.toggleTray = function () {
        tray_body.toggleClass('hidden-tray');
    };

    this.closeTray = function () {
        tray.addClass('hidden-tray');
    };

    this.openTray = function (flush_body=false) {
        tray.removeClass('hidden-tray');
        if (flush_body) {
            tray_body_col.empty();
        }
    };

    this.updateHeaderTitle = function (title) {
        tray_header_title.html(title);
    };

    this.addOrUpdateProgressBarItem = function (item_id, title, progress_value) {
        const exist_items = $(`#${item_id}`);

        if (!exist_items.length) {
            const progress_bar_item = resources.find('.js-tray_progress_bar_item').clone();
            progress_bar_item.attr('id', item_id);
            progress_bar_item.find('.js-title').html(title);
            tray_body_col.append(progress_bar_item);
        }
        self.updateItemProgressBar(item_id, progress_value);
    };

    this.addOrUpdateMessageItem = function (item_id, title, datetime, ...messages) {
        let exist_items = $(`#${item_id}`);

        if (!exist_items.length) {
            exist_items = resources.find('.js-tray_message_item').clone();
        }
        const container = exist_items.find('.js-tray_container_for_messages');

        exist_items.find('.js-tray_item_row').remove();
        exist_items.attr('id', item_id);
        exist_items.find('.js-title').html(title);

        for (let i=0; i <= messages.length; i++) {
            const tray_item_row = resources.find('.js-tray_item_row').clone();
            tray_item_row.html(messages[i]);
            container.append(tray_item_row);
        }

        exist_items.find('.js-footer').html(datetime);
        tray_body_col.append(exist_items);

        self.controlItemsCount();
    };

    this.addProgressBarItemBarColor = function (item_id, color) {
        const bar = $(`#${item_id}`).find('.js-bar');
        bar.css({'background-color': color});
    };

    this.addInfoRow = function(item_id, info) {
        const exist_items = $(`#${item_id}`);

        if (exist_items.length) {
            const tray_item_row = resources.find('.js-tray_item_row').clone();
            tray_item_row.html(info);
            exist_items.append(tray_item_row);
        }
    };

    this.updateItemProgressBar = function (item_id, progress_value) {
        const item = tray_body_col.find(`#${item_id}`);
        const bar = item.find('.js-bar');
        if (progress_value <= 100) {
            bar.css({'width': `${progress_value}%`});
        }
    };

    this.removeItem = function (item_id) {
        tray_body_col.find(`#${item_id}`).remove();
    };

    this.controlItemsCount = function () {
        const items = tray_body_col.find('.js-tray_item');
        if (items.length > max_items) {
            items.last().remove();
        }
    };

    this.initSignals = function () {
        tray.on('click', '.js-tray_collapse_toggle', function (event) {
            self.toggleTray();
            event.preventDefault();
        });
        tray.on('click', '.js-tray_close', function (event) {
            self.closeTray();
            event.preventDefault();
        });
    };
};