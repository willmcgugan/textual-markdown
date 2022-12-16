import sys

from .browser_app import BrowserApp


if __name__ == "__main__":

    try:
        path = sys.argv[1]
    except Exception:
        path = "README.md"
    app = BrowserApp(path)
    app.run()
