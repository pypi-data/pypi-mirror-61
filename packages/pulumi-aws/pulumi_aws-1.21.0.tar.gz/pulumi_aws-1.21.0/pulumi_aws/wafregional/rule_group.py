# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class RuleGroup(pulumi.CustomResource):
    activated_rules: pulumi.Output[list]
    """
    A list of activated rules, see below
    
      * `action` (`dict`) - Specifies the action that CloudFront or AWS WAF takes when a web request matches the conditions in the rule.
    
        * `type` (`str`) - The rule type, either [`REGULAR`](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html), [`RATE_BASED`](https://www.terraform.io/docs/providers/aws/r/wafregional_rate_based_rule.html), or `GROUP`. Defaults to `REGULAR`.
    
      * `priority` (`float`) - Specifies the order in which the rules are evaluated. Rules with a lower value are evaluated before rules with a higher value.
      * `rule_id` (`str`) - The ID of a [rule](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html)
      * `type` (`str`) - The rule type, either [`REGULAR`](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html), [`RATE_BASED`](https://www.terraform.io/docs/providers/aws/r/wafregional_rate_based_rule.html), or `GROUP`. Defaults to `REGULAR`.
    """
    arn: pulumi.Output[str]
    """
    The ARN of the WAF Regional Rule Group.
    """
    metric_name: pulumi.Output[str]
    """
    A friendly name for the metrics from the rule group
    """
    name: pulumi.Output[str]
    """
    A friendly name of the rule group
    """
    tags: pulumi.Output[dict]
    """
    Key-value mapping of resource tags
    """
    def __init__(__self__, resource_name, opts=None, activated_rules=None, metric_name=None, name=None, tags=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a WAF Regional Rule Group Resource
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] activated_rules: A list of activated rules, see below
        :param pulumi.Input[str] metric_name: A friendly name for the metrics from the rule group
        :param pulumi.Input[str] name: A friendly name of the rule group
        :param pulumi.Input[dict] tags: Key-value mapping of resource tags
        
        The **activated_rules** object supports the following:
        
          * `action` (`pulumi.Input[dict]`) - Specifies the action that CloudFront or AWS WAF takes when a web request matches the conditions in the rule.
        
            * `type` (`pulumi.Input[str]`) - The rule type, either [`REGULAR`](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html), [`RATE_BASED`](https://www.terraform.io/docs/providers/aws/r/wafregional_rate_based_rule.html), or `GROUP`. Defaults to `REGULAR`.
        
          * `priority` (`pulumi.Input[float]`) - Specifies the order in which the rules are evaluated. Rules with a lower value are evaluated before rules with a higher value.
          * `rule_id` (`pulumi.Input[str]`) - The ID of a [rule](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html)
          * `type` (`pulumi.Input[str]`) - The rule type, either [`REGULAR`](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html), [`RATE_BASED`](https://www.terraform.io/docs/providers/aws/r/wafregional_rate_based_rule.html), or `GROUP`. Defaults to `REGULAR`.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/wafregional_rule_group.html.markdown.
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

            __props__['activated_rules'] = activated_rules
            if metric_name is None:
                raise TypeError("Missing required property 'metric_name'")
            __props__['metric_name'] = metric_name
            __props__['name'] = name
            __props__['tags'] = tags
            __props__['arn'] = None
        super(RuleGroup, __self__).__init__(
            'aws:wafregional/ruleGroup:RuleGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, activated_rules=None, arn=None, metric_name=None, name=None, tags=None):
        """
        Get an existing RuleGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[list] activated_rules: A list of activated rules, see below
        :param pulumi.Input[str] arn: The ARN of the WAF Regional Rule Group.
        :param pulumi.Input[str] metric_name: A friendly name for the metrics from the rule group
        :param pulumi.Input[str] name: A friendly name of the rule group
        :param pulumi.Input[dict] tags: Key-value mapping of resource tags
        
        The **activated_rules** object supports the following:
        
          * `action` (`pulumi.Input[dict]`) - Specifies the action that CloudFront or AWS WAF takes when a web request matches the conditions in the rule.
        
            * `type` (`pulumi.Input[str]`) - The rule type, either [`REGULAR`](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html), [`RATE_BASED`](https://www.terraform.io/docs/providers/aws/r/wafregional_rate_based_rule.html), or `GROUP`. Defaults to `REGULAR`.
        
          * `priority` (`pulumi.Input[float]`) - Specifies the order in which the rules are evaluated. Rules with a lower value are evaluated before rules with a higher value.
          * `rule_id` (`pulumi.Input[str]`) - The ID of a [rule](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html)
          * `type` (`pulumi.Input[str]`) - The rule type, either [`REGULAR`](https://www.terraform.io/docs/providers/aws/r/wafregional_rule.html), [`RATE_BASED`](https://www.terraform.io/docs/providers/aws/r/wafregional_rate_based_rule.html), or `GROUP`. Defaults to `REGULAR`.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/wafregional_rule_group.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["activated_rules"] = activated_rules
        __props__["arn"] = arn
        __props__["metric_name"] = metric_name
        __props__["name"] = name
        __props__["tags"] = tags
        return RuleGroup(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

