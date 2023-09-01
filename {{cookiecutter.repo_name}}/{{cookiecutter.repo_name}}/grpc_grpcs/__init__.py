

def includeme(config):
    config.include('pyramid_grpc')
    config.scan(".")