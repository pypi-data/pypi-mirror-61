# -* coding: utf-8 *-
"""
:py:mod:`swapietl.swapi_impl`
=============================
Implementation of the exercise using the swapi library written by
Paul Hallett (https://github.com/phalt/swapi-python)

Although the library has some caveats (as for example, having to compute the height and casting
it into an integer value to be able to apply properly the sort) this is definitely the fastest way
get the result developed, due the abstraction of the API, but with no doubt there's a loot of room
for improvement.

Was about to monkey patch the library, but nobody likes that kind of hacks ;) (except people from gevent)
"""
# System imports
import logging
import csv
from collections import Counter

# Third-party imports
import swapi
import requests

# Local imports
from .models import CustomCharacter


LOGGER = logging.getLogger('swapietl')

# Species cache dictionary
SPECIES_CACHE = {}


def get_species(species_url):
    """ Return species from swapi

    Since this is not implemented in swapi library, using a dictionary as a lazy cache we
    prevent querying the api more than one time for getting information about a species.

    :param str species_url: Species url to retrieve
    :return: Species object
    :rtype: swapi.models.Species
    """
    LOGGER.debug('Retrieving info for species %s', species_url)
    if species_url not in SPECIES_CACHE:
        LOGGER.debug('Species %s not in cache. Querying the api...', species_url)
        SPECIES_CACHE[species_url] = swapi.get_species(extract_id_from_url(species_url))
    return SPECIES_CACHE[species_url]


def extract_id_from_url(url):
    """Extract entity id from url

    :return: Entity name and id from the url
    :rtype: str
    """
    return url.split('/')[-2]


def get_character_appearances():
    """Return list of characters from all movies

    :return: List of characters entities from swapi
    :rtype: list(string)
    """
    LOGGER.debug('Querying the swapi films endpoint to retrieve all films')
    films = swapi.get_all(swapi.FILMS)
    LOGGER.debug('Query produced %s results', films.count())
    character_list = []
    for film in films.iter():
        character_list += film.characters
    return character_list


def get_top_character_appearances(top=10):
    """Return the list of top character appearances

    :param int top: Number of character to return
    :rtype: list(CustomCharacter)
    """
    top_character_counter = Counter(get_character_appearances()).most_common(top)
    return [serialize_to_custom_model(character_url, appearances)
            for character_url, appearances in top_character_counter]


def serialize_to_custom_model(swapi_character_url, appearances):
    LOGGER.debug('Retrieving info for character %s', swapi_character_url)
    swapi_character = swapi.get_person(extract_id_from_url(swapi_character_url))
    species = [get_species(species_url) for species_url in swapi_character.species]
    return CustomCharacter(swapi_character=swapi_character,
                           appearances=appearances,
                           species=species)


def export_to_csv(characters, filename):
    """ Export a list of characters to a file

    :param list characters: List of characters to save
    :param str filename: Filename where to save those characters
    :return: None
    """
    LOGGER.debug('Opening file %s in write mode', filename)
    with open(filename, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(('name', 'species', 'height', 'appearances'))
        for character in characters:
            LOGGER.debug('Dumping %s into a csv row', character)
            csv_writer.writerow(
                [character.name, '-'.join([species.name for species in character.species]),
                 character.height, character.appearances]
            )


def upload_file_to(filename, url):
    response = requests.post(url, files={'output.csv': open(filename, 'rb')})
    return response.status_code, response.text
