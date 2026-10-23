import time

from flask import Flask, redirect, render_template, request, abort, jsonify, Response, g
import os

app = Flask(__name__)


@app.before_request
def start_request_timer():
    g.request_started_at = time.perf_counter()


@app.after_request
def add_server_timing(response):
    duration_ms = (time.perf_counter() - g.request_started_at) * 1000
    response.headers.add('Server-Timing', f'app;dur={duration_ms:.2f}')
    return response


@app.route('/invite')
def invite():
    return redirect('https://discord.com/oauth2/authorize?client_id=844489130822074390&permissions=313344&scope=bot')

@app.route('/video')
def video():
    video_url = request.args.get('url')
    text = request.args.get('text')
    image = request.args.get('image')
    if video_url:
        # File names are IDs, so only show a name when one is given (e.g. the skin variant name)
        title = text or "Video"
        description = os.path.splitext(os.path.basename(video_url))[1]
        if not description:
            description = "Video file"
        if not image:
            image = ""
        return render_template('video.html', video_url=video_url, title=title, description=description, image=image,
                               text=text)
    else:
        if os.getenv("RAILWAY_ENVIRONMENT_NAME"):
            return redirect("/", code=302)
        else:
            return abort(400, "Missing url parameter")

@app.route('/freevalorantpoints')
@app.route('/freevalorantpoints.html')
def freevalorantpoints():
    return render_template('freevp.html', target=request.args.get('target'))

@app.route('/cd')
def cheater_detected():
    return render_template('cd.html')

@app.route('/privacy')
@app.route('/privacy.html')
def privacy():
    return redirect('https://nogra.app/privacy', code=301)


@app.route('/terms')
@app.route('/terms.html')
def terms():
    return redirect('https://nogra.app/terms', code=301)


@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/index')
def index_2():
    return redirect('/')


@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nAllow: /\n\nSitemap: https://cypherslaptop.nogra.app/sitemap.xml\n",
                    mimetype='text/plain')


@app.route('/sitemap.xml')
def sitemap():
    return Response('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                    '  <url><loc>https://cypherslaptop.nogra.app/</loc></url>\n'
                    '</urlset>\n', mimetype='application/xml')


@app.route('/status')
def get_status():
    current_time = time.time()
    start_time = app.config['START_TIME']

    # Calculate the uptime in seconds, minutes, and hours
    uptime_seconds = int(current_time - start_time)
    uptime_minutes, uptime_seconds = divmod(uptime_seconds, 60)
    uptime_hours, uptime_minutes = divmod(uptime_minutes, 60)

    # Create the JSON object with the status information
    status = {
        "status": "OK",
        "uptime": f"{uptime_hours} hours, {uptime_minutes} minutes, {uptime_seconds} seconds",
        "last_restart": app.config['START_TIME']
    }

    # Return the JSON object as the response
    return jsonify(status)


if __name__ == '__main__':
    # from waitress import serve
    app.config['START_TIME'] = time.time()
    app.run(host="0.0.0.0", port=8080)
