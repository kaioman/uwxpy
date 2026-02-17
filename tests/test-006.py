import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger
from http import HTTPStatus
from uwxpy.core.aiartworks import AIArtworks
from uwxpy.service.analysis_prompt_service import AnalysisPromptService
from uwxpy.service.generate_prompt_service import GeneratePromptService

# アプリ初期化
app.init_app(__file__, "logger.json", "uwxpy.json")

aps = AnalysisPromptService(
    persona_path="tests/prompt/personas.json", 
    analysis_template_path="tests/prompt/analysis_prompt_templates.json"
)

gps = GeneratePromptService(
    modes_path="tests/prompt/modes.json", 
    word_data_path="tests/prompt/words_data.json", 
    style_anchor_path="tests/prompt/style_anchor.json"
)

# aiartworksインスタンス生成
aiartworks_client = AIArtworks(
    aps=aps,
    gps=gps
)

try:
    # 画像編集+ツイートテスト
    res = aiartworks_client.edit_image_and_tweet(
        source_file_path="tests/source_image/unchain8.png",
        output_abs_path="tests/gen_images",
        persona_key="cyber_rebel_philosophy"
    )
    
    if res.status == HTTPStatus.OK:
        # 生成+Tweet成功
        app_logger.info("Image edit and tweet completed successfully.")
    else:
        # 生成失敗
        app_logger.warning("Image edit and tweet failed.")
        
except Exception as e:
    app_logger.error(e)
