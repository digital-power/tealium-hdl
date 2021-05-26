from ipywidgets import widgets
from IPython.display import display, clear_output

import hdl.config as cfg

from hdl.api import delete_datalayers

from hdl.styles import LAYOUT_DELETE_FILES_LIST, LAYOUT_DELETE_QUESTIONS, LAYOUT_DELETE_QUESTION_BOX
from hdl.styles import STYLE_BUTTON, LAYOUT_DELETE_BUTTON, LAYOUT_DELETE_SUBMIT_BOX, LAYOUT_GOBACK_BUTTON
from hdl.styles import LAYOUT_GOBACK_BOX, LAYOUT_OUTPUT, LAYOUT_DELETE_TEXTFIELD


class DeleteMenu:
    def __init__(self, selected_filenames, view_menu):
        self.selected_filenames = selected_filenames
        self.view_menu = view_menu

        self.delete_text_field = None

        self.title = widgets.HTML(
            '<h4><center><b>You are about to delete the file(s) below:</b></center></h4>')
        self.output = widgets.Output(layout=LAYOUT_OUTPUT)
        self.delete_widget = self.get_delete_files_widget()

    def get_delete_files_list(self):
        """Create HTML List to show elements that are to be deleted"""
        files = [widgets.HTML(
            f'<b>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{filename}</b>') for filename in self.selected_filenames]

        files_list = widgets.VBox(files)

        return widgets.HBox([files_list], layout=LAYOUT_DELETE_FILES_LIST)

    def get_delete_questions(self):
        """Create widgets that ask if it's okay to delete a datalayer"""
        question_sure = widgets.HTML("""
            <center>Are you really sure you want to do this? \n
            This has immediate effect on your website data!</center>
        """)

        question_validation = widgets.HTML(
            '<center>Type "delete" and click on the Delete button in order to finalize this action.</center>')

        return widgets.VBox([question_sure, question_validation], layout=LAYOUT_DELETE_QUESTIONS)

    def action_goback(self, _element):
        """Action when the Go Back button is clicked"""
        self.view_menu.show()

    def action_submit(self, _element):
        """Action when the delete submit button is clicked"""
        self.output.clear_output()

        with self.output:
            if self.delete_text_field.value == 'delete':
                delete_datalayers(self.selected_filenames)
            else:
                print('Please enter the value "delete" to confirm')

    def get_delete_files_widget(self):
        """Create delete files widget"""
        files_list = self.get_delete_files_list()
        questions = self.get_delete_questions()
        files_questions_box = widgets.VBox(
            [files_list, questions], layout=LAYOUT_DELETE_QUESTION_BOX)

        delete_submit_button = widgets.Button(
            description='Delete',
            style=STYLE_BUTTON,
            button_style='primary',
            layout=LAYOUT_DELETE_BUTTON
        )
        delete_submit_button.on_click(self.action_submit)

        self.delete_text_field = widgets.Text(layout=LAYOUT_DELETE_TEXTFIELD)
        delete_submit_box = widgets.HBox(
            [self.delete_text_field, delete_submit_button], layout=LAYOUT_DELETE_SUBMIT_BOX)

        button_goback = widgets.Button(
            description='Go Back',
            style=STYLE_BUTTON,
            button_style='warning',
            layout=LAYOUT_GOBACK_BUTTON
        )
        button_goback.on_click(self.action_goback)
        goback_box = widgets.HBox([button_goback], layout=LAYOUT_GOBACK_BOX)

        return widgets.VBox([files_questions_box, delete_submit_box, goback_box])

    def show(self):
        """Show Delete Menu"""
        clear_output()

        cfg.OPEN_MENU = 'delete'

        display(self.title, self.delete_widget, self.output)
