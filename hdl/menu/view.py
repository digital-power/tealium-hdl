import os
import json

from ipywidgets import widgets, HBox
from IPython.display import display, clear_output

import hdl.config as cfg

from hdl.api import list_datalayers, get_datalayer
from hdl.utility import dict_to_df, merge_dfs, create_folder, generate_folder_name
from hdl.menu import DeleteMenu, NavigationButtons

from hdl.styles import LAYOUT_ACTION_BUTTON_OTHER, LAYOUT_CHECKBOX, LAYOUT_SEARCH, LAYOUT_CHECKBOX_BOX_VIEW
from hdl.styles import LAYOUT_SELECTALL_BUTTON, LAYOUT_OUTPUT, LAYOUT_ACTION_BUTTON_TOP, LAYOUT_VIEW_PRELOAD_BOX
from hdl.styles import LAYOUT_VIEW_PRELOAD_LABEL, LAYOUT_CHECKBOX_LABEL, STYLE_BUTTON, LAYOUT_CHECKBOX_WRAPPER


class ViewMenu:
    def __init__(self, root):
        self.filenames = []
        self.selected_filenames = []

        self.checkbox_dict = {}
        self.label_dict = {}

        self.checkbox_boxes = None
        self.checkbox_labels = None

        self.title = widgets.HTML(
            value='<h4><b><center>Here you can find the uploaded datalayers in Tealium HDL.</center></b></h4>')

        self.file_widget = self.get_file_widget()

        self.output = widgets.Output(layout=LAYOUT_OUTPUT)
        self.navigation_buttons = NavigationButtons(root=root).navigation_buttons


    def checkbox_change_listener(self, _change):
        """Change listener for checkboxes. Builds a new selected_filenames array each time
        a checkbox is checked. This is horrendous of course"""
        self.selected_filenames.clear()
        self.output.clear_output()

        for filename in self.checkbox_dict:
            if self.checkbox_dict[filename].value is True:
                self.selected_filenames.append(filename)


    def load_datalayers(self):
        """Load exisiting datalayers into widget"""
        self.filenames = list_datalayers()

        for filename in self.filenames:
            self.checkbox_dict[filename] = widgets.Checkbox(
                vaue=False,
                indent=False,
                layout=LAYOUT_CHECKBOX
            )
            self.checkbox_dict[filename].observe(self.checkbox_change_listener, names='value')

            self.label_dict[filename] = widgets.Label(
                f'{filename}',
                layout=LAYOUT_CHECKBOX_LABEL
            )

        self.checkbox_boxes.children = list(self.checkbox_dict.values())
        self.checkbox_labels.children = list(self.label_dict.values())


    def search_widget_change_listener(self, change):
        """Change handler for the search widget. Filters visible checkboxes"""
        search_input = change['new']
        new_checkboxes = []
        new_labels = []

        if search_input == '':
            new_checkboxes = [self.checkbox_dict[filename] for filename in self.filenames]
            new_labels = [self.label_dict[filename] for filename in self.filenames]
        else:
            matches = [filename for filename in self.filenames if search_input in filename]
            new_checkboxes = [self.checkbox_dict[filename] for filename in matches]
            new_labels = [self.label_dict[filename] for filename in matches]

        self.checkbox_boxes.children = new_checkboxes
        self.checkbox_labels.children = new_labels


    def get_search_widget(self):
        """Return a search widget"""
        search_widget = widgets.Text(
            layout=LAYOUT_SEARCH,
            placeholder='Type here to search..',
            continuous_update=False
        )
        search_widget.observe(self.search_widget_change_listener, names='value')

        return search_widget


    def selectall_button_listener(self, element):
        """action when selectall button is clicked"""
        if element.description == 'Select All':
            element.description = 'Deselect All'
            for item in self.checkbox_boxes.children:
                item.value = True
        else:
            element.description = 'Select All'
            for item in self.checkbox_boxes.children:
                item.value = False


    def get_selectall_button(self):
        """Button to select or deselect all checkboxes in the file widget"""
        button = widgets.Button(
            description='Select All',
            style=STYLE_BUTTON,
            button_color='lightgray',
            layout=LAYOUT_SELECTALL_BUTTON
        )

        button.on_click(self.selectall_button_listener)

        return button


    def action_download(self, _element):
        """Action when the Download datalayer(s) button is clicked"""
        self.output.clear_output(True)

        with self.output:
            if len(self.selected_filenames) == 0:
                display(widgets.HTML('<b>Select a datalayer ID to download!</b>'))
            else:
                folder_name = generate_folder_name('_hdl_json_downloads')
                folder_path = os.path.join(os.getcwd(), folder_name)

                create_folder(folder_path)

                for filename in self.selected_filenames:
                    datalayer = get_datalayer(filename)

                    with open(os.path.join(folder_path, f'{filename}.json'), 'w') as file:
                        file.write(json.dumps(datalayer, indent=4))

                    print(f'Downloaded the file: {filename}.json')

                print(f'***All files are stored in the folder: "{folder_name}"')


    def action_download_master(self, _element):
        """Action when the Download masterfile button is clicked"""
        self.output.clear_output(True)

        with self.output:
            if len(self.selected_filenames) == 0:
                display(widgets.HTML('<b>Select a datalayer ID to download!</b>'))
            else:
                folder_name = generate_folder_name('_hdl_master_downloads')
                folder_path = os.path.join(os.getcwd(), folder_name)

                create_folder(folder_path)

                master_dict = {}

                for filename in self.selected_filenames:
                    master_dict[filename] = get_datalayer(filename)

                with open(os.path.join(folder_path, 'master.json'), 'w') as file:
                    file.write(json.dumps(master_dict, indent=4))

                print(f'Downloaded the following master file "{folder_name}/master.json"')


    def action_delete(self, _element):
        """Action when the delete datalayer(s) button is clicked"""
        self.output.clear_output(True)

        with self.output:
            if len(self.selected_filenames) == 0:
                display(widgets.HTML('<b>You have not selected anything.</b>'))
                return

        delete_menu = DeleteMenu(self.selected_filenames, self)
        delete_menu.show()


    def action_show(self, _element):
        """Action when the Show datalayer(s) button is clicked"""
        self.output.clear_output(True)

        with self.output:
            if len(self.selected_filenames) == 0:
                display(widgets.HTML('<b>Select a datalayer ID to show the output!</b>'))
            else:
                datalayer_dfs = []
                for filename in self.selected_filenames:
                    datalayer = get_datalayer(filename)

                    datalayer_dfs.append(dict_to_df(
                        datalayer=datalayer,
                        filename=filename
                    ))

                merged_dfs = merge_dfs(datalayer_dfs)

                html_df = widgets.HTML(
                    merged_dfs.style.set_table_attributes(
                        'class="table"'
                    ).render(),
                    indent=False
                )

                display(HBox((html_df,)))


    def get_action_buttons(self):
        """Get Action buttons for the View menu"""
        button_show = widgets.Button(
            description='Show DataLayer(s)',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_ACTION_BUTTON_TOP
        )
        button_show.on_click(self.action_show)

        button_download = widgets.Button(
            description='Download DataLayer(s)',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_ACTION_BUTTON_OTHER
        )
        button_download.on_click(self.action_download)

        button_master = widgets.Button(
            description='Download Master File',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_ACTION_BUTTON_OTHER
        )
        button_master.on_click(self.action_download_master)

        button_delete = widgets.Button(
            description='Delete DataLayer(s)',
            style=STYLE_BUTTON,
            button_style='danger',
            layout=LAYOUT_ACTION_BUTTON_OTHER
        )
        button_delete.on_click(self.action_delete)

        return widgets.VBox([
            button_show,
            button_download,
            button_master,
            button_delete
        ])


    def get_file_widget(self):
        """Return a widget where existing JSON datalayer files can be selected"""
        search_widget = self.get_search_widget()

        self.checkbox_boxes = widgets.VBox(layout=LAYOUT_CHECKBOX_BOX_VIEW)
        self.checkbox_labels = widgets.VBox()

        self.checkbox_boxes.children = [widgets.Checkbox(
            value=False,
            indent=False,
            layout=LAYOUT_VIEW_PRELOAD_BOX
        )]

        self.checkbox_labels.children = [widgets.Label(
            'Loading items, please wait...',
            layout=LAYOUT_VIEW_PRELOAD_LABEL
        )]

        checkboxes = widgets.HBox([self.checkbox_boxes, self.checkbox_labels])
        checkboxes_wrapper = widgets.VBox([checkboxes], layout=LAYOUT_CHECKBOX_WRAPPER)

        selectall_button = self.get_selectall_button()

        file_widget_checkboxes = widgets.VBox(
            [search_widget, checkboxes_wrapper, selectall_button]
        )

        action_buttons = self.get_action_buttons()

        file_widget = widgets.HBox([file_widget_checkboxes, action_buttons], layout={
            'justify_content': 'space-between'
        })

        return file_widget

    def refresh(self):
        """Refresh View Menu"""
        self.output.clear_output()

        self.filenames = []
        self.selected_filenames = []

        self.checkbox_dict = {}
        self.label_dict = {}

        self.checkbox_boxes = None
        self.checkbox_labels = None

        self.file_widget = self.get_file_widget()

        self.show()

        self.load_datalayers()


    def show(self):
        """Show the view Menu"""
        clear_output()

        cfg.OPEN_MENU = 'view'

        display(self.title, self.file_widget, self.output, self.navigation_buttons)
