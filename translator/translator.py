from Questgen import main
from pprint import pprint
import nltk
nltk.download('stopwords')
# for help on the tags nltk.help.upenn_tagset('RB')
# python -m nltk.downloader universal_tagset
# python -m spacy download en

qe = main.BoolQGen()
payload = {
    "input_text": "Sachin Ramesh Tendulkar is a former international cricketer from India and a former captain of the Indian national team. He is widely regarded as one of the greatest batsmen in the history of cricket. He is the highest run scorer of all time in International cricket."
}
output = qe.predict_boolq(payload)
pprint(output)
