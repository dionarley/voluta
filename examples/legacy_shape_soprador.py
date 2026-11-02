import matplotlib.pyplot as plt
import numpy as np

# Parâmetros de projeto
R2 = 100   # Raio externo do rotor (mm)
K = 25     # Taxa de expansão da voluta (mm por radiano/volta)

# Ângulo theta variando de 0 a 1.5 voltas (3*pi radianos)
theta = np.linspace(0, 1.5 * 2 * np.pi, 1000)
R = R2 + K * (theta / (2 * np.pi))

# Conversão para coordenadas cartesianas
x = R * np.cos(theta)
y = R * np.sin(theta)

# Configuração do gráfico
plt.figure(figsize=(7, 7))
plt.plot(x, y, label='Perfil da Voluta (Espiral)', color='#1f77b4', linewidth=2.5)

# Representação do Rotor (Impeller) no centro
impeller = plt.Circle((0, 0), R2, color='#ff7f0e', alpha=0.4, label='Rotor ($D_2$)')
plt.gca().add_patch(impeller)

# Linhas de referência e eixos
plt.axhline(0, color='grey', linewidth=0.8, linestyle='--')
plt.axvline(0, color='grey', linewidth=0.8, linestyle='--')

plt.title('Traçado Geométrico da Voluta de um Soprador Centrífugo', fontsize=12, fontweight='bold')
plt.xlabel('Eixo X (mm)', fontsize=10)
plt.ylabel('Eixo Y (mm)', fontsize=10)
plt.grid(True, linestyle=':', alpha=0.6)
plt.axis('equal')
plt.legend(loc='upper right')

# Exibição do gráfico
plt.show()