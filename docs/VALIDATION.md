# Validation status — 10Eros v1.5

The CUDA 12.8 image for commit `901be83fd810811da1c70e2d5a5ca9f2ffc7c998` passed [GitHub Actions](https://github.com/acdevmedia/comfyui-eros/actions/runs/40450520146), dependency checks, and CPU ComfyUI validation for all six workflows. Published digest: `sha256:2c80b33cc63a6ec2c4db61cd96793a9fcfaf5f9deb699d3d959d36825800ac73`.

GPU checks passed on a Runpod NVIDIA A100-SXM4-80GB with driver 595.91.07, PyTorch 2.11.0+cu128 and SageAttention 1.0.6:

- The startup SageAttention kernel executed successfully, and generation used `--use-sage-attention`.
- All six BF16 workflows generated 25-frame MP4s at 960 × 544 with H.264 video and AAC audio.
- A BF16 image-to-video hybrid shot generated 241 frames at 24 fps, 10.041667 seconds, at 960 × 544 with AAC audio. The warmed fixture run took 26.15 seconds; this single sample does not establish general throughput.
- The independent experimental FP8 v1.5 checkpoint passed SHA256 verification and a 25-frame text-to-video generation check.
- No inference exceptions occurred in the completed matrix. Inputs were neutral synthetic sailboat images, a descriptive prompt, and a quiet tone for the supplied-audio workflow.

The later layout polish is checked against the flattened executable graph: titles, positions, sizes, colors, notes and initial camera behavior do not change execution. Pristine installed workflows were backed up before the polished versions were applied to the test pod. The pod was left running at the user's request.

Local checks cover graph links, checkpoint/adapter selection, source revisions and SHA256 metadata, storage budgets, version consistency, deterministic packaging, shell syntax and Python compilation. A fixture installer test exercises both precision variants, restart reuse and workflow preservation without downloading weights locally.

ComfyUI v0.43.0 uses its release-pinned frontend 1.57.4. The matched torch/vision/audio family is 2.11.0/0.26.0/2.11.0 with CUDA 12.8; newer standalone torch releases lack a matching released torchaudio family. Python 3.12 remains the official base interpreter. The first CUDA 13.0 build also passed CPU checks; the final CUDA 12.8 target was used for A100 deployment. Runpod's explicit CUDA scheduler filter prevented allocation; removing that filter produced a compatible host.

No local Docker builds were performed. Image builds and publication run in Actions. Output media checks establish format, dimensions, frame count and an audio stream; perceptual quality, lip sync and audio synchronization remain for human evaluation. Prior Sulphur timings are not claimed for Eros.
