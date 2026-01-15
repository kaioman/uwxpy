import uwxpy.configs.app_init as app
import libcore_hng.testmodule as tm
import libcore_hng.utils.app_logger as app_logger

def libcore_test():
    msg = tm.test_function()
    app_logger.info(msg)
    print(app.core.config.uwgen_api_key)
    print(app.core.config.uwgen_endpoint)
    
# アプリ初期化
app.init_app(__file__, "logger.json", "uwxpy.json")

libcore_test()
