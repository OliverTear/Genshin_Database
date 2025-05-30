import sqlite3
dbname = 'genshin.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute('Drop table CharacterList')
cur.execute('CREATE TABLE IF NOT EXISTS CharacterList(kana STRING, name STRING, rarity INT, element STRING, weapon STRING, sex STRING, birthday STRING, country STRING, region STRING, HP INT, ATK INT, DEF INT, OriginalValue STRING, CollectionValue STRING, ElementalEnergy INT, Version FLOAT)')
# artifactlist = ["氷風を彷徨う勇士", "雷を鎮める尊者", "烈火を渡る賢者", "愛される少女", "剣闘士のﾌｨﾅｰﾚ", "翠緑の影","大地を流浪する楽団", "雷のような怒り", "燃え盛る炎の魔女", "旧貴族のしつけ", "血染めの騎士道", "悠久の磐岩","逆飛びの流星", "沈淪の心", "千岩牢固", "蒼白の炎", "追憶のしめ縄", "絶縁の旗印","華館夢醒形骸記", "海染硨磲", "辰砂往生録", "来歆の余響", "深林の記憶", "金ﾒｯｷの夢","砂上の楼閣の史話", "楽園の絶花", "水仙の夢", "花海甘露の光", "ﾌｧﾝﾄﾑﾊﾝﾀｰ", "黄金の劇団","残響の森で囁かれる夜話", "在りし日の歌", "諧律奇想の断章", "遂げられなかった想い", "灰燼の都に立つ英雄の絵巻", "黒曜の秘典","深廊の終曲", "長き夜の誓い", "", "", "", "","旅人の心", "奇跡", "狂戦士", "教官", "亡命者", "守護の心","勇士の心", "武人", "博徒", "学者", "○祭りの人"]
# characterlist = ["主人公", "アーロイ", "ジン", "アルベド", "ディルック", "エウルア", "クレー", "モナ", "ウェンティ", "刻晴", "七七", "胡桃", "魈", "申鶴", "鍾離", "閑雲", "白朮", "夜蘭", "甘雨", "神里綾人", "楓原万葉", "神里綾華", "千織", "荒瀧一斗", "雷電将軍", "珊瑚宮心海", "夢見月瑞希", "八重神子", "宵宮", "ニィロウ", "アルハイゼン", "ディシア", "セノ", "放浪者", "ナヒーダ", "ティナリ", "フリーナ", "クロリンデ", "ナヴィア", "エミリエ", "ヌヴィレット", "リオセスリ", "リネ", "シグウィン", "シロネン", "マーヴィカ", "キィニチ", "ムアラニ", "ヴァレサ", "シトラリ", "チャスカ", "アルレッキーノ", "タルタリヤ", "ベネット", "ガイア", "レザー", "ノエル", "ロサリア", "ミカ", "バーバラ", "スクロース", "リサ", "アンバー", "フィッシュル", "ディオナ", "行秋", "辛炎", "嘉明", "北斗", "重雲", "香菱", "ヨォーヨ", "雲菫", "煙緋", "藍硯", "凝光", "久岐忍", "綺良々", "早柚", "トーマ", "鹿野院平蔵", "九条裟羅", "ゴロー", "レイラ", "ドリー", "カーヴェ", "キャンディス", "ファルザン", "セトス", "コレイ", "リネット", "フレミネ", "シュヴルーズ", "シャルロット", "イアンサ", "カチーナ", "オロルン"]
# for i in characterlist:
#     cur.execute('INSERT INTO CharacterList(name) values("' + i + '")')
# conn.commit()

cur.execute('CREATE TABLE IF NOT EXISTS WeaponList(type STRING, rarity INT, name STRING, BASEATK INT, SubEffect STRING, SubEffectValue STRING, ElementalEnergy INT, Version FLOAT)')

cur.close()
conn.close()

