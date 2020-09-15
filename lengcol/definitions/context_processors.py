from definitions import services


def last_terms(request):
    last_terms = services.TermGathering.get_last_terms(5)
    return {'last_terms': last_terms}
