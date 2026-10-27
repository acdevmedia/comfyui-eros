# 10Eros v1.5 for ComfyUI on Runpod

Generate video with audio from text, images, first/last frames, or an image and soundtrack. This bundle uses [TenStrip’s latest 10Eros v1.5](https://huggingface.co/TenStrip/LTX2.3-10Eros) and its recommended [DMD hybrid-v2 adapter](https://huggingface.co/TenStrip/LTX2.3_DMD_Lora).

Repository: [acdevmedia/comfyui-eros](https://github.com/acdevmedia/comfyui-eros). Container: **`ghcr.io/acdevmedia/eros-comfyui:1.5`**. Every successful build also publishes an immutable `sha-<commit>` tag.

## Start a pod

1. Build and publish the image through this repository’s GitHub Actions workflow. Source changes alone do not publish an image.
2. Add a Hugging Face read token to Runpod Secrets as `HUGGINGFACE_TOKEN`. Accept any model terms using that account.
3. Review the template with `python3 scripts/create-runpod-template.py --dry-run`, then run it without `--dry-run` to create or update the Eros template. It reads `RUNPOD_API_KEY` from the environment or local `.env`.
4. Deploy the Eros template on an NVIDIA A100 80 GB or another GPU with sufficient VRAM and a CUDA 12.8-compatible host driver. Keep the 200 GB container disk.
5. Wait for model verification and **ComfyUI is READY on port 8188**, then open **Connect → HTTP 8188**.

The template uses temporary container storage. Download your videos and edited workflows before stopping, replacing, or deleting the pod. Outputs live in `/workspace/runpod-slim/ComfyUI/output`.

## Workflows

The Workflows sidebar receives six files prefixed `v1.5_bf16_` (or `v1.5_fp8_`) so older installed workflows are preserved:

- **01 Image to Video — Distilled:** an image and prompt, using the hybrid adapter on both passes.
- **02 Text to Video — Distilled:** a prompt, using the hybrid adapter on both passes.
- **03 Image to Video — Base:** full base sampling followed by hybrid refinement.
- **04 Text to Video — Base:** full base sampling followed by hybrid refinement.
- **05 First and Last Frame to Video:** two images and a prompt, with hybrid sampling.
- **06 Image and Audio to Video:** an image, soundtrack and prompt, with hybrid sampling.

Upload your inputs, describe the shot, adjust **Shot settings**, then click **Run**. Defaults remain 960 × 544, 24 fps and 241 frames, approximately ten seconds. Frame counts must be `8n + 1`. Longer clips require more memory and time.

The accelerated workflows use hybrid-v2 at strength 1.0, CFG 1, Euler-family sampling, the author’s first-pass sigmas `1, .955, .893, .812, .715, .603, .482, .241, .121, 0`, and refinement sigmas `.92, .725, .421875, 0`. First-pass sigmas are exposed in Shot settings. The Base workflows retain their full scheduler and expose sampling steps instead. The former condition-safe adapter and LCM refinement are removed.

The first four workflows retain the repaired graph structure from the earlier Sulphur bundle; workflows 05/06 retain the official LTX 2.3 conditioning structure. Applying the new hybrid settings to these six adapted workflows still requires GPU validation. The author’s original DMD I2V example and adapter recommendations are saved under `versions/1.5/upstream/` for reference.

## Models

The default `EROS_MODEL_VARIANT=bf16` uses the creator’s **`10Eros_v1.5_bf16.safetensors`**, approximately 46.14 GB. Set `EROS_MODEL_VARIANT=fp8` for **`10Eros_v1.5_fp8mixed_experimental_learned.safetensors`**, approximately 30.24 GB, from [LokkenJP’s conversion linked by the model author](https://huggingface.co/LokkenJP/10EROS_1.5_fp8_exp_learned). The FP8 conversion is an independent experimental quantization of v1.5, not a TenStrip-produced checkpoint.

Both variants also download:

- `LTX2.3_DMD_hybrid_v2.safetensors`, approximately 5.10 GB.
- `gemma_3_12B_it_fp4_mixed.safetensors`, approximately 9.45 GB.
- `ltx-2.3-spatial-upscaler-x2-1.1.safetensors`, approximately 1.00 GB.

Total downloads are approximately **61.7 GB for BF16**, or **45.8 GB for FP8**. Each file has a pinned source revision, exact byte size and SHA256 in `versions/1.5/profile.json`. Interrupted downloads resume; verified files are reused. No weights are baked into the image. There is no native-distilled model variant in this bundle.

Changing precision does not overwrite saved workflows. The installer names fresh workflows by version and precision; open the newly installed files after changing `EROS_MODEL_VARIANT`. Old checkpoint files stay on disk until you remove them.

## Runtime and settings

The bundle upgrades ComfyUI to **v0.43.0**, with its release-pinned frontend **1.57.4**, Transformers **5.21.0**, Diffusers **0.42.0**, Hugging Face Hub **2.3.0**, and SageAttention **1.0.6**. KJNodes and ComfyUI-LTXVideo are pinned at their current upstream heads. The official Runpod base **1.4.1** remains the latest upstream release.

PyTorch/torchvision/torchaudio are upgraded together to **2.11.0 / 0.26.0 / 2.11.0**, using **CUDA 12.8** wheels. Newer standalone PyTorch releases exist, but do not have a matching released torchaudio family; this bundle keeps the matched family. Python 3.12 remains the interpreter supplied by the official base. The CUDA wheel runtime requires a compatible NVIDIA host driver; changing Python packages does not upgrade the host driver.

`versions/1.5/runtime-constraints.txt` pins the coordinated dependencies. The image records its complete installed package list in `/opt/eros-python-lock.txt`. Packages are installed at build time, with no updates at boot.

Template environment settings:

- `EROS_MODEL_VARIANT`: `bf16` by default; `fp8` is optional.
- `EROS_VERSION`: `1.5`.
- `HF_TOKEN`: `{{ RUNPOD_SECRET_HUGGINGFACE_TOKEN }}`.
- `HF_HOME`: `/workspace/.cache/huggingface`.
- `COMFYUI_ATTENTION`: `sage` by default, or `pytorch` for a fresh launch configuration.
- `OMP_NUM_THREADS`: automatically set from the container CPU quota unless explicitly supplied.

After first boot, ComfyUI launch arguments are maintained in `/workspace/runpod-slim/comfyui_args.txt`; changing the attention environment variable does not overwrite that file. Existing user settings are preserved.

Startup logs: `/workspace/logs/eros-startup.log`. Downloads require ten GB of free output reserve beyond the missing model bytes. A rejected download usually means an invalid token, missing read permission, or model terms that need acceptance.

## Validation and builds

Local source checks cover graph links, pinned assets, checkpoint/adapter selection, budgets, version consistency, shell syntax and deterministic workflow packaging. Actions builds install dependencies, run `pip check`, start a CPU-only ComfyUI server and verify every workflow’s nodes and required inputs before publishing. No local Docker builds are used.

The current upgrade has not yet been image-built or GPU-tested. CPU checks cannot establish inference quality, audio synchronization, peak VRAM or generation speed. No prior Sulphur performance result is claimed for this bundle. See [validation status](docs/VALIDATION.md).

[Source](https://github.com/acdevmedia/comfyui-eros) · [Builds](https://github.com/acdevmedia/comfyui-eros/actions) · [Model license](versions/1.5/LICENSE-model.txt)
