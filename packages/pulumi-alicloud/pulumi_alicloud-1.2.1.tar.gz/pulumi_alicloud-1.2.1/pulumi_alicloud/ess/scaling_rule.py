# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ScalingRule(pulumi.CustomResource):
    adjustment_type: pulumi.Output[str]
    """
    Adjustment mode of a scaling rule. Optional values:
    - QuantityChangeInCapacity: It is used to increase or decrease a specified number of ECS instances.
    - PercentChangeInCapacity: It is used to increase or decrease a specified proportion of ECS instances.
    - TotalCapacity: It is used to adjust the quantity of ECS instances in the current scaling group to a specified value.
    """
    adjustment_value: pulumi.Output[float]
    """
    Adjusted value of a scaling rule. Value range:
    - QuantityChangeInCapacity：(0, 500] U (-500, 0]
    - PercentChangeInCapacity：[0, 10000] U [-100, 0]
    - TotalCapacity：[0, 1000]
    """
    ari: pulumi.Output[str]
    cooldown: pulumi.Output[float]
    """
    Cool-down time of a scaling rule. Value range: [0, 86,400], in seconds. The default value is empty，if not set, the return value will be 0, which is the default value of integer.
    """
    disable_scale_in: pulumi.Output[bool]
    """
    Indicates whether scale in by the target tracking policy is disabled. Default to false.
    """
    estimated_instance_warmup: pulumi.Output[float]
    """
    The estimated time, in seconds, until a newly launched instance will contribute CloudMonitor metrics. Default to 300.
    """
    metric_name: pulumi.Output[str]
    """
    A CloudMonitor metric name.
    """
    scaling_group_id: pulumi.Output[str]
    """
    ID of the scaling group of a scaling rule.
    """
    scaling_rule_name: pulumi.Output[str]
    """
    Name shown for the scaling rule, which must contain 2-64 characters (English or Chinese), starting with numbers, English letters or Chinese characters, and can contain number, underscores `_`, hypens `-`, and decimal point `.`. If this parameter value is not specified, the default value is scaling rule id. 
    """
    scaling_rule_type: pulumi.Output[str]
    """
    The scaling rule type, either "SimpleScalingRule", "TargetTrackingScalingRule", "StepScalingRule". Default to "SimpleScalingRule".
    """
    step_adjustments: pulumi.Output[list]
    """
    Steps for StepScalingRule. See Block stepAdjustment below for details.
    
      * `metricIntervalLowerBound` (`str`)
      * `metricIntervalUpperBound` (`str`)
      * `scalingAdjustment` (`float`)
    """
    target_value: pulumi.Output[float]
    """
    The target value for the metric.
    """
    def __init__(__self__, resource_name, opts=None, adjustment_type=None, adjustment_value=None, cooldown=None, disable_scale_in=None, estimated_instance_warmup=None, metric_name=None, scaling_group_id=None, scaling_rule_name=None, scaling_rule_type=None, step_adjustments=None, target_value=None, __props__=None, __name__=None, __opts__=None):
        """
        Create a ScalingRule resource with the given unique name, props, and options.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] adjustment_type: Adjustment mode of a scaling rule. Optional values:
               - QuantityChangeInCapacity: It is used to increase or decrease a specified number of ECS instances.
               - PercentChangeInCapacity: It is used to increase or decrease a specified proportion of ECS instances.
               - TotalCapacity: It is used to adjust the quantity of ECS instances in the current scaling group to a specified value.
        :param pulumi.Input[float] adjustment_value: Adjusted value of a scaling rule. Value range:
               - QuantityChangeInCapacity：(0, 500] U (-500, 0]
               - PercentChangeInCapacity：[0, 10000] U [-100, 0]
               - TotalCapacity：[0, 1000]
        :param pulumi.Input[float] cooldown: Cool-down time of a scaling rule. Value range: [0, 86,400], in seconds. The default value is empty，if not set, the return value will be 0, which is the default value of integer.
        :param pulumi.Input[bool] disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. Default to false.
        :param pulumi.Input[float] estimated_instance_warmup: The estimated time, in seconds, until a newly launched instance will contribute CloudMonitor metrics. Default to 300.
        :param pulumi.Input[str] metric_name: A CloudMonitor metric name.
        :param pulumi.Input[str] scaling_group_id: ID of the scaling group of a scaling rule.
        :param pulumi.Input[str] scaling_rule_name: Name shown for the scaling rule, which must contain 2-64 characters (English or Chinese), starting with numbers, English letters or Chinese characters, and can contain number, underscores `_`, hypens `-`, and decimal point `.`. If this parameter value is not specified, the default value is scaling rule id. 
        :param pulumi.Input[str] scaling_rule_type: The scaling rule type, either "SimpleScalingRule", "TargetTrackingScalingRule", "StepScalingRule". Default to "SimpleScalingRule".
        :param pulumi.Input[list] step_adjustments: Steps for StepScalingRule. See Block stepAdjustment below for details.
        :param pulumi.Input[float] target_value: The target value for the metric.
        
        The **step_adjustments** object supports the following:
        
          * `metricIntervalLowerBound` (`pulumi.Input[str]`)
          * `metricIntervalUpperBound` (`pulumi.Input[str]`)
          * `scalingAdjustment` (`pulumi.Input[float]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/ess_scaling_rule.html.markdown.
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

            __props__['adjustment_type'] = adjustment_type
            __props__['adjustment_value'] = adjustment_value
            __props__['cooldown'] = cooldown
            __props__['disable_scale_in'] = disable_scale_in
            __props__['estimated_instance_warmup'] = estimated_instance_warmup
            __props__['metric_name'] = metric_name
            if scaling_group_id is None:
                raise TypeError("Missing required property 'scaling_group_id'")
            __props__['scaling_group_id'] = scaling_group_id
            __props__['scaling_rule_name'] = scaling_rule_name
            __props__['scaling_rule_type'] = scaling_rule_type
            __props__['step_adjustments'] = step_adjustments
            __props__['target_value'] = target_value
            __props__['ari'] = None
        super(ScalingRule, __self__).__init__(
            'alicloud:ess/scalingRule:ScalingRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, adjustment_type=None, adjustment_value=None, ari=None, cooldown=None, disable_scale_in=None, estimated_instance_warmup=None, metric_name=None, scaling_group_id=None, scaling_rule_name=None, scaling_rule_type=None, step_adjustments=None, target_value=None):
        """
        Get an existing ScalingRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] adjustment_type: Adjustment mode of a scaling rule. Optional values:
               - QuantityChangeInCapacity: It is used to increase or decrease a specified number of ECS instances.
               - PercentChangeInCapacity: It is used to increase or decrease a specified proportion of ECS instances.
               - TotalCapacity: It is used to adjust the quantity of ECS instances in the current scaling group to a specified value.
        :param pulumi.Input[float] adjustment_value: Adjusted value of a scaling rule. Value range:
               - QuantityChangeInCapacity：(0, 500] U (-500, 0]
               - PercentChangeInCapacity：[0, 10000] U [-100, 0]
               - TotalCapacity：[0, 1000]
        :param pulumi.Input[float] cooldown: Cool-down time of a scaling rule. Value range: [0, 86,400], in seconds. The default value is empty，if not set, the return value will be 0, which is the default value of integer.
        :param pulumi.Input[bool] disable_scale_in: Indicates whether scale in by the target tracking policy is disabled. Default to false.
        :param pulumi.Input[float] estimated_instance_warmup: The estimated time, in seconds, until a newly launched instance will contribute CloudMonitor metrics. Default to 300.
        :param pulumi.Input[str] metric_name: A CloudMonitor metric name.
        :param pulumi.Input[str] scaling_group_id: ID of the scaling group of a scaling rule.
        :param pulumi.Input[str] scaling_rule_name: Name shown for the scaling rule, which must contain 2-64 characters (English or Chinese), starting with numbers, English letters or Chinese characters, and can contain number, underscores `_`, hypens `-`, and decimal point `.`. If this parameter value is not specified, the default value is scaling rule id. 
        :param pulumi.Input[str] scaling_rule_type: The scaling rule type, either "SimpleScalingRule", "TargetTrackingScalingRule", "StepScalingRule". Default to "SimpleScalingRule".
        :param pulumi.Input[list] step_adjustments: Steps for StepScalingRule. See Block stepAdjustment below for details.
        :param pulumi.Input[float] target_value: The target value for the metric.
        
        The **step_adjustments** object supports the following:
        
          * `metricIntervalLowerBound` (`pulumi.Input[str]`)
          * `metricIntervalUpperBound` (`pulumi.Input[str]`)
          * `scalingAdjustment` (`pulumi.Input[float]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/ess_scaling_rule.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["adjustment_type"] = adjustment_type
        __props__["adjustment_value"] = adjustment_value
        __props__["ari"] = ari
        __props__["cooldown"] = cooldown
        __props__["disable_scale_in"] = disable_scale_in
        __props__["estimated_instance_warmup"] = estimated_instance_warmup
        __props__["metric_name"] = metric_name
        __props__["scaling_group_id"] = scaling_group_id
        __props__["scaling_rule_name"] = scaling_rule_name
        __props__["scaling_rule_type"] = scaling_rule_type
        __props__["step_adjustments"] = step_adjustments
        __props__["target_value"] = target_value
        return ScalingRule(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

