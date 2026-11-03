# Presets

A preset is the per-person setup a router or agent starts from: the system prompt, the languages, which cloud models may be
tried and in what order, the profile and the memory blocks.

- Real presets live in `presets/` (next to this folder). That directory is in `.gitignore` and `tools/privacy_scan.sh` rejects
  any path under it, so a preset with a name, an address, a chat id or a key cannot be committed by accident.
- This folder holds only generic examples with placeholders. Copy one to `presets/<name>/` and fill it in there.
