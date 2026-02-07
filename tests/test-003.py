import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger
from pycorex.gemini_client import GeminiClient
from uwxpy.core.aiartworks import AIArtworks

# アプリ初期化
app.init_app(__file__, "logger.json", "uwxpy.json")

# aiartworksインスタンス生成
aiartworks_client = AIArtworks()

try:
    payload = {
        "model": GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
        "resolution": GeminiClient.ImageSize.TWO_K.value,
        "aspect": GeminiClient.AspectRatio.SQUARE.value,
        "safety_filter": GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
        "safety_level": GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value
    }
    
    # 画像生成テスト
    res = aiartworks_client.generate_image(
        prompt="リクルートスーツの女性が居酒屋で酒をあおっている",
        output_abs_path="gen_images",
        **payload
    )
    
    # ロガーテスト
    app_logger.info("Image generation Successfully.")
except Exception as e:
    app_logger.error(e)
