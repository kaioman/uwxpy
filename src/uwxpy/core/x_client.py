import io
import tweepy
import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger
from http import HTTPStatus
from tweepy.errors import TweepyException
from uwxpy.models.tweet_result import TweetResult
from uwxpy.exceptions.x_api_error import XApiError

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
    
    def tweet(self, text: str, media_ids: list[str] | None = None) -> TweetResult:
        """
        Xにツイートを投稿する
        """
        
        try:
            # Xにテキストデータを投稿
            response = self.x_client.create_tweet(
                text=text,
                media_ids=media_ids
            )
            tweet_id = response.data.get("id")
            app_logger.info(f"Tweet successfully posted to X. tweet_id={tweet_id}")
            
            return TweetResult(
                status=HTTPStatus.OK,
                tweet_id=tweet_id,
                media_id=media_ids,
                raw=response.data,
            )
        except TweepyException as e:
            raise XApiError(e)
        except Exception as e:
            raise XApiError(e)
    
    def upload_media(self, media_bytes: bytes) -> TweetResult:
        """
        画像などのメディアをアップロードして**media_id**を返す
        """

        try:
            #media = self.x_api.media_upload(media=media_bytes)
            file_obj = io.BytesIO(media_bytes)
            media = self.x_api.media_upload(filename="upload.png", file=file_obj)
            media_id = media.media_id
            app_logger.info(f"Media uploaded successfully. media_id={media_id}")

            return TweetResult(
                status=HTTPStatus.OK,
                tweet_id=None,
                media_id=media_id,
                raw=media
            )
        except Exception as e:
            raise XApiError(e)
    
    def tweet_with_media(self, text: str, media_bytes: bytes) -> TweetResult:
        """
        画像付きツイートを投稿する
        """
        
        media_result = self.upload_media(media_bytes)
        if (media_result.status != HTTPStatus.OK):
            return media_result
        media_id = media_result.media_id
        return self.tweet(text=text, media_ids=[media_id])