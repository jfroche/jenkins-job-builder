# Copyright 2015 Openstack Foundation

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
The view pipeline module handles creating Jenkins Build Pipeline views.
To create a list view specify ``list`` in the ``view-type`` attribute
to the :ref:`View-pipeline` definition.
Requires the Jenkins
:jenkins-wiki:`Build Pipeline Plugin <build+pipeline+plugin>`.

:View Parameters:
    * **name** (`str`): The name of the view.
    * **view-type** (`str`): The type of view.
    * **description** (`str`): A description of the view. (optional)
    * **filter-executors** (`bool`): Show only executors that can
      execute the included views. (default false)
    * **filter-queue** (`bool`): Show only included jobs in builder
      queue. (default false)
    * **first-job** (`str`): Parent Job in the view.
    * **no-of-displayed-builds** (`str`): Number of builds to display.
      (default 1)
    * **title** (`str`): Build view title. (optional)
    * **linkStyle** (`str`): Console output link style. Can be
      'Lightbox', 'New Window', or 'This Window'. (default Lightbox)
    * **css-Url** (`str`): Url for Custom CSS files (optional)
    * **latest-job-only** (`bool`) Trigger only latest job.
      (default false)
    * **manual-trigger** (`bool`) Always allow manual trigger.
      (default false)
    * **show-parameters** (`bool`) Show pipeline parameters.
      (default false)
    * **parameters-in-headers** (`bool`) Show pipeline parameters in
      headers. (default false)
    * **starts-with-parameters** (`bool`) Use Starts with parameters.
      (default false)
    * **refresh-frequency** (`str`) Frequency to refresh in seconds.
      (default '3')
    * **definition-header** (`bool`) Show pipeline definition header.
      (default false)

Example:

    .. literalinclude::
        /../../tests/view_pipeline/fixtures/pipeline_view001.yaml

Example:

    .. literalinclude::
        /../../tests/view_pipeline/fixtures/pipeline_view002.yaml
"""


import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base


class BuildPipeline(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        linktypes = ['Lightbox', 'New Window']
        root = XML.Element('au.com.centrumsystems.hudson.'
                           'plugin.buildpipeline.BuildPipelineView',
                           {'plugin': 'build-pipeline-plugin@1.4.3'})
        XML.SubElement(root, 'name').text = data['name']
        desc_text = data.get('description', None)
        if desc_text is not None:
            XML.SubElement(root, 'description').text = desc_text

        filterExecutors = data.get('filter-executors', False)
        FE_element = XML.SubElement(root, 'filterExecutors')
        FE_element.text = str(filterExecutors).lower()

        filterQueue = data.get('filter-queue', False)
        FQ_element = XML.SubElement(root, 'filterQueue')
        FQ_element.text = str(filterQueue).lower()

        XML.SubElement(root, 'properties',
                       {'class': 'hudson.model.View$PropertyList'})

        GBurl = ('au.com.centrumsystems.hudson.plugin.buildpipeline.'
                 'DownstreamProjectGridBuilder')
        gridBuilder = XML.SubElement(root, 'gridBuilder', {'class': GBurl})

        jobname = data.get('first-job', '')
        XML.SubElement(gridBuilder, 'firstJob').text = jobname

        builds = str(data.get('no-of-displayed-builds', 1))
        XML.SubElement(root, 'noOfDisplayedBuilds').text = builds

        title = data.get('title', None)
        BVT_element = XML.SubElement(root, 'buildViewTitle')
        if title is not None:
            BVT_element.text = title

        linkStyle = data.get('link-style', 'Lightbox')
        LS_element = XML.SubElement(root, 'consoleOutputLinkStyle')
        if linkStyle in linktypes:
            LS_element.text = linkStyle
        else:
            LS_element.text = 'Lightbox'

        cssUrl = data.get('css-Url', None)
        CU_element = XML.SubElement(root, 'cssUrl')
        if cssUrl is not None:
            CU_element.text = cssUrl

        latest_job_only = data.get('latest-job-only', False)
        OLJ_element = XML.SubElement(root, 'triggerOnlyLatestJob')
        OLJ_element.text = str(latest_job_only).lower()

        manual_trigger = data.get('manual-trigger', False)
        AMT_element = XML.SubElement(root, 'alwaysAllowManualTrigger')
        AMT_element.text = str(manual_trigger).lower()

        show_parameters = data.get('show-parameters', False)
        PP_element = XML.SubElement(root, 'showPipelineParameters')
        PP_element.text = str(show_parameters).lower()

        parameters_in_headers = data.get('parameters-in-headers', False)
        PIH_element = XML.SubElement(root, 'showPipelineParametersInHeaders')
        PIH_element.text = str(parameters_in_headers).lower()

        start_with_parameters = data.get('start-with-parameters', False)
        SWP_element = XML.SubElement(root, 'startsWithParameters')
        SWP_element.text = str(start_with_parameters).lower()

        refresh_frequency = str(data.get('refresh-frequency', 3))
        XML.SubElement(root, 'refreshFrequency').text = refresh_frequency

        headers = data.get('definition-header', False)
        DH_element = XML.SubElement(root, 'showPipelineDefinitionHeader')
        DH_element.text = str(headers).lower()

        return root


class DeliveryPipeline(jenkins_jobs.modules.base.Base):
    sequence = 0

    def root_xml(self, data):
        linktypes = ['Lightbox', 'New Window']
        root = XML.Element('se.diabol.jenkins.pipeline.DeliveryPipelineView',
                           {'plugin': 'delivery-pipeline-plugin'})
        XML.SubElement(root, 'name').text = data['name']
        desc_text = data.get('description', None)
        if desc_text is not None:
            XML.SubElement(root, 'description').text = desc_text

        filterExecutors = data.get('filter-executors', False)
        XML.SubElement(root, 'filterExecutors').text = str(filterExecutors).lower()

        filterQueue = data.get('filter-queue', False)
        XML.SubElement(root, 'filterQueue').text = str(filterQueue).lower()

        XML.SubElement(root, 'properties',
                       {'class': 'hudson.model.View$PropertyList'})

        CS = XML.SubElement(root, 'componentSpec')
        Specs = XML.SubElement(CS, 'se.diabol.jenkins.pipeline.DeliveryPipelineView_-ComponentSpec')

        viewname = data.get('name', '')
        XML.SubElement(CS,'name').text = viewname

        firstjobname = data.get('first-job', '')
        XML.SubElement(CS, 'firstJob').text = firstjobname

        lastjobname = data.get('last-job', '')
        XML.SubElement(CS,'lastJob').text = lastjobname

        pipelines = str(data.get('no-of-pipelines', '3'))
        XML.SubElement(root, 'noOfPipelines').text = pipelines

        showAggregatedPipe = str(data.get('show-aggregated-pipeline', False))
        XML.SubElement(root,'showAggregatedPipeline').text = str(showAggregatedPipe).lower()

        noofcolumns = str(data.get('no-of-columns', '1'))
        XML.SubElement(root,'noOfColumns').text=noofcolumns

        sorting = str(data.get('sorting', 'none'))
        XML.SubElement(root,'sorting').text = str(sorting)

        showavatars = str(data.get('show-avatars', False))
        XML.SubElement(root,'showAvatars').text = str(showavatars).lower()

        updateinterval = str(data.get('update-interval', '10'))
        XML.SubElement(root,'updateInterval').text = updateinterval

        showchanges = str(data.get('show-changes', False))
        XML.SubElement(root,'showChanges').text = str(showchanges).lower()

        allowmanualtrig = str(data.get('allow-manual-triggers', False))
        XML.SubElement(root,'allowManualTriggers').text = str(allowmanualtrig).lower()

        showtotalbuildt = str(data.get('show-total-build-time', False))
        XML.SubElement(root,'showTotalBuildTime').text = str(showtotalbuildt).lower()

        allowrebuild = str(data.get('allow-rebuild', False))
        XML.SubElement(root,'allowRebuild').text = str(allowrebuild).lower()

        allowpipestart = str(data.get('allow-pipeline-start', False))
        XML.SubElement(root,'allowPipelineStart').text = str(allowpipestart).lower()

        showdesc = str(data.get('show-description', False))
        XML.SubElement(root,'showDescription').text = str(showdesc).lower()

        showpromo = str(data.get('show-promotions', False))
        XML.SubElement(root,'showPromotions').text = str(showpromo).lower()

        showtestresult = str(data.get('show-test-results', False))
        XML.SubElement(root,'showTestResults').text = str(showtestresult).lower()

        showstaticanal = str(data.get('show-static-analysis-results', False))
        XML.SubElement(root,'showStaticAnalysisResults').text = str(showstaticanal).lower()

        regexpfirstjob = str(data.get('first-job-regexp'))
        XML.SubElement(root,'regexpFirstJobs').text = regexpfirstjob

        xml_jobs = XML.SubElement(root, 'regexpFirstJobs')
        jobs = data.get('regexp-first-jobs', [])
        for job in jobs:
            xml_job = XML.SubElement(xml_jobs, 'se.diabol.jenkins.pipeline.'
                                           'DeliveryPipelineView_-RegExpSpec')
            XML.SubElement(xml_job, 'regexp').text = job

        return root
