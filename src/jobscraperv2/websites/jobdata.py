# Author: Olin Gallet
# Date: 7/11/2022
#
# JobData represents a typical job posting found on a job search engine.  It contains
# information about the company, title, description, link, and location to the post.

class JobData:
    def __init__(self, company:str, title:str, description:str, link:str, location:str):
        ''' Constructs a new JobData

        :param: company the name of the job company
        :type: str

        :param: title the job's title
        :type: str

        :param: description the job's description
        :type: str

        :param link the job's link
        :type: str

        :param link the job's location
        :type: str
        '''
        self._company = company
        self._title = title
        self._description = description
        self._link = link
        self._location = location

    def get_company(self) -> str:
        ''' Gets the job's company name.

        :return: the job's company name
        :rtype: str
        '''
        return self._company
    
    def get_title(self) -> str:
        ''' Gets the job title.

        :return: the job's title
        :rtype: str
        '''
        return self._title

    def get_description(self) -> str:
        ''' Gets the job's description.

        :return: the job's description
        :rtype: str
        '''
        return self._description

    def get_link(self) -> str:
        ''' Gets the job's link.

        :return: the job's link
        :rtype: str
        '''
        return self._link
    
    def get_location(self) -> str:
        ''' Gets the job's location.

        :return: the job's location
        :rtype: str
        '''
        return self._location