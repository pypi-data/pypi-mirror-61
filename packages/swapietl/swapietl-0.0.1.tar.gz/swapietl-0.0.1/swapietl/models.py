# -* coding: utf-8 *-
"""
:py:mod:`swapietl.models.py`
----------------------------
Models used for managing data.
"""
# System imports
# Third-party imports
# Local imports


class CustomCharacter:
    # Although we are not going to handle with 100k character in memory, let's save some mem using slots
    __slots__ = ('_swapi_character', 'appearances', 'species')

    def __init__(self, swapi_character, appearances, species):
        """CustomCharacter initialization

        :param swapi.model.People swapi_character: Character from swapi (People)
        :param int appearances: Number of appearances (just to avoid recomputing)
        :param list(swapi.model.Species) species: List of species of this character
        """
        self._swapi_character = swapi_character
        self.appearances = appearances
        self.species = species

    @property
    def _sort_height(self):
        """Swapi height is in string , this is an implementation to be able to sort by"""
        try:
            return int(self._swapi_character.height)
        except ValueError:
            # Height could be 'unknown' which is impossible to cast to integer
            return 0

    def __getattr__(self, item):
        """Lets populate attributes from swapi character"""
        return getattr(self._swapi_character, item)

    def __repr__(self):
        return '<CustomCharacter - {}>'.format(self.name)
