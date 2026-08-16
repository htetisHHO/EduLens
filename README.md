# EduLens

EduLens is a desktop app that verifies educational claims. It runs a PyQt5 window
that loads the HTML/CSS/JS interface in `ui/` and talks to the Python backend
through a `QWebChannel` bridge.

## Requirements

- Python 3.8+
- PyQt5 and PyQtWebEngine
- [Ollama](https://ollama.com/) running locally (used by the chatbot)

```bash
pip install PyQt5 PyQtWebEngine ollama
```

## Running the app

Run `main.py` inside the `ui` folder:

```bash
cd ui
python main.py
```

On Windows you can also double-click `run_EduLens.bat` from the project root.

**Note:** run the app from inside `ui/`. `ui/main.py` imports `bridge` from that
same folder and loads `CB1.html` relative to it, so starting from another
directory will fail to find those modules.

## Project layout

```
EduLens/
├── main.py             # older TruthLens entry point (kept for reference)
├── backend.py
├── run_EduLens.bat     # Windows launcher
└── ui/
    ├── main.py         # ← run this
    ├── bridge.py       # QWebChannel bridge between the UI and Python
    ├── backend.py      # rule-based claim analysis
    ├── chatbot.py      # Ollama-backed claim analysis
    ├── CB1.html ...    # app screens (CB1.html is the first screen)
    ├── login.html
    ├── CreateAccount.html
    ├── LearnMore.html
    ├── css/
    ├── js/
    └── images/
```
