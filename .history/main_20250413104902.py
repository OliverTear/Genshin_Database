import sqlite3



import flet as ft
  
  
def main(page: ft.Page):
    page.title = "Multi-Page App"
    page.window.width = 600
    page.window.height = 1200
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
    cur.execute('SELECT * FROM ArtifactList')
    artifactlist = cur.fetchall()
    for artifact in artifactlist:
        print(artifact[1])
    
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
        elif page_name == "add_character":
            page.views.clear()
            page.views.append(add_character_view())
        elif page_name == "list_character":
            page.views.clear()
            page.views.append(list_character_view())
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
                    ft.IconButton(ft.Icons.PERSON_ADD, on_click=lambda _: navigate_to("add_character")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: navigate_to("list_character")),
                ],
            ),
            controls=[
                ft.Text("Genshin Original Database", size=40),
                ft.Column(
                [
                    ft.Row([
                        ft.Container(
                            content=ft.Text("add_artifact"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.BROWN_100,
                            width=150,
                            height=150,
                            border_radius=10,
                            on_click=lambda _: navigate_to("add_artifact"),
                        ),
                        ft.Container(
                            content=ft.Text("add_weapon"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.BROWN_100,
                            width=150,
                            height=150,
                            border_radius=10,
                            on_click=lambda _: navigate_to("add_weapon"),
                        ),
                        ft.Container(
                            content=ft.Text("add_character"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.BROWN_100,
                            width=150,
                            height=150,
                            border_radius=10,
                            on_click=lambda _: navigate_to("add_character"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                    ),
                    ft.Row([
                        ft.Container(
                            content=ft.Text("list_artifact"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.BROWN_100,
                            width=150,
                            height=150,
                            border_radius=10,
                            on_click=lambda _: navigate_to("list_artifact"),
                        ),
                        ft.Container(
                            content=ft.Text("list_weapon"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.BROWN_100,
                            width=150,
                            height=150,
                            border_radius=10,
                            on_click=lambda _: navigate_to("list_weapon"),
                        ),
                        ft.Container(
                            content=ft.Text("list_character"),
                            margin=10,
                            padding=10,
                            alignment=ft.alignment.center,
                            bgcolor=ft.Colors.BROWN_100,
                            width=150,
                            height=150,
                            border_radius=10,
                            on_click=lambda _: navigate_to("list_character"),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                    ),
                ],

                scroll=ft.ScrollMode.ALWAYS,
                expand=True
                ),
                ],
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=ft.padding.all(20),
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
                    ft.IconButton(ft.Icons.PERSON_ADD, on_click=lambda _: navigate_to("add_character")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: navigate_to("list_character")),
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
                    ft.IconButton(ft.Icons.PERSON_ADD, on_click=lambda _: navigate_to("add_character")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: navigate_to("list_character")),
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
                    ft.IconButton(ft.Icons.PERSON_ADD, on_click=lambda _: navigate_to("add_character")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: navigate_to("list_character")),
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
                    ft.IconButton(ft.Icons.PERSON_ADD, on_click=lambda _: navigate_to("add_character")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: navigate_to("list_character")),
                ],
            ),
            controls=[
                ft.Text("This is Page 4", size=30),
            ],
        )
    def add_character_view():
        return ft.View(
            "/add_character",
            appbar=ft.AppBar(
                title=ft.Text("Page 5"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ADD, on_click=lambda _: navigate_to("add_artifact")),
                    ft.IconButton(ft.Icons.PLAYLIST_ADD_OUTLINED, on_click=lambda _: navigate_to("add_weapon")),
                    ft.IconButton(ft.Icons.PERSON_ADD, on_click=lambda _: navigate_to("add_character")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: navigate_to("list_character")),
                ],
            ),
            controls=[
                ft.Text("This is Page 5", size=30),
            ],
        )
    def list_character_view():
        return ft.View(
            "/list_character",
            appbar=ft.AppBar(
                title=ft.Text("Page 6"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FORMAT_LIST_BULLETED_ADD, on_click=lambda _: navigate_to("add_artifact")),
                    ft.IconButton(ft.Icons.PLAYLIST_ADD_OUTLINED, on_click=lambda _: navigate_to("add_weapon")),
                    ft.IconButton(ft.Icons.PERSON_ADD, on_click=lambda _: navigate_to("add_character")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST, on_click=lambda _: navigate_to("list_artifact")),
                    ft.IconButton(ft.Icons.FEATURED_PLAY_LIST_OUTLINED, on_click=lambda _: navigate_to("list_weapon")),
                    ft.IconButton(ft.Icons.PERSON, on_click=lambda _: navigate_to("list_character")),
                ],
            ),
            controls=[
                ft.Text("This is Page 6", size=30),
            ],
        )
    

    page.views.append(home_view())
    page.update()
    page.on_close = lambda e: conn.close()

ft.app(target=main)