from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os
from socket import gethostbyname, gethostname
from pathlib import Path

button_style = """
            padding: 5px 15px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-size: 14px;
        """

details_style = """
        cursor: pointer;
        padding: 5px 15px;
        background: #4CAF50;
        color: white;
        border-radius: 20px;
        list-style: none;
    """

background_color = "#1a1a2e"
font_color = "white"
padding_body = "40px"

padding_file = "15px"
file_background_color = "#ffffff10"
file_border_radius = "10px"
file_margin_bottom = "5px"
file_height = "10px"

if len(sys.argv) > 1:
    folder_path = Path(sys.argv[1])
else:
    folder_path = Path(r".")

def create_html_from_folder(path: Path):
    ip = gethostbyname(gethostname())
    is_show_secret_file = False
    is_secret_file = False

    secret_file_html = ""

    with open("index.html", "w") as file:
        file.write(f'<html><head><title>HTTP SERVER</title></head><body style="background: {background_color}; color: {font_color}; font-family: Arial; padding: {padding_body};"><h1 style="text-align: center;">IP: {ip}:8000</h1>')
    file = open("index.html", "a")
    for root, dirs, files in path.walk():
        print("Папка:", root.absolute(), root.relative_to(path))
        print({root.relative_to(path).parts})
        if root.name:
            if root.relative_to(path).parts[0][0] == "." and not is_show_secret_file:
                secret_file_html += f'<details style="background: #ffffff10; border-radius: 10px; padding: 10px;">\n<summary style="{details_style}">Show secret file</summary>'
                is_show_secret_file = True
            if root.relative_to(path).parts[0][0] == ".":
                is_secret_file = True

        if not is_secret_file:
            file.write(f'<p>{root.relative_to(path)}</p>\n<ul style="list-style: none; padding: {padding_body};">')
        else:
            secret_file_html += f'<p>{root.relative_to(path)}</p>\n<ul style="list-style: none; padding: {padding_body};">'
        for name in files:
            file_path = root/name
            print("  файл:", name)
            if not is_secret_file:
                file.write(f'\n<li style="display: flex; justify-content: space-between; align-items: center; padding: {file_height}; margin-bottom: {file_margin_bottom}; background: {file_background_color}; border-radius: {file_border_radius};">')
                file.write(f'\n<span>{name}</span>\n<a href="/download?file={file_path}&name={name}" style="{button_style}">download</a>\n</li>')
            else:
                secret_file_html += f'\n<li style="display: flex; justify-content: space-between; align-items: center; padding: {file_height}; margin-bottom: {file_margin_bottom}; background: {file_background_color}; border-radius: {file_border_radius};">'
                secret_file_html += f'\n<span>{name}</span>\n<a href="/download?file={file_path}&name={name}" style="{button_style}">download</a>\n</li>'
        if not is_secret_file:
            file.write("</ul>")
        else:
            secret_file_html += "</ul>"
        is_secret_file = False
    if is_show_secret_file:
        secret_file_html += "</details>"
    file.write(secret_file_html)
    file.write("</body></html></h1></body></html>")

create_html_from_folder(folder_path)

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            with open("index.html", "r", encoding="utf-8") as f:
                html = f.read()
            self.wfile.write(html.encode("utf-8"))
        elif self.path.startswith('/download'):
            params = parse_qs(urlparse(self.path).query)
            filepath = params.get('file', [None])[0]
            name = params.get('name', [None])[0]

            print(params, filepath, name, self.path)
            if not name:
                name = Path(filepath).name

            if filepath:
                self.send_response(200)
                self.send_header("Content-type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{name}"')
                self.end_headers()
                with open(filepath, "rb") as f:
                    self.wfile.write(f.read())


server = HTTPServer(("0.0.0.0", 8000), MyHandler)
print("Server is start: http://localhost:8000")
server.serve_forever()
