# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetApplicationResult:
    """
    A collection of values returned by getApplication.
    """
    def __init__(__self__, host_ids=None, instance_ids=None, name=None, id=None):
        if host_ids and not isinstance(host_ids, list):
            raise TypeError("Expected argument 'host_ids' to be a list")
        __self__.host_ids = host_ids
        """
        A list of host IDs associated with the application.
        """
        if instance_ids and not isinstance(instance_ids, list):
            raise TypeError("Expected argument 'instance_ids' to be a list")
        __self__.instance_ids = instance_ids
        """
        A list of instance IDs associated with the application.
        """
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        __self__.name = name
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetApplicationResult(GetApplicationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApplicationResult(
            host_ids=self.host_ids,
            instance_ids=self.instance_ids,
            name=self.name,
            id=self.id)

def get_application(name=None,opts=None):
    """
    Use this data source to access information about an existing resource.
    
    :param str name: The name of the application in New Relic.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-newrelic/blob/master/website/docs/d/application.html.markdown.
    """
    __args__ = dict()

    __args__['name'] = name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('newrelic:index/getApplication:getApplication', __args__, opts=opts).value

    return AwaitableGetApplicationResult(
        host_ids=__ret__.get('hostIds'),
        instance_ids=__ret__.get('instanceIds'),
        name=__ret__.get('name'),
        id=__ret__.get('id'))
