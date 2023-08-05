===================================================
BTC Floating Windows
===================================================

Floating windows for use as pop-ups, modal or separate sources of information
in a user graphical interface.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "floating_windows" to your INSTALLED_APPS setting like this::

      INSTALLED_APPS = (
          ...
          'floating_windows',
      )

2. Add static files css/js::

    <link type="text/css" rel="stylesheet" href="{% static 'floating_windows/css/windows.css' %}">
    <script src="{% static 'floating_windows/js/windows.js' %}"></script>

3. Create and add window(s) template(s) to the base template::

    <!-- Separate template "sign_in_modal.html" -->
    {% extends 'floating_windows/windows/default.html' %}

    {% block body_content %}
        <!-- window body -->
    {% endblock %}

    <!-- In base template -->
    {% include 'blocks/floating_windows/sign_in_modal.html' with fw_id='auth' %}

4. You can load windows content dynamically through ajax, in this case, you need to add basic window
   template that will be used by the script to copy and create new windows::

    <!-- In base template -->
    {% include 'floating_windows/windows/default.html' %}

5. Initialize windows script::

    const fw = new FloatingWindows();
    // you can disable / enable some functionality
    fw.set_windows_ids_to_url = false;  // you can disable automatic window opening
    fw.push_windows_events_to_history = false; // you can disable window opening when moving forward or backward
                                               // through browser history
    // etc. see code for thin setup
    // here you need to list the id of windows, separated by commas
    fw.initWindows('auth', 'register');

    $(document).on('floating-window:opened', function (event, window_id, options) {
        // tracking of signals about the opening of windows for loading content in them.
        // configure content load here
    });

6. Setup trigger in template. For several windows with background on same page, which can display in same time,
   you must specify `data-floating-window-z-index` attribute for background and window correct display::

    <button type="button" class="js-floating_window_open"
         data-floating-window="#w1"
         data-floating-window-title="Title"
         data-floating-window-show-footer="true"
         data-floating-window-set-background="body"          background parent container (bcg of popups is ignoring)
         data-floating-window-z-index="200"                  set this attr to set windows hierarchy
         data-floating-window-hide-on-outside-click="true"   popup
         data-floating-window-position="40px,50px">
        Trigger
    </button>

Example:

.. image:: https://user-images.githubusercontent.com/33987296/74094685-3af89000-4af6-11ea-995b-35b3b1820f4a.png
