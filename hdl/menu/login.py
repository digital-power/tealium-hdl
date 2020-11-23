from ipywidgets import widgets
from IPython.display import display, clear_output

import hdl.config as cfg

from hdl.api import auth
from hdl.styles import STYLE_TEXT_INPUT, LAYOUT_TEXT_INPUT, STYLE_BUTTON

class LoginMenu:
    def __init__(self, root, account = None, profile = None, username = None, key = None):
        self.root = root

        self.default_input = {
            'account': account,
            'profile': profile,
            'username': username,
            'key': key
        }

        self.input_fields = {}

        self.input_widget = self.get_input_widget()

    def get_loading_widget(self):
        """Loading widget when the Current HDL data is loaded after succesfull login"""
        loading_widget = widgets.HTML('<h3><center>Login Success >> Loading Current HDL Data...</center></h3>')

        return loading_widget


    def action_login(self, _element):
        """Action to login to the tealium API"""
        cfg.ACCOUNT = self.input_fields['account'].value
        cfg.PROFILE = self.input_fields['profile'].value

        username = self.input_fields['username'].value
        key = self.input_fields['key'].value

        if auth(username, key):
            clear_output()
            loading_widget = self.get_loading_widget()
            display(loading_widget)

            self.root.view_menu.load_datalayers()
            self.root.main_menu.show()

    def get_input_widget(self):
        """Get Input fields to login to the tealium API"""
        self.input_fields['account'] = widgets.Text(
            description="Tealium Account:",
            style=STYLE_TEXT_INPUT,
            layout=LAYOUT_TEXT_INPUT,
            value=self.default_input['account']
        )

        self.input_fields['profile'] = widgets.Text(
            description="Tealium Profile:",
            style=STYLE_TEXT_INPUT,
            layout=LAYOUT_TEXT_INPUT,
            value=self.default_input['profile']
        )

        self.input_fields['username'] = widgets.Text(
            description="Tealium User Email:",
            style=STYLE_TEXT_INPUT,
            layout=LAYOUT_TEXT_INPUT,
            value=self.default_input['username']
        )

        self.input_fields['key'] = widgets.Text(
            description="Tealium User API Key:",
            style=STYLE_TEXT_INPUT,
            layout=LAYOUT_TEXT_INPUT,
            value=self.default_input['key'],
            placeholder='You can find the API key in Tealium iQ - Edit/View User Settings'
        )

        input_submit = widgets.Button(
            description='Log in',
            style=STYLE_BUTTON,
            button_style='primary'
        )
        input_submit.on_click(self.action_login)

        return widgets.VBox(list(self.input_fields.values()) + [input_submit])


    def show(self):
        """Display the login Menu"""
        clear_output()

        cfg.OPEN_MENU = 'login'

        display(self.input_widget)
