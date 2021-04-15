# from gevent import monkey
#
# monkey.patch_all()
# import psycopg2
# from psycopg2 import extensions
# from gevent._socketcommon import wait_read, wait_write
#
#
# def patch_psycopg():
#     """Configure Psycopg to be used with gevent in non-blocking way."""
#     if not hasattr(extensions, "set_wait_callback"):
#         raise ImportError(
#             "support for coroutines not available in this Psycopg version (%s)"
#             % psycopg2.__version__
#         )
#
#     extensions.set_wait_callback(gevent_wait_callback)
#
#
# def gevent_wait_callback(conn, timeout=None):
#     """A wait callback useful to allow gevent to work with Psycopg."""
#     while 1:
#         state = conn.poll()
#         if state == extensions.POLL_OK:
#             break
#         elif state == extensions.POLL_READ:
#             wait_read(conn.fileno(), timeout=timeout)
#         elif state == extensions.POLL_WRITE:
#             wait_write(conn.fileno(), timeout=timeout)
#         else:
#             raise psycopg2.OperationalError("Bad result from poll: %r" % state)
#
#
# def post_fork(server, worker):
#     patch_psycopg()
#     worker.log.info("Made Psycopg2 Green")


import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lightning_plus.settings.local")

application = get_wsgi_application()
