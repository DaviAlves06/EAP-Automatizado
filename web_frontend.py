"""
Interface web simples para arrastar e soltar arquivos de projeto em XML
e gerar o Excel (sem dependência de MS Project/COM).
Requisitos extras: pip install flask openpyxl
Compatível com ambiente sem MS Project (ex.: Vercel/serverless) usando XML exportado.
Execute localmente com: python web_frontend.py
"""

import os
import tempfile
from datetime import datetime
from xml.etree import ElementTree as ET

import openpyxl
from flask import Flask, jsonify, render_template_string, request, send_from_directory


def get_localname(tag: str) -> str:
    """Extrai o nome local removendo namespace."""
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def parse_ms_date(raw: str) -> str:
    """Converte data do XML do Project para dd/mm/aaaa."""
    if not raw:
        return ""
    try:
        clean = raw.replace("Z", "+00:00")
        dt = datetime.fromisoformat(clean)
        return dt.strftime("%d/%m/%Y")
    except Exception:
        return ""


def sanitize_filename(name: str) -> str:
    """Sanitize the requested Excel filename, enforce .xlsx."""
    base = "".join(c for c in name if c.isalnum() or c in (" ", "-", "_")).strip()
    if not base:
        base = "blocos"
    if not base.lower().endswith(".xlsx"):
        base += ".xlsx"
    return base


def load_tasks_from_xml(xml_path: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    tasks = []

    def first_child_text(el, wanted):
        for child in el:
            if get_localname(child.tag) == wanted:
                return child.text or ""
        return ""

    def find_extended_value(el, field_ids):
        for ext in el.findall(".//"):
            if get_localname(ext.tag) != "ExtendedAttribute":
                continue
            fid = first_child_text(ext, "FieldID")
            if fid and fid.strip() in field_ids:
                val = first_child_text(ext, "Value")
                if val:
                    return val
        return ""

    for t in root.iter():
        if get_localname(t.tag) != "Task":
            continue
        name = first_child_text(t, "Name")
        if not name:
            continue
        outline_number = first_child_text(t, "OutlineNumber") or ""
        outline_level_raw = first_child_text(t, "OutlineLevel") or ""
        try:
            outline_level = int(outline_level_raw) if outline_level_raw else len(outline_number.split(".")) if outline_number else 0
        except Exception:
            outline_level = 0

        number1 = first_child_text(t, "Number1")
        if not number1:
            number1 = find_extended_value(t, {"188743731"})  # Number1 custom field

        tasks.append(
            {
                "uid": first_child_text(t, "UID"),
                "name": name,
                "outline_number": outline_number,
                "outline_level": outline_level,
                "start": parse_ms_date(first_child_text(t, "Start")),
                "finish": parse_ms_date(first_child_text(t, "Finish")),
                "economias": number1,
            }
        )
    return tasks


def find_descendant(tasks, block, keyword: str):
    """Retorna a primeira subtarefa descendente cujo nome contém a keyword."""
    prefix = block["outline_number"]
    base_level = block["outline_level"]
    for t in tasks:
        on = t["outline_number"]
        if not on or not prefix:
            continue
        if not on.startswith(prefix + "."):
            continue
        if t["outline_level"] <= base_level:
            continue
        if keyword.lower() in t["name"].lower():
            return t
    return None


def extract_to_excel(xml_path, output_dir, excel_name: str | None = None):
    """
    Processa o XML exportado do MS Project e gera um Excel.
    Retorna quantidade de blocos e caminho final.
    """
    tasks = load_tasks_from_xml(xml_path)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Blocos e Subtarefas"
    headers = [
        "Bloco",
        "Nível",
        "Início Obras",
        "Término Obras",
        "Início Projeto Executivo",
        "Término Projeto Executivo",
        "Início Imobilização",
        "Término Imobilização",
        "Início Bloco",
        "Término Bloco",
        "Qtd. Econo. Previstas",
    ]
    ws.append(headers)

    blocks = [t for t in tasks if "bloco" in t["name"].lower()]

    for bloco in blocks:
        obra = find_descendant(tasks, bloco, "obra")
        projeto = find_descendant(tasks, bloco, "projeto executivo")
        imob = find_descendant(tasks, bloco, "imobilização")

        ws.append(
            [
                bloco["name"].strip(),
                bloco["outline_level"],
                obra["start"] if obra else "",
                obra["finish"] if obra else "",
                projeto["start"] if projeto else "",
                projeto["finish"] if projeto else "",
                imob["start"] if imob else "",
                imob["finish"] if imob else "",
                bloco["start"],
                bloco["finish"],
                bloco["economias"],
            ]
        )

    base_name = sanitize_filename(excel_name) if excel_name else os.path.splitext(os.path.basename(xml_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_name = f"{base_name.replace('.xlsx','')}_{timestamp}.xlsx"
    os.makedirs(output_dir, exist_ok=True)
    excel_path = os.path.join(output_dir, output_name)
    wb.save(excel_path)
    return len(blocks), excel_path


app = Flask(__name__)

# Em ambientes serverless (ex.: Vercel), /tmp é gravável
BASE_DIR = os.getenv("TMPDIR") or tempfile.gettempdir()
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


HTML_PAGE = """
<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <title>Extração de Blocos (XML do MS Project)</title>
  <style>
    body { font-family: 'Segoe UI', Arial, sans-serif; max-width: 820px; margin: 40px auto; background: #f8f9fb; color: #1f2937; }
    h1 { color: #111827; }
    .card { background: #fff; border-radius: 14px; padding: 28px; box-shadow: 0 12px 35px rgba(0,0,0,0.07); }
    .dropzone {
      border: 2px dashed #3f51b5;
      padding: 48px;
      text-align: center;
      color: #3f51b5;
      border-radius: 12px;
      background: linear-gradient(135deg, #f5f7ff 0%, #f8fbff 100%);
      transition: all 0.2s ease;
    }
    .dropzone.hover { background: #e8ebff; box-shadow: 0 12px 30px rgba(63,81,181,0.1); }
    .row { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 12px; }
    .input-group { flex: 1 1 260px; }
    label { display: block; margin-bottom: 6px; font-weight: 600; color: #374151; }
    input[type="text"] {
      width: 100%; padding: 10px 12px; border: 1px solid #d1d5db; border-radius: 10px;
      font-size: 14px; transition: border 0.2s ease, box-shadow 0.2s ease;
    }
    input[type="text"]:focus { outline: none; border-color: #3f51b5; box-shadow: 0 0 0 3px rgba(63,81,181,0.15); }
    button {
      margin-top: 12px; padding: 10px 16px; cursor: pointer; background: #3f51b5; color: white;
      border: none; border-radius: 10px; font-weight: 600; transition: background 0.2s ease;
    }
    button:hover { background: #3142a6; }
    #status { margin-top: 20px; }
    a { color: #1a73e8; }
  </style>
</head>
<body>
  <div class="card">
    <h1>Extração de Blocos (XML → Excel)</h1>
    <p>Exporte seu projeto do MS Project para XML, depois arraste e solte aqui (ou clique para selecionar). Escolha o nome do Excel antes de gerar.</p>
    <div class="row">
      <div class="input-group">
        <label for="excelName">Nome do Excel (opcional, sem .xlsx)</label>
        <input type="text" id="excelName" placeholder="ex: relatorio_blocos">
      </div>
    </div>
    <div id="dropzone" class="dropzone" style="margin-top:16px;">
      Solte o arquivo XML do MS Project aqui
      <br><br>
      <input type="file" id="fileInput" accept=".xml" style="display:none" />
      <button onclick="document.getElementById('fileInput').click()">Selecionar XML</button>
    </div>
  </div>
  <div id="status"></div>
  <script>
    const dz = document.getElementById('dropzone');
    const input = document.getElementById('fileInput');
    const excelName = document.getElementById('excelName');
    const status = document.getElementById('status');

    function uploadFile(file) {
      const formData = new FormData();
      formData.append('file', file);
      if (excelName.value.trim()) {
        formData.append('excel_name', excelName.value.trim());
      }
      status.innerHTML = 'Processando...';
      fetch('/upload', { method: 'POST', body: formData })
        .then(res => res.json())
        .then(data => {
          if (!data.success) {
            status.innerHTML = '<b>Erro:</b> ' + data.error;
            return;
          }
          status.innerHTML = `
            <p><b>Blocos encontrados:</b> ${data.blocks}</p>
            <p><a href="${data.download_url}">Baixar Excel gerado</a></p>
          `;
        })
        .catch(err => {
          status.innerHTML = '<b>Erro:</b> ' + err;
        });
    }

    dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('hover'); });
    dz.addEventListener('dragleave', () => dz.classList.remove('hover'));
    dz.addEventListener('drop', e => {
      e.preventDefault();
      dz.classList.remove('hover');
      if (e.dataTransfer.files.length) uploadFile(e.dataTransfer.files[0]);
    });
    input.addEventListener('change', e => {
      if (e.target.files.length) uploadFile(e.target.files[0]);
    });
  </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if not file or not file.filename.lower().endswith(".xml"):
        return jsonify(success=False, error="Envie um arquivo XML exportado do MS Project"), 400
    excel_name = request.form.get("excel_name") or ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".xml", dir=UPLOAD_DIR) as tmp:
        file.save(tmp.name)
        temp_path = tmp.name

    try:
        blocks, excel_path = extract_to_excel(temp_path, OUTPUT_DIR, excel_name=excel_name)
        download_name = os.path.basename(excel_path)
        return jsonify(
            success=True,
            blocks=blocks,
            download_url=f"/download/{download_name}",
        )
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(OUTPUT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

