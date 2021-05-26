import os

from IPython.display import display, clear_output
from ipywidgets import widgets

import hdl.config as cfg

from hdl.api import datalayer_exists, get_datalayer
from hdl.utility import split_masterfile, read_json, scan_folders
from hdl.menu import UploadConfirmMenu, NavigationButtons

from hdl.styles import LAYOUT_OUTPUT, LAYOUT_CHECKBOX, LAYOUT_CHECKBOX_LABEL, LAYOUT_FOLDER_WIDGET, LAYOUT_SEARCH
from hdl.styles import LAYOUT_CHECKBOX_BOX_UPLOAD, LAYOUT_CHECKBOX_WRAPPER, STYLE_BUTTON, LAYOUT_ACTION_BUTTON_TOP
from hdl.styles import LAYOUT_ACTION_BUTTON_OTHER, LAYOUT_SELECTALL_BUTTON, LAYOUT_UPLOAD_PRELOAD_BOX
from hdl.styles import LAYOUT_UPLOAD_PRELOAD_LABEL


class UploadMenu:
    def __init__(self, root):
        self.filenames = []
        self.selected_filenames = []

        self.dir_tree = {}
        self.selected_folder = None

        self.checkbox_dict = {}
        self.label_dict = {}

        self.checkbox_boxes = None
        self.checkbox_labels = None

        self.title = widgets.HTML(value='<h4><b><center>Upload or split JSON files to Tealium HDL.</center></b></h4>')
        self.folder_widget = self.get_folder_widget()
        self.file_widget = self.get_file_widget()

        self.widget = widgets.VBox([self.folder_widget, self.file_widget])

        self.output = widgets.Output(layout=LAYOUT_OUTPUT)
        self.navigation_buttons = NavigationButtons(root=root).navigation_buttons

        self.file_widget_first_load()


    def file_widget_first_load(self):
        """Kick-start folder widget change listener to show files for the first Folder"""
        folders = list(self.dir_tree.keys())
        if len(folders) > 0:
            self.folder_widget_change_listener({'new': folders[0]})


    def checkbox_change_listener(self, _change):
        """Change listener for checkboxes. Builds a new selected_filenames array each time
        a checkbox is checked. This is horrendous of course"""
        self.selected_filenames.clear()
        self.output.clear_output()

        for filename in self.checkbox_dict:
            if self.checkbox_dict[filename].value is True:
                self.selected_filenames.append(filename)


    def folder_widget_change_listener(self, change):
        """Loads checkboxes for JSON files if a new folder is selected"""
        self.selected_folder = change['new']
        self.filenames = self.dir_tree[self.selected_folder]

        self.checkbox_boxes.children = [widgets.Checkbox(
            value=False,
            indent=False,
            layout=LAYOUT_UPLOAD_PRELOAD_BOX
        )]

        self.checkbox_labels.children = [widgets.Label(
            'Loading items, please wait...',
            layout=LAYOUT_UPLOAD_PRELOAD_LABEL
        )]

        self.checkbox_dict = {}
        self.label_dict = {}

        for filename in self.filenames:
            self.checkbox_dict[filename] = widgets.Checkbox(
                value=False,
                index=False,
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


    def get_folder_widget(self):
        """Return Widget in which a local folder can be selected"""
        folder_widget_title = widgets.HTML(value='<b>1. Select a folder.</b>')

        current_dir = os.getcwd()
        folder_paths = scan_folders(current_dir)

        for folder_path in folder_paths:
            files_in_folder = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

            json_files = [f for f in files_in_folder if f.endswith('.json')]

            self.dir_tree[folder_path] = json_files

        folder_widget = widgets.Select(
            options=self.dir_tree.keys(),
            value=list(self.dir_tree.keys())[0],
            layout=LAYOUT_FOLDER_WIDGET
        )

        folder_widget.observe(
            self.folder_widget_change_listener,
            names='value'
        )

        return widgets.VBox([folder_widget_title, folder_widget])


    def get_search_widget(self):
        """Return a search widget"""
        search_widget = widgets.Text(
            layout=LAYOUT_SEARCH,
            placeholder='Type here to search..'
        )

        search_widget.observe(self.search_widget_change_listener, names='value')

        return search_widget


    def get_file_widget(self):
        """Return a widget where JSON files in a folder can be selected to be uploaded"""
        file_widget_title = widgets.HTML(value='<b>2.Search and select the required JSON file.</b>')

        file_widget_search = self.get_search_widget()

        self.checkbox_boxes = widgets.VBox(layout=LAYOUT_CHECKBOX_BOX_UPLOAD)
        self.checkbox_labels = widgets.VBox()

        checkboxes = widgets.HBox([self.checkbox_boxes, self.checkbox_labels])
        checkboxes_wrapper = widgets.VBox([checkboxes], layout=LAYOUT_CHECKBOX_WRAPPER)

        selectall_button = self.get_selectall_button()

        file_widget_checkboxes = widgets.VBox(
            [file_widget_search, checkboxes_wrapper, selectall_button]
        )

        action_buttons = self.get_action_buttons()

        checkboxes_and_buttons = widgets.HBox([file_widget_checkboxes, action_buttons], layout={
            'justify_content': 'space-between'
        })

        file_widget = widgets.VBox([file_widget_title, checkboxes_and_buttons])

        return file_widget


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


    def action_upload(self, _element):
        """Action when the upload button is clicked"""
        self.output.clear_output(True)

        with self.output:
            if len(self.selected_filenames) == 0:
                display(widgets.HTML('<b>You have to select something first!</b>'))
                return


        file_paths = [os.path.join(self.selected_folder, filename) for filename in self.selected_filenames]

        datalayer_list = []

        for file_path in file_paths:
            file_name = file_path.split('\\')[-1]
            datalayer_id = file_name.replace('.json', '').replace('&=', '').replace('=', '').lower()
            data = read_json(file_path)

            exists = datalayer_exists(datalayer_id)
            old_data = get_datalayer(datalayer_id) if exists else None

            datalayer_list.append({
                'action_type': cfg.ACTION_UPDATE if exists else cfg.ACTION_CREATE,
                'datalayer_id': datalayer_id,
                'file_path': file_path,
                'old': old_data,
                'new': data
            })

        confirm_menu = UploadConfirmMenu(datalayer_list, self)
        confirm_menu.show()


    def action_split(self, _element):
        """Split JSON master file (file with multiple datalayer JSONs)"""
        self.output.clear_output(True)

        with self.output:
            if len(self.selected_filenames) == 0:
                display(widgets.HTML('<b>You have to select something first!</b>'))
            else:
                full_file_paths = [os.path.join(self.selected_folder, filename) for filename in self.selected_filenames]

                split_masterfile(full_file_paths)


    def get_action_buttons(self):
        """Return action buttons (upload & split)"""
        button_upload = widgets.Button(
            description='Upload File(s)',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_ACTION_BUTTON_TOP
        )
        button_upload.on_click(self.action_upload)

        button_split = widgets.Button(
            description='Split Master File',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_ACTION_BUTTON_OTHER
        )
        button_split.on_click(self.action_split)

        return widgets.VBox([button_upload, button_split])

    def refresh(self):
        """Refresh Upload Menu"""
        self.output.clear_output()

        self.filenames = []
        self.selected_filenames = []

        self.dir_tree = {}
        self.selected_folder = None

        self.checkbox_dict = {}
        self.label_dict = {}

        self.checkbox_boxes = None
        self.checkbox_labels = None

        self.folder_widget = self.get_folder_widget()
        self.file_widget = self.get_file_widget()

        self.widget = widgets.VBox([self.folder_widget, self.file_widget])

        self.show()

        self.file_widget_first_load()


    def show(self):
        """Show the Upload menu"""
        clear_output()

        cfg.OPEN_MENU = 'upload'

        display(self.title, self.widget, self.output, self.navigation_buttons)
