# Official Runpod image, resolved from upstream comfyui-v1.4.1. No local builds.
FROM runpod/comfyui:1.4.1-comfyuiv0.35.0-cuda12.8@sha256:d411ebacf3fdbc98ded7f78f06ac12aae20c08041cde79ab08173c156d04aae5
SHELL ["/bin/bash", "-euo", "pipefail", "-c"]
ENV EROS_VERSION=1.5 EROS_MODEL_VARIANT=bf16 \
    HF_HOME=/workspace/.cache/huggingface HF_HUB_DISABLE_TELEMETRY=1 \
    COMFYUI_ATTENTION=sage PYTHONUNBUFFERED=1
# Upgrade the matched torch/vision/audio family together. The CUDA wheel supplies
# its userspace runtime; the host must provide a CUDA 12.8-compatible NVIDIA driver.
COPY versions/1.5/runtime-constraints.txt /opt/comfyui-runtime-constraints.txt
RUN python3 -m pip install --no-cache-dir --upgrade --index-url https://download.pytorch.org/whl/cu128 \
    'torch==2.11.0+cu128' 'torchvision==0.26.0+cu128' 'torchaudio==2.11.0+cu128'

RUN curl -fsSL https://github.com/Comfy-Org/ComfyUI/archive/426f5eea52a7ece1dd599fff4cb6cd1f352ddd24.tar.gz -o /tmp/comfy.tar.gz && \
    rm -rf /opt/comfyui-baked && mkdir /opt/comfyui-baked && \
    tar xzf /tmp/comfy.tar.gz --strip-components=1 -C /opt/comfyui-baked && rm /tmp/comfy.tar.gz && \
    mkdir -p /opt/comfyui-baked/custom_nodes/ComfyUI-KJNodes && \
    curl -fsSL https://github.com/kijai/ComfyUI-KJNodes/archive/92783f23cf9df6a57ca4c5e035b4714ac0e2bcb4.tar.gz | \
    tar xz --strip-components=1 -C /opt/comfyui-baked/custom_nodes/ComfyUI-KJNodes && \
    mkdir -p /opt/comfyui-baked/custom_nodes/ComfyUI-LTXVideo && \
    curl -fsSL https://github.com/Lightricks/ComfyUI-LTXVideo/archive/220e1d45aa0469f518e982102fca4dca92a61862.tar.gz | \
    tar xz --strip-components=1 -C /opt/comfyui-baked/custom_nodes/ComfyUI-LTXVideo && \
    python3 -m pip install --no-cache-dir -c /opt/comfyui-runtime-constraints.txt \
    -r /opt/comfyui-baked/requirements.txt \
    -r /opt/comfyui-baked/custom_nodes/ComfyUI-KJNodes/requirements.txt \
    -r /opt/comfyui-baked/custom_nodes/ComfyUI-LTXVideo/requirements.txt \
    'sageattention==1.0.6' 'huggingface_hub==2.3.0' 'transformers==5.21.0' 'diffusers==0.42.0' && \
    python3 -m pip check && \
    printf 'COMFYUI_VERSION=v0.43.0\nEROS_VERSION=1.5\n' > /opt/comfyui-baked/.runpod-bundle-version && \
    python3 -m pip freeze > /opt/eros-python-lock.txt
COPY scripts /opt/eros/scripts
COPY versions /opt/eros/versions
ARG VCS_REF=development
RUN printf "EROS_BUNDLE=%s\n" "$VCS_REF" >> /opt/comfyui-baked/.runpod-bundle-version && \
    sed -i 's/BAKED_NODES=(/BAKED_NODES=("ComfyUI-LTXVideo" /' /start.sh && \
    chmod +x /opt/eros/scripts/*.sh && /opt/eros/scripts/validate.sh build && python3 /opt/eros/scripts/check-build-server.py
EXPOSE 8188
ENTRYPOINT ["/opt/eros/scripts/entrypoint.sh"]
