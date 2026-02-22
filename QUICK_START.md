# 🚀 QUICK START - 5 MINUTES TO AI-POWERED APP

## STEP 1: Install Package (30 seconds)
```bash
pip install anthropic --break-system-packages
```

## STEP 2: Get API Key (2 minutes)
1. Go to: https://console.anthropic.com
2. Sign up/Login
3. Create API key
4. Copy it (starts with sk-ant-...)

## STEP 3: Set API Key (30 seconds)
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

## STEP 4: Add Files (1 minute)
- Copy **ai_agent.py** to project root (where app.py is)
- Copy **chat.html** to templates/ folder

## STEP 5: Update app.py (1 minute)

Add this at the top after imports:
```python
from ai_agent import get_ai_agent

# Initialize AI
try:
    ai_agent = get_ai_agent()
    print("✅ AI Agent initialized!")
except Exception as e:
    print(f"⚠️ AI failed: {e}")
    ai_agent = None
```

Then copy ALL the routes from **ai_integration.py** into your app.py

## STEP 6: Test! (30 seconds)
```bash
python app.py
```

Visit: http://localhost:5000/chat

Say: "สวัสดีครับ"

## ✅ THAT'S IT!

You now have:
- 🗣️ Thai conversation practice
- 🎓 Intelligent tutoring
- 🌏 Cultural guide
- ☸️ Buddhist teachings
- 📝 Content generator
- 💡 Smart hints

## 💰 COSTS
- Testing (100 messages): ~$0.50
- Daily practice (50 messages/day): ~$10/month
- Heavy use (200 messages/day): ~$40/month

Pay only for what you use!

## 🆘 PROBLEMS?

**"Module not found"**
→ Run: pip install anthropic --break-system-packages

**"Invalid API key"**  
→ Check you copied the full key from console.anthropic.com

**"AI Agent initialization failed"**
→ Make sure: export ANTHROPIC_API_KEY='your-key'

**Chat loads but no response**
→ Check console for errors, verify API key is set

## 📖 FULL GUIDE

See **PHASE_1_SETUP_GUIDE.md** for:
- Detailed instructions
- Troubleshooting
- Best practices
- Cost management
- Advanced features

## 🔜 NEXT: PHASE 2

After Phase 1 works, we'll add:
- AI tutor buttons on quizzes
- Smart hints in exercises
- Translation helpers
- Dynamic content generation

---

**Phase 1 = Complete AI Chat Interface**
**Phase 2 = Deep App Integration**
**Phase 3 = Buddhist + Cultural Specialists**  
**Phase 4 = Voice & Advanced Features**
