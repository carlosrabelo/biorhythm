# Biorhythm

Calculadora de biorritmo que computa os ciclos físico, emocional e intelectual a partir de uma data de nascimento.

## Destaques

- Calcula os três ciclos do biorritmo: físico (23 dias), emocional (28 dias) e intelectual (33 dias)
- Aceita datas no formato AAAA-MM-DD (ISO 8601)
- Rejeita datas inválidas e datas de nascimento no futuro
- Retorna os valores como porcentagens entre -100 e +100
- Referência opcional `--as-of` para cálculos determinísticos
- Setup via Make com ruff, mypy e pytest
- Entry point instalável via `make install`

## Instalação

### Build from Source

```bash
git clone https://github.com/carlosrabelo/biorhythm.git
cd biorhythm
make setup
```

Instale em `~/.local/bin` (padrão), ou em todo o sistema em `/usr/local/bin` (sudo apenas para a cópia):

```bash
make install
make install-system
make uninstall    # removes from both common locations
```

## Uso

```bash
.venv/bin/python -m biorhythm.cli 2000-01-01 --as-of 2000-01-12
# Physical biorhythm     : 13.62
# Emotional biorhythm    : 62.35
# Intellectual biorhythm : 86.60
```

Omita `--as-of` para usar hoje como data de referência:

```bash
.venv/bin/python -m biorhythm.cli 2000-01-01
```

Ou após `make install`:

```bash
biorhythm 2000-01-01
biorhythm 2000-01-01 --as-of 2020-06-15
```

## Estrutura do Projeto

```
biorhythm/           # Source code package
    cli.py           # Entry point (CLI)
    processor.py     # Calculation logic
    errors.py        # Custom exceptions
tests/               # Test suite
.make/               # Automation scripts
pyproject.toml       # Metadata and dependencies
Makefile             # Orchestration
```

## Desenvolvimento

```bash
make setup           # Create .venv and install dependencies (first time only)
make test            # Run all tests
make quality         # Format, lint, and type-check
make install         # Install entry point to ~/.local/bin
make install-system  # Install entry point to /usr/local/bin
make uninstall       # Remove from both common locations
```

## Licença

Este projeto está licenciado sob a Licença MIT — veja [LICENSE](LICENSE) para detalhes.
