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
        "safety_level": GeminiClient.SafetyFilterLevel.BLOCK_NONE.value
    }
    
    # 画像生成テスト
    res = aiartworks_client.generate_image(
        prompt="2 girls, anime style illustration, masterpiece, 8k resolution, ray tracing, short hair with bangs, futuristic cyberpunk bodysuit, jumping high in the air, low angle shot, sharp piercing eyes, floating islands in the sky, exploding sparks, safe for work, no nudity, high quality art",
        output_abs_path="gen_images",
        **payload
    )
    
    # 画像ツイートテスト
    if res:
        result = aiartworks_client.tweet_with_media("2 girls test\n#AI\n#AIArt", res["images"][0])
    
        # 生成+Tweet成功
        app_logger.info("Image generation and tweet completed successfully.")
    else:
        # 生成失敗
        app_logger.warning("Image generation failed.")
        
except Exception as e:
    app_logger.error(e)
