"""
training_data.py
All labeled training samples and reply templates for the Naive Bayes model.
Add more samples here to improve model accuracy.
"""

# ─── Labeled Training Samples ─────────────────────────────────────────────────
# Format: (text, intent_label)
TRAINING_SAMPLES = [

    # ── Greetings ──────────────────────────────────────────────────────────────
    ("hello", "greeting"),
    ("hi there", "greeting"),
    ("hey", "greeting"),
    ("good morning", "greeting"),
    ("good evening", "greeting"),
    ("good afternoon", "greeting"),
    ("what's up", "greeting"),
    ("howdy", "greeting"),
    ("greetings", "greeting"),
    ("hey there", "greeting"),
    ("sup", "greeting"),
    ("yo", "greeting"),
    ("hiya", "greeting"),
    ("how's it going", "greeting"),
    ("long time no see", "greeting"),

    # ── Farewell ───────────────────────────────────────────────────────────────
    ("bye", "farewell"),
    ("goodbye", "farewell"),
    ("see you later", "farewell"),
    ("talk later", "farewell"),
    ("gotta go", "farewell"),
    ("take care", "farewell"),
    ("catch you later", "farewell"),
    ("i'm leaving", "farewell"),
    ("see ya", "farewell"),
    ("later", "farewell"),
    ("ttyl", "farewell"),
    ("have a good one", "farewell"),
    ("talk soon", "farewell"),
    ("i'm heading out", "farewell"),
    ("peace out", "farewell"),

    # ── Agreement ──────────────────────────────────────────────────────────────
    ("yes", "agree"),
    ("sure", "agree"),
    ("absolutely", "agree"),
    ("that makes sense", "agree"),
    ("i agree", "agree"),
    ("exactly", "agree"),
    ("totally", "agree"),
    ("for sure", "agree"),
    ("definitely", "agree"),
    ("of course", "agree"),
    ("yeah that's right", "agree"),
    ("you're correct", "agree"),
    ("i think so too", "agree"),
    ("that's true", "agree"),
    ("no doubt", "agree"),

    # ── Disagreement ───────────────────────────────────────────────────────────
    ("no", "disagree"),
    ("i don't think so", "disagree"),
    ("not really", "disagree"),
    ("i disagree", "disagree"),
    ("that's wrong", "disagree"),
    ("i doubt it", "disagree"),
    ("i'm not sure about that", "disagree"),
    ("that doesn't seem right", "disagree"),
    ("i beg to differ", "disagree"),
    ("nope", "disagree"),
    ("negative", "disagree"),
    ("i can't agree with that", "disagree"),

    # ── Question ───────────────────────────────────────────────────────────────
    ("how are you", "question"),
    ("what do you think", "question"),
    ("can you help", "question"),
    ("what time is it", "question"),
    ("where are you", "question"),
    ("when is the meeting", "question"),
    ("why did that happen", "question"),
    ("who did this", "question"),
    ("what is this about", "question"),
    ("can you explain", "question"),
    ("do you know", "question"),
    ("have you heard", "question"),
    ("what happened", "question"),
    ("are you available", "question"),
    ("how does this work", "question"),

    # ── Gratitude ──────────────────────────────────────────────────────────────
    ("thank you", "gratitude"),
    ("thanks a lot", "gratitude"),
    ("i appreciate it", "gratitude"),
    ("much appreciated", "gratitude"),
    ("thanks so much", "gratitude"),
    ("grateful", "gratitude"),
    ("thanks for your help", "gratitude"),
    ("i owe you one", "gratitude"),
    ("you're a lifesaver", "gratitude"),
    ("that was really helpful", "gratitude"),
    ("cheers", "gratitude"),
    ("big thanks", "gratitude"),

    # ── Apology ────────────────────────────────────────────────────────────────
    ("sorry", "apology"),
    ("i apologize", "apology"),
    ("my bad", "apology"),
    ("forgive me", "apology"),
    ("i'm sorry about that", "apology"),
    ("my mistake", "apology"),
    ("i didn't mean that", "apology"),
    ("pardon me", "apology"),
    ("i take that back", "apology"),
    ("won't happen again", "apology"),
    ("please excuse me", "apology"),

    # ── Acknowledgement ────────────────────────────────────────────────────────
    ("ok", "acknowledge"),
    ("got it", "acknowledge"),
    ("understood", "acknowledge"),
    ("noted", "acknowledge"),
    ("alright", "acknowledge"),
    ("i see", "acknowledge"),
    ("roger that", "acknowledge"),
    ("copy that", "acknowledge"),
    ("makes sense", "acknowledge"),
    ("i hear you", "acknowledge"),
    ("fair enough", "acknowledge"),
    ("point taken", "acknowledge"),
    ("i'll keep that in mind", "acknowledge"),
    ("duly noted", "acknowledge"),

    # ── Positive ───────────────────────────────────────────────────────────────
    ("great job", "positive"),
    ("well done", "positive"),
    ("awesome", "positive"),
    ("amazing work", "positive"),
    ("fantastic", "positive"),
    ("love it", "positive"),
    ("nice", "positive"),
    ("excellent", "positive"),
    ("brilliant", "positive"),
    ("that's great", "positive"),
    ("impressive", "positive"),
    ("you crushed it", "positive"),
    ("outstanding", "positive"),
    ("superb", "positive"),
    ("you nailed it", "positive"),

    # ── Invitation ─────────────────────────────────────────────────────────────
    ("let's meet", "invite"),
    ("want to join", "invite"),
    ("come over", "invite"),
    ("are you free", "invite"),
    ("want to hang out", "invite"),
    ("let's catch up", "invite"),
    ("join us", "invite"),
    ("let's do this", "invite"),
    ("you should come", "invite"),
    ("we're getting together", "invite"),
    ("want to collaborate", "invite"),
    ("let's connect", "invite"),

    # ── Help Request ───────────────────────────────────────────────────────────
    ("can you help me", "help"),
    ("i need help", "help"),
    ("i'm stuck", "help"),
    ("can someone assist", "help"),
    ("having trouble with this", "help"),
    ("i need support", "help"),
    ("not sure what to do", "help"),
    ("could use some guidance", "help"),
    ("any suggestions", "help"),
    ("what would you recommend", "help"),

    # ── Confusion ──────────────────────────────────────────────────────────────
    ("i don't understand", "confused"),
    ("what do you mean", "confused"),
    ("that's confusing", "confused"),
    ("can you clarify", "confused"),
    ("i'm lost", "confused"),
    ("huh", "confused"),
    ("what", "confused"),
    ("this doesn't make sense", "confused"),
    ("could you rephrase that", "confused"),
    ("i'm not following", "confused"),
]

# ─── Smart Reply Templates ─────────────────────────────────────────────────────
# Maps each intent to a list of possible reply suggestions.
REPLY_TEMPLATES = {
    "greeting":     ["Hey! 👋", "Hello there!", "Hi! How's it going?"],
    "farewell":     ["See you later! 👋", "Bye! Take care!", "Talk soon!"],
    "agree":        ["Totally agree! 🙌", "Exactly my thoughts!", "100%!"],
    "disagree":     ["I see your point though 🤔", "Let's discuss further!", "Hmm, interesting take"],
    "question":     ["Great question!", "Let me check on that!", "Good point — I'll look into it"],
    "gratitude":    ["You're welcome! 😊", "Happy to help!", "No problem at all!"],
    "apology":      ["No worries! 😊", "It's okay!", "Don't worry about it!"],
    "acknowledge":  ["Sounds good!", "Got it! ✅", "Perfect, thanks!"],
    "positive":     ["Thanks! 😊", "Appreciate it! 🙏", "That means a lot!"],
    "invite":       ["Sounds fun! 🎉", "I'd love to!", "Count me in!"],
    "help":         ["Sure, I can help!", "Of course! What do you need?", "Happy to assist 🙌"],
    "confused":     ["Let me explain!", "Happy to clarify 😊", "Sure, let me break it down"],
}

# ─── Fallback suggestions (used when confidence is low) ───────────────────────
FALLBACK_SUGGESTIONS = ["👍", "Sounds good!", "Got it!", "Sure!", "Interesting!"]
