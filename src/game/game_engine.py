"""
ゲームエンジンのコアシステム
エリア移動とエンカウントの制御
"""
from src.game.area import AreaManager
from src.game.player import Player
from src.data.areas_data import create_areas

class GameEngine:
    """ゲームエンジン"""
    def __init__(self):
        self.area_manager = AreaManager()
        self.player = Player()
        self.game_state = 'field'  # 'field', 'battle', 'menu', 'dialogue'
        self.transition_data = None  # エリア遷移データ
        self.is_transitioning = False  # 遷移中フラグ
        
        # エリアデータをロード
        self._load_areas()
        
    def _load_areas(self):
        """エリアデータをロード"""
        areas = create_areas()
        for area in areas:
            self.area_manager.add_area(area)
        
        # 初期エリアを設定
        self.area_manager.set_current_area("shinjuku_center")
        self.player.set_position(6, 5)
    
    def handle_player_move(self, dx, dy):
        """
        プレイヤーの移動を処理
        エリア移動ポイントを優先してチェック
        """
        if self.game_state != 'field' or self.is_transitioning:
            return {'success': False, 'reason': 'not_in_field'}
        
        # 移動先の位置を計算
        current_pos = self.player.get_position()
        new_x = current_pos[0] + dx
        new_y = current_pos[1] + dy
        new_position = (new_x, new_y)
        
        # 移動可能かチェック
        current_area = self.area_manager.current_area
        if not current_area.is_walkable(new_position):
            return {'success': False, 'reason': 'not_walkable'}
        
        # プレイヤーを移動
        self.player.move(dx, dy)
        
        # エリア移動ポイントを優先してチェック
        transition = self.area_manager.check_area_transition(new_position)
        if transition:
            return self._handle_area_transition(transition)
        
        # エリア移動がない場合、エンカウントチェック
        encounter = self.area_manager.check_encounter(new_position)
        if encounter:
            return self._handle_encounter(encounter)
        
        return {'success': True, 'action': 'move'}
    
    def _handle_area_transition(self, transition):
        """
        エリア遷移を処理
        視覚的な連携のためのデータを返す
        """
        self.is_transitioning = True
        self.transition_data = transition
        
        return {
            'success': True,
            'action': 'area_transition',
            'transition': transition
        }
    
    def execute_area_transition(self):
        """
        エリア遷移を実行
        アニメーション後に呼び出される
        """
        if not self.transition_data:
            return False
        
        # 新しいエリアに移動
        target_area = self.transition_data['target_area']
        entrance_pos = self.transition_data['entrance_position']
        
        if self.area_manager.set_current_area(target_area):
            self.player.set_position(entrance_pos[0], entrance_pos[1])
            self.is_transitioning = False
            self.transition_data = None
            return True
        
        return False
    
    def _handle_encounter(self, encounter):
        """
        エンカウントを処理
        """
        self.game_state = 'battle'
        return {
            'success': True,
            'action': 'encounter',
            'encounter': encounter
        }
    
    def check_npc_interaction(self):
        """
        プレイヤーの前方のNPCをチェック
        """
        if self.game_state != 'field':
            return None
        
        # プレイヤーの向いている方向の座標を計算
        pos = self.player.get_position()
        direction = self.player.direction
        
        target_pos = pos
        if direction == 'up':
            target_pos = (pos[0], pos[1] - 1)
        elif direction == 'down':
            target_pos = (pos[0], pos[1] + 1)
        elif direction == 'left':
            target_pos = (pos[0] - 1, pos[1])
        elif direction == 'right':
            target_pos = (pos[0] + 1, pos[1])
        
        # NPCを検索
        current_area = self.area_manager.current_area
        for npc in current_area.npcs:
            if npc.position == target_pos:
                return npc.interact()
        
        return None
    
    def get_current_state(self):
        """現在のゲーム状態を取得"""
        return {
            'game_state': self.game_state,
            'player': self.player,
            'current_area': self.area_manager.current_area,
            'is_transitioning': self.is_transitioning,
            'transition_data': self.transition_data
        }
