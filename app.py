from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_PLAYER = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>🎬 مشغل البث المباشر</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/plyr@3.7.8/dist/plyr.css">
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/plyr@3.7.8/dist/plyr.polyfilled.js"></script>
    <style>
        body {
            background-color: #000;
            color: white;
            font-family: 'Tahoma', sans-serif;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        h2 {
            margin-top: 15px;
            color: #00ffcc;
        }
        #player-container {
            max-width: 900px;
            margin: 20px auto;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 0 25px rgba(0, 255, 255, 0.3);
        }
        video {
            width: 100%;
            border-radius: 15px;
        }
        .server-list {
            margin: 15px auto;
        }
        .server-btn {
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            background-color: #00cc99;
            color: white;
            margin: 5px;
            cursor: pointer;
            transition: 0.3s;
            font-size: 16px;
        }
        .server-btn:hover {
            background-color: #00ffaa;
        }
        .server-btn.active {
            background-color: #ff0066;
        }
    </style>
</head>
<body>

    <h2>🎬 مشغل بث مباشر</h2>

    <div class="server-list">
        {% for s in servers %}
        <button class="server-btn {% if s == current_server %}active{% endif %}" onclick="switchServer('{{ s }}')">
            {{ s }}
        </button>
        {% endfor %}
    </div>

    <div id="player-container">
        <video id="video" controls autoplay playsinline></video>
    </div>

    <script>
        const video = document.getElementById('video');
        const player = new Plyr(video);
        const url = "{{ stream_url or '' }}";
        const servers = {{ servers|tojson }};
        let currentServer = "{{ current_server }}";

        function playStream(server, link) {
            const serverUrl = server + link;

            if (Hls.isSupported()) {
                const hls = new Hls();
                hls.loadSource(serverUrl);
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    video.play();
                });
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = serverUrl;
                video.addEventListener('loadedmetadata', function() {
                    video.play();
                });
            } else {
                alert('❌ المتصفح لا يدعم تشغيل هذا النوع من البث.');
            }
        }

        function switchServer(server) {
            const params = new URLSearchParams(window.location.search);
            const link = params.get('url');
            if (link) {
                window.location.href = `/player?url=${encodeURIComponent(link)}&server=${encodeURIComponent(server)}`;
            }
        }

        if (url && currentServer) {
            playStream(currentServer, url);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return "<h3 style='color:white;background:black;text-align:center;padding:20px;'>يرجى استخدام /player?url=رابط_الفيديو</h3>"

@app.route('/player')
def player():
    stream_url = request.args.get('url')
    current_server = request.args.get('server', 'Server 1')

    # قائمة السيرفرات (يمكنك تعديلها)
    servers = {
        "Server 1": "",
        "Server 2": "https://proxy1.example.com/?url=",
        "Server 3": "https://proxy2.example.com/?url=",
    }

    return render_template_string(
        HTML_PLAYER,
        stream_url=stream_url,
        servers=list(servers.keys()),
        current_server=current_server
    )

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
