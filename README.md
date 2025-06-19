# Vulcan Supply Chain Tutorial

This repository contains the complete hands-on tutorial files for learning Vulcan's hybrid AI approach through supply chain risk automation. **[Read the full tutorial here](#)** to understand the concepts and architectural decisions behind this implementation.

## 🚀 Quick Start

**Option 1: GitHub Codespaces (Recommended)**

[![Use this template](https://img.shields.io/badge/Use%20this%20template-2ea44f?style=for-the-badge)](https://github.com/damasosanoja/vulcan-tutorial/generate)

1. Click the **"USE THIS TEMPLATE"** button above to create your own copy
2. Open **your new repository** in Codespaces
3. Enter your OpenAI or Gemini API keys (optional but recommended for the full Vulcan experience)
4. Run: `./demo 1` (works immediately, no API keys required!)

**Option 2: Local Development**

Clone this repository to the desired location and run:

```
cd vulcan-tutorial
pip install -r requirements.txt
chmod +x demo
./demo 1  # Mock simulation (no API key required)
```

## 🎯 What You'll Learn

- **Why LLM+RAG fails** for complex business automation
- **Hybrid architecture** that combines AI flexibility with computational reliability  
- **Microprompting techniques** that reduce AI hallucination risk
- **Forward-chaining rules** that create intelligent automation cascades
- **Advanced patterns** for AI-enhanced decision systems

## 📚 Tutorial Progression

This tutorial follows a carefully designed 2-stage progression:

### Stage 1: Mock AI Simulation

```
./demo 1  # Default - works immediately, no API key required
```

- ✅ **Perfect for learning** - demonstrates concepts without API complexity
- Shows microprompting methodology with deterministic responses
- Identical output format to real AI for easy comparison

### Stage 2: Real AI Integration 

```
./demo 1 --gemini     # Requires GEMINI_API_KEY
./demo 1 --openai     # Requires OPENAI_API_KEY  
```

- ⚙️ **Real LLM integration** - experience authentic AI behavior with error handling
- Supports both OpenAI and Gemini providers
- Identical rule structure to mock - seamless transition

### Stage 3: Enhanced Safeguards

```
./demo 1 --gemini --enhanced   # Advanced patterns with fallbacks
./demo 4 --openai --enhanced   # Critical keyword override demo
```

- 🛡️ **Advanced safeguards** - deterministic fallback guardrails
- Shows how to override AI decisions for critical business scenarios

## 🎮 Try Different Scenarios

```
./demo 1      # Tariff crisis triggers supplier switching
./demo 2      # Normal operations, no alerts  
./demo 3      # Shipping delays, monitoring alert only
./demo 4      # Enhanced rules override demonstration

./demo --help # Complete command reference
```

## 🔧 API Key Configuration

### For Codespaces (Automatic)
When you create a Codespace, you'll be prompted to enter your API keys. These are stored securely and persist across sessions.

### For Local Development  

Create a `.env` file in the `root` folder and paste your API key:

```
OPENAI_API_KEY=your_openai_key_here    # Preferred provider
GEMINI_API_KEY=your_gemini_key_here    # Alternative provider
```

**💡 Pro Tip:** Start with `./demo 1` - it works immediately without any API keys!

## 🗂️ Project Structure

```
├── 📄 LICENSE                    # MIT License
├── 📄 README.md                  # This file
├── 🚀 demo                       # Bash launcher (./demo 1)
├── 🐍 demo.py                    # Python launcher (python demo.py 1)
├── 📁 events/                    # Test scenarios
│   ├── event-1.txt              #   └─ Tariff crisis (HIGH risk)
│   ├── event-2.txt              #   └─ Normal operations (LOW risk)  
│   ├── event-3.txt              #   └─ Shipping delays (MEDIUM risk)
│   └── event-4.txt              #   └─ Enhanced rules demo
├── 📁 prompts/                   # AI prompt templates
│   └── ai-reasoning-prompt.txt  #   └─ Microprompting template
├── 📄 requirements.txt           # Python dependencies
├── 📁 runners/                   # Stage implementations
│   ├── __init__.py              #   └─ Package marker
│   ├── ai_integration.py        #   └─ Real AI integration (Stage 2)
│   └── mock_simulation.py       #   └─ Mock AI simulation (Stage 1)
└── 📁 supply_chain/             # Core tutorial package
    ├── __init__.py              #   └─ Package marker
    ├── initial_state.py         #   └─ Baseline facts
    ├── prompt_loader.py         #   └─ Template management
    ├── rules_ai_baseline.py     #   └─ Real AI rules (baseline)
    ├── rules_ai_enhanced.py     #   └─ Real AI + fallback guardrails
    ├── rules_mock.py            #   └─ Mock AI simulation rules
    └── schema.py                #   └─ Domain model (Facts)
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

- **Tutorial Article**: [Read the full tutorial](#) (comprehensive walkthrough)
- **Vulcan Documentation**: [Full documentation here](https://latchfield.com/vulcan/docs/)

## 🤝 Contributing

This tutorial is designed to be self-contained and educational. If you find areas for improvement or have suggestions for additional scenarios, please open an issue or submit a pull request.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.