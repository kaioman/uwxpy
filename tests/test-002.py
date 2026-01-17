import uwxpy.configs.app_init as app
import libcore_hng.utils.app_logger as app_logger
from uwxpy.core.x_client import XClient

# アプリ初期化
app.init_app(__file__, "logger.json", "uwxpy.json")

# XClientインスタンス生成
x_client = XClient()

try:
    # Tweetテスト
    res = x_client.tweet("Test Tweet. What's up?")
    print(res.tweet_id)
    print(res.status)
    
    # ロガーテスト
    app_logger.info("Tweet Successfully.")
except Exception as e:
    app_logger.error(e)
