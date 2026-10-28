
import os
import requests
import uvicorn
from dotenv import load_dotenv
from openai import OpenAI
from fastapi import FastAPI, Request, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

load_dotenv()
GIT_TOKEN = os.getenv("GITHUB_TOKEN")
GROQ_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="ReviewPulse AI")

PAGE = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ReviewPulse AI</title>
<style>
*{box-sizing:border-box}
:root{color-scheme:dark}
body{margin:0;background:#090d18;color:#e8edf8;font-family:Inter,Segoe UI,Arial,sans-serif}
header{height:72px;padding:0 5%;display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #20283b;background:#0d1220}
.brand{display:flex;align-items:center;gap:12px;font-size:20px;font-weight:750}
.logo{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,#8b5cf6,#3b82f6);display:grid;place-items:center;font-size:21px}
.muted{color:#8c98b2;font-size:13px}
.status{color:#6ee7b7;font-size:12px;border:1px solid #205a4a;background:#10291f;border-radius:20px;padding:8px 12px}
main{max-width:1450px;margin:auto;padding:35px 5%}
.hero{display:flex;justify-content:space-between;align-items:center;gap:20px;margin-bottom:30px}
h1{font-size:clamp(27px,4vw,38px);margin:0 0 10px;letter-spacing:-1px}
h1 span{color:#a78bfa}
p{color:#96a2ba;line-height:1.6}
.hero p{margin:0}
.grid{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(300px,1fr);gap:22px}
.card{background:#101727;border:1px solid #252e43;border-radius:17px;overflow:hidden;min-width:0}
.cardhead{padding:19px 21px;border-bottom:1px solid #252e43;display:flex;justify-content:space-between;align-items:center;gap:10px}
.cardhead h2{font-size:15px;margin:0}
.tag{font-size:11px;color:#b7a4ff;background:#292047;border-radius:6px;padding:6px 9px}
.controls{display:flex;gap:10px;align-items:center;flex-wrap:wrap}
select{background:#171f32;color:#dbe3f5;border:1px solid #303b52;padding:9px;border-radius:8px}
textarea{display:block;width:100%;height:350px;resize:vertical;border:0;outline:none;background:#0c1220;color:#d9e4ff;padding:22px;font:13px/1.8 Consolas,monospace}
.editorfoot{padding:13px 18px;display:flex;justify-content:space-between;gap:12px;align-items:center;border-top:1px solid #252e43}
button{cursor:pointer;border:0;border-radius:9px;padding:12px 18px;font-weight:700}
.primary{background:linear-gradient(110deg,#8b5cf6,#4f72f5);color:white}
.primary:hover{filter:brightness(1.12)}
.secondary{background:#202a3e;color:#dbe4f8}
button:disabled{opacity:.55;cursor:wait}
.result{padding:22px;min-height:350px;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.8 Consolas,monospace;color:#d1d9e9}
.empty{text-align:center;padding:75px 15px;color:#8290aa;font-family:Inter,Arial,sans-serif}
.empty .symbol{font-size:35px;margin-bottom:12px}
.empty strong{display:block;color:#dce4f4;margin-bottom:7px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:22px}
.stat{padding:17px;background:#101727;border:1px solid #252e43;border-radius:13px}
.stat strong{display:block;font-size:20px;margin-bottom:7px}
.stat span{font-size:12px;color:#91a0ba}
.bottom{margin-top:22px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:12px;color:#8290aa}
#error{color:#fca5a5;font-size:13px;padding:0 20px 15px;display:none}
@media(max-width:800px){.grid{grid-template-columns:1fr}.hero{align-items:flex-start;flex-direction:column}textarea{height:280px}main{padding:25px 4%}}
</style>
</head>
<body>
<header>
  <div class="brand"><div class="logo">⌘</div>ReviewPulse <span style="color:#a78bfa">AI</span></div>
  <div class="status">● API Connected</div>
</header>
<main>
  <section class="hero">
    <div>
      <h1>Ship better code with <span>AI reviews.</span></h1>
      <p>Find bugs, spot security risks, and improve your code before it ships.</p>
    </div>
    <div class="muted">POWERED BY GROQ AI</div>
  </section>
  <section class="grid">
    <div class="card">
      <div class="cardhead">
        <h2>Code Workspace</h2>
        <div class="controls">
          <select id="language">
            <option>Python</option><option>JavaScript</option>
            <option>Java</option><option>C</option><option>C++</option>
          </select>
          <button class="secondary" id="sample">Load sample</button>
        </div>
      </div>
      <textarea id="code" spellcheck="false" placeholder="// Paste your code here..."></textarea>
      <div id="error"></div>
      <div class="editorfoot">
        <span class="muted" id="count">0 lines</span>
        <button class="primary" id="review">✦ Review Code →</button>
      </div>
    </div>
    <div class="card">
      <div class="cardhead">
        <h2>Review Results</h2>
        <span class="tag">AI ANALYSIS</span>
      </div>
      <div class="result" id="result"><div class="empty"><div class="symbol">⌘</div><strong>Ready to review</strong>Paste your code and click Review Code to get your AI-powered analysis.</div></div>
    </div>
  </section>
  <section class="stats">
    <div class="stat"><strong id="health">—</strong><span>Code health score</span></div>
    <div class="stat"><strong id="issues">—</strong><span>Review completed</span></div>
    <div class="stat"><strong id="languageStat">—</strong><span>Selected language</span></div>
  </section>
  <div class="bottom"><span>ReviewPulse AI · Intelligent code review</span><span>GitHub webhook integration enabled when configured</span></div>
</main>
<script>
const code=document.getElementById('code');
const result=document.getElementById('result');
const btn=document.getElementById('review');
const err=document.getElementById('error');
const lang=document.getElementById('language');
function countLines(){document.getElementById('count').textContent=code.value.split('\n').length+' lines'}
code.addEventListener('input',countLines);
lang.addEventListener('change',()=>document.getElementById('languageStat').textContent=lang.value);
document.getElementById('sample').onclick=()=>{
 const samples={
 Python:'def divide(a, b):\n    return a / b\n\npassword = "admin123"\nprint(divide(10, 0))',
 JavaScript:'function getUser(userId) {\n  const query = "SELECT * FROM users WHERE id = " + userId;\n  return database.execute(query);\n}',
 Java:'public int divide(int a, int b) {\n    return a / b;\n}',
 C:'#include <stdio.h>\nint main() {\n    int a = 10, b = 0;\n    printf("%d", a / b);\n    return 0;\n}',
 'C++':'#include <iostream>\nusing namespace std;\nint main() {\n    int a = 10, b = 0;\n    cout << a / b;\n}'
 };
 code.value=samples[lang.value];countLines();
};
btn.onclick=async()=>{
 if(!code.value.trim()){err.style.display='block';err.textContent='Please paste some code first.';return}
 err.style.display='none';btn.disabled=true;btn.textContent='Analyzing code...';
 result.textContent='Analyzing your code with ReviewPulse AI. Please wait...';
 document.getElementById('health').textContent='...';
 document.getElementById('issues').textContent='...';
 try{
  const response=await fetch('/review',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code:code.value,language:lang.value})});
  const data=await response.json();
  if(!response.ok)throw new Error(data.detail||'Review failed');
  result.textContent=data.review;
  const match=data.review.match(/(?:health score|score)[:\s*]+(\d{1,2})\s*\/\s*10/i);
  document.getElementById('health').textContent=match?match[1]+'/10':'Done';
  document.getElementById('issues').textContent='Complete';
  document.getElementById('languageStat').textContent=lang.value;
 }catch(e){
  result.textContent='Could not complete the review.';
  err.style.display='block';err.textContent=e.message;
  document.getElementById('health').textContent='—';
  document.getElementById('issues').textContent='—';
 }finally{btn.disabled=false;btn.textContent='✦ Review Code →'}
};
</script>
</body>
</html>
"""


def get_ai_review(code, language="code changes"):
    if not GROQ_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing from your .env file.")

    client = OpenAI(
        api_key=GROQ_KEY,
        base_url="https://api.groq.com/openai/v1"
    )

    prompt = f"""
You are a senior software engineer performing a careful code review.
Review the following {language} code.

Check for:
- Bugs and incorrect logic
- Security vulnerabilities
- Performance problems
- Readability and maintainability
- Concrete improvements

Start your response with:
AI CODE REVIEW SUMMARY
Overall Health Score: X/10

Then include Critical Issues, Other Issues, and Suggestions.
Explain issues clearly and give corrected code snippets where useful.
Do not claim an issue exists unless the code supports that conclusion.

CODE:
{code[:20000]}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content


@app.get("/", response_class=HTMLResponse)
async def home():
    return HTMLResponse(PAGE)


class ReviewRequest(BaseModel):
    code: str
    language: str = "Python"


@app.post("/review")
async def review_code(data: ReviewRequest):
    if not data.code.strip():
        raise HTTPException(status_code=400, detail="Please provide code to review.")
    try:
        review = get_ai_review(data.code, data.language)
        return {"review": review}
    except Exception as e:
        print(f"Review error: {e}")
        raise HTTPException(
            status_code=500,
            detail="AI review failed. Check your Groq API key, quota, and server terminal."
        )


def get_diff(repo, pr_no):
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_no}"
    headers = {
        "Authorization": f"Bearer {GIT_TOKEN}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()
    return response.text


def post_comment(repo, pr_no, text):
    url = f"https://api.github.com/repos/{repo}/issues/{pr_no}/comments"
    headers = {"Authorization": f"Bearer {GIT_TOKEN}"}
    response = requests.post(
        url, json={"body": text}, headers=headers, timeout=30
    )
    response.raise_for_status()


@app.post("/webhook")
async def webhook(request: Request, bg: BackgroundTasks):
    data = await request.json()

    if "pull_request" in data and data.get("action") in ["opened", "synchronize"]:
        repo = data["repository"]["full_name"]
        pr_no = data["number"]
        print(f"Detected PR #{pr_no}. Starting AI review...")
        bg.add_task(process_review, repo, pr_no)

    return {"ok": True}


def process_review(repo, pr_no):
    try:
        if not GIT_TOKEN:
            raise RuntimeError("GITHUB_TOKEN is missing from .env")

        print(f"Fetching code for {repo} PR #{pr_no}...")
        diff = get_diff(repo, pr_no)

        print("AI is analyzing...")
        review = get_ai_review(diff, "GitHub pull request diff")

        print("Posting review to GitHub...")
        post_comment(repo, pr_no, review)
        print("Review posted successfully.")
    except Exception as e:
        print(f"GitHub review failed: {e}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
