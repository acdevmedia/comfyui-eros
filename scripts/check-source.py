#!/usr/bin/env python3
"""Small structural checks run locally and in Actions without model downloads."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=list((ROOT/'versions/1.5/workflows').glob('*.json'))
catalog=json.loads((ROOT/'versions/1.5/workflow-catalog.json').read_text())
# Four author workflows plus the adapted official LTX 2.3 examples listed in the catalog.
assert sorted(p.name for p in files)[4:]==sorted(e['file'] for e in catalog.values())
for path in files:
    d=json.loads(path.read_text())
    if 'nodes' in d:
        ids={n['id'] for n in d['nodes']}
        assert len(ids)==len(d['nodes'])
        assert all(l[1] in ids and l[3] in ids for l in d['links'])
        for sg in d.get('definitions',{}).get('subgraphs',[]):
            inner={n['id'] for n in sg['nodes']}|{-10,-20}
            assert all(l['origin_id'] in inner and l['target_id'] in inner for l in sg['links'])
        for n in d['nodes']:
            if n['type']=='LoraLoaderModelOnly' and 'sulphur' in str(n.get('widgets_values',[])):assert n['mode']==4
    else:
        for n in d.values():
            for v in n['inputs'].values():
                if isinstance(v,list):assert v[0] in d
p=json.loads((ROOT/'versions/1.5/profile.json').read_text())
assert {x['variant'] for x in p['models']} == {'fp8', 'bf16', 'all'}
assert p['default_checkpoint'] == next(x['file'] for x in p['models'] if x['variant']==p['default_variant'])
for path in files + list((ROOT/'versions/1.5/api').glob('*.json')):
    text=path.read_text()
    assert p['default_checkpoint'] in text, f'{path}: incorrect checkpoint'
    assert 'sulphur_dev_' not in text, f'{path}: stale checkpoint'
assert all(sum(x['size'] for x in p['models'] if x['variant'] in (variant,'all'))<100e9 for variant in ('fp8','bf16'))
assert all(len(x['sha256'])==64 and len(x['revision'])==40 for x in p['models'])
# Check delivered sampling and deployment identity alongside graph structure.
for path in (ROOT/'versions/1.5/api').glob('*.json'):
    api=json.loads(path.read_text())
    for node in api.values():
        if node['class_type']=='LoraLoaderModelOnly':
            assert node['inputs']['lora_name']=='LTX2.3_DMD_hybrid_v2.safetensors'
            assert node['inputs']['strength_model']==1.0
        if node['class_type']=='KSamplerSelect':
            assert node['inputs']['sampler_name']=='euler_ancestral'
        if 'BASE' not in path.name:assert node['class_type']!='LTXVScheduler'
docker=(ROOT/'Dockerfile').read_text()
assert f"EROS_VERSION={p['version']} EROS_MODEL_VARIANT={p['default_variant']}" in docker
assert p['comfyui_commit'] in docker
constraints=(ROOT/'versions/1.5/runtime-constraints.txt').read_text()
assert 'torch=='+p['torch_version'] in constraints
assert 'comfyui-frontend-package=='+p['frontend_version'] in constraints
print(f'PASS: {len(files)} workflow graphs; valid links, pinned assets, default model budget <100 GB.')
