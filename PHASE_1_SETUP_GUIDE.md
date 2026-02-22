# PHASE 1: CORE AI SYSTEM - SETUP GUIDE
# Thai Language Learning App - AI Integration

## 📦 WHAT'S INCLUDED

Phase 1 gives you a complete AI agent with 6 modes:
✅ 🗣️ Conversation Mode - Practice Thai dialogue
✅ 🎓 Tutor Mode - Get explanations and answers  
✅ 📝 Generator Mode - Create custom exercises
✅ 🌏 Cultural Guide - Learn Thai customs
✅ ☸️ Buddhist Guide - Explore Theravada teachings
✅ 💡 Helper Mode - Get smart hints

## 🚀 INSTALLATION STEPS

### Step 1: Install Required Package

```bash
pip install anthropic --break-system-packages
```

### Step 2: Get Your Anthropic API Key

1. Go to https://console.anthropic.com
2. Sign up or log in
3. Navigate to "API Keys" section
4. Create a new API key
5. Copy the key (starts with "sk-ant-...")

### Step 3: Set Your API Key

**Option A - Environment Variable (Recommended for production):**

Linux/Mac:
```bash
export ANTHROPIC_API_KEY='sk-ant-your-key-here'
```

Windows (Command Prompt):
```cmd
set ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Windows (PowerShell):
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

**Option B - In Code (For testing only):**
Add to app.py after imports:
```python
import os
os.environ['ANTHROPIC_API_KEY'] = 'sk-ant-your-key-here'
```

⚠️ **SECURITY WARNING**: Never commit API keys to Git! 
Add this to your .gitenv file if using Option B.

### Step 4: Copy Files to Your Project

Copy these files to your project:

1. **ai_agent.py** → Root directory (same level as app.py)
2. **chat.html** → templates/ directory
3. **ai_integration.py** → Reference file (contains code to add to app.py)

### Step 5: Update Your app.py

Add this import near the top of app.py (after other imports):

```python
from ai_agent import get_ai_agent
```

Add this initialization code after `app = Flask(__name__)`:

```python
# Initialize AI agent
try:
    ai_agent = get_ai_agent()
    print("✅ AI Agent initialized successfully!")
except Exception as e:
    print(f"⚠️ AI Agent initialization failed: {e}")
    print("   Please set ANTHROPIC_API_KEY environment variable")
    ai_agent = None
```

Add all the routes from ai_integration.py to your app.py.
(You can copy the entire "AI ROUTES" section)

### Step 6: Update Navigation (Optional but Recommended)

Add AI Chat link to your navigation in base.html:

Find the navigation section and add:

```html
<li><a href="/chat">🤖 AI Chat</a></li>
```

### Step 7: Test the Installation

1. Start your Flask app:
```bash
python app.py
```

2. Look for this in the startup output:
```
✅ AI Agent initialized successfully!
```

3. Visit: http://localhost:5000/chat

4. Try these test messages:
   - "สวัสดีครับ" (Hello in Thai)
   - "Explain Thai tones to me"
   - "Tell me about Thai Buddhism"

## ✅ VERIFICATION CHECKLIST

- [ ] anthropic package installed
- [ ] API key obtained from console.anthropic.com
- [ ] API key set as environment variable or in code
- [ ] ai_agent.py copied to project root
- [ ] chat.html copied to templates/
- [ ] app.py updated with imports and routes
- [ ] Flask app starts without errors
- [ ] "✅ AI Agent initialized" appears in console
- [ ] Can access /chat page
- [ ] Can send messages and get responses
- [ ] All 6 modes work (test by switching modes)

## 💰 COST INFORMATION

**Claude Sonnet 4 Pricing:**
- Input: ~$3 per million tokens
- Output: ~$15 per million tokens

**Real Usage Examples:**
- Simple conversation (10 messages): ~$0.05
- Long tutoring session (50 messages): ~$0.25
- Heavy daily use (200 messages): ~$1.00

**Typical Monthly Costs:**
- Light personal use: $5-10/month
- Regular practice: $20-30/month
- Heavy development/testing: $50-100/month

You only pay for what you use. No subscription required.

## 🎯 WHAT YOU CAN DO NOW

### 1. Practice Thai Conversation
Visit: http://localhost:5000/chat
- Switch to "🗣️ Conversation" mode
- Start chatting in Thai or English
- Get corrections and suggestions
- Build real conversational skills

### 2. Get Grammar Help
- Switch to "🎓 Tutor" mode
- Ask questions like:
  - "Explain classifier words"
  - "How do Thai tones work?"
  - "What's the difference between ครับ and ค่ะ?"

### 3. Learn About Culture
- Switch to "🌏 Cultural Guide" mode
- Ask about:
  - Thai festivals
  - Wai etiquette
  - Regional differences
  - Social customs

### 4. Explore Buddhism
- Switch to "☸️ Buddhist Guide" mode
- Learn dharma in Thai
- Understand Buddhist terminology
- Connect language to practice

### 5. Generate Custom Content
- Switch to "📝 Generator" mode
- Request:
  - "Make a quiz about Thai food"
  - "Create flashcards for numbers"
  - "Give me a reading passage"

### 6. Get Smart Hints
- Switch to "💡 Helper" mode
- Get help without spoilers
- Progressive hints that teach

## 🔧 TROUBLESHOOTING

### Problem: "AI Agent initialization failed"
**Solution**: Check your API key
- Verify key starts with "sk-ant-"
- Check environment variable is set
- Try using Option B (in-code) for testing

### Problem: "ModuleNotFoundError: No module named 'anthropic'"
**Solution**: Install the package
```bash
pip install anthropic --break-system-packages
```

### Problem: "APIError: Invalid API key"
**Solution**: 
- Get a new key from console.anthropic.com
- Make sure you copied the entire key
- Check for extra spaces or quotes

### Problem: Chat page loads but no response
**Solution**: Check browser console (F12)
- Look for JavaScript errors
- Check Network tab for failed requests
- Verify /api/ai/chat route is working

### Problem: "Rate limit exceeded"
**Solution**:
- Wait a few seconds between requests
- You're likely testing too fast
- Normal usage won't hit limits

## 📊 MONITORING YOUR USAGE

### In the App:
- Token counter at bottom of chat shows current session usage
- Each message shows token cost

### In Anthropic Console:
1. Go to console.anthropic.com
2. Click "Usage" in sidebar
3. See detailed breakdown by day/model
4. Set up budget alerts (optional)

### Estimated Tokens:
- Simple question: ~500 tokens ($0.01)
- Medium conversation: ~2000 tokens ($0.04)
- Long tutoring: ~5000 tokens ($0.10)

## 🎓 BEST PRACTICES

### 1. Start Conversations Fresh
- Use "Clear Chat" when changing topics
- Keeps context relevant
- Reduces token usage

### 2. Use Appropriate Modes
- Conversation: For practice
- Tutor: For questions
- Cultural/Buddhist: For specific topics
- Generator: For creating materials
- Helper: For hints during exercises

### 3. Be Specific
❌ "Help me learn Thai"
✅ "Explain how to use Thai classifiers with examples"

### 4. Export Important Chats
- Use "Export" button to save transcripts
- Review later for study
- Build personal reference library

### 5. Combine with App Features
- Learn alphabet first (structured)
- Use AI for questions (flexible)
- Practice with quizzes (assessment)
- Chat with AI (real application)

## 🔜 WHAT'S COMING IN PHASE 2

Phase 2 will add:
- 🎯 AI Tutor Button on quiz pages
- 💡 Intelligent hints in exercises
- 🌐 Translation helper
- 📚 Dynamic quiz generation
- 🎨 Better UI integration

These features will integrate AI directly into your existing exercises!

## 📝 NOTES FOR DEVELOPERS

### Architecture Overview:
- **ai_agent.py**: Core AI logic, modes, system prompts
- **chat.html**: Frontend UI for conversations
- **app.py routes**: API endpoints connecting frontend to backend
- **Session management**: Each chat gets unique session_id
- **Context tracking**: User level/XP passed to AI for personalization

### Extending the System:
- Add new modes by editing `get_system_prompt()` in ai_agent.py
- Customize prompts for your teaching style
- Add new API endpoints for specialized features
- Integrate with existing quiz/exercise pages

### Security Considerations:
- API key must be kept secret
- Use environment variables in production
- Add rate limiting if hosting publicly
- Consider user authentication for multi-user deployment

## 🆘 NEED HELP?

If you get stuck:
1. Check the troubleshooting section above
2. Review console output for error messages
3. Test API key with simple curl command:
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: YOUR_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{"model":"claude-sonnet-4-20250514","max_tokens":100,"messages":[{"role":"user","content":"Hello"}]}'
   ```
4. Check Anthropic status: status.anthropic.com

## 🎉 SUCCESS!

Once everything is working, you have:
- A complete AI tutor in 6 modes
- Unlimited practice conversations
- Cultural and Buddhist knowledge base
- Custom content generation
- All integrated into your existing app!

**Ready for Phase 2?** Let me know when you've tested Phase 1 and we'll add:
- AI buttons on quiz pages
- Smart hints in exercises  
- Translation helpers
- And more!

---

**Phase 1 Status**: ✅ COMPLETE - READY TO USE
**Next Phase**: Phase 2 - Learning Features Integration
