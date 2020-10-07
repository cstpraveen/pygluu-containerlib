import os

from pygluu.containerlib.persistence.couchbase import (  # noqa: F401
    render_couchbase_properties,
    sync_couchbase_truststore,
)
from pygluu.containerlib.persistence.hybrid import render_hybrid_properties  # noqa: F401
from pygluu.containerlib.persistence.ldap import (  # noqa: F401
    render_ldap_properties,
    sync_ldap_truststore,
)


def render_salt(manager, src: str, dest: str) -> None:
    """Render file contains salt string, i.e. ``/etc/gluu/conf/salt``.

    The generated file has the following contents:

    .. code-block:: text

        encode_salt = random-salt-string

    :params manager: An instance of :class:`~pygluu.containerlib.manager._Manager`.
    :params src: Absolute path to the template.
    :params dest: Absolute path where generated file is located.
    """
    encode_salt = manager.secret.get("encoded_salt")

    with open(src) as f:
        txt = f.read()

    with open(dest, "w") as f:
        rendered_txt = txt % {"encode_salt": encode_salt}
        f.write(rendered_txt)


def render_gluu_properties(src: str, dest: str) -> None:
    """Render file contains properties for Gluu Server,
    i.e. ``/etc/gluu/conf/gluu.properties``.

    :params src: Absolute path to the template.
    :params dest: Absolute path where generated file is located.
    """
    with open(src) as f:
        txt = f.read()

    with open(dest, "w") as f:
        rendered_txt = txt % {
            "gluuOptPythonFolder": "/opt/gluu/python",
            "certFolder": "/etc/certs",
            "persistence_type": os.environ.get("GLUU_PERSISTENCE_TYPE", "ldap"),
        }
        f.write(rendered_txt)
