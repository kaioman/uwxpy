from pycorex.configs.pycorex import PyCorexConfig
from uwxpy.models.x_api import XAPIModel

class UwxpyConfig(PyCorexConfig):
    """
    uwxpy共通設定クラス
    """
    
    x_api: XAPIModel = XAPIModel()
    """ X API設定クラスモデル"""

    image_output_abs_path: str
    """ 画像出力先相対パス """