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
    
    # 画像編集テスト
    res = aiartworks_client.edit_image(
        prompt="Imagine the girl from the original image in a completely different scene. Keeping her face and the original anime art style, redraw her standing with feet shoulder-width apart in a hero pose. She is now wearing a medieval knight armor with a cape, and her expression has changed to a serious determined face. Replace the background with fantasy castle battlements under dramatic shadows.",
        source_file_path="source_image/unchain8.png",
        output_abs_path="gen_images",
        **payload
    )
    
    # 画像ツイートテスト
    if res:
        result = aiartworks_client.tweet_with_media("Image edit testing\n#AI\n#AIArt", res["images"][0])
    
        # 生成+Tweet成功
        app_logger.info("Image generation and tweet completed successfully.")
    else:
        # 生成失敗
        app_logger.warning("Image generation failed.")
        
except Exception as e:
    app_logger.error(e)
