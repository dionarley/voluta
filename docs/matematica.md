# Matemática

Esta página resume as equações implementadas no pacote `voluta`. O documento
original está disponível em
[Matemática dos Sopradores](assets/matematica-dos-sopradores.pdf).

## 1. Parâmetros globais

| Símbolo | Significado | Unidade |
| --- | --- | --- |
| \(Q\) | Vazão volumétrica | m³/s |
| \(\Delta P_t\) | Elevação de pressão total | Pa |
| \(N\) | Rotação | RPM |
| \(\rho\) | Massa específica do ar | kg/m³ |
| \(\eta\) | Eficiência global | – |

Ao nível do mar, adota-se normalmente \(\rho \approx 1{,}2\ \text{kg/m}^3\).

## 2. Triângulos de velocidade

A velocidade absoluta \(\vec{C}\) é a soma vetorial da velocidade periférica
\(\vec{U}\) com a velocidade relativa \(\vec{W}\):

\[
\vec{C} = \vec{U} + \vec{W}
\]

A velocidade periférica em um diâmetro \(D\) é:

\[
U = \frac{\pi D N}{60}
\]

com \(U\) em m/s, \(D\) em m e \(N\) em RPM.

Os ângulos principais são:

- \(\beta\): ângulo da pá, medido em relação à direção tangencial;
- \(\alpha\): ângulo absoluto do escoamento.

As componentes meridional e tangencial da velocidade absoluta são \(C_m\) e
\(C_u\). A componente meridional é a responsável pelo transporte de massa
através da área de fluxo.

## 3. Equação de Euler

A transferência teórica de energia por unidade de massa é:

\[
H_{th} = \frac{1}{g}\left(U_2 C_{u2} - U_1 C_{u1}\right)
\]

Multiplicando por \(\rho g\), obtém-se a elevação de pressão teórica:

\[
\Delta P_{th} = \rho \left(U_2 C_{u2} - U_1 C_{u1}\right)
\]

Para entrada radial sem pré-rotação, \(C_{u1} \approx 0\):

\[
\Delta P_{th} = \rho U_2 C_{u2}
\]

Em pás curvadas para trás, a componente tangencial na saída é reduzida:

\[
C_{u2} = U_2 - C_{m2}\cot\beta_2
\]

Por isso, pás curvadas para trás produzem menor elevação de pressão por estágio,
mas tendem a operar com melhor eficiência e maior estabilidade.

## 4. Dimensionamento do rotor

### Diâmetro de saída

O coeficiente adimensional de pressão \(\psi\) relaciona a elevação de pressão
com a velocidade periférica:

\[
U_2 = \sqrt{\frac{2\Delta P_t}{\rho\psi}}
\]

\[
D_2 = \frac{60 U_2}{\pi N}
\]

### Diâmetro de entrada

A entrada é dimensionada para limitar a velocidade meridional \(C_{1m}\),
tipicamente entre \(15\) e \(25\ \text{m/s}\):

\[
D_1 = \sqrt{\frac{4Q}{\pi C_{1m}}}
\]

### Largura das pás

A conservação de massa em uma seção de área \(A = \pi D b\) fornece:

\[
Q = \pi D_1 b_1 C_{1m} = \pi D_2 b_2 C_{2m}
\]

Logo:

\[
b = \frac{Q}{\pi D C_m}
\]

## 5. Voluta

A carcaça converte energia cinética em pressão estática. No modelo adotado, o
raio da voluta segue a espiral de Arquimedes:

\[
R(\theta) = R_2 + K\frac{\theta}{2\pi}
\]

onde:

- \(R_2\) é o raio externo do rotor;
- \(\theta\) é o ângulo polar medido a partir da língua da voluta;
- \(K\) é a taxa de expansão da voluta por volta.

O perfil cartesiano é obtido por:

\[
x(\theta) = R(\theta)\cos\theta, \qquad
y(\theta) = R(\theta)\sin\theta
\]

No exemplo original, \(R_2 = 100\ \text{mm}\), \(K = 25\ \text{mm/volta}\) e o
traçado cobre \(1{,}5\) voltas. A implementação está em
[`volute_radius`](api.md#voluta.geometry.volute_radius) e
[`volute_profile`](api.md#voluta.geometry.volute_profile).

!!! note "Interpretação de \(K\)"
    A constante \(K\) controla o crescimento da área da seção da voluta. Em um
    projeto real, ela é escolhida para manter a velocidade do escoamento
    aproximadamente constante (ou levemente decrescente) ao longo da carcaça,
    evitando perdas por atrito e separação.

## 6. Leis de afinidade

Para manter semelhança geométrica e dinâmica, ao alterar rotação e diâmetro:

| Grandeza | Relação com \(N\) | Relação com \(D\) |
| --- | --- | --- |
| Vazão | \(Q_2 = Q_1 (N_2/N_1)\) | \(Q_2 = Q_1 (D_2/D_1)^3\) |
| Pressão | \(\Delta P_2 = \Delta P_1 (N_2/N_1)^2\) | \(\Delta P_2 = \Delta P_1 (D_2/D_1)^2\) |
| Potência | \(P_2 = P_1 (N_2/N_1)^3\) | \(P_2 = P_1 (D_2/D_1)^5\) |

As duas relações podem ser combinadas:

\[
Q_2 = Q_1 \left(\frac{N_2}{N_1}\right)\left(\frac{D_2}{D_1}\right)^3
\]

\[
\Delta P_2 = \Delta P_1 \left(\frac{N_2}{N_1}\right)^2\left(\frac{D_2}{D_1}\right)^2
\]

\[
P_2 = P_1 \left(\frac{N_2}{N_1}\right)^3\left(\frac{D_2}{D_1}\right)^5
\]

## 7. Potência e eficiência

A potência hidráulica útil é \(Q\Delta P_t\). A potência mecânica no eixo
considera as perdas volumétricas, mecânicas e aerodinâmicas por meio da
eficiência global:

\[
P_{eixo} = \frac{Q\Delta P_t}{\eta}
\]

As perdas internas incluem atrito nas pás, choque na entrada quando o vetor
relativo não se alinha com o ângulo da pá e perdas na voluta e no difusor.
Em projetos reais, essas perdas são avaliadas com correlações empíricas e
ensaios.

## 8. Mapa entre equações e código

| Equação | Função Python |
| --- | --- |
| \(U = \pi D N / 60\) | [`peripheral_velocity`](api.md#voluta.aero.peripheral_velocity) |
| \(\Delta P_{th} = \rho(U_2C_{u2}-U_1C_{u1})\) | [`euler_pressure`](api.md#voluta.aero.euler_pressure) |
| \(U_2\) e \(D_2\) | [`outlet_diameter`](api.md#voluta.aero.outlet_diameter) |
| \(D_1\) | [`inlet_diameter`](api.md#voluta.aero.inlet_diameter) |
| \(b = Q/(\pi D C_m)\) | [`blade_width`](api.md#voluta.aero.blade_width) |
| \(P_{eixo} = Q\Delta P/\eta\) | [`shaft_power`](api.md#voluta.aero.shaft_power) |
| Leis de afinidade | [`affinity_flow`](api.md#voluta.aero.affinity_flow), [`affinity_pressure`](api.md#voluta.aero.affinity_pressure), [`affinity_power`](api.md#voluta.aero.affinity_power) |
| \(R(\theta) = R_2 + K\theta/2\pi\) | [`volute_radius`](api.md#voluta.geometry.volute_radius) |
