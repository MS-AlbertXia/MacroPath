import json
import os
from openai import OpenAI

class OpenAIClient:
    def __init__(self):
        self.api_key = None
        self.model = "gpt-3.5-turbo"
        self.temperature = 0.7
        self.api_base = "https://api.openai.com/v1"
        self.client = None
        self.load_config()
    
    def load_config(self):
        """加载配置"""
        config_path = "app/resources/openai_config.json"
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.api_key = config.get('api_key')
                    self.model = config.get('model', self.model)
                    self.temperature = config.get('temperature', self.temperature)
                    self.api_base = config.get('api_base', self.api_base)
                    if self.api_key:
                        self.client = OpenAI(
                            api_key=self.api_key,
                            base_url=self.api_base
                        )
            except Exception as e:
                print(f"加载OpenAI配置失败: {e}")
    
    def save_config(self, api_key, model, temperature, api_base):
        """保存配置"""
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.api_base = api_base
        
        if api_key:
            self.client = OpenAI(
                api_key=api_key,
                base_url=api_base
            )
        
        config_path = "app/resources"
        if not os.path.exists(config_path):
            os.makedirs(config_path)
        
        config = {
            'api_key': api_key,
            'model': model,
            'temperature': temperature,
            'api_base': api_base
        }
        
        try:
            with open(f"{config_path}/openai_config.json", 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存OpenAI配置失败: {e}")
            return False
    
    def get_response(self, prompt, max_tokens=1000):
        """获取AI响应"""
        if not self.api_key:
            return "错误: 请在设置中配置API密钥"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个专业的AI学习助手，帮助学生解答学习问题，提供学习建议和指导。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"错误: {str(e)}"
    
    def is_configured(self):
        """检查是否已配置"""
        return bool(self.api_key)