import json
import os

class ConfigManager:
    """配置管理器，用于管理和持久化用户设置"""
    
    def __init__(self):
        self.config_path = "app/resources/user_config.json"
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置"""
        default_config = {
            "username": "学生",
            "email": "",
            "daily_goal": "2小时",
            "reminder_enabled": True,
            "auto_save_enabled": True,
            "avatar_path": "",
            "oidc_issuer_url": "https://account.ae-3803.com",
            "oidc_client_id": "",
            "oidc_redirect_port": 8765,
            "oidc_scopes": "openid profile email offline_access"
        }
        
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # 合并默认配置和加载的配置
                    for key, value in default_config.items():
                        if key not in config:
                            config[key] = value
                    return config
            except Exception as e:
                print(f"加载用户配置失败: {e}")
                return default_config
        else:
            return default_config
    
    def save_config(self):
        """保存配置"""
        config_dir = os.path.dirname(self.config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"保存用户配置失败: {e}")
            return False
    
    def get_username(self):
        """获取用户名"""
        return self.config.get("username", "学生")
    
    def set_username(self, username):
        """设置用户名"""
        self.config["username"] = username
        return self.save_config()
    
    def get_email(self):
        """获取邮箱"""
        return self.config.get("email", "")
    
    def set_email(self, email):
        """设置邮箱"""
        self.config["email"] = email
        return self.save_config()
    
    def get_daily_goal(self):
        """获取每日学习目标"""
        return self.config.get("daily_goal", "2小时")
    
    def set_daily_goal(self, daily_goal):
        """设置每日学习目标"""
        self.config["daily_goal"] = daily_goal
        return self.save_config()
    
    def get_reminder_enabled(self):
        """获取学习提醒是否启用"""
        return self.config.get("reminder_enabled", True)
    
    def set_reminder_enabled(self, enabled):
        """设置学习提醒是否启用"""
        self.config["reminder_enabled"] = enabled
        return self.save_config()
    
    def get_auto_save_enabled(self):
        """获取自动保存是否启用"""
        return self.config.get("auto_save_enabled", True)
    
    def set_auto_save_enabled(self, enabled):
        """设置自动保存是否启用"""
        self.config["auto_save_enabled"] = enabled
        return self.save_config()
    
    def get_avatar_path(self):
        """获取头像路径"""
        return self.config.get("avatar_path", "")
    
    def set_avatar_path(self, avatar_path):
        """设置头像路径"""
        self.config["avatar_path"] = avatar_path
        return self.save_config()

    def get_oidc_issuer_url(self):
        return self.config.get("oidc_issuer_url", "https://account.ae-3803.com")

    def set_oidc_issuer_url(self, url):
        self.config["oidc_issuer_url"] = url
        return self.save_config()

    def get_oidc_client_id(self):
        return self.config.get("oidc_client_id", "")

    def set_oidc_client_id(self, client_id):
        self.config["oidc_client_id"] = client_id
        return self.save_config()

    def get_oidc_redirect_port(self):
        return int(self.config.get("oidc_redirect_port", 8765))

    def set_oidc_redirect_port(self, port):
        self.config["oidc_redirect_port"] = int(port)
        return self.save_config()

    def get_oidc_scopes(self):
        return self.config.get("oidc_scopes", "openid profile email offline_access")

    def set_oidc_scopes(self, scopes):
        self.config["oidc_scopes"] = scopes
        return self.save_config()

# 创建全局配置管理器实例
config_manager = ConfigManager()
