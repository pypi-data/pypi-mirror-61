# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class NrqlAlertCondition(pulumi.CustomResource):
    enabled: pulumi.Output[bool]
    expected_groups: pulumi.Output[float]
    ignore_overlap: pulumi.Output[bool]
    name: pulumi.Output[str]
    nrql: pulumi.Output[dict]
    policy_id: pulumi.Output[float]
    runbook_url: pulumi.Output[str]
    terms: pulumi.Output[list]
    type: pulumi.Output[str]
    value_function: pulumi.Output[str]
    violation_time_limit_seconds: pulumi.Output[float]
    def __init__(__self__, resource_name, opts=None, enabled=None, expected_groups=None, ignore_overlap=None, name=None, nrql=None, policy_id=None, runbook_url=None, terms=None, type=None, value_function=None, violation_time_limit_seconds=None, __props__=None, __name__=None, __opts__=None):
        """
        Use this resource to create and manage NRQL alert conditions in New Relic.
        
        ## Terms
        
        The `term` mapping supports the following arguments:
        
        - `duration` - (Required) In minutes, must be in the range of `1` to `120`, inclusive.
        - `operator` - (Optional) `above`, `below`, or `equal`. Defaults to `equal`.
        - `priority` - (Optional) `critical` or `warning`. Defaults to `critical`.
        - `threshold` - (Required) Must be 0 or greater.
        - `time_function` - (Required) `all` or `any`.
        
        ## NRQL
        
        The `nrql` attribute supports the following arguments:
        
        - `query` - (Required) The NRQL query to execute for the condition.
        - `since_value` - (Required) The value to be used in the `SINCE <X> MINUTES AGO` clause for the NRQL query. Must be between `1` and `20`.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        
        The **nrql** object supports the following:
        
          * `query` (`pulumi.Input[str]`)
          * `sinceValue` (`pulumi.Input[str]`)
        
        The **terms** object supports the following:
        
          * `duration` (`pulumi.Input[float]`)
          * `operator` (`pulumi.Input[str]`)
          * `priority` (`pulumi.Input[str]`)
          * `threshold` (`pulumi.Input[float]`)
          * `timeFunction` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-newrelic/blob/master/website/docs/r/nrql_alert_condition.html.markdown.
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
            __props__['expected_groups'] = expected_groups
            __props__['ignore_overlap'] = ignore_overlap
            __props__['name'] = name
            if nrql is None:
                raise TypeError("Missing required property 'nrql'")
            __props__['nrql'] = nrql
            if policy_id is None:
                raise TypeError("Missing required property 'policy_id'")
            __props__['policy_id'] = policy_id
            __props__['runbook_url'] = runbook_url
            if terms is None:
                raise TypeError("Missing required property 'terms'")
            __props__['terms'] = terms
            __props__['type'] = type
            __props__['value_function'] = value_function
            __props__['violation_time_limit_seconds'] = violation_time_limit_seconds
        super(NrqlAlertCondition, __self__).__init__(
            'newrelic:index/nrqlAlertCondition:NrqlAlertCondition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, enabled=None, expected_groups=None, ignore_overlap=None, name=None, nrql=None, policy_id=None, runbook_url=None, terms=None, type=None, value_function=None, violation_time_limit_seconds=None):
        """
        Get an existing NrqlAlertCondition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        
        The **nrql** object supports the following:
        
          * `query` (`pulumi.Input[str]`)
          * `sinceValue` (`pulumi.Input[str]`)
        
        The **terms** object supports the following:
        
          * `duration` (`pulumi.Input[float]`)
          * `operator` (`pulumi.Input[str]`)
          * `priority` (`pulumi.Input[str]`)
          * `threshold` (`pulumi.Input[float]`)
          * `timeFunction` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-newrelic/blob/master/website/docs/r/nrql_alert_condition.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["enabled"] = enabled
        __props__["expected_groups"] = expected_groups
        __props__["ignore_overlap"] = ignore_overlap
        __props__["name"] = name
        __props__["nrql"] = nrql
        __props__["policy_id"] = policy_id
        __props__["runbook_url"] = runbook_url
        __props__["terms"] = terms
        __props__["type"] = type
        __props__["value_function"] = value_function
        __props__["violation_time_limit_seconds"] = violation_time_limit_seconds
        return NrqlAlertCondition(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

