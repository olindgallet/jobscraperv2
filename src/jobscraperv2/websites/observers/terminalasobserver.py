# Author: Olin Gallet
# Date: 11/11/2022
#
# The TerminalAsObserver displays output to the terminal in a quick, colorful format
# for reviewing results. 
#

import time
from plumbum import colors
from .observerinterface import ObserverInterface
from ..jobdata import JobData

class TerminalAsObserver(ObserverInterface):
    def __init__(self):
        pass

    async def notify(self, job_data:JobData):
        print(colors.yellow | '[' +  time.strftime('%H:%M:%S' + ']'))
        print(colors.orchid | job_data.get_company())
        print(colors.yellow | job_data.get_title())
        print(colors.blue | job_data.get_link())
        print()
