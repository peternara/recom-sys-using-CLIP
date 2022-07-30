# Modified by Sehyun Kim, 2022-07-20(July 20th, 2022), @RebuilderAI, Seoul, South Korea

import clip
import numpy as np
import openai
from PIL import Image
import torch
openai_api_key = "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"
openai.api_key = openai_api_key

# With clip_version ViT-L/14 inference for each image takes more than 12 seconds, too slow to use.
# Available CLIP model versions: ["RN50", "RN101", "RN50x4", "RN50x16", "RN50x64", "ViT-B/32", "ViT-B/16", "ViT-L/14"] {type:"string"}
clip_version = "ViT-B/16"

gpt_version = "text-davinci-002" #@param ["text-davinci-001", "text-davinci-002", "text-curie-001", "text-babbage-001", "text-ada-001"] {type:"string"}

clip_feat_dim = {'RN50': 1024, 'RN101': 512, 'RN50x4': 640, 'RN50x16': 768, 'RN50x64': 1024, 'ViT-B/32': 512, 'ViT-B/16': 512, 'ViT-L/14': 768}[clip_version]

# Download CLIP model weights.
# model, preprocess = clip.load(clip_version)  # clip.available_models()

def num_params(model):
    return np.sum([int(np.prod(p.shape)) for p in model.parameters()])

# Define CLIP helper functions (e.g., nearest neighbor search).
def get_text_feats(model, in_text, batch_size=64):
    text_tokens = clip.tokenize(in_text).cuda()
    text_id = 0
    text_feats = np.zeros((len(in_text), clip_feat_dim), dtype=np.float32)
    while text_id < len(text_tokens):  # Batched inference.
        batch_size = min(len(in_text) - text_id, batch_size)
        text_batch = text_tokens[text_id:text_id+batch_size]
        with torch.no_grad():
            batch_feats = model.encode_text(text_batch).float()
        batch_feats /= batch_feats.norm(dim=-1, keepdim=True)
        batch_feats = np.float32(batch_feats.cpu())
        text_feats[text_id:text_id+batch_size, :] = batch_feats
        text_id += batch_size
    return text_feats

def get_img_feats(model, preprocess, img):
    img_pil = Image.fromarray(np.uint8(img))
    img_in = preprocess(img_pil)[None, ...]
    with torch.no_grad():
      img_feats = model.encode_image(img_in.cuda()).float()
    img_feats /= img_feats.norm(dim=-1, keepdim=True)
    img_feats = np.float32(img_feats.cpu())
    return img_feats

def get_nn_text(raw_texts, text_feats, img_feats):
    scores = text_feats @ img_feats.T
    scores = scores.squeeze()
    high_to_low_ids = np.argsort(scores).squeeze()[::-1]
    high_to_low_texts = [raw_texts[i] for i in high_to_low_ids]
    high_to_low_scores = np.sort(scores).squeeze()[::-1]
    return high_to_low_texts, high_to_low_scores

# Define GPT-3 helper functions
def prompt_llm(prompt, max_tokens=64, temperature=0, stop=None):
    response = openai.Completion.create(engine=gpt_version, prompt=prompt, max_tokens=max_tokens, temperature=temperature, stop=stop)
    return response["choices"][0]["text"].strip()