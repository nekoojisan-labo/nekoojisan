"""
NPC（ノンプレイヤーキャラクター）システム
"""

class NPC:
    """NPCクラス"""
    def __init__(self, name, position, sprite_type, dialogue=None):
        self.name = name
        self.position = position  # (x, y)
        self.sprite_type = sprite_type  # 'merchant', 'innkeeper', 'guide', 'guildmaster' など
        self.dialogue = dialogue or []
        self.interaction_type = 'talk'  # 'talk', 'shop', 'inn', 'guild' など
        
    def interact(self):
        """NPCとの相互作用"""
        return {
            'npc_name': self.name,
            'type': self.interaction_type,
            'dialogue': self.dialogue
        }


class Enemy:
    """敵クラス"""
    def __init__(self, name, level, hp, attack, defense, exp_reward, gold_reward):
        self.name = name
        self.level = level
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
        
    def take_damage(self, damage):
        """ダメージを受ける"""
        actual_damage = max(1, damage - self.defense)
        self.hp = max(0, self.hp - actual_damage)
        return self.hp <= 0
    
    def get_attack_damage(self):
        """攻撃力を取得"""
        import random
        return self.attack + random.randint(-2, 2)
