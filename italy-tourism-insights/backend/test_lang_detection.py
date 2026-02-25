text = 'Buongiorno! Vorrei trovare un hotel a Roma'
text_lower = text.lower()

italian_words = ["che", "per", "una", "questo", "quale", "dove", "cosa", 
                "albergo", "ristorante", "visitare", "tour", "viaggiare",
                "vorrei", "posso", "ciao", "buongiorno", "buonasera", "grazie",
                "per favore", "arrivederci", "bellissimo", "meraviglioso"]

english_words = ["the", "and", "is", "are", "this", "that", "have", "been",
                "are", "hotel", "restaurant", "where", "what", "would", "can",
                "hello", "good morning", "thank you", "please", "goodbye",
                "beautiful", "wonderful", "amazing"]

italian_count = sum(1 for word in italian_words if word in text_lower)
english_count = sum(1 for word in english_words if word in text_lower)

print("Text:", text_lower)
print("Italian found:", [w for w in italian_words if w in text_lower])
print("English found:", [w for w in english_words if w in text_lower])
print("Italian count:", italian_count)
print("English count:", english_count)
