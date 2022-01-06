import os, sys, requests, json, time

class NoDataSetTokenError(Exception):
    pass

class NoPhosphomaticsKey(Exception):
    pass

class Phosphomatics(object):
    '''
    Phosphomatics experiment session.

    Args:
        key (str): Phosphomatics API key. Contact the developers to obtain a key.
    '''

    def __init__(self, key = None):

        if not key:
            raise NoPhosphomaticsKey('A phosphomatics API key must be provided')

        self.key = key
        self.datasetToken = None
        self.BASE_URL = 'https://phosphomatics.com'

        self.validationRoutineExempt = [
            'startNewExperiment',
            'setDataSetToken',
            '__setDefaultDict',
            'getDataSetToken'
        ]

        self.__setDefaultDict()
        return

    def __setDefaultDict(self):
        self.default_params = {
            'datasetToken': self.getDataSetToken(), 'key': self.key, 'api': True}
        return

    def __getDefaultDict(self):
        return self.default_params

    def __addArgsToDefaultDict(self, args = None, target = None):

        data = self.__getDefaultDict()

        if args:
            data = {**data, **args}
        if target:
            data['apiFunctionTarget'] = target

        return data

    def __getattribute__(self,name):
        """
        Before any function call (except to those given in self.validationRoutineExempt,
        check that a dataset token has been acquired and is vallid
        """

        attr = object.__getattribute__(self, name)

        if hasattr(attr, '__call__') and \
                (attr.__name__ not in self.validationRoutineExempt):

            def newfunc(*args, **kwargs):

                if not self.datasetToken:
                    raise NoDataSetTokenError(
                        'No data set token is set! Run getDataSetToken() to begin a new experiment'
                    )

                result = attr(*args, **kwargs)

                return result
            return newfunc
        else:
            return attr

    def __monitorRemoteTask(self, taskID, supplemental_args = None):

        data = self.__addArgsToDefaultDict(args = {'taskID': taskID})

        if supplemental_args:
            data = {**data, **supplemental_args}

        t1 = time.time()
        url = self.BASE_URL + '/checkProcessingStatus'

        while True:
            print(
                'processing: %s s' %(
                    int(time.time() - t1)
                ), end = '\r', flush = True
            )
            time.sleep(1)

            r = requests.post(url, data = data)
            r = r.json()
            if 'processingDone' in r:
                del r['processingDone']
                try:
                    del r['container']
                except:
                    pass
                return r
        return

    def __updateGroupList(self):

        data = self.__addArgsToDefaultDict(target = 'getUserDataGroups')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)
        userDataGroups = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        self.userDataGroups = userDataGroups['userDataGroups']
        return

    def __updateSelectedGroup(self):

        return

    def setDataSetToken(self, datasetToken):
        '''
        Sets the datasetToken for a prior phosphomatics analysis.

        Args:
            datasetToken (str): An existing phosphomaitcs datasetToken
        '''
        self.datasetToken = datasetToken
        self.__setDefaultDict()
        return

    def getDataSetToken(self):
        '''
        Get the datasetToken for the current analysis.

        Returns:
            DatasetToken for the current analysis
        '''
        return self.datasetToken

    def startNewExperiment(self):
        '''
        Prepare a new experiment on the phosphomatics server and \
        obtain a valid datasetToken.

        Returns:
            DatasetToken for the current analysis

        Raises:
            Exception: Error generating datasetToken.
        '''

        url = self.BASE_URL + '/getNewDataSetToken'
        r = requests.post(url, data = { 'key': self.key })
        try:
            self.datasetToken = r.json()['datasetToken']
            self.__setDefaultDict()
        except Exception as e:
            raise Exception('Error getting data set token')
            self.datasetToken = None
        return self.getDataSetToken()

    def uploadExperimentalData(self, file):
        '''
        Upload phosphorylation site and quantitation data. Data file must be \
        in a phosphomatics-compatible format. See \
        `here <https://www.phosphomatics.com/help>`_ for details.

        Args:
            file (str): Path to experimental data file.

        Raises:
            NoDataSetTokenError: Raised if method called before a valid \
            datasetToken is obtained or set.
        '''

        if isinstance(file, str): file = open(file,'rb')

        url = self.BASE_URL + '/uploadExperimentalData'
        data = self.__getDefaultDict()
        r = requests.post(
            url, data = data, files = {'file': file}
        )
        return

    def uploadParameterSet(self, file):
        '''
        Upload phosphomatics parameter file.

        Args:
            file (str): Path to phosphomatics parameter file.

        Raises:
            NoDataSetTokenError: Raised if method called before a valid \
            datasetToken is obtained or set.
        '''

        if isinstance(file, str): file = open(file,'rb')

        url = self.BASE_URL + '/uploadParameterSet'
        data = self.__getDefaultDict()
        requests.post(
            url, data = data, files = {'file': file}
        )
        return

    def process(self):
        '''
        Run initial data processing through phosphomatics. Must be called \
        after uploading Experimental data and processing parameter files.

        Raises:
            NoDataSetTokenError: Raised if method called before a valid \
            datasetToken is obtained or set.
        '''
        url = self.BASE_URL + '/process'
        data = self.__addArgsToDefaultDict(args = { 'url': '/processSampleGroupings' })
        r = requests.post( url, data = data)

        self.__monitorRemoteTask(
            r.json()['taskID'],
            supplemental_args = {'url': '/processSampleGroupings'}
        )
        self.__updateGroupList()
        return

    def volcano(self, kwargs):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'getVolcanoPlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def getUserDataGroups (self):
        '''
        Get all data groups that have been created.

        Returns:
            List of dicts containing group information.

           Dicts have keys
             - id (int) - anidentifier for this individual data group
             - name (str) - data group name
             - selected (str) - 'true' if the data group is currently active, 'false' if not

        Raises:
            NoDataSetTokenError: Raised if method called before a valid \
            datasetToken is obtained or set.
        '''
        data = self.__addArgsToDefaultDict(args = {}, target = 'getUserDataGroups')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result['userDataGroups']

    def getActiveDataGroup (self):
        '''
        Get the currently active data group

        Returns:
            Dict containing group information for selected data group.

           Dict has keys
             - id (int) - anidentifier for this individual data group
             - name (str) - data group name
             - selected (str) - 'true' if the data group is currently active, 'false' if not

        Raises:
            NoDataSetTokenError: Raised if method called before a valid \
            datasetToken is obtained or set.
        '''
        data = self.__addArgsToDefaultDict(args = {}, target = 'getUserDataGroups')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        selected_group = [
            _ for _ in result['userDataGroups'] if _['selected'] == 'true'
        ]
        if selected_group:
            return selected_group[0]
        else:
            return None

    def setSelectedGroup (self, id = None):
        '''
        Change the currently active data group.

        Args:
            id (int): Integer id of data group to be selected.

        Raises:
            NoDataSetTokenError: Raised if method called before a valid \
            datasetToken is obtained or set.
        '''

        if not isinstance(id, int):
            return None

        data = self.__addArgsToDefaultDict(args = {'groupid': str(id)}, target = 'setSelectedGroup')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)
        return

    def makeDistributionPlot (self, sample = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeDistributionPlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeCorrelationMatrix (self, method = None, transform = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeCorrelationMatrix')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeQuantilePlot (self, container = None, sample = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeQuantilePlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeClusterMap (self, fc = None, pval = None, pvalType = None, numClusters = None, transformation = None, metric = None, method = None, container = None, targetClusters = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeClusterMap')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makePCAPlot (self, pval = None, pvalType = None, fc = None, transformation = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makePCAPlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeLDAPlot (self, pval = None, pvalType = None, fc = None, transformation = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeLDAPlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeVolcano (self, fc = None, pval = None, pvalType = None, group1 = None, group2 = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeVolcano')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeSCurve (self, group1 = None, group2 = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeSCurve')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def doKSEAAnslysis (self, group1 = None, group2 = None, networkin = None, networkinThreshold = None, mThreshold = None, pThreshold = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'doKSEAAnslysis')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makePhosphorylationNetworks (self, group1 = None, group2 = None, specificity = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makePhosphorylationNetworks')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def getEnrichmentForProteinList (self, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'getEnrichmentForProteinList')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def getSequenceAnslysis (self, displayType = None, palette = None, showN = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'getSequenceAnslysis')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeKinaseClusterMap (self, numClusters = None, transformation = None, palette = None, metric = None, method = None, specificity = None, container = None, targetClusters = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeKinaseClusterMap')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeKinaseVolcanoPlot (self, fc = None, pval = None, pvalType = None, group1 = None, group2 = None, container = None, specificity = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeKinaseVolcanoPlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeKinaseSCurve (self, group1 = None, group2 = None, specificity = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeKinaseSCurve')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def getQuantitationPlotForSelectedKinase (self, specificity = None, kinaseUPID = None, plotType = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'getQuantitationPlotForSelectedKinase')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeSubstrateCorrelationPlot (self, substrateUPID = None, position = None, residue = None, topN = None, method = None, plotType = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeSubstrateCorrelationPlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

    def makeFeatureAbundancePlot (self, substrateUPID = None, position = None, residue = None, plotType = None, container = None):
        data = self.__addArgsToDefaultDict(args = kwargs, target = 'makeFeatureAbundancePlot')
        url = self.BASE_URL + '/apiTask'
        r = requests.post( url, data = data)

        result = self.__monitorRemoteTask(
            r.json()['taskID'],
        )
        return result

