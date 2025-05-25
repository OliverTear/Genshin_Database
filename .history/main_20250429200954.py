import sqlite3
import json
from urllib.request import Request, urlopen, urlretrieve, install_opener, build_opener
from bs4 import BeautifulSoup
import ssl
import flet as ft
import types

IntList = list
sqlite3.register_adapter(IntList, lambda l: ';'.join([str(i) for i in l]))
sqlite3.register_converter("IntList", lambda s: [int(i) for i in s.split(';')])






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
    cur.execute('CREATE TABLE IF NOT EXISTS Character(id INTEGER PRIMARY KEY AUTOINCREMENT,name STRING, level INTEGER, weapon STRING, artifactID1 INTEGER, artifactID2 INTEGER, artifactID3 INTEGER, artifactID4 INTEGER, artufactID5)')
    cur.execute('SELECT * FROM ArtifactList')
    artifactlist = cur.fetchall()
    cur.execute('SELECT * FROM CharacterList')
    characterlist = cur.fetchall()
    cur.execute('SELECT * FROM WeaponList')
    weaponlist = cur.fetchall()
    characterdropdownlist = []
    for character in characterlist:
        characterdropdownlist.append(ft.dropdown.Option(character[1]))



    def read_bs(url):
        ssl._create_default_https_context = ssl._create_unverified_context
        headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"
        }
        request = Request(url, headers=headers)
        html = urlopen(request).read()
        return BeautifulSoup(html, 'html.parser')


    def read_information(e):
        def close_dlg(e):
            Dialog.open = False
            page.update()
        Dialog = ft.AlertDialog(
            title=ft.Text("更新中..."),
            modal=True,
            actions=[
                ft.TextButton("閉じる",on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(Dialog)
        page.update()

        bsObj = read_bs("https://wikiwiki.jp/genshinwiki/%E3%82%AD%E3%83%A3%E3%83%A9%E3%82%AF%E3%82%BF%E3%83%BC%E4%B8%80%E8%A6%A7")
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
        if len(sqlitelist) != len(characterlist):
            cur.execute("DELETE FROM CharacterList")
            for i in sqlitelist:
                cur.execute(i)
            conn.commit()
        weapontype = ["片手剣", "両手剣", "長柄武器", "法器", "弓"]
        sqlitelist = []
        bsObj = read_bs("https://wikiwiki.jp/genshinwiki/%E6%AD%A6%E5%99%A8/%E4%B8%80%E8%A6%A7")
        for table in bsObj.findAll("table"):
            for tab in table:
                rows = tab.find_all("tr")
                Allrows = []
                for row in rows:
                    csvRow = []
                    for cell in row.findAll(['td', 'th']):
                        csvRow.append(cell.get_text())
                    Allrows.append(csvRow)
            # print(Allrows)
            for row in Allrows:
                if row[0] == "☆5":
                    row[0] = "5"
                elif row[0] == "☆4":
                    row[0] = "4"
                elif row[0] == "☆3":
                    row[0] = "3"
                elif row[0] == "☆2":
                    row[0] = "2"
                elif row[0] == "☆1":
                    row[0] = "1"
                if row[6] == "-":
                    row[6] = "FALSE"
                else:
                    row[6] = "TRUE"
                sqlitelist.append(f'INSERT INTO WeaponList(type, rarity, name, BASEATK, SubEffect, SubEffectValue, Support, Get) VALUES("{weapontype[0]}", {row[0]}, "{row[2]}", {row[3]}, "{row[4]}", "{row[5]}", {row[6]}, "{row[7]}")')
            weapontype.pop(0)
        if len(sqlitelist) != len(weaponlist):
            cur.execute("DELETE FROM WeaponList")
            for i in sqlitelist:
                cur.execute(i)
            conn.commit()
        Dialog.open = False
        page.update()
        return sqlitelist
    
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
                    ft.IconButton(ft.Icons.REFRESH_SHARP, on_click = read_information),
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
                    ft.IconButton(ft.Icons.REFRESH_SHARP, on_click = read_information),
                ],
            ),
            controls=[
                ft.Text("ああああ", size=30),
            ],
        )

    def add_weapon_view():

        def get_rarity(e):
            global rarity
            if e == None:
                rarity = None
            else:
                rarity = e.control.value
        def get_kind(e):
            global kind
            if e == None:
                kind = None
            else:
                kind = e.control.value
        def close_dlg(e):
            Dialog.open = False
            page.update()
        def open_dlg(e):
            Dialog.title = ft.Text("武器の詳細検索")
            radiokinds = ft.RadioGroup(
                content=ft.Column(
                    [
                        ft.Radio(value="片手剣", label="片手剣"),
                        ft.Radio(value="両手剣", label="両手剣"),
                        ft.Radio(value="長柄武器", label="長柄武器"),
                        ft.Radio(value="法器", label="法器"),
                        ft.Radio(value="弓", label="弓"),
                        ft.Radio(value="全て", label="全て"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                ),
                on_change= get_kind,
                value=kind,
            )
            radiorarity = ft.RadioGroup(
                content=ft.Column(
                    [
                        ft.Radio(value="☆5", label="☆5"),
                        ft.Radio(value="☆4", label="☆4"),
                        ft.Radio(value="☆3", label="☆3"),
                        ft.Radio(value="☆2", label="☆2"),
                        ft.Radio(value="☆1", label="☆1"),
                        ft.Radio(value="全て", label="全て"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                ),
                on_change=get_rarity,
                value=rarity
            )
            Dialog.actions = [
                ft.Row(
                    [
                        
                    ft.Row(
                        [
                            ft.Text("武器の種類"),
                            radiokinds
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Row(
                        [
                            ft.Text("レアリティ"),
                            radiorarity
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ],
                ),
                ft.TextButton("閉じる",on_click=close_dlg),
            ]
            page.open(Dialog)
            page.update()
        
        def search(e):
            global kind, rarity
            def decide_weapon(e):
                searchbar.value = e.control.data[2]
                Dialog.open = False
                page.update()

            print(kind, rarity, searchbar.value)
            if kind == None and rarity == None and searchbar.value == "":
                page.open(Dialog)
                Dialog.title=ft.Text("エラー")
                Dialog.content = ft.Text("検索条件を指定してください")
                page.update()
            else:
                if kind == None:
                    kind = ""
                else:
                    if rarity == None and (searchbar.value == None or not searchbar.value):
                        kindsql = "type LIKE '"+kind+"'"
                    else:
                        kindsql = "type LIKE '"+kind+"' AND "
                if rarity == None:
                    rarity = ""
                else:
                    if searchbar.value == None or not searchbar.value:
                        raritysql = "rarity LIKE '"+rarity+"'"
                    else:
                        raritysql = "rarity LIKE '"+rarity+"' AND "
                if searchbar.value == None or not searchbar.value:
                    searchbarvaluesql = ""
                else:
                    searchbarvaluesql = "name LIKE '"+searchbar.value+"'"
                print('SELECT * FROM WeaponList WHERE '+kindsql+raritysql+searchbarvaluesql)
                cur.execute('SELECT * FROM WeaponList WHERE '+kindsql+raritysql+searchbarvaluesql)
                weaponresult = cur.fetchall()
                if weaponresult == []:
                    page.open(Dialog)
                    Dialog.title=ft.Text("エラー")
                    Dialog.actions = ft.Text("該当する武器がありません")
                    page.update()
                elif len(weaponresult) == 1:
                    searchbar.value = data[0][2]
                else:
                    rows = []
                    for data in weaponresult:
                        data = list(data)
                        for i in range(1, len(data)):
                            if type(data[i]) == types.NoneType:
                                data[i] = "0"
                        print(data)
                        checkbutton = ft.IconButton(
                            icon=ft.Icons.CHECK,
                            data = data,
                            on_click=decide_weapon,
                        )
                        cells = [ft.DataCell(ft.Text(data[1])),ft.DataCell(ft.Text(data[2])),ft.DataCell(ft.Text(data[3])), ft.DataCell(checkbutton)]
                        rows.append(ft.DataRow(cells=cells))
                    header = [ft.DataColumn(ft.Text("武器種")), ft.DataColumn(ft.Text("レアリティ")), ft.DataColumn(ft.Text("名前")), ft.DataColumn(ft.Text("決定"))]
                    data_table = ft.DataTable(columns=header, rows=rows)
                    Dialog.actions =[
                        # ft.Text("該当する武器が"+str(len(weaponresult))+"件見つかりました"),
                        ft.Column(
                            controls=[data_table],
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True
                        ),
                    ]
                    Dialog.title = ft.Column(
                            controls=[data_table],
                            scroll=ft.ScrollMode.ALWAYS,
                            expand=True
                        ),
                    Dialog.scrollable = True
                    page.open(Dialog)
                        

        get_kind(None)
        get_rarity(None)
        Dialog = ft.AlertDialog(
            title=ft.Text("エラー"),
            modal=True,
            actions=[
                ft.TextButton("閉じる",on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        searchbar = ft.TextField(
            label="武器を検索",
            border_radius=10,
            border_color=ft.colors.AMBER,
            border_width=2,
            width=200,
        )
        detailsearch = ft.IconButton(
            icon=ft.Icons.FILTER_ALT,
            on_click=open_dlg,
        )
        search = ft.IconButton(
            icon=ft.Icons.SEARCH,
            on_click=search,
        )


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
                    ft.IconButton(ft.Icons.REFRESH_SHARP, on_click = read_information),
                ],
            ),
            controls=[
                ft.Text("This is Page 2", size=30),
                ft.Row(
                    [
                        searchbar,
                        detailsearch,
                        search
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                ),
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
                    ft.IconButton(ft.Icons.REFRESH_SHARP, on_click = read_information),
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
                    ft.IconButton(ft.Icons.REFRESH_SHARP, on_click = read_information),
                ],
            ),
            controls=[
                ft.Text("This is Page 4", size=30),
            ],
        )
    
    def add_character_view():
        def register_character(e):
            def close_dlg(e):
                Dialog.open = False
                page.update()
            Dialog = ft.AlertDialog(
                title=ft.Text("エラー"),
                modal=True,
                actions=[
                    ft.TextButton("閉じる",on_click=close_dlg),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            charactername = characterdropdown.value
            levelvalue = level.value

            if charactername is None:
                page.open(Dialog)
                Dialog.title=ft.Text("エラー")
                Dialog.content = ft.Text("キャラクターを選択してください")
                page.update()
            elif levelvalue == "":
                page.open(Dialog)
                Dialog.title=ft.Text("エラー")
                Dialog.content = ft.Text("レベルを入力してください")
                page.update()
            else:
                cur.execute("select name from character where name LIKE '"+charactername+"';")
                if type(cur.fetchone()) == types.NoneType:
                    # キャラクターを登録する処理
                    cur.execute('INSERT INTO Character(name, level) VALUES(?, ?)', (characterdropdown.value, level.value))
                    conn.commit()
                    page.open(Dialog)
                    Dialog.title=ft.Text("登録完了")
                    Dialog.content = ft.Text("キャラクターを登録しました")
                    page.update()
                else:
                    page.open(Dialog)
                    Dialog.title=ft.Text("エラー")
                    Dialog.content = ft.Text("すでに登録されています")
                    page.update()
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
                    ft.IconButton(ft.Icons.REFRESH_SHARP, on_click = read_information),
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
        def close_dlg(e):
                Dialog.open = False
                Dialog.actions = [ft.TextButton("閉じる",on_click=close_dlg),]
                page.update()
        Dialog = ft.AlertDialog(
            modal=True,
            actions=[
                ft.TextButton("閉じる",on_click=close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        def delete_character(e):
            Dialog.title = ft.Text("キャラクターを削除します")
            Dialog.actions = [
                ft.TextButton("はい", on_click=delete_character_yes,data = e.control.data,),
                ft.TextButton("いいえ", on_click=close_dlg),
            ]
            page.open(Dialog)
            page.update()
        
        def delete_character_yes(e):
            Dialog.title = ft.Text("キャラクターを削除しました")
            Dialog.actions = [ft.TextButton("閉じる",on_click=close_dlg),]
            page.update()
            cur.execute('DELETE FROM Character WHERE id = ?', (e.control.data[0],))
            conn.commit()
            page.update()
        
        def edit_character(e):
            def edit_character_yes(e):
                print(e.control.data)
                Dialog.title = ft.Text("キャラクターを編集しました")
                Dialog.actions = [ft.TextButton("閉じる",on_click=close_dlg),]
                cur.execute('UPDATE Character SET level = ? WHERE id = ?', (editlevel.value, e.control.data[0],))
                conn.commit()
                page.update()
            Dialog.title = ft.Text("キャラクターを編集します")
            editlevel = ft.TextField(
                label="レベル",
                border_radius=10,
                border_color=ft.colors.AMBER,
                border_width=2,
                width=50,
                value = str(e.control.data[2]),
            )
            Dialog.actions = [
                ft.Row(
                    [
                        ft.Text("Level"),
                        editlevel
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Column([
                ft.TextButton("変更する", on_click=edit_character_yes,data = e.control.data),
                ft.TextButton("キャンセル", on_click=close_dlg),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                ),

            ]
            page.open(Dialog)
            page.update()
        
        updatebutton = ft.ElevatedButton(
            text="更新",
            icon=ft.Icons.REFRESH_SHARP,
            on_click=lambda _: navigate_to("list_character"),
        )

        rows = []
        cur.execute('SELECT * FROM Character')
        characterdata = cur.fetchall()
        for data in characterdata:
            data = list(data)
            for i in range(1, len(data)):
                if type(data[i]) == types.NoneType:
                    data[i] = "0"
            print(data)
            editbutton = ft.IconButton(
                icon=ft.Icons.EDIT_SHARP,
                on_click=edit_character,
                data = data
                
            )
            deletebutton = ft.IconButton(
                icon=ft.Icons.DELETE_SHARP,
                on_click=delete_character,
                data = data
            )
            cells = [ft.DataCell(ft.Text(data[1])),ft.DataCell(ft.Text(data[2])),ft.DataCell(ft.Text(data[3])),ft.DataCell(ft.Text(data[4])),ft.DataCell(editbutton), ft.DataCell(deletebutton)]
            rows.append(ft.DataRow(cells=cells))
        header = [ft.DataColumn(ft.Text("キャラクター")), ft.DataColumn(ft.Text("レベル")), ft.DataColumn(ft.Text("武器")), ft.DataColumn(ft.Text("聖遺物")), ft.DataColumn(ft.Text("編集")), ft.DataColumn(ft.Text("削除"))]
        data_table = ft.DataTable(columns=header, rows=rows)
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
                    ft.IconButton(ft.Icons.REFRESH_SHARP, on_click = read_information),
                ],
            ),
            controls=[
                ft.Text("CharacterList", size=30),
                updatebutton,
                ft.Column(
                    controls=[data_table],
                    scroll=ft.ScrollMode.ALWAYS,
                    expand=True
                ),
            ],
        )
    

    page.views.append(home_view())
    page.update()
    page.on_close = lambda e: conn.close()

ft.app(target=main)