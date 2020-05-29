import ipywidgets as widgets
import urllib
import functools
import requests
import pandas as pd
import os.path, json
import datetime
import shutil

from urllib.parse import urlencode
from datetime import datetime
from ipywidgets import widgets, Layout, interactive, Output, interactive_output, HBox, VBox
from IPython.display import display, clear_output
from collections.abc import Mapping

class TealiumHDL:
    
    def __init__(self):
        style = {'description_width': '25%'}
        box_layout = Layout(width='70%', margin='0%')
        self.l_field_acc = widgets.Text(description="Tealium Account:",
                                 style=style,
                                 layout=box_layout)
        self.l_field_profile = widgets.Text(description="Tealium Profile:",
                                 style=style,
                                 layout=box_layout)
        self.l_field_user = widgets.Text(description="Tealium User Email:",
                                  style=style,
                                  layout=box_layout)
        self.l_field_api = widgets.Text(description="Tealium User API Key:",
                                 style=style,
                                 layout=box_layout,
                                 placeholder='You can find the API key in Tealium iQ - Edit/View User Settings'
                                )
        l_button_submit = widgets.Button(description='Log in',
                                         style={'font_weight': 'bold'},
                                         button_style='primary')
        display(self.l_field_acc,
                self.l_field_profile,
                self.l_field_user,
                self.l_field_api,
                l_button_submit)
        self.l_widgets = [self.l_field_acc,
                          self.l_field_profile,
                          self.l_field_user,
                          self.l_field_api,
                          l_button_submit]

        l_button_submit.on_click(self.loginHDL)

    def loginHDL(self,b):
        self.current_dir = os.getcwd()
        self.tealium_account = self.l_field_acc.value
        self.tealium_profile = self.l_field_profile.value
        self.tealium_username = self.l_field_user.value
        self.tealium_api_key = self.l_field_api.value
        self.tealium_auth_url = 'https://api.tealiumiq.com/v2/auth'
        self.tealium_api_url = f'https://api.tealiumiq.com/v2/dle/accounts/{self.tealium_account}' \
                            f'/profiles/{self.tealium_profile}/datalayers/'
        self.current_dir = os.getcwd()
        self.folders_in_dir = [f.name for f in os.scandir(self.current_dir) if f.is_dir()]
        self.file_dir = {}
        self.selected_items = []
        self.descriptions = []

        try:
            self.tealium_token = json.loads(requests.post(self.tealium_auth_url
                                      , data={'username': self.tealium_username
                                              , 'key': self.tealium_api_key}).text)['token']
            self.request_header = {'Authorization' : 'Bearer ' + self.tealium_token, 
                   'Accept' : 'application/json', 
                   'Content-Type' : 'application/json'}
        except Exception as identifier:
            print('Error: Wrong Tealium credentials or API key')

        if len(self.tealium_token) > 800:
            clear_output()
            self.hdl_main_menu()
            
    def view_menu_preload(self):
        r = requests.get(self.tealium_api_url, headers=self.request_header)
        if r.status_code == 200:
            try:
                output_list = json.loads(r.text)['fileStatuses']
                id_list = []
                for i in output_list:
                    id_list.append(i['file']
                                    .replace(f'dle/{self.tealium_account}/{self.tealium_profile}/','')
                                    .replace('.js',''))
            except ValueError as e:
                return print('Something was wrong')
        return id_list
        
    def hdl_main_menu(self):   
                
        self.descriptions = self.view_menu_preload()       
        option_table_layout = {'width': '450px', 'margin':'5px'}
        other_layout = {'width': '200px', 'margin':'5px'}
        
        menu_question = widgets.HTML(value='<h3><b><center>Tealium HDL Model - Navigation Menu</center></b></h3>')

        menu_button_view = widgets.Button(description='View files in Tealium HDL',
                                         style={'font_weight': 'bold'},
                                         button_style='primary', layout=option_table_layout)
        menu_button_upload = widgets.Button(description='Upload files to Tealium HDL',
                                         style={'font_weight': 'bold'},
                                         button_style='primary', layout=option_table_layout)
        menu_button_readme = widgets.Button(description='Read more',
                                         style={'font_weight': 'bold'},
                                         button_style='info', layout=other_layout)
        menu_button_logout = widgets.Button(description='Log out',
                                         style={'font_weight': 'bold'},
                                         button_style='warning', layout=other_layout)

        dip_img =  widgets.HTML('<div id="img" style="width:auto; height:200px; '
                            'border:1px dashed lightgray; text-align:center; vertical-align:center;">'
                            '<img style="vertical-align:middle;"'
                            'src="https://digital-power.com/wp-content/uploads/2018/08/logo_dip_rgb.png" alt="">'                       
                            '</div>')

        menu_button_box= widgets.HBox([menu_button_upload, menu_button_view],
                                     layout=Layout(justify_content='space-between',margin='40px 0px 0px 0px'))

        menu_box_with_image = widgets.VBox([dip_img,menu_button_box])

        other_box = widgets.HBox([menu_button_readme,menu_button_logout]
                                 , layout=Layout(justify_content='space-between',margin='40px 0px 0px 0px'))

        main_menu = widgets.VBox([menu_question, menu_box_with_image, other_box])
        display(main_menu)
        
        def logout(b):
            clear_output()
            print('You have logged out successfully')

        def upload(b):
            clear_output()
            self.descriptions = []
            self.upload_menu_create()
            
        def read_me(b):
            print('This feature will be implemented soon')
            
        def view(b):
            clear_output()
            #get descriptions from view preload and overwrite descriptions for checkbox menu
            self.view_menu_create()
            
        menu_button_view.on_click(view)
        menu_button_upload.on_click(upload)
        menu_button_logout.on_click(logout)
        menu_button_readme.on_click(read_me)
        
    def widget_search(self):
        widget_search = widgets.Text(layout={'width':'650px','margin':'0px 0px 20px 0px'}
                                     ,placeholder='Type here to search..')
        return widget_search
        
    def widget_search_listener(self,change):
        search_input = change['new']
        if search_input == '':
            # Reset search field
            new_checkboxes = [self.checkbox_dict[description] for description in self.descriptions]
            new_labels = [self.labels_dict[description] for description in self.descriptions]
        else:
            # Filter by search field using difflib.
            close_matches = [k for k in self.descriptions if search_input in k]
            new_checkboxes = [self.checkbox_dict[description] for description in close_matches]
            new_labels = [self.labels_dict[description] for description in close_matches]
        self.options_checkbox.children = new_checkboxes
        self.options_labels.children = new_labels
                
    def widget_multi_checkbox(self):
                
        self.options_checkbox = widgets.VBox(layout = {'margin':'1px -180px 0px 0px'})
        self.options_labels = widgets.VBox()

        if self.open_menu == 'view':
            self.options_checkbox.children = [widgets.Checkbox(value=False
                                                               , indent=False
                                                               , layout=Layout(width='200px'
                                                                               ,visibility='hidden'))]
            self.options_labels.children = [widgets.Label('Loading items, please wait...'
                                                     ,layout=Layout(width='600px'))]
            
        options_widget = widgets.HBox([self.options_checkbox,self.options_labels])
        options_widget_V = widgets.VBox([options_widget],
                                        layout=Layout(overflow_y='auto',
                                                      display='block',
                                                      height='200px',
                                                      border='1px solid darkgray',
                                                      width='649px'))
        
        
        self.button_selectAll = widgets.Button(description='Select All',
                         style={'font_weight': 'bold'},
                         button_color='lightgray', layout={'width': '200px',
                                                         'margin':'10px 0px 0px 0px',
                                                        'justify-content':'flex-start'})

        def on_select_all_bc(b):
            if b.description == 'Select All':
                b.description = 'Deselect All'
                for item in self.options_checkbox.children:
                    item.value = True
            else:
                b.description = 'Select All'
                for item in self.options_checkbox.children:
                    item.value = False

        #listeners
        self.button_selectAll.on_click(on_select_all_bc)
        
        multi_select = widgets.VBox([options_widget_V, self.button_selectAll])
            
        return multi_select
    
    def widget_multi_checkbox_new_values(self):
        names = []
        checkbox_objects, label_objects = [],[]
        
        for key in self.descriptions:
            checkbox_objects.append(widgets.Checkbox(value=False, indent=False,layout=Layout(width='200px')))
            label_objects.append(widgets.Label(f'{key}',layout=Layout(width='600px')))
            names.append(key)
        
        self.checkbox_dict = {names[i]: checkbox for i, checkbox in enumerate(checkbox_objects)}
        self.labels_dict = {names[i]: label for i, label in enumerate(label_objects)}        
        self.options_checkbox.children = checkbox_objects
        self.options_labels.children = label_objects
        
        self.selected_items = []
        def select_data(**kwargs):
            self.selected_items.clear()
            self.action_output.clear_output()
            for key in self.checkbox_dict:
                if self.checkbox_dict[key].value is True:
                    self.selected_items.append(key)
                
        clear_output = widgets.interactive_output(select_data, self.checkbox_dict)
        
    def upload_menu_widget_folder(self):
        self.current_dir = os.getcwd()
        self.folders_in_dir = [f.name for f in os.scandir(self.current_dir) if f.is_dir()]
        self.file_dir = {}
        for entry in self.folders_in_dir:
            # Create full path
            fullPath = os.path.join(self.current_dir, entry)
            files_in_fullPath = [f for f in os.listdir(fullPath) if os.path.isfile(os.path.join(fullPath, f))]
            json_files = [f for f in files_in_fullPath if '.json' in f]
            self.file_dir[fullPath] = json_files
        widget_folder = widgets.Select(options=self.file_dir.keys(),
                                      layout=Layout(width='auto', margin='0px 0px 0px 0px'))
        return widget_folder
        
    def upload_menu_widget_folder_listener(self,change):
        self.selected_folder_path = change['new']
        self.descriptions = []
        self.descriptions = self.file_dir[self.selected_folder_path]
        self.widget_multi_checkbox_new_values()
        self.button_selectAll.description = 'Select All'
        
    def upload_menu_action_buttons(self):
        #action buttons
        self.button_upload = widgets.Button(description='Upload File',
                                         style={'font_weight': 'bold'},
                                         button_style='primary', layout={'width': '200px',
                                                                             'margin':'0px 5px 5px 5px'})
        self.button_split = widgets.Button(description='Split Master File',
                                         style={'font_weight': 'bold'},
                                         button_style='primary', layout={'width': '200px',
                                                                             'margin':'25px 5px 5px 5px'})
        return self.button_upload,self.button_split
    
    def upload_menu_action_buttons_listeners(self):

        self.action_output = widgets.Output()
        self.action_output.layout = Layout(max_height='400px',overflow_y='auto',display='block')
        
        def on_upload_bc(b):
            with self.action_output:
                clear_output(True)
                if len(self.selected_items) == 0:
                    no_select = widgets.HTML(value='<b>You have to select something first!</b>')
                    display(no_select)
                else:
                    filepath = self.selected_folder_path
                    for item in self.selected_items:
                        json_file = item
                        file = open(os.path.join(filepath,json_file))
                        try:
                            payload = json.load(file)
                            datalayer_id = json_file.replace('.json','').replace('&=','').replace('=','')
                            request_url = self.tealium_api_url + datalayer_id
                            r = requests.post(request_url, data=json.dumps(payload), headers=self.request_header)
                            status = r.text
                            if status == '':
                                status = 'success'
                            else:
                                status = status
                            print(f'> The file: "{datalayer_id}" uploaded as a datalayer to Tealium HDL with status: "{status}"')
                        except ValueError as e:
                            return f'> The file: "{file}" does not contain a correct JSON format!'
                    print('*** All selected files are processed ***')
                
        self.button_upload.on_click(on_upload_bc)
        
        def on_split_bc(b):
            with self.action_output:
                clear_output(True)
                if len(self.selected_items) == 0:
                    no_select = widgets.HTML(value='<b>You have to select something first!</b>')
                    display(no_select)
                else:
                    for item in self.selected_items:
                        file = item
                        with open(os.path.join(self.selected_folder_path,file), "r") as f:
                            try:
                                data = json.load(f)
                                #Validate if all keys has dict structure
                                if isinstance(data, Mapping):
                                    for k, v in data.items():
                                        if isinstance(v, Mapping):
                                            master_validate = True
                                        else:
                                            master_validate = False
                                            break
                            except ValueError as e:
                                return f'The file {file} does not contain a correct JSON format!'
                        if master_validate is True:
                            folder_name = datetime.today().strftime('%Y-%m-%d') + '_master_split_' + item.replace('.json','')
                            filepath = os.path.join(self.current_dir, folder_name)
                            if os.path.exists(filepath):
                                shutil.rmtree(filepath)
                            os.mkdir(filepath)
                            for k,v in data.items():
                                filename = k+".json"
                                with open(os.path.join(filepath,filename),"w") as f:
                                    i = json.dumps(v)
                                    f.write('%s' %(i))
                            print(f'> The folder: "{folder_name}" is created in your directory' \
                                  f'\n     Writing output from "{file}" to that folder.')
                        else:
                            print(f'> The file: "{file}" does contain the right format in order to split the file.')
        self.button_split.on_click(on_split_bc)
        
        return self.action_output

    def view_menu_action_buttons(self):
        self.button_show = widgets.Button(description='Show DataLayer(s)',
                                         style={'font_weight': 'bold'},
                                         button_style='primary', layout={'width': '200px',
                                                                         'margin':'0px 5px 5px 5px'})

        self.button_download = widgets.Button(description='Download DataLayer(s)',
                                         style={'font_weight': 'bold'},
                                         button_style='primary', layout={'width': '200px',
                                                                         'margin':'20px 5px 5px 5px'})

        self.button_master = widgets.Button(description='Download Master File',
                                         style={'font_weight': 'bold'},
                                         button_style='primary', layout={'width': '200px',
                                                                         'margin':'20px 5px 5px 5px'})

        self.button_delete = widgets.Button(description='Delete DataLayer(s)',
                                         style={'font_weight': 'bold'},
                                         button_style='danger', layout={'width': '200px',
                                                                         'margin':'20px 5px 5px 5px'})

        button_action_box = widgets.VBox([self.button_show, 
                                          self.button_download,
                                          self.button_master,
                                          self.button_delete])
        return button_action_box

    def view_menu_action_buttons_listeners(self):
        
        self.action_output = widgets.Output()
        self.action_output.layout = Layout(max_height='400px',overflow_y='auto',display='block')
        
        def on_show_selected_bc(b):
            with self.action_output:
                clear_output(True)
                dfs = []
                if not self.selected_items:
                    info_show = widgets.HTML(value='<b>Select a datalayer ID to show the output!</b>')
                    display(info_show)
                elif len(self.selected_items) > 0:
                    for item in self.selected_items:
                        r = requests.get(f"https://tags.tiqcdn.com/dle/unive/adv-unive-nl/{item}.js")
                        tealium_request_js = r.text.split('= ')
                        json_string = tealium_request_js[1]
                        data = json.loads(json_string)
                        df = pd.DataFrame([data.keys(),data.values()]).transpose()
                        df.columns = ['Variable',tealium_request_js[0].split('[\'')[1].replace("\'] ","")]
                        dfs.append(df)
                    from functools import reduce
                    joined_df = reduce(lambda x, y: pd.merge(x,
                                                            y,
                                                            on='Variable',
                                                            how='outer'), dfs).fillna('')
                    df_html = widgets.HTML(joined_df.style.set_table_attributes('class="table"').render(), indent=False)
                    final_df = HBox([df_html])
                    display(final_df)
                    
        self.button_show.on_click(on_show_selected_bc)

        def on_download_output_bc(b):
            with self.action_output:
                clear_output(True)
                if not self.selected_items:
                    info_download = widgets.HTML(value='<b>Select a datalayer ID to do a download!</b>')
                    display(info_download)
                elif len(self.selected_items) > 0:
                    if b.description == 'Download Master File':
                        folder_name = datetime.today().strftime('%Y-%m-%d') + '_hdl_master_downloads'
                        filepath = os.path.join(self.current_dir, folder_name)
                        if not os.path.exists(folder_name):
                            os.mkdir(filepath)
                        json_dict = {}
                        for item in self.selected_items:
                            r = requests.get(f"https://tags.tiqcdn.com/dle/unive/adv-unive-nl/{item}.js")
                            tealium_request_js = r.text.split('= ')
                            data = tealium_request_js[1]
                            json_data = json.loads(data)
                            json_dict[item] = json_data
                        file_name = datetime.today().strftime('%Y-%m-%d-%H%M%S') +"_master.json"
                        with open(os.path.join(filepath,file_name),"w") as f:
                            file_output = json.dumps(json_dict)
                            f.write('%s' %(file_output))
                        print(f'> Downloaded the following master file: "{file_name}".')
                        print(f'***Stored in the folder: "{folder_name}"***')  
                    else:
                        folder_name = datetime.today().strftime('%Y-%m-%d') + '_hdl_json_downloads'
                        filepath = os.path.join(self.current_dir, folder_name)
                        if not os.path.exists(folder_name):
                            os.mkdir(filepath)
                        for item in self.selected_items:
                            r = requests.get(f"https://tags.tiqcdn.com/dle/unive/adv-unive-nl/{item}.js")
                            tealium_request_js = r.text.split('= ')
                            file_data = tealium_request_js[1]
                            file_name = item+".json"
                            with open(os.path.join(filepath,file_name),"w") as f:
                                f.write('%s' %(file_data))
                            print(f'> Downloaded the following dataLayer file: "{file_name}".')
                        print(f'***All your files are stored in the folder: "{folder_name}"***')

        self.button_download.on_click(on_download_output_bc)
        self.button_master.on_click(on_download_output_bc)
        
        def on_delete_bc(b):
            if len(self.selected_items) > 0:
                clear_output()
                self.view_menu_delete_function()
            elif not self.selected_items:                
                with self.action_output:
                    clear_output(True)
                    info_delete = widgets.HTML(value='<b>You have not selected anything.</b>')
                    display(info_delete)
            
        self.button_delete.on_click(on_delete_bc)
        
        return self.action_output
    
    def delete_function_on_delete_output_bc(self,b):
        with self.action_output:
            if self.delete_text_field.value == 'delete':
                clear_output()
                delete_items = self.selected_items
                status_list = []
                #delete items:
                for item in delete_items:
                    request_url = self.tealium_api_url + item
                    r = requests.delete(request_url, headers=self.request_header)
                    status = r.text
                    if status=='':
                        status_list.append('success')
                    else:
                        status_list.append(status)
                #generate delete output:
                title = widgets.HTML('')
                if len(status_list) == 1 and status_list[0] == "success":
                    o = '<b><center>*** The file is successfully deleted from Tealium HDL. ***</center></b>'
                    final_result = widgets.HTML(o)
                elif len(status_list) > 1:
                    status_check = False;
                    status_check = all(elem == "success" for elem in status_list)    
                    if status_check:
                        o = '<b><center>*** All the above files are successfully deleted from Tealium HDL. ***</center></b>'
                        final_result = widgets.HTML(o)
                    else:
                        result_list = []
                        for item,status in zip(delete_items,status_list):
                            title = widgets.HTML('<b>There was something wrong with one or more files:</b>')
                            delete_item = widgets.HTML(f'> The file <b>{item}</b> has been deleted with the status <b>{status}</b>')
                            result_list.append(delete_item)
                        final_result = widgets.VBox(result_list)
                display(title,final_result)
            else:
                clear_output()
                print('Please enter the value "delete" in the text box in order to fulfill your delete action.')
        
        return self.action_output
    
    def view_menu_delete_function(self):
        delete_title = widgets.HTML(value='<h4><center><b>You are about to delete the file(s) below:</b></center></h4>')
        cols = [('', self.selected_items)]
        vboxes = []
        for header, data in cols:
            vboxes.append(widgets.VBox([widgets.HTML('<b>%s</b>' % header)] + [
                d if isinstance(d, widgets.Widget) else widgets.HTML(f'<b>>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{d}</b>') for d in data],
            layout=widgets.Layout()))

        files = widgets.HBox(vboxes,layout=Layout(max_height='200px',
                                                 border='1px solid lightgray',
                                                 overflow_y='auto',
                                                 display='block'))

        question_sure = widgets.HTML(value='<center>Are you really sure you want to do this? This has immediate effect on your website!</center>')
        question_help = widgets.HTML(value='<center>Type "delete" and click on the Delete button in order to finalize this action.</center>')
        question_box = widgets.VBox([question_sure,question_help],layout=Layout(margin='20px 0px 0px 0px'))

        files_question_box = widgets.VBox([files,question_box],layout=Layout(justify_content='center'))

        self.delete_text_field = widgets.Text(layout={'width': '200px'})

        button_delete_submit = widgets.Button(description='Submit',
                                                 style={'font_weight': 'bold'},
                                                 button_style='primary', layout={'width': '200px'})
        
        button_delete_submit.on_click(self.delete_function_on_delete_output_bc)

        delete_box = widgets.HBox([self.delete_text_field,button_delete_submit],layout=Layout(justify_content='center'))

        button_go_back_view = widgets.Button(description='Go back',
                                                 style={'font_weight': 'bold'},
                                                 button_style='warning', layout={'width': '200px',
                                                                                 'margin':'40px 5px 5px 0px'})
        
        def go_back_to_view_menu(b):
            clear_output()
            self.view_menu_create()

        button_go_back_view.on_click(go_back_to_view_menu)
        
        back_view_box = widgets.HBox([button_go_back_view],layout=Layout(justify_content='flex-end'))
        
        display(delete_title, files_question_box, delete_box,self.action_output, back_view_box)
        
    def default_action_buttons(self):
        
        self.button_logout = widgets.Button(description='Log out',
                                 style={'font_weight': 'bold'},
                                 button_style='warning', layout={'width': '200px',
                                                                 'margin':'5px 5px 5px 0px'})
        
        self.button_go_back = widgets.Button(description='Go back to main menu',
                                         style={'font_weight': 'bold'},
                                         button_style='warning', layout={'width': '200px',
                                                                         'margin':'5px 5px 5px 0px'})


        self.button_readme = widgets.Button(description='Read more',
                                         style={'font_weight': 'bold'},
                                         button_style='info', layout={'width': '200px',
                                                                      'margin':'5px 5px 5px 0px'})
        
        self.button_refresh = widgets.Button(description='Refresh page',
                                         style={'font_weight': 'bold'},
                                         button_style='success', layout={'width': '200px',
                                                                         'margin':'5px 5px 5px 0px'})

    def default_action_buttons_listeners(self):
        
        def go_back_to_menu(b):
            clear_output()
            self.hdl_main_menu()

        self.button_go_back.on_click(go_back_to_menu)
        
        def refresh_menu(b):
            if self.open_menu == 'upload':
                clear_output()
                self.upload_menu_create()
            elif self.open_menu == 'view':
                clear_output()
                self.view_menu_create()
        
        self.button_refresh.on_click(refresh_menu)
                
    def upload_menu_create(self):
        
        self.open_menu = 'upload'
        
        #Menu Title
        q = widgets.HTML(value='<h4><b><center>Upload or split JSON files to Tealium HDL.</center></b></h4>')
        
        #folder widget
        folder_question = widgets.HTML(value='<b>1. Select a folder.</b>')       
        widget_folder = self.upload_menu_widget_folder()                   
        widget_folder.observe(self.upload_menu_widget_folder_listener, names='value')
        select_widget_folder = widgets.VBox([folder_question, widget_folder]) 
        
        #Checkbox widget
        checkbox_info = widgets.HTML(value='<b>2.Search and select the required JSON file.</b>')
        widget_search = self.widget_search()
        widget_search.observe(self.widget_search_listener, names='value')
        
        widget_checkbox = self.widget_multi_checkbox()
        checkbox_with_search = widgets.VBox([widget_search,widget_checkbox])
        
        #action buttons
        upload,split = self.upload_menu_action_buttons()
        button_action_box = widgets.VBox([upload, split])
        
        #total excluding output or other box
        checkbox_with_buttons = widgets.HBox([checkbox_with_search,button_action_box]
                                             , layout={'justify_content':'space-between'})
        final_widget_checkbox = widgets.VBox([checkbox_info,checkbox_with_buttons],
                                            layout=Layout(margin='20px 0px 0px 0px'))
        
        widget_total = widgets.VBox([select_widget_folder, final_widget_checkbox])
        
        #Create output listeners
        action_output = self.upload_menu_action_buttons_listeners()
        
        #other box
        self.default_action_buttons()
        other_box = widgets.HBox([self.button_refresh, self.button_go_back], layout={'justify_content':'space-between'}) 
        self.default_action_buttons_listeners()
        
        #total display
        display(q,widget_total,action_output,other_box)
        
    def view_menu_create(self):
        
        self.open_menu = 'view'
        
        #Menu Title
        q = widgets.HTML(value='<h4><b><center>Here you can find the uploaded datalayers in Tealium HDL.</center></b></h4>')
        
        #search + checkbox widget
        widget_search = self.widget_search()
        widget_search.observe(self.widget_search_listener, names='value')
        
        widget_checkbox = self.widget_multi_checkbox()
        
        checkbox_with_search = widgets.VBox([widget_search,widget_checkbox])
        
        #action buttons
        button_action_box = self.view_menu_action_buttons()

        #Final box
        multi_checkbox_box = widgets.HBox([checkbox_with_search,button_action_box]
                                          , layout={'justify_content':'space-between'})
        
        #Create output listeners
        action_output = self.view_menu_action_buttons_listeners()        

        #other box
        self.default_action_buttons()
        other_box = widgets.HBox([self.button_refresh, self.button_go_back], layout={'justify_content':'space-between'}) 
        self.default_action_buttons_listeners()

        #total display
        display(q,multi_checkbox_box, action_output, other_box)

        #get values in checkbox widget
        self.widget_multi_checkbox_new_values()