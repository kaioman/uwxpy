import json
import random

class GeneratePrompt:
    
    def __init__(self, modes_path, word_path, style_anchor_path):
        with open(modes_path, 'r', encoding='utf-8') as f:
            self.modes = json.load(f)['modes']
        with open(word_path, 'r', encoding='utf-8') as f:
            self.word_data = json.load(f)
        with open(style_anchor_path, 'r', encoding='utf-8') as f:
            self.style_anchor = json.load(f)

    def _get_random_element(self, mode_key):
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
    
    def _get_simple_element(self, mode_key):
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
        
    def create_rewrite_request(self, mode_key='action', is_edit=False):
        """
        リライト依頼文を生成して、Geminiにプロンプトのリライトをリクエストする
        """
        
        # 黄金律ブロック
        style_anchor = ",".join(self.style_anchor['line_deitail_heavy']) + ","

        # ランダム要素取得
        if is_edit:
            e = self._get_simple_element(mode_key)    
        else:
            e = self._get_random_element(mode_key)

        # 生成/編集の判定
        if is_edit:
            
            request = (
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
        
            request = (
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
        return request, e