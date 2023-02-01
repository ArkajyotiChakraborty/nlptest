from typing import Dict, List
import pandas as pd

_DEFAULT_PERTURBATIONS = [
    "uppercase",
    "lowercase",
    "titlecase",
    "add_punctuation",
    "strip_punctuation",
    "add_typo",
    "american_to_british",
    "add_context",
    "add_contractions",
    "swap_entities",
    "swap_cohyponyms"
]

_TYPO_FREQUENCY = {
    "a": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 594, 1, 42401, 1, 1, 1, 10893, 3882, 1, 3062],
    "b": [1, 1, 1, 1, 1, 16112, 21182, 10826, 1, 1, 1, 1, 1, 19375, 1, 1, 1, 1, 1, 1, 1, 6146, 1, 1, 1, 1],
    "c": [1, 1, 1, 19151, 1, 15124, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 37974, 1, 1, 7444, 1, 1, 1, 1],
    "d": [1, 1, 1, 1, 39499, 16091, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 64063, 80813, 1, 1, 7848, 10614, 2018, 1, 1],
    "e": [1, 1, 1, 1, 1, 17080, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 76503, 75665, 1, 1, 1, 13193, 1, 1, 1],
    "f": [1, 1, 1, 1, 1, 1, 13344, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 18722, 1, 20980, 1, 5822, 1, 1, 1, 1],
    "g": [1, 1, 1, 1, 1, 1, 1, 10144, 1, 1, 1, 1, 1, 23414, 1, 1, 1, 22092, 1, 30296, 1, 5093, 1, 1, 5295, 1],
    "h": [1, 1, 1, 1, 1, 1, 1, 1, 1, 2663, 1, 1, 11486, 11859, 1, 1, 1, 1, 1, 23856, 10462, 1, 1, 1, 1, 1],
    "i": [1, 1, 1, 1, 1, 1, 1, 1, 1, 699, 9983, 40985, 1, 1, 82987, 1, 1, 1, 1, 1, 63669, 1, 1, 1, 1, 1],
    "j": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1248, 1, 3464, 2011, 1, 1, 1, 1, 1, 1, 568, 1, 1, 1, 1, 1],
    "k": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14651, 8496, 1, 8366, 1, 1, 1, 1, 1, 5455, 1, 1, 1, 1, 1],
    "l": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 43713, 30126, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "m": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 23433, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "n": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "o": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 18072, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "p": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "q": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2041, 1, 1, 1, 728, 1, 1, 1],
    "r": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 54571, 1, 1, 1, 1, 1, 1],
    "s": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 17079, 3613, 1, 7300],
    "t": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13286, 1],
    "u": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 6783, 1],
    "v": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "w": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "x": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 516],
    "y": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "z": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}

_PERTURB_CLASS_MAP = {
    "uppercase": 'UpperCase',
    "lowercase": 'LowerCase',
    "titlecase": 'TitleCase',
    "add_punctuation": 'AddPunctuation',
    "strip_punctuation": 'StripPunctuation',
    "add_typo": 'AddTypo',
    "american_to_british": 'ConvertAccent',
    "british_to_american": 'ConvertAccent',
    "add_context": 'AddContext',
    "add_contractions": 'AddContractions',
    "swap_entities": 'SwapEntities',
    "swap_cohyponyms": 'SwapCohyponyms'
}

def create_terminology(ner_data: pd.DataFrame) -> Dict[str, List[str]]:
    """Iterate over the DataFrame to create terminology from the predictions. IOB format converted to the IO.

    Args:
        ner_data: Pandas DataFrame that has 2 column, 'text' as string and 'label' as list of labels

    Returns:
        Dictionary of entities and corresponding list of words.
    """
    terminology = {}

    chunk = list()
    ent_type = None
    for i, row in ner_data.iterrows():

        sent_labels = row.label
        for token_indx, label in enumerate(sent_labels):

            if label.startswith('B'):

                if chunk:
                    if terminology.get(ent_type, None):
                        terminology[ent_type].append(" ".join(chunk))
                    else:
                        terminology[ent_type] = [" ".join(chunk)]

                sent_tokens = row.text.split(' ')
                chunk = [sent_tokens[token_indx]]
                ent_type = label[2:]

            elif label.startswith('I'):

                sent_tokens = row.text.split(' ')
                chunk.append(sent_tokens[token_indx])

            else:

                if chunk:
                    if terminology.get(ent_type, None):
                        terminology[ent_type].append(" ".join(chunk))
                    else:
                        terminology[ent_type] = [" ".join(chunk)]

                chunk = None
                ent_type = None

    return terminology
