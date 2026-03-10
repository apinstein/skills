# 🛠️ Agent Skills

A portable library of [Agent Skills](https://agentskills.io) for AI coding agents.

## Skills

| Skill | Description |
|-------|-------------|
| [pr-address-feedback](skills/pr-address-feedback/) | Read all review feedback on a GitHub PR (with Reviewable.io) and systematically address each thread |

## Installation

### Manual
```bash
cp -r skills/<skill-name> /path/to/your/project/.agent/skills/
```

### Via npx (Ai-Agent-Skills)
```bash
npx ai-agent-skills install apinstein/skills
npx ai-agent-skills install apinstein/skills/pr-address-feedback # specific skil
```

## Structure

Each skill follows the [Agent Skills open standard](https://agentskills.io/specification):

```
skills/<name>/
├── SKILL.md          # Instructions + metadata
├── scripts/          # Optional helper scripts
└── references/       # Optional documentation
```

## License

MIT
