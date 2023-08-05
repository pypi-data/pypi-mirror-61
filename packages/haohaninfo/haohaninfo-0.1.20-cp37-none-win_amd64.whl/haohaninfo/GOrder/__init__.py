import platform
bit = platform.architecture()[0]

from haohaninfo.GOrder.GOGetKBar import Login,GetIndicator,GetKBar as GetHistoryKBar
if(bit == '32bit'):
    from haohaninfo.GOrder.GOCommand import GOCommand
    from haohaninfo.GOrder.GOQuote import GOQuote
    
else:
    from haohaninfo.GOrder.GOCommand64 import GOCommand
    from haohaninfo.GOrder.GOQuote64 import GOQuote