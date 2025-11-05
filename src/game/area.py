"""
エリア管理システム
エリア間の移動とエリアデータの管理
"""

class AreaConnection:
    """エリア接続情報"""
    def __init__(self, target_area, entrance_position, direction):
        self.target_area = target_area  # 移動先エリア名
        self.entrance_position = entrance_position  # 移動先の出現位置 (x, y)
        self.direction = direction  # 移動方向 ('north', 'south', 'east', 'west')


class AreaExit:
    """エリア出口情報"""
    def __init__(self, position, connection):
        self.position = position  # 出口の位置 (x, y)
        self.connection = connection  # AreaConnection オブジェクト


class Area:
    """ゲームエリア"""
    def __init__(self, name, display_name, width, height):
        self.name = name
        self.display_name = display_name
        self.width = width
        self.height = height
        self.exits = []  # AreaExit のリスト
        self.npcs = []  # NPCのリスト
        self.encounters = []  # エンカウント設定のリスト
        self.walkable_tiles = set()  # 歩行可能なタイル位置のセット
        self.obstacles = set()  # 障害物の位置のセット
        
    def add_exit(self, exit_area):
        """エリア出口を追加"""
        self.exits.append(exit_area)
        
    def add_npc(self, npc):
        """NPCを追加"""
        self.npcs.append(npc)
        
    def set_encounter(self, encounter_data):
        """エンカウント設定を追加"""
        self.encounters.append(encounter_data)
        
    def get_exit_at_position(self, position):
        """指定位置にある出口を取得"""
        for exit_point in self.exits:
            if exit_point.position == position:
                return exit_point.connection
        return None
    
    def is_walkable(self, position):
        """指定位置が歩行可能かチェック"""
        x, y = position
        # マップの範囲外チェック
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        # 障害物チェック
        if position in self.obstacles:
            return False
        return True


class AreaManager:
    """エリア管理クラス"""
    def __init__(self):
        self.areas = {}  # エリア名: Areaオブジェクト
        self.current_area = None
        
    def add_area(self, area):
        """エリアを登録"""
        self.areas[area.name] = area
        
    def get_area(self, area_name):
        """エリアを取得"""
        return self.areas.get(area_name)
    
    def set_current_area(self, area_name):
        """現在のエリアを設定"""
        if area_name in self.areas:
            self.current_area = self.areas[area_name]
            return True
        return False
    
    def check_area_transition(self, position):
        """
        指定位置でのエリア遷移をチェック
        エリア移動ポイントを優先
        """
        if not self.current_area:
            return None
            
        # エリア移動ポイントを優先してチェック
        exit_connection = self.current_area.get_exit_at_position(position)
        if exit_connection:
            return {
                'type': 'area_transition',
                'target_area': exit_connection.target_area,
                'entrance_position': exit_connection.entrance_position,
                'direction': exit_connection.direction
            }
        
        return None
    
    def check_encounter(self, position):
        """
        エンカウントチェック（エリア移動後のみ実行される）
        """
        if not self.current_area:
            return None
            
        # エンカウント判定
        for encounter in self.current_area.encounters:
            # エンカウント率の計算などをここに実装
            # 簡易実装として、ランダムでエンカウント
            import random
            if random.random() < encounter.get('rate', 0.1):
                return {
                    'type': 'encounter',
                    'enemies': encounter.get('enemies', [])
                }
        
        return None
