import uwxpy.configs.app_init as app
import libcore_hng.utils.crypto as crypto

# アプリ初期化
app.init_app(__file__, "app_config.json", "gcp_config.json","uwxpy.json")

# 設定ファイルを暗号化して新規ファイルとして作成
key = crypto.create_encryption_file_from_secret_manager("configs/uwxpy.json", "DECRYPTION_KEY")

# 生成された鍵を表示
print("以下の鍵を GCP Secret Manager (または環境変数 APP_SECRET_KEY) に登録してください:")
print(key.decode("utf-8"))