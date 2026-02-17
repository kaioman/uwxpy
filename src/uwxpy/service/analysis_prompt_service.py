from uwxpy.service.core.base_prompt_service import BasePromptService

class AnalysisPromptService(BasePromptService):
    """
    解析用プロンプト生成サービス
    """

    def __init__(self, persona_path="personas.json", analysis_template_path="analysis_prompt_template.json"):
        """
        コンストラクタ

        Parameters
        ----------
        persona_path : str
            Personaファイルパス
        analysis_template_path : str
            画像解析プロンプト設定ファイルパス
        """

        # 基底側コンストラクタ
        super().__init__()

        # personas初期化
        self.personas = self._load_json(persona_path)
            
        # analysis_prompt_template初期化
        self.analysis_prompt_template = self._load_json(analysis_template_path)

    def get_analysis_prompt(self, persona_key, analysis_template_key) -> str:
        persona = self.personas.get(persona_key)
        analysis_template = self.analysis_prompt_template.get(analysis_template_key)
        if not persona or not analysis_template:
            return "Descripbe the image."
        
        if isinstance(analysis_template, list):
            template_str = "\n".join(analysis_template)
        else:
            template_str = analysis_template
        
        # JSONの構造に合わせてマッピング
        context = {
            "name": persona['name'],
            "tone": persona['tone'],
            **persona['traits'],
            **persona['viewpoint'],
            **persona['core_logic'],
        }
        return template_str.format(**context)