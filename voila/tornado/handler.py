#############################################################################
# Copyright (c) 2018, Voilà Contributors                                    #
# Copyright (c) 2018, QuantStack                                            #
#                                                                           #
# Distributed under the terms of the BSD 3-Clause License.                  #
#                                                                           #
# The full license is in the file LICENSE, distributed with this software.  #
#############################################################################
from aiologger import Logger
import logging
import tornado.web
from ..handler import VoilaHandler

#-----------------------------------------------------------------------------#
#logging
AsyncLogger = Logger.with_default_handlers(
    name=__name__,
    level=logging.DEBUG
)
#-----------------------------------------------------------------------------#

class TornadoVoilaHandler(VoilaHandler):
    
    cached_gen = {}
    
    @tornado.web.authenticated
    async def get(self, path=None):
              
        _key    = ''        #FIXME
        _async  = False

        #
        try:gen = self.cached_gen[_key]
        except KeyError:
            self.cached_gen[_key] = _gen = []
            _async      = True
            gen         = self.get_generator(path=path)
        
        #
        await AsyncLogger.info(
            f'{self.__class__.__name__}:'
            + f'rendring using {_async=} gen'
            )
        
        #
        if _async:           
            async for html in gen:
                self.write(html)
                _gen.append(html)
                self.flush()

        #
        else:           
            for html in gen:
                self.write(html)
                self.flush()

