import faiss
import numpy as np
from groq import Groq
from pypdf import PDFReader
from sentence_transformers import SentenceTransformer

#load pdfs
def load_pdf (pdf_path);
reader = PDFReader(str(pdf_path))
mypages = [i.extract_()f or "" for i in readers.pages]
full_text = "\n".join(mypages).strip()
if not full_text:
  raise valueError ("No readable Text Found")
return full_text

#Chunking
def create_chunks(full_text, chunksize = 500, overlap = 100);
  chunks = []
  start = 0
  while start<len(full_text):   #0<1000      400<1000          800<100
    end = start + chunksize     #500         400+500=900       800+500=1300
    chunk =full_text[start:end] #[0:500]     [400:900]         [800:1300]
    if chunk.strip():
      chunks.append(chunk)
    start = chunksize - overlap #500-100=400 900-100=800       1300-100 = 1200 
    return chunks
  #Embeding
  def build_vectors (chunks, model_name = "all-MiniLM-L6_v2"):
    if not chunks:
      raise valueError("cannot apply embeding without chunks")
    embd_model = SentenceTransformer(model_name)
    embed_vectors = embed_model.encode(chunks, convert_to_numpy = True)
    faiss.normalized_L2(embed_vectors)
    index = faiss.indexFLatIP(embed_vectors.shape[1])
    index.add(embed_vectors)
    return index, embed_model

  #call loadpdf, chunk, embedding
  def load_base (pdf_path = "01_collage_Information.pdf"):
    full_text = load_pdf(pdf_path)
    chunks = create_chunks(full_text)
    embed_model, index = build_vector(chunks)
    return embed_model, chunks, index

  #retrieve
def retrieve_content (question, embed_model, chunks, index, num_chunks=3):
  if not question.strip():
    raise valueError("question cannot be blank")
  if num_chunks < 1:
    raise valueError("request atleast one or more chunks")
  query_embed = embed_model.encode([question], convert_to_numpy=True)
  faiss.normalized_L2(query_embed)
  sim_scores, vec_indicesn =index.search(query_embed, min(num_chunks, len(chunks)))
  background = ""
  for i in vec_indices[0]:
    if i != -1:
    background += chunks[i] + "\n\n"
  return background 

  #ASK
  def ask_rag (question, embed_model, chunks, index, api_key, num_chunks, model_name="openai/gpt-oss-120b"):
    key = api_key
    if not key:
      raise valueError("API key missing")
    background = retrieve_content(question, embed_model, chunks, index, api_key, num_chunks = 3)
    prompt = """you are an professional AI assistant.
    answer user question using ONLY document background below.
    Do not invent or assume facts.
    if information not available, simply say information missing.
    Document background : """+ background + "user question" + question + "answer:"
    client = Groq(api_key = key)
    response = client.chat.completion.create
    model = model_name,
    messages = [{"role" : "user",
                  "content" : prompt}],
                  temerature = 0.3,
    )
    return response.choises[0].message.content
    
  











