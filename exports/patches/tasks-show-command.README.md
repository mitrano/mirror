# Patch: tasks show command

Este patch adiciona o comando:

```bash
uv run python -m memory tasks show <task_id>
```

Ele exibe os detalhes completos e amigáveis de uma tarefa: objetivo, ID, jornada, status, origem, etapa, prazo, horário, datas, contexto e metadados.

## Como testar antes de aplicar

```bash
git apply --check exports/patches/tasks-show-command.patch
```

## Como aplicar

```bash
git apply exports/patches/tasks-show-command.patch
```

## Arquivos incluídos

- `src/memory/cli/tasks_cmd.py`
- `src/memory/__main__.py`
- `tests/unit/memory/cli/test_tasks_cmd.py`
- `REFERENCE.md`
- `.pi/skills/mm-tasks/SKILL.md`
- `.claude/skills/mm:tasks/SKILL.md`
- `docs/manual-mirror-completo.md`
