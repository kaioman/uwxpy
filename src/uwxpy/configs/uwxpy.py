from libcore_hng.core.base_config import BaseConfig
from pycorex.configs.pycorex import PyCorexConfig

class UwxpyConfig(PyCorexConfig):
    """
    uwxpy共通設定クラス
    """
    
    uwgen_api_key: str = ""
    """ Uwgen APIキー """
    
    uwgen_endpoint: str = ""
    """ Uwgen APIエンドポイントURL """

    x_consumer_key: str = ""
    """ X コンシューマキー """
    
    x_consumer_secret: str = ""
    """ X コンシューマ秘密鍵 """
    
    x_access_token: str = ""
    """ X アクセストークン """
    
    x_access_token_secret: str = ""
    """ X アクセストークン秘密鍵 """
    