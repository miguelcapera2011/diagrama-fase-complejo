import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.header("6.1 Máxima varianza en p = 0.5")

st.write("""
La varianza de la proporción es:  
**Var(p̂) = p(1-p)/n**  
Aquí tomamos n=1 para ver solo la forma de la función.
""")

p_vals = np.linspace(0, 1, 300)
var_vals = p_vals * (1 - p_vals)

fig, ax = plt.subplots()
ax.plot(p_vals, var_vals)
ax.set_xlabel("p")
ax.set_ylabel("Varianza")
ax.set_title("Varianza de p(1-p)")

st.pyplot(fig)

st.info("Se observa claramente que la varianza es máxima en p = 0.5.")
