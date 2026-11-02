# Como contribuir

## Preparação

```bash
uv sync
```

## Antes de abrir um pull request

```bash
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run mkdocs build --strict
```

Se a formatação falhar, aplique a correção automática:

```bash
uv run ruff format .
uv run ruff check --fix .
```

## Diretrizes

- Use unidades do SI na API e documente a unidade no nome do parâmetro quando
  houver ambiguidade (`flow_rate_m3_s`, `pressure_rise_pa`, `rpm`).
- Adicione testes para qualquer nova equação, com pelo menos um caso conhecido.
- Atualize a página [Matemática](docs/matematica.md) e a referência da API
  quando adicionar ou alterar uma equação.
- Mantenha as mensagens de erro em português e os identificadores em inglês,
  seguindo o padrão atual do código.
- Preserve os artefatos originais em `docs/assets/` e
  `examples/legacy_shape_soprador.py`.

## Commits

Sugestão de padrão:

```text
feat: adiciona cálculo de perdas na voluta
fix: corrige unidade do diâmetro de entrada
docs: detalha hipóteses da equação de Euler
test: cobre leis de afinidade com diâmetro
```

## Licença

Ao contribuir, você concorda que a contribuição será distribuída sob a licença
MIT deste repositório.
