import sqlite3

def main():

    # genshin.dbを作成する
    # すでに存在していれば、それにアスセスする。
    dbname = "genshin.db"
    conn = sqlite3.connect(dbname)
    # sqliteを操作するカーソルオブジェクトを作成
    cur = conn.cursor()

    # Artifactというtableを作成してみる
    # 大文字部はSQL文。小文字でも問題ない。
    cur.execute('CREATE TABLE Artifact(id INTEGER PRIMARY KEY AUTOINCREMENT,setname STRING, type STRING, mainstat STRING, mainstatvalue INTEGER, substat1 STRING, substat1value INTEGER, substat2 STRING, substat2value INTEGER, substat3 STRING, substat3value INTEGER, substat4 STRING, substat4value INTEGER, level INTEGER, rarity INTEGER)')

    conn.close()

import flet as ft
  
  
def main(page: ft.Page):
    page.title = "Multi-Page App"

    def navigate_to(page_name):


        if page_name == "home":
            page.views.clear()
            page.views.append(home_view())
        elif page_name == "make_optioncode":
            page.views.clear()
            page.views.append(make_optioncode_view())
        elif page_name == "edit_optioncode":
            page.views.clear()
            page.views.append(edit_optioncode_view())
        elif page_name == "page3":
            page.views.clear()
            page.views.append(page3_view())
        elif page_name == "page4":
            page.views.clear()
            page.views.append(page4_view())
        page.update()

    def home_view():
        return ft.View(
            "/",
            appbar=ft.AppBar(
                title=ft.Text("Home"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FIBER_NEW, on_click=lambda _: navigate_to("make_optioncode")),
                    ft.IconButton(ft.Icons.EDIT_NOTE, on_click=lambda _: navigate_to("edit_optioncode")),
                    ft.IconButton(ft.Icons.LOOKS_3, on_click=lambda _: navigate_to("page3")),
                    ft.IconButton(ft.Icons.LOOKS_4, on_click=lambda _: navigate_to("page4")),
                ],
            ),
            controls=[
                ft.Text("Welcome to the Home Page!", size=30),
            ],
        )
    
    def make_optioncode_view():
        
        return ft.View(
            "/make_optioncode",
            appbar=ft.AppBar(
                title=ft.Text("OptionCode.dat Maker"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FIBER_NEW, on_click=lambda _: navigate_to("make_optioncode")),
                    ft.IconButton(ft.Icons.EDIT_NOTE, on_click=lambda _: navigate_to("edit_optioncode")),
                    ft.IconButton(ft.Icons.LOOKS_3, on_click=lambda _: navigate_to("page3")),
                    ft.IconButton(ft.Icons.LOOKS_4, on_click=lambda _: navigate_to("page4")),
                ],
            ),
            controls=[
                ft.Text("ペーストしたデータを元にOptionCode.datを生成します", size=30),
            ],
        )

    def edit_optioncode_view():
        return ft.View(
            "/edit_optioncode",
            appbar=ft.AppBar(
                title=ft.Text("Page 2"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FIBER_NEW, on_click=lambda _: navigate_to("make_optioncode")),
                    ft.IconButton(ft.Icons.EDIT_NOTE, on_click=lambda _: navigate_to("edit_optioncode")),
                    ft.IconButton(ft.Icons.LOOKS_3, on_click=lambda _: navigate_to("page3")),
                    ft.IconButton(ft.Icons.LOOKS_4, on_click=lambda _: navigate_to("page4")),
                ],
            ),
            controls=[
                ft.Text("This is Page 2", size=30),
            ],
        )

    def page3_view():
        return ft.View(
            "/page3",
            appbar=ft.AppBar(
                title=ft.Text("Page 3"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FIBER_NEW, on_click=lambda _: navigate_to("make_optioncode")),
                    ft.IconButton(ft.Icons.EDIT_NOTE, on_click=lambda _: navigate_to("edit_optioncode")),
                    ft.IconButton(ft.Icons.LOOKS_3, on_click=lambda _: navigate_to("page3")),
                    ft.IconButton(ft.Icons.LOOKS_4, on_click=lambda _: navigate_to("page4")),
                ],
            ),
            controls=[
                ft.Text("This is Page 3", size=30),
            ],
        )

    def page4_view():
        return ft.View(
            "/page4",
            appbar=ft.AppBar(
                title=ft.Text("Page 4"),
                actions=[
                    ft.IconButton(ft.Icons.HOME, on_click=lambda _: navigate_to("home")),
                    ft.IconButton(ft.Icons.FIBER_NEW, on_click=lambda _: navigate_to("make_optioncode")),
                    ft.IconButton(ft.Icons.EDIT_NOTE, on_click=lambda _: navigate_to("edit_optioncode")),
                    ft.IconButton(ft.Icons.LOOKS_3, on_click=lambda _: navigate_to("page3")),
                    ft.IconButton(ft.Icons.LOOKS_4, on_click=lambda _: navigate_to("page4")),
                ],
            ),
            controls=[
                ft.Text("This is Page 4", size=30),
            ],
        )

    page.views.append(home_view())
    page.update()

ft.app(target=main)




if __name__ == "__main__":
    main()
