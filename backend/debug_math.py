
import numpy as np
avg_ppl = 46.1
score = float(1.0 / (1.0 + np.exp((avg_ppl - 43.5) / 6.0)))
print(f"PPL: {avg_ppl}, Score: {score}")
