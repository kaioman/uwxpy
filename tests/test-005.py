import os
import sys
import uwxpy.configs.app_init as app
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import libcore_hng.utils.app_logger as app_logger
from pycorex.gemini_client import GeminiClient
from uwxpy.core.aiartworks import AIArtworks

# アプリ初期化
app.init_app(__file__, "logger.json", "uwxpy.json")

from tests.generate_prompt import GeneratePrompt

#p = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
p = os.path.abspath(os.path.join(os.path.dirname(__file__)))

pgen = GeneratePrompt(os.path.join(p, "prompt/modes.json"), os.path.join(p, "prompt/words.json"), os.path.join(p, "prompt/style_anchor.json"))

rewite_gen_prompt, e = pgen.create_rewrite_request(mode_key='action', is_edit=False)
rewite_edit_prompt, e = pgen.create_rewrite_request(mode_key='chill', is_edit=True)

# aiartworksインスタンス生成
aiartworks_client = AIArtworks()

try:
    payload = {
        "model": GeminiClient.GeminiModel.GEMINI_3_0_FLASH_PREVIEW.value,
        "max_output_tokens": 3000
    }
    
    # リライトプロンプト生成テスト
    res = aiartworks_client.generate_text(
        prompt=rewite_edit_prompt,
        **payload
    )
    
    # リライトプロンプト出力
    if res:
        print(res["text"])
    
except Exception as e:
    app_logger.error(e)