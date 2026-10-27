# Validation status — 10Eros v1.5

Passed locally:

- All six UI workflows and six API graphs select the v1.5 checkpoint and hybrid-v2 adapter.
- Graph links, model revisions, SHA256 metadata and storage budgets validate.
- Both precision variants install six correctly named workflows in an isolated installer test using tiny fixture weights. A second run performs no downloads, and installed workflow edits/files remain intact.
- Workflow regeneration is deterministic.
- Python compilation and shell syntax checks pass.
- The Runpod template dry run selects `ghcr.io/acdevmedia/eros-comfyui:1.5`, BF16 and Eros environment names.
- Current model, adapter, ComfyUI release, custom node heads, package releases and Actions release pins were checked against their upstream metadata.

The runtime uses ComfyUI v0.43.0 and its supported frontend 1.57.4. The torch/vision/audio family is 2.11.0/0.26.0/2.11.0 with CUDA 13.0: newer standalone torch releases do not have a matching released torchaudio family. The official Runpod base and its Python 3.12 interpreter are retained. This is a coordinated compatible target, not a claim that every component has the numerically highest available version.

Pending: GitHub Actions image build, dependency installation/`pip check`, CPU ComfyUI smoke checks against the upgraded runtime, and Runpod GPU inference. No local Docker build was performed. No model weights were downloaded during local verification.

The GPU check must cover both precision loaders, hybrid LoRA key mapping, SageAttention with the upgraded torch/CUDA stack, the six adapted workflows, final dimensions/duration and audio. Prior Sulphur performance measurements do not validate Eros. No Eros speed, VRAM, quality or audio synchronization claims are made before that run.
