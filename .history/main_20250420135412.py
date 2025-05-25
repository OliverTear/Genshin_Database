import sqlite3
import json
from urllib.request import Request, urlopen, urlretrieve, install_opener, build_opener
from bs4 import BeautifulSoup
import ssl
import flet as ft

IntList = list
sqlite3.register_adapter(IntList, lambda l: ';'.join([str(i) for i in l]))
sqlite3.register_converter("IntList", lambda s: [int(i) for i in s.split(';')])

def read_characterlist():
    ssl._create_default_https_context = ssl._create_unverified_context
    # URLの指定

    url = "https://wikiwiki.jp/genshinwiki/%E3%82%AD%E3%83%A3%E3%83%A9%E3%82%AF%E3%82%BF%E3%83%BC%E4%B8%80%E8%A6%A7"
    headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
    }
    request = Request(url, headers=headers)
    html = urlopen(request).read()
    bsObj = BeautifulSoup(html, 'html.parser')
    # テーブルを指定
    table = bsObj.findAll("table")[0]
    for tab in table:
        rows = tab.find_all("tr")
        Allrows = []
        for row in rows:
            csvRow = []
            for cell in row.findAll(['td', 'th']):
                csvRow.append(cell.get_text())
            Allrows.append(csvRow)
    sqlitelist = []
    for row in Allrows:
        if row[3] == "☆5":
            row[3] = "5"
        elif row[3] == "☆4":
            row[3] = "4"
        if row[15] == "―":
            row[15] = "0"
        row[10] = row[10].replace(",", "")
        sqlitelist.append(f'INSERT INTO CharacterList(kana, name, rarity, element, weapon, sex, birthday, country, region, HP, ATK, DEF, OriginalValue, CollectionValue, ElementalEnergy, Version) VALUES("{row[1]}", "{row[2]}", {row[3]}, "{row[4]}", "{row[5]}", "{row[6]}", "{row[7]}", "{row[8]}", "{row[9]}", {row[10]}, {row[11]}, {row[12]}, "{row[13]}", "{row[14]}", {row[15]}, {row[16]})')
    return sqlitelist
    # rows = table.findAll("tr")
    # print(rows)  




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
    cur.execute('CREATE TABLE IF NOT EXISTS Character(id INTEGER PRIMARY KEY AUTOINCREMENT,name STRING, level INTEGER, weapon STRING, artifactID1 INTEGER, artifactID2 INTEGER, artifactID3 INTEGER, artifactID4 INTEGER)')
    cur.execute('SELECT * FROM ArtifactList')
    artifactlist = cur.fetchall()
    cur.execute('SELECT * FROM CharacterList')
    characterlist = cur.fetchall()
    insert_list =  read_characterlist()
    if len(insert_list) != len(characterlist):
        for i in insert_list:
            cur.execute(i)
        conn.commit()
    cur.execute('SELECT * FROM CharacterList')
    characterlist = cur.fetchall()
    characterdropdownlist = []
    for character in characterlist:
        characterdropdownlist.append(ft.dropdown.Option(character[1]))
    
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
        def register_character(e):
            def close_dlg(e):
                error.open = False
                page.update()
            error = ft.AlertDialog(
                content=ft.Text("キャラクターを選択してください"),
                open=True,
                actions=[ft.TextButton("閉じる",on_click=close_dlg),],
            )
            print(characterdropdown.value)
            print(level.value)
            if characterdropdown.value is None:
                error.open = True
                page.update()
                return
        characterdropdown = ft.Dropdown(
            label="キャラクターを選択してください",
            options=characterdropdownlist,
            value=None,
            border_radius=10,
            border_color=ft.colors.AMBER,
            border_width=2,
            width=200,
        )
        level = ft.TextField(
            label="レベル",
            border_radius=10,
            border_color=ft.colors.AMBER,
            border_width=2,
            width=50,
        )
        RegisterButton = ft.ElevatedButton(
            text="登録",
            bgcolor=ft.colors.BLUE_ACCENT_400,
            color=ft.colors.WHITE,
            on_click=register_character,
            width=100,
            height=50,
        )

        # 聖遺物と武器は後ほど追加
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
                ft.Column(
                    [
                    ft.Row(
                        [
                            characterdropdown,
                            level,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True
                    ),
                    ft.Row(
                        [
                            RegisterButton,
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