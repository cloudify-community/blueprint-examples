import os
import signal

from cloudify import ctx

# Here, we read the `pid` runtime property which we previously
# saved when running `install.py`
pid = ctx.instance.runtime_properties['pid']
ctx.logger.info('Running process PID: {0}'.format(pid))
try:
    os.kill(pid, signal.SIGTERM)
    ctx.logger.info('Python Webserver Terminated!')
except:
    ctx.logger.info('Webserver not running.')
