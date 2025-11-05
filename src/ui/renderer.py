"""
ゲーム画面の描画システム
Pygameを使用したレンダリング
"""
import pygame
from typing import Tuple

# 色定義
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_BLUE = (25, 25, 60)
COLOR_BLUE = (67, 135, 203)
COLOR_LIGHT_BLUE = (100, 180, 255)
COLOR_CYAN = (0, 255, 255)
COLOR_GREEN = (0, 200, 100)
COLOR_DARK_GREEN = (0, 100, 50)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (200, 50, 50)
COLOR_PURPLE = (150, 50, 150)
COLOR_GRAY = (100, 100, 100)
COLOR_DARK_GRAY = (50, 50, 50)

# グリッドサイズ
TILE_SIZE = 64
INFO_PANEL_HEIGHT = 100


class GameRenderer:
    """ゲーム描画クラス"""
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("RPG Game")
        
        # フォント
        pygame.font.init()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # 日本語フォントの設定（システムフォントを使用）
        try:
            self.font_jp_large = pygame.font.SysFont('notosanscjkjp', 32)
            self.font_jp_medium = pygame.font.SysFont('notosanscjkjp', 24)
            self.font_jp_small = pygame.font.SysFont('notosanscjkjp', 18)
        except:
            # フォールバック
            self.font_jp_large = self.font_large
            self.font_jp_medium = self.font_medium
            self.font_jp_small = self.font_small
        
        # トランジションエフェクト
        self.transition_alpha = 0
        self.transition_direction = 'in'  # 'in' or 'out'
        
    def clear_screen(self):
        """画面をクリア"""
        self.screen.fill(COLOR_DARK_BLUE)
    
    def draw_grid(self, area, camera_offset=(0, 0)):
        """グリッドを描画"""
        offset_x, offset_y = camera_offset
        
        # グリッド線を描画
        for x in range(area.width + 1):
            screen_x = x * TILE_SIZE - offset_x
            pygame.draw.line(
                self.screen,
                COLOR_GRAY,
                (screen_x, -offset_y),
                (screen_x, area.height * TILE_SIZE - offset_y),
                1
            )
        
        for y in range(area.height + 1):
            screen_y = y * TILE_SIZE - offset_y
            pygame.draw.line(
                self.screen,
                COLOR_GRAY,
                (-offset_x, screen_y),
                (area.width * TILE_SIZE - offset_x, screen_y),
                1
            )
    
    def draw_tiles(self, area, camera_offset=(0, 0)):
        """タイルを描画"""
        offset_x, offset_y = camera_offset
        
        for y in range(area.height):
            for x in range(area.width):
                screen_x = x * TILE_SIZE - offset_x
                screen_y = y * TILE_SIZE - offset_y
                
                # 障害物
                if (x, y) in area.obstacles:
                    pygame.draw.rect(
                        self.screen,
                        COLOR_DARK_GRAY,
                        (screen_x + 2, screen_y + 2, TILE_SIZE - 4, TILE_SIZE - 4)
                    )
                # 歩行可能タイル
                else:
                    pygame.draw.rect(
                        self.screen,
                        COLOR_DARK_BLUE,
                        (screen_x + 2, screen_y + 2, TILE_SIZE - 4, TILE_SIZE - 4)
                    )
    
    def draw_npcs(self, area, camera_offset=(0, 0)):
        """NPCを描画"""
        offset_x, offset_y = camera_offset
        
        for npc in area.npcs:
            x, y = npc.position
            screen_x = x * TILE_SIZE - offset_x + TILE_SIZE // 2
            screen_y = y * TILE_SIZE - offset_y + TILE_SIZE // 2
            
            # NPCの種類によって色を変える
            if 'merchant' in npc.sprite_type:
                color = COLOR_YELLOW
            elif npc.sprite_type == 'guide':
                color = COLOR_LIGHT_BLUE
            elif npc.sprite_type == 'innkeeper':
                color = COLOR_PURPLE
            elif npc.sprite_type == 'guildmaster':
                color = COLOR_GREEN
            else:
                color = COLOR_WHITE
            
            # NPCを円で描画
            pygame.draw.circle(
                self.screen,
                color,
                (screen_x, screen_y),
                TILE_SIZE // 3
            )
            
            # 名前表示
            name_surface = self.font_jp_small.render(npc.name, True, COLOR_WHITE)
            name_rect = name_surface.get_rect(center=(screen_x, screen_y - TILE_SIZE // 2))
            self.screen.blit(name_surface, name_rect)
    
    def draw_player(self, player, camera_offset=(0, 0)):
        """プレイヤーを描画"""
        offset_x, offset_y = camera_offset
        
        x, y = player.get_position()
        screen_x = x * TILE_SIZE - offset_x + TILE_SIZE // 2
        screen_y = y * TILE_SIZE - offset_y + TILE_SIZE // 2
        
        # プレイヤーを描画（青い三角形）
        size = TILE_SIZE // 3
        
        if player.direction == 'up':
            points = [
                (screen_x, screen_y - size),
                (screen_x - size, screen_y + size),
                (screen_x + size, screen_y + size)
            ]
        elif player.direction == 'down':
            points = [
                (screen_x, screen_y + size),
                (screen_x - size, screen_y - size),
                (screen_x + size, screen_y - size)
            ]
        elif player.direction == 'left':
            points = [
                (screen_x - size, screen_y),
                (screen_x + size, screen_y - size),
                (screen_x + size, screen_y + size)
            ]
        else:  # right
            points = [
                (screen_x + size, screen_y),
                (screen_x - size, screen_y - size),
                (screen_x - size, screen_y + size)
            ]
        
        pygame.draw.polygon(self.screen, COLOR_CYAN, points)
    
    def draw_area_exits(self, area, camera_offset=(0, 0)):
        """エリア出口を描画"""
        offset_x, offset_y = camera_offset
        
        for exit_point in area.exits:
            x, y = exit_point.position
            screen_x = x * TILE_SIZE - offset_x + TILE_SIZE // 2
            screen_y = y * TILE_SIZE - offset_y + TILE_SIZE // 2
            
            # 出口を緑色の矢印で描画
            pygame.draw.circle(
                self.screen,
                COLOR_GREEN,
                (screen_x, screen_y),
                TILE_SIZE // 4
            )
    
    def draw_info_panel(self, player, area):
        """情報パネルを描画"""
        panel_y = self.screen_height - INFO_PANEL_HEIGHT
        
        # パネル背景
        pygame.draw.rect(
            self.screen,
            COLOR_BLACK,
            (0, panel_y, self.screen_width, INFO_PANEL_HEIGHT)
        )
        pygame.draw.line(
            self.screen,
            COLOR_BLUE,
            (0, panel_y),
            (self.screen_width, panel_y),
            2
        )
        
        # エリア名
        area_text = self.font_jp_medium.render(area.display_name, True, COLOR_WHITE)
        self.screen.blit(area_text, (20, panel_y + 10))
        
        # プレイヤー情報
        hp_text = f"HP: {player.hp}/{player.max_hp}"
        mp_text = f"MP: {player.mp}/{player.max_mp}"
        level_text = f"レベル: {player.level}"
        exp_text = f"経験値: {player.exp}"
        gold_text = f"ゴールド: {player.gold}"
        
        hp_surface = self.font_jp_small.render(hp_text, True, COLOR_WHITE)
        mp_surface = self.font_jp_small.render(mp_text, True, COLOR_WHITE)
        level_surface = self.font_jp_small.render(level_text, True, COLOR_WHITE)
        exp_surface = self.font_jp_small.render(exp_text, True, COLOR_WHITE)
        gold_surface = self.font_jp_small.render(gold_text, True, COLOR_WHITE)
        
        # HP/MPバー
        bar_width = 200
        bar_height = 20
        
        # HPバー
        hp_ratio = player.hp / player.max_hp
        pygame.draw.rect(
            self.screen,
            COLOR_DARK_GRAY,
            (80, panel_y + 45, bar_width, bar_height)
        )
        pygame.draw.rect(
            self.screen,
            COLOR_RED,
            (80, panel_y + 45, int(bar_width * hp_ratio), bar_height)
        )
        self.screen.blit(hp_surface, (85, panel_y + 48))
        
        # MPバー
        mp_ratio = player.mp / player.max_mp
        pygame.draw.rect(
            self.screen,
            COLOR_DARK_GRAY,
            (300, panel_y + 45, bar_width, bar_height)
        )
        pygame.draw.rect(
            self.screen,
            COLOR_BLUE,
            (300, panel_y + 45, int(bar_width * mp_ratio), bar_height)
        )
        self.screen.blit(mp_surface, (305, panel_y + 48))
        
        # レベル、経験値、ゴールド
        self.screen.blit(level_surface, (550, panel_y + 20))
        self.screen.blit(exp_surface, (550, panel_y + 45))
        self.screen.blit(gold_surface, (550, panel_y + 70))
    
    def draw_transition_effect(self, transition_data):
        """
        エリア遷移エフェクトを描画
        """
        if self.transition_direction == 'out':
            self.transition_alpha = min(255, self.transition_alpha + 15)
        else:  # 'in'
            self.transition_alpha = max(0, self.transition_alpha - 15)
        
        if self.transition_alpha > 0:
            # 半透明のオーバーレイ
            overlay = pygame.Surface((self.screen_width, self.screen_height))
            overlay.fill(COLOR_BLACK)
            overlay.set_alpha(self.transition_alpha)
            self.screen.blit(overlay, (0, 0))
            
            # 遷移情報テキスト
            if transition_data and self.transition_alpha > 100:
                target_area_name = transition_data.get('target_area', '')
                # エリア名を日本語に変換
                area_names = {
                    'shinjuku_center': '新宿 - 中央区画',
                    'shibuya_mall': '渋谷商業街 - ショッピングモール'
                }
                display_name = area_names.get(target_area_name, target_area_name)
                
                text = self.font_jp_large.render(f"{display_name}へ", True, COLOR_WHITE)
                text_rect = text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                self.screen.blit(text, text_rect)
        
        return self.transition_alpha >= 255 or self.transition_alpha <= 0
    
    def start_transition(self, direction='out'):
        """トランジション開始"""
        self.transition_direction = direction
        if direction == 'out':
            self.transition_alpha = 0
        else:
            self.transition_alpha = 255
    
    def draw_controls_help(self):
        """操作方法を描画"""
        help_texts = [
            "↑←→↓: 移動",
            "SPACE: アクション",
            "z: 神威発動",
            "x: メニュー",
            "s: セーブ (セーブポイント)"
        ]
        
        x = self.screen_width - 250
        y = 10
        
        for text in help_texts:
            surface = self.font_jp_small.render(text, True, COLOR_WHITE)
            self.screen.blit(surface, (x, y))
            y += 25
    
    def update_display(self):
        """画面を更新"""
        pygame.display.flip()
