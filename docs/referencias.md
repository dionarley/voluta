# Referências

## Documento base

- **Matemática dos Sopradores** — conversa original que originou este projeto:
  [PDF](assets/matematica-dos-sopradores.pdf) ·
  [conversa no Gemini](https://gemini.google.com/app/23f85cae2b96e5cd)

O PDF reúne os parâmetros de entrada, os triângulos de velocidade, a equação de
Euler, o dimensionamento do rotor, a geometria da voluta, as leis de afinidade
e as perdas. O script e o SVG originais foram preservados em
`examples/legacy_shape_soprador.py` e `assets/voluta.svg`.

## Leitura sugerida

- Cengel, Y. A.; Cimbala, J. M. *Fluid Mechanics: Fundamentals and
  Applications*. McGraw-Hill.
- Fox, R. W.; McDonald, A. T.; Pritchard, P. J. *Introduction to Fluid
  Mechanics*. Wiley.
- Bleier, F. P. *Fan Handbook: Selection, Application, and Design*. McGraw-Hill.
- Eck, B. *Fans: Design and Operation of Centrifugal, Axial-Flow and
  Cross-Flow Fans*. Pergamon Press.
- Dixon, S. L.; Hall, C. A. *Fluid Mechanics and Thermodynamics of
  Turbomachinery*. Butterworth-Heinemann.
- ASHRAE. *ASHRAE Handbook — HVAC Systems and Equipment*, capítulos sobre
  ventiladores.

## Normas e boas práticas

- ISO 5801 — *Industrial fans: Performance testing using standardized
  airways*.
- AMCA 210 — *Laboratory Methods of Testing Fans for Certified Aerodynamic
  Performance Rating*.
- AMCA 300 — *Reverberant Room Method for Sound Testing of Fans*.

As referências servem como aprofundamento; o código implementa apenas o modelo
preliminar descrito na página [Matemática](matematica.md).
