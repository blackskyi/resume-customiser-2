#!/usr/bin/env python3
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os, sys, tempfile, shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, 'edited_resumes')
os.makedirs(OUTPUT_DIR, exist_ok=True)
sys.path.insert(0, SCRIPT_DIR)

from resume_updater import ResumeUpdater

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return '<script>window.location.href="/ui";</script>'

@app.route("/ui")
def serve_ui():
    return """<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Resume Customizer</title><style>* { margin: 0; padding: 0; box-sizing: border-box; } body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; } .container { background: white; border-radius: 15px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); padding: 40px; max-width: 600px; width: 100%; } h1 { color: #333; margin-bottom: 10px; text-align: center; } .subtitle { color: #999; text-align: center; margin-bottom: 30px; font-size: 14px; } .upload-box { border: 2px dashed #667eea; padding: 40px; text-align: center; cursor: pointer; border-radius: 10px; margin-bottom: 20px; transition: all 0.3s; } .upload-box:hover { border-color: #764ba2; background: #f9f7ff; } .upload-box input { display: none; } .upload-icon { font-size: 50px; margin-bottom: 10px; } .upload-text { color: #333; font-weight: bold; margin-bottom: 5px; } .file-info { color: #28a745; margin-top: 10px; font-size: 14px; } textarea { width: 100%; height: 150px; padding: 15px; border: 2px solid #e0e0e0; border-radius: 10px; margin-bottom: 20px; font-family: Arial; font-size: 14px; resize: vertical; } textarea:focus { outline: none; border-color: #667eea; } .button-group { display: flex; gap: 15px; margin-bottom: 20px; } button { flex: 1; padding: 12px; border: none; border-radius: 10px; font-weight: bold; cursor: pointer; font-size: 16px; transition: all 0.3s; } .btn-customize { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; } .btn-customize:hover { transform: translateY(-2px); box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3); } .btn-reset { background: #f0f0f0; color: #333; } .btn-reset:hover { background: #e0e0e0; } .status-box { padding: 15px; border-radius: 10px; display: none; margin-top: 20px; text-align: center; font-size: 14px; line-height: 1.6; } .status-box.show { display: block; } .success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; } .error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }</style></head><body><div class="container"><h1>📄 Resume Customizer</h1><p class="subtitle">Upload your resume and paste job requirements to customize it instantly</p><div class="upload-box" id="uploadBox"><div class="upload-icon">📎</div><div class="upload-text">Click to select resume (.docx)</div><div class="upload-text" style="font-size: 12px; color: #999; margin-top: 5px;">or drag & drop</div><div class="file-info" id="fileName"></div></div><input type="file" id="fileInput" accept=".docx"><textarea id="requirements" placeholder="Paste your job requirements or job description here..."></textarea><div class="button-group"><button class="btn-customize" id="customizeBtn">✨ Customize Resume</button><button class="btn-reset" id="resetBtn">🔄 Reset</button></div><div class="status-box" id="statusBox"></div></div><script>const uploadBox = document.getElementById('uploadBox');const fileInput = document.getElementById('fileInput');const requirements = document.getElementById('requirements');const customizeBtn = document.getElementById('customizeBtn');const resetBtn = document.getElementById('resetBtn');const statusBox = document.getElementById('statusBox');const fileName = document.getElementById('fileName');uploadBox.addEventListener('click', () => { fileInput.click(); });fileInput.addEventListener('change', () => {fileName.textContent = fileInput.files[0] ? '✓ ' + fileInput.files[0].name : '';});uploadBox.addEventListener('dragover', (e) => {e.preventDefault();uploadBox.style.borderColor = '#764ba2';uploadBox.style.background = '#f9f7ff';});uploadBox.addEventListener('dragleave', () => {uploadBox.style.borderColor = '#667eea';uploadBox.style.background = 'white';});uploadBox.addEventListener('drop', (e) => {e.preventDefault();uploadBox.style.borderColor = '#667eea';uploadBox.style.background = 'white';fileInput.files = e.dataTransfer.files;if (fileInput.files[0]) {fileName.textContent = '✓ ' + fileInput.files[0].name;}});customizeBtn.addEventListener('click', async () => {if (!fileInput.files[0] || !requirements.value) {statusBox.textContent = '⚠️ Please select a resume file and paste requirements';statusBox.className = 'status-box show error';return;}customizeBtn.disabled = true;statusBox.textContent = '⏳ Processing your resume...';statusBox.className = 'status-box show';const formData = new FormData();formData.append('resume', fileInput.files[0]);formData.append('requirements', requirements.value);try {const response = await fetch('/api/customize-resume', {method: 'POST',body: formData});const data = await response.json();if (data.success) {const filename = data.filePath.split('/').pop(); const downloadLink = document.createElement('a'); downloadLink.href = '/api/download-resume/' + encodeURIComponent(filename); downloadLink.download = filename; document.body.appendChild(downloadLink); downloadLink.click(); document.body.removeChild(downloadLink); statusBox.innerHTML = '✅ Resume customized and downloaded!<br>📁 File: <strong>' + filename + '</strong>';statusBox.className = 'status-box show success';} else {statusBox.textContent = '❌ Error: ' + data.message;statusBox.className = 'status-box show error';}} catch (error) {statusBox.textContent = '❌ Error: ' + error.message;statusBox.className = 'status-box show error';} finally {customizeBtn.disabled = false;}});resetBtn.addEventListener('click', () => {fileInput.value = '';requirements.value = '';fileName.textContent = '';statusBox.className = 'status-box';});</script></body></html>"""

@app.route('/api/customize-resume', methods=['POST'])
def customize_resume():
    try:
        if 'resume' not in request.files or 'requirements' not in request.form:
            return jsonify({'success': False, 'message': 'Missing resume or requirements'})
        resume_file = request.files['resume']
        requirements_text = request.form['requirements']
        if resume_file.filename == '':
            return jsonify({'success': False, 'message': 'No file selected'})
        temp_dir = tempfile.mkdtemp()
        temp_resume_path = os.path.join(temp_dir, resume_file.filename)
        resume_file.save(temp_resume_path)
        updater = ResumeUpdater(temp_resume_path, OUTPUT_DIR)
        output_file = updater.update_resume(requirements_text)
        if not output_file or not os.path.exists(output_file):
            shutil.rmtree(temp_dir)
            return jsonify({'success': False, 'message': 'Failed to process resume'})
        shutil.rmtree(temp_dir)
        return jsonify({'success': True, 'filePath': output_file, 'message': 'Resume customized successfully'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'success': False, 'message': str(e)})


@app.route('/api/download-resume/<filename>')
def download_resume(filename):
    try:
        file_path = os.path.join(OUTPUT_DIR, filename)
        if not os.path.abspath(file_path).startswith(os.path.abspath(OUTPUT_DIR)):
            return jsonify({'success': False, 'message': 'Invalid file'}), 400
        if not os.path.exists(file_path):
            return jsonify({'success': False, 'message': 'File not found'}), 404
        return send_file(file_path, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
    except Exception as e:
        print(f'Download error: {str(e)}')
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'service': 'resume-customizer'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    print('='*60)
    print('RESUME CUSTOMIZER - PRODUCTION')
    print('='*60)
    print(f'📁 Output folder: {OUTPUT_DIR}')
    print(f'🌐 Running on: 0.0.0.0:{port}')
    print('='*60)
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
