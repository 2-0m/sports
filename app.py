from flask import Flask, render_template_string, request

app = Flask(__name__)

HTML_PLAYER = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>🎬 مشغل بث مباشر متعدد السيرفرات</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/plyr@3.7.8/dist/plyr.css">
    <link href="https://vjs.zencdn.net/7.21.1/video-js.css" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <script src="https://cdn.jsdelivr.net/npm/plyr@3.7.8/dist/plyr.polyfilled.js"></script>
    <script src="https://vjs.zencdn.net/7.21.1/video.min.js"></script>
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

    <h2>🎬 مشغل بث مباشر متعدد السيرفرات</h2>

    <div class="server-list">
        {% for s in servers %}
        <button class="server-btn {% if s == current_server %}active{% endif %}" onclick="switchServer('{{ s }}', this)">
            {{ s }}
        </button>
        {% endfor %}
    </div>

    <div id="player-container">
        <div id="player-area"></div>
    </div>

    <script>
        const servers = {{ servers_json | safe }};
        const streamLink = "{{ stream_url or '' }}";
        let currentPlayer = null;
        let hls = null;

        // وظيفة إنشاء المشغل حسب نوع السيرفر
        function loadPlayer(serverName) {
            const base = servers[serverName].base || "";
            const type = servers[serverName].type;
            const fullUrl = base ? base + streamLink : streamLink;
            const container = document.getElementById("player-area");
            container.innerHTML = ""; // تنظيف المنطقة

            if (!streamLink) {
                container.innerHTML = "<p style='color:red'>⚠️ لم يتم تمرير رابط البث.</p>";
                return;
            }

            // إزالة أي مشغل سابق
            if (hls) { hls.destroy(); hls = null; }
            if (currentPlayer && currentPlayer.destroy) { currentPlayer.destroy(); }

            if (type === "plyr") {
                const video = document.createElement("video");
                video.id = "plyr-player";
                video.setAttribute("controls", "");
                video.setAttribute("autoplay", "");
                container.appendChild(video);

                const player = new Plyr(video);
                currentPlayer = player;

                if (Hls.isSupported()) {
                    hls = new Hls();
                    hls.loadSource(fullUrl);
                    hls.attachMedia(video);
                    hls.on(Hls.Events.MANIFEST_PARSED, () => video.play());
                } else {
                    video.src = fullUrl;
                    video.play();
                }

            } else if (type === "videojs") {
                const video = document.createElement("video");
                video.id = "videojs-player";
                video.className = "video-js vjs-default-skin";
                video.setAttribute("controls", "");
                video.setAttribute("autoplay", "");
                video.setAttribute("preload", "auto");
                video.innerHTML = `<source src="${fullUrl}" type="application/x-mpegURL">`;
                container.appendChild(video);

                currentPlayer = videojs(video, {
                    fluid: true,
                    autoplay: true,
                    controls: true
                });

            } else if (type === "native") {
                const video = document.createElement("video");
                video.id = "native-player";
                video.setAttribute("controls", "");
                video.setAttribute("autoplay", "");
                video.src = fullUrl;
                container.appendChild(video);
                video.play();
            }
        }

        function switchServer(serverName, btn) {
            document.querySelectorAll('.server-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            loadPlayer(serverName);
        }

        // التشغيل الافتراضي
        window.onload = () => {
            loadPlayer("{{ current_server }}");
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return "<h3 style='color:white;background:black;text-align:center;padding:20px;'>Mustafa Abbas</h3>"

@app.route('/player')
def player():
    stream_url = request.args.get('url')
    current_server = request.args.get('server', 'Server 1')

    # كل سيرفر له مشغل خاص
    servers = {
        "Server 1": {"type": "plyr", "base": ""},
        "Server 2": {"type": "videojs", "base": ""},
        "Server 3": {"type": "native", "base": ""},
    }

    return render_template_string(
        HTML_PLAYER,
        stream_url=stream_url,
        servers=list(servers.keys()),
        servers_json=servers,
        current_server=current_server
    )

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
