import random
from pycorex.gemini_client import GeminiClient
from pycorex.uwgen_client import UwgenClient
from uwxpy.service.core.base_prompt_service import BasePromptService

class GeneratePromptService(BasePromptService):
    """
    プロンプト生成サービス
    """

    def __init__(self, modes_path="modes.json" , word_data_path="words_data.json", style_anchor_path="style_anchor.json"):
        """
        コンストラクタ
        
        Parameters
        ----------
        aiart_client : UwgenClient
            Uwgenクライアント
        modes_path : str
            プロンプトモード設定ファイルパス
        word_data_path : str
            プロンプトワード設定ファイルパス
        style_anchor_path : str
            黄金律プロンプト設定ファイルパス
        """
        
        # 基底側コンストラクタ
        super().__init__()
        
        # modes初期化
        self.modes = self._load_json(modes_path)['modes']
        # words_data初期化
        self.word_data = self._load_json(word_data_path)
        # style_anchor初期化
        self.style_anchor = self._load_json(style_anchor_path)
        
    def _get_generate_random_element(self, mode_key):
        modes_map = self.modes.get(mode_key, self.modes['chill'])['mapping']
        w = self.word_data        
        comp_key = random.choice(list(w['subject_compositions'].keys()))
        
        return {
            "quality": random.choice(w['categories']['quality'][modes_map['quality']]),
            "subject": random.choice(w['subject_compositions'][comp_key]), 
            "hair": random.choice(w['hairstyle'][modes_map['hairstyle']]),
            "outfit": random.choice(w['outfit'][modes_map['outfit']]),
            "pose": random.choice(w['pose_and_angle'][modes_map['pose_and_angle']]),
            "expression": random.choice(w['expression'][modes_map['expression']]),
            "location": random.choice(w['location'][modes_map['location']]),
            "effect": random.choice(w['effects'][modes_map['effects']]),
            "style": w['fixed_elements']['style'],
            "safety": w['fixed_elements']['safety'],
        }
    
    def _get_edit_random_element(self, mode_key):
        modes_map = self.modes.get(mode_key, self.modes['chill'])['mapping']
        w = self.word_data
        
        mandatory_change = {
            "pose_and_composition": random.choice(w['pose_and_angle'][modes_map['pose_and_angle']])
        }
        
        other_options = {
            "outfit": random.choice(w['outfit'][modes_map['outfit']]),
            "location": random.choice(w['location'][modes_map['location']]),
            "expression": random.choice(w['expression'][modes_map['expression']]),
            "effect": random.choice(w['effects'][modes_map['effects']]),
        }
        
        selected_keys = random.choice(list(other_options.keys()))
        
        change_desc = f"New Pose/Composition: {mandatory_change['pose_and_composition']}, New {selected_keys.capitalize()}: {other_options[selected_keys]}"

        return {
            "change_description": change_desc,
            "safety": w['fixed_elements']['style'],
            "quality": random.choice(w['categories']['quality'][modes_map['quality']]),
        }
        
    def create_rewrite_request(self, aiart_client: UwgenClient, mode_key='action', is_edit=False):
        """
        リライト依頼文を生成して、Geminiにプロンプトのリライトをリクエストする
        """
        
        # 黄金律ブロック
        style_anchor = ",".join(self.style_anchor['line_deitail_heavy']) + ","

        # ランダム要素取得
        if is_edit:
            e = self._get_edit_random_element(mode_key)    
        else:
            e = self._get_generate_random_element(mode_key)

        # 生成/編集の判定
        if is_edit:
            request_prompt = (
                f"Role: Expert Image Prompt Engineer.\n"
                f"Task: Rewrite the prompt to change the image composition and one detail significantly. \n"
                f"Instruction: YOU MUST change the character's pose and camera angle as specified. \n"
                f"Maintain the character's identity but create a new visual structure. \n\n"
                f"### Mandatory Changes ###\n"
                f"- {e['change_description']}\n"
                f"- Style: {style_anchor}\n"
                f"- Quality: {e['quality']}\n\n"
                f"### Output Rules ###\n"
                f"1. Output ONLY the final image prompt in English.\n"
                f"2. Describe the new pose and compsition vividly at the beginning of the paragraph.\n"
                f"3. No Japanese, No explanations. End with: ({e['safety']})"
            )
        else:
            target_label = "Current"
            task_instruction = (
                "Task: Create a brand-new, vivid, and emotional image generation prompt from scratch.\n"
                "Instruction: Focus on building a complete world and atmosphere around these elements."
            )
        
            request_prompt = (
                f"Role: You are a professional prompt engineer and safety compliance specialist.\n"
                f"{task_instruction}\n\n"
                f"### Crucial Safety & Transformation Rule ###\n"
                f"Analyze elements for filter-triggering terms (suggestive, risky, or sensitive topics).\n"
                f"DO NOT omit them. Instead, TRANSFORM them into artistic, metaphorical, and safe-yet-vivid expressions.\n"
                f"Example: '2 girls in bed' -> 'Two close companions sharing a serene, quiet moment on a plush lounge'.\n\n"
                f"### Elements ###\n"
                f"- Quality: {e['quality']}\n"
                f"- Subject & Style: {e['subject']} ({style_anchor})\n"
                f"- {target_label} Scene: {e['pose']} at {e['location']}\n"
                f"- {target_label} Details: {e['hair']}, {e['outfit']}, {e['expression']}\n"
                f"- Ambience: {e['effect']}\n\n"
                f"### Output Rules ###\n"
                f"1. One single emotional paragraph in English. Output ONLY the final prompt.\n"
                f"2. Integrate 'extremely delicate fine lines' naturally into the description.\n"
                f"3. Strictly NO bolding (**), NO introductory text, and NO conversational fillers.\n"
                f"4. End the paragraph with: ({e['safety']})"
        )
        
        # リライトプロンプト用payload
        payload = {
            "model": GeminiClient.GeminiModel.GEMINI_3_0_FLASH_PREVIEW.value,
            "max_output_tokens": 3000
        }
    
        # リライトプロンプト生成
        rewrite_prompt_response = aiart_client.generate_text(
            prompt=request_prompt,
            **payload
        )
        if not rewrite_prompt_response:
            return ""
        
        # リライトプロンプトを返す
        return rewrite_prompt_response["text"]