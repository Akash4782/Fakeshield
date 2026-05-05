import json

dataset_path = "vanguard_adversarial_dataset.json"
with open(dataset_path, 'r') as f:
    data = json.load(f)

new_human_samples = [
    {
        "text": "The problem with virtual particles isn't that they don't 'exist' in a tangible sense, but that our mathematical scaffolding for them—perturbation theory—requires them as a bookkeeping device. In a non-perturbative regime, like deep inside a proton where the strong force is coupling everything into a chaotic soup, the very notion of a 'single' virtual gluon begins to lose its utility. We are left with a field that is doing everything at once, and our neat diagrams are just a human attempt to slice the infinite into digestible bites.",
        "label": "HUMAN",
        "topic": "Quantum Physics"
    },
    {
        "text": "Camus' Sisyphus is the ultimate hero of the mundane because he doesn't hope for the boulder to stay at the top. Hope, in the existentialist view, is a form of 'philosophical suicide'—a way to escape the crushing reality of the present by projecting meaning into an imaginary future. By embracing the struggle as sufficient in itself, Sisyphus negates the gods who punished him. His happiness is a quiet, spiteful rebellion against a universe that refuses to offer a 'why'.",
        "label": "HUMAN",
        "topic": "Philosophy"
    },
    {
        "text": "The discovery of the Denisovan tooth in a Siberian cave didn't just add a branch to our family tree; it set the whole tree on fire. We used to think of human evolution as a clean, sequential march out of Africa. Instead, we're finding a messy, 500,000-year-long cocktail party where Neanderthals, Denisovans, and Ghost populations were swapping genes across three continents. We aren't a pure lineage; we are a genomic mosaic of every cousin who survived long enough to leave a mark.",
        "label": "HUMAN",
        "topic": "Anthropology"
    },
    {
        "text": "The Tristan Chord at the beginning of Wagner's opera is famous because it refuses to resolve. It hangs there, suspended in a tonal purgatory, creating a physical sense of yearning in the listener. This isn't just clever music theory; it's a structural manifestation of the opera's theme: a love that can never be satisfied in the physical world. By the time the chord finally resolves hours later at the very end of the work, the audience has been psychologically primed for the release of death.",
        "label": "HUMAN",
        "topic": "Music Theory"
    },
    {
        "text": "Brutalism is often hated because it feels 'cold', but that was never the intention of architects like Le Corbusier or the Smithsons. For them, raw concrete—'béton brut'—was about honesty. It was a rejection of the superficial ornamentation of the Victorian era, which they saw as a mask for class inequality. A brutalist building doesn't lie to you about what it is; it shows its scars, its form-work, and its structural skeleton. It's a socialist architecture that values utility over vanity.",
        "label": "HUMAN",
        "topic": "Architecture"
    },
    {
        "text": "The 'hard problem' of consciousness remains hard because we are trying to use an objective tool—science—to measure a subjective state—qualia. You can map every neuron firing when I see a red apple, and you can even predict my behavior based on that firing, but you haven't explained the 'redness' of the red. There is a fundamental explanatory gap between 'matter in motion' and 'the feeling of being'. Until we bridge that, our neuroscience is just a very detailed map of a territory we don't actually understand.",
        "label": "HUMAN",
        "topic": "Neuroscience"
    },
    {
        "text": "Fermented foods aren't just a way to preserve calories; they are a form of 'outsourced digestion' that allowed early human populations to inhabit marginal environments. In the Levant, the transition from gathering wild grains to cultivating them was mediated by the crock and the pit. By domesticating microbes before we domesticated cattle, we essentially created a secondary, external gut that could break down toxins and synthesize vitamins that our own bodies couldn't handle on their own.",
        "label": "HUMAN",
        "topic": "Culinary History"
    },
    {
        "text": "Deep sea mining is currently a legal 'Wild West' because the International Seabed Authority is caught between two impossible mandates: protecting the marine environment and facilitating the extraction of 'the common heritage of mankind'. As we rush to mine polymetallic nodules for EV batteries, we risk destroying ecosystems that operate on geological timescales. A single plume of sediment from a robotic harvester can travel hundreds of miles, choking life in a benthic world that has remained undisturbed for millions of years.",
        "label": "HUMAN",
        "topic": "International Law"
    },
    {
        "text": "Chomsky's Universal Grammar is like a 'pre-installed operating system' for language, but the connectionists argue that we're just very good at pattern recognition. The problem for the connectionists is 'poverty of the stimulus'—how children learn complex recursive structures that they've never actually heard. A toddler doesn't need to be told the rules of a nested relative clause; they just 'know' them. This suggests that the human brain isn't just a blank slate, but a specialized machine for generating infinite meaning from finite sounds.",
        "label": "HUMAN",
        "topic": "Linguistics"
    },
    {
        "text": "The holographic principle suggests that the entire three-dimensional world we inhabit is just a projection of information stored on a distant, two-dimensional boundary. If this is true, then 'space' itself is an emergent property, much like the image on a TV screen emerges from the pixels. This isn't just stoner physics; it's a necessary conclusion if we want to reconcile general relativity with quantum mechanics. We are, quite literally, the shadows of a more fundamental reality.",
        "label": "HUMAN",
        "topic": "Physics"
    },
    {
        "text": "The necktie is perhaps the most absurd garment in the modern wardrobe: it has no thermal function, it's uncomfortable, and it's a literal noose. Yet, its semiotic power is immense. It signals an adherence to a specific corporate or diplomatic hierarchy, acting as a 'symbolic umbilical cord' that connects the wearer to the established order. To remove one's tie in a formal setting is an act of micro-rebellion, a way of saying that one's identity is no longer bound by the constraints of the institution.",
        "label": "HUMAN",
        "topic": "Sociology"
    },
    {
        "text": "Deep Ecology argues that the environmental crisis isn't a 'resource problem' but a 'perception problem'. We see the world as a collection of objects for our use rather than a web of relationships we belong to. In contrast, Eco-modernists believe that 'the way out is through'—using more technology, more nuclear power, and more urbanization to decouple human progress from nature. It's a debate between humility and hubris, between learning to live within limits and trying to engineer our way past them.",
        "label": "HUMAN",
        "topic": "Environmentalism"
    },
    {
        "text": "The 'resource curse' explains why countries with the most oil or diamonds often have the least democracy. When a government can fund itself by selling a commodity rather than taxing its citizens, it no longer needs their consent. The state becomes an 'extractive machine' that serves the elites and the multinational corporations, while the population is left with inflation, corruption, and a hollowed-out economy. Paradoxically, the most stable nations are often the ones that have to work the hardest for their wealth.",
        "label": "HUMAN",
        "topic": "Politics"
    },
    {
        "text": "In 1940s film noir, the 'male gaze' isn't just about looking at women; it's about the fear of being seen. The protagonist is usually a man who thinks he's in control, only to realize he's being manipulated by a woman who is smarter and more ruthless than he is. The heavy shadows and tilted camera angles reflect his psychological disorientation. He is trapped in a world where the 'truth' is always just out of frame, and his attempt to master the situation only leads him deeper into the trap.",
        "label": "HUMAN",
        "topic": "Cinema"
    },
    {
        "text": "The immersion vs engagement debate in VR is a struggle over the player's agency. Immersion is about 'being there'—the sensory trickery that makes you forget the headset. Engagement is about 'doing stuff'—the mechanical loops that keep you playing. High immersion without engagement is just a tech demo; high engagement without immersion is just a mobile game. The 'holy grail' of VR is a state where the physical presence and the mechanical will are perfectly aligned, creating a new kind of 'lived experience' in a digital world.",
        "label": "HUMAN",
        "topic": "Gaming"
    },
    {
        "text": "Post-modernism is often accused of 'relativism', but its core insight is that all 'Grand Narratives'—from Marxism to Science to Progress—are human constructions. Jean-François Lyotard defined it as 'incredulity toward metanarratives'. It doesn't mean that facts don't exist, but that the *meaning* we give those facts is always filtered through power and language. By deconstructing the stories we tell ourselves, we aren't losing the truth; we're just seeing the strings that move the puppets.",
        "label": "HUMAN",
        "topic": "Critical Theory"
    }
]

new_ai_samples = [
    {
        "text": "Zero-trust architecture is a security framework that requires all users, whether in or outside the organization's network, to be authenticated, authorized, and continuously validated for security configuration and posture before being granted or keeping access to applications and data. This approach assumes that there is no implicit trust granted to assets or user accounts based solely on their physical or network location. By implementing granular access controls and constant monitoring, organizations can significantly reduce the risk of data breaches and insider threats. As cyberattacks become more sophisticated, zero-trust is becoming an essential component of a modern cybersecurity strategy.",
        "label": "AI",
        "topic": "Cybersecurity"
    },
    {
        "text": "Edge AI refers to the deployment of artificial intelligence algorithms and models directly on local devices, such as smartphones, IoT sensors, and autonomous vehicles, rather than on a centralized cloud server. This allows for real-time data processing and decision-making with minimal latency, as the data does not need to travel to the cloud and back. Furthermore, edge AI can enhance privacy and security by keeping sensitive data on the device. As the number of connected devices continues to grow, edge AI will play a critical role in enabling more responsive and efficient intelligent systems across various industries, from healthcare to manufacturing.",
        "label": "AI",
        "topic": "Edge AI"
    },
    {
        "text": "A multi-cloud strategy involves the use of two or more cloud computing services from different providers. This approach allows organizations to avoid vendor lock-in, optimize costs, and leverage the unique strengths and features of different cloud platforms. By distributing workloads across multiple clouds, businesses can also improve their resilience and disaster recovery capabilities. However, managing a multi-cloud environment can be complex and requires specialized tools and expertise to ensure consistent security and performance. Despite these challenges, many organizations are adopting multi-cloud strategies to gain greater flexibility and agility in their digital transformation efforts.",
        "label": "AI",
        "topic": "Cloud Computing"
    },
    {
        "text": "Non-fungible tokens (NFTs) are unique digital assets that are stored on a blockchain, providing a secure and transparent way to verify ownership and authenticity. Unlike cryptocurrencies, which are fungible and can be exchanged for one another, NFTs represent a specific item or piece of content, such as digital art, music, or virtual real estate. This technology has the potential to revolutionize the way we create, share, and monetize digital content by giving creators more control over their work and enabling new forms of digital ownership. While the NFT market has seen significant volatility, the underlying technology continues to evolve and find new applications in various fields.",
        "label": "AI",
        "topic": "NFTs"
    },
    {
        "text": "5G technology is the fifth generation of mobile networks, offering significantly higher speeds, lower latency, and greater capacity than its predecessor, 4G. This advancement is expected to enable a wide range of new applications and services, such as autonomous vehicles, remote surgery, and immersive virtual reality experiences. By providing more reliable and responsive connectivity, 5G will also support the massive growth of the Internet of Things (IoT) and the development of smart cities. As 5G networks continue to roll out globally, they will drive innovation and economic growth by transforming the way we communicate, work, and interact with the world around us.",
        "label": "AI",
        "topic": "5G Technology"
    },
    {
        "text": "The choice between Lidar and camera-based sensors for autonomous vehicles is a subject of ongoing debate in the automotive industry. Lidar, which uses laser pulses to create a detailed 3D map of the environment, offers high precision and works well in various lighting conditions. However, it can be expensive and complex to integrate. Cameras, on the other hand, are more affordable and can capture a wealth of visual information, such as color and texture, which is essential for tasks like traffic sign recognition. Many companies are opting for a hybrid approach that combines both sensors to leverage their respective strengths and ensure a higher level of safety and reliability for self-driving cars.",
        "label": "AI",
        "topic": "Autonomous Vehicles"
    },
    {
        "text": "Smart home technology involves the use of internet-connected devices to automate and control various aspects of a household, such as lighting, heating, and security. While these systems offer greater convenience and energy efficiency, they also introduce new security challenges, as each connected device can potentially be a point of entry for cyberattacks. To protect their homes, users should focus on securing their home networks, using strong and unique passwords for all devices, and regularly updating their software. As the smart home market continues to grow, it is essential for both manufacturers and consumers to prioritize security to ensure that these technologies remain safe and reliable.",
        "label": "AI",
        "topic": "Smart Home"
    },
    {
        "text": "Hadoop and Spark are two of the most popular frameworks for processing large-scale data sets, each with its own unique strengths and use cases. Hadoop is a distributed storage and processing framework that is well-suited for batch processing of massive amounts of data. Spark, on the other hand, is an in-memory data processing engine that is designed for high-speed, real-time analytics and machine learning. While Hadoop is often more cost-effective for long-term storage and large-scale batch jobs, Spark offers significantly faster performance for interactive queries and streaming data. Many organizations use a combination of both frameworks to build more comprehensive and efficient big data pipelines.",
        "label": "AI",
        "topic": "Big Data"
    },
    {
        "text": "Virtual reality (VR) technology is increasingly being used to enhance workplace collaboration by providing immersive and interactive environments for remote teams. By using VR headsets, employees can meet in virtual offices, participate in shared training sessions, and collaborate on complex 3D projects as if they were in the same room. This can lead to greater engagement, better communication, and more effective problem-solving than traditional video conferencing. As VR technology becomes more affordable and accessible, we can expect to see more organizations adopting it as a key tool for managing distributed workforces and fostering a more connected and innovative work culture.",
        "label": "AI",
        "topic": "Virtual Reality"
    },
    {
        "text": "Recommendation engines are a type of AI algorithm that is used by e-commerce platforms to personalize the shopping experience for their customers. By analyzing user behavior, such as search history, past purchases, and product ratings, these systems can suggest items that a customer is likely to be interested in. This can lead to increased sales, higher customer satisfaction, and a more engaging user experience. As the amount of data available to e-commerce companies continues to grow, recommendation engines are becoming more sophisticated and accurate, using techniques like deep learning and collaborative filtering to provide more relevant and timely suggestions.",
        "label": "AI",
        "topic": "E-commerce"
    }
]

data["samples"].extend(new_human_samples)
data["samples"].extend(new_ai_samples)

with open(dataset_path, 'w') as f:
    json.dump(data, f, indent=2)

print(f"Dataset updated. Total samples: {len(data['samples'])}")
