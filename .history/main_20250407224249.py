import sqlite3



import flet as ft
  
  
def main(page: ft.Page):
    page.title = "Multi-Page App"
    page.theme = ft.Theme(
        color_scheme_seed=ft.colors.AMBER,
        font_family="Arial",
    )
    # genshin.dbを作成する
    # すでに存在していれば、それにアスセスする。
    dbname = "genshin.db"
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # Artifactというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute('CREATE TABLE IF NOT EXISTS Artifact(id INTEGER PRIMARY KEY AUTOINCREMENT,setname STRING, type STRING, mainstat STRING, mainstatvalue INTEGER, substat1 STRING, substat1value INTEGER, substat2 STRING, substat2value INTEGER, substat3 STRING, substat3value INTEGER, substat4 STRING, substat4value INTEGER, level INTEGER, rarity INTEGER)')

    
    def navigate_to(page_name):
        if page_name == "home":
            page.views.clear()
            page.views.append(home_view())
        elif page_name == "add_artifact":
            page.views.clear()
            page.views.append(add_artifact_view())
        elif page_name == "add_weapon":
            page.views.clear()
            page.views.append(add_weapon_view())
        elif page_name == "list_artifact":
            page.views.clear()
            page.views.append(list_artifact_view())
        elif page_name == "list_weapon":
            page.views.clear()
            page.views.append(list_weapon_view())
        page.update()

    def home_view():
        return ft.View(
            "/",
            appbar=ft.AppBar(
                title=ft.Text("Home"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ADD, on_click=lambda _: navigate_to("add_artifact")),
                    ft.IconButton(ft.Icons.PLAYLIST_ADD_OUTLINED, on_click=lambda _: navigate_to("add_weapon")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                ],
            ),
            controls=[
                ft.Text("Welcome to the Home Page!", size=30),
                ft.Column(
                [
                    ft.ElevatedButton(
                        "Add Artifact",
                        on_click=lambda _: navigate_to("add_artifact"),
                        icon=ft.icons.FORMAT_LIST_BULLETED_ADD,
                        width=600,
                        height=250,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            color=ft.colors.AMBER,
                            text_style=ft.TextStyle(
                                color=ft.colors.WHITE,
                                size=50,
                            ),
                            icon_size=50,
                        ),
                    ),
                    ft.ElevatedButton(
                        "Add Weapon",
                        on_click=lambda _: navigate_to("add_weapon"),
                        icon=ft.icons.PLAYLIST_ADD_OUTLINED,
                        width=600,
                        height=250,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            color=ft.colors.AMBER,
                            text_style=ft.TextStyle(
                                color=ft.colors.WHITE,
                                size=50,
                            ),
                            icon_size=50,
                        ),
                    ),
                    ft.ElevatedButton(
                        "List Artifact",
                        on_click=lambda _: navigate_to("list_artifact"),
                        icon=ft.icons.FEATURED_PLAY_LIST,
                        width=600,
                        height=250,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            color=ft.colors.AMBER,
                            text_style=ft.TextStyle(
                                color=ft.colors.WHITE,
                                size=50,
                            ),
                            icon_size=50,
                        ),
                    ),
                    ft.ElevatedButton(
                        "List Weapon",
                        on_click=lambda _: navigate_to("list_weapon"),
                        icon=ft.icons.FEATURED_PLAY_LIST_OUTLINED,
                        width=600,
                        height=250,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=20),
                            color=ft.colors.AMBER,
                            text_style=ft.TextStyle(
                                color=ft.colors.WHITE,
                                size=50,
                            ),
                            icon_size=50,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                scroll=ft.ScrollMode.ALWAYS,
                ),
            ],
        )
    
    def add_artifact_view():
        
        return ft.View(
            "/add_artifact",
            appbar=ft.AppBar(
                title=ft.Text("聖遺物を追加します"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ADD, on_click=lambda _: navigate_to("add_artifact")),
                    ft.IconButton(ft.Icons.PLAYLIST_ADD_OUTLINED, on_click=lambda _: navigate_to("add_weapon")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                ],
            ),
            controls=[
                ft.Text("ああああ", size=30),
            ],
        )

    def add_weapon_view():
        return ft.View(
            "/add_weapon",
            appbar=ft.AppBar(
                title=ft.Text("Page 2"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ADD, on_click=lambda _: navigate_to("add_artifact")),
                    ft.IconButton(ft.Icons.PLAYLIST_ADD_OUTLINED, on_click=lambda _: navigate_to("add_weapon")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                ],
            ),
            controls=[
                ft.Text("This is Page 2", size=30),
            ],
        )

    def list_artifact_view():
        return ft.View(
            "/list_artifact",
            appbar=ft.AppBar(
                title=ft.Text("Page 3"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ADD, on_click=lambda _: navigate_to("add_artifact")),
                    ft.IconButton(ft.Icons.PLAYLIST_ADD_OUTLINED, on_click=lambda _: navigate_to("add_weapon")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                ],
            ),
            controls=[
                ft.Text("This is Page 3", size=30),
            ],
        )

    def list_weapon_view():
        return ft.View(
            "/list_weapon",
            appbar=ft.AppBar(
                title=ft.Text("Page 4"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ADD, on_click=lambda _: navigate_to("add_artifact")),
                    ft.IconButton(ft.Icons.PLAYLIST_ADD_OUTLINED, on_click=lambda _: navigate_to("add_weapon")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                ],
            ),
            controls=[
                ft.Text("This is Page 4", size=30),
            ],
        )

    page.views.append(home_view())
    page.update()
    page.on_close = lambda e: conn.close()

ft.app(target=main)