"""
エリアデータの定義
"""
from src.game.area import Area, AreaExit, AreaConnection
from src.game.npc import NPC

def create_areas():
    """ゲーム内の全エリアを作成"""
    areas = []
    
    # 新宿 - 中央区画
    shinjuku_center = Area("shinjuku_center", "新宿 - 中央区画", 12, 12)
    shinjuku_center.walkable_tiles = set((x, y) for x in range(12) for y in range(12))
    
    # 障害物の設定（建物など）
    obstacles = [
        (2, 2), (2, 3), (3, 2), (3, 3),  # 左上の建物
        (8, 2), (8, 3), (9, 2), (9, 3),  # 右上の建物
        (5, 6), (6, 6),  # 中央の障害物
    ]
    shinjuku_center.obstacles = set(obstacles)
    
    # NPCの配置
    shinjuku_center.add_npc(NPC(
        "幻獣商人ノジョウ",
        (2, 5),
        "merchant",
        ["ようこそ、私の店へ。", "珍しい品物がありますよ。"]
    ))
    
    shinjuku_center.add_npc(NPC(
        "防具商人サクラ",
        (8, 5),
        "merchant_armor",
        ["強力な防具を揃えています。", "冒険には防御が大切ですよ。"]
    ))
    
    shinjuku_center.add_npc(NPC(
        "アイテム商人エユウキ",
        (10, 5),
        "merchant_items",
        ["回復アイテムはいかがですか？", "危険な冒険には必需品ですよ。"]
    ))
    
    shinjuku_center.add_npc(NPC(
        "魔法商人ミミト",
        (11, 5),
        "merchant_magic",
        ["魔法の道具を販売しています。", "不思議な力が宿っていますよ。"]
    ))
    
    shinjuku_center.add_npc(NPC(
        "ガイド",
        (5, 3),
        "guide",
        ["この街へようこそ！", "困ったことがあれば聞いてください。"]
    ))
    
    shinjuku_center.add_npc(NPC(
        "宿屋の主人",
        (1, 8),
        "innkeeper",
        ["お疲れ様です。", "一晩の宿泊は100ゴールドです。"]
    ))
    
    shinjuku_center.add_npc(NPC(
        "新宿へ案内人#1",
        (5, 7),
        "npc",
        ["北へ進めば住宅街です。", "南へ進めば商業街があります。"]
    ))
    
    shinjuku_center.add_npc(NPC(
        "ギルドマスター",
        (10, 8),
        "guildmaster",
        ["冒険者ギルドへようこそ。", "クエストをお受けになりますか？"]
    ))
    
    # エンカウント設定
    shinjuku_center.set_encounter({
        'rate': 0.05,
        'enemies': ['スライム', 'ゴブリン']
    })
    
    # 渋谷商業街 - ショッピングモール
    shibuya_mall = Area("shibuya_mall", "渋谷商業街 - ショッピングモール", 12, 10)
    shibuya_mall.walkable_tiles = set((x, y) for x in range(12) for y in range(10))
    
    # 障害物（店舗など）
    mall_obstacles = [
        (3, 3), (3, 4), (4, 3), (4, 4),
        (8, 3), (8, 4), (9, 3), (9, 4),
    ]
    shibuya_mall.obstacles = set(mall_obstacles)
    
    # NPCの配置
    shibuya_mall.add_npc(NPC(
        "アカリ",
        (6, 6),
        "npc",
        ["感覚を失った仲民", "..."]
    ))
    
    # エンカウント設定（ショッピングモールはエンカウントなし）
    shibuya_mall.set_encounter({
        'rate': 0.0,
        'enemies': []
    })
    
    # エリア間の接続を設定
    # 新宿中央区画 ⇔ 渋谷商業街
    shinjuku_center.add_exit(AreaExit(
        (6, 0),  # 新宿の北出口
        AreaConnection("shibuya_mall", (6, 9), "north")
    ))
    
    shibuya_mall.add_exit(AreaExit(
        (6, 9),  # 渋谷の南出口
        AreaConnection("shinjuku_center", (6, 1), "south")
    ))
    
    # 新宿中央区画から東へ
    shinjuku_center.add_exit(AreaExit(
        (11, 6),  # 東出口
        AreaConnection("shibuya_mall", (1, 5), "east")
    ))
    
    # 渋谷から西へ
    shibuya_mall.add_exit(AreaExit(
        (0, 5),  # 西出口
        AreaConnection("shinjuku_center", (10, 6), "west")
    ))
    
    areas.append(shinjuku_center)
    areas.append(shibuya_mall)
    
    return areas
