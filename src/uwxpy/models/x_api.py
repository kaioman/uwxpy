
from libcore_hng.core.base_config_model import BaseConfigModel

class XAPIModel(BaseConfigModel):
    """
    X API設定クラス
    """
    
    consumer_key: str = ""
    """ X コンシューマキー """
    
    consumer_secret: str = ""
    """ X コンシューマ秘密鍵 """
    
    access_token: str = ""
    """ X アクセストークン """
    
    access_token_secret: str = ""
    """ X アクセストークン秘密鍵 """
