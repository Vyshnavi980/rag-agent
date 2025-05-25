from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
RAG_API_URL = "http://localhost:8003/generate"

HTML = """
<!doctype html>
<html><head><title>RAG Prompt & File Upload</title></head>
<body style="font-family:Arial; max-width:800px; margin:40px auto; padding:20px; background:#f9f9f9; border-radius:10px;">
<h2>Upload a File and Enter a Prompt</h2>
<form method="post" enctype="multipart/form-data">
  <label>Upload file:</label><br><input type="file" name="file"><br><br>
  <label>Prompt:</label><br><textarea name="prompt" rows="5" style="width:100%;"></textarea><br><br>
  <input type="submit" value="Submit" style="padding:10px 20px; background:#007BFF; color:#fff; border:none; border-radius:6px; cursor:pointer;">
</form>
{% if response %}
  <h3>Response from RAG API:</h3><pre style="background:#eef; padding:15px; border-radius:6px; white-space:pre-wrap;">{{ response }}</pre>
{% endif %}
</body></html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    response = None
    if request.method == "POST":
        prompt = request.form.get("prompt", "").strip()
        if not prompt:
            response = "Please enter a prompt."
        else:
            file = request.files.get("file")
            context_lines = []
            if file:
                try:
                    content = file.read().decode("utf-8")
                    context_lines = [line.strip() for line in content.splitlines() if line.strip()][:50]
                except Exception:
                    response = "Uploaded file is not valid UTF-8 text."
            if not response:
                payload = {
                    "query": prompt,
                    "context": "\n".join(context_lines)  # send as single string
                }
                try:
                    r = requests.post(RAG_API_URL, json=payload)
                    r.raise_for_status()
                    data = r.json()
                    response = data.get("generated_text", "No generated_text found in response.")
                except Exception as e:
                    response = f"Error contacting RAG API: {e}"
    return render_template_string(HTML, response=response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
