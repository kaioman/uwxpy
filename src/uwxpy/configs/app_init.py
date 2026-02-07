from libcore_hng.utils.app_core import AppInitializer
from pycorex.configs import app_init as core_app
from uwxpy.configs.uwxpy import UwxpyConfig

class UwxpyAppInitializer(AppInitializer[UwxpyConfig]):
    """
    AppInitializer拡張クラス
    """
    def __init__(self, base_file: str = __file__, *config_file: str):
        # 基底コンストラクタに拡張Configクラスを渡す
        super().__init__(UwxpyConfig, base_file, *config_file)

core: UwxpyAppInitializer | None = None
""" AppInitializer拡張クラスインスタンス """

def init_app(base_file: str = __file__, *config_file: str) -> UwxpyAppInitializer:
    """
    アプリケーション初期化
    """
    global core
    core = UwxpyAppInitializer(base_file, *config_file)
    if core_app.core is None:
        core_app.init_app(base_file, *config_file)
    return core
