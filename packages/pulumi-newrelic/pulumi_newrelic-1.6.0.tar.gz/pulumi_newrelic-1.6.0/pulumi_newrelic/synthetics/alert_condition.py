# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class AlertCondition(pulumi.CustomResource):
    enabled: pulumi.Output[bool]
    """
    Set whether to enable the alert condition. Defaults to `true`.
    """
    monitor_id: pulumi.Output[str]
    """
    The ID of the Synthetics monitor to be referenced in the alert condition. 
    """
    name: pulumi.Output[str]
    """
    The title of this condition.
    """
    policy_id: pulumi.Output[float]
    """
    The ID of the policy where this condition should be used.
    """
    runbook_url: pulumi.Output[str]
    """
    Runbook URL to display in notifications.
    """
    def __init__(__self__, resource_name, opts=None, enabled=None, monitor_id=None, name=None, policy_id=None, runbook_url=None, __props__=None, __name__=None, __opts__=None):
        """
        Use this resource to create and manage synthetics alert conditions in New Relic.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Set whether to enable the alert condition. Defaults to `true`.
        :param pulumi.Input[str] monitor_id: The ID of the Synthetics monitor to be referenced in the alert condition. 
        :param pulumi.Input[str] name: The title of this condition.
        :param pulumi.Input[float] policy_id: The ID of the policy where this condition should be used.
        :param pulumi.Input[str] runbook_url: Runbook URL to display in notifications.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-newrelic/blob/master/website/docs/r/synthetics_alert_condition.html.markdown.
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

            __props__['enabled'] = enabled
            if monitor_id is None:
                raise TypeError("Missing required property 'monitor_id'")
            __props__['monitor_id'] = monitor_id
            __props__['name'] = name
            if policy_id is None:
                raise TypeError("Missing required property 'policy_id'")
            __props__['policy_id'] = policy_id
            __props__['runbook_url'] = runbook_url
        super(AlertCondition, __self__).__init__(
            'newrelic:synthetics/alertCondition:AlertCondition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, enabled=None, monitor_id=None, name=None, policy_id=None, runbook_url=None):
        """
        Get an existing AlertCondition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] enabled: Set whether to enable the alert condition. Defaults to `true`.
        :param pulumi.Input[str] monitor_id: The ID of the Synthetics monitor to be referenced in the alert condition. 
        :param pulumi.Input[str] name: The title of this condition.
        :param pulumi.Input[float] policy_id: The ID of the policy where this condition should be used.
        :param pulumi.Input[str] runbook_url: Runbook URL to display in notifications.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-newrelic/blob/master/website/docs/r/synthetics_alert_condition.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["enabled"] = enabled
        __props__["monitor_id"] = monitor_id
        __props__["name"] = name
        __props__["policy_id"] = policy_id
        __props__["runbook_url"] = runbook_url
        return AlertCondition(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

