#!/usr/bin/env python3
"""Local preview with the same extensionless paths as GitHub Pages."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse


class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        resolved = super().translate_path(path)
        candidate = Path(resolved)
        if not candidate.exists() and not candidate.suffix:
            html = candidate.with_suffix('.html')
            if html.is_file():
                return str(html)
        return resolved


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=4173)
    options = parser.parse_args()
    directory = str(Path(__file__).resolve().parent.parent)
    server = ThreadingHTTPServer(('127.0.0.1', options.port),
        lambda *args, **kwargs: Handler(*args, directory=directory, **kwargs))
    print(f'Local: http://127.0.0.1:{options.port}', flush=True)
    server.serve_forever()
