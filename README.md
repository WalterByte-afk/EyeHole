<div align="center">
  <img src="assets/banner.jpg" alt="EyeHole Banner" width="100%">
  
  # 👁️ EyeHole Framework
  **Advanced ctOS Central Interface & Tool Manager**
  
  [![Python](https://img.shields.io/badge/Python-3.8+-cyan.svg?style=for-the-badge&logo=python)](https://www.python.org/)
  [![Platform](https://img.shields.io/badge/Platform-Termux%20%7C%20Windows%20%7C%20Linux-red.svg?style=for-the-badge)]()
  [![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)]()
</div>

<br>

EyeHole is an extensible, modular command-line framework designed with a sleek, Watch Dogs / DedSec aesthetic. It allows users to dynamically load, manage, and execute custom scripts and utilities from a centralized dashboard.

## 🚀 Features

- **Dynamic Module Loading:** Link any local script or binary to the dashboard on the fly.
- **ctOS Glitch UI:** Built-in terminal matrix glitch effects, centered ASCII art, and hardware beep SFX.
- **Auto-Grab Protocol:** Automatically intercepts the newest photo from your device's camera roll (Termux & Windows support) for seamless image-processing workflows.
- **Dynamic Variable Injection:** Pass `{INPUT}` (Usernames, IP addresses) or `{TARGET_IMAGE}` directly into your tools at runtime.

## ⚙️ Installation

```bash
git clone https://github.com/WalterByte-afk/EyeHole.git
cd EyeHole
python eyehole_framework.py
```

## 🛠️ How to Add Tools

The framework is completely empty by design. You construct your own arsenal.

1. Clone your favorite tools into the `tools/` directory.
2. Boot up EyeHole and press `[A] Add New Module`.
3. Provide the execution command using placeholders.

**Example: Adding an OSINT Username tool**
> Execution Command: `python tools/sherlock/sherlock.py {INPUT}`
> *EyeHole will automatically prompt you for the target name and inject it into `{INPUT}`!*

## ⚠️ Disclaimer
This framework is provided for educational and diagnostic purposes only. Users are responsible for ensuring that they have permission to execute tools linked within the framework.

---
<div align="center">
  <i>"JOIN YES? Y=YES N=NO"</i>
</div>
