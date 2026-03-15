#!/usr/bin/env python3
"""
Update tech words on markteasdale.com
Generates current AI/tech trending terms and updates index.html
Run every 6 months or whenever you want fresh terms.

Usage: python3 update-words.py
"""

import re
import subprocess
import json
from datetime import datetime

# Current tech words - edit this list or have AI generate it
TECH_WORDS = [
    # AI Models & Platforms
    "Claude", "OpenAI", "GPT-4", "GPT-5", "ChatGPT", "Anthropic",
    "Gemini", "Llama 3", "Mistral", "Ollama", "Copilot", "Perplexity",
    "Midjourney", "DALL-E", "Stable Diffusion", "Sora", "Whisper",
    # AI Concepts
    "LLM", "RAG", "Embeddings", "NLP", "Machine Learning",
    "Neural Networks", "Deep Learning", "Transformers", "BERT",
    "Fine-Tuning", "LoRA", "Inference", "Tokenizer", "Attention",
    "Prompt Engineering", "AI Agents", "Multi-Modal", "Diffusion",
    "Reinforcement Learning", "Computer Vision", "Semantic Search",
    "Vector DB", "Knowledge Graph", "Edge AI", "MLOps",
    "Generative AI", "Foundation Models", "Chain of Thought",
    # Frameworks & Tools
    "Langchain", "LlamaIndex", "Hugging Face", "TensorFlow",
    "PyTorch", "Keras", "scikit-learn", "Pandas", "NumPy",
    # Languages & Runtimes
    "Python", "JavaScript", "TypeScript", "Node.js", "VBA", "SQL",
    # Web & Cloud
    "Next.js", "React", "Supabase", "PostgreSQL", "Flask",
    "Vercel", "Tailwind", "WebGL", "GraphQL", "REST API",
    "WebSockets", "OAuth", "Redis", "MongoDB",
    "AWS", "Azure", "Docker", "Kubernetes", "CI/CD", "GitHub",
    # Mark's Stack
    "Twilio", "Graph API", "OCR", "Tesseract", "PaddleOCR",
    "SMTP", "Cron Jobs", "Data Pipeline", "API", "Automation",
    # Trending
    "MCP", "Tool Use", "Agentic AI", "Claude Code",
    "Cursor", "Windsurf", "v0", "Bolt", "Lovable",
    "OpenRouter", "Groq", "Cerebras", "Local LLM",
    "Context Window", "System Prompt", "Function Calling",
    "Structured Output", "Streaming", "Batch API",
    "AI Safety", "Alignment", "RLHF", "DPO",
    "Retrieval", "Chunking", "Reranking", "Hybrid Search",
]


def update_html(words):
    """Replace the techWords array in index.html."""
    with open("index.html", "r") as f:
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

    with open("index.html", "w") as f:
        f.write(html)

    print(f"Updated {len(words)} tech words in index.html")
    print(f"Last updated: {datetime.now().strftime('%Y-%m-%d')}")


if __name__ == "__main__":
    update_html(TECH_WORDS)
    print("\nTo deploy: git add index.html && git commit -m 'Update tech words' && git push origin main")
