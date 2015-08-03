FROM otechlabs/base:latest

MAINTAINER Dawid Malinowski <d.malinowski@oberthur.com>

WORKDIR /opt

RUN apt-get update \
    && apt-get install --yes --force-yes python-setuptools python-dev libyaml-dev git \
    # install python deps
    && easy_install pip \
    && pip install PyYAML \
    && pip install six pbr

RUN mkdir /opt/jenkins-job-builder
ADD . /opt/jenkins-job-builder

RUN cd /opt/jenkins-job-builder && python setup.py install \
    # override python-jenkins with develop version
    && cd /opt \
    && git clone https://github.com/oberthur/python-jenkins \
    && cd python-jenkins \
    && git checkout master \
    && python setup.py install

# clean all cache to clean space
RUN apt-get -qqy purge git \
    && rm -rf /var/lib/apt/lists/* \
    && rm -fr /opt/jenkins-job-builder \
    && rm -fr /opt/python-jenkins \
    && apt-get -qqy autoremove \
    && apt-get clean

ENTRYPOINT ["/usr/local/bin/jenkins-jobs"]
