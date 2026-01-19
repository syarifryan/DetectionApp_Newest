# import json, os
# import torch

# class ConfigManager:
#     CONFIG_FILE = "config/config.json"

#     @classmethod
#     def load_config(cls):
#         if not os.path.exists(cls.CONFIG_FILE):
#             raise FileNotFoundError(f"Config file not found: {cls.CONFIG_FILE}")
#         with open(cls.CONFIG_FILE, 'r') as f:
#             config = json.load(f)

#         # Device auto-detect
#         dev = config.get("device", "auto")
#         if dev == "auto":
#             config["device"] = "cuda" if torch.cuda.is_available() else "cpu"
#         else:
#             # allow explicit values: "cpu", "cuda", "0", "1", etc.
#             if dev.isdigit():
#                 config["device"] = dev  # GPU index like "0" (Ultralytics accepts "0")
#             else:
#                 config["device"] = dev

#         return config


# File: config/config_manager.py
import json, os
import torch

class ConfigManager:
    CONFIG_FILE = "config/config.json"

    @classmethod
    def load_config(cls):
        if not os.path.exists(cls.CONFIG_FILE):
            raise FileNotFoundError(f"Config file not found: {cls.CONFIG_FILE}")
        with open(cls.CONFIG_FILE, 'r') as f:
            config = json.load(f)

        # Device auto-detect
        dev = config.get("device", "auto")
        if dev == "auto":
            config["device"] = "cuda" if torch.cuda.is_available() else "cpu"
        else:
            if dev. isdigit():
                config["device"] = dev
            else:
                config["device"] = dev

        return config

    @classmethod
    def save_config(cls, config):
        """Simpan konfigurasi ke file JSON"""
        with open(cls. CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=4)