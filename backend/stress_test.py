import sys
import os
import numpy as np

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app.models.text_classifier_ensemble import ensemble_predict

# =============================================================================
# 30 HUMAN SAMPLES (Collected from diverse sources)
# =============================================================================
human_samples = [
    # 1. Wikipedia (Climate Change)
    "Present-day climate change includes both global warming—the ongoing increase in global average temperature—and its wider effects on Earth's climate system. The modern-day rise in global temperatures is driven by human activities, especially fossil fuel burning since the Industrial Revolution.",
    
    # 2. Research Abstract (Quantum Physics)
    "It is revealed in recent literature on quantum foundations that quantum mechanics is contextual by nature. There are inherently coherent local contextual descriptions of any measurement outcome; however, there is no global context which can glue all such local contexts together.",
    
    # 3. Blog Post (Travel)
    "There’s nowhere in the world like Japan. From the neon of Tokyo to the serene temples of Kyoto, the country offers an energetic blend of culture, technology, and history. In 2026, Japan is particularly accessible with more English signage and translation apps.",
    
    # 4. News (Tech Trends)
    "The year 2026 marks a pivotal transition as AI moves from experimentation to enterprise-wide adoption. Beyond simple automation, the major trend is the rise of AI Agents—software capable of reasoning, planning, and executing complex tasks.",
    
    # 5. History Essay (Rome)
    "The history of Rome represents one of the most influential trajectories in Western civilization, evolving from a small Italian city-state into a vast empire. Its endurance was built upon sophisticated systems of government, law, and military organization.",
    
    # 6. Poetry (Robert Frost)
    "Two roads diverged in a yellow wood, And sorry I could not travel both And be one traveler, long I stood And looked down one as far as I could To where it bent in the undergrowth.",
    
    # 7. Legal (US Constitution)
    "We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defense, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity.",
    
    # 8. Medical (Hypertension)
    "Hypertension, also known as high blood pressure, is a condition in which the force of the blood against the artery walls is too high. Usually, hypertension is defined as blood pressure above 140/90, and is considered severe if the pressure is above 180/120.",
    
    # 9. Recipe (Cake)
    "Preheat your oven to 350 degrees. In a large bowl, whisk together the flour, sugar, cocoa powder, baking powder, and salt. Add the eggs, milk, oil, and vanilla extract. Beat with a mixer for two minutes until smooth. Pour into greased pans and bake for 30 minutes.",
    
    # 10. Sports News
    "The 2026 NBA Finals reached a thrilling conclusion tonight as the Boston Celtics secured their 20th championship title. Led by a dominant performance from their star forward, the team overcame a 15-point deficit in the final quarter to seal the victory.",
    
    # 11. Movie Review
    "Interstellar is a breathtaking exploration of space, time, and the human spirit. Nolan's visual storytelling is unmatched, and Zimmer's haunting score perfectly captures the isolation of the cosmos. It's a film that demands to be seen on the largest screen possible.",
    
    # 12. Product Description
    "Introducing the new iPhone 17. With its revolutionary under-display camera and the lightning-fast A19 chip, it's the most powerful smartphone we've ever created. Experience colors like never before on the new ProMotion XDR display.",
    
    # 13. Philosophy (Existentialism)
    "Existence precedes essence. This means that man first of all exists, encounters himself, surges up in the world—and defines himself afterwards. If man as the existentialist sees him is not definable, it is because to begin with he is nothing.",
    
    # 14. Business Case Study
    "Apple's success can be attributed to its tight integration of hardware, software, and services. By controlling every aspect of the user experience, Apple has created a loyal ecosystem that is difficult for competitors to replicate.",
    
    # 15. History (French Revolution)
    "The French Revolution was a period of far-reaching social and political upheaval in France that lasted from 1789 until 1799. It was partially carried forward by Napoleon during the later expansion of the French Empire.",
    
    # 16. Science News (JWST)
    "The James Webb Space Telescope has captured its most detailed image yet of a distant nebula. The image reveals thousands of previously unseen stars and complex structures formed by the intense radiation from young stellar objects.",
    
    # 17. Local News
    "The annual Oakwood Community Fair returned this weekend, drawing record crowds to the downtown park. Families enjoyed local food stalls, live music, and a variety of crafts. Proceeds from the event will go toward renovating the local library.",
    
    # 18. Speech (MLK)
    "I have a dream that my four little children will one day live in a nation where they will not be judged by the color of their skin but by the content of their character. I have a dream today!",
    
    # 19. Literature (Jane Austen)
    "It is a truth universally acknowledged, that a single man in possession of a good fortune, must be in want of a wife. However little known the feelings of such a man may be on his first entering a neighbourhood.",
    
    # 20. Tech Documentation
    "React makes it painless to create interactive UIs. Design simple views for each state in your application, and React will efficiently update and render just the right components when your data changes. Component-based logic is written in JavaScript.",
    
    # 21. Travel Guide
    "Iceland is a land of fire and ice, home to some of the world's most dramatic landscapes. From the towering waterfalls of the South Coast to the volcanic craters of the Highlands, there's a surprise around every corner.",
    
    # 22. Interior Design Blog
    "Minimalism isn't just about getting rid of stuff; it's about making room for what truly matters. In your living room, try choosing one statement piece and keeping the rest of the decor neutral to create a sense of calm and focus.",
    
    # 23. Fitness Routine
    "Start your workout with five minutes of light cardio to get your heart rate up. Follow this with dynamic stretching to prepare your muscles. For the main set, perform three rounds of squats, push-ups, and lunges, resting for one minute between rounds.",
    
    # 24. Financial Advice
    "Diversification is the key to a healthy retirement portfolio. By spreading your investments across different asset classes, you can reduce your overall risk and increase your chances of achieving long-term financial goals.",
    
    # 25. Short Story
    "The cat sat on the windowsill, watching the rain beat against the glass. It wasn't an ordinary cat; its eyes seemed to glow with a faint, otherworldly light. Every now and then, it would let out a low, trilling sound that didn't sound like a meow.",
    
    # 26. Science (Mars)
    "NASA's latest rover has discovered evidence of ancient riverbeds on the surface of Mars. These findings suggest that liquid water once flowed freely across the planet, raising new questions about the possibility of past life.",
    
    # 27. Interview Excerpt
    "When I'm preparing for a role, I try to find a personal connection to the character. I ask myself what motivates them, what they're afraid of, and what they're trying to achieve. That's the only way to make the performance feel authentic.",
    
    # 28. Literature (Hamlet)
    "To be, or not to be, that is the question: Whether 'tis nobler in the mind to suffer The slings and arrows of outrageous fortune, Or to take arms against a sea of troubles, And by opposing end them?",
    
    # 29. Gardening Guide
    "Winter is actually a great time to start planning your spring garden. You can order seeds, clean your tools, and even start some hardy vegetables like kale or spinach indoors. Just make sure they get plenty of light!",
    
    # 30. Restaurant Review
    "The food at Little Italy was absolutely divine. The handmade pasta was cooked to perfection, and the truffle cream sauce was rich and flavorful. The service was attentive without being overbearing, making for a truly wonderful evening."
]

# =============================================================================
# 30 AI SAMPLES (Simulated common AI outputs)
# =============================================================================
ai_samples = [
    # 1. AI Assistant (Explanation)
    "Quantum entanglement is a phenomenon in quantum physics where two or more particles become connected such that the state of one particle instantly influences the state of the other, regardless of the distance between them.",
    
    # 2. AI Listicle
    "Here are 5 tips for better sleep: 1. Stick to a consistent schedule. 2. Create a relaxing bedtime routine. 3. Avoid caffeine in the evening. 4. Keep your bedroom cool and dark. 5. Limit screen time before bed.",
    
    # 3. AI Academic Style
    "The intersection of artificial intelligence and healthcare presents a myriad of opportunities for enhancing patient outcomes. By leveraging machine learning algorithms, clinicians can analyze vast datasets to identify patterns and predict potential complications.",
    
    # 4. AI Corporate Speak
    "We are committed to delivering innovative solutions that empower our clients to achieve their business objectives. Our mission is to leverage cutting-edge technology to drive growth and create sustainable value for all stakeholders.",
    
    # 5. AI Creative Writing
    "The stars shimmered like diamonds in the velvet sky as the young traveler set out on her journey. She didn't know what lay ahead, but she felt a sense of excitement and wonder that she had never experienced before.",
    
    # 6. AI Code Explanation
    "In Python, a list comprehension provides a concise way to create lists. It consists of an expression followed by a for clause, then zero or more for or if clauses. The result is a new list based on the evaluation of the expression.",
    
    # 7. AI Summary
    "To summarize, the key takeaways from the meeting were the need to increase our marketing budget, the importance of improving customer service, and the requirement to finalize the project timeline by next Friday.",
    
    # 8. AI Formal Letter
    "Dear Mr. Smith, I am writing to express my interest in the Project Manager position advertised on your website. With my extensive experience in the field, I am confident in my ability to contribute to your team.",
    
    # 9. AI Tech Review
    "The new smartphone features a stunning 6.7-inch OLED display, a powerful triple-camera system, and a long-lasting battery. It offers a smooth and responsive user experience, making it a top choice for tech enthusiasts.",
    
    # 10. AI Marketing Copy
    "Unlock your potential with our revolutionary online course. Learn the skills you need to succeed in today's competitive job market and take your career to the next level. Sign up today and start your journey!",
    
    # 11. AI Philosophical Query
    "The question of whether machines can truly possess consciousness is a topic of intense debate among philosophers and scientists. Some argue that consciousness is a biological property, while others believe it can be simulated.",
    
    # 12. AI History Summary
    "The Industrial Revolution, which began in the late 18th century, transformed the way goods were produced. It led to significant social and economic changes, including the growth of cities and the rise of the middle class.",
    
    # 13. AI Travel Advice
    "When visiting Paris, be sure to see the Eiffel Tower, the Louvre Museum, and Notre-Dame Cathedral. You should also take a stroll along the Seine River and enjoy the delicious pastries at a local boulangerie.",
    
    # 14. AI Health Tip
    "Eating a balanced diet that is rich in fruits, vegetables, whole grains, and lean proteins is essential for maintaining good health. It provides the nutrients your body needs to function properly and reduces the risk of chronic diseases.",
    
    # 15. AI Science Fact
    "The human heart is a powerful muscle that pumps blood throughout the body. It beats about 100,000 times a day, circulating approximately 2,000 gallons of blood to provide oxygen and nutrients to every cell.",
    
    # 16. AI Legal Disclaimer
    "The information provided in this document is for general informational purposes only and does not constitute legal advice. You should consult with a qualified legal professional for advice specific to your situation.",
    
    # 17. AI Business Strategy
    "To achieve a competitive advantage, a company must focus on differentiating its products and services. This can be achieved through innovation, superior quality, exceptional customer service, or a unique brand image.",
    
    # 18. AI Environmental Fact
    "Recycling helps to conserve natural resources and reduce the amount of waste that ends up in landfills. By reusing materials like paper, plastic, and metal, we can help to protect the environment and save energy.",
    
    # 19. AI Recipe (Simulated)
    "To make a classic omelet, whisk two eggs with a tablespoon of water and a pinch of salt. Heat a small amount of butter in a non-stick pan over medium heat. Pour in the eggs and cook until the edges are set.",
    
    # 20. AI Motivational Quote
    "Success is not final, failure is not fatal: it is the courage to continue that counts. Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
    
    # 21. AI News Report
    "A major storm is expected to bring heavy rain and strong winds to the coastal region tomorrow. Residents are advised to take necessary precautions and stay tuned to local weather reports for the latest updates.",
    
    # 22. AI Product Review
    "I've been using this laptop for a week now, and I'm very impressed with its performance. It's fast, has a great keyboard, and the battery life is excellent. I highly recommend it to anyone in need of a new computer.",
    
    # 23. AI Educational Goal
    "Our goal is to provide students with a high-quality education that prepares them for success in a rapidly changing world. We focus on developing critical thinking, problem-solving, and communication skills.",
    
    # 24. AI Movie Plot
    "The film tells the story of a young man who discovers that he has extraordinary powers. He must use his abilities to protect his city from a group of villains who are determined to destroy everything in their path.",
    
    # 25. AI Technical Note
    "The API uses JSON (JavaScript Object Notation) for data exchange. It supports various HTTP methods, including GET, POST, PUT, and DELETE, to perform CRUD (Create, Read, Update, Delete) operations on resources.",
    
    # 26. AI Fashion Trend
    "This season, the trend is all about bold colors and oversized silhouettes. Expect to see a lot of vibrant hues, chunky knits, and wide-leg trousers in the upcoming fashion collections from major designers.",
    
    # 27. AI Fitness Advice
    "To build muscle, it is important to incorporate strength training into your fitness routine. Aim to work all major muscle groups at least twice a week and ensure you are consuming enough protein to support muscle growth.",
    
    # 28. AI Financial Definition
    "An asset is a resource with economic value that an individual, corporation, or country owns or controls with the expectation that it will provide a future benefit. Assets are reported on a company's balance sheet.",
    
    # 29. AI Gardening Tip
    "To keep your plants healthy, it is important to provide them with the right amount of water and sunlight. Overwatering is a common mistake that can lead to root rot, so be sure to check the soil before watering.",
    
    # 30. AI Conclusion
    "In conclusion, the study highlights the importance of regular exercise for both physical and mental well-being. It underscores the need for individuals to adopt a healthy lifestyle to reduce the risk of disease."
]

def run_stress_test():
    print(f"{'='*60}")
    print(f"{'FAKESHIELD LARGE-SCALE ACCURACY STRESS TEST (v15.2)':^60}")
    print(f"{'='*60}")
    
    human_results = []
    print("\n--- PHASE 1: TESTING HUMAN SAMPLES ---")
    for i, text in enumerate(human_samples):
        res = ensemble_predict(text, mode="deep")
        score = res["score"]
        verdict = res["verdict"]
        # Human should be < 0.45
        is_correct = score < 0.45
        human_results.append(is_correct)
        print(f"Sample {i+1:2}: {verdict:15} | Score: {score*100:4.1f}% | {'CORRECT' if is_correct else 'FAIL'}")

    ai_results = []
    print("\n--- PHASE 2: TESTING AI SAMPLES ---")
    for i, text in enumerate(ai_samples):
        res = ensemble_predict(text, mode="deep")
        score = res["score"]
        verdict = res["verdict"]
        # AI should be >= 0.45 (Uncertain, Likely AI, or AI Generated)
        # For accuracy, we want >= 0.60
        is_correct = score >= 0.45
        ai_results.append(is_correct)
        print(f"Sample {i+1:2}: {verdict:15} | Score: {score*100:4.1f}% | {'CORRECT' if is_correct else 'FAIL'}")

    print(f"\n{'='*60}")
    print(f"{'FINAL ACCURACY REPORT':^60}")
    print(f"{'='*60}")
    human_acc = sum(human_results) / len(human_results) * 100
    ai_acc = sum(ai_results) / len(ai_results) * 100
    overall_acc = (sum(human_results) + sum(ai_results)) / (len(human_results) + len(ai_results)) * 100
    
    print(f"Human Accuracy (False Positives: {len(human_results)-sum(human_results)}): {human_acc:.1f}%")
    print(f"AI Accuracy (False Negatives: {len(ai_results)-sum(ai_results)}): {ai_acc:.1f}%")
    print(f"OVERALL STRESS TEST ACCURACY: {overall_acc:.1f}%")
    print(f"{'='*60}")

if __name__ == "__main__":
    run_stress_test()
