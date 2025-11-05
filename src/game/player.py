"""
プレイヤー管理システム
"""

class Player:
    """プレイヤークラス"""
    def __init__(self, name="プレイヤー"):
        self.name = name
        self.level = 1
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.exp = 15
        self.gold = 1020
        self.position = [5, 5]  # [x, y]
        self.direction = 'down'  # 'up', 'down', 'left', 'right'
        self.inventory = []
        
    def move(self, dx, dy):
        """プレイヤーを移動"""
        self.position[0] += dx
        self.position[1] += dy
        
        # 向きを更新
        if dx > 0:
            self.direction = 'right'
        elif dx < 0:
            self.direction = 'left'
        elif dy > 0:
            self.direction = 'down'
        elif dy < 0:
            self.direction = 'up'
    
    def set_position(self, x, y):
        """位置を設定"""
        self.position = [x, y]
    
    def get_position(self):
        """位置を取得"""
        return tuple(self.position)
    
    def take_damage(self, damage):
        """ダメージを受ける"""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0
    
    def heal(self, amount):
        """回復"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def use_mp(self, amount):
        """MPを使用"""
        if self.mp >= amount:
            self.mp -= amount
            return True
        return False
    
    def restore_mp(self, amount):
        """MP回復"""
        self.mp = min(self.max_mp, self.mp + amount)
    
    def gain_exp(self, exp):
        """経験値を獲得"""
        self.exp += exp
        # レベルアップ処理（簡易版）
        while self.exp >= 100:
            self.level_up()
    
    def level_up(self):
        """レベルアップ"""
        self.level += 1
        self.exp -= 100
        self.max_hp += 10
        self.hp = self.max_hp
        self.max_mp += 5
        self.mp = self.max_mp
    
    def gain_gold(self, amount):
        """ゴールドを獲得"""
        self.gold += amount
    
    def spend_gold(self, amount):
        """ゴールドを消費"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
