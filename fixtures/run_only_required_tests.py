import pytest
from dotenv import load_dotenv
import os
from pytest import FixtureRequest


SUPPORTED_ENVS = ["dev", "prod", "stage"]


@pytest.fixture(scope="session", autouse=True)
def load_env(request: FixtureRequest):
    env = request.config.getoption("--env")

    env_file = f"env/.env.{env}"

    if os.path.exists(env_file):
        load_dotenv(env_file)

    else:
        raise FileNotFoundError(f"Env файл {env_file} не найден")


def pytest_addoption(parser):
    parser.addoption(
        "--env",
        action="store",
        default="prod",
        help="Переменная для запуска тестов на разных окружениях: dev, prod, stage",
    )


#     parser.addoption(
#         "--page",
#         action="store",
#         default=None,
#         help="Запускаем тесты для определенной страницы: ...",
#     )


# def pytest_collection_modifyitems(config, items):
#     current_env = config.getoption("--env")

#     skip_markers = {}

#     for env in SUPPORTED_ENVS:
#         if env != current_env:
#             skip_markers[env] = pytest.mark.skip(
#                 reason=f"Test requires --env={env}, current is --env={current_env}"
#             )

#     for item in items:
#         for env in SUPPORTED_ENVS:
#             if item.get_closest_marker(env) and env != current_env:
#                 item.add_marker(skip_markers[env])

#     requested = config.getoption("--page")
#     if not requested:
#         return

#     reason = f"Test does not use fixture '{requested}' (--page={requested})"
#     for item in items:
#         if requested not in _get_used_fixtures(item):
#             item.add_marker(pytest.mark.skip(reason=reason))


# def _get_used_fixtures(item) -> set[str]:
#     fixtures = set(item.fixturenames)
#     marker = item.get_closest_marker("usefixtures")
#     if marker:
#         for arg in marker.args:
#             fixtures.update(f.strip() for f in arg.split(",") if f.strip())
#     return fixtures
