import json
from typing import List
from urllib.request import urlopen
from urllib.parse import quote as urlquote

UD_DEFID_URL = 'https://api.urbandictionary.com/v0/define?defid='
UD_DEFINE_URL = 'https://api.urbandictionary.com/v0/define?term='
UD_RANDOM_URL = 'https://api.urbandictionary.com/v0/random'

class UrbanDefinition:
    def __init__(self, word: str, definition: str, example: str, upvotes: int, downvotes: int):
        self.word = word
        self.definition = definition
        self.example = example
        self.upvotes = upvotes
        self.downvotes = downvotes

    def __str__(self) -> str:
        return f"Word: {self.word}\nDefinition: {self.definition}\nExample: {self.example}\nUpvotes: {self.upvotes}\nDownvotes: {self.downvotes}"

def _get_urban_json(url: str) -> dict:
    try:
        with urlopen(url) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Error fetching data from Urban Dictionary API: {str(e)}")

def _parse_urban_json(json_data: dict, check_result: bool = True) -> List[UrbanDefinition]:
    if json_data is None or any(e in json_data for e in ('error', 'errors')):
        raise ValueError('Invalid input for Urban Dictionary API')
    
    if check_result and ('list' not in json_data or len(json_data['list']) == 0):
        return []
    
    return [UrbanDefinition(
        definition['word'],
        definition['definition'],
        definition['example'],
        int(definition['thumbs_up']),
        int(definition['thumbs_down'])
    ) for definition in json_data['list']]

def define(term: str) -> List[UrbanDefinition]:
    """Search for term/phrase and return list of UrbanDefinition objects."""
    json_data = _get_urban_json(UD_DEFINE_URL + urlquote(term))
    return _parse_urban_json(json_data)

def defineID(defid: int) -> List[UrbanDefinition]:
    """Search for UD's definition ID and return list of UrbanDefinition objects."""
    json_data = _get_urban_json(UD_DEFID_URL + urlquote(str(defid)))
    return _parse_urban_json(json_data)

def random() -> List[UrbanDefinition]:
    """Return random definitions as a list of UrbanDefinition objects."""
    json_data = _get_urban_json(UD_RANDOM_URL)
    return _parse_urban_json(json_data, check_result=False)
