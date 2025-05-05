# MCP

# 🧠 AI Weather Agent using MCP, NOAA API, and GROQ LLM

A Python-based, context-aware AI system that fetches **real-time US weather alerts** using the **NOAA/NWS API**, shares information using a **Model Context Protocol (MCP)**, and generates **natural-language responses** using the **GROQ LLM** — all without classes!

---

## 🚀 Features

- ✅ Real-time weather alerts from [api.weather.gov](https://api.weather.gov)
- ✅ Model Context Protocol (MCP) for shared agent memory
- ✅ GROQ LLM integration for intelligent responses
- ✅ Pure Python (functional approach, no classes)

---

## 📌 How It Works

1. **Weather Agent** fetches alerts from NOAA/NWS API.
2. Data is stored in a **centralized context store** (a global dictionary).
3. The **LLM Agent (GROQ)** reads from context and generates user-facing messages.

```python
context = {
    "weather_alerts": {
        "TX": "Severe Thunderstorm Warning",
        "CA": "Heat Advisory"
    },
    "user_query": "What's happening in Texas?"
}
