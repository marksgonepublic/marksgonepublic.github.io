#!/usr/bin/env python3
"""
Auto-update tech words on markteasdale.com using Claude API.
Generates current AI/tech trending terms and updates index.html.

Usage: python3 update-words.py
Cron:  0 0 1 */3 * cd /mnt/c/OpenAI/Memory/projects/MarkTeasdale && python3 update-words.py --auto
"""

import re
import subprocess
import sys
import os

# Try to import anthropic, fall back to manual list
try:
    import anthropic
    HAS_API = True
except ImportError:
    HAS_API = False

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
HTML_PATH = os.path.join(SCRIPT_DIR, "index.html")

PROMPT = """Generate a list of exactly 120 current AI and tech terms/tools for a developer's personal landing page.
The developer works in property management and builds AI-powered software using Claude, Python, Supabase, and other modern tools.

Requirements:
- Focus heavily on the LATEST AI tools and concepts (2025-2026 era)
- Include Anthropic/Claude ecosystem prominently (Claude, Claude Code, MCP, Tool Use, etc.)
- Include current trending AI: latest model names, frameworks, concepts
- Include practical dev tools: languages, databases, cloud, DevOps
- Include the developer's actual stack: Python, VBA, Supabase, Next.js, React, PostgreSQL, Flask, Twilio, Ollama, OCR, Tesseract
- NO outdated terms - if something has been superseded, use the newer version
- Each term should be 1-3 words max
- Return ONLY a JSON array of strings, nothing else

Example format: ["Claude", "MCP", "Python", "Supabase", ...]"""


def get_words_from_claude():
    """Use Claude API to generate current tech terms."""
    import json
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[{"role": "user", "content": PROMPT}]
    )
    text = message.content[0].text.strip()
    # Extract JSON array
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        words = json.loads(match.group())
        return [w for w in words if isinstance(w, str) and len(w) < 30]
    raise ValueError("Could not parse word list from Claude response")


# Fallback manual list (update this if no API key available)
FALLBACK_WORDS = [
    "Claude", "Claude Code", "Claude Max", "MCP", "Tool Use", "Anthropic",
    "OpenAI", "GPT-4o", "ChatGPT", "Gemini", "Llama 3", "Mistral",
    "Copilot", "Perplexity", "Midjourney", "Sora", "Whisper",
    "LLM", "RAG", "Embeddings", "NLP", "Machine Learning",
    "Neural Networks", "Deep Learning", "Transformers",
    "Fine-Tuning", "LoRA", "Inference", "Attention",
    "Prompt Engineering", "AI Agents", "Multi-Modal", "Diffusion",
    "Computer Vision", "Semantic Search", "Vector DB",
    "Knowledge Graph", "Edge AI", "MLOps", "Generative AI",
    "Foundation Models", "Chain of Thought", "Agentic AI",
    "Langchain", "LlamaIndex", "Hugging Face", "TensorFlow",
    "PyTorch", "Keras", "scikit-learn", "Pandas", "NumPy",
    "Python", "JavaScript", "TypeScript", "Node.js", "VBA", "SQL",
    "Next.js", "React", "Supabase", "PostgreSQL", "Flask",
    "Vercel", "Tailwind", "WebGL", "GraphQL", "REST API",
    "WebSockets", "OAuth", "Redis", "MongoDB",
    "AWS", "Azure", "Docker", "Kubernetes", "CI/CD", "GitHub",
    "Twilio", "Graph API", "OCR", "Tesseract", "PaddleOCR",
    "SMTP", "Cron Jobs", "Data Pipeline", "API", "Automation",
    "Cursor", "Windsurf", "v0", "Bolt", "Lovable",
    "OpenRouter", "Groq", "Cerebras", "Ollama", "Local LLM",
    "Context Window", "System Prompt", "Function Calling",
    "Structured Output", "Streaming", "Batch API",
    "AI Safety", "Alignment", "RLHF", "DPO",
    "Retrieval", "Chunking", "Reranking", "Hybrid Search",
    "BERT", "Tokenizer", "Stable Diffusion",
    "TensorFlow", "MLOps", "Data Pipeline",
    "Kubernetes", "Docker", "GitHub", "CI/CD",
]


def update_html(words):
    """Replace the techWords array in index.html."""
    with open(HTML_PATH, "r") as f:
        html = f.read()

    # Build the new array string
    lines = ['            var techWords = [']
    for i in range(0, len(words), 6):
        batch = words[i:i+6]
        quoted = ', '.join(f'"{w}"' for w in batch)
        comma = ',' if i + 6 < len(words) else ''
        lines.append(f'                {quoted}{comma}')
    lines.append('            ];')
    new_array = '\n'.join(lines)

    # Replace the existing array
    pattern = r'            var techWords = \[.*?\];'
    html = re.sub(pattern, new_array, html, flags=re.DOTALL)

    with open(HTML_PATH, "w") as f:
        f.write(html)

    print(f"Updated {len(words)} tech words in index.html")


def git_push():
    """Commit and push changes."""
    os.chdir(SCRIPT_DIR)
    subprocess.run(["git", "add", "index.html"], check=True)
    subprocess.run(["git", "commit", "-m", "Auto-update tech words (quarterly)"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("Pushed to GitHub Pages")


if __name__ == "__main__":
    auto = "--auto" in sys.argv

    if HAS_API and os.environ.get("ANTHROPIC_API_KEY"):
        print("Generating fresh tech terms via Claude API...")
        try:
            words = get_words_from_claude()
            print(f"Got {len(words)} terms from Claude")
        except Exception as e:
            print(f"API failed ({e}), using fallback list")
            words = FALLBACK_WORDS
    else:
        print("No API key found, using fallback list")
        words = FALLBACK_WORDS

    update_html(words)

    if auto:
        git_push()
    else:
        print("\nTo deploy: git add index.html && git commit -m 'Update tech words' && git push origin main")
