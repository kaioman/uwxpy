import random
import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger
from http import HTTPStatus
from pycorex.gemini_client import GeminiClient
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
    payload_override = {
        "model": GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
        "aspect": GeminiClient.AspectRatio.WIDE.value,
    }
    
    # Personaランダム選択
    persona_key = random.choice(
        [
            "cyber_rebel_philosophy",
            "default_android_girl",
            "intellectual_idealist_android",
            "impish_chaos_android",
        ]
    )
    
    # Persona画像取得
    source_image_path = aiartworks_client.analysis_psrv.personas[persona_key]["source_image"]
    
    res = aiartworks_client.edit_image_and_tweet(
        source_file_path=source_image_path,
        output_abs_path="tests/gen_images",
        persona_key=persona_key,
        mode_key=random.choice(["chill","action"]),
        **payload_override
    )
    
    if res.status == HTTPStatus.OK:
        # 生成+Tweet成功
        app_logger.info("Image edit and tweet completed successfully.")
    else:
        # 生成失敗
        app_logger.warning("Image edit and tweet failed.")
        
except Exception as e:
    app_logger.error(e)
