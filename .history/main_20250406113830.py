import sqlite3

def main():
    print("Hello from genshin-database!")
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

import dateditor
  
  
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
        OptionInput_CSV = ft.TextField(
            label="ペーストしたデータ",
            max_lines = 10,
            multiline=True,
            value="",
        )
        OptionOutput_PATH = ft.TextField(
            label="パス",
            value="OptionCode.dat",
        )
        OptionOutput_TEXT = ft.TextField(
            label="生成されたデータ",
            max_lines = 10,
            multiline=True,
            value="",
        )
        def make_optioncode_send(e):
            OptionOutput_TEXT.value = dateditor.make_optioncode(OptionInput_CSV.value, OptionOutput_PATH.value)
            OptionInput_CSV.value = ""
            page.update()
        
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
                OptionInput_CSV,
                ft.Text("保存先", size=30),
                OptionOutput_PATH,
                ft.Button("生成", on_click = lambda e : make_optioncode_send(e)),
                ft.Text("生成されたデータ", size=30),
                OptionOutput_TEXT,
            ],
        )

    def edit_optioncode_view():
        optiondata = ""
        def send_edit_data(e):
            global oplist
            if e.control.selected == True:
                e.control.selected = False
            else:
                e.control.selected = True
            oplist[e.control.data] = e.control.selected
            print(e.control.data , e.control.selected)
            print(oplist)
            page.update()

        def read_data(e):
            global oplist
            optiondata = dateditor.read_optioncode(editfile_PATH.value)
            alldata = dateditor.view_optioncode(optiondata)
            oplist = [True]
            opcount = 1
            rows = []
            for data in alldata:
                for i in range(16):
                    chip = ft.Chip(
                        label=ft.Text("Option" + str(opcount)),
                        selected_color= ft.Colors.AMBER,
                        data = opcount,
                        selected = (data[i] == "1"),
                        on_click=lambda e: send_edit_data(e),
                        width=300,
                    )
                    oplist.append(data[i] == "1")
                    opcount += 1
                    cells = [ft.DataCell(chip), ft.DataCell(ft.Text(value="Option" + str(i),))]
                    rows.append(ft.DataRow(cells=cells))
            data_table.rows = rows
            page.update()
        

        header = [ft.DataColumn(ft.Text("ON/OFF")), ft.DataColumn(ft.Text("OptionName"))]
        rows = []
        data_table = ft.DataTable(columns=header, rows=rows)

        editfile_PATH = ft.TextField(
            label="パス",
            value="",
        )
        ReadButton = ft.Button("読み込み", on_click = lambda e : read_data(e))
        savebotton = ft.Button("保存", on_click = lambda e : print("保存"))

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
                ft.Row(
                    controls=[
                        ft.Column(
                            controls=[data_table],
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("datファイル保存先", size=30),
                                editfile_PATH,
                                ReadButton,
                            ],
                            expand=True
                        ),
                    ],
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                ),
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
