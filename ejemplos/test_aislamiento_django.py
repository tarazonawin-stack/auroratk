"""Ejemplo AuroraTK (R06, perfiles stack-python + tipo-web): aislamiento entre usuarios.

Cópialo a `tests/test_aislamiento.py` y completa las dos tablas de abajo. Usa pytest-django.
Comprueba tres cosas en TODAS las URL del proyecto, también en las que se agreguen después:
1. Sin sesión, ninguna URL responde 200 salvo las públicas declaradas.
2. Con sesión, un id ajeno responde exactamente igual (404 y el mismo contenido) que un id que no
   existe: así nadie descubre qué ids existen cambiando un número en la URL (OWASP A01).
3. Ninguna URL con id queda sin decidir: está en OWNED o en SHARED; si no, la prueba falla.

Example (R06): every URL needs login; another user's id returns the same 404 as a missing one;
every URL with an id must be listed, so a new view cannot be forgotten.
"""

import uuid
from collections.abc import Callable, Iterator
from typing import Any

import pytest
from django.urls import URLPattern, URLResolver, get_resolver, reverse

# URL públicas, por nombre (con su espacio de nombres). · Public URLs, by name.
PUBLIC_URL_NAMES = {"login", "logout", "password_reset", "admin:login"}

# Vistas de un registro con dueño: nombre → función que crea un registro de `owner`.
# Owned-record views: name → function creating a record owned by `owner`.
OWNED: dict[str, Callable[[Any], Any]] = {
    # "tickets:detail": lambda owner: Ticket.objects.create(owner=owner, title="x"),
}

# URL con id que todos los usuarios con sesión pueden ver a propósito. · Intentionally shared.
SHARED: set[str] = set()

DUMMY = {"int": 999_999, "str": "x", "slug": "x", "uuid": uuid.UUID(int=0), "path": "x"}


def url_patterns(patterns: list[Any] | None = None, ns: str = "") -> Iterator[tuple[str, URLPattern]]:
    """Every named URL of the project, with its full name (namespace:name)."""
    for item in get_resolver().url_patterns if patterns is None else patterns:
        if isinstance(item, URLResolver):
            inner = f"{ns}{item.namespace}:" if item.namespace else ns
            yield from url_patterns(item.url_patterns, inner)
        elif isinstance(item, URLPattern) and item.name:
            yield f"{ns}{item.name}", item


def dummy_kwargs(pattern: URLPattern) -> dict[str, Any]:
    converters = getattr(pattern.pattern, "converters", {})
    return {key: DUMMY.get(type(conv).__name__.removesuffix("Converter").lower(), "x")
            for key, conv in converters.items()}


@pytest.mark.django_db
def test_every_url_needs_login(client: Any) -> None:
    open_urls = []
    for name, pattern in url_patterns():
        if name in PUBLIC_URL_NAMES or name.startswith("admin:"):
            continue  # el admin de Django ya exige su propio login · Django admin has its own login
        url = reverse(name, kwargs=dummy_kwargs(pattern))
        if client.get(url).status_code == 200:
            open_urls.append(f"{name} ({url})")
    assert open_urls == [], f"Responden sin sesión · Open without login: {open_urls}"


def test_every_url_with_an_id_is_decided() -> None:
    undecided = [name for name, pattern in url_patterns()
                 if dummy_kwargs(pattern) and not name.startswith("admin:")
                 and name not in OWNED and name not in SHARED and name not in PUBLIC_URL_NAMES]
    assert undecided == [], f"Agrégalas a OWNED o SHARED · Add them to OWNED or SHARED: {undecided}"


@pytest.mark.django_db
@pytest.mark.parametrize("name", sorted(OWNED))
def test_another_users_record_looks_missing(client: Any, django_user_model: Any, name: str) -> None:
    me = django_user_model.objects.create_user(username="me", password="x-Test-1234")
    other = django_user_model.objects.create_user(username="other", password="x-Test-1234")
    theirs = OWNED[name](other)
    client.force_login(me)
    key = next(iter(dummy_kwargs(dict(url_patterns())[name])))
    foreign = client.get(reverse(name, kwargs={key: theirs.pk}))
    missing_pk = uuid.uuid4() if isinstance(theirs.pk, uuid.UUID) else 999_999_999
    missing = client.get(reverse(name, kwargs={key: missing_pk}))
    assert foreign.status_code == 404
    assert (foreign.status_code, foreign.content) == (missing.status_code, missing.content)
