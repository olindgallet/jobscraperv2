# Author: Olin Gallet
# Date: 8/11/2022
#
# The ObserverInterface is to be implemented by all potential observers
# that want to be notified when new job data is scraped.  

from abc import ABC, abstractmethod
from ..jobdata import JobData

class ObserverInterface(ABC):
    def __init__(self):
        pass

    @abstractmethod
    async def notify(self, job_data:JobData):
        pass