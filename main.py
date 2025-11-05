#!/usr/bin/env python3
"""
RPGゲーム メインプログラム
エリア移動の視覚的連携を実装
エリア移動ポイント > エンカウント の優先順位
"""
import pygame
import sys
from src.game.game_engine import GameEngine
from src.ui.renderer import GameRenderer, TILE_SIZE, INFO_PANEL_HEIGHT

class Game:
    """ゲームメインクラス"""
    
    def __init__(self):
        pygame.init()
        
        # 画面設定
        self.screen_width = 928  # 14.5タイル分
        self.screen_height = 768 + INFO_PANEL_HEIGHT
        
        # ゲームエンジンとレンダラーを初期化
        self.engine = GameEngine()
        self.renderer = GameRenderer(self.screen_width, self.screen_height)
        
        # ゲームループ制御
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # カメラ
        self.camera_offset = [0, 0]
        
        # トランジション制御
        self.is_transitioning = False
        self.transition_stage = 'none'  # 'none', 'fade_out', 'execute', 'fade_in'
        
    def calculate_camera_offset(self):
        """カメラオフセットを計算（プレイヤーを中心に）"""
        player_pos = self.engine.player.get_position()
        area = self.engine.area_manager.current_area
        
        # プレイヤーを画面中央に配置
        target_x = player_pos[0] * TILE_SIZE - self.screen_width // 2 + TILE_SIZE // 2
        target_y = player_pos[1] * TILE_SIZE - (self.screen_height - INFO_PANEL_HEIGHT) // 2 + TILE_SIZE // 2
        
        # マップの端でカメラを止める
        max_x = max(0, area.width * TILE_SIZE - self.screen_width)
        max_y = max(0, area.height * TILE_SIZE - (self.screen_height - INFO_PANEL_HEIGHT))
        
        target_x = max(0, min(target_x, max_x))
        target_y = max(0, min(target_y, max_y))
        
        return [target_x, target_y]
    
    def handle_events(self):
        """イベント処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # トランジション中は入力を受け付けない
                if self.is_transitioning:
                    continue
                
                # 移動キー
                if event.key == pygame.K_UP:
                    self.handle_move(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.handle_move(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.handle_move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.handle_move(1, 0)
                
                # アクションキー
                elif event.key == pygame.K_SPACE:
                    self.handle_action()
                
                # その他のキー
                elif event.key == pygame.K_z:
                    print("神威発動")
                elif event.key == pygame.K_x:
                    print("メニュー")
                elif event.key == pygame.K_s:
                    print("セーブ")
                
                # デバッグ用：ESCで終了
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def handle_move(self, dx, dy):
        """移動処理"""
        result = self.engine.handle_player_move(dx, dy)
        
        if result['success']:
            action = result.get('action')
            
            if action == 'area_transition':
                # エリア遷移を開始
                self.start_area_transition(result['transition'])
            elif action == 'encounter':
                # エンカウント処理
                print(f"エンカウント: {result['encounter']}")
    
    def handle_action(self):
        """アクション処理（話しかける、調べるなど）"""
        interaction = self.engine.check_npc_interaction()
        if interaction:
            print(f"[{interaction['npc_name']}]")
            for line in interaction['dialogue']:
                print(f"  {line}")
    
    def start_area_transition(self, transition_data):
        """
        エリア遷移を開始
        視覚的なフェードアウト→移動実行→フェードイン
        """
        self.is_transitioning = True
        self.transition_stage = 'fade_out'
        self.renderer.start_transition('out')
        self.engine.transition_data = transition_data
    
    def update_transition(self):
        """トランジションの更新"""
        if not self.is_transitioning:
            return
        
        if self.transition_stage == 'fade_out':
            # フェードアウト完了をチェック
            if self.renderer.transition_alpha >= 255:
                self.transition_stage = 'execute'
                # エリア遷移を実行
                self.engine.execute_area_transition()
                # カメラ位置を更新
                self.camera_offset = self.calculate_camera_offset()
                # フェードイン開始
                self.renderer.start_transition('in')
                self.transition_stage = 'fade_in'
        
        elif self.transition_stage == 'fade_in':
            # フェードイン完了をチェック
            if self.renderer.transition_alpha <= 0:
                self.transition_stage = 'none'
                self.is_transitioning = False
                self.engine.is_transitioning = False
    
    def render(self):
        """描画処理"""
        self.renderer.clear_screen()
        
        # 現在のエリアとプレイヤー情報を取得
        state = self.engine.get_current_state()
        area = state['current_area']
        player = state['player']
        
        # カメラオフセットを更新（トランジション中以外）
        if not self.is_transitioning:
            self.camera_offset = self.calculate_camera_offset()
        
        # マップを描画
        self.renderer.draw_tiles(area, self.camera_offset)
        self.renderer.draw_grid(area, self.camera_offset)
        self.renderer.draw_area_exits(area, self.camera_offset)
        self.renderer.draw_npcs(area, self.camera_offset)
        self.renderer.draw_player(player, self.camera_offset)
        
        # 情報パネルを描画
        self.renderer.draw_info_panel(player, area)
        
        # 操作方法を描画
        self.renderer.draw_controls_help()
        
        # トランジションエフェクトを描画
        if self.is_transitioning:
            self.renderer.draw_transition_effect(state['transition_data'])
        
        # 画面を更新
        self.renderer.update_display()
    
    def run(self):
        """メインループ"""
        print("=== RPG Game Started ===")
        print("エリア移動の視覚的連携を実装")
        print("優先度: エリア移動ポイント > エンカウント")
        print()
        
        while self.running:
            # イベント処理
            self.handle_events()
            
            # トランジション更新
            self.update_transition()
            
            # 描画
            self.render()
            
            # FPS制御
            self.clock.tick(self.fps)
        
        # 終了処理
        pygame.quit()
        sys.exit()


def main():
    """メイン関数"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
