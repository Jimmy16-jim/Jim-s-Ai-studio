import streamlit as st
import random
import base64

st.set_page_config(page_title="AI Text Studio", page_icon="🧠", layout="wide")
if st.button("🏠 Back to Home"):
    st.switch_page("app.py")

# ---------- BACKGROUND ----------

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

text_bg1 = image_to_base64("assets/text1.jpg")
text_bg2 = image_to_base64("assets/text2.jpg")

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    animation: textStudioBg 18s infinite;
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

@keyframes textStudioBg {{
    0% {{
        background-image: linear-gradient(rgba(0,0,0,.76), rgba(0,0,0,.9)), url("data:image/jpg;base64,{text_bg1}");
    }}
    50% {{
        background-image: linear-gradient(rgba(0,0,0,.76), rgba(0,0,0,.9)), url("data:image/jpg;base64,{text_bg2}");
    }}
    100% {{
        background-image: linear-gradient(rgba(0,0,0,.76), rgba(0,0,0,.9)), url("data:image/jpg;base64,{text_bg1}");
    }}
}}

[data-testid="stSidebar"] {{
    background: rgba(8,8,25,.97);
    border-right: 1px solid rgba(168,85,247,.35);
}}

.title {{
    font-size: 55px;
    font-weight: 900;
    text-align: center;
    color: white;
    text-shadow: 0 0 22px #a855f7;
    margin-bottom: 20px;
}}

.info-box, .output-box {{
    background: rgba(0,0,0,.62);
    padding: 28px;
    border-radius: 22px;
    border: 1px solid rgba(255,255,255,.18);
    color: white;
    font-size: 17px;
    line-height: 1.8;
}}

.stButton>button {{
    width: 100%;
    height: 52px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg,#7f00ff,#e100ff);
    color: white;
    font-size: 17px;
    font-weight: 800;
}}

.stButton>button:hover {{
    box-shadow: 0 0 25px #c084fc;
    transform: scale(1.02);
}}
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🧠 AI Text & Creator Guide Studio</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
<h3>🚀 Fast Creator Writing Assistant</h3>
<p>
Generate scripts, captions, titles, hashtags, creator guides, monetization plans and channel growth strategies instantly.
This module is optimized for speed and works without paid APIs.
</p>
</div>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------

st.sidebar.markdown("## ⚙️ Text Studio Controls")

tool = st.sidebar.selectbox("Choose Tool", [
    "YouTube Title Generator",
    "Instagram Caption Generator",
    "Video Script Generator",
    "Reel Hook Generator",
    "Hashtag Generator",
    "Thumbnail Text Generator",
    "Video Description Generator",
    "Brand Bio Generator",
    "Content Calendar Generator",
    "Monetization Guide",
    "Content Creation Guide",
    "Channel/Page Handling Guide",
    "AI Creator Assistant"
])

topic = st.sidebar.text_input("Enter Topic / Niche", "AI tools")
platform = st.sidebar.selectbox("Platform", ["YouTube", "Instagram", "TikTok", "Facebook", "General"])
tone = st.sidebar.selectbox("Tone", ["Professional", "Friendly", "Viral", "Motivational", "Gaming", "Educational"])
length = st.sidebar.selectbox("Output Length", ["Short", "Medium", "Detailed", "Full Professional"])
days = st.sidebar.selectbox("Calendar Duration", ["7 Days", "15 Days", "30 Days"])

question = ""
if tool == "AI Creator Assistant":
    question = st.sidebar.text_area("Ask your creator question", "How can I grow my channel?")

generate = st.sidebar.button("✨ Generate")

# ---------- SMART DATA ----------

def length_level(length):
    return {
        "Short": 1,
        "Medium": 2,
        "Detailed": 3,
        "Full Professional": 4
    }.get(length, 2)

def niche_angle(topic):
    topic_l = topic.lower()

    if any(x in topic_l for x in ["game", "gaming", "gta", "pubg", "free fire"]):
        return {
            "audience": "young viewers, gamers and entertainment-focused audiences",
            "style": "fast-paced visuals, bold thumbnails, energetic hooks and exciting editing",
            "examples": "gameplay highlights, reaction clips, challenge videos, tips, rankings and funny moments"
        }

    if any(x in topic_l for x in ["fitness", "gym", "health", "diet"]):
        return {
            "audience": "people who want self-improvement, better health and practical routines",
            "style": "clear demonstrations, motivational tone, progress-based content and simple explanations",
            "examples": "workout plans, diet tips, transformation videos, mistakes to avoid and daily routines"
        }

    if any(x in topic_l for x in ["business", "money", "finance", "earning", "startup"]):
        return {
            "audience": "students, entrepreneurs and people interested in income growth",
            "style": "professional presentation, proof-based points, practical steps and strong examples",
            "examples": "case studies, earning methods, mistakes, strategy breakdowns and comparison videos"
        }

    if any(x in topic_l for x in ["ai", "technology", "tech", "coding", "software"]):
        return {
            "audience": "students, tech learners, creators and people interested in digital tools",
            "style": "simple explanations, screen recordings, examples, demonstrations and tool comparisons",
            "examples": "tutorials, AI tool reviews, coding explainers, project demos and productivity hacks"
        }

    if any(x in topic_l for x in ["beauty", "fashion", "makeup", "skin"]):
        return {
            "audience": "lifestyle viewers, beginners and people looking for personal improvement",
            "style": "clean visuals, before-after results, product-focused shots and friendly explanation",
            "examples": "tutorials, product reviews, routines, styling tips and transformation videos"
        }

    return {
        "audience": "people interested in practical and useful content around this topic",
        "style": "clear explanation, attractive visuals, useful examples and simple language",
        "examples": "tips, tutorials, mistakes, comparisons, guides and personal experience videos"
    }

# ---------- BASIC GENERATORS ----------

def titles(topic):
    items = [
        f"{topic}: Complete Beginner Guide",
        f"I Tried {topic} and This Happened!",
        f"Top 5 Things You Must Know About {topic}",
        f"How {topic} Can Change Your Content Game",
        f"The Truth About {topic} Nobody Tells You",
        f"{topic} Explained in Simple Words",
        f"Best Way to Start with {topic}",
        f"Common Mistakes People Make in {topic}",
        f"How to Use {topic} Like a Pro",
        f"Why {topic} is Becoming So Popular"
    ]
    return "\n".join(f"{i+1}. {title}" for i, title in enumerate(items))

def captions(topic, tone):
    return f"""Creating better content with {topic}! 🚀

If you want real growth, focus on:
• clear message
• strong visuals
• useful information
• consistency
• audience engagement

The goal is not just to post more.
The goal is to post better.

Save this for later and follow for more creator tips ✨"""

def hooks(topic):
    items = [
        f"Stop scrolling! This is why {topic} matters.",
        f"Most people use {topic} the wrong way.",
        f"Here is a simple trick to improve your results with {topic}.",
        f"You will not believe how powerful {topic} can be.",
        f"If you create content, you need to understand {topic}.",
        f"This one idea can completely change how you use {topic}.",
        f"Beginners usually make this mistake with {topic}.",
        f"Want better results? Start using {topic} properly."
    ]
    return "\n".join(f"{i+1}. {x}" for i, x in enumerate(items))

def hashtags(topic):
    clean = topic.replace(" ", "")
    return f"#{clean} #AI #ContentCreator #DigitalMarketing #Reels #YouTube #CreatorTips #ViralContent #Editing #Growth #OnlineBusiness #CreatorStudio"

def thumbnail_text(topic):
    lines = [
        f"BEST {topic.upper()}",
        "SECRET REVEALED",
        "THIS CHANGED EVERYTHING",
        "YOU NEED THIS!",
        "TOP 5 TIPS",
        "DON'T MISS THIS",
        "I TRIED THIS!",
        "INSANE RESULTS"
    ]
    return "\n".join(lines)

def description(topic):
    return f"""In this video, we discuss {topic} in a simple and practical way.

You will learn:
• what {topic} means
• why it is useful
• how to apply it in real content creation
• common mistakes beginners should avoid
• simple tips for better results

If you found this helpful, like, comment, share and subscribe.

#AI #ContentCreation #CreatorStudio #Editing #DigitalTools"""

def bio(topic, platform):
    return f"""Helping creators grow with {topic} 🚀
Content tips | Editing ideas | Digital growth
Built for {platform} creators
Follow for practical creator guidance ✨"""

def calendar(topic, days):
    number = int(days.split()[0])
    angles = [
        "Beginner tips",
        "Common mistakes",
        "Step-by-step tutorial",
        "Before and after example",
        "Myth vs reality",
        "Tool recommendation",
        "Quick checklist",
        "Case study",
        "Motivational post",
        "Behind the scenes"
    ]
    output = []
    for i in range(1, number + 1):
        angle = angles[(i - 1) % len(angles)]
        output.append(f"Day {i}: {angle} about {topic}")
    return "\n".join(output)

# ---------- LONG GENERATORS WITHOUT REPETITION ----------

def video_script(topic, platform, tone, length):
    angle = niche_angle(topic)
    level = length_level(length)

    sections = [
        f"""TITLE:
{topic} - Complete Video Script for {platform}

OPENING HOOK:
If you are interested in {topic}, this video will help you understand it in a simple and practical way. Many people start without a clear plan, and because of that, their content does not perform well. In this video, we will break the topic into easy steps.""",

        f"""INTRODUCTION:
Hello everyone, welcome back. Today we are going to talk about {topic}. This topic is useful for {angle['audience']}. The best part is that you do not need to be perfect in the beginning. You only need a clear direction, consistent effort and a simple strategy.""",

        f"""SECTION 1 - BASIC UNDERSTANDING:
Before creating content about {topic}, it is important to understand the audience. Your audience includes {angle['audience']}. They want content that is easy to understand, visually attractive and practically useful. If your content solves a problem or gives value, people are more likely to watch, save and share it.""",

        f"""SECTION 2 - CONTENT STYLE:
For this topic, the recommended content style is {angle['style']}. This means your content should not feel boring or random. Every video should have a clear hook, a useful middle part and a strong ending. Good editing, clean captions and attractive thumbnails can improve results.""",

        f"""SECTION 3 - CONTENT EXAMPLES:
Some good content ideas for {topic} are {angle['examples']}. These formats work because they are simple, searchable and easy for the audience to connect with. A beginner should start with short, clear and direct videos instead of trying to create perfect content.""",

        f"""SECTION 4 - PRACTICAL STEPS:
First, choose one specific idea. Second, write a short script. Third, record only the important points. Fourth, edit the video by removing boring parts. Fifth, add captions and a clear title. Finally, post it and check the response. This process helps improve content quality over time."""
    ]

    if level >= 2:
        sections += [
            f"""SECTION 5 - ENGAGEMENT STRATEGY:
Engagement is very important on {platform}. Ask viewers a question, encourage comments and use a clear call to action. Instead of only saying “like and subscribe,” give people a reason. For example, say that you will share more useful content about {topic} in future videos.""",

            f"""SECTION 6 - COMMON MISTAKES:
A common mistake is creating content without knowing the audience. Another mistake is using weak titles and thumbnails. Some creators also make videos too long without giving value. To avoid this, keep the message clear, use good pacing and focus on one main idea per video."""
        ]

    if level >= 3:
        sections += [
            f"""SECTION 7 - IMPROVEMENT PLAN:
After posting, study the performance. Check watch time, likes, comments, shares and saves. If people leave early, improve your hook. If people do not click, improve your thumbnail and title. If people do not comment, ask better questions. Content creation improves through testing.""",

            f"""SECTION 8 - BRANDING:
Your content should have a consistent style. Use similar colors, fonts, tone and thumbnail structure. This makes your content recognizable. Over time, people should understand your brand just by looking at your posts or videos."""
        ]

    if level >= 4:
        sections += [
            f"""SECTION 9 - LONG TERM ROADMAP:
In the first month, focus on learning and posting consistently. In the second month, improve editing and thumbnails. In the third month, study analytics and double down on what works. After that, start building a stronger identity around {topic}. This roadmap helps you grow without confusion.""",

            f"""FINAL CONCLUSION:
To succeed with {topic}, remember three things: clarity, consistency and improvement. Do not wait for perfect conditions. Start with simple content, learn from each upload and improve step by step. If this video helped you, share it with someone who wants to grow as a creator."""
        ]

    return "\n\n".join(sections)

def monetization_guide(topic, platform, length):
    angle = niche_angle(topic)
    level = length_level(length)

    sections = [
        f"""MONETIZATION GUIDE FOR {platform.upper()}

Niche: {topic}

Monetization means earning money from your content, audience, skills or personal brand. For a niche like {topic}, the main audience is {angle['audience']}. Before earning money, the first goal should be building trust and creating useful content.""",

        f"""1. Build Audience Trust:
Money comes after trust. If people trust your knowledge, recommendations and content style, they are more likely to buy products, join communities or follow your suggestions. Focus on solving real problems and giving practical value.""",

        f"""2. Ad Revenue:
On platforms like YouTube, creators can earn through ads after meeting eligibility requirements. To improve ad revenue, create searchable content, use strong titles, improve watch time and post consistently.""",

        f"""3. Sponsorships:
Brands pay creators to promote products or services. For {topic}, sponsorships can come from tools, apps, services, products or brands connected to your niche. Even small creators can get sponsorships if their audience is targeted.""",

        f"""4. Affiliate Marketing:
Affiliate marketing means promoting a product and earning commission when someone buys from your link. This works best when the product is genuinely useful for your audience."""
    ]

    if level >= 2:
        sections += [
            f"""5. Digital Products:
You can sell digital products such as ebooks, templates, guides, presets, thumbnails, content calendars, editing packs or online courses. Digital products are powerful because they can be sold multiple times without repeated physical cost.""",

            f"""6. Freelancing:
Your content skills can become services. You can offer editing, thumbnail design, script writing, social media handling, content planning or page management. This is one of the easiest ways for beginners to earn before becoming a large creator."""
        ]

    if level >= 3:
        sections += [
            f"""7. Paid Community:
Once your audience grows, you can build a paid group, mentorship program or exclusive community. This is useful when your audience wants deeper guidance and direct support.""",

            f"""8. Brand Positioning:
Your profile should clearly show what you do. Use a clean bio, proper profile picture, good banner and consistent content style. Brands prefer creators who look organized and professional."""
        ]

    if level >= 4:
        sections += [
            f"""9. Six Month Monetization Roadmap:
Month 1: Choose niche and post consistently.
Month 2: Improve content quality, thumbnails and captions.
Month 3: Study analytics and identify best-performing content.
Month 4: Start affiliate marketing and small collaborations.
Month 5: Offer freelancing services or digital products.
Month 6: Approach brands and create a media kit.""",

            f"""10. Final Advice:
Do not depend on only one income source. A smart creator combines ad revenue, sponsorships, affiliate marketing, digital products and services. The strongest monetization comes when your audience sees you as valuable and trustworthy."""
        ]

    return "\n\n".join(sections)

def content_creation_guide(topic, platform, length):
    angle = niche_angle(topic)
    level = length_level(length)

    sections = [
        f"""CONTENT CREATION GUIDE FOR {platform.upper()}

Topic/Niche: {topic}

Content creation is the process of planning, producing, editing and publishing content for an audience. For {topic}, your audience usually includes {angle['audience']}. The goal is to create content that is clear, useful and engaging.""",

        f"""1. Choose a Clear Content Goal:
Every post or video should have a purpose. It can educate, entertain, inspire, promote or explain. If your goal is unclear, the content becomes confusing for viewers.""",

        f"""2. Understand Your Audience:
The audience should feel that your content is made for them. Understand their problems, interests and expectations. This helps you create better hooks, examples and explanations.""",

        f"""3. Use Content Pillars:
Content pillars are main categories. For {topic}, you can create tutorials, mistakes, tips, comparisons, reviews, behind-the-scenes content and personal experiences."""
    ]

    if level >= 2:
        sections += [
            f"""4. Write Strong Hooks:
The first few seconds matter the most. A good hook creates curiosity. Example hooks include: “Most beginners make this mistake,” “Here is a simple trick,” or “This changed how I use {topic}.”""",

            f"""5. Improve Visual Quality:
Use clean visuals, readable text, good lighting and proper framing. For digital content, strong visuals can increase attention and retention."""
        ]

    if level >= 3:
        sections += [
            f"""6. Editing Strategy:
Remove unnecessary pauses, add captions, use zoom effects and keep the video moving. Editing should support the message, not distract from it.""",

            f"""7. Posting Strategy:
Consistency matters. Posting three to five times a week is better than posting randomly. A schedule helps the audience know when to expect new content."""
        ]

    if level >= 4:
        sections += [
            f"""8. Analytics:
Study watch time, likes, comments, shares and saves. If viewers leave early, improve hooks. If posts get low reach, improve titles, thumbnails or timing.""",

            f"""9. Final Content System:
Research ideas, write short scripts, create content in batches, edit properly, post consistently and review analytics weekly. This system helps creators improve over time."""
        ]

    return "\n\n".join(sections)

def channel_guide(topic, platform, length):
    level = length_level(length)

    sections = [
        f"""CHANNEL / PAGE HANDLING GUIDE FOR {platform.upper()}

Niche: {topic}

Managing a channel or page means handling profile setup, branding, content planning, posting, audience engagement and analytics. A professional page should look clear, organized and trustworthy.""",

        f"""1. Profile Setup:
Use a clean profile picture, attractive banner and simple bio. Your bio should explain what your audience will get from your content.""",

        f"""2. Branding:
Use consistent colors, fonts, thumbnails and content style. Branding helps people recognize your content quickly.""",

        f"""3. Posting Schedule:
Plan your content weekly. Beginners can start with three to five posts per week. Consistency helps build audience trust."""
    ]

    if level >= 2:
        sections += [
            f"""4. Audience Interaction:
Reply to comments, ask questions and encourage discussion. This makes followers feel connected to your page.""",

            f"""5. Content Mix:
Use educational, entertaining and promotional content. Do not post only promotional content because people follow pages for value."""
        ]

    if level >= 3:
        sections += [
            f"""6. Analytics Review:
Every week, check which posts performed best. Study reach, engagement, saves and watch time. Then create more content around successful topics.""",

            f"""7. Collaboration:
Collaborate with other creators in your niche. Collaborations help you reach new audiences and build credibility."""
        ]

    if level >= 4:
        sections += [
            f"""8. Long-Term System:
Create a monthly content plan, keep backup content ready, improve thumbnails, test new formats and build a recognizable brand identity.""",

            f"""9. Final Advice:
A good channel grows through patience, consistency and improvement. Avoid copying blindly. Learn from others, but build your own identity."""
        ]

    return "\n\n".join(sections)

def creator_assistant(topic, question, length):
    level = length_level(length)
    angle = niche_angle(topic)

    answer = [
        f"""AI CREATOR ASSISTANT RESPONSE

Question:
{question}

Topic/Niche:
{topic}

Answer:
For this topic, your audience is mainly {angle['audience']}. The best strategy is to create useful, clear and engaging content. Start by understanding what your audience wants, then create content that solves their problems or gives them practical value.""",

        f"""Practical Steps:
1. Choose one clear niche.
2. Create three to five content pillars.
3. Use strong hooks in every post or video.
4. Add captions and improve visuals.
5. Post consistently.
6. Study analytics every week.
7. Improve based on what works."""
    ]

    if level >= 3:
        answer.append(f"""Advanced Suggestion:
Create content in different formats such as tutorials, mistakes, comparisons, reactions, guides and case studies. This keeps your page fresh and helps you understand which format your audience likes most.""")

    if level >= 4:
        answer.append(f"""Long-Term Plan:
For the first month, focus on posting and learning. In the second month, improve quality and branding. In the third month, start tracking analytics properly. After that, build monetization options such as affiliate marketing, services, sponsorships and digital products.""")

    return "\n\n".join(answer)

# ---------- OUTPUT ----------

if generate:
    if not topic.strip():
        st.warning("Please enter a topic or niche.")
    else:
        if tool == "YouTube Title Generator":
            output = titles(topic)
        elif tool == "Instagram Caption Generator":
            output = captions(topic, tone)
        elif tool == "Video Script Generator":
            output = video_script(topic, platform, tone, length)
        elif tool == "Reel Hook Generator":
            output = hooks(topic)
        elif tool == "Hashtag Generator":
            output = hashtags(topic)
        elif tool == "Thumbnail Text Generator":
            output = thumbnail_text(topic)
        elif tool == "Video Description Generator":
            output = description(topic)
        elif tool == "Brand Bio Generator":
            output = bio(topic, platform)
        elif tool == "Content Calendar Generator":
            output = calendar(topic, days)
        elif tool == "Monetization Guide":
            output = monetization_guide(topic, platform, length)
        elif tool == "Content Creation Guide":
            output = content_creation_guide(topic, platform, length)
        elif tool == "Channel/Page Handling Guide":
            output = channel_guide(topic, platform, length)
        elif tool == "AI Creator Assistant":
            output = creator_assistant(topic, question, length)
        else:
            output = "Select a tool."

        st.markdown(f"""
        <div class="output-box">
        <h2>✨ Generated Output</h2>
        <pre style="white-space: pre-wrap; font-family: inherit;">{output}</pre>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            "💾 Download Text",
            output,
            file_name="generated_text.txt",
            mime="text/plain"
        )
else:
    st.info("👈 Choose a tool, enter your topic/niche, select length and click Generate.")