from ipywidgets import widgets
from IPython.display import display, clear_output

import hdl.config as cfg
from hdl.config import ACTION_CREATE, ACTION_UPDATE

from hdl.api import upload_datalayer
from hdl.utility import create_backup, diff_json

from hdl.styles import LAYOUT_UPLOAD_WIDGET, LAYOUT_UPLOAD_UPDATE_DIFF, STYLE_BUTTON, LAYOUT_UPLOAD_BUTTON
from hdl.styles import LAYOUT_GOBACK_BUTTON, LAYOUT_GOBACK_BOX, LAYOUT_UPLOAD_SUBMIT_BOX, LAYOUT_OUTPUT
from hdl.styles import LAYOUT_UPLOAD_UPDATE_BOX, LAYOUT_CREATE_FILES_LIST, LAYOUT_UPDATE_FILES_LIST


class UploadConfirmMenu:
    def __init__(self, datalayer_list, upload_menu):
        self.upload_menu = upload_menu
        self.datalayer_list = datalayer_list
        self.create_datalayer_list = [
            datalayer for datalayer in datalayer_list if datalayer['action_type'] == ACTION_CREATE]
        self.update_datalayer_list = [
            datalayer for datalayer in datalayer_list if datalayer['action_type'] == ACTION_UPDATE]

        self.create_widget = self.get_create_widget()
        self.update_widget = self.get_update_widget()
        self.buttons = self.get_buttons()
        self.output = widgets.Output(layout=LAYOUT_OUTPUT)

    def action_submit(self, _element):
        """Action when the upload submit button is pressed"""
        with self.output:
            for datalayer in self.datalayer_list:
                datalayer_id = datalayer['datalayer_id']
                data = datalayer['new']
                old_data = datalayer['old']
                action_type = datalayer['action_type']

                resp = upload_datalayer(datalayer_id, data)
                if resp:
                    create_backup(
                        action_type=action_type,
                        datalayer_id=datalayer_id,
                        old=old_data,
                        new=data
                    )

    def action_goback(self, _element):
        """Action when the goback buttons is pressed"""
        self.upload_menu.show()

    def get_buttons(self):
        """Create submit and goback buttons"""
        submit_button = widgets.Button(
            description='Submit',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_UPLOAD_BUTTON
        )
        submit_button.on_click(self.action_submit)
        submit_box = widgets.HBox(
            [submit_button], layout=LAYOUT_UPLOAD_SUBMIT_BOX)

        button_goback = widgets.Button(
            description='Go Back',
            style=STYLE_BUTTON,
            button_style='warning',
            layout=LAYOUT_GOBACK_BUTTON
        )
        button_goback.on_click(self.action_goback)
        goback_box = widgets.HBox([button_goback], layout=LAYOUT_GOBACK_BOX)

        return widgets.VBox([submit_box, goback_box])

    def get_create_html_list(self):
        """Create HTML list of files"""
        files = [widgets.HTML(
            f'<b>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{file["datalayer_id"]}</b>') for file in self.create_datalayer_list]

        html_list = widgets.VBox(files)

        return widgets.HBox([html_list], layout=LAYOUT_CREATE_FILES_LIST)

    def get_create_widget(self):
        """Get the list with datalayers that are to be created through the upload"""
        if len(self.create_datalayer_list) > 0:
            create_title = widgets.HTML(
                '<h4><center><b>Below datalayers will be created:</b></center></h4>')
            create_html_list = self.get_create_html_list()

            return widgets.VBox([create_title, create_html_list], layout=LAYOUT_UPLOAD_WIDGET)

        return widgets.VBox([])

    def get_update_html_list(self):
        """Create HTML List with to be updated datalayers"""
        update_html_list = []
        for datalayer in self.update_datalayer_list:
            new_data = datalayer['new']
            old_data = datalayer['old']
            datalayer_id = datalayer['datalayer_id']

            diff_title = widgets.VBox(
                [widgets.HTML(f'<b>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{datalayer_id}</b>')]
            )

            html_diff = widgets.VBox(
                [widgets.HTML(diff_json(old_data, new_data))],
                layout=LAYOUT_UPLOAD_UPDATE_DIFF
            )

            update_html_list.append(widgets.HBox(
                [diff_title, html_diff], layout=LAYOUT_UPLOAD_UPDATE_BOX))

        return widgets.VBox(update_html_list, layout=LAYOUT_UPDATE_FILES_LIST)

    def get_update_widget(self):
        """Get the list of datalayers that are updated through the upload"""
        if len(self.update_datalayer_list) > 0:
            update_title = widgets.HTML(
                value='<h4><center><b>Below datalayers will be updated:</b></center></h4>'
            )
            update_html_list = self.get_update_html_list()

            return widgets.VBox([update_title, update_html_list])

        return widgets.VBox([])

    def show(self):
        """Show upload confirm menu"""
        clear_output()

        cfg.OPEN_MENU = 'confirm_upload'

        display(self.create_widget, self.update_widget,
                self.buttons, self.output)
