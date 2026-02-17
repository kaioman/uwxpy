import libcore_hng.utils.app_logger as app_logger
from http import HTTPStatus
from typing import Optional
from pycorex.gemini_client import GeminiClient
from pycorex.uwgen_client import UwgenClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from uwxpy.core.x_client import XClient
from uwxpy.models.tweet_result import TweetResult
from uwxpy.service.analysis_prompt_service import AnalysisPromptService
from uwxpy.service.generate_prompt_service import GeneratePromptService

class AIArtworks(XClient):
    """
    AI画像生成クライアント
    """
    
    # 標準のペイロード設定
    DEFAULT_PAYLOAD = {
        "model": GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value,
        "resolution": GeminiClient.ImageSize.TWO_K.value,
        "aspect": GeminiClient.AspectRatio.SQUARE.value,
        "safety_filter": GeminiClient.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT.value,
        "safety_level": GeminiClient.SafetyFilterLevel.BLOCK_ONLY_HIGH.value
    }
    
    def __init__(self, aps: AnalysisPromptService=None, gps: GeneratePromptService=None):
        """
        コンストラクタ        
        """
        
        # 基底側コンストラクタ
        super().__init__()

        # aiart_clientクライアント
        self.aiart_client = UwgenClient()

        # AnalysisPromptService
        self.analysis_psrv = aps
        
        # GeneratePromptService
        self.generate_psrv = gps
        
    def generate_text(self, 
        prompt: str,  
        **payload):
        """
        テキスト生成
        """
        
        try:
            # テキスト生成を実行
            result = self.aiart_client.generate_text(
                prompt=prompt,
                **payload
            )
            
            # 処理結果を返す
            return result
        
        except Exception as e:
            app_logger.error(f"Unexpected error: {e}")
            
    def generate_image(self, 
        prompt: str, 
        output_abs_path, 
        **payload):
        """
        画像生成
        """
        
        try:
            # 画像生成を実行
            result = self.aiart_client.generate_image(
                prompt=prompt,
                **payload
            )
            
            # 画像ファイルを出力する
            self.aiart_client.output_images(result["images"], output_abs_path)

            # 処理結果を返す
            return result

        except NoCandidatesError as e:
            app_logger.error(f"Image generation failed: {e}")
        except Exception as e:
            app_logger.error(f"Unexpected error: {e}")
    
    def edit_image(self, 
        prompt: str, 
        source_file_path: str, 
        output_abs_path, 
        **payload):
        """
        画像編集
        """
        
        try:
            # 画像編集を実行
            result = self.aiart_client.edit_image(
                prompt=prompt,
                source_image_path=source_file_path,
                **payload
            )
            
            # 画像ファイルを出力してパスリストをresultに追加する
            result["images_path"] = self.aiart_client.output_images(result["images"], output_abs_path)

            # 処理結果を返す
            return result
        
        except NoCandidatesError as e:
            app_logger.error(f"Image edit failed: {e}")
        except Exception as e:
            app_logger.error(f"Unexpected error: {e}")
    
    def analyze_image(self, 
        prompt: str, 
        source_file_path: str, 
        **payload):
        """
        画像解析
        """
        
        try:
            # 画像解析を実行
            result = self.aiart_client.analyze_image(
                prompt=prompt,
                source_image_path=source_file_path,
                **payload
            )
            
            # 処理結果を返す
            return result
        
        except Exception as e:
            app_logger.error(f"Unexpected error: {e}")
    
    def generate_image_and_tweet(self):
        pass
    
    def edit_image_and_tweet(self,
        source_file_path: str,
        output_abs_path: str,
        edit_prompt: Optional[str] = None,
        analysis_prompt: Optional[str] = None,
        persona_key: str = "default_android_girl",
        analysis_template_key: str = "tweet_analysis_v1",
        mode_key: str = "action",
        **payload_override) -> TweetResult:
        """
        画像編集＋ツイート
        """
        
        # パラメータ―統合
        current_payload = {**self.DEFAULT_PAYLOAD, **payload_override}
        
        # 画像編集用プロンプト決定
        edit_prompt = edit_prompt if edit_prompt else self.generate_psrv.create_rewrite_request(self.aiart_client, mode_key, is_edit=True)

        # 開始ログ
        app_logger.info(f"Editing image: {source_file_path}")
        
        # 画像編集実行
        edit_image_result = self.edit_image(
            prompt=edit_prompt,
            source_file_path=source_file_path,
            output_abs_path=output_abs_path,
            **current_payload
        )
        
        if not edit_image_result:
            return TweetResult(
                status=HTTPStatus.BAD_REQUEST,
                tweet_id=None,
                media_id=None,
                raw=None
            ) 
        
        # 画像ファイルリストを取得する
        file_path_list: list = edit_image_result["images_path"]

        # 画像解析用プロンプト取得ログ
        app_logger.info("Getting analysis image prompt...")

        # 画像解析用プロンプト取得
        analysis_prompt = analysis_prompt if analysis_prompt else self.analysis_psrv.get_analysis_prompt(persona_key, analysis_template_key)

        # 解析ログ
        app_logger.info("Analyzing edited image for tweet message...")
        
        # 画像ファイルパスリスト判定
        if len(file_path_list) == 0:
            return TweetResult(
                status=HTTPStatus.BAD_REQUEST,
                tweet_id=None,
                media_id=None,
                raw=None                
            ) 
            
        # 画像解析
        analysis_result = self.analyze_image(
            prompt=analysis_prompt,
            source_file_path=file_path_list[0],
            model=GeminiClient.GeminiModel.GEMINI_3_0_PRO_IMAGE_PREVIEW.value
        )
        if not analysis_result:
            return TweetResult(
                status=HTTPStatus.BAD_REQUEST,
                tweet_id=None,
                media_id=None,
                raw=None
            ) 
        
        # 解析結果を取得
        twwet_messaage = analysis_result['text']

        # 画像ツイートを実行して結果を返す
        return self.tweet_with_media(twwet_messaage, edit_image_result["images"][0])        
