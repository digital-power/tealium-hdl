from ipywidgets import Layout

STYLE_BUTTON = {
    'font_weight': 'bold'
}

STYLE_TEXT_INPUT = {
    'description_width': '25%'
}

LAYOUT_TEXT_INPUT = Layout(width='90%', padding='5px')

LAYOUT_MAIN_BUTTON_PRIMARY = Layout(
    width='450px',
    margin='5px'
)

LAYOUT_MAIN_BUTTON_SECONDARY = Layout(
    width='200px',
    margin='5px'
)

LAYOUT_BUTTON_BOX = Layout(justify_content='space-between', margin='40px 0px 0px 0px')

LAYOUT_SEARCH = Layout(width='650px', margin='0px 0px 20px 0px')

LAYOUT_FOLDER_WIDGET = Layout(width='auto', margin='0px 0px 0px 0px')

LAYOUT_CHECKBOX_BOX_UPLOAD = Layout(margin='0px -90px 0px -75px', padding='2px 0px 0px 0px')
LAYOUT_CHECKBOX_BOX_VIEW = Layout(margin='0px -180px 0px 5px', padding='2px 0px 0px 0px')

LAYOUT_CHECKBOX = Layout(width='200px')

LAYOUT_CHECKBOX_LABEL = Layout(width='600px')

LAYOUT_CHECKBOX_WRAPPER = Layout(
    overflow_y='auto',
    display='block',
    height='200px',
    border='1px solid darkgray',
    width='649px'
)

LAYOUT_SELECTALL_BUTTON = Layout(
    width='200px',
    margin='10px 0px 0px 0px',
    justify_content='flex-start'
)

LAYOUT_ACTION_BUTTON_TOP = Layout(
    width='200px',
    margin='0px 5px 5px 5px'
)

LAYOUT_ACTION_BUTTON_OTHER = Layout(
    width='200px',
    margin='25px 5px 5px 5px'
)

LAYOUT_DEFAULT_BUTTON = Layout(
    width='200px',
    margin='5px 5px 5px 0px'
)

LAYOUT_OUTPUT = Layout(
    max_height='600px',
    overflow_y='auto',
    display='block'
)

LAYOUT_VIEW_PRELOAD_BOX = Layout(
    width='200px',
    visibility='hidden'
)
LAYOUT_UPLOAD_PRELOAD_BOX = LAYOUT_VIEW_PRELOAD_BOX

LAYOUT_VIEW_PRELOAD_LABEL = Layout(
    width='600px'
)
LAYOUT_UPLOAD_PRELOAD_LABEL = LAYOUT_VIEW_PRELOAD_LABEL

LAYOUT_DELETE_FILES_LIST = Layout(
    max_height='200px',
    border='1px solid lightgray',
    overflow_y='auto',
    display='block'
)

LAYOUT_CREATE_FILES_LIST = Layout(
    max_height='400px',
    border='1px solid lightgray',
    overflow_y='auto',
    display='block',
    margin='0px 0px 0px -20px'
)

LAYOUT_UPDATE_FILES_LIST = Layout(
    overflow_y='auto',
    display='block'
)

LAYOUT_DELETE_QUESTIONS = Layout(
    margin='20px 0px 0px 0px'
)

LAYOUT_DELETE_QUESTION_BOX = Layout(
    justify_content='center'
)

LAYOUT_DELETE_TEXTFIELD = LAYOUT_DELETE_BUTTON = LAYOUT_UPLOAD_BUTTON = LAYOUT_CHECKBOX

LAYOUT_DELETE_SUBMIT_BOX = Layout(
    justify_content='center'
)

LAYOUT_UPLOAD_SUBMIT_BOX = Layout(
    justify_content='center'
)

LAYOUT_GOBACK_BUTTON = Layout(
    width='200px',
    margin='40px 5px 5px 0px'
)

LAYOUT_GOBACK_BOX = Layout(
    justify_content='flex-end'
)

LAYOUT_UPLOAD_WIDGET = Layout(
    padding='20px',
)

LAYOUT_UPLOAD_UPDATE_DIFF = Layout(
    margin='0px 0px 0px 50px'
)

LAYOUT_UPLOAD_UPDATE_BOX = Layout(
    align_items='center',
    margin='0px 0px 15px 0px',
    border='1px solid lightgray'
)
