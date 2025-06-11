# 🔮 ML+Dev Track: Week 3
## 🎯 Tweet Generation Engine (Task 2)

### 🧠 Quick Recap
Last week, you:
- Built a model to predict tweet likes from metadata
- Created a Flask API with a `/predict` endpoint
- Used features like `word_count`, `char_count`, `has_media`, etc.
- Successfully tested your API and got predictions

Now, you'll build a **second API** for generating tweet content! 🎉  
**Key Point**: You'll keep your Week 2 API running and add this new one alongside it.

### 🏁 Week 3 Goals
By the end of the week, you will:
- Create a simple tweet generator (no complex AI needed to start!)
- Build a `/generate` API endpoint (similar to your `/predict` endpoint)
- Test both APIs working together
- Have fun generating creative tweets!

**✅ Deliverable: Working `/generate` API that creates tweets from input data**

---

## 🚀 Step 1: Start Simple - Template-Based Generation

Let's begin with something achievable that builds on what you already know!

### 📝 Create Your Tweet Generator Class

```python
# tweet_generator.py
import random

class SimpleTweetGenerator:
    def __init__(self):
        # Simple templates - you can add more!
        self.templates = {
            'announcement': [
                "🚀 Exciting news from {company}! {message}",
                "Big announcement: {company} is {message} 🎉",
                "Hey everyone! {company} has {message} ✨"
            ],
            'question': [
                "What do you think about {topic}? Let us know! 💬",
                "Quick question: How do you feel about {topic}? 🤔",
                "{company} wants to know: What's your take on {topic}? 🗣️"
            ],
            'general': [
                "Check out what {company} is up to! {message} 🌟",
                "{company} update: {message} 💯",
                "From the {company} team: {message} 🔥"
            ]
        }
    
    def generate_tweet(self, company, tweet_type="general", message="Something awesome!", topic="innovation"):
        # Pick a random template
        template_list = self.templates.get(tweet_type, self.templates['general'])
        template = random.choice(template_list)
        
        # Fill in the template
        tweet = template.format(
            company=company,
            message=message,
            topic=topic
        )
        
        # Make sure it's not too long (Twitter limit is 280 characters)
        if len(tweet) > 280:
            tweet = tweet[:277] + "..."
        
        return tweet

# Test it out!
generator = SimpleTweetGenerator()
test_tweet = generator.generate_tweet("Nike", "announcement", "launching new running shoes")
print(test_tweet)
```

### 🧪 Test Your Generator
```python
# Quick test
generator = SimpleTweetGenerator()

print("Test 1:", generator.generate_tweet("Starbucks", "question", topic="coffee"))
print("Test 2:", generator.generate_tweet("Apple", "announcement", "releasing iOS update"))
print("Test 3:", generator.generate_tweet("Tesla", "general", "changing the world"))
```

---

## 🌐 Step 2: Build Your Generation API (Just Like Week 2!)

This will look very similar to your prediction API from Week 2:

```python
# app_generator.py (separate file from your Week 2 predictor)
from flask import Flask, request, jsonify
from tweet_generator import SimpleTweetGenerator

app = Flask(__name__)
generator = SimpleTweetGenerator()

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        
        # Get inputs (similar to how you got features in Week 2)
        company = data.get('company', 'Our Company')
        tweet_type = data.get('tweet_type', 'general')
        message = data.get('message', 'Something awesome!')
        topic = data.get('topic', 'innovation')
        
        # Generate tweet (similar to how you predicted likes)
        generated_tweet = generator.generate_tweet(company, tweet_type, message, topic)
        
        return jsonify({
            'generated_tweet': generated_tweet,
            'success': True,
            'company': company,
            'type': tweet_type
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Tweet Generator API is running!'})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Different port from your Week 2 API
```

---

## 🧪 Step 3: Test Your New API

### Using curl (just like Week 2):
```bash
curl -X POST http://localhost:5001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Nike",
    "tweet_type": "announcement",
    "message": "launching new Air Max shoes",
    "topic": "running"
  }'
```

### Using Python (just like Week 2):
```python
import requests

# Test your new generator API
response = requests.post('http://localhost:5001/generate', json={
    'company': 'Starbucks',
    'tweet_type': 'question',
    'message': 'trying new recipes',
    'topic': 'coffee'
})

print("Generated Tweet:", response.json())
```

---

## 🔗 Step 4: Run Both APIs Together

Now you have two APIs working! Here's how to test them both:

### Terminal 1 (Week 2 API):
```bash
cd your_week2_folder
python app.py  # Your prediction API on port 5000
```

### Terminal 2 (Week 3 API):
```bash
cd your_week3_folder  
python app_generator.py  # Your generation API on port 5001
```

### Test Both:
```python
import requests

# Test prediction API (from Week 2)
prediction_response = requests.post('http://localhost:5000/predict', json={
    'word_count': 15,
    'char_count': 120,
    'has_media': True,
    'hour': 14,
    'sentiment': 0.8
})

# Test generation API (from Week 3)  
generation_response = requests.post('http://localhost:5001/generate', json={
    'company': 'Nike',
    'tweet_type': 'announcement',
    'message': 'launching new product',
    'topic': 'sports'
})

print("Predicted Likes:", prediction_response.json())
print("Generated Tweet:", generation_response.json())
```

---

## ✅ Week 3 Core Deliverables (Everyone Should Complete This!)

**✅ Simple tweet generator class** with templates  
**✅ Flask API with `/generate` endpoint**  
**✅ Successfully test both Week 2 and Week 3 APIs together**  
**✅ JSON responses similar to your prediction API**

**🎯 You're Done with the Basics! Everything above should be achievable by anyone who completed Week 2.**

---

## 🏆 BONUS SECTION 

Want to go beyond the basics? Try these challenges:

### 🤖 Bonus 1: Add AI-Powered Generation

Install transformers and use a real AI model:

```python
# bonus_ai_generator.py
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class AITweetGenerator:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained('gpt2')
        self.model = GPT2LMHeadModel.from_pretrained('gpt2')
        self.tokenizer.pad_token = self.tokenizer.eos_token
    
    def generate_ai_tweet(self, prompt, max_length=60):
        inputs = self.tokenizer.encode(prompt, return_tensors='pt')
        
        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=max_length,
                temperature=0.8,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
        
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        tweet = generated_text[len(prompt):].strip()
        return tweet[:280]  # Twitter limit

# Add this to your API as a bonus endpoint
@app.route('/generate_ai', methods=['POST'])
def generate_ai():
    # Implementation here...
    pass
```

### 🎨 Bonus 2: Smart Feature Integration

Use your Week 2 features to make smarter tweets:

```python
def generate_smart_tweet(self, word_count_target, sentiment_target, has_media):
    # Adjust templates based on predicted features
    if sentiment_target > 0.5:
        templates = self.positive_templates
    elif sentiment_target < -0.5:
        templates = self.negative_templates
    else:
        templates = self.neutral_templates
    
    # Adjust length based on word_count_target
    # Add media mentions if has_media is True
    # ... your smart logic here
```

### 🌟 Bonus 3: Advanced Template System

```python
class AdvancedTweetGenerator:
    def __init__(self):
        self.brand_voices = {
            'casual': {'emojis': True, 'tone': 'friendly'},
            'professional': {'emojis': False, 'tone': 'formal'},
            'playful': {'emojis': True, 'tone': 'fun'},
        }
        
        self.industry_templates = {
            'tech': ["🚀 Innovation alert: {message}", "Tech news: {message}"],
            'food': ["🍕 Delicious update: {message}", "Tasty news: {message}"],
            'fashion': ["✨ Style update: {message}", "Fashion alert: {message}"]
        }
    
    def generate_branded_tweet(self, company, industry, brand_voice, message):
        # Advanced generation logic here...
        pass
```

### 🔥 Bonus 4: Connect to Your Week 2 Model

```python
@app.route('/generate_and_predict', methods=['POST'])
def generate_and_predict():
    """Generate a tweet AND predict how many likes it will get!"""
    data = request.get_json()
    
    # Generate tweet
    generated_tweet = generator.generate_tweet(...)
    
    # Calculate features from generated tweet
    features = extract_features_from_tweet(generated_tweet)
    
    # Predict likes using your Week 2 model
    predicted_likes = model.predict([features])[0]
    
    return jsonify({
        'generated_tweet': generated_tweet,
        'predicted_likes': int(predicted_likes),
        'success': True
    })
```

---

## 📚 Learning Resources

**For Everyone:**
- [Flask Tutorial - Official Docs](https://flask.palletsprojects.com/en/2.0.x/tutorial/)
- [Python String Formatting](https://docs.python.org/3/tutorial/inputoutput.html)
- [Working with JSON in Python](https://docs.python.org/3/library/json.html)

**For Bonus Sections:**
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [GPT-2 Text Generation](https://huggingface.co/gpt2)
- [Advanced Flask Patterns](https://flask.palletsprojects.com/en/2.0.x/patterns/)

---

## 🔮 What's Next (Week 4)

- Build a simple web interface (probably using Streamlit)
- Connect your prediction API + generation API in one interface
- Let users input metadata and see both predicted likes AND generated tweets
- Create a demo that marketers can actually use!

**Build smart. Start simple. Scale up! 🚀**

---

## 🤔 Common Questions

**Q: Do I need to install heavy AI libraries?**  
A: No! Start with the template approach. AI is in the bonus section.

**Q: Will my Week 2 code still work?**  
A: Yes! You're building a separate API that works alongside your existing one.

**Q: What if I can't get the AI models working?**  
A: The template generator is perfectly fine! Many real apps use template-based generation.

**Q: How do I know if my API is working?**  
A: Same way you tested Week 2 - use curl or Python requests to send JSON and get responses back.
