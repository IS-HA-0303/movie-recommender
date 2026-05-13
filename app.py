import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests
import scipy.sparse

st.set_page_config(page_title="CineAI", page_icon="🎬", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,600&display=swap');
:root{--green:#1db954;--green2:#1ed760;--bg:#050810;--bg2:#0a0d14;--bg3:#0f1320;--card:#111827;--card2:#161d2e;--border:rgba(255,255,255,0.07);--text:#e4e4e4;--muted:#a3aab8;--white:#ffffff;}
*,*::before,*::after{box-sizing:border-box;}
html,body,.stApp{font-family:'Montserrat',sans-serif;background:var(--bg);color:var(--text);overflow-x:hidden;}
#MainMenu,footer,header{visibility:hidden;}
.block-container{padding:0 2rem 5rem 2rem !important;max-width:1440px !important;}
.stApp::before{content:'';position:fixed;inset:0;pointer-events:none;z-index:0;background:radial-gradient(ellipse 80% 50% at 20% 10%,rgba(29,185,84,0.05) 0%,transparent 60%),radial-gradient(ellipse 60% 40% at 80% 80%,rgba(29,185,84,0.03) 0%,transparent 55%);}
#trail{position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:9999;}
::-webkit-scrollbar{width:5px;}::-webkit-scrollbar-track{background:var(--bg2);}::-webkit-scrollbar-thumb{background:rgba(29,185,84,0.35);border-radius:3px;}
section[data-testid="stSidebar"]{background:var(--bg2) !important;border-right:1px solid var(--border) !important;}
section[data-testid="stSidebar"] .block-container{padding:1rem 1rem 2rem !important;}
.sb-logo{display:flex;align-items:center;gap:10px;padding:0.5rem 0 1.2rem;border-bottom:1px solid var(--border);margin-bottom:1rem;}
.sb-logo-icon{font-size:2rem;}
.sb-logo-name{font-family:'Playfair Display',serif;font-size:1.4rem;font-weight:700;background:linear-gradient(135deg,#fff 0%,#1db954 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.sb-logo-tag{font-size:9px;color:var(--green);letter-spacing:0.2em;text-transform:uppercase;font-weight:600;display:block;margin-top:2px;}
.sb-sec{font-size:9px;font-weight:700;letter-spacing:0.22em;text-transform:uppercase;color:var(--green);margin:1.2rem 0 0.5rem;display:block;}
.u-card{background:rgba(29,185,84,0.1);border:1px solid rgba(29,185,84,0.25);border-radius:10px;padding:11px 13px;margin-top:6px;}
.u-name{font-weight:700;font-size:13px;color:var(--green2);display:block;}
.u-meta{font-size:11.5px;color:var(--muted);margin-top:3px;line-height:1.7;display:block;}
.sb-row{display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:12px;}
.sb-k{color:var(--muted);}.sb-v{color:var(--white);font-weight:600;}
div[data-baseweb="select"]>div{background:var(--bg3) !important;border:1px solid rgba(29,185,84,0.25) !important;border-radius:8px !important;color:var(--white) !important;font-size:13px !important;}
div[data-baseweb="select"] span,div[data-baseweb="select"] div{color:var(--white) !important;}
.stToggle label p,label[data-testid="stWidgetLabel"] p{color:var(--text) !important;font-size:13px !important;font-weight:500 !important;}
.stSlider [role="slider"]{background:var(--green) !important;border-color:var(--green) !important;}
div[data-testid="stButton"]{display:flex !important;justify-content:center !important;}
.stButton>button{background:var(--green) !important;color:#000 !important;border:none !important;border-radius:999px !important;font-weight:700 !important;font-size:14px !important;letter-spacing:0.1em !important;text-transform:uppercase !important;padding:14px 52px !important;width:auto !important;min-width:260px !important;transition:all 0.2s !important;box-shadow:0 4px 24px rgba(29,185,84,0.35) !important;}
.stButton>button:hover{background:var(--green2) !important;transform:scale(1.04) !important;box-shadow:0 8px 36px rgba(29,185,84,0.55) !important;}
.hero{text-align:center;padding:3.5rem 0 2rem;}
.hero-pre{font-size:10px;letter-spacing:0.35em;text-transform:uppercase;color:var(--green);margin-bottom:18px;font-weight:600;}
.hero-title{font-family:'Playfair Display',serif;font-size:clamp(56px,9vw,108px);font-weight:700;line-height:0.9;color:var(--white);}
.hero-title span{font-style:italic;background:linear-gradient(135deg,#1db954 0%,#1ed760 50%,#4ade80 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.hero-sub{font-size:15px;color:var(--muted);margin-top:16px;letter-spacing:0.02em;}
.hero-dots{display:flex;justify-content:center;gap:6px;margin-top:20px;}
.dot{width:5px;height:5px;border-radius:50%;background:var(--green);opacity:0.4;animation:pdot 1.6s ease-in-out infinite;}
.dot:nth-child(2){animation-delay:0.2s;}.dot:nth-child(3){animation-delay:0.4s;}
@keyframes pdot{0%,100%{opacity:0.3;transform:scale(1);}50%{opacity:1;transform:scale(1.5);}}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:2rem;}
.sbox{background:var(--card);border:1px solid var(--border);border-radius:12px;padding:18px 10px;text-align:center;position:relative;overflow:hidden;transition:border-color 0.3s,transform 0.2s;}
.sbox::before{content:'';position:absolute;top:0;left:50%;transform:translateX(-50%);width:60%;height:1px;background:linear-gradient(90deg,transparent,var(--green),transparent);opacity:0.5;}
.sbox:hover{border-color:rgba(29,185,84,0.3);transform:translateY(-2px);}
.sn{font-family:'Playfair Display',serif;font-size:30px;font-weight:700;color:var(--green2);line-height:1;}
.sl{font-size:9.5px;color:var(--muted);letter-spacing:0.14em;text-transform:uppercase;margin-top:5px;font-weight:600;}
.sp{background:var(--card);border:1px solid var(--border);border-radius:16px;padding:24px 28px 20px;margin-bottom:1rem;}
.sp-lbl{font-size:9.5px;letter-spacing:0.22em;text-transform:uppercase;color:var(--green);margin-bottom:12px;display:block;font-weight:700;}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin-top:14px;align-items:center;}
.chip{display:inline-flex;align-items:center;gap:4px;padding:4px 12px;border-radius:999px;font-size:11px;font-weight:600;border:1px solid;letter-spacing:0.03em;}
.cg{background:rgba(29,185,84,0.12);color:#1ed760;border-color:rgba(29,185,84,0.3);}
.cw{background:rgba(255,255,255,0.05);color:#94a3b8;border-color:rgba(255,255,255,0.12);}
.cbl{background:rgba(56,189,248,0.08);color:#67e8f9;border-color:rgba(56,189,248,0.2);}
.co{background:rgba(251,146,60,0.08);color:#fdba74;border-color:rgba(251,146,60,0.2);}
.istrip{background:rgba(29,185,84,0.06);border:1px solid rgba(29,185,84,0.15);border-left:2px solid var(--green);border-radius:8px;padding:10px 15px;font-size:13px;color:rgba(29,185,84,0.9);margin:10px 0 14px;line-height:1.5;font-weight:500;}
.shdr{font-size:10px;letter-spacing:0.22em;text-transform:uppercase;color:var(--green);font-weight:700;display:flex;align-items:center;gap:12px;margin:6px 0 18px;}
.shdr::after{content:'';flex:1;height:1px;background:linear-gradient(90deg,rgba(29,185,84,0.3),transparent);}
.selbanner{background:var(--card2);border:1px solid rgba(29,185,84,0.15);border-radius:14px;padding:16px 20px;margin-bottom:22px;position:relative;overflow:hidden;}
.selbanner::before{content:'';position:absolute;top:0;left:0;bottom:0;width:3px;background:linear-gradient(180deg,var(--green),transparent);}
.sel-pre{font-size:9.5px;color:var(--muted);letter-spacing:0.15em;text-transform:uppercase;font-weight:600;}
.sel-name{font-family:'Playfair Display',serif;font-size:22px;color:var(--white);margin:4px 0 8px;}
.mc-wrap{border-radius:14px;overflow:hidden;border:1px solid var(--border);background:var(--card);transition:all 0.35s cubic-bezier(0.4,0,0.2,1);cursor:pointer;display:block;}
.mc-wrap:hover{transform:translateY(-8px) scale(1.02);border-color:rgba(29,185,84,0.55);box-shadow:0 24px 60px rgba(0,0,0,0.7),0 0 0 1px rgba(29,185,84,0.15),0 0 40px rgba(29,185,84,0.12);}
.mc-poster-box{position:relative;width:100%;padding-top:150%;overflow:hidden;background:#080c14;}
.mc-poster-box img{position:absolute;top:0;left:0;width:100%;height:100%;object-fit:cover;display:block;transition:transform 0.4s ease;}
.mc-wrap:hover .mc-poster-box img{transform:scale(1.07);}
.mc-poster-box::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(5,8,16,0.8) 100%);opacity:0;transition:opacity 0.35s ease;}
.mc-wrap:hover .mc-poster-box::after{opacity:1;}
.nop{position:absolute;top:0;left:0;width:100%;height:100%;display:flex;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(135deg,#0d1520,#111827);color:#374151;font-size:11px;font-weight:600;gap:6px;}
.nop-icon{font-size:26px;opacity:0.35;}
.mc-badges{display:flex;justify-content:space-between;padding:0 8px;margin-top:-28px;position:relative;z-index:5;pointer-events:none;}
.mc-rank-b{background:var(--green);color:#000;font-size:10px;font-weight:800;width:26px;height:26px;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 10px rgba(29,185,84,0.6);}
.mc-score-b{background:rgba(5,8,16,0.92);border:1px solid rgba(29,185,84,0.4);color:var(--green2);font-size:10px;font-weight:700;padding:3px 9px;border-radius:6px;}
.mc-info{padding:10px 13px 14px;background:var(--card);}
.mc-title{font-size:12.5px;font-weight:600;color:var(--white);line-height:1.3;margin:8px 0 6px;}
.mc-pills{display:flex;gap:4px;flex-wrap:wrap;margin-bottom:6px;}
.mp{font-size:8.5px;font-weight:700;padding:2px 6px;border-radius:4px;letter-spacing:0.06em;text-transform:uppercase;}
.mp-b{background:rgba(29,185,84,0.15);color:#1ed760;}
.mp-t{background:rgba(148,163,184,0.1);color:#94a3b8;}
.mp-c{background:rgba(56,189,248,0.1);color:#67e8f9;}
.mc-why{font-size:10.5px;color:var(--muted);font-style:italic;line-height:1.45;border-top:1px solid rgba(255,255,255,0.05);padding-top:7px;}
.stbl{width:100%;border-collapse:collapse;font-size:13px;}
.stbl thead th{padding:10px 16px;font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:var(--muted);font-weight:700;border-bottom:1px solid var(--border);text-align:center;}
.stbl thead th:first-child,.stbl thead th:nth-child(2){text-align:left;}
.stbl tbody td{padding:9px 16px;color:#9ca3af;border-bottom:1px solid rgba(255,255,255,0.03);text-align:center;}
.stbl tbody td:first-child{text-align:left;color:var(--muted);}
.stbl tbody td:nth-child(2){text-align:left;color:var(--white);}
.stbl tbody tr:hover td{background:rgba(29,185,84,0.025);}
.td-final{color:#1ed760 !important;font-weight:700;}
.foot{text-align:center;padding:28px 0 10px;border-top:1px solid var(--border);margin-top:24px;font-size:11.5px;color:#374151;line-height:2.2;}
.foot strong{color:var(--green);}
</style>

<canvas id="trail"></canvas>
<script>
(function(){
    const c=document.getElementById('trail'),x=c.getContext('2d');
    let W=window.innerWidth,H=window.innerHeight;
    c.width=W;c.height=H;
    window.addEventListener('resize',()=>{W=window.innerWidth;H=window.innerHeight;c.width=W;c.height=H;});
    const P=[];let mx=-999,my=-999;
    document.addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;});
    function spawn(){if(mx<0)return;const a=Math.random()*Math.PI*2,s=Math.random()*1.4+0.2;P.push({x:mx+(Math.random()-.5)*10,y:my+(Math.random()-.5)*10,vx:Math.cos(a)*s,vy:Math.sin(a)*s-.5,r:Math.random()*2.2+0.8,life:1,decay:Math.random()*.025+.012,hue:Math.random()>.7?'201,168,76':'29,185,84'});}
    function frame(){x.clearRect(0,0,W,H);for(let i=0;i<4;i++)spawn();for(let i=P.length-1;i>=0;i--){const p=P[i];p.x+=p.vx;p.y+=p.vy;p.vy+=.03;p.life-=p.decay;if(p.life<=0){P.splice(i,1);continue;}x.beginPath();x.arc(p.x,p.y,p.r,0,Math.PI*2);x.fillStyle=`rgba(${p.hue},${p.life*.5})`;x.fill();}requestAnimationFrame(frame);}
    frame();
})();
</script>
""", unsafe_allow_html=True)


# ── Load all data ──────────────────────────────────────────────
@st.cache_resource
def load_all():
    movies  = pd.DataFrame(pickle.load(open('movie_dict.pkl',        'rb')))
    tmdb_ml = pd.DataFrame(pickle.load(open('tmdb_ml_dict.pkl',      'rb')))
    csim    = pickle.load(open('content_similarity.pkl', 'rb'))
    bsim    = pickle.load(open('bert_similarity.pkl',    'rb'))
    mb      = pd.DataFrame(pickle.load(open('movies_bert_dict.pkl',  'rb')))
    als     = pickle.load(open('als_model.pkl',    'rb'))
    u2i     = pickle.load(open('user_to_idx.pkl',  'rb'))
    i2m     = pickle.load(open('idx_to_movie.pkl', 'rb'))
    sp      = scipy.sparse.load_npz('sparse_user_movie.npz')
    rat     = pd.read_csv('data/ratings_clean.csv')
    return movies, tmdb_ml, csim, bsim, mb, als, u2i, i2m, sp, rat

movies, tmdb_ml, csim, bsim, mb, als, u2i, i2m, sp, rat = load_all()


# ── Fetch poster — safe version with full error handling ───────
def fetch_poster(movie_id):
    """
    Safe poster fetch. Returns URL string or None.
    Never crashes the app.
    """
    if movie_id is None:
        return None
    try:
        api_key  = st.secrets["api_key"]
        url      = (f"https://api.themoviedb.org/3/movie/{int(movie_id)}"
                    f"?api_key={api_key}&language=en-US")
        response = requests.get(url, timeout=5)
        if response.status_code != 200:
            return None
        data   = response.json()
        poster = data.get('poster_path', '')
        if poster:
            return "https://image.tmdb.org/t/p/w500/" + poster
        return None
    except Exception:
        return None


def get_tmdb_id(title):
    r = movies[movies['title'] == title]
    if len(r) > 0:
        return int(r['movie_id'].values[0])
    return None


def show_poster(url, width=None):
    """Render poster or placeholder. Never crashes."""
    if url:
        if width:
            st.image(url, width=width)
        else:
            st.image(url, use_container_width=True)
    else:
        st.markdown(
            "<div class='no-poster'>🎬<br>No Poster</div>",
            unsafe_allow_html=True)


# ── Recommendation engine ──────────────────────────────────────
def norm(d):
    if not d: return {}
    v = list(d.values())
    mn, mx = min(v), max(v)
    rng = mx - mn if mx != mn else 1
    return {k: (val - mn) / rng for k, val in d.items()}

def c_scores(title):
    if title not in movies['title'].values: return {}
    idx = movies[movies['title'] == title].index[0]
    d   = csim[idx]
    return {movies.iloc[i]['title']: float(d[i]) for i in range(len(d))}

def b_scores(title):
    if title not in mb['title'].values: return {}
    idx = mb[mb['title'] == title].index[0]
    d   = bsim[idx]
    return {mb.iloc[i]['title']: float(d[i]) for i in range(len(d))}

def col_scores(uid, n=200):
    uid = int(uid)
    if uid not in u2i: return {}
    ux = u2i[uid]
    rids, sc = als.recommend(userid=ux, user_items=sp[ux],
                              N=n, filter_already_liked_items=True)
    out = {}
    for mi, s in zip(rids, sc):
        mi = int(mi)
        if mi not in i2m: continue
        row = tmdb_ml[tmdb_ml['movieId'] == i2m[mi]]
        if len(row): out[row['title'].values[0]] = float(s)
    return out

def why(b, t, c, mode):
    r = []
    if mode in ['hybrid','bert']:
        if b > 0.55:   r.append("very similar themes & tone")
        elif b > 0.30: r.append("similar story & mood")
    if mode in ['hybrid','content'] and t > 0.3:
        r.append("shared genre, cast & director")
    if mode == 'hybrid':
        if c > 0.5:    r.append("loved by similar users")
        elif c > 0.2:  r.append("popular with similar taste")
    if not r: r.append("matches your selection")
    return "— " + " · ".join(r)

def recommend(title, uid, mode, n, alpha, beta, gamma):
    cn  = norm(c_scores(title))
    bn  = norm(b_scores(title))
    col = norm(col_scores(uid)) if uid else {}
    rows = []
    for t in set(mb['title'].tolist()):
        if t == title: continue
        bv = bn.get(t, 0.0)
        tv = cn.get(t, 0.0)
        cv = col.get(t, 0.0)
        if mode == 'hybrid':
            s = (alpha*bv + beta*tv + gamma*cv) if uid \
                else (alpha/(alpha+beta))*bv + (beta/(alpha+beta))*tv
        elif mode == 'bert':    s = bv
        elif mode == 'content': s = tv
        else:                   s = cv
        rows.append({'title':t,'bert':round(bv,4),
                     'tfidf':round(tv,4),'collab':round(cv,4),'score':round(s,4)})
    return (pd.DataFrame(rows)
            .sort_values('score', ascending=False)
            .head(n).reset_index(drop=True))


# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">
        <span class="sb-logo-icon">🎬</span>
        <div>
            <span class="sb-logo-name">CineAI</span>
            <span class="sb-logo-tag">Smart Recommender</span>
        </div>
    </div>""", unsafe_allow_html=True)

    st.markdown('<span class="sb-sec">Mode</span>', unsafe_allow_html=True)
    mode = st.selectbox("mode", ['hybrid','bert','content','collab'],
        format_func=lambda x: {
            'hybrid':  '⚡  Hybrid — All Layers',
            'bert':    '🧠  BERT Semantic',
            'content': '📝  TF-IDF Content',
            'collab':  '👥  Collaborative'
        }[x], label_visibility='collapsed')

    st.markdown('<span class="sb-sec">Profile</span>', unsafe_allow_html=True)
    guest   = st.toggle("Guest mode (no login)", value=True)
    user_id = None
    if not guest:
        avail   = sorted(list(u2i.keys()))[:500]
        user_id = st.selectbox("uid", avail, label_visibility='collapsed')
        ur      = rat[rat['userId'] == user_id]
        st.markdown(f"""
        <div class="u-card">
            <span class="u-name">User {user_id}</span>
            <span class="u-meta">{len(ur):,} movies rated<br>
            Avg rating: {ur['rating'].mean():.1f} ⭐</span>
        </div>""", unsafe_allow_html=True)

    alpha, beta, gamma = 0.5, 0.3, 0.2
    if mode == 'hybrid':
        st.markdown('<span class="sb-sec">Layer Weights</span>',
                    unsafe_allow_html=True)
        alpha = st.slider("BERT",    0.0, 1.0, 0.5, 0.05)
        beta  = st.slider("TF-IDF", 0.0, 1.0, 0.3, 0.05)
        gamma = st.slider("Collab", 0.0, 1.0, 0.2, 0.05)

    st.markdown('<span class="sb-sec">Results</span>', unsafe_allow_html=True)
    n_recs = st.slider("n", 3, 10, 5, label_visibility='collapsed')

    st.markdown('<span class="sb-sec">Model Stats</span>',
                unsafe_allow_html=True)
    for k, v in [("Movies indexed", f"{len(mb):,}"),
                 ("Users trained",  f"{len(u2i):,}"),
                 ("Ratings used",   f"{len(rat):,}"),
                 ("BERT dims",      "384"),
                 ("Precision@10",   "71.2%")]:
        st.markdown(
            f'<div class="sb-row"><span class="sb-k">{k}</span>'
            f'<span class="sb-v">{v}</span></div>',
            unsafe_allow_html=True)


# ── Main page ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-pre">AI-Powered Cinema Intelligence</div>
    <div class="hero-title">Cine<span>AI</span></div>
    <div class="hero-sub">Discover films that truly resonate with you</div>
    <div class="hero-dots">
        <div class="dot"></div><div class="dot"></div><div class="dot"></div>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("""
<div class="stats">
    <div class="sbox"><div class="sn">4,806</div><div class="sl">Movies</div></div>
    <div class="sbox"><div class="sn">84K</div><div class="sl">Users Trained</div></div>
    <div class="sbox"><div class="sn">71.2%</div><div class="sl">Precision@10</div></div>
    <div class="sbox"><div class="sn">3</div><div class="sl">AI Layers</div></div>
</div>""", unsafe_allow_html=True)

st.markdown('<div class="sp"><span class="sp-lbl">Select a movie to begin</span>',
            unsafe_allow_html=True)
all_movies = sorted(mb['title'].tolist())
def_i      = all_movies.index('The Dark Knight') \
             if 'The Dark Knight' in all_movies else 0
selected   = st.selectbox("pick", all_movies, index=def_i,
                           label_visibility='collapsed')

_cmap = {'hybrid':('⚡','Hybrid','cg'), 'bert':('🧠','BERT','cbl'),
         'content':('📝','TF-IDF','cw'), 'collab':('👥','Collaborative','co')}
ico, lbl, cls = _cmap[mode]
chip_html  = f"<span class='chip {cls}'>{ico} {lbl}</span>"
chip_html += (f"<span class='chip cg'>👤 User {user_id}</span>"
              if user_id else "<span class='chip cw'>👤 Guest</span>")
st.markdown(f"<div class='chips'>{chip_html}</div>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

if user_id:
    st.markdown(
        f"<div class='istrip'>⚡ <strong>Personalised</strong> — "
        f"Recs for User {user_id} via BERT + TF-IDF + ALS "
        f"across {len(rat):,} real ratings.</div>",
        unsafe_allow_html=True)
else:
    st.markdown(
        "<div class='istrip'>👤 <strong>Guest mode</strong> — "
        "BERT + TF-IDF recommendations. Disable guest mode in "
        "the sidebar for personalised results.</div>",
        unsafe_allow_html=True)

_, col_c, _ = st.columns([2, 2, 2])
with col_c:
    go = st.button("▶  Find My Movies")


# ── Results ────────────────────────────────────────────────────
if go:
    with st.spinner("Curating your picks…"):
        recs = recommend(selected, user_id, mode, n_recs,
                         alpha, beta, gamma)

        # Fetch posters safely — never crashes
        posters = []
        for _, row in recs.iterrows():
            tid = get_tmdb_id(row['title'])
            posters.append(fetch_poster(tid))

        sel_poster = fetch_poster(get_tmdb_id(selected))

    # Selected banner
    c1, c2 = st.columns([1, 8])
    with c1:
        show_poster(sel_poster, width=72)
    with c2:
        st.markdown(f"""
        <div class="selbanner">
            <div class="sel-pre">Because you selected</div>
            <div class="sel-name">{selected}</div>
            <div class="chips">{chip_html}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(
        f'<div class="shdr">Top {n_recs} Recommendations</div>',
        unsafe_allow_html=True)

    cols = st.columns(n_recs, gap="small")
    for i in range(len(recs)):
        row   = recs.iloc[i]
        expl  = why(row['bert'], row['tfidf'], row['collab'], mode)
        pills = ""
        if mode in ['hybrid','bert']:
            pills += f"<span class='mp mp-b'>BERT {row['bert']:.2f}</span>"
        if mode in ['hybrid','content']:
            pills += f"<span class='mp mp-t'>TF {row['tfidf']:.2f}</span>"
        if mode in ['hybrid','collab'] and user_id:
            pills += f"<span class='mp mp-c'>ALS {row['collab']:.2f}</span>"

        with cols[i]:
            poster_html = (
                f"<img src='{posters[i]}' alt='{row['title']}'/>"
                if posters[i]
                else "<div class='nop'><div class='nop-icon'>🎬</div><div>No Poster</div></div>"
            )
            st.markdown(f"""
            <div class="mc-wrap">
                <div class="mc-poster-box">{poster_html}</div>
                <div class="mc-badges">
                    <div class="mc-rank-b">#{i+1}</div>
                    <div class="mc-score-b">{row['score']:.2f}</div>
                </div>
                <div class="mc-info">
                    <div class="mc-title">{row['title']}</div>
                    <div class="mc-pills">{pills}</div>
                    <div class="mc-why">{expl}</div>
                </div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.expander("📊  Score Breakdown"):
        # Use st.dataframe — always renders correctly, no HTML issues
        table_df = recs[['title','bert','tfidf','collab','score']].copy()
        table_df.index = table_df.index + 1   # start from 1
        table_df.columns = ['Title', 'BERT', 'TF-IDF', 'Collab', 'Final ↑']
        st.dataframe(
            table_df,
            use_container_width=True,
            column_config={
                "Title":   st.column_config.TextColumn("Title",   width="large"),
                "BERT":    st.column_config.NumberColumn("BERT",   format="%.4f", width="small"),
                "TF-IDF":  st.column_config.NumberColumn("TF-IDF", format="%.4f", width="small"),
                "Collab":  st.column_config.NumberColumn("Collab", format="%.4f", width="small"),
                "Final ↑": st.column_config.NumberColumn("Final ↑",format="%.4f", width="small"),
            }
        )

    with st.expander("🧠  How It Works"):
        st.markdown(f"""
**Mode: `{mode.upper()}`**

| Layer | Technology | Role |
|-------|-----------|------|
| 🧠 BERT | Sentence Transformers | Reads *meaning* — themes, tone, plot |
| 📝 TF-IDF | Count Vectorizer + Cosine | Genre, cast, director, keywords |
| 👥 ALS | Implicit Matrix Factorization | {len(rat):,} real user ratings |

Weights → BERT `{alpha}` · TF-IDF `{beta}` · Collab `{gamma}`
        """)

st.markdown("""
<div class="foot">
    <strong>CineAI</strong> — Production-grade Hybrid Movie Recommender<br>
    BERT · TF-IDF · ALS · MovieLens 25M · TMDB
</div>""", unsafe_allow_html=True)


