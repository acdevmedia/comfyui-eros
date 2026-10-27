"""Give the six workflows a consistent layout without changing their execution."""
from workflow_panels import flatten


def style_workflow(data, title):
    before = flatten(data)
    inputs = [n for n in data['nodes'] if n['type'] in ('LoadImage', 'LoadAudio', 'LoadVideo')]
    height = 860 if len(inputs) > 1 else 680
    image_index = 0
    for node in data['nodes']:
        typ = node['type']
        if typ == 'PrimitiveStringMultiline':
            node.update(title='01 · Describe your shot', pos=[0, 100], size=[480, 220], color='#28524d', bgcolor='#172f2c')
        elif typ in ('LoadImage', 'LoadAudio', 'LoadVideo'):
            label = 'Your soundtrack' if typ == 'LoadAudio' else 'Your source video' if typ == 'LoadVideo' else ('First frame' if image_index == 0 else 'Last frame') if 'First and Last' in title else 'Starting image'
            node.update(title=label, pos=[0, 380 + inputs.index(node) * 320], size=[480, 260 if len(inputs)>1 else 300], color='#334c63', bgcolor='#1b2b3b')
            if typ == 'LoadImage':image_index += 1
        elif typ.startswith('Save'):
            node.update(title='03 · Your audio' if 'Audio' in typ else '03 · Your video', pos=[1120, 100], size=[580, height], color='#3c5540', bgcolor='#223025')
        else:
            node.update(title='02 · Shot settings', pos=[540, 100], size=[520, height], color='#484661', bgcolor='#29283d')
    last = max(n['id'] for graph in [data] + data.get('definitions', {}).get('subgraphs', []) for n in graph.get('nodes', [])) + 1
    data['nodes'].append({'id':last, 'type':'MarkdownNote', 'pos':[0,-60], 'size':[1700,100], 'flags':{}, 'order':0, 'mode':0,
        'inputs':[], 'outputs':[], 'title':'10Eros 1.5 · '+title,
        'properties':{}, 'widgets_values':['**Make a shot.** Describe the scene, add your inputs, adjust Shot settings, then click **Run**.\n\nDefault: 960 × 544 · 24 fps · 241 frames (about 10 seconds).'],
        'color':'#23413c', 'bgcolor':'#142723'})
    data['last_node_id'] = last
    # Let the frontend fit the whole graph to the actual window on first open.
    data.setdefault('extra', {}).pop('ds', None)
    assert before == flatten(data), 'Styling changed workflow execution'
    return data
