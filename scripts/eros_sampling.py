"""Apply the v1.5 hybrid adapter and the author's DMD sigma recommendations."""
HYBRID = 'LTX2.3_DMD_hybrid_v2.safetensors'
FIRST = '1.000, 0.955, 0.893, 0.812, 0.715, 0.603, 0.482, 0.241, 0.121, 0.0'
REFINE = '0.92, 0.725, 0.421875, 0.0'


def configure(api, *, base=False):
    for node in api.values():
        typ, inputs = node['class_type'], node['inputs']
        if typ == 'LoraLoaderModelOnly':
            inputs.update(lora_name=HYBRID, strength_model=1.0)
        if typ == 'KSamplerSelect':
            inputs['sampler_name'] = 'euler_ancestral'
        if typ == 'ManualSigmas':
            inputs['sigmas'] = FIRST if float(inputs['sigmas'].split(',')[0]) == 1 else REFINE
    if not base:
        for node in api.values():
            if node['class_type'] == 'LTXVScheduler':
                node['class_type'] = 'ManualSigmas'
                node['inputs'] = {'sigmas': FIRST}
    return api
