from torch import nn
# from eval import img2text_CLIP
from transformers import BertTokenizer, BertModel

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
bert_model = BertModel.from_pretrained("bert-base-uncased")
cos_similarity = nn.CosineSimilarity(dim=1, eps=1e-6)

synonym_dict = {}
synonym_dict['amazing'] = ['awesome', 'incredible', 'fascinating']
synonym_dict['brisk'] = ['lively', 'energetic', 'active']
synonym_dict['calm'] = ['relaxed', 'serene', 'quiet']
synonym_dict['cozy'] = ['comfortable', 'comfy', 'restful']

antonym_dict = {}
antonym_dict['wonderful'] = ['awful', 'terrible', 'bad']

vocab_feat_dict = {}
cos_sim_dict = {}

sen_dict = {}
sen_dict["I love horror movies"] = ["Lights out is a horror movie"]
sen_dict["The dog bites the man"] = ["The man bites the dog", "The man bites the woman", "A Labrador Retriever is biting the boy"]
sen_feat_dict = {}

test_sen = "The mood of the studio should be light and airy, and the best studio light is natural light. The two best background colors are white and cream"

for vocab, syn_list in synonym_dict.items():
    encoded_vocab = tokenizer(vocab, return_tensors='pt')
    vocab_feat = bert_model(**encoded_vocab).pooler_output
    vocab_feat_dict[vocab] = vocab_feat
        
    for syn in syn_list:
        encoded_syn = tokenizer(syn, return_tensors='pt')
        syn_feat = bert_model(**encoded_syn).pooler_output
        vocab_feat_dict[syn] = syn_feat

        cos_sim_dict[(vocab,syn)] = cos_similarity(vocab_feat, syn_feat)

for vocab, ant_list in antonym_dict.items():
    encoded_vocab = tokenizer(vocab, return_tensors='pt')
    vocab_feat = bert_model(**encoded_vocab).pooler_output
    vocab_feat_dict[vocab] = vocab_feat
        
    for ant in ant_list:
        encoded_ant = tokenizer(ant, return_tensors='pt')
        ant_feat = bert_model(**encoded_ant).pooler_output
        vocab_feat_dict[ant] = ant_feat

        cos_sim_dict[(vocab, ant)] = cos_similarity(vocab_feat, ant_feat)

# for key, val in cos_sim_dict.items():
#     print(key, val)

for sen, sim_sen in sen_dict.items():
    encoded_sen = tokenizer(sen, return_tensors='pt')
    sen_feat = bert_model(**encoded_sen).pooler_output
    sen_feat_dict[sen] = sen_feat
        
    for s in sim_sen:
        encoded_s = tokenizer(s, return_tensors='pt')
        s_feat = bert_model(**encoded_s).pooler_output
        sen_feat_dict[sen] = s_feat

        cos_sim_dict[(sen, s)] = cos_similarity(sen_feat, s_feat)


for key, val in cos_sim_dict.items():
    print(key, val)

