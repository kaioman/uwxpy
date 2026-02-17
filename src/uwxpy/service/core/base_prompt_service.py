import os
import json
import pycorex.configs.app_init as app

class BasePromptService:
    
    def _load_json(self, abs_path: str) -> dict:
        """
        設定をJSONから読み込む
        
        Parameters
        ----------
        abs_path : str
            JSONファイル相対パス

        """
        
        # JSONファイルのフルパス取得
        abs_path_full = app.core.config.project_root_path / abs_path
        # JSONファイル存在確認
        if os.path.exists(abs_path_full):
            # JSONファイルを読み込み結果を返す
            with open(abs_path_full, 'r', encoding='utf-8') as f:
                return json.load(f)