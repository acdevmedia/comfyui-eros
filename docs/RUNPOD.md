# Runpod deployment

Use the local [README](../README.md) for the 10Eros setup. Publish `ghcr.io/acdevmedia/eros-comfyui:1.5` through GitHub Actions, then run `python3 scripts/create-runpod-template.py` to create a separate Eros template. Use `--dry-run` to review its payload. The existing Sulphur template is not updated.
