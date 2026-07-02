import pytest
from datetime import datetime
from typing import Any
from playwright.sync_api import Response
from pathlib import Path
from helpers import MSK_TIMEZONE
from jinja2 import Environment, FileSystemLoader
from dataclasses import dataclass, asdict
import allure


# TODO: Сделать свой вариант
# from shlex import quote

# def to_curl(request, compressed=False, verify=True, pretty=False):
#     """
#     Returns a string with a curl command that makes the same HTTP request as
#     the provided request object.

#     Parameters
#     ----------
#     compressed : bool
#         If `True` then a `--compressed` argument will be added to the result
#     verify : bool
#         If `False` then a `--insecure` argument will be added to the result,
#         disabling TLS certificate verification
#     """
#     command = []

#     inferred_method = 'GET'
#     if request.body is not None:
#         inferred_method = 'POST'
#     if request.method != inferred_method:
#         command.append('-X ' + quote(request.method))

#     for k, v in request.headers.items():
#         if v:
#             command.append('-H ' + quote('{0}: {1}'.format(k, v)))
#         else:
#             # -H 'Accept:' disables sending the Accept header, use semicolon to send
#             # empty header
#             command.append('-H ' + quote('{0};'.format(k)))

#     if request.body:
#         body = request.body
#         if isinstance(body, bytes):
#             body = body.decode('utf-8')
#         data_type = '-d'
#         if body.startswith('@'):  # -d @filename causes curl to read from file
#             data_type = '--data-raw'
#         command.append(data_type + ' ' + quote(body))

#     if compressed:
#         command.append('--compressed')

#     if not verify:
#         command.append('--insecure')

#     command.append(quote(request.url))

#     joiner = ' '
#     if pretty and len(command) > 3:
#         joiner = ' \\\n  '
#     return 'curl ' + joiner.join(command)


# TODO: Заиспользовать что то такого плана для подсветки json
# <link href="path/to/prettify.css" type="text/css" rel="stylesheet" />
# <script src="path/to/prettify.js"></script>

# <script>
#   document.addEventListener('DOMContentLoaded', PR.prettyPrint);
# </script>

# <pre class="prettyprint">${JSON.stringify(jsonData, null, 2)}</pre>


@dataclass
class NetworkRequest:
    url: str
    method: str
    request_headers: dict[str, str] | None
    request_body: str | None
    response_body: Any | None
    response_headers: dict[str, str] | None
    status: int
    # TODO: Сделать тип для этого.
    # Contains the request's resource type as it was perceived by the rendering engine. ResourceType will be one of the
    # following: `document`, `stylesheet`, `image`, `media`, `font`, `script`, `texttrack`, `xhr`, `fetch`,
    # `eventsource`, `websocket`, `manifest`, `other`.
    resource_type: str


def create_html_network_report(responses: list[NetworkRequest]):
    templates_path = Path(__file__).parent / "templates"
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template("network_report.html")

    return template.render(
        generation_time=datetime.now(MSK_TIMEZONE).strftime("%Y-%m-%d %H:%M:%S"),
        responses=responses,
    )


def attach_network_to_allure(responses: list[NetworkRequest]):
    network_html_report = create_html_network_report(responses)
    allure.attach(
        network_html_report,
        name="network_report",
        attachment_type=allure.attachment_type.HTML,
    )


@pytest.fixture(scope="function", autouse=True)
def capture_network(page):
    responses = []

    def on_response(response: Response):
        if (
            "application/json" in response.headers.get("content-type", "")
            and response.status >= 400
        ):
            try:
                request_body = response.request.post_data_json
                response_body = response.json()
            except Exception:
                request_body = response_body = None
            request_headers = dict(response.request.headers)
            response_headers = dict(response.headers)
        else:
            request_body = response_body = request_headers = response_headers = None

        responses.append(
            asdict(
                NetworkRequest(
                    url=response.request.url,
                    method=response.request.method,
                    request_headers=request_headers,
                    response_headers=response_headers,
                    request_body=request_body,
                    response_body=response_body,
                    status=response.status,
                    resource_type=response.request.resource_type,
                )
            )
        )

    page.on("response", on_response)

    yield responses

    attach_network_to_allure(responses)
