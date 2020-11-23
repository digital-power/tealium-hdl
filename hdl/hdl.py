from .menu import MainMenu, UploadMenu, ViewMenu, LoginMenu


class TealiumHDL:
    def __init__(self, account=None, profile=None, username=None, key=None):
        self.selected_items = []

        self.main_menu = MainMenu(root=self)
        self.upload_menu = UploadMenu(root=self)
        self.view_menu = ViewMenu(root=self)


        self.login_menu = LoginMenu(
            root=self,
            account=account,
            profile=profile,
            username=username,
            key=key
        )

        self.login_menu.show()
