from cornice import Service

# Create the Cornice Optin service
hello_service = Service(
    name="simple_service",
    path="/api/v1/simple_service",
    description="Optin Service",
)

@hello_service.get(
    pcm_show="v1",)
def get_sim(request):
    return {"hello": "world"}