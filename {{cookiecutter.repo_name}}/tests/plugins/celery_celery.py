import pytest

from celery import Celery


@pytest.fixture
def celery_app(request, app, celery_app, app_request):
    from pyramid_celery import celery_app as pyramid_celery_app

    # celery_app.conf.update(task_always_eager=True)
    # celery_app.conf.update({'PYRAMID_REQUEST': app_request})
    # import pytest; pytest.set_trace()

    pyramid_celery_app.conf.update(celery_app.conf)
    pyramid_celery_app.conf.update({"PYRAMID_REQUEST": app_request})

    return pyramid_celery_app


@pytest.fixture
def setup_celery_app(celery_setup_config: dict, celery_setup_name: str) -> Celery:  # type: ignore
    import pytest

    pytest.set_trace()
    yield celery_app
