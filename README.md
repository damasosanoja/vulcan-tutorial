# Vulcan Supply Chain Tutorial

**Learn Vulcan's hybrid AI approach through hands-on supply chain risk automation**

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/damasosanoja/vulcan-tutorial)


Learn how to build reliable AI-enhanced automation systems using **Vulcan**, a forward-chaining inference engine that combines computational logic with AI intelligence. Through a realistic supply chain risk scenario, you'll learn why traditional LLM+RAG approaches fail in high-stakes automation and how Vulcan's hybrid architecture solves these problems.

## 🎯 What You'll Learn

- **Why LLM+RAG fails** for complex business automation
- **Hybrid architecture** that combines AI flexibility with computational reliability  
- **Microprompting techniques** that reduce AI hallucination risk
- **Forward-chaining rules** that create intelligent automation cascades
- **Production patterns** for AI-enhanced decision systems

## 🚀 Quick Start

**Option 1: GitHub Codespaces (Recommended)**
1. Click the "Open in GitHub Codespaces" badge above
2. Wait for the environment to load (2-3 minutes)
3. Run the mock AI tutorial: `python supply_chain.py --mock events/event-1.txt`

**Option 2: Local Development**
```bash
git clone your-repo-url
cd vulcan-supply-chain-tutorial
pip install -r requirements.txt
python supply_chain.py --mock events/event-1.txt
```

## 📚 Tutorial Progression

This tutorial follows a carefully designed 3-stage progression:

### Stage 1: Mock AI Simulation
```bash
python supply_chain.py --mock events/event-1.txt
```
- ✅ **No API key required** - perfect for learning concepts
- Demonstrates microprompting methodology with deterministic responses
- Shows console output that matches real AI implementation exactly

### Stage 2: Real AI Integration  
```bash
python supply_chain.py events/event-1.txt
```
- ⚙️ **Requires GEMINI_API_KEY** (enter as Codespace secret when prompted)
- Real Gemini LLM classification with production error handling
- Identical rule structure to mock - seamless transition

### Stage 3: Enhanced Safeguards
```bash
python supply_chain.py --enhanced events/event-4.txt  
```
- 🛡️ **Production-ready** with deterministic fallback guardrails
- Shows how to override AI decisions for critical business scenarios
- Demonstrates Vulcan's hybrid architecture advantages

## 🗂️ Project Structure

```
├── 📁 events/                  # Test scenarios
│   ├── event-1.txt            #   └─ Tariff announcement (HIGH risk)
│   ├── event-2.txt            #   └─ Normal operations (LOW risk)  
│   ├── event-3.txt            #   └─ Shipping delays (MEDIUM risk)
│   └── event-4.txt            #   └─ Enhanced rules demo
├── 📁 supply_chain/           # Core tutorial package
│   ├── schema.py              #   └─ Domain model (Facts)
│   ├── rules.py               #   └─ Stage 0: Pure deterministic rules
│   ├── rules_mock.py          #   └─ Stage 1: Mock AI simulation  
│   ├── rules_gemini.py        #   └─ Stage 2: Real AI integration
│   └── rules_gemini_enhanced.py  └─ Stage 3: Enhanced safeguards
├── 📁 prompts/                # AI prompt templates
├── main.py                    # Stage 0: Quick deterministic demo
├── main-01.py                 # Stage 1: Mock AI runner
├── main-02.py                 # Stage 2: Real AI runner  
└── supply_chain.py            # 🎯 Unified launcher (recommended)
```

## 🔧 API Key Configuration

### For Codespaces (Automatic)
When you first open this repository in Codespaces, you'll be prompted to enter your `GEMINI_API_KEY`. This is stored securely and persists across sessions.

### For Local Development  
Create a `.env` file:
```bash
GEMINI_API_KEY=your_actual_key_here
```

**💡 Pro Tip:** Start with `--mock` examples - they work immediately without any API keys!

## 🎮 Try Different Scenarios

```bash
# Tariff crisis triggers supplier switching
python supply_chain.py --mock events/event-1.txt

# Normal operations, no alerts  
python supply_chain.py --mock events/event-2.txt

# Shipping delays, monitoring alert only
python supply_chain.py --mock events/event-3.txt

# Enhanced rules override AI classification
python supply_chain.py --enhanced events/event-4.txt
```

## 🔍 What Makes This Different

**Traditional LLM+RAG Problems:**
- ❌ Unreliable decision making under pressure
- ❌ Poor audit trails for business decisions  
- ❌ Difficulty managing complex rule interdependencies
- ❌ High risk of hallucination in critical scenarios

**Vulcan's Hybrid Solution:**
- ✅ **AI for intelligent classification** - natural language understanding
- ✅ **Computational logic for business rules** - guaranteed reliability
- ✅ **Microprompting approach** - reduces hallucination risk
- ✅ **Forward-chaining automation** - complex cascades from simple rules
- ✅ **Complete audit trails** - explainable business decisions

## 📖 Learning Resources

- **Vulcan Documentation**: [Link to Vulcan docs]
- **Microprompting Guide**: See `prompts/ai-reasoning-prompt.txt`
- **Architecture Deep Dive**: Examine the progression from `rules.py` → `rules_mock.py` → `rules_gemini.py`

## 🤝 Contributing

This tutorial is designed to be self-contained and educational. If you find areas for improvement or have suggestions for additional scenarios, please open an issue or submit a pull request.

## 📄 License

MIT License

---

**Ready to learn hybrid AI automation?** Click the Codespaces badge above and start with `python supply_chain.py --mock events/event-1.txt` 🚀