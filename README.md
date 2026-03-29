# Colab Ollama Server Free

Run Ollama with GPU on Google Colab, exposed via Cloudflare tunnel.

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/YOUR_USERNAME/YOUR_REPO/blob/main/backend/src/modules/llm/colab/server.ipynb)

## Quick Start

1. Click badge above → opens Colab
2. Runtime → Change runtime type → **GPU**
3. Run cell → get tunnel URL
4. Use URL as Ollama endpoint

## Files

- `server.py` — Installs Ollama, starts GPU server, opens tunnel
- `test.py` — Simple hello test

## Config

Edit `MODEL` in the form sidebar (default: `qwen3.5:9b`)
