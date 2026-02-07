import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger
from pycorex.uwgen_client import UwgenClient
from pycorex.exceptions.no_candidates_error import NoCandidatesError
from uwxpy.core.x_client import XClient

class AIArtworks(XClient):
    """
    AI画像生成クライアント
    """
    
    def __init__(self):
        """
        コンストラクタ
        """
        
        # 基底側コンストラクタ
        super().__init__()

        # aiart_clientクライアント
        self.aiart_client = UwgenClient()
        
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
            
            # 画像ファイルを出力する
            self.aiart_client.output_images(result["images"], output_abs_path)

            # 処理結果を返す
            return result
        
        except NoCandidatesError as e:
            app_logger.error(f"Image generation failed: {e}")
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