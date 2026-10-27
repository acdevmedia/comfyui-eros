#!/usr/bin/env bash
set -Eeuo pipefail
mode=${1:-build}
ffmpeg -version | head -n 1
python3 - "$mode" <<'PY'
import importlib.metadata as m
import json
import sys
from pathlib import Path
import torch
from sageattention import sageattn
from huggingface_hub import hf_hub_download
print('[validation] Python',sys.version.split()[0],'PyTorch',torch.__version__,'CUDA',torch.version.cuda,'SageAttention',m.version('sageattention'),flush=True)
profile=json.loads(Path('/opt/eros/versions/1.5/profile.json').read_text())
assert torch.__version__==profile['torch_version']
assert torch.version.cuda==profile['cuda_version']
for package,key in [('transformers','transformers_version'),('diffusers','diffusers_version'),('huggingface-hub','huggingface_hub_version'),('comfyui-frontend-package','frontend_version')]:
    assert m.version(package)==profile[key], (package,m.version(package),profile[key])
for path in Path('/opt/eros/versions/1.5').rglob('*.json'):json.loads(path.read_text())
assert '--use-sage-attention' in Path('/opt/comfyui-baked/comfy/cli_args.py').read_text()
if sys.argv[1]=='runtime':
    assert torch.cuda.is_available(), 'No CUDA GPU available. Select an NVIDIA GPU pod.'
    print('[GPU]',torch.cuda.get_device_name(),torch.cuda.get_device_capability(),flush=True)
    q=torch.randn(1,8,256,128,device='cuda',dtype=torch.float16)
    out=sageattn(q,q,q,tensor_layout='HND',is_causal=False)
    torch.cuda.synchronize()
    assert out.isfinite().all(), 'SageAttention returned nonfinite output'
    print('[attention] SageAttention kernel executed successfully on the assigned GPU. ComfyUI selection is confirmed in its launch log.',flush=True)
PY
