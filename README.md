# Test_AI_Chat
Privacy-first local AI assistant running on custom hardware. Built to automate personal finances and etc.

🧠 Local AI Assistant (Proof of Concept)
A privacy-first, locally hosted AI assistant designed to serve as the intelligent core of my personal productivity ecosystem (HubSystem).

🎯 Vision & Purpose
The primary goal of this project is to create a fully autonomous AI agent that processes sensitive personal data (finances, schedules, daily workflows) entirely on local hardware, ensuring zero data leakage to cloud APIs (like OpenAI or Anthropic).

Eventually, this AI will act as a personal orchestrator: categorizing expenses, planning shifts, and automating routine tasks via API integrations with my existing services.

🚀 Current State (PoC)
Currently, the project is in the Proof of Concept phase.
Implemented a lightweight, responsive chat interface.

Established API communication with a locally running Large Language Model (LLM).

Basic context management and prompt handling.

🛠️ Tech Stack
Frontend: Vanilla JavaScript, HTML5, CSS3 (Tailwind)
Backend: Python / FastAPI (acting as middleware/router)
LLM Engine: Ollama / LM Studio

Target Models: Llama-3-8B-Instruct

💻 Hardware Infrastructure

Understanding the VRAM and compute requirements for LLM inference, this project is deployed on a custom-built home server/PC:
CPU: [Intel© Xeon© CPU E5-2650 v4 @ 2.20GHz × 12]

RAM: [20GB DDR4]

🗺️ Roadmap
This project is part of a larger ecosystem. The development plan:
[x] Phase 1: Setup local LLM infrastructure and hardware.
[x] Phase 2: Build a basic web-based chat interface (Current PoC).
[ ] Phase 3: Integrate with FinLit (Personal Finance Tracker) for automated receipt parsing and smart categorization.
[ ] Phase 4: Integrate with Smart Schedule to manage work shifts, vacations, and calculate salary impacts.
[ ] Phase 5: Implement Tool Calling / Function Calling to allow the AI to execute database operations autonomously.


Navigate to http://localhost:3000 to start chatting with your local AI.
