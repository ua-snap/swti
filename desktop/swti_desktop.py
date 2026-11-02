# pylint: disable=C0103,C0413,E0401
"""
Stand-alone desktop entry point for the Statewide Temperature Index.

Serves the Dash app on a private localhost port in a background thread
and shows it in a native macOS window (WebKit, via pywebview).
"""

import os
import sys
import logging
import threading
import webbrowser
from pathlib import Path

APP_NAME = "Alaska Statewide Temperature Index"
BUNDLE_ID = "edu.alaska.uaf.accap.swti"

# Opens links to other sites (UAF, ASOS, GitHub...) in the user's browser
# instead of navigating the app window away from the chart.
EXTERNAL_LINKS_JS = """
if (!window.__swtiExternalLinks) {
    window.__swtiExternalLinks = true;
    document.addEventListener("click", function (event) {
        var link = event.target.closest && event.target.closest("a[href]");
        if (!link || link.hasAttribute("download")) return;
        if (!/^(https?|mailto):$/.test(link.protocol)) return;
        if (link.origin === window.location.origin) return;
        event.preventDefault();
        window.pywebview.api.open_external(link.href);
    }, true);
}
"""


def resource_dir():
    """Directory holding application.py, assets/ and data/."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # pylint: disable=W0212
    return Path(__file__).resolve().parent.parent


def configure_environment():
    """Set up env vars, logging and paths before the Dash app is imported."""
    cache_dir = Path.home() / "Library" / "Caches" / BUNDLE_ID
    downloads_dir = cache_dir / "downloads"
    downloads_dir.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("SWTI_DESKTOP", "1")
    os.environ.setdefault("SWTI_DOWNLOADS_DIR", str(downloads_dir))

    level = getattr(
        logging, os.getenv("DASH_LOG_LEVEL", "info").upper(), logging.INFO
    )
    if getattr(sys, "frozen", False):
        # The packaged app always shows live data, even if a developer's
        # shell environment (inherited via `open`) has FLASK_DEBUG set.
        os.environ.pop("FLASK_DEBUG", None)

        # A frozen app has no usable stdout, so log to ~/Library/Logs and
        # use certifi's CA bundle for any HTTPS requests.
        import certifi

        os.environ.setdefault("SSL_CERT_FILE", certifi.where())
        log_dir = Path.home() / "Library" / "Logs" / APP_NAME
        log_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=log_dir / "swti.log",
            filemode="w",
            level=level,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        )
    else:
        logging.basicConfig(level=level)

    root = str(resource_dir())
    os.chdir(root)
    if root not in sys.path:
        sys.path.insert(0, root)


class Api:  # pylint: disable=R0903
    """Functions exposed to the page as window.pywebview.api.*"""

    def open_external(self, url):
        """Open a link in the default browser."""
        if url.startswith(("http://", "https://", "mailto:")):
            webbrowser.open(url)


def start_server(wsgi_app):
    """Serve the app on a free localhost port; returns its URL."""
    from werkzeug.serving import make_server

    server = make_server("127.0.0.1", 0, wsgi_app, threaded=True)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_port}/"
    logging.info("Serving %s at %s", APP_NAME, url)
    return url


def main():
    configure_environment()

    import webview
    from application import application

    url = start_server(application)

    webview.settings["ALLOW_DOWNLOADS"] = True
    window = webview.create_window(
        APP_NAME,
        url,
        js_api=Api(),
        width=1200,
        height=900,
        min_size=(720, 600),
    )
    window.events.loaded += lambda: window.evaluate_js(EXTERNAL_LINKS_JS)
    webview.start()


if __name__ == "__main__":
    main()
