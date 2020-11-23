from ipywidgets import widgets

import hdl.config as cfg

from hdl.styles import STYLE_BUTTON, LAYOUT_DEFAULT_BUTTON


class NavigationButtons:
    def __init__(self, root):
        self.root = root
        self.navigation_buttons = self.get_navigation_buttons()


    def action_go_back(self, _element):
        """Action when the go back button is clicked"""
        self.root.main_menu.show()

    def action_refresh(self, _element):
        """Action when the refresh button is clicked"""
        if cfg.OPEN_MENU == 'upload':
            self.root.upload_menu.refresh()

        if cfg.OPEN_MENU == 'view':
            self.root.view_menu.refresh()

    def get_navigation_buttons(self):
        """Get Navigation Buttons"""
        button_go_back = widgets.Button(
            description='Back to main menu',
            style=STYLE_BUTTON,
            button_style='warning',
            layout=LAYOUT_DEFAULT_BUTTON
        )

        button_refresh = widgets.Button(
            description='Refresh page',
            style=STYLE_BUTTON,
            button_style='success',
            layout=LAYOUT_DEFAULT_BUTTON
        )

        button_go_back.on_click(self.action_go_back)
        button_refresh.on_click(self.action_refresh)

        return widgets.HBox(
            [button_refresh, button_go_back],
            layout={
                'justify_content': 'space-between'
            }
        )
