import os
import json
import subprocess
from flask import Flask, render_template_string, request, jsonify, send_from_directory

app = Flask(__name__, static_folder='.', static_url_path='')

DATA_FILE = os.path.join('photoapp', 'data.json')
IMAGES_DIR = os.path.join('images', 'gallery')

# Ensure git is set up
def git_status():
    try:
        status = subprocess.check_output(['git', 'status', '--porcelain']).decode('utf-8')
        return status
    except subprocess.CalledProcessError:
        return "Git not initialized or error."

def git_commit_and_push(message):
    try:
        subprocess.check_call(['git', 'add', '.'])
        subprocess.check_call(['git', 'commit', '-m', message])
        subprocess.check_call(['git', 'push', 'origin', 'master']) # Assuming master or main
        return True, "Success"
    except subprocess.CalledProcessError as e:
        return False, str(e)

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.route('/admin')
def admin():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    artworks = data.get('artworks', data) if isinstance(data, dict) else data
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Site Manager</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            .artwork-card { margin-bottom: 20px; border: 1px solid #ddd; padding: 15px; border-radius: 5px; }
            .thumb { max-width: 100px; max-height: 100px; }
        </style>
    </head>
    <body class="bg-light">
        <div class="container mt-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h1>Site Manager</h1>
                <div>
                    <a href="/" class="btn btn-secondary" target="_blank">Preview Site</a>
                    <button onclick="publishChanges()" class="btn btn-primary">Publish to GitHub</button>
                </div>
            </div>
            
            <div id="status" class="alert alert-info" style="display:none"></div>

            <div class="card mb-4">
                <div class="card-header">Add New Artwork</div>
                <div class="card-body">
                    <form id="addForm" class="row g-3">
                        <div class="col-md-3">
                            <input type="text" class="form-control" placeholder="Image Filename" id="newImage" required>
                            <small class="text-muted">Must exist in images/gallery/</small>
                        </div>
                        <div class="col-md-3">
                            <input type="text" class="form-control" placeholder="Title" id="newTitle">
                        </div>
                        <div class="col-md-4">
                            <input type="text" class="form-control" placeholder="Description (e.g. Oil on Canvas<br>20x20)" id="newDesc">
                        </div>
                        <div class="col-md-1">
                            <input type="text" class="form-control" placeholder="Year" id="newYear">
                        </div>
                        <div class="col-md-1">
                            <button type="submit" class="btn btn-success">Add</button>
                        </div>
                    </form>
                </div>
            </div>

            <div id="artworks-list">
                {% for art in artworks %}
                <div class="artwork-card bg-white" data-index="{{ loop.index0 }}">
                    <div class="row align-items-center">
                        <div class="col-md-2">
                            <img src="/images/gallery/{{ art.image }}" class="thumb" onerror="this.src='https://via.placeholder.com/100?text=Missing'">
                        </div>
                        <div class="col-md-9">
                            <div class="row mb-2">
                                <div class="col">
                                    <label>Title</label>
                                    <input type="text" class="form-control" value="{{ art.title }}" onchange="updateArt({{ loop.index0 }}, 'title', this.value)">
                                </div>
                                <div class="col">
                                    <label>Year</label>
                                    <input type="text" class="form-control" value="{{ art.year }}" onchange="updateArt({{ loop.index0 }}, 'year', this.value)">
                                </div>
                            </div>
                            <div class="row">
                                <div class="col">
                                    <label>Description</label>
                                    <input type="text" class="form-control" value="{{ art.description }}" onchange="updateArt({{ loop.index0 }}, 'description', this.value)">
                                </div>
                                <div class="col">
                                    <label>Image File</label>
                                    <input type="text" class="form-control" value="{{ art.image }}" onchange="updateArt({{ loop.index0 }}, 'image', this.value)">
                                </div>
                            </div>
                        </div>
                        <div class="col-md-1 text-end">
                            <button class="btn btn-danger btn-sm" onclick="deleteArt({{ loop.index0 }})">&times;</button>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </div>

        <script>
            let artworks = {{ artworks | tojson }};

            function updateArt(index, field, value) {
                artworks[index][field] = value;
                saveData();
            }

            function deleteArt(index) {
                if(confirm('Are you sure?')) {
                    artworks.splice(index, 1);
                    saveData().then(() => location.reload());
                }
            }

            document.getElementById('addForm').addEventListener('submit', function(e) {
                e.preventDefault();
                const newArt = {
                    image: document.getElementById('newImage').value,
                    title: document.getElementById('newTitle').value,
                    description: document.getElementById('newDesc').value,
                    year: document.getElementById('newYear').value
                };
                artworks.unshift(newArt);
                saveData().then(() => location.reload());
            });

            function saveData() {
                return fetch('/admin/save', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({artworks: artworks})
                });
            }

            function publishChanges() {
                const btn = document.querySelector('button[onclick="publishChanges()"]');
                const status = document.getElementById('status');
                btn.disabled = true;
                btn.textContent = 'Publishing...';
                
                fetch('/publish', {method: 'POST'})
                    .then(r => r.json())
                    .then(data => {
                        status.style.display = 'block';
                        status.textContent = data.message;
                        status.className = data.success ? 'alert alert-success' : 'alert alert-danger';
                        btn.disabled = false;
                        btn.textContent = 'Publish to GitHub';
                    });
            }
        </script>
    </body>
    </html>
    """
    return render_template_string(html, artworks=artworks)

@app.route('/admin/save', methods=['POST'])
def save_data():
    new_data = request.json
    # Preserve structure if it was wrapped in "artworks"
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        old_data = json.load(f)
    
    if isinstance(old_data, dict) and 'artworks' in old_data:
        final_data = {'artworks': new_data['artworks']}
    else:
        final_data = new_data['artworks']
        
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(final_data, f, indent=4)
    
    return jsonify({"success": True})

@app.route('/publish', methods=['POST'])
def publish():
    success, msg = git_commit_and_push("Update via Site Manager")
    return jsonify({"success": success, "message": msg})

if __name__ == '__main__':
    print("Starting server at http://localhost:5000")
    print("Admin UI at http://localhost:5000/admin")
    app.run(debug=True, port=5000)
