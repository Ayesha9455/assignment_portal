import json, os
from datetime import datetime
from urllib.parse import urlparse
from flask import Flask, request, render_template_string, redirect, url_for

CSS = """
:root{--ink:#0f172a;--muted:#64748b;--line:#e8eaf3;--p1:#6366f1;--p2:#8b5cf6;--p3:#06b6d4;--ok:#10b981}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:"Segoe UI",system-ui,-apple-system,Roboto,Arial,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}
a{text-decoration:none;color:inherit}
svg.i{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:none}

/* ---------- PAGE 1 : FORM ---------- */
body.form-page{min-height:100vh;display:grid;place-items:center;padding:28px 16px;position:relative;overflow-x:hidden;
  background:radial-gradient(circle at 15% 20%,#312e81 0,transparent 45%),radial-gradient(circle at 85% 80%,#0e7490 0,transparent 45%),#0b1020}
.blob{position:absolute;border-radius:50%;filter:blur(70px);opacity:.55;animation:float 14s ease-in-out infinite}
.b1{width:340px;height:340px;background:#6366f1;top:-80px;left:-60px}
.b2{width:300px;height:300px;background:#06b6d4;bottom:-90px;right:-40px;animation-delay:-5s}
.b3{width:220px;height:220px;background:#a855f7;top:55%;left:55%;animation-delay:-9s}
@keyframes float{0%,100%{transform:translate(0,0) scale(1)}50%{transform:translate(30px,-30px) scale(1.12)}}
.shell{position:relative;z-index:1;display:grid;grid-template-columns:1.05fr 1fr;width:min(1040px,100%);background:#fff;
  border-radius:28px;overflow:hidden;box-shadow:0 40px 90px rgba(0,0,0,.5);animation:rise .7s ease both}
@keyframes rise{from{opacity:0;transform:translateY(24px)}to{opacity:1;transform:none}}
.brand-side{position:relative;overflow:hidden;color:#fff;padding:46px 42px;display:flex;flex-direction:column;
  background:linear-gradient(155deg,#4338ca,#7c3aed 55%,#0891b2)}
.brand-side:before,.brand-side:after{content:"";position:absolute;border-radius:50%;background:rgba(255,255,255,.08)}
.brand-side:before{width:320px;height:320px;right:-120px;top:-100px}
.brand-side:after{width:240px;height:240px;left:-90px;bottom:-80px}
.brand-side>*{position:relative;z-index:1}
.logo{display:flex;align-items:center;gap:12px;margin-bottom:34px}
.logo .mark{width:48px;height:48px;border-radius:14px;background:rgba(255,255,255,.18);display:grid;place-items:center;backdrop-filter:blur(6px)}
.logo .mark svg{width:26px;height:26px}
.logo small{display:block;opacity:.8;font-size:.78rem;letter-spacing:.04em}
.logo b{font-size:.98rem}
.brand-side h1{font-size:2.15rem;line-height:1.15;font-weight:800;margin-bottom:12px}
.brand-side .lead{opacity:.88;line-height:1.55;margin-bottom:30px;max-width:380px}
.steps{list-style:none;display:grid;gap:16px;margin-bottom:auto}
.steps li{display:flex;gap:14px;align-items:center;background:rgba(255,255,255,.12);padding:12px 14px;border-radius:14px;backdrop-filter:blur(6px)}
.steps .n{width:32px;height:32px;border-radius:50%;background:#fff;color:#4338ca;font-weight:800;display:grid;place-items:center;flex:none}
.steps span{font-size:.93rem}
.course{margin-top:30px;font-size:.82rem;opacity:.8;display:flex;align-items:center;gap:8px}
.form-side{padding:46px 44px}
.stepper{display:flex;align-items:center;gap:10px;font-size:.8rem;font-weight:700;color:var(--p1);margin-bottom:10px;letter-spacing:.05em;text-transform:uppercase}
.bar{height:6px;border-radius:99px;background:#eef0fb;overflow:hidden;margin-bottom:22px}
.bar i{display:block;height:100%;width:50%;background:linear-gradient(90deg,var(--p1),var(--p3));border-radius:99px}
.form-side h2{font-size:1.6rem;margin-bottom:6px}
.form-side .sub{color:var(--muted);margin-bottom:22px;font-size:.95rem}
.alert{display:flex;gap:10px;align-items:flex-start;background:#fef2f2;color:#b91c1c;border:1px solid #fecaca;
  padding:11px 14px;border-radius:12px;margin-bottom:10px;font-size:.9rem;animation:shake .4s}
@keyframes shake{0%,100%{transform:translateX(0)}25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}
.field{margin-top:16px}
.field label{display:block;font-weight:600;font-size:.85rem;margin-bottom:7px;color:#334155}
.input{position:relative}
.input svg{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:#94a3b8;transition:color .2s}
.input input{width:100%;padding:13px 14px 13px 44px;font-size:.96rem;border:1.5px solid var(--line);border-radius:12px;background:#f8f9fe;color:var(--ink);transition:all .2s}
.input input::placeholder{color:#a3adc2}
.input input:focus{outline:none;border-color:var(--p1);background:#fff;box-shadow:0 0 0 4px rgba(99,102,241,.15)}
.input:focus-within svg{color:var(--p1)}
.btn{margin-top:26px;width:100%;display:flex;align-items:center;justify-content:center;gap:10px;padding:15px;border:0;border-radius:14px;cursor:pointer;
  font-size:1.02rem;font-weight:700;color:#fff;background:linear-gradient(90deg,var(--p1),var(--p2) 55%,var(--p3));
  box-shadow:0 12px 28px rgba(99,102,241,.4);transition:transform .15s,box-shadow .15s}
.btn:hover{transform:translateY(-2px);box-shadow:0 18px 34px rgba(99,102,241,.5)}
.btn:active{transform:translateY(0)}
.hint{display:flex;gap:8px;align-items:center;justify-content:center;margin-top:16px;color:var(--muted);font-size:.8rem}
.hint svg{width:15px;height:15px}
.viewlink{display:block;text-align:center;margin-top:12px;font-size:.88rem;color:var(--p1);font-weight:600}
.viewlink:hover{text-decoration:underline}
@media(max-width:880px){.shell{grid-template-columns:1fr}.brand-side{padding:32px 26px}.form-side{padding:32px 26px}.brand-side h1{font-size:1.7rem}}

/* ---------- PAGE 2 : SUBMISSIONS ---------- */
body.list-page{background:#f4f6fc;min-height:100vh}
.top{background:linear-gradient(120deg,#1e1b4b,#4338ca 55%,#7c3aed);color:#fff;padding:22px 24px 120px;position:relative;overflow:hidden}
.top:before{content:"";position:absolute;width:420px;height:420px;border-radius:50%;background:rgba(255,255,255,.07);right:-120px;top:-200px}
.wrap{max-width:1120px;margin:0 auto;position:relative}
.nav{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap}
.nav .logo{margin:0}
.navbtn{display:inline-flex;align-items:center;gap:8px;background:#fff;color:#4338ca;font-weight:700;padding:11px 18px;border-radius:12px;font-size:.92rem;transition:transform .15s}
.navbtn:hover{transform:translateY(-2px)}
.top h1{margin-top:34px;font-size:2rem;font-weight:800}
.top p{opacity:.85;margin-top:6px}
.stepper.light{color:#c7d2fe;margin:26px 0 0}
main{max-width:1120px;margin:-84px auto 40px;padding:0 24px;position:relative}
.success{display:flex;gap:20px;align-items:center;background:#fff;border-radius:20px;padding:22px 26px;margin-bottom:22px;
  box-shadow:0 14px 40px rgba(30,27,75,.14);border:1px solid #bbf7d0;animation:rise .6s ease both}
.tick{width:62px;height:62px;border-radius:50%;background:linear-gradient(135deg,#34d399,#059669);display:grid;place-items:center;flex:none;box-shadow:0 10px 24px rgba(5,150,105,.4)}
.tick svg{width:32px;height:32px;fill:none;stroke:#fff;stroke-width:3.2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:40;stroke-dashoffset:40;animation:draw .7s .3s ease forwards}
@keyframes draw{to{stroke-dashoffset:0}}
.success h3{font-size:1.15rem;margin-bottom:3px}
.success p{color:var(--muted);font-size:.93rem}
.success b{color:var(--ink)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px;margin-bottom:22px}
.stat{background:#fff;border-radius:18px;padding:20px;display:flex;gap:16px;align-items:center;box-shadow:0 10px 30px rgba(30,27,75,.08)}
.stat .ic{width:52px;height:52px;border-radius:14px;display:grid;place-items:center;color:#fff;flex:none}
.stat .ic svg{width:24px;height:24px}
.stat .num{font-size:1.6rem;font-weight:800;line-height:1.1}
.stat .lbl{color:var(--muted);font-size:.85rem;margin-top:2px}
.card{background:#fff;border-radius:20px;box-shadow:0 10px 30px rgba(30,27,75,.08);overflow:hidden}
.toolbar{display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;padding:22px 24px;border-bottom:1px solid var(--line)}
.toolbar h2{font-size:1.2rem;display:flex;align-items:center;gap:10px}
.count{background:#eef0ff;color:#4338ca;font-size:.78rem;font-weight:700;padding:3px 10px;border-radius:99px}
.search{position:relative;min-width:260px}
.search svg{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#94a3b8;width:18px;height:18px}
.search input{width:100%;padding:11px 14px 11px 40px;border:1.5px solid var(--line);border-radius:12px;background:#f8f9fe;font-size:.92rem}
.search input:focus{outline:none;border-color:var(--p1);background:#fff;box-shadow:0 0 0 4px rgba(99,102,241,.14)}
.scroll{overflow-x:auto}
table{width:100%;border-collapse:collapse;min-width:760px}
th{text-align:left;font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;color:#8591a8;background:#fafbff;padding:13px 20px}
td{padding:16px 20px;border-top:1px solid var(--line);font-size:.93rem;vertical-align:middle}
tbody tr{transition:background .15s}
tbody tr:hover{background:#f7f8ff}
.idx{color:#9aa5bb;font-weight:700}
.who{display:flex;align-items:center;gap:12px;font-weight:600}
.av{width:38px;height:38px;border-radius:50%;color:#fff;display:grid;place-items:center;font-weight:800;flex:none}
.reg{display:inline-block;background:#eef0ff;color:#4338ca;font-weight:700;font-size:.8rem;padding:5px 11px;border-radius:99px;letter-spacing:.02em}
.open{display:inline-flex;align-items:center;gap:6px;color:#4338ca;font-weight:700;font-size:.85rem;background:#f1f2ff;padding:7px 12px;border-radius:10px}
.open:hover{background:#e0e3ff}
.open svg{width:15px;height:15px}
.when{color:var(--muted);font-size:.86rem;white-space:nowrap}
.empty{text-align:center;padding:60px 20px;color:var(--muted)}
.empty .big{width:76px;height:76px;margin:0 auto 14px;border-radius:50%;background:#eef0ff;display:grid;place-items:center;color:#6366f1}
.empty .big svg{width:34px;height:34px}
.empty h3{color:var(--ink);margin-bottom:6px}
.empty .navbtn{margin-top:18px;background:linear-gradient(90deg,var(--p1),var(--p2));color:#fff}
footer{text-align:center;color:#94a3b8;font-size:.82rem;padding:0 0 28px}
"""

ICON_USER = '<svg class="i" viewBox="0 0 24 24"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
ICON_ID = '<svg class="i" viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="11" r="2"/><path d="M15 9h3M15 13h3M6 17c.5-1.5 1.7-2 3-2s2.5.5 3 2"/></svg>'
ICON_FILE = '<svg class="i" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8"/></svg>'
ICON_LINK = '<svg class="i" viewBox="0 0 24 24"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>'
ICON_CAP = '<svg class="i" viewBox="0 0 24 24"><path d="M22 10 12 5 2 10l10 5 10-5z"/><path d="M6 12v5c3 2.5 9 2.5 12 0v-5"/></svg>'
ICON_ARROW = '<svg class="i" viewBox="0 0 24 24"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ICON_LOCK = '<svg class="i" viewBox="0 0 24 24"><rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>'
ICON_ALERT = '<svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>'
ICON_PLUS = '<svg class="i" viewBox="0 0 24 24"><path d="M12 5v14M5 12h14"/></svg>'
ICON_SEARCH = '<svg class="i" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>'
ICON_EXT = '<svg class="i" viewBox="0 0 24 24"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6M15 3h6v6M10 14 21 3"/></svg>'
ICON_USERS = '<svg class="i" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/></svg>'
ICON_CLOCK = '<svg class="i" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>'
ICON_INBOX = '<svg class="i" viewBox="0 0 24 24"><path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>'

HEAD = ("""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Assignment Submission Portal | CUI Attock</title>
<style>""" + CSS + "</style></head>")

FORM_PAGE = HEAD + """
<body class="form-page">
<div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>
<div class="shell">
  <aside class="brand-side">
    <div class="logo"><div class="mark">""" + ICON_CAP + """</div>
      <div><b>COMSATS University Islamabad</b><small>ATTOCK CAMPUS</small></div></div>
    <h1>Assignment<br>Submission Portal</h1>
    <p class="lead">A fast and simple way to hand in your work. Share your link, hit submit, and you are done.</p>
    <ul class="steps">
      <li><span class="n">1</span><span>Enter your name and registration number</span></li>
      <li><span class="n">2</span><span>Add the assignment title and your submission link</span></li>
      <li><span class="n">3</span><span>Submit and see your confirmation</span></li>
    </ul>
    <div class="course">""" + ICON_FILE + """ DevOps for Cloud Computing &middot; CSC418</div>
  </aside>

  <section class="form-side">
    <div class="stepper">Step 1 of 2</div>
    <div class="bar"><i></i></div>
    <h2>Student details</h2>
    <p class="sub">Fill in all the fields below to submit your assignment.</p>
    {% for e in errors %}<div class="alert">""" + ICON_ALERT + """<span>{{ e }}</span></div>{% endfor %}
    <form method="post" action="/submit" novalidate>
      <div class="field"><label for="name">Full name</label>
        <div class="input">""" + ICON_USER + """<input id="name" name="name" placeholder="e.g. Ayesha Shahzad" value="{{ form.name }}"></div></div>
      <div class="field"><label for="reg_no">Registration number</label>
        <div class="input">""" + ICON_ID + """<input id="reg_no" name="reg_no" placeholder="e.g. SP23-BCS-005" value="{{ form.reg_no }}"></div></div>
      <div class="field"><label for="title">Assignment title</label>
        <div class="input">""" + ICON_FILE + """<input id="title" name="title" placeholder="e.g. DevOps Lab Mid" value="{{ form.title }}"></div></div>
      <div class="field"><label for="url">Submission URL</label>
        <div class="input">""" + ICON_LINK + """<input id="url" name="url" placeholder="https://github.com/username/repo" value="{{ form.url }}"></div></div>
      <button class="btn" type="submit">Submit Assignment """ + ICON_ARROW + """</button>
    </form>
    <div class="hint">""" + ICON_LOCK + """ Your submission is saved securely</div>
    <a class="viewlink" href="/submissions">View all submissions</a>
  </section>
</div>
</body></html>
"""

LIST_PAGE = HEAD + """
<body class="list-page">
{% set palette = ['#6366f1','#06b6d4','#f59e0b','#ec4899','#10b981','#8b5cf6'] %}
<div class="top"><div class="wrap">
  <div class="nav">
    <div class="logo"><div class="mark">""" + ICON_CAP + """</div>
      <div><b>COMSATS University Islamabad</b><small>ATTOCK CAMPUS &middot; CSC418</small></div></div>
    <a class="navbtn" href="/">""" + ICON_PLUS + """ New submission</a>
  </div>
  <div class="stepper light">Step 2 of 2</div>
  <h1>{% if saved %}Submission complete{% else %}All submissions{% endif %}</h1>
  <p>Assignment Submission Portal &middot; DevOps for Cloud Computing</p>
</div></div>

<main>
  {% if saved and last %}
  <div class="success">
    <div class="tick"><svg viewBox="0 0 24 24"><path d="M5 13l4 4L19 7"/></svg></div>
    <div><h3>Submission saved successfully</h3>
      <p>Thank you, <b>{{ last.name }}</b> ({{ last.reg_no }}). Your assignment <b>{{ last.title }}</b> has been recorded.</p></div>
  </div>
  {% endif %}

  <div class="stats">
    <div class="stat"><div class="ic" style="background:linear-gradient(135deg,#6366f1,#8b5cf6)">""" + ICON_INBOX + """</div>
      <div><div class="num">{{ submissions|length }}</div><div class="lbl">Total submissions</div></div></div>
    <div class="stat"><div class="ic" style="background:linear-gradient(135deg,#06b6d4,#0ea5e9)">""" + ICON_USERS + """</div>
      <div><div class="num">{{ students }}</div><div class="lbl">Unique students</div></div></div>
    <div class="stat"><div class="ic" style="background:linear-gradient(135deg,#f59e0b,#f97316)">""" + ICON_CLOCK + """</div>
      <div><div class="num" style="font-size:1.1rem;padding-top:4px">{{ latest }}</div><div class="lbl">Latest submission</div></div></div>
  </div>

  <div class="card">
    <div class="toolbar">
      <h2>Saved submissions <span class="count">{{ submissions|length }}</span></h2>
      <div class="search">""" + ICON_SEARCH + """<input id="q" placeholder="Search by name, reg no or title"></div>
    </div>
    <div class="scroll">
    {% if submissions %}
    <table>
      <thead><tr><th>#</th><th>Student</th><th>Reg No</th><th>Assignment</th><th>Link</th><th>Submitted</th></tr></thead>
      <tbody>
      {% for s in submissions|reverse %}
        <tr>
          <td class="idx">{{ submissions|length - loop.index0 }}</td>
          <td><div class="who"><span class="av" style="background:{{ palette[loop.index0 % 6] }}">{{ s.name[:1]|upper }}</span>{{ s.name }}</div></td>
          <td><span class="reg">{{ s.reg_no }}</span></td>
          <td>{{ s.title }}</td>
          <td><a class="open" href="{{ s.url }}" target="_blank" rel="noopener">Open link """ + ICON_EXT + """</a></td>
          <td class="when">{{ s.get('submitted_at', '-') }}</td>
        </tr>
      {% endfor %}
      </tbody>
    </table>
    {% else %}
      <div class="empty"><div class="big">""" + ICON_INBOX + """</div><h3>No submissions yet</h3>
        <p>Submitted assignments will appear here.</p>
        <a class="navbtn" href="/">""" + ICON_PLUS + """ Make the first submission</a></div>
    {% endif %}
    </div>
  </div>
</main>
<footer>Assignment Submission Portal &copy; 2026 &middot; COMSATS University Islamabad, Attock Campus</footer>
<script>
var q=document.getElementById('q');
if(q){q.addEventListener('input',function(){
  var t=q.value.toLowerCase();
  document.querySelectorAll('tbody tr').forEach(function(r){
    r.style.display=r.textContent.toLowerCase().indexOf(t)>-1?'':'none';
  });
});}
</script>
</body></html>
"""

def is_valid_url(url):
    if " " in url:
        return False
    p = urlparse(url)
    return p.scheme in ("http", "https") and bool(p.netloc)

def validate(data):
    errors = []
    labels = {"name": "Name", "reg_no": "Registration number",
              "title": "Assignment title", "url": "Submission URL"}
    for key, label in labels.items():
        if not data.get(key, "").strip():
            errors.append(f"{label} is required")
    url = data.get("url", "").strip()
    if url and not is_valid_url(url):
        errors.append("Submission URL is invalid")
    return errors

def create_app(storage_file="submissions.json"):
    app = Flask(__name__)

    def load():
        if os.path.exists(storage_file):
            with open(storage_file) as f:
                return json.load(f)
        return []

    def save(items):
        with open(storage_file, "w") as f:
            json.dump(items, f, indent=2)

    @app.get("/")
    def index():
        empty = {"name": "", "reg_no": "", "title": "", "url": ""}
        return render_template_string(FORM_PAGE, errors=[], form=empty)

    @app.post("/submit")
    def submit():
        data = {k: request.form.get(k, "").strip()
                for k in ("name", "reg_no", "title", "url")}
        errors = validate(data)
        if errors:
            return render_template_string(FORM_PAGE, errors=errors, form=data), 400
        data["submitted_at"] = datetime.now().strftime("%d %b %Y, %H:%M")
        items = load()
        items.append(data)
        save(items)
        return redirect(url_for("submissions_page", saved=1))

    @app.get("/submissions")
    def submissions_page():
        items = load()
        students = len({s["reg_no"].lower() for s in items})
        last = items[-1] if items else None
        latest = last.get("submitted_at", "-") if last else "-"
        return render_template_string(LIST_PAGE, submissions=items, students=students,
                                      latest=latest, last=last,
                                      saved=request.args.get("saved") == "1")

    @app.get("/api/submissions")
    def api_submissions():
        return json.dumps(load()), 200, {"Content-Type": "application/json"}

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
