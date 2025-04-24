from aiologger import Logger
import logging
import tornado
from jupyter_server.base.handlers import APIHandler
from jupyter_core.utils import ensure_async

#-----------------------------------------------------------------------------#
#logging
AsyncLogger = Logger.with_default_handlers(
    name=__name__,
    level=logging.DEBUG
)
#-----------------------------------------------------------------------------#

class VoilaShutdownKernelHandler(APIHandler):
    """Handler to shut down kernel on page's `beforeunload` event."""

    @tornado.web.authenticated
    async def post(self, kernel_id):
        
        await AsyncLogger.info(
            f'{self.__class__.__name__}:'
            + 'override'
            + f' {self.request=}'
            + f' {kernel_id=}'
            )

        return #FIXME

        await ensure_async(self.kernel_manager.shutdown_kernel(kernel_id))
        self.set_status(204)
        self.finish()
