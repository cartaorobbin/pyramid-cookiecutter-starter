from cornice import Service

# Create the Cornice Optin service
greet_service = Service(
    name="greet_service",
    path="/api/v1/greet",
    description="Greet Service",
)

@greet_service.get(
    pcm_show="v1",)
def get_sim(request):
    return {"hello": "world"}