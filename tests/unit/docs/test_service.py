# Copyright 2015 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
# http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
import os

from tests.unit.docs import BaseDocsTest
from boto3.docs.service import ServiceDocumenter


class TestServiceDocumenter(BaseDocsTest):
    def test_document_service(self):
        service_documenter = ServiceDocumenter('myservice', self.session)
        contents = service_documenter.document_service().decode('utf-8')
        lines = [
            '*********',
            'MyService',
            '*********',
            '.. contents:: Table of Contents',
            '   :depth: 2',
            '======',
            'Client',
            '======',
            '.. py:class:: MyService.Client',
            '  These are the available methods:',
            '  *   :py:meth:`sample_operation`',
            '==========',
            'Paginators',
            '==========',
            'The available paginators are:',
            '* :py:class:`MyService.Paginator.SampleOperation`',
            '.. py:class:: MyService.Paginator.SampleOperation',
            '  .. py:method:: paginate(**kwargs)',
            '=======',
            'Waiters',
            '=======',
            'The available waiters are:',
            '* :py:class:`MyService.Waiter.SampleOperationComplete`',
            '.. py:class:: MyService.Waiter.SampleOperationComplete',
            '  .. py:method:: wait(**kwargs)',
            '================',
            'Service Resource',
            '================',
            '.. py:class:: MyService.ServiceResource()',
            "  These are the resource's available actions:",
            '  *   :py:meth:`sample_operation()`',
            "  These are the resource's available sub-resources:",
            '  *   :py:meth:`Sample()`',
            "  These are the resource's available collections:",
            '  *   :py:attr:`samples`',
            '  .. py:method:: sample_operation(**kwargs)',
            '  .. py:method:: Sample(name)',
            '  .. py:attribute:: samples',
            '    .. py:method:: all()',
            '    .. py:method:: filter(**kwargs)',
            '    .. py:method:: limit(**kwargs)',
            '    .. py:method:: page_size(**kwargs)',
            '======',
            'Sample',
            '======',
            '.. py:class:: MyService.Sample(name)',
            "  These are the resource's available identifiers:",
            '  *   :py:attr:`name`',
            "  These are the resource's available attributes:",
            '  *   :py:attr:`bar`',
            '  *   :py:attr:`foo`',
            "  These are the resource's available actions:",
            '  *   :py:meth:`load()`',
            '  *   :py:meth:`operate()`',
            '  *   :py:meth:`reload()`',
            "  These are the resource's available waiters:",
            '  *   :py:meth:`wait_until_complete()`',
            '  .. py:attribute:: name',
            '  .. py:attribute:: bar',
            '  .. py:attribute:: foo',
            '  .. py:method:: load()',
            '  .. py:method:: operate(**kwargs)',
            '  .. py:method:: reload()',
            '  .. py:method:: wait_until_complete(**kwargs)',
        ]
        self.assert_contains_lines_in_order(lines, contents)

    def test_document_service_no_resource(self):
        os.remove(self.resource_model_file)
        service_documenter = ServiceDocumenter('myservice', self.session)
        contents = service_documenter.document_service().decode('utf-8')
        self.assertNotIn('Service Resource', contents)

    def test_document_service_no_paginators(self):
        # Delete the resource model so that the resource is not documented
        # as it may try to look at the paginator model during documentation.
        os.remove(self.resource_model_file)
        os.remove(self.paginator_model_file)
        service_documenter = ServiceDocumenter('myservice', self.session)
        contents = service_documenter.document_service().decode('utf-8')
        self.assertNotIn('Paginators', contents)

    def test_document_service_no_waiter(self):
        # Delete the resource model so that the resource is not documented
        # as it may try to look at the waiter model during documentation.
        os.remove(self.resource_model_file)
        os.remove(self.waiter_model_file)
        service_documenter = ServiceDocumenter('myservice', self.session)
        contents = service_documenter.document_service().decode('utf-8')
        self.assertNotIn('Waiters', contents)
