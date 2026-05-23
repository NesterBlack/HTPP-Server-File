from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import sys
import os
from socket import gethostbyname, gethostname
import pathlib

dirs_ignor = [r".git", r".venv", r".idea"]

button_style = """
            padding: 5px 15px;
            background: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 20px;
            font-size: 14px;
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
    folder_path = sys.argv[1]
else:
    folder_path = "."

def create_html_from_folder(path):
    ip = gethostbyname(gethostname())
    with open("index.html", "w") as file:
        file.write(f'<html><head><title>HTTP SERVER</title></head><body style="background: {background_color}; color: {font_color}; font-family: Arial; padding: {padding_body};"><h1 style="text-align: center;">IP: {ip}:8000</h1>')
    file = open("index.html", "a")
    folders_count = 0
    for root, dirs, files in os.walk(path):
        if all(dir not in root for dir in dirs_ignor):
            print("Папка:", root)
            folders_count += 1
            file.write(f'<p>{root}</p>\n<ul style="list-style: none; padding: {padding_body};">')
            for name in files:
                file_path = root + rf"\{name}"
                print("  файл:", name)
                file.write(f'\n<li style="display: flex; justify-content: space-between; align-items: center; padding: {file_height}; margin-bottom: {file_margin_bottom}; background: {file_background_color}; border-radius: {file_border_radius};">')
                file.write(f'\n<span>{name}</span>\n<a href="/download?file={file_path}&name={name}" style="{button_style}">download</a>\n</li>')
            file.write("</ul>")

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
                name = pathlib.Path(filepath).name

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
