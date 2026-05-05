"""
FakeShield AI Text Lab — Accuracy Benchmark v18.0
====================================================
Tests real Wikipedia text, real research paper excerpts, and AI-generated text.
Reports per-sample verdicts and overall accuracy.
"""

import sys
import os
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.new_forensic_engine import analyze_forensic as analyze

# ─────────────────────────────────────────────────────────────────────────────
# TEST CORPUS
# ─────────────────────────────────────────────────────────────────────────────

# GROUND TRUTH: HUMAN (Wikipedia excerpts — verbatim)
HUMAN_SAMPLES = [
    {
        "id": "wiki_photosynthesis",
        "source": "Wikipedia: Photosynthesis",
        "text": """Photosynthesis is a process used by plants and other organisms to convert
light energy into chemical energy that, through cellular respiration, can later
be released to fuel the organism's activities. Some of this chemical energy is
stored in carbohydrate molecules, such as sugars and starches, which are
synthesized from carbon dioxide and water – hence the name photosynthesis,
from the Greek phōs, "light", and synthesis, "putting together". In most cases,
oxygen is also released as a waste product. Most plants, algae, and
cyanobacteria perform photosynthesis; these organisms are called photoautotrophs.
Photosynthesis is largely responsible for producing and maintaining the oxygen
content of the Earth's atmosphere, and supplies most of the energy necessary
for life on Earth. Although photosynthesis is performed differently by different
species, the process always begins when energy from light is absorbed by proteins
called reaction centres that contain photosynthetic pigments. In plants, these
proteins are held inside organelles called chloroplasts, which are most abundant
in leaf cells, while in bacteria they are embedded in the plasma membrane.
In light-dependent reactions, some energy is used to strip electrons from
suitable substances, such as water, producing oxygen gas."""
    },
    {
        "id": "wiki_black_hole",
        "source": "Wikipedia: Black Hole",
        "text": """A black hole is a region of spacetime where gravity is so strong that nothing,
not even light or other electromagnetic waves, has enough speed to escape it.
The theory of general relativity predicts that a sufficiently compact mass can
deform spacetime to form a black hole. The boundary of no escape is called the
event horizon. A black hole has a great effect on the fate and circumstances of
an object crossing it, but it has no locally detectable features according to
general relativity. In many ways, a black hole acts like an ideal black body,
as it reflects no light. Moreover, quantum field theory in curved spacetime
predicts that event horizons emit Hawking radiation, with the same spectrum as
a black body of a temperature inversely proportional to its mass. This temperature
is of the order of billionths of a kelvin for stellar black holes, making it
essentially impossible to observe directly. Objects whose gravitational fields are
too strong for light to escape were first considered in the 18th century by
John Michell and Pierre-Simon Laplace. The first modern solution of general
relativity that would characterize a black hole was found by Karl Schwarzschild
in 1916, although its interpretation as a region of space from which nothing can
escape was not fully appreciated for decades."""
    },
    {
        "id": "research_bert",
        "source": "Research Paper: BERT (Devlin et al., 2018) — Abstract",
        "text": """We introduce a new language representation model called BERT, which stands for
Bidirectional Encoder Representations from Transformers. Unlike recent language
representation models (Peters et al., 2018a; Radford et al., 2018), BERT is
designed to pre-train deep bidirectional representations from unlabeled text by
jointly conditioning on both left and right context in all layers. As a result,
the pre-trained BERT model can be fine-tuned with just one additional output layer
to create state-of-the-art models for a wide range of tasks, such as question
answering and language inference, without substantial task-specific architecture
modifications. BERT is conceptually simple and empirically powerful. It obtains
new state-of-the-art results on eleven natural language processing tasks, including
pushing the GLUE score to 80.5% (7.7% point absolute improvement), MultiNLI
accuracy to 86.7% (4.6% absolute improvement), SQuAD v1.1 question answering
Test F1 to 93.2 (1.5 point absolute improvement) and SQuAD v2.0 Test F1 to 83.1
(5.1 point absolute improvement)."""
    },
    {
        "id": "research_attention",
        "source": "Research Paper: Attention Is All You Need (Vaswani et al., 2017)",
        "text": """The dominant sequence transduction models are based on complex recurrent or
convolutional neural networks that include an encoder and a decoder. The best
performing models also connect the encoder and decoder through an attention
mechanism. We propose a new simple network architecture, the Transformer, based
solely on attention mechanisms, dispensing with recurrence and convolutions
entirely. Experiments on two machine translation tasks show these models to be
superior in quality while being more parallelizable and requiring significantly
less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German
translation task, improving over the existing best results, including ensembles,
by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model
establishes a new single-model state-of-the-art BLEU score of 41.0 after training
for 3.5 days on eight GPUs, a small fraction of the training costs of the best
models from the literature. We show that the Transformer generalizes well to other
tasks by applying it successfully to English constituency parsing both with large
and limited training data."""
    },
    {
        "id": "personal_narrative",
        "source": "Personal Blog Post / Human Writing",
        "text": """I still remember the first time I saw a neural network learn something on its own.
I was a second-year PhD student, exhausted from weeks of debugging code that
wouldn't converge, when suddenly the loss curve started dropping. Not dramatically —
just a quiet, steady decline over three hundred epochs. I watched it for twenty
minutes without moving. My coffee went cold. My advisor knocked on my office door
and I didn't even look up. What I was watching felt like witnessing something alive.
That feeling has never entirely left me, even after years of working with models
far larger and more capable. There's something deeply strange about teaching a
machine to recognize patterns. You write the math, you set the hyperparameters,
you curate the data — and then you step back and let it figure something out that
you haven't explicitly told it. It reminds me of gardening, in a way. You prepare
the soil, you water consistently, and then at some point the thing grows on its own,
following rules you helped set but don't fully control. My grandmother used to say
that the best gardeners know when to stop interfering. I think about that a lot."""
    },
]

# GROUND TRUTH: AI GENERATED (Clearly written by AI — ChatGPT / Gemini style)
AI_SAMPLES = [
    {
        "id": "ai_climate_change",
        "source": "AI Generated: Climate Change Explainer (ChatGPT-style)",
        "text": """Climate change is one of the most pressing challenges facing humanity in the 21st century.
At its core, it refers to long-term shifts in global temperatures and weather patterns,
primarily driven by human activities such as the burning of fossil fuels, deforestation,
and industrial processes. It is worth noting that the consequences of climate change are
multifaceted and far-reaching, affecting ecosystems, economies, and human health on a
global scale. Furthermore, the scientific consensus is clear: the Earth's average
temperature has increased by approximately 1.1 degrees Celsius since the pre-industrial
era, and without significant intervention, this warming is projected to continue.
To address this challenge, a multifaceted approach is required. This includes transitioning
to renewable energy sources such as solar and wind power, improving energy efficiency across
all sectors, and implementing carbon pricing mechanisms to incentivize emission reductions.
Moreover, international cooperation is essential, as climate change is inherently a global
problem that transcends national borders. In conclusion, addressing climate change requires
not only technological innovation but also fundamental shifts in our economic systems and
individual behaviors. The decisions we make in the coming decades will determine the
trajectory of our planet for centuries to come."""
    },
    {
        "id": "ai_machine_learning",
        "source": "AI Generated: Machine Learning Tutorial (Gemini-style)",
        "text": """Machine learning (ML) is a transformative subset of artificial intelligence that enables
systems to learn and improve from experience without being explicitly programmed. In this
comprehensive overview, we will explore the fundamental concepts, key algorithms, and
practical applications of machine learning in today's data-driven world.
At its core, machine learning leverages statistical techniques to identify patterns within
large datasets, enabling systems to make predictions or decisions with minimal human
intervention. The field is broadly categorized into three paradigms: supervised learning,
unsupervised learning, and reinforcement learning. Supervised learning involves training
a model on labeled data, where the desired output is known. Unsupervised learning, on the
other hand, deals with unlabeled data and seeks to discover hidden patterns or structures.
Reinforcement learning is inspired by behavioral psychology, where an agent learns to make
decisions by interacting with an environment and receiving feedback in the form of rewards
or penalties. Furthermore, deep learning, a specialized subset of machine learning, has
revolutionized the field by enabling the training of neural networks with many layers.
These deep neural networks have achieved remarkable success in domains such as computer
vision, natural language processing, and speech recognition. It is important to understand
that the success of any machine learning model depends heavily on the quality and quantity
of training data, as well as careful feature engineering and model selection."""
    },
    {
        "id": "ai_history_essay",
        "source": "AI Generated: History Essay (Claude-style)",
        "text": """The Industrial Revolution, which began in Britain in the late 18th century and spread
throughout the world during the 19th century, represents one of the most significant
transformations in human history. This period of rapid industrialization fundamentally
altered virtually every aspect of daily life, from the way goods were produced to how
people worked, lived, and interacted with one another. It is worth noting that the
revolution did not occur in isolation but was the culmination of several interconnected
developments, including advances in agricultural productivity, the availability of
coal and iron, and a series of crucial technological innovations. The invention of
the steam engine, often credited to James Watt, was perhaps the most pivotal of these
innovations. By harnessing the power of steam, manufacturers could power machinery
at a scale and speed previously unimaginable. This led to the establishment of large
factories, which replaced the cottage industries and artisan workshops that had
characterized pre-industrial production. Furthermore, the development of an extensive
railway network facilitated the rapid movement of goods and people, connecting previously
isolated communities and creating new markets. The consequences of industrialization
were profound and complex. On one hand, it led to unprecedented economic growth and
raised living standards for many. On the other hand, it also gave rise to significant
social problems, including the exploitation of child labor and dangerous working conditions."""
    },
    {
        "id": "ai_quantum_computing",
        "source": "AI Generated: Technical Explainer (GPT-4 style)",
        "text": """Quantum computing represents a paradigm shift in computational power, leveraging the
principles of quantum mechanics to process information in fundamentally different ways
than classical computers. Unlike classical bits, which represent information as either
0 or 1, quantum bits, or qubits, can exist in a superposition of both states simultaneously.
This property, along with quantum entanglement and interference, allows quantum computers
to explore multiple computational paths at once, offering exponential speedup for certain
types of problems. The potential applications of quantum computing are vast and
transformative. In the realm of cryptography, quantum computers could break many of the
encryption schemes that currently secure our digital communications. Consequently, there
is significant research underway in post-quantum cryptography to develop algorithms that
are resistant to quantum attacks. Furthermore, in drug discovery and materials science,
quantum simulation could model molecular interactions with unprecedented accuracy, accelerating
the development of new medicines and materials. It is important to note that practical,
fault-tolerant quantum computers remain a significant engineering challenge. Current quantum
systems are noisy and error-prone, limiting the depth of circuits that can be reliably
executed. Nonetheless, the field is advancing rapidly, with companies like IBM, Google,
and various well-funded startups achieving notable milestones in qubit counts and error rates."""
    },
]

# ─────────────────────────────────────────────────────────────────────────────
# RUN BENCHMARK
# ─────────────────────────────────────────────────────────────────────────────

def run_benchmark():
    print("\n" + "="*70)
    print("  FAKESHIELD AI TEXT LAB — ACCURACY BENCHMARK v18.0")
    print("="*70)
    print(f"  Testing {len(HUMAN_SAMPLES)} Human Samples + {len(AI_SAMPLES)} AI Samples")
    print("="*70 + "\n")

    results = []

    # --- Human Samples ---
    print("▶  HUMAN TEXT SAMPLES (Expected: AUTHENTIC / LIKELY HUMAN)\n")
    human_correct = 0
    for sample in HUMAN_SAMPLES:
        r = analyze(sample["text"], mode="deep")
        score = r["score"] * 100
        verdict = r["verdict"]
        is_correct = score <= 50  # Score ≤ 50% = correctly identified as human
        human_correct += int(is_correct)
        icon = "✅" if is_correct else "❌"
        print(f"  {icon} [{sample['id']}]")
        print(f"     Source  : {sample['source']}")
        print(f"     Score   : {score:.1f}% AI | Verdict: {verdict}")
        
        # Show key signals
        sigs = r.get("signals", {})
        if sigs:
            print(f"     Signals : Neural={sigs.get('classifier_signal',0):.2f} | "
                  f"Bino={sigs.get('binoculars_signal',0):.2f} | "
                  f"Shield={sigs.get('human_shield',0):.2f} | "
                  f"PPL={sigs.get('ppl_signal',0):.2f}")
        print()

    # --- AI Samples ---
    print("▶  AI TEXT SAMPLES (Expected: AI GENERATED / LIKELY AI)\n")
    ai_correct = 0
    for sample in AI_SAMPLES:
        r = analyze(sample["text"], mode="deep")
        score = r["score"] * 100
        verdict = r["verdict"]
        is_correct = score >= 60  # Score ≥ 60% = correctly identified as AI
        ai_correct += int(is_correct)
        icon = "✅" if is_correct else "❌"
        print(f"  {icon} [{sample['id']}]")
        print(f"     Source  : {sample['source']}")
        print(f"     Score   : {score:.1f}% AI | Verdict: {verdict}")
        sigs = r.get("signals", {})
        if sigs:
            print(f"     Signals : Neural={sigs.get('classifier_signal',0):.2f} | "
                  f"Bino={sigs.get('binoculars_signal',0):.2f} | "
                  f"Shield={sigs.get('human_shield',0):.2f} | "
                  f"PPL={sigs.get('ppl_signal',0):.2f}")
        print()

    # --- Summary ---
    total_h = len(HUMAN_SAMPLES)
    total_a = len(AI_SAMPLES)
    total   = total_h + total_a
    correct = human_correct + ai_correct

    h_acc = (human_correct / total_h) * 100
    a_acc = (ai_correct / total_a) * 100
    overall = (correct / total) * 100

    print("="*70)
    print("  BENCHMARK RESULTS")
    print("="*70)
    print(f"  Human Text Accuracy  : {human_correct}/{total_h} → {h_acc:.0f}%")
    print(f"  AI Text Accuracy     : {ai_correct}/{total_a} → {a_acc:.0f}%")
    print(f"  OVERALL ACCURACY     : {correct}/{total} → {overall:.0f}%")
    print("="*70)

    if overall >= 80:
        print("  🎯 RESULT: EXCELLENT — System performing at industry-standard level!")
    elif overall >= 65:
        print("  ⚠️  RESULT: GOOD — Some improvement needed in specific categories.")
    else:
        print("  ❌ RESULT: NEEDS WORK — Significant calibration required.")
    print("="*70 + "\n")


if __name__ == "__main__":
    run_benchmark()
