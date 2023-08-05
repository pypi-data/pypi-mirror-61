# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Monitor(pulumi.CustomResource):
    bypass_head_request: pulumi.Output[bool]
    """
    Bypass HEAD request.
    """
    frequency: pulumi.Output[float]
    """
    The interval (in minutes) at which this monitor should run.
    """
    locations: pulumi.Output[list]
    """
    The locations in which this monitor should be run.
    """
    name: pulumi.Output[str]
    """
    The title of this monitor.
    """
    sla_threshold: pulumi.Output[float]
    """
    The base threshold for the SLA report.
    """
    status: pulumi.Output[str]
    """
    The monitor status (i.e. `ENABLED`, `MUTED`, `DISABLED`)
    """
    treat_redirect_as_failure: pulumi.Output[bool]
    """
    Fail the monitor check if redirected.
    """
    type: pulumi.Output[str]
    """
    The monitor type. Valid values are `SIMPLE`, `BROWSER`, `SCRIPT_BROWSER`, and `SCRIPT_API`.
    """
    uri: pulumi.Output[str]
    """
    The URI for the monitor to hit.
    """
    validation_string: pulumi.Output[str]
    """
    The string to validate against in the response.
    """
    verify_ssl: pulumi.Output[bool]
    """
    Verify SSL.
    """
    def __init__(__self__, resource_name, opts=None, bypass_head_request=None, frequency=None, locations=None, name=None, sla_threshold=None, status=None, treat_redirect_as_failure=None, type=None, uri=None, validation_string=None, verify_ssl=None, __props__=None, __name__=None, __opts__=None):
        """
        Use this resource to create, update, and delete a synthetics monitor in New Relic.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] bypass_head_request: Bypass HEAD request.
        :param pulumi.Input[float] frequency: The interval (in minutes) at which this monitor should run.
        :param pulumi.Input[list] locations: The locations in which this monitor should be run.
        :param pulumi.Input[str] name: The title of this monitor.
        :param pulumi.Input[float] sla_threshold: The base threshold for the SLA report.
        :param pulumi.Input[str] status: The monitor status (i.e. `ENABLED`, `MUTED`, `DISABLED`)
        :param pulumi.Input[bool] treat_redirect_as_failure: Fail the monitor check if redirected.
        :param pulumi.Input[str] type: The monitor type. Valid values are `SIMPLE`, `BROWSER`, `SCRIPT_BROWSER`, and `SCRIPT_API`.
        :param pulumi.Input[str] uri: The URI for the monitor to hit.
        :param pulumi.Input[str] validation_string: The string to validate against in the response.
        :param pulumi.Input[bool] verify_ssl: Verify SSL.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-newrelic/blob/master/website/docs/r/synthetics_monitor.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['bypass_head_request'] = bypass_head_request
            if frequency is None:
                raise TypeError("Missing required property 'frequency'")
            __props__['frequency'] = frequency
            if locations is None:
                raise TypeError("Missing required property 'locations'")
            __props__['locations'] = locations
            __props__['name'] = name
            __props__['sla_threshold'] = sla_threshold
            if status is None:
                raise TypeError("Missing required property 'status'")
            __props__['status'] = status
            __props__['treat_redirect_as_failure'] = treat_redirect_as_failure
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
            __props__['uri'] = uri
            __props__['validation_string'] = validation_string
            __props__['verify_ssl'] = verify_ssl
        super(Monitor, __self__).__init__(
            'newrelic:synthetics/monitor:Monitor',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, bypass_head_request=None, frequency=None, locations=None, name=None, sla_threshold=None, status=None, treat_redirect_as_failure=None, type=None, uri=None, validation_string=None, verify_ssl=None):
        """
        Get an existing Monitor resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] bypass_head_request: Bypass HEAD request.
        :param pulumi.Input[float] frequency: The interval (in minutes) at which this monitor should run.
        :param pulumi.Input[list] locations: The locations in which this monitor should be run.
        :param pulumi.Input[str] name: The title of this monitor.
        :param pulumi.Input[float] sla_threshold: The base threshold for the SLA report.
        :param pulumi.Input[str] status: The monitor status (i.e. `ENABLED`, `MUTED`, `DISABLED`)
        :param pulumi.Input[bool] treat_redirect_as_failure: Fail the monitor check if redirected.
        :param pulumi.Input[str] type: The monitor type. Valid values are `SIMPLE`, `BROWSER`, `SCRIPT_BROWSER`, and `SCRIPT_API`.
        :param pulumi.Input[str] uri: The URI for the monitor to hit.
        :param pulumi.Input[str] validation_string: The string to validate against in the response.
        :param pulumi.Input[bool] verify_ssl: Verify SSL.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-newrelic/blob/master/website/docs/r/synthetics_monitor.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["bypass_head_request"] = bypass_head_request
        __props__["frequency"] = frequency
        __props__["locations"] = locations
        __props__["name"] = name
        __props__["sla_threshold"] = sla_threshold
        __props__["status"] = status
        __props__["treat_redirect_as_failure"] = treat_redirect_as_failure
        __props__["type"] = type
        __props__["uri"] = uri
        __props__["validation_string"] = validation_string
        __props__["verify_ssl"] = verify_ssl
        return Monitor(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

