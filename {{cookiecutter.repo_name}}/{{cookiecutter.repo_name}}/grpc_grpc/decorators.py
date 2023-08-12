
services = []

def config_grpc_service(function):
    services.append(function)
    def wrapper():
        pass
    return wrapper

def get_services():
    return services