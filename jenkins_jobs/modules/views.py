# Copyright 2012 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


"""
The Views module supplies a wide range of options that are
implemented as Jenkins views.

**Component**: views
  :Macro: property
  :Entry Point: jenkins_jobs.views

Example::

  job:
    name: test_job

    views:
      - delivery-pipeline-view:
          name: CI/CD
"""


import xml.etree.ElementTree as XML
import jenkins_jobs.modules.base
from jenkins_jobs.errors import JenkinsJobsException
import logging

logger = logging.getLogger(__name__)


def delivery_pipeline(parser, xml_parent, data):
    """yaml: delivery-pipeline

    name
    no-of-pipelines
    show-aggregated-pipeline
    no-of-columns
    sorting:
        none
        se.diabol.jenkins.pipeline.sort.NameComparator
        se.diabol.jenkins.pipeline.sort.LatestActivityComparator
    update-interval
    show-avatars
    show-changes
    show-total-build-time
    allow-manual-triggers
    allow-rebuild
    allow-pipeline-start
    component-name
    component-first-job

    Example:

    .. literalinclude:: /../../tests/builders/fixtures/views001.yaml
       :language: yaml

    """
    delivery = XML.SubElement(xml_parent, 'se.diabol.jenkins.pipeline'
                           '.DeliveryPipelineView')
    component = XML.SubElement(delivery, 'componentSpecs')
    spec = XML.SubElement(component, 'se.diabol.jenkins'
                          '.pipeline'
                          '.DeliveryPipelineView_-ComponentSpec')

    settings = [
        ('name', 'name', ''),
        ('filter-executors', 'filterExecutors', False),
        ('filter-queue', 'filterQueue', False),
        ('no-of-pipelines', 'noOfPipelines', '3'),
        ('show-aggregated-pipeline', 'showAggregatedPipeline', False),
        ('no-of-columns', 'noOfColumns', '3'),
        ('sorting', 'sorting', 'none'),
        ('show-avatars', 'showAvatars', False),
        ('update-interval', 'updateInterval', '10'),
        ('show-changes', 'showChanges', False),
        ('allow-manual-triggers', 'allowManualTriggers', False),
        ('show-total-build-time', 'showTotalBuildTime', False),
        ('allow-rebuild', 'allowRebuild', False),
        ('allow-pipeline-start', 'allowPipelineStart', False),
        ('regexp-first-jobs', 'regexpFirstJobs', ''),
        ('component-name', 'name', ''),
        ('component-first-job', 'firstJob', '')
        ]

    for key, tag_name, default in settings:
        xml_config = XML.SubElement(delivery, tag_name)
        config_value = data.get(key, default)

        if key in ('component-name', 'component-first-job'):
            xml_config = XML.SubElement(spec, tag_name)
            xml_config.text = str(config_value)
        else:
            if isinstance(default, bool):
                xml_config.text = str(config_value).lower()
            else:
                xml_config.text = str(config_value)


class Views(jenkins_jobs.modules.base.Base):
    sequence = 30

    component_type = 'views'
    component_list_type = 'views'

    def gen_xml(self, parser, xml_parent, data):
        properties = xml_parent.find('views')
        if properties is None:
            properties = XML.SubElement(xml_parent, 'views')

        for prop in data.get('views', []):
            self.registry.dispatch('views', parser, properties, prop)