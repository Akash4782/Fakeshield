from vanguard_diagnostic import ensemble_predict, load_vanguard_v85
import json

load_vanguard_v85()

ai_text = """
The intersection of economic policy and sustainable development is a critical area of study for modern governments. Furthermore, the implementation of carbon tax initiatives underscores the importance of fiscal responsibility in environmental management. Moreover, the integration of green technologies into industrial sectors provides a pathway for long-term growth. In conclusion, a coordinated approach between public and private sectors is essential for achieving climate targets. 
Furthermore, the emergence of smart grids and decentralized energy systems has revolutionized the way we consume and distribute power. These advancements not only enhance efficiency but also empower local communities to take control of their energy needs. Organizations must establish robust frameworks to ensure that the transition to a low-carbon economy is both inclusive and equitable. As we move forward, the synergy between technological innovation and policy reform will likely define the next era of environmental stewardship. This collaborative approach can lead to innovative solutions for complex global challenges, ranging from climate mitigation to sustainable urban planning. Ultimately, the successful deployment of green technologies depends on our ability to balance economic growth with environmental preservation.
"""

print("\n--- AI TEXT DEBUG (TITAN-v85.6) ---")
res = ensemble_predict(ai_text)
print(json.dumps({
    "overall_score": res["overall_score"],
    "verdict": res["verdict"],
    "signals": res["signals"]
}, indent=2))
