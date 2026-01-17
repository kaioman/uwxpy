import libcore_hng.utils.app_logger as app_logger
from tweepy.errors import TweepyException
from http import HTTPStatus

class XApiError(TweepyException):
    """
    X API例外クラス
    """
    
    def __init__(self, original: Exception):
        self.original = original
        
        # TweepyExceptionからHTTPステータスを取得
        response = getattr(original, "response", None)
        self.status = getattr(response, "status_code", HTTPStatus.INTERNAL_SERVER_ERROR)
        
        # エラーメッセージ
        self.message = str(original)
        
        # レスポンステキスト
        self.response_text = getattr(response, "text", None)
        
        # ログ出力
        app_logger.error(self._build_message())
        
        # 基底側コンストラクタ
        super().__init__(self.message)
        
    def __str__(self):
        return f"XApiError(status={self.status}, message={self.message})"
    
    def _build_message(self) -> str:
        """
        例外メッセージを組み立てる内部メソッド
        """
        
        # ベースメッセージ
        base = self.message
        
        # ステータスコード
        if self.status is not None:
            base += f"(status_code={self.status})"
        
        # レスポンステキスト
        if self.response_text:
            base += f" | response={self.response_text}"
        
        return base