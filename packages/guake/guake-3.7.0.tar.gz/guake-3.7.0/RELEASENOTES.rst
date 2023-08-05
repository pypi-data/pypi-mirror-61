=====
guake
=====

.. _guake_3.7.0:

3.7.0
=====

.. _guake_3.7.0_Release Summary:

Release Summary
---------------

.. releasenotes/notes/bugfix-6247eee74843266a.yaml @ b'82c3e9514c2e974e61368b4342af3096a8b13cbc'

Fixes the bug when "New Tab" or "Split Terminal" resets colors set by "--bgcolor" command.


.. releasenotes/notes/feature-custom_terminal_colors-f68215b30bcb61b3.yaml @ b'13516f37d1f987268369d450c707e32911901a52'

Custom colors for every terminal added. Colors are saved alongside with another tab info. "Reset custom colors" menu item added to hte tab context menu.


.. releasenotes/notes/feature_manage_colors-3c4e19b536430948.yaml @ b'6239619d2a479141d0655d280f6558405517c90e'

Resetting colors of the current page. Managing background and foreground colors of the current terminal. --reset-colors, --bgcolor-focused, --fgcolor-focused and
  --reset-colors-focused command line arguments added.


.. releasenotes/notes/feature_manage_colors-a1cb608cb342d401.yaml @ b'0f940eb287a70f255a7c417c9b2df81ff54134a7'

--bgcolor-focused, --fgcolor-focused and --reset-colors-focused command line arguments
    renamed to --bgcolor-current, --fgcolor-current and --reset-colors-current respectively.


.. releasenotes/notes/tab-names-last-dir-567eefdb3da75113.yaml @ b'bf4dd87d24d0f680dc2e7245a741933b2990a3e8'

Adds an option to display only the last directory on the current path as the tab name.


.. _guake_3.7.0_New Features:

New Features
------------

.. releasenotes/notes/add-easy-tab-selection-cc8f354553bfade4.yaml @ b'ab2d9fdeb6a2454cb330d03714dfd2e786315a21'

- Add tab selection popover in each notebook

.. releasenotes/notes/add-fullscreen-hide-tabbar-6b2529a3c134ed37.yaml @ b'ff5490e4c8486ad6426fc1838f0ba202d9f21fd7'

- Add fullscreen hide tabbar option

.. releasenotes/notes/feature_manage_colors-3c4e19b536430948.yaml @ b'6239619d2a479141d0655d280f6558405517c90e'

- List new features here followed by the ticket number, for example::
  
    - Resetting colors of the current page.
    - Setting of background and foreground colors and resetting colors of the focused terminal.

.. releasenotes/notes/feature_manage_colors-a1cb608cb342d401.yaml @ b'0f940eb287a70f255a7c417c9b2df81ff54134a7'

- Setting of background and foreground colors and resetting colors of the current terminal (not the focused one).

.. releasenotes/notes/select-split-terminal-235cc40fdc3dd598.yaml @ b'b09861e47b1270ca5c7eb9a227db206f991a7d4b'

- Add --select-terminal and --selected-terminal options to Guake CLI

.. releasenotes/notes/tab-names-last-dir-567eefdb3da75113.yaml @ b'bf4dd87d24d0f680dc2e7245a741933b2990a3e8'

- Adds an option to display only the last directory on the current path as the tab name.

.. releasenotes/notes/tab-names-last-dir-567eefdb3da75113.yaml @ b'bf4dd87d24d0f680dc2e7245a741933b2990a3e8'

- Reworked the tab name selection to use a drop-down menu.

.. releasenotes/notes/unfullscreen-through-dbus-and-cli-4ddb33c3fce47636.yaml @ b'98300df61951ca084c60dfa10449922d0c63b603'

- Unfullscreen through D-Bus interface, as well as through CLI.


.. _guake_3.7.0_Known Issues:

Known Issues
------------

.. releasenotes/notes/feature-custom_terminal_colors-f68215b30bcb61b3.yaml @ b'13516f37d1f987268369d450c707e32911901a52'

- When a user changes a background color of a terminal or a tab, this color is saved, and cannot
  be reset by changing settings. This is OK.
  The issue is that the user cannot set color transparency, and the transparency becomes fixed
  until the terminal colors are reset by the user (with a --reset* command or via the tab
  context menu.


.. _guake_3.7.0_Deprecations:

Deprecations
------------

.. releasenotes/notes/tab-names-last-dir-567eefdb3da75113.yaml @ b'bf4dd87d24d0f680dc2e7245a741933b2990a3e8'

- Translations need to be updated.


.. _guake_3.7.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-43bafb402b26f8c8.yaml @ b'2bc4913006cb5a546793eb352db71b901861b171'

- Fix Crash (TypeError) when common keys are found in config #1713

.. releasenotes/notes/bugfix-6247eee74843266a.yaml @ b'82c3e9514c2e974e61368b4342af3096a8b13cbc'

- Fixes the bug when "New Tab" or "Split Terminal" resets colors set by "--bgcolor" command.

.. releasenotes/notes/fix-1656-ae7c0158dfe70d08.yaml @ b'd36836e53ffc722a5d0ffe053a01a02916a046fc'

- Add pew package to Pipfile

.. releasenotes/notes/fix-composited-changed-didnot-update-visual-9387a8ae28d33c5d.yaml @ b'90eac30e39619021d3d8f8229628aefdf88ecf62'

- When composited changed, it will update Guake window visual to make it transparent

.. releasenotes/notes/fix-fullscreen-handle-in-wm-trigger-a1e3205ec1ec3cac.yaml @ b'5205ce2b3360d19e1a53a7996c502a33a435f794'

- Fix fullscreen/unfullscreen not handle correctly when trigger by wm

.. releasenotes/notes/fix-search-revealer-visible-settings-ddf78f6f845595a8.yaml @ b'1b60f7b5043947baaed587b1eb4a35fc08227ab9'

- Fix search revealer causing terminal unclickable at bottom right

.. releasenotes/notes/fix_scrollbar_on_new_tab-990934fbc6e44ccd.yaml @ b'1e9f5d432fae23cc187f625d1aac0dee42d341bb'

- - adding a new tab no longer shows the hidden scrollbars on other tabs

.. releasenotes/notes/remove-draw-callback-4c890ab1970512de.yaml @ b'3db732eadd55235a5a7f171241f40c3dd1b196fa'

- Remove no need window draw callback

.. releasenotes/notes/revamp-make-uninstall-79a613b66b7a08a0.yaml @ b'fce21e7d9b65ff4ed786a4b8bc99216e789dcc99'

- Fix `make uninstall` not cleaning up properly

.. releasenotes/notes/translations-20b5b8a21fd16b32.yaml @ b'91d1b10b4734c8247996238b830132cd3be263a6'

- Update some dependencies for build environment

.. releasenotes/notes/translations-20b5b8a21fd16b32.yaml @ b'91d1b10b4734c8247996238b830132cd3be263a6'

- Update the error message on missing dependencies (ex: when use 'pip install' guake)


.. _guake_3.7.0_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/translations-20b5b8a21fd16b32.yaml @ b'91d1b10b4734c8247996238b830132cd3be263a6'

- Dutch

.. releasenotes/notes/translations-20b5b8a21fd16b32.yaml @ b'91d1b10b4734c8247996238b830132cd3be263a6'

- Polish

.. releasenotes/notes/translations-20b5b8a21fd16b32.yaml @ b'91d1b10b4734c8247996238b830132cd3be263a6'

- French


.. _guake_3.7.0_Other:

Other
-----

.. releasenotes/notes/pipx-e298c749a371bb59.yaml @ b'24e10eb3e037fc178bf69fde620070a11c0137dd'

- Add a recommendation on how to install Guake from pypi. The best way is to use `pipx` installer,
  which install guake in its own virtual environment and create a launcher in `~/.local/bin`.


.. _guake_3.6.3:

3.6.3
=====

.. _guake_3.6.3_New Features:

New Features
------------

.. releasenotes/notes/add-drag-and-drop-7b977070e8427a67.yaml @ b'3031c8470e5045fdc03ecc1ef39146531e76f069'

- Add drag-n-drop to terminal (text & uris)

.. releasenotes/notes/add-scrolling-speed-9434dc74b52afb1b.yaml @ b'0e2dbcbfbc455e4145ce579700e952c1864833a4'

- When scrolling with "shift" (1 page) or "shift + ctrl" (4 pages) it will be faster (#271)


.. _guake_3.6.3_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/add-check-schema-version-restore-tabs-session-bb1d8b19e881f6dc.yaml @ b'a6bccbf4cfcca31ea8347afde2c21b822a7ad467'

- Add schema_version check for tabs session restore

.. releasenotes/notes/add-save-restore-terminal-split-b62d71cc2575f123.yaml @ b'0e6c5a97273e7a2e3d389ad90ec5e8f04b0d9a02'

- Add save/restore terminal split for tabs session - Save/Restore terminal split by pre-order traversal full binary tree in list

.. releasenotes/notes/add-save-restore-terminal-split-b62d71cc2575f123.yaml @ b'0e6c5a97273e7a2e3d389ad90ec5e8f04b0d9a02'

- Bump tabs session schema_version to 2 (to support terminal split)

.. releasenotes/notes/add-save-restore-terminal-split-b62d71cc2575f123.yaml @ b'0e6c5a97273e7a2e3d389ad90ec5e8f04b0d9a02'

- Lazy restore terminal split until Guake is visible

.. releasenotes/notes/add-save-restore-terminal-split-b62d71cc2575f123.yaml @ b'0e6c5a97273e7a2e3d389ad90ec5e8f04b0d9a02'

- Manage terminal signal handler by handler_ids

.. releasenotes/notes/bugfix-avoid-spurious-fullscreen-resize-6f3345c7a4494b1f.yaml @ b'd6cf1e57a702c83a7dd78693655fe5d92a0432f8'

- Avoid spurious resize event when showing fullscreened window

.. releasenotes/notes/disable-workspace-specific-tab-sets-on-non-X11-backend-f6b7e04a738c4271.yaml @ b'9506b66fedf3c6ff6e785ef79f3f86ad5e63242b'

- Make sure workspace-specific-tab-sets only enable on X11 backend (due to wnck)

.. releasenotes/notes/fix-dev-locale-1e63d9674936fab8.yaml @ b'e7dd9d758f216a94ee2a53ec51782943486c89ea'

- Add install/uninstall-dev-locale to support dev locale

.. releasenotes/notes/fix-dual-terminal-box-grab-focus-dead-child-bee6ce64bdc02880.yaml @ b'c76cde53152fe97951b591fe9c213995ae950b66'

- Fix DualTerminalBox grab focus when remove dead child

.. releasenotes/notes/fix-make-prefix-161844c63e1cd2b7.yaml @ b'33863bda21d09864479df81908e595af39e05636'

- Support customize prefix for make

.. releasenotes/notes/fix-rename-terminal-focus-c33af663235ed0df.yaml @ b'6edf810618808ab434126ca63c48ffd8f768f456'

- Fix re-focus on terminal after rename dialog destroy

.. releasenotes/notes/fix-split-by-menu-not-follow-cwd-ae4e6c34d8c5ddce.yaml @ b'9a3769b2a2fec5019273c5992c827a964382e75d'

- Fix split terminal by menu will not follow last terminal cwd (if option set)

.. releasenotes/notes/fix-vte-shell-kill-e50891934975b03f.yaml @ b'5ab40924dc89745115356c861f5f627bd84b7220'

- Fix delete_shell using os.waitpid (should not use it)


.. _guake_3.6.3_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/translations-c238c7afffa0f2fd.yaml @ b'6a6a6b21384493209111b7b25b351328d3ff91e3'

- German

.. releasenotes/notes/translations-c238c7afffa0f2fd.yaml @ b'6a6a6b21384493209111b7b25b351328d3ff91e3'

- French


.. _guake_3.6.2:

3.6.2
=====

.. _guake_3.6.2_New Features:

New Features
------------

.. releasenotes/notes/feature_new_tab_after-060d7990dc6f4473.yaml @ b'b7b54e87562bf56e9ad28ef545dc8b967807a38a'

- List new features here followed by the ticket number, for example::
  
    - RFE: Open new tab next to current tab #582


.. _guake_3.6.2_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/release-75c0331149c5bc63.yaml @ b'1f43921bfe1d1e4d36a69138b28620b6f13b6daa'

- Respect the XDG Base Directory Specification by supporting ``XDG_CONFIG_HOME``
  environment variable to find the ``~/.config`` directory.


.. _guake_3.6.2_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/release-75c0331149c5bc63.yaml @ b'1f43921bfe1d1e4d36a69138b28620b6f13b6daa'

- Czech (thanks @p-bo)

.. releasenotes/notes/release-75c0331149c5bc63.yaml @ b'1f43921bfe1d1e4d36a69138b28620b6f13b6daa'

- Dutch (thanks @Vistaus)

.. releasenotes/notes/release-75c0331149c5bc63.yaml @ b'1f43921bfe1d1e4d36a69138b28620b6f13b6daa'

- Norwegian Bokmål (thanks @comradekingu)

.. releasenotes/notes/release-75c0331149c5bc63.yaml @ b'1f43921bfe1d1e4d36a69138b28620b6f13b6daa'

- Polish (thanks @piotrdrag)

.. releasenotes/notes/release-75c0331149c5bc63.yaml @ b'1f43921bfe1d1e4d36a69138b28620b6f13b6daa'

- Russian (thanks @f2404)


.. _guake_3.6.2_Notes for Package Maintainers:

Notes for Package Maintainers
-----------------------------

.. releasenotes/notes/release-75c0331149c5bc63.yaml @ b'1f43921bfe1d1e4d36a69138b28620b6f13b6daa'

- The ``data`` directory is back into ``guake`` module, in order to prepare for
  the migration to importlib-resource (#1405). This should simplify a lot
  the load of resources, and avoid all the complication due to difference in
  prod/dev/traditional linux/debian customization/...


.. _guake_3.6.1:

3.6.1
=====

.. _guake_3.6.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/fix-search-box-background-1fb10348b8104cd3.yaml @ b'b374633c25f9e84f7802c798d3c9d77b4ac7d6e8'

- Fix search box background so that it will follow current theme

.. releasenotes/notes/hotfix-5b676642440c4100.yaml @ b'26304f158757effd740ba129b399f9b90b9a098d'

- Minor build system fixes


.. _guake_3.6.0:

3.6.0
=====

.. _guake_3.6.0_Release Summary:

Release Summary
---------------

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

This release brings three of the most awaited features on Guake:

   - search in current terminal
   - session saving
   - settings export and import

Our MVC ("Most Valuable Contributor") for this release is Louie Lu (@mlouielu) who worked hard to build these three features in a row! Thank you very much for your hard work !


.. _guake_3.6.0_New Features:

New Features
------------

.. releasenotes/notes/add-cli-support-option-16c5b10c88d04b06.yaml @ b'6ead8dc507f159a780e58147a674ce53eb2ad3c7'

- Add --support option to Guake CLI for user when need to report issue

.. releasenotes/notes/add-save-restore-tabs-efb4a554a7c0dc30.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Add save/restore tabs function.

.. releasenotes/notes/add-save-restore-tabs-efb4a554a7c0dc30.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Add label parameter to ``notebook.new_page_with_focus``

.. releasenotes/notes/add-search-terminal-43a0aa5950e79a74.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Add search box for terminal. Default hotkey is ``Ctrl+Shift+F``.

.. releasenotes/notes/prefs-startup-tabs-13392d3c186ce2a3.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Add session save preferences for startup/tabs:
  
    - "restore-tabs-startup": when enabled, it will restore tabs when startup
    - "restore-tabs-notify": when enabled, it will notify user after tabs restored (except startup)
    - "save-tabs-when-changed": when enabled, it will automatically save tabs session
      when changed (new/del/reorder)

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- Add CLI option to split tab: ``--split-vertical`` and ``--split-horizontal``.

.. releasenotes/notes/save-prefs-351292e24b6e6bea.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Save and restore Guake settings


.. _guake_3.6.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/add-libwnck-dep-a64492dc9d26d03e.yaml @ b'cd8fbf03d8f9d28412b3cb9065cf2a0aaaeab8d7'

- Add libwnck to bootstrap scripts

.. releasenotes/notes/fix-1499-5cd0a55ad7ffe97e.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Fix a need for double toggling to hide when using command line with ``--show`` and option with ``only_show_hide = False``.

.. releasenotes/notes/fix-1518-4b5de175dfca99f3.yaml @ b'9a0d8ca23d62f8166040ad0fbb420f9e1b5ed686'

- Remove unused logging level setup

.. releasenotes/notes/fix-save-tabs-on-window-title-change-028035febe6c6f40.yaml @ b'3b1f811104157bc4a7ecd6c0ba450c3887070e1c'

- Fix window-title-changed didn't save tabs

.. releasenotes/notes/fix-typo-dde86618d8422a65.yaml @ b'b69fa720b516913bccb04b631bcf380b9b027eed'

- fix typo

.. releasenotes/notes/fix-vte-warning-ae9a71b84c4fedf3.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Fix ``vte-warning`` when using ``Vte.Regex.new_for_match``

.. releasenotes/notes/fix-workspace-save-restore-tabs-853a7118729d8f29.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Workspaces can now properly save/restore tabs

.. releasenotes/notes/fix-workspace-save-restore-tabs-853a7118729d8f29.yaml @ b'2a626da6a4c3db662226561e929cfd7fd7539611'

- Fix ``on_terminal_title_changed`` only searching in current_notebook (it should find every notebook)


.. _guake_3.6.0_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- fr (French)

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- pl (Polish)

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- added zh_TW (Chinese Traditional). Louie Lu would be very glad to have some help on localizing Guake!

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- ru (Russian)

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- nb (Norvegian)

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- sv (Swedish)

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- nl (Dutch)


.. _guake_3.6.0_Notes for Package Maintainers:

Notes for Package Maintainers
-----------------------------

.. releasenotes/notes/release-40d6398f70cc1032.yaml @ b'a6b5e9cb93cd71c9d3b4663928df5eeee06828b4'

- Package maintainers should be aware that ``libwnck`` (Window Navigator Construction Kit)
  is now a mandatory dependency of Guake.


.. _guake_3.5.0:

3.5.0
=====

.. _guake_3.5.0_Release Summary:

Release Summary
---------------

.. releasenotes/notes/relnote-f015e2cd43e71011.yaml @ b'a85c905459755bdf49e9a864d6ce5a069672434c'

This version is mainly a maintaince release, after the big reworks on Guake from last year. I took some delay in fixing Guake due to a growing family.
Thanks again for the various contributors who submitted their patches, it helps a lot the whole community. I may be able to find more time in the upcoming months to add even cooler features to our beloved Guake.


.. _guake_3.5.0_New Features:

New Features
------------

.. releasenotes/notes/hotkey-new-tab-home-3942e1e6ba0932af.yaml @ b'89d39aa06f480a9ec113d4d7a29d6f719579b6e9'

- new hotkey (CTRL+SHIFT+H) to open new tab in home directory

.. releasenotes/notes/new-tab-button-df72cfcb9e7d422d.yaml @ b'acdb9223f7a85ac1bc6da6eb649634e64c87d647'

- "New tab" button #1471

.. releasenotes/notes/new-tab-double-click-249fdf02195bb5db.yaml @ b'b55e50773fdfc64baa1850031f45d56517b0a354'

- Open new tab by double-clicking on the tab bar

.. releasenotes/notes/notebook-menu-e562dfd6c62b38c1.yaml @ b'c3ca237bc43cc46ba5f7747e8a5e58a8f657930f'

- Add new context menu on the notebook

.. releasenotes/notes/palette-7cd39716dc53b84c.yaml @ b'cce2b8db90d438bd1683d3636e0cb8530e037c78'

- Add a CLI option to change palette scheme #1345

.. releasenotes/notes/relnote-f015e2cd43e71011.yaml @ b'a85c905459755bdf49e9a864d6ce5a069672434c'

- Bold text is also bright (>= VTE 0.52 only)

.. releasenotes/notes/split_options-7b2e2e469ebcc509.yaml @ b'51dff399c358b09f37ef76e51a134a2fa51d94c7'

- `guake --split-vertical` and `--split-horizontal` split the current
   tab just like the context menu does

.. releasenotes/notes/tab-close-buttons-1dfe8cb1049ee4dc.yaml @ b'e0dba674ee819962efc1f27a27417b94c3c67fa2'

- Optional close buttons for tabs (disabled by default)

.. releasenotes/notes/workspace_specific_tab_sets-2065f54ceca2ff26.yaml @ b'51dff399c358b09f37ef76e51a134a2fa51d94c7'

- Guake can now provide a set of tabs per workspace


.. _guake_3.5.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-1e9b3a5f5997f024.yaml @ b'51dff399c358b09f37ef76e51a134a2fa51d94c7'

- Reverse transparency slider (to be more meaningful, #1501

.. releasenotes/notes/bugfix-4e0564c5ad651093.yaml @ b'7c91cfe398b1707cac348e63b01ebd00cf2a4c01'

- Fix command-line select tab behavior #1492

.. releasenotes/notes/double_event_fix-c49129c68ead0b6b.yaml @ b'2b90489201fcf4c6f5d92a575e280ff8dd5df243'

- removed duplicate event bind? previously I had issue where quick-open event would be fired 
  twice because of this.

.. releasenotes/notes/fix-1097-b9f4f72778cfe055.yaml @ b'4a117df631a762dd9af1b81033adc208c43562b3'

- fixes

.. releasenotes/notes/fix-1451-d6ed2b40dc05bcf9.yaml @ b'7df65d8baface0553741717fcc760ec4d12f7c99'

- fixes

.. releasenotes/notes/rework-74bb086447b94d17.yaml @ b'51dff399c358b09f37ef76e51a134a2fa51d94c7'

- fix unnecessary show/hide

.. releasenotes/notes/rework-74bb086447b94d17.yaml @ b'51dff399c358b09f37ef76e51a134a2fa51d94c7'

- fix settings only applied to the active workspace if more the 1 is used

.. releasenotes/notes/rework-74bb086447b94d17.yaml @ b'51dff399c358b09f37ef76e51a134a2fa51d94c7'

- fix prompt quit dialog numbers when more then 1 workspace is used


.. _guake_3.5.0_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/relnote-f015e2cd43e71011.yaml @ b'a85c905459755bdf49e9a864d6ce5a069672434c'

- fr

.. releasenotes/notes/workspace_specific_tab_sets-2065f54ceca2ff26.yaml @ b'51dff399c358b09f37ef76e51a134a2fa51d94c7'

- de


.. _guake_3.5.0_Other:

Other
-----

.. releasenotes/notes/relnote-f015e2cd43e71011.yaml @ b'a85c905459755bdf49e9a864d6ce5a069672434c'

- For `Guake translators using weblate <https://hosted.weblate.org/projects/guake/guake/>`_,
  I had to force push because of big conflicts. Some may have loose recent translation in your
  language. Sorry for that.


.. _guake_3.4.0:

3.4.0
=====

.. _guake_3.4.0_Release Summary:

Release Summary
---------------

.. releasenotes/notes/split-terminal-b924ad9a29f59b8b.yaml @ b'82509847402ac900d1c8b48dd93f681e27e1b83f'

This major release provides one of the most awaited feature to every Guake adicts: Split terminal. Split easily vertically and horizontally each terminal and have more than one terminal per tab.
There have been several shortcut changes to help navigate easily on your screen: Ctrl+Shift+Up/Down/Left/Right to switch from terminal to terminal.
Thanks for you hard work, @aichingm !


.. _guake_3.4.0_New Features:

New Features
------------

.. releasenotes/notes/split-terminal-b924ad9a29f59b8b.yaml @ b'82509847402ac900d1c8b48dd93f681e27e1b83f'

- Split and resize terminals via mouse or keyboard shortcuts.


.. _guake_3.4.0_Deprecations:

Deprecations
------------

.. releasenotes/notes/split-terminal-b924ad9a29f59b8b.yaml @ b'82509847402ac900d1c8b48dd93f681e27e1b83f'

- "New terminal" / "Rename terminal" / "Close terminal" items has been removed from the
  terminal context menu. They are still available on the tab context menu.


.. _guake_3.4.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-afa83c6312e2f1a0.yaml @ b'7665e4eb6fd4d7fef3aee05206d9a05b12371881'

- Fix multiline selection right click (#1413)

.. releasenotes/notes/fix-1017-1dec922dcf6e914d.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- Fix tab name (#1017)

.. releasenotes/notes/fix-1149-b3ba58cf4b8db01b.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- fixes jumping preference window (#1149)

.. releasenotes/notes/fix-1421-c2cbf1c5f50da9af.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- fix no focus after closing a split terminal (#1421)

.. releasenotes/notes/fix-469-f73da051e0bd7181.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- Add note about shell that does not support --login parameter (#469)


.. _guake_3.4.0_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- pl (Piotr Drąg on weblate)

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- nl (Heimen Stoffels on weblate)

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- nb (Allan Nordhøy on weblate)

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- ru (Igor on weblate)

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- zh_CN (庄秋彬 on weblate)

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- cs (Pavel Borecki on weblate)

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- de (Robin Bauknecht on weblate)

.. releasenotes/notes/translations-bf782198a51d50f3.yaml @ b'653cd0b424d36bc26432ca0ada2800d7e6163184'

- fr (Gaetan Semet)


.. _guake_3.3.3:

3.3.3
=====

.. _guake_3.3.3_Release Summary:

Release Summary
---------------

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

This release adds a big rewrite of the Terminal underlying mechanism by Mario Aichinger. It will serve as a foundation layer for long-awaiting features such as `Split Terminal <https://github.com/Guake/guake/issues/71>`_, `Find Text <https://github.com/Guake/guake/issues/116>`_, `Save/Load Session <https://github.com/Guake/guake/issues/114>`_, and so on.


.. _guake_3.3.3_New Features:

New Features
------------

.. releasenotes/notes/add-copy-url-b39441ee986bf333.yaml @ b'6bc9e53a91fcf751ad225a4627fee822d7826696'

- add a new option in the context menu (copy url)

.. releasenotes/notes/context-menu-b45d815f7feaeecb.yaml @ b'4faf3b4bc03343f4fd8bfd4f84fc6b95f9960301'

- support for per terminal context menus

.. releasenotes/notes/context-menu-b45d815f7feaeecb.yaml @ b'4faf3b4bc03343f4fd8bfd4f84fc6b95f9960301'

- new more fullscreen handeling

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

- load default font via python Gio and not via cli call

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

- add json example for custom commands in the code

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

- port screen selectino (use_mouse) to Gdk

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

- add notification for failed show-hide key rebindings

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

- add one-click key binding editing

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

- port word character exceptions for newer vte versions

.. releasenotes/notes/gtk3-ports-676e683e82c3fa77.yaml @ b'5b7ac8c83cea027c86ca5566a8e2f16e19572998'

- use Gtk.Box instead of Gtk.HBox

.. releasenotes/notes/notebook-tabs-7986ca919d5904b3.yaml @ b'd7674bad12a141fc16b7c18f14931832c55770e1'

- use Gtk.Notebook's tabs implementation

.. releasenotes/notes/tab-scroll-switching-6c674056d1394dcd.yaml @ b'bdab3af5ef14baf22dae147d191f8187c4567922'

- enable tab switching by scrolling (mouse wheel) over the tabs/tab-bar


.. _guake_3.3.3_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/fix-1370-dca809a64dff2e3b.yaml @ b'0b1ada6a87b442eb50d6b07ca6a99b8fa80fd0d5'

- fixes Settings schema 'guake.general' does not contain a key named 'display_n'

.. releasenotes/notes/terminal-3d38462063ba8bf5.yaml @ b'7b3f22ac0a0aecdcfb5885bee9d671f5f6e42f2d'

- fixes ``guake --fgcolor/--bgcolor`` error (#1376).


.. _guake_3.3.3_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/translations-b4a5bede065fcdcc.yaml @ b'8d05cf38d27650d1156ef165e57a1abfe6322d0b'

- fr (thanks samuelorsi125t and ButterflyOfFire)

.. releasenotes/notes/translations-b4a5bede065fcdcc.yaml @ b'8d05cf38d27650d1156ef165e57a1abfe6322d0b'

- ru (thanks Igor)

.. releasenotes/notes/translations-b4a5bede065fcdcc.yaml @ b'8d05cf38d27650d1156ef165e57a1abfe6322d0b'

- pl (thanks Piotr Drąg)

.. releasenotes/notes/translations-b4a5bede065fcdcc.yaml @ b'8d05cf38d27650d1156ef165e57a1abfe6322d0b'

- cz (thanks Pavel Borecki)

.. releasenotes/notes/translations-b4a5bede065fcdcc.yaml @ b'8d05cf38d27650d1156ef165e57a1abfe6322d0b'

- de (thanks Dirk den Hoedt and Mario Aichinger)

.. releasenotes/notes/translations-b4a5bede065fcdcc.yaml @ b'8d05cf38d27650d1156ef165e57a1abfe6322d0b'

- gl (thanks Nacho Vidal)


.. _guake_3.3.3_Notes for Package Maintainers:

Notes for Package Maintainers
-----------------------------

.. releasenotes/notes/dependencies-40d6237664b473cb.yaml @ b'dbca6271141def815e503aa9782dfbd80df051cd'

- Please note ``libutempter0`` should now be considered as a mandatory dependency of Guake.
  It solves the frozen terminal issue on exit (#1014)


.. _guake_3.3.2:

3.3.2
=====

.. _guake_3.3.2_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/travis-72ba95b09d9d6e67.yaml @ b'66dc3f0a3e631d971db4486c472458af267e9099'

- Travis build cleaned build artifacts before deployment, leading to missing files when
  built in the CI.


.. _guake_3.3.1:

3.3.1
=====

.. _guake_3.3.1_Release Summary:

Release Summary
---------------

.. releasenotes/notes/translations-4106dec297b04a63.yaml @ b'45d6fad258e74f28fa294e73f18587d2b2028327'

This minor release mainly fix some issues when installing Guake though ``pip install --user --upgrade guake``.
A big thanks also to everyone who contributed to the translations on `Weblate <https://hosted.weblate.org/projects/guake/guake/>`_.

.. _guake_3.3.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-desktop-icons-d138f5862005ec4c.yaml @ b'e0047fe787f063042b40b2e14578fe9d29eb8be7'

- Don't translate application icon (this finally fixes Guake application icon not being displayed with German locale, which was only partially resolved with #1320)

.. releasenotes/notes/pip-b3c70a8c17ca5533.yaml @ b'45d6fad258e74f28fa294e73f18587d2b2028327'

- Install of Guake through pip install was broken (missing ``paths.py``). Now fixed. Discarded generation of bdist. (fix


.. _guake_3.3.1_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/translation-a33ff067822bbfb9.yaml @ b'f94bf912c86708a4cc9eb36cca13f8b3b7810f41'

- sv (thanks to @MorganAntonsson)

.. releasenotes/notes/translation-de-c6495c0ae7523117.yaml @ b'f94bf912c86708a4cc9eb36cca13f8b3b7810f41'

- de (thanks to @rzimmer)

.. releasenotes/notes/translations-4106dec297b04a63.yaml @ b'45d6fad258e74f28fa294e73f18587d2b2028327'

- fr

.. releasenotes/notes/translations-4106dec297b04a63.yaml @ b'45d6fad258e74f28fa294e73f18587d2b2028327'

- ru (thanks Igor "f2404" on Weblate)

.. releasenotes/notes/translations-4106dec297b04a63.yaml @ b'45d6fad258e74f28fa294e73f18587d2b2028327'

- cz (thanks Pavel Borecki on Weblate)

.. releasenotes/notes/translations-4106dec297b04a63.yaml @ b'45d6fad258e74f28fa294e73f18587d2b2028327'

- pl (thanks Piotr Drąg on Weblate)

.. releasenotes/notes/translations-4106dec297b04a63.yaml @ b'45d6fad258e74f28fa294e73f18587d2b2028327'

- it (thanks Maurizio De Santis on Weblate)


.. _guake_3.3.1_Other:

Other
-----

.. releasenotes/notes/credits-17a8ac0624e7a46b.yaml @ b'f94bf912c86708a4cc9eb36cca13f8b3b7810f41'

- Update about screen's credits


.. _guake_3.3.0:

3.3.0
=====

.. _guake_3.3.0_New Features:

New Features
------------

.. releasenotes/notes/pip-a8c7f5e91190b7ba.yaml @ b'86995359b2ed76d582bf7db3e37a19be4d411314'

- ``pip install guake`` now compiles the gsettings schema and finds its languages automatically.


.. _guake_3.3.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/wayland-3fcce3b30835e66d.yaml @ b'150a3a77f9355cb49e3c45a9be850b2f1ac684ec'

- Wayland is a bit more well supported. The X11 backend is now used by default for
  GDK and it seems to make the shortcut works under most situation.
  
  A more cleaner solution would be to develop a GAction
  (`vote for this feature here <https://feathub.com/Guake/guake/+29>`_])

.. releasenotes/notes/wayland-3fcce3b30835e66d.yaml @ b'150a3a77f9355cb49e3c45a9be850b2f1ac684ec'

- A new command has been added: ``guake-toggle``, should be faster than
  ``guake -t``. You can use it when you register the global shortcut manually
  (X11 or Wayland).


.. _guake_3.2.2:

3.2.2
=====

.. _guake_3.2.2_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-b26aac4094ce8154.yaml @ b'48cf239e6accf9833926f2b9697731bfaca588aa'

- Fix transparency regression on ubuntu composite (#1333)

.. releasenotes/notes/bugfix-bb8c6dcf8cbd3b20.yaml @ b'2908357bf851063dbac7e813dfa746a06e0ba469'

- Fix transparency issue

.. releasenotes/notes/bugfix-bb8c6dcf8cbd3b20.yaml @ b'2908357bf851063dbac7e813dfa746a06e0ba469'

- Fix right-click on link

.. releasenotes/notes/bugfix-bb8c6dcf8cbd3b20.yaml @ b'2908357bf851063dbac7e813dfa746a06e0ba469'

- Fix bad css override on check tab background (#1326)

.. releasenotes/notes/bugfix-desktop-icon-68a8c2d6d2ef390c.yaml @ b'a4c9f1a74fb5e333ca0a789cce3189e5535ee390'

- Fix Guake application icon not displayed with German locale

.. releasenotes/notes/bugfix-f11b203584eeeb8e.yaml @ b'99ea0ab7ab8d14abb91d914da7bbc88d70411117'

- fix ctrl+click on hyperlinks on VTE 0.50 (#1295)

.. releasenotes/notes/palette-008d16139cff7b9c.yaml @ b'34b6259b388f44dab571e729ae1e9cc54d3d3b62'

- Fixed "Gruvbox Dark" color palette (swapped foreground and background)

.. releasenotes/notes/palette-ac719dfbd2dd49e9.yaml @ b'da0a5c25e7587292131895b34ff394e74075cd07'

- Swapped foreground and background colors for palettes added in commit #58842e9.


.. _guake_3.2.2_Other:

Other
-----

.. releasenotes/notes/update-bootstrap-scripts-1ba9e40b4ab1bfd4.yaml @ b'2fa4c7b238babc6e9cd5869c47209ea6dad75014'

- Add option groupes to the bootstrap scripts


.. _guake_3.2.1:

3.2.1
=====

.. _guake_3.2.1_New Features:

New Features
------------

.. releasenotes/notes/palette-548f459256895a64.yaml @ b'de681c82ec77c7bebc9e23a76bf114641e8f5863'

- Thanks to @arcticicestudio, a new nice, clean new palette theme is available for Guake users:
  Nord (#1275)


.. _guake_3.2.1_Known Issues:

Known Issues
------------

.. releasenotes/notes/hyperlinks-778efab6774df2e6.yaml @ b'3718a0a41c4c20bf3e966c48a9b3aefbe8874f0e'

- Multiline url are sometimes not handled correctly.

.. releasenotes/notes/translations-daa7e7aa85eec3bb.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- Users of Byobu or Tmux as default shell should disable the "login shell" option
  (in the "Shell" panel). This uses an option, ``--login``, that does not exist on these
  two tools.


.. _guake_3.2.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-5b330b910cf335bb.yaml @ b'9a53c4268b2764fb0a499405824e8adf967abdaf'

- Fix duplication in theme list (#1304)

.. releasenotes/notes/bugfix-ce7825d37bcf2273.yaml @ b'56f16c9b600fb2044b8d3db1fb6fe220438a258e'

- Fix right click selection in Midnight Commander

.. releasenotes/notes/fix-hyperlink-50901cd04a88876e.yaml @ b'fa20efa6d1530162f9c97f05d0552598a5d31afc'

- Corrected usage of ``Vte.Regex.new_for_match`` to fix regular expression matching
  (hyperlinks, quick open) on VTE >0.50 (#1295)

.. releasenotes/notes/hyperlinks-778efab6774df2e6.yaml @ b'3718a0a41c4c20bf3e966c48a9b3aefbe8874f0e'

- URL with ``'`` (simple quote) and ``()`` (parenthesis) are now captured by hyperlink matcher.
  This may causes some issues with log and so that use parenthesis *around* hyperlinks,
  but since parenthesis and quotes are valid characters inside a URL, like for instance
  URL created by Kibana, they deserve the right to be shown as proper url in Guake.
  
  User can still select the URL in the terminal if he wishes to capture the exact url, before
  doing a Ctrl+click or a right click.
  
  For developers, it is advised to end the URL with a character that cannot be used in URL, such
  as space, tab, new line. Ending with a dot (``.``) or a comma (``,``) will not be seen as part
  of the URL by Guake, so most logs and traces that adds a dot or a comma at the end of the URL
  might still work.

.. releasenotes/notes/translations-daa7e7aa85eec3bb.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- Fix "Grubbox Dark" theme


.. _guake_3.2.1_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/translations-daa7e7aa85eec3bb.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- fr

.. releasenotes/notes/translations-daa7e7aa85eec3bb.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- pl

.. releasenotes/notes/translations-daa7e7aa85eec3bb.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- ru


.. _guake_3.2.1_Other:

Other
-----

.. releasenotes/notes/docs-0c95ec1b74cc65d0.yaml @ b'352a2570ff7342a4a2cf53101b6afca7f6533e9e'

- Rework the documentation. The README grew up a lot and was hard to use. It has been cut into
  several user manual pages in the official online documentation.


.. _guake_3.2.0:

3.2.0
=====

.. _guake_3.2.0_New Features:

New Features
------------

.. releasenotes/notes/theme-1c1f13e63e46d98b.yaml @ b'0779655fd34df6fb98d1bb49db1cbd46d7b44d6d'

- Allow user to select the theme within the preference UI

.. releasenotes/notes/theme-a11c5b3cf19de34f.yaml @ b'21cf658bacd2b3559ebdb36a1527d0c3631e631f'

- Selected tab use "selected highlight" color from theme (#1036)


.. _guake_3.2.0_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/theme-1c1f13e63e46d98b.yaml @ b'0779655fd34df6fb98d1bb49db1cbd46d7b44d6d'

- fr


.. _guake_3.1.1:

3.1.1
=====

.. _guake_3.1.1_New Features:

New Features
------------

.. releasenotes/notes/quick-open-52d040f5e34e4d35.yaml @ b'8491450161e24cde0548a7e8541e85fb73ae0722'

- Quick open displays a combobox with predefined settings for Visual Studio Code, Atom and
  Sublime Text.


.. _guake_3.1.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-6096693463dd6c84.yaml @ b'8491450161e24cde0548a7e8541e85fb73ae0722'

- Fix  hyperlink VTE


.. _guake_3.1.0:

3.1.0
=====

.. _guake_3.1.0_Release Summary:

Release Summary
---------------

.. releasenotes/notes/install-b017d0fe51f8e2ad.yaml @ b'97bf2cb22586bde930ea12b3ebfbc1e611967359'


This version of Guake brings mostly bug fixes, and some new features like "Quick Open on selection". I have also reworked internally the Quick Open so that it can automatically open files from logs from pytest and other python development tools output.
However, there might still some false positive on the hovering of the mouse in the terminal, the most famous being the output of ``ls -l`` which may have the mouse looks like it sees hyperlinks on the terminal everywhere. Click does nothing but its an annoying limitation.
Package maintainers should read the "Notes for Package Maintainers" of this release note carefully.


.. _guake_3.1.0_New Features:

New Features
------------

.. releasenotes/notes/autostart-300343bbe644bd7e.yaml @ b'ddc45d6d3359675b08b169585b97b51a1dc3b675'

- New "start at login" option in the settings (only for GNOME) #251

.. releasenotes/notes/debug-d435207215fdcc2e.yaml @ b'8f5a665141cc0c6951d81026a079762b0239851b'

- Add ``--verbose``/``-v`` parameter to enable debug logging. Please note the existing ``-v``
  (for version number) has been renamed ``-V``.

.. releasenotes/notes/hyperlink-e40e87ae4dc83c8e.yaml @ b'ed0278eba97a56a11b64050ef41e9c42c5ae19aa'

- Support for hyperlink VTE extension
  (`described here <https://gist.github.com/egmontkob/eb114294efbcd5adb1944c9f3cb5feda>`_ )
  #945 (Untested, as it requires VTE 0.50)

.. releasenotes/notes/palettes-ec272b2335a1fa06.yaml @ b'5065bd3f426ab77197f9c4ebd96bef11840f0a53'

- Add great color palettes from
  `Guake Color Scheme <https://github.com/ziyenano/Guake-Color-Schemes>`_, thanks for @ziyenano :
  
    - `Aci`,
    - `aco`,
    - `Azu`,
    - `Bim`,
    - `Cai`,
    - `Elementary`,
    - `Elic`,
    - `Elio`,
    - `Freya`,
    - `Gruvbox Dark`,
    - `Hemisu Dark`,
    - `Hemisu Light`,
    - `Jup`,
    - `Mar`,
    - `Material`,
    - `Miu`,
    - `Monokai dark`,
    - `Nep`,
    - `One Light`,
    - `Pali`,
    - `Peppermint`,
    - `Sat`,
    - `Shel`,
    - `Tin`,
    - `Ura`,
    - `Vag`.

.. releasenotes/notes/right-clic-f15043342128eb58.yaml @ b'0ff272c3f65ea9be7c5256962dbbf8be720f9763'

- Allow application to capture right click (ex: Midnight commander). #1096.
  It is still possible to show the contextual menu with Shift+right click.


.. _guake_3.1.0_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-78df60050b344c0b.yaml @ b'3dd342c500bda9e03400d30980481308b4e30472'

- delete tab even without libutempter (#1198)

.. releasenotes/notes/bugfix-abe62750f777873f.yaml @ b'b86c84922fe6d6485b5141b21bac9acd99884124'

- Fix crash when changing command file #1229

.. releasenotes/notes/bugfix-b54670a057197a9f.yaml @ b'347d02a69b1af3c0a3bf781d3d09ba5b7cc8a73d'

- fix ``import sys`` in ``simplegladeapp.py``

.. releasenotes/notes/bugfix_1225-6eecf165d1d0e732.yaml @ b'347d02a69b1af3c0a3bf781d3d09ba5b7cc8a73d'

- change scope of ``which_align`` variable in ``pref.py`` (#1225)

.. releasenotes/notes/quick_open-bb22f82761ad564b.yaml @ b'8274e950893f9ed119f88ca6b99ebe167571143c'

- Fix several issues on Quick Edit:
  
  - quick open freezes guake
  - support for systems with PCRE2 (regular expression in terminal) disabled for VTE, like
    Ubuntu 17.10 and +.
  
    This might disable quick open and open url on direct Ctrl+click.
    User can still select the wanted url or text and Cltr+click or use contextual menu.
  
    See this `discussion on Tilix <https://github.com/gnunn1/tilix/issues/916>`_, another
    Terminal emulator that suffurs the same issue.
  
  - quick open now appears in contextual menu (#1157)
  - bad translation update on the contextual menu. This causes new strings that was hidden to
    appear for translators.
  - Fix quick open on pattern "File:line" line that was not opening the wanted file.

.. releasenotes/notes/translation-bd1cd0a5447ee42f.yaml @ b'56f16c9b600fb2044b8d3db1fb6fe220438a258e'

- Fix user interface translations #1228

.. releasenotes/notes/translation-ccde91d14559d6ab.yaml @ b'0d6bf217c40a522c23cc83a7e06ad98273cbe32b'

- Some systems such as Ubuntu did displayed Guake with a translated interface (#1209). The locale system has been reworked to fix that.

.. releasenotes/notes/translation-ccde91d14559d6ab.yaml @ b'0d6bf217c40a522c23cc83a7e06ad98273cbe32b'

- There might be broken translations, or not up-to-date language support by Guake. A global refresh of all existing translations would be welcomed. Most has not been updated since the transition to Guake 3, so these languages support might probably be unfunctional or at least partialy localized.

.. releasenotes/notes/translation-ccde91d14559d6ab.yaml @ b'0d6bf217c40a522c23cc83a7e06ad98273cbe32b'

- A big thank you for all the volunteers and Guake enthousiats would often update their own translation to help guake being used world-wide.
  - Help is always welcomed for updating translations !

.. releasenotes/notes/vte-d6fd6406c673f71a.yaml @ b'5e6339865120775e77436e03ed90cef6bc715dc9'

- Support for vte 2.91 (0.52) #1222


.. _guake_3.1.0_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/autostart-300343bbe644bd7e.yaml @ b'ddc45d6d3359675b08b169585b97b51a1dc3b675'

- fr_FR

.. releasenotes/notes/autostart-300343bbe644bd7e.yaml @ b'ddc45d6d3359675b08b169585b97b51a1dc3b675'

- pl

.. releasenotes/notes/update-de-translation-cfcb77e0e6b4543e.yaml @ b'2fe5656610a72d3a41fbf97c3e74a160b9821052'

- de


.. _guake_3.1.0_Notes for Package Maintainers:

Notes for Package Maintainers
-----------------------------

.. releasenotes/notes/install-b017d0fe51f8e2ad.yaml @ b'97bf2cb22586bde930ea12b3ebfbc1e611967359'

- The setup mecanism has changed a little bit. Some maintainers used to patch the source code
  of Guake to change the pixmap, Gtk schema or locale paths directly in the ``guake/globals.py``
  file. This was due to a lack of flexibility of the installation target of the ``Makefile``.
  
  The ``make install`` target looks now a little bit more familiar, allowing distribution
  packager to set the various paths directly with make flags.
  
  For example:
  
  .. code-block:: bash
  
      sudo make install \
          prefix=/usr \
          DESTDIR=/path/for/packager \
          PYTHON_SITE_PACKAGE_NAME=site-package \
          localedir=/usr/share/locale
  
  The main overrides are:
  
  - ``IMAGE_DIR``: where the pixmap should be installed. Default: ``/usr/local/share/guake/pixmaps``
  - ``localedir``: where locales should be installed. Default: ``/usr/local/share/locale``
  - ``GLADE_DIR``: where the Glade files should be installed. Default: ``/usr/local/share/guake``
  - ``gsettingsschemadir``: where gsettings/dconf schema should be installed.
    Default: ``/usr/local/share/glib-2.0/schemas/``
  
  I invite package maintainers to open tickets on Github about any other difficulties
  encountered when packaging Guake.


.. _guake_3.0.5:

3.0.5
=====

.. _guake_3.0.5_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/bugfix-705c264a6b77f4d3.yaml @ b'45866977af61fdc18e2f8e4170ff6e8667ddea36'

- Apply cursor blinking to new tabs as well, not only on settings change.

.. releasenotes/notes/bugfix-c065e1a8b8e41270.yaml @ b'a17a2b5a4abcf18df96f83c1dca9f9519d75a5eb'

- Fix window losefocus hotkey #1080

.. releasenotes/notes/bugfix-cb51b18bfd3c8da3.yaml @ b'9465a191732f101891432bcdb70ce27cf6b37d8a'

- Fix refocus if open #1188

.. releasenotes/notes/fix-preference-window-header-color,-align-close-button-and-change-borders-to-margins-fa7ffffc45b12ea5.yaml @ b'2333606e7af3deb165bc8de23c392472420cf163'

- fix preferences window header color, align the close button more nicely and change borders to margins

.. releasenotes/notes/wayland-fa246d324c92fd80.yaml @ b'12a05905b2131dc091271cdf24b3c8b069da4cb0'

- Implements a timestamp for wayland (#1215)


.. _guake_3.0.4:

3.0.4
=====

.. _guake_3.0.4_New Features:

New Features
------------

.. releasenotes/notes/Add-window-displacement-options-to-move-guake-away-from-the-edges-1b2d46997e8dbe91.yaml @ b'93099961f7c90a22089b76a8a9acf1414bea56e5'

- Add window displacement options to move guake away from the screen edges

.. releasenotes/notes/Add-window-displacement-options-to-move-guake-away-from-the-edges-1b2d46997e8dbe91.yaml @ b'93099961f7c90a22089b76a8a9acf1414bea56e5'

- User can manually enter the name of the GTK theme it wants Guake to use. Note there is no
  Preference settings yet, one needs to manually enter the name using ``dconf-editor``, in the
  key ``/apps/guake/general/gtk-theme-name``. Use a name matching one the folders in
  ``/usr/share/themes``. Please also considere this is a early adopter features and has only
  been tested on Ubuntu systems.
  Dark theme preference can be se with the key ``/apps/guake/general/gtk-prefer-dark-theme``.

.. releasenotes/notes/fix-make-install-system-as-non-root-user-40cdbb0509660741.yaml @ b'7fb39459c9dd852411fcd968fcfbbf33f5bfa4ca'

- Allow make install-system to be run as non root user and print a message if so.

.. releasenotes/notes/quick_open-032209b39bb6831f.yaml @ b'4423af1c134e80a81e4c68fdcf5eea2ade969c74'

- Quick open can now open file under selection. Simply select a filename in the current terminal
  and do a Ctrl+click, if the file path can be found, it will be open in your editor. It allows
  to virtually open any file path in your terminal (if they are on your local machine), but
  requires the user to select the file path first, compared to the Quick Open feature that
  finds file names using regular expression.
  
  Also notes that is it able to look in the current folder if the selected file name exists,
  allowing Ctrl+click on relative paths as well.
  
  Line number syntax is also supported: ``filename.txt:5`` will directly on the 5th line if
  your Quick Open is set for.


.. _guake_3.0.4_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/Add-window-displacement-options-to-move-guake-away-from-the-edges-1b2d46997e8dbe91.yaml @ b'93099961f7c90a22089b76a8a9acf1414bea56e5'

- fixes issue with vertically stacked dual monitors #1162

.. releasenotes/notes/bugfix-654583b5646cf905.yaml @ b'1367a6b7cdf856efea50e0956f894be088d1f681'

- Quick Open functionnality is restored #1121

.. releasenotes/notes/bugfix-90bd70c984ad6a73.yaml @ b'69ae4fe8036eae8e2f7418cd08fccb95fe41eb07'

- Unusable Guake with "hide on focus lose" option #1152

.. releasenotes/notes/dbus-c3861541c24b328a.yaml @ b'c0443dd7df49346a87f1fa08a52c1c6f76727ad8'

- Speed up guake D-Bus communication (command line such as ``guake -t``).


.. _guake_3.0.3:

3.0.3
=====

.. _guake_3.0.3_Release Summary:

Release Summary
---------------

.. releasenotes/notes/gtk3-a429d01811754c42.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

This minor release mainly focus on fixing big problems that was remaining after the migration to GTK3. I would like to akwonledge the work of some contributors that helped testing and reporting issues on Guake 3.0.0. Thanks a lot to @egmontkob and @aichingm.


.. releasenotes/notes/prefs-032d2ab0c8e2f17a.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

The Preference window has been deeply reworked and the hotkey management has been rewriten. This was one the the major regression in Guake 3.0.


.. _guake_3.0.3_New Features:

New Features
------------

.. releasenotes/notes/auto-edit-648e3609c9aee103.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- [dev env] automatically open reno slug after creation for editing

.. releasenotes/notes/dev-env-fb2967d1ba8ee495.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- [dev env]: Add the possibility to terminate guake with ``Ctrl+c`` on terminal
  where Guake has been launched

.. releasenotes/notes/scroll-959087c80640ceaf.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Add "Infinite scrolling" option in "Scrolling" panel #274

.. releasenotes/notes/show-focus-cab5307b44905f7e.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Added hotkey for showing and focusing Guake window when it is opened or closed.
  It is convenient when Guake window are overlapped with another windows and user
  needs to just showing it without closing and opening it again. #1133


.. _guake_3.0.3_Known Issues:

Known Issues
------------

.. releasenotes/notes/packages-55d1017dd708b8de.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- Quick Edit feature is not working (#1121)


.. _guake_3.0.3_Deprecations:

Deprecations
------------

.. releasenotes/notes/visible-bell-12de7acf136d3fa4.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Remove visible bell feature #1081


.. _guake_3.0.3_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/fix-guake-showing-up-on-startup-0fdece37dc1616e4.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Command options do not work, crash when disabling keybinding #1111

.. releasenotes/notes/fix-guake-showing-up-on-startup-0fdece37dc1616e4.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Do not open Guake window upon startup #1113

.. releasenotes/notes/fix-in/decrease-height-8176a8313d9a1aba.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Fix crash on increase/decrease main window height shortcut #1099

.. releasenotes/notes/fix-rename-tab-shortcut-62ad1410c2958929.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Resolved conflicting default shortcut for ``Ctrl+F2`` (now, rename current tab is set to
  ``Ctrl+Shift+R``) #1101, #1098

.. releasenotes/notes/hotkeys-42708e8968fd7b25.yaml @ b'41c5b8b408b0360483f2e467f616f88a534acf83'

- The hotkey management has been rewriten and is now fully functional

.. releasenotes/notes/prefs-032d2ab0c8e2f17a.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Rework the Preference window and reorganize the settings. Lot of small issues
  has been fixed.
  The Preference window now fits in a 1024x768 screen.

.. releasenotes/notes/run-command-517683bd988aa06a.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Fix 'Failed to execute child process "-"' - #1119

.. releasenotes/notes/scroll-959087c80640ceaf.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- History size spin is fixed and now increment by 1000 steps. Default history value is now set to
  1000, because "1024" has no real meaning for end user. #1082


.. _guake_3.0.3_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/translation-31e67dc4190a9067.yaml @ b'7cb971cf125e41f6294b8b17003276abb18a8734'

- de

.. releasenotes/notes/translation-31e67dc4190a9067.yaml @ b'7cb971cf125e41f6294b8b17003276abb18a8734'

- fr

.. releasenotes/notes/translation-31e67dc4190a9067.yaml @ b'7cb971cf125e41f6294b8b17003276abb18a8734'

- ru


.. _guake_3.0.3_Other:

Other
-----

.. releasenotes/notes/packages-55d1017dd708b8de.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- The dependencies of the Guake executable has been slightly better described in README.
  There is an example for Debian/Ubuntu in the file ``scripts/bootstrap-dev-debian.sh`` which is
  the main environment where Guake is developed and tested.

.. releasenotes/notes/packages-55d1017dd708b8de.yaml @ b'40849130c85207d03bd077270ff09e632aa1cd58'

- Package maintainers are encouraged to submit their ``bootstrap-dev-[distribution].sh``,
  applicable for other distributions, to help users install Guake from source, and other package
  maintainers.


.. _guake_3.0.2:

3.0.2
=====

.. _guake_3.0.2_New Features:

New Features
------------

.. releasenotes/notes/dark_theme-4bb6be4b2cfd92ae.yaml @ b'b0f73e5d93f3b688cf311f5925eb0c95d8cc64e4'

- Preliminary Dark theme support. To use it, install the 'numix' theme in your system.
  For example, Ubuntu/Debian users would use ``sudo apt install numix-gtk-theme``.


.. _guake_3.0.2_Known Issues:

Known Issues
------------

.. releasenotes/notes/dark_theme-4bb6be4b2cfd92ae.yaml @ b'b0f73e5d93f3b688cf311f5925eb0c95d8cc64e4'

- Cannot enable or disable the GTK or Dark theme by a preference setting.


.. _guake_3.0.2_Deprecations:

Deprecations
------------

.. releasenotes/notes/resizer-d7c6553879852019.yaml @ b'4b50f6714f56e72b38856ec1933790c5624e3399'

- Resizer discontinued


.. _guake_3.0.2_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/make-096ad37e6079df09.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Fix ``sudo make uninstall/install`` to work only with ``/usr/local``

.. releasenotes/notes/make-096ad37e6079df09.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Fix translation ``mo`` file generation

.. releasenotes/notes/make-096ad37e6079df09.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- Fix crash on Wayland

.. releasenotes/notes/match-b205323a7aa019f9.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Fix quick open and open link in terminal

.. releasenotes/notes/not_composited_de-505082d1c18eda3c.yaml @ b'6459a2c14fd5366fae5d245aac9df21e7e7955dc'

- Fixed Guake initialization on desktop environment that does not support compositing.


.. _guake_3.0.1:

3.0.1
=====

.. _guake_3.0.1_Release Summary:

Release Summary
---------------

.. releasenotes/notes/maintenance-e02e946e15c940ab.yaml @ b'5cbf4cf065f11067118430eda32cb2fcb5516874'

Minor maintenance release.


.. _guake_3.0.1_Bug Fixes:

Bug Fixes
---------

.. releasenotes/notes/maintenance-e02e946e15c940ab.yaml @ b'5cbf4cf065f11067118430eda32cb2fcb5516874'

- Code cleaning and GNOME desktop file conformance


.. _guake_3.0.0:

3.0.0
=====

.. _guake_3.0.0_Release Summary:

Release Summary
---------------

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

Guake has been ported to GTK-3 thanks to the huge work of @aichingm. This also implies Guake now uses the latest version of the terminal emulator component, VTE 2.91.
Guake is now only working on Python 3 (version 3.5 or 3.6). Official support for Python 2 has been dropped.
This enables new features in upcoming releases, such as "find in terminal", or "split screen".


.. _guake_3.0.0_New Features:

New Features
------------

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Ported to GTK3:
  
    - cli arguments
    - D-Bus
    - context menu of the terminal, the tab bar and the tray icon
    - scrollbar of the terminal
    - ``ctrl+d`` on terminal
    - fix double click on the tab bar
    - fix double click on tab to rename
    - fix clipboard from context menu
    - notification module
    - keyboard shortcuts
    - preference screen
    - port ``gconfhandler`` to ``gsettingshandler``
    - about dialog
    - pattern matching
    - ``Guake.accel*`` methods

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Guake now use a brand new build system:
  
    - ``pipenv`` to manage dependencies in `Pipfile`
    - enforced code styling and checks using Pylint, Flake8, Yapf, ISort.
    - simpler release management thanks to PBR

.. releasenotes/notes/reno-3b5ad9829b256250.yaml @ b'8ea70114fc51ffef8436da8cde631a8246cc6794'

- [dev env] `reno <https://docs.openstack.org/reno/latest/>`_ will be used to generate
  release notes for Guake starting version 3.0.0.
  It allows developers to write the right chunk that will appear in the release
  note directly from their Pull Request.

.. releasenotes/notes/update-window-title-c6e6e3917821902d.yaml @ b'7bea32df163cde90d4aeca26a58305fc2db05bfd'

- Update Guake window title when:
  
    - the active tab changes
    - the active tab is renamed
    - the vte title changes


.. _guake_3.0.0_Known Issues:

Known Issues
------------

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Translation might be broken in some language, waiting for the translation file to be updated by volunteers

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Resizer does not work anymore

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Package maintainers have to rework their integration script completely

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- quick open and open link in terminal is broken

.. releasenotes/notes/update-window-title-c6e6e3917821902d.yaml @ b'7bea32df163cde90d4aeca26a58305fc2db05bfd'

- **Note for package maintainers**: Guake 3 has a minor limitation regarding Glib/GTK Schemas
  files. Guake looks for the gsettings schema inside its data directory. So you will probably
  need install the schema twice, once in ``/usr/local/lib/python3.5/dist-packages/guake/data/``
  and once in ``/usr/share/glib-2.0/schemas`` (see
  `#1064 <https://github.com/Guake/guake/issues/1064>`_).
  This is planned to be fixed in Guake 3.1


.. _guake_3.0.0_Upgrade Notes:

Upgrade Notes
-------------

.. releasenotes/notes/pref-af8621e5c04d973c.yaml @ b'5f6952a8385f93bfc649b434b6e4728b046f714d'

- Minor rework of the preference window.


.. _guake_3.0.0_Deprecations:

Deprecations
------------

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Background picture is no more customizable on each terminal

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- Visual Bell has been deprecated


.. _guake_3.0.0_Translation Updates:

Translation Updates
-------------------

.. releasenotes/notes/gtk3-800a345dfd067ae6.yaml @ b'dcb33c0f7048f5c96c2d13f747bbd686c65dd91d'

- fr-FR

