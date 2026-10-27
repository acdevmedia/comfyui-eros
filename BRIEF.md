# Eros bundle maintenance brief

Build the Runpod ComfyUI bundle for `acdevmedia/comfyui-eros`, publishing `ghcr.io/acdevmedia/eros-comfyui:1.5` and immutable commit tags through GitHub Actions. Do not build Docker images locally.

Use 10Eros v1.5 with the author's recommended DMD hybrid-v2 adapter and sigma schedules. BF16 is the default creator checkpoint; the optional independent experimental FP8 conversion must be identified clearly. Preserve the six shot-control workflows, audio conditioning, automatic CPU quota sizing, resumable downloads and SHA256 verification.

All current version assets live under `versions/1.5/`. Pin current compatible dependencies and model revisions. The official base supplies Python 3.12; the matched torch/audio/vision family uses CUDA 12.8. Do not equate a newer standalone package version with a compatible family.

Keep existing user workflows intact. Name installed workflows with bundle version and precision. Do not include credentials, model weights, runtime artifacts or videos in the repository or image context.

Use source validation and deterministic packaging locally, image installation plus CPU smoke checks in Actions, and actual Runpod GPU generation before claiming runtime performance or model quality. README.md and docs/VALIDATION.md describe the current deployment state.
