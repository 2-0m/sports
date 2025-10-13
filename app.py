from flask import Flask, render_template_string, request

app = Flask(__name__)

# واجهة HTML مدمجة في Flask
HTML_PLAYER = """
<!DOCTYPE html>
<html lang="ar">
<head>
    <meta charset="UTF-8">
    <title>مشغل البث المباشر</title>
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
            margin-top: 20px;
            color: #00ffcc;
        }
        #player-container {
            max-width: 900px;
            margin: 20px auto;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2);
        }
        video {
            width: 100%;
            border-radius: 15px;
        }
        #input-section {
            margin-top: 25px;
        }
        input[type="text"] {
            width: 70%;
            padding: 10px;
            font-size: 16px;
            border-radius: 10px;
            border: none;
            outline: none;
            text-align: left;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            margin-left: 10px;
            border: none;
            border-radius: 10px;
            background-color: #00cc99;
            color: white;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background-color: #00ffaa;
        }
    </style>
</head>
<body>

    <h2>🎬 مشغل بث مباشر</h2>

    <div id="input-section">
        <form method="get" action="/player">
            <input type="text" name="url" id="streamUrl" placeholder="أدخل رابط البث (m3u8 أو mp4)" value="{{ stream_url or '' }}">
            <button type="submit">تشغيل</button>
        </form>
    </div>

    <div id="player-container">
        <video id="video" controls playsinline></video>
    </div>

    <script>
        const video = document.getElementById('video');
        const player = new Plyr(video);
        const url = "{{ stream_url or '' }}";

        if (url) {
            if (Hls.isSupported()) {
                const hls = new Hls();
                hls.loadSource(url);
                hls.attachMedia(video);
                hls.on(Hls.Events.MANIFEST_PARSED, function() {
                    video.play();
                });
            } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
                video.src = url;
                video.addEventListener('loadedmetadata', function() {
                    video.play();
                });
            } else {
                alert('❌ المتصفح لا يدعم تشغيل هذا النوع من البث.');
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_PLAYER)

@app.route('/player')
def player():
    stream_url = request.args.get('url')
    return render_template_string(HTML_PLAYER, stream_url=stream_url)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
