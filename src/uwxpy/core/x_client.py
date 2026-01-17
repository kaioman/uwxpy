import tweepy
import uwxpy.configs.app_init as app
from http import HTTPStatus

class XClient:
    """
    X API v2クライアント
    """
    
    def __init__(self):
        """
        コンストラクタ
        """
        
        # x_clientインスタンス生成
        self.x_client = tweepy.Client(
            consumer_key=app.core.config.x_api.consumer_key,
            consumer_secret=app.core.config.x_api.consumer_secret,
            access_token=app.core.config.x_api.access_token,
            access_token_secret=app.core.config.x_api.access_token_secret
        )
        
        # tweepy APIインスタンス生成
        auth = tweepy.OAuth1UserHandler(
            consumer_key=app.core.config.x_api.consumer_key,
            consumer_secret=app.core.config.x_api.consumer_secret,
            access_token=app.core.config.x_api.access_token,
            access_token_secret=app.core.config.x_api.access_token_secret
        )
        self.x_api = tweepy.API(auth)
        
    def tweet(self, text: str, media_ids: list[str] | None = None) -> dict:
        """
        Xにツイートを投稿する
        """
        
        try:
            response = self.x_client.create_tweet(
                text=text,
                media_ids=media_ids
            )
            return {
                "status": HTTPStatus.OK,
                "tweet_id": response.data.get("id"),
                "raw": response.data,
            }
        except Exception as e:
            raise RuntimeError(f"Tweet failed: {e}")
    
    def upload_media(self, media_bytes: bytes) -> str:
        """
        画像などのメディアをアップロードして**media_id**を返す
        """

        try:
            media = self.x_api.media_upload(media=media_bytes)
            return media.media_id
        except Exception as e:
            raise RuntimeError(f"Media upload failed {e}")
    
    def tweet_with_media(self, text: str, media_bytes: bytes) -> dict:
        """
        画像付きツイートを投稿する
        """
        
        media_id = self.upload_media(media_bytes)
        return self.tweet(text=text, media_ids=[media_id])