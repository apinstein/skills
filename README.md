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
npx ai-agent-skills install apinstein/skills/skills
npx ai-agent-skills install apinstein/skills/skills/pr-address-feedback # specific skil
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

## Antigravity Note

While `npx ai-agent-skills` can install for "Gemini", AntiGravity only looks for global skills in `~/.gemini/antigravity/skills/`. To get AntiGravity to see all Gemini global skills, do this:

```bash
npx ai-agent-skills install --gemini apinstein/skills/skills/pr-address-feedback
cd ~/.gemini/antigravity
ln -s ../skills ./ 
```
