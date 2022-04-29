"""
ZMQ-specific functions
"""

import logging

from salt.exceptions import SaltSystemExit

log = logging.getLogger(__name__)

try:
    import zmq
except ImportError:
    zmq = None
    log.debug("ZMQ module is not found")

ZMQDefaultLoop = None
ZMQ_VERSION_INFO = (-1, -1, -1)
LIBZMQ_VERSION_INFO = (-1, -1, -1)

try:
    if zmq:
        ZMQ_VERSION_INFO = tuple(int(v_el) for v_el in zmq.__version__.split("."))
        LIBZMQ_VERSION_INFO = tuple(int(v_el) for v_el in zmq.zmq_version().split("."))
except Exception:  # pylint: disable=broad-except
    log.exception("Error while getting LibZMQ/PyZMQ library version")


def check_ipc_path_max_len(uri):
    # The socket path is limited to 107 characters on Solaris and
    # Linux, and 103 characters on BSD-based systems.
    if zmq is None:
        return
    ipc_path_max_len = getattr(zmq, "IPC_PATH_MAX_LEN", 103)
    if ipc_path_max_len and len(uri) > ipc_path_max_len:
        raise SaltSystemExit(
            "The socket path is longer than allowed by OS. "
            "'{}' is longer than {} characters. "
            "Either try to reduce the length of this setting's "
            "path or switch to TCP; in the configuration file, "
            'set "ipc_mode: tcp".'.format(uri, ipc_path_max_len)
        )
