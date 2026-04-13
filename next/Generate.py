import re
import json
import base64
import os

# ─────────────────────────────────────────────
# 1. ARTICLE CONTENT
# ─────────────────────────────────────────────

article_title = "News Article with Interactive Elements"

article_paragraphs = [
    "রাজশাহীর ফরহান শপিং মেলার শপ চুয়েলার্স থেকে ৫০০ হার্টনেকার চুরির চাঞ্চল্যকর ঘটনার রহস্য উদঘাটন করেছে ঢাকা মহানগর গোয়েন্দা পুলিশ (ডিবি)। দুর্ধর্ষ এই চুরির ঘটনায় জড়িত সন্দেহে চার জনকে গ্রেফতার করা হয়েছে এবং তাদের কাছ থেকে বিপুল পরিমাণ চোরাই হার্টনেকার উদ্ধার করা হয়েছে বলে জানিয়েছে ডিবি।",
    "তদন্তে জানা গেছে, চোরাই চক্রের মূল পরিকল্পনাকারী দীর্ঘদিন ধরে এই এলাকায় সক্রিয় ছিল। পুলিশ জানায় যে তারা বিভিন্ন প্রমাণ সংগ্রহ করে অভিযান পরিচালনা করে। গ্রেফতারকৃতদের বিরুদ্ধে আইনগত ব্যবস্থা গ্রহণ করা হচ্ছে।",
    "ডিবির এক কর্মকর্তা জানান, উদ্ধার করা মালামালের মধ্যে রয়েছে বিভিন্ন ধরনের মূল্যবান গহনা এবং নগদ অর্থ। এই সংক্রান্ত তদন্ত অব্যাহত রয়েছে এবং আরও গ্রেফতার হতে পারে বলে জানানো হয়েছে।",
]

# ─────────────────────────────────────────────
# 2. TERMS
#
#  type must be exactly one of:
#    "text" | "image" | "audio" | "video" | "youtube"
#
#  YouTube: paste ANY YouTube URL — watch, share, or embed.
#           Python auto-converts it to the correct embed URL.
#
#  video / image / audio: use a URL or a local file path.
#           Local files are auto-embedded as base64 (works offline).
# ─────────────────────────────────────────────

terms = {
    "গোয়েন্দা পুলিশ": {
        "title": "গোয়েন্দা পুলিশ (ডিবি)",
        "color": "red",
        "type": "text",              # ← FIX: was missing "type" key
        "text": "ঢাকা মেট্রোপলিটন পুলিশের গোয়েন্দা বিভাগ (ডিবি) বাংলাদেশের প্রধান তদন্তকারী সংস্থাগুলোর একটি। গুরুত্বপূর্ণ অপরাধ মামলায় তারা তদন্ত পরিচালনা করে।",
        "image": "", "audio": "", "video": "", "youtube": "",
    },
    "সন্দেহে": {
        "title": "সন্দেহভাজন — কেন এমনটা বলা হল?",
        "color": "red",
        "type": "text",
        "text": '"সন্দেহে" শব্দটি ব্যবহার করা হয়েছে কারণ আইনি প্রক্রিয়ায় আদালতে দোষী প্রমাণিত না হওয়া পর্যন্ত কাউকে অপরাধী বলা যায় না।',
        "image": "", "audio": "", "video": "", "youtube": "",
    },
    "পরিকল্পনাকারী": {
        "title": "পরিকল্পনাকারী",
        "color": "blue",
        "type": "text",
        "text": "পরিকল্পনাকারী বলতে সেই ব্যক্তিকে বোঝায় যে অপরাধমূলক কার্যক্রমের মূল পরিকল্পনা প্রণয়ন করে এবং দলকে নির্দেশনা দেয়।",
        "image": "", "audio": "", "video": "", "youtube": "",
    },
    "প্রমাণ": {
        "title": "প্রমাণ সংগ্রহ প্রক্রিয়া",
        "color": "green",
        "type": "image",
        "text": "পুলিশ সাধারণত ফিজিক্যাল এভিডেন্স, সিসিটিভি ফুটেজ এবং ডিজিটাল তথ্য সংগ্রহ করে তদন্ত পরিচালনা করে।",
        "image": "photo.jpg",        # ← local file OR "https://..." URL
        "audio": "", "video": "", "youtube": "",
    },
    "আইনগত ব্যবস্থা": {
        "title": "আইনগত ব্যবস্থা — ভিডিও",
        "color": "red",
        "type": "video",             # ← FIX: was "videoClip", must be "video"
        "text": "গ্রেফতারকৃতদের বিরুদ্ধে চুরি ও সংগঠিত অপরাধ সংক্রান্ত ধারায় মামলা দায়ের করা হয়।",
        "image": "",
        "audio": "",
        "video": "clip.mp4",         # ← local file OR "https://..." URL
        "youtube": "",
    },
    "গহনা": {
        "title": "উদ্ধারকৃত গহনা — ভিডিও রিপোর্ট",
        "color": "blue",
        "type": "youtube",
        "text": "উদ্ধারকৃত মালামালে স্বর্ণালংকার, হীরার গহনা ও নগদ অর্থ ছিল।",
        "image": "", "audio": "", "video": "",
        # ← FIX: paste ANY YouTube URL — watch link, share link, or embed link.
        #         Python will auto-extract the video ID and build the correct embed URL.
        "youtube": "https://www.youtube.com/watch?v=7N74i_rAfFE",
    },
}


# ─────────────────────────────────────────────
# 4. HELPERS
# ─────────────────────────────────────────────

MIME_MAP = {
    ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
    ".gif": "image/gif",  ".webp": "image/webp", ".svg": "image/svg+xml",
    ".mp4": "video/mp4",  ".webm": "video/webm", ".ogv": "video/ogg",
    ".mp3": "audio/mpeg", ".wav":  "audio/wav",  ".oga": "audio/ogg",
}

def embed_local(path):
    """Embed a local file as a base64 data-URI, or return the URL unchanged."""
    if not path:
        return path
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if not os.path.isfile(path):
        print(f"  ⚠️  File not found: {path!r} — skipping embed")
        return ""          # return empty so the media block is hidden
    ext = os.path.splitext(path)[1].lower()
    mime = MIME_MAP.get(ext, "application/octet-stream")
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    size_kb = os.path.getsize(path) // 1024
    print(f"  📎 Embedded: {path!r}  ({mime}, {size_kb} KB)")
    return f"data:{mime};base64,{b64}"

def to_youtube_embed(url):
    """
    Convert any YouTube URL format to a clean embed URL.
      https://www.youtube.com/watch?v=ABC123          → https://www.youtube.com/embed/ABC123
      https://youtu.be/ABC123                          → https://www.youtube.com/embed/ABC123
      https://www.youtube.com/embed/ABC123             → unchanged
      https://www.youtube.com/watch?v=ABC&list=XYZ     → https://www.youtube.com/embed/ABC123
    """
    if not url:
        return url
    if "/embed/" in url:
        # Already an embed URL — strip extra query params after the ID if any
        return url.split("?")[0]
    # youtu.be short link
    if "youtu.be/" in url:
        video_id = url.split("youtu.be/")[1].split("?")[0].split("&")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    # Standard watch link
    if "v=" in url:
        video_id = url.split("v=")[1].split("&")[0].split("?")[0]
        return f"https://www.youtube.com/embed/{video_id}"
    print(f"  ⚠️  Could not parse YouTube URL: {url!r}")
    return url

# ─────────────────────────────────────────────
# 5. RESOLVE ALL MEDIA PATHS
# ─────────────────────────────────────────────

for word, data in terms.items():
    for field in ("image", "audio", "video"):
        data[field] = embed_local(data[field])
    data["youtube"] = to_youtube_embed(data.get("youtube", ""))

# ─────────────────────────────────────────────
# 6. INJECT HIGHLIGHTS
# ─────────────────────────────────────────────

COLOR_CLASS = {
    "red":   "text-red-600 border-red-500",
    "blue":  "text-blue-700 border-blue-500",
    "green": "text-green-700 border-green-600",
}

def inject_highlights(text, terms):
    for word in sorted(terms.keys(), key=len, reverse=True):
        color  = terms[word].get("color", "red")
        cls    = COLOR_CLASS.get(color, COLOR_CLASS["red"])
        safe   = word.replace("'", "\\'")
        span   = (
            f'<span class="hl {cls}" onclick="showPopup(\'{safe}\')">'
            f'{word}'
            f'<span class="zoom-icon">🔍</span>'
            f'</span>'
        )
        text = re.sub(re.escape(word), span, text, count=1)
    return text

processed_paragraphs = [inject_highlights(p, terms) for p in article_paragraphs]
paras_html = "\n".join(f'<p class="mb-4 leading-8">{p}</p>' for p in processed_paragraphs)



# ─────────────────────────────────────────────
# 8. BADGE MAP  (sent to JS)
# ─────────────────────────────────────────────

BADGE = {
    "text":    ["Text",    "bg-blue-100 text-blue-700"],
    "image":   ["Image",   "bg-green-100 text-green-700"],
    "audio":   ["Audio",   "bg-purple-100 text-purple-700"],
    "video":   ["Video",   "bg-amber-100 text-amber-700"],
    "youtube": ["YouTube", "bg-red-100 text-red-700"],
}
badge_json = json.dumps(BADGE, ensure_ascii=False)
terms_json = json.dumps(terms, ensure_ascii=False)

# ─────────────────────────────────────────────
# 9. FULL HTML
# ─────────────────────────────────────────────

html = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Interactive Teaching Platform</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  .hl {{
    cursor: pointer;
    font-weight: 600;
    border-bottom: 2px dotted;
    transition: opacity 0.15s;
  }}
  .hl:hover {{ opacity: 0.65; }}
  .zoom-icon {{
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 15px; height: 15px;
    background: #ede9fe;
    border: 1px solid #c4b5fd;
    border-radius: 50%;
    font-size: 7px;
    vertical-align: middle;
    margin-left: 2px;
    color: #5b21b6;
  }}
  @keyframes modalUp {{
    from {{ opacity: 0; transform: translateY(14px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
  }}
  .modal-animate {{ animation: modalUp 0.2s ease forwards; }}
</style>
</head>
<body class="bg-indigo-50 text-gray-800 font-sans">

<!-- HEADER -->
<header class="bg-gradient-to-r from-indigo-800 to-indigo-500 text-white text-center py-10 px-4">
  <h1 class="text-3xl font-semibold tracking-tight mb-1">Interactive Teaching Platform</h1>
  <p class="text-indigo-200 text-sm">Click on highlighted terms to explore multimedia content</p>
</header>

<!-- LAYOUT -->
<main class="max-w-5xl mx-auto px-5 py-8 grid grid-cols-1 lg:grid-cols-[1fr_260px] gap-6">

  <div>
    <!-- Article card -->
    <div class="bg-white rounded-2xl border border-indigo-100 shadow-sm p-6">
      <h2 class="text-indigo-700 font-semibold text-base border-b-2 border-indigo-200 pb-2 mb-4">
        {article_title}
      </h2>
      <div class="text-gray-700 leading-8 text-[15px]">
        {paras_html}
      </div>
    </div>

  
  </div>

  
</main>

<!-- MODAL -->
<div id="overlay"
     class="hidden fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
     onclick="overlayClick(event)">
  <div id="modal"
       class="modal-animate bg-white rounded-2xl shadow-2xl w-full max-w-md relative p-6 border border-gray-100">

    <button onclick="closePopup()"
            class="absolute top-3 right-4 text-gray-400 hover:text-gray-700 text-2xl leading-none font-light">
      &times;
    </button>

    <h3 id="modal-title"  class="text-gray-900 font-semibold text-lg mb-1 pr-6"></h3>
    <span id="modal-badge" class="inline-block text-xs font-semibold px-3 py-0.5 rounded-full mb-3"></span>
    <div  id="modal-media" class="mb-3"></div>
    <p    id="modal-body"  class="text-gray-600 text-sm leading-7"></p>
  </div>
</div>

<script>
const TERMS  = {terms_json};
const BADGES = {badge_json};

function showPopup(word) {{
  const t = TERMS[word];
  if (!t) return;

  document.getElementById('modal-title').textContent = t.title || word;

  const [label, cls] = BADGES[t.type] || ['Info', 'bg-gray-100 text-gray-600'];
  const badge = document.getElementById('modal-badge');
  badge.textContent = label;
  badge.className = 'inline-block text-xs font-semibold px-3 py-0.5 rounded-full mb-3 ' + cls;

  const media = document.getElementById('modal-media');
  media.innerHTML = '';

  if (t.type === 'image' && t.image) {{
    media.innerHTML = `<img src="${{t.image}}" alt="${{t.title}}"
      class="w-full rounded-xl border border-gray-100 object-cover max-h-56">`;

  }} else if (t.type === 'audio' && t.audio) {{
    media.innerHTML = `<audio controls src="${{t.audio}}" class="w-full mt-1"></audio>`;

  }} else if (t.type === 'video' && t.video) {{
    media.innerHTML = `
      <video controls src="${{t.video}}"
        class="w-full rounded-xl border border-gray-100 max-h-52"
        preload="metadata">
        Your browser does not support the video tag.
      </video>`;

  }} else if (t.type === 'youtube' && t.youtube) {{
    media.innerHTML = `
      <div class="relative w-full" style="padding-top:56.25%">
        <iframe src="${{t.youtube}}"
          class="absolute inset-0 w-full h-full rounded-xl"
          frameborder="0"
          allowfullscreen
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
        </iframe>
      </div>`;
  }}

  document.getElementById('modal-body').textContent = t.text || '';

  // show + re-trigger animation
  const overlay = document.getElementById('overlay');
  const modal   = document.getElementById('modal');
  overlay.classList.remove('hidden');
  modal.classList.remove('modal-animate');
  void modal.offsetWidth;          // force reflow
  modal.classList.add('modal-animate');
  document.body.style.overflow = 'hidden';
}}

function closePopup() {{
  document.getElementById('overlay').classList.add('hidden');
  document.getElementById('modal-media').innerHTML = ''; // stop media playback
  document.body.style.overflow = '';
}}

function overlayClick(e) {{
  if (e.target.id === 'overlay') closePopup();
}}

document.addEventListener('keydown', e => {{ if (e.key === 'Escape') closePopup(); }});

function toggleAcc(btn) {{
  const body    = btn.nextElementSibling;
  const isOpen  = body.classList.toggle('hidden');   // isOpen = now hidden
  btn.querySelector('.chev').textContent = isOpen ? '▼' : '▲';
  btn.classList.toggle('bg-indigo-700', !isOpen);
  btn.classList.toggle('bg-indigo-600',  isOpen);
}}
</script>
</body>
</html>
"""

# ─────────────────────────────────────────────
# 10. WRITE FILE
# ─────────────────────────────────────────────

output_path = "article.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅  Done!  Open '{output_path}' in your browser.")
print("   No server needed — just double-click the file.\n")