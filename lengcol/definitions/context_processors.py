from definitions import services


def last_definitions(request):
    last_definitions = services.DefinitionGathering.get_last_definitions(5)
    return {'last_definitions': last_definitions}
