from ipywidgets import widgets
from IPython.display import display, clear_output

import hdl.config as cfg

from hdl.styles import STYLE_BUTTON, LAYOUT_MAIN_BUTTON_PRIMARY, LAYOUT_MAIN_BUTTON_SECONDARY, LAYOUT_BUTTON_BOX

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.title = widgets.HTML(value='<h3><b><center>Tealium HDL Model - Navigation Menu</center></b></h3>')

        self.menu_button_view = widgets.Button(
            description='View files in Tealium HDL',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_MAIN_BUTTON_PRIMARY
        )

        self.menu_button_upload = widgets.Button(
            description='Upload files to Tealium HDL',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_MAIN_BUTTON_PRIMARY
        )

        self.menu_button_readme = widgets.Button(
            description='Read more',
            style=STYLE_BUTTON,
            button_style='info',
            layout=LAYOUT_MAIN_BUTTON_SECONDARY
        )

        self.menu_button_logout = widgets.Button(
            description='Log out',
            style=STYLE_BUTTON,
            button_style='warning',
            layout=LAYOUT_MAIN_BUTTON_SECONDARY
        )

        self.dip_img = widgets.HTML(value="""
            <div id="img" style="width:auto; height:200px; border:1px dashed lightgray; text-align:center; vertical-align:center;">
                <img style="vertical-align:middle" src='https://digital-power.com/wp-content/uploads/2018/08/logo_dip_rgb.png' alt="">
            </div>
        """)

        self.primary_button_box = widgets.HBox(
            [self.menu_button_upload, self.menu_button_view],
            layout=LAYOUT_BUTTON_BOX
        )

        self.secondary_button_box = widgets.HBox(
            [self.menu_button_readme, self.menu_button_logout],
            layout=LAYOUT_BUTTON_BOX
        )

        self.menu_button_view.on_click(self.action_view)
        self.menu_button_upload.on_click(self.action_upload)
        self.menu_button_logout.on_click(self.action_logout)
        self.menu_button_readme.on_click(self.action_readmore)

    def action_view(self, _element):
        """Handler when the view button is clicked"""
        self.root.view_menu.show()

    def action_upload(self, _element):
        """Handler when the upload button is clicked"""
        self.root.upload_menu.show()

    def action_logout(self, _element):
        """logout handler. Remove existing login info"""
        clear_output()
        cfg.ACCOUNT = ''
        cfg.PROFILE = ''
        cfg.REQUEST_HEADERS['Authorization'] = ''
        print('You have logged out successfully')

    def action_readmore(self, _element):
        """Handler when the readmore button is clicked"""
        print('This feature will be implemented soon')

    def show(self):
        """Show Main menu"""
        clear_output()

        cfg.OPEN_MENU = 'main'

        display(widgets.VBox([
            self.title,
            self.dip_img,
            self.primary_button_box,
            self.secondary_button_box,
        ]))
