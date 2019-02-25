
import uuid

from cloudify import ctx, utils
from fabric.api import put, run, sudo

CONFIG_PATH = '/etc/haproxy/haproxy.cfg'
NEW_CONFIG_PATH = 'resources/haproxy.cfg'


def configure():
    ctx.logger.info('Configuring HAProxy')
    haproxy_config = ctx.download_resource(NEW_CONFIG_PATH)
    tmpfile = '/tmp/haproxy_{0}.cfg'.format(uuid.uuid4())
    put(haproxy_config, tmpfile)
    ctx.logger.info('Validating the given HAProxy configuration file')
    run('/usr/sbin/haproxy -f {0} -c'.format(tmpfile))
    ctx.logger.info('Copying the configuration file to {0}'
                    .format(CONFIG_PATH))
    sudo('mv {0} {1}'.format(tmpfile, CONFIG_PATH))
    ctx.logger.info('Restarting HAProxy service')
    sudo('service haproxy restart')
    ctx.logger.info('HAProxy was configured successfully')
