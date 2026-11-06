"""Give the workflows a consistent layout without changing their execution."""
from workflow_panels import flatten


def style_workflow(data, title, labels=None, guided=False):
    before = flatten(data)
    labels = labels or {}
    inputs = [n for n in data['nodes'] if n['type'] in ('LoadImage', 'LoadAudio', 'LoadVideo', 'SphereLightManualNode')]
    # Show the opening frame first: it is the later loader in the first and last frame graph.
    if 'First and Last' in title:inputs.sort(key=lambda n:n['id'],reverse=True)
    height = 1320 if len(inputs) > 1 else 960
    for node in data['nodes']:
        typ = node['type']
        if typ == 'PrimitiveStringMultiline':
            node.update(title='01 · Describe your shot', pos=[0, 100], size=[480, 220], color='#28524d', bgcolor='#172f2c')
        elif typ in ('LoadImage', 'LoadAudio', 'LoadVideo', 'SphereLightManualNode'):
            label = labels.get(str(node['id'])) or ('Your soundtrack' if typ == 'LoadAudio' else 'Your source video' if typ == 'LoadVideo' else ('First frame' if inputs.index(node) == 0 else 'Last frame') if 'First and Last' in title else 'Starting image')
            node.update(title=label, pos=[0, 380 + inputs.index(node) * 540], size=[480, 520 if len(inputs)>1 else 680], color='#334c63', bgcolor='#1b2b3b')
        elif typ.startswith('Save'):
            node.update(title='03 · Your audio' if 'Audio' in typ else '03 · Your video', pos=[1120, 100], size=[580, height], color='#3c5540', bgcolor='#223025')
        else:
            node.update(title='02 · Shot settings', pos=[540, 100], size=[520, height], color='#484661', bgcolor='#29283d')
    last = max(n['id'] for graph in [data] + data.get('definitions', {}).get('subgraphs', []) for n in graph.get('nodes', [])) + 1
    data['nodes'].append({'id':last, 'type':'MarkdownNote', 'pos':[0,-60], 'size':[1700,100], 'flags':{}, 'order':0, 'mode':0,
        'inputs':[], 'outputs':[], 'title':'10Eros 1.5 · '+title,
        'properties':{}, 'widgets_values':['**Make a shot.** Follow the guide on the left, add your inputs, adjust Shot settings, then click **Run**.' if guided else '**Make a shot.** Describe the scene, add your inputs, adjust Shot settings, then click **Run**.\n\nDefault: 960 × 544 · 24 fps · 241 frames (about 10 seconds). With an image, Width and Height set the frame\'s area and the image sets its shape, so a head-to-toe portrait stays head to toe. Turn on Exact Frame in Shot settings to use your exact Width and Height instead, which centre-crops the image.'],
        'color':'#23413c', 'bgcolor':'#142723'})
    data['last_node_id'] = last
    # Let the frontend fit the whole graph to the actual window on first open.
    data.setdefault('extra', {}).pop('ds', None)
    assert before == flatten(data), 'Styling changed workflow execution'
    return data
