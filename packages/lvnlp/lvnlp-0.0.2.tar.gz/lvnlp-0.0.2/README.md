# LVNLP

## Setup
- `python3.6+`
- `pip3 install lvnlp`


## Tools

### NLPPIPE_CLIENT
```
from lvnlp import nlppipe_run
print(nlppipe_run('Jānis brauc uz Rīgu.', ['tokenizer', 'ner']))
```


### NER_ALLENNLP
Run API:
- `python3 -m lvnlp.ner_allennlp <MODEL_PATH>`
- Visit `http://localhost:8800?text=Jānis brauc uz Rīgu.`

From code:
```
p = TaggerPredictor.from_path(<MODEL_PATH>, 'tagger')
print(p.get_entities("""Ar cieņu , Rasa Jankovska p.k. 77923842011"""))
[{'text': 'Rasa Jankovska', 'label': 'person', 'start': 11, 'end': 25}, {'text': '77923842011', 'label': 'person_id', 'start': 31, 'end': 42}]
```


## License
GPL-3.0
