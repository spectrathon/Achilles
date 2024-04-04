from matplotlib import pyplot as plt
from sentence_transformers import SentenceTransformer, util
import torch
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize
import nltk
from nltk.corpus import stopwords
import yake
import wikipedia
kw_extractor = yake.KeywordExtractor()
nltk.download('stopwords')
model = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

def runner_cde(text):

  #text = """The himalayas are the smallest mountain range."""
  language = "en"
  max_ngram_size = 2
  deduplication_threshold = 0.7
  numOfKeywords = 20
  custom_kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, top=numOfKeywords, features=None)
  keywords = custom_kw_extractor.extract_keywords(text)
  #articles= text + "\n"
  articles=""
  for kw in keywords:
    results=wikipedia.search(kw[0])
    for result in results:
      try:
        articles = articles + "\n" + wikipedia.page(result, auto_suggest=False, redirect=True).content
      except:
        print("")


  lists = []

  lists = articles.split('\n')

  # print(lists)

  fstring=""  
  for i in lists:
    c=0
    if i != "":
      for j in i:
        if j == '.':
          c=1
          break
      if c==1:
        fstring= fstring + i+'\n'


  with open("new.txt",'w') as f:
     f.write(fstring)
  
  ps = PorterStemmer()
  f = open("new.txt")
  a = sent_tokenize(f.read())

  # removal of stopwords
  stop_words = list(stopwords.words('english'))

  # removal of punctuation signs
  punc = '''=!()-[]{};:'"\, <>./?@#$%^&*_~'''
  s = [(word_tokenize(a[i])) for i in range(len(a))]
  outer_1 = []

  for i in range(len(s)):
      inner_1 = []

      for j in range(len(s[i])):

          if s[i][j] not in (punc or stop_words):
              s[i][j] = ps.stem(s[i][j])

              if s[i][j] not in stop_words:
                  inner_1.append(s[i][j].lower())

      outer_1.append(set(inner_1))
  rvector = outer_1[0]

  for i in range(1, len(s)):
      rvector = rvector.union(outer_1[i])
  outer = []

  for i in range(len(outer_1)):
      inner = []

      for w in rvector:

          if w in outer_1[i]:
              inner.append(1)

          else:
              inner.append(0)
      outer.append(inner)
  comparison = text


  check = (word_tokenize(comparison))
  check = [ps.stem(check[i]).lower() for i in range(len(check))]


  check1 = []
  for w in rvector:
      if w in check:
          check1.append(1)  # create a vector
      else:
          check1.append(0)

  ds = []

  for j in range(len(outer)):
      similarity_index = 0
      c = 0

      if check1 == outer[j]:
          ds.append(0)
      else:
          for i in range(len(rvector)):

              c += check1[i]*outer[j][i]

          similarity_index += c
          ds.append(similarity_index)


  ds
  maximum = max(ds)
  test = [""]
  print()
  print()
  print("")
  j=0
  for i in range(len(ds)):

      if ds[i] == maximum:
          test.append(a[i])



  query_embedding = model.encode(text)
  passage_embedding = model.encode(test)

  result = util.dot_score(query_embedding, passage_embedding)

  maxi = torch.max(result)

  # for i in maxi:
  #   print(i)

  return maxi




def main(stringer):
  result = runner_cde(stringer)
  results = False
  if result > 0.75:
    results = True
  #print(result)
  return(results,result)
