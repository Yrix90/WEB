# UTF-8


def search4vowels(pharse: str) -> set:
    """ Returns the set of vowels found in 'pharse"."""
    return set('aeiou').intersection(set(pharse))


def search4letters(pharse: str, letters: str='aeiou') -> set:
    """Reuns the set of 'letters' found in 'pharse'."""
    return set(letters).intersection(set(pharse))

