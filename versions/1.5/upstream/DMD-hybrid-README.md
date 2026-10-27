---
base_model:
- Lightricks/LTX-2.3
---

This is an extraction of DMD distillation deltas in JoyAi Echo to use in other LTX models. Reshaped for sampling functionality from the LTX 384 1.1 shapes and audio replaced from the LTX 384 1.1 distilled lora. But importantly without it's issues with resampling to base model learning and conditioning drop from the latent and most look overwrites and extra unneccesary details added at upscale resampling. Use at 1.0 in the usual 8/4 step upscale or experiment with other sigmas, any euler or other LTX compatible samplers, no custom loading or sampling needed.

Hybrid versions: my interpretation of efforts here to hybridize both distillations: https://huggingface.co/maximsobolev275/LTX2.3-DMD-Distill-Lora-Hybrids. My version works inside blocks 0-25 to increase the overall movement strength slightly above the standalone DMD versions without letting the LTX distilled lora redraw or bring it's negative base-model tendencies. Overall effect should be improvements to movement smoothness and consistency and possibly some issue with conditioning change, try with stronger conditioning and less aggressive upscale or possibly lower steps and lower preprocessing, but I attempted actually layer blending in v1 which I don't think is the way forward. v2 version replaces the early motion and composition like the other versions which results in much cleaner delta directions and detailing more finer motion especially when it comes to repetetive explicit-type motions. There are infinite ways to blend the two so it might be a few versions. v1 = (blocks 0-12 flat 0.5 BLEND then cosine ramp downward from 0.5 to 0 on blocks 13-25) v2 = (blocks 0-29 replaced with 384 at 0.8 strength video/1.0 audio)

Decent target sigmas:

First Pass - 1.000, 0.955, 0.893, 0.812, 0.715, 0.603, 0.482, 0.241, 0.121, 0.0

First Pass Higher Quality - 1.000, 0.968, 0.926, 0.875, 0.812, 0.741, 0.661, 0.574, 0.482, 0.241, 0.121, 0.000

Upscale - 0.92, 0.725, 0.421875, 0.0

Upscale Less Aggressive - 0.77, 0.55, 0.29, 0.0

https://github.com/TenStrip/10S-Comfy-nodes
