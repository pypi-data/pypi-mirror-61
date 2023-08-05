# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Instance(pulumi.CustomResource):
    deploy_type: pulumi.Output[float]
    """
    The deploy type of the instance. Currently only support two deploy type, 4: eip/vpc instance, 5: vpc instance.
    """
    disk_size: pulumi.Output[float]
    """
    The disk size of the instance. When modify this value, it only support adjust to a greater value.
    """
    disk_type: pulumi.Output[float]
    """
    The disk type of the instance. 0: efficient cloud disk , 1: SSD.
    """
    eip_max: pulumi.Output[float]
    """
    The max bandwidth of the instance. When modify this value, it only support adjust to a greater value.
    """
    io_max: pulumi.Output[float]
    """
    The max value of io of the instance. When modify this value, it only support adjust to a greater value.
    """
    name: pulumi.Output[str]
    """
    Name of your Kafka instance. The length should between 3 and 64 characters. If not set, will use instance id as instance name.
    """
    paid_type: pulumi.Output[str]
    """
    The paid type of the instance. Support two type, "PrePaid": pre paid type instance, "PostPaid": post paid type instance. Default is PostPaid. When modify this value, it only support adjust from post pay to pre pay. 
    """
    spec_type: pulumi.Output[str]
    """
    The spec type of the instance. Support two type, "normal": normal version instance, "professional": professional version instance. Default is normal. When modify this value, it only support adjust from normal to professional. Note only pre paid type instance support professional specific type.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    topic_quota: pulumi.Output[float]
    """
    The max num of topic can be create of the instance. When modify this value, it only adjust to a greater value.
    """
    vpc_id: pulumi.Output[str]
    """
    The ID of attaching VPC to instance.
    """
    vswitch_id: pulumi.Output[str]
    """
    The ID of attaching vswitch to instance.
    """
    zone_id: pulumi.Output[str]
    """
    The Zone to launch the kafka instance.
    """
    def __init__(__self__, resource_name, opts=None, deploy_type=None, disk_size=None, disk_type=None, eip_max=None, io_max=None, name=None, paid_type=None, spec_type=None, tags=None, topic_quota=None, vswitch_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an ALIKAFKA instance resource.
        
        > **NOTE:** Available in 1.59.0+
        
        > **NOTE:** ALIKAFKA instance resource only support create post pay instance. Creation or modification may took about 10-40 minutes.
        
        > **NOTE:** Only the following regions support create alikafka pre paid instance.
        [`cn-hangzhou`,`cn-beijing`,`cn-shenzhen`,`cn-shanghai`,`cn-qingdao`,`cn-hongkong`,`cn-huhehaote`,`cn-zhangjiakou`,`ap-southeast-1`,`ap-south-1`,`ap-southeast-5`]
        
        > **NOTE:** Only the following regions support create alikafka post paid instance.
        [`cn-hangzhou`,`cn-beijing`,`cn-shenzhen`,`cn-shanghai`,`cn-qingdao`,`cn-hongkong`,`cn-huhehaote`,`cn-zhangjiakou`,`ap-southeast-1`]
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] deploy_type: The deploy type of the instance. Currently only support two deploy type, 4: eip/vpc instance, 5: vpc instance.
        :param pulumi.Input[float] disk_size: The disk size of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[float] disk_type: The disk type of the instance. 0: efficient cloud disk , 1: SSD.
        :param pulumi.Input[float] eip_max: The max bandwidth of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[float] io_max: The max value of io of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[str] name: Name of your Kafka instance. The length should between 3 and 64 characters. If not set, will use instance id as instance name.
        :param pulumi.Input[str] paid_type: The paid type of the instance. Support two type, "PrePaid": pre paid type instance, "PostPaid": post paid type instance. Default is PostPaid. When modify this value, it only support adjust from post pay to pre pay. 
        :param pulumi.Input[str] spec_type: The spec type of the instance. Support two type, "normal": normal version instance, "professional": professional version instance. Default is normal. When modify this value, it only support adjust from normal to professional. Note only pre paid type instance support professional specific type.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[float] topic_quota: The max num of topic can be create of the instance. When modify this value, it only adjust to a greater value.
        :param pulumi.Input[str] vswitch_id: The ID of attaching vswitch to instance.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/alikafka_instance.html.markdown.
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

            if deploy_type is None:
                raise TypeError("Missing required property 'deploy_type'")
            __props__['deploy_type'] = deploy_type
            if disk_size is None:
                raise TypeError("Missing required property 'disk_size'")
            __props__['disk_size'] = disk_size
            if disk_type is None:
                raise TypeError("Missing required property 'disk_type'")
            __props__['disk_type'] = disk_type
            __props__['eip_max'] = eip_max
            if io_max is None:
                raise TypeError("Missing required property 'io_max'")
            __props__['io_max'] = io_max
            __props__['name'] = name
            __props__['paid_type'] = paid_type
            __props__['spec_type'] = spec_type
            __props__['tags'] = tags
            if topic_quota is None:
                raise TypeError("Missing required property 'topic_quota'")
            __props__['topic_quota'] = topic_quota
            if vswitch_id is None:
                raise TypeError("Missing required property 'vswitch_id'")
            __props__['vswitch_id'] = vswitch_id
            __props__['vpc_id'] = None
            __props__['zone_id'] = None
        super(Instance, __self__).__init__(
            'alicloud:alikafka/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, deploy_type=None, disk_size=None, disk_type=None, eip_max=None, io_max=None, name=None, paid_type=None, spec_type=None, tags=None, topic_quota=None, vpc_id=None, vswitch_id=None, zone_id=None):
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] deploy_type: The deploy type of the instance. Currently only support two deploy type, 4: eip/vpc instance, 5: vpc instance.
        :param pulumi.Input[float] disk_size: The disk size of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[float] disk_type: The disk type of the instance. 0: efficient cloud disk , 1: SSD.
        :param pulumi.Input[float] eip_max: The max bandwidth of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[float] io_max: The max value of io of the instance. When modify this value, it only support adjust to a greater value.
        :param pulumi.Input[str] name: Name of your Kafka instance. The length should between 3 and 64 characters. If not set, will use instance id as instance name.
        :param pulumi.Input[str] paid_type: The paid type of the instance. Support two type, "PrePaid": pre paid type instance, "PostPaid": post paid type instance. Default is PostPaid. When modify this value, it only support adjust from post pay to pre pay. 
        :param pulumi.Input[str] spec_type: The spec type of the instance. Support two type, "normal": normal version instance, "professional": professional version instance. Default is normal. When modify this value, it only support adjust from normal to professional. Note only pre paid type instance support professional specific type.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[float] topic_quota: The max num of topic can be create of the instance. When modify this value, it only adjust to a greater value.
        :param pulumi.Input[str] vpc_id: The ID of attaching VPC to instance.
        :param pulumi.Input[str] vswitch_id: The ID of attaching vswitch to instance.
        :param pulumi.Input[str] zone_id: The Zone to launch the kafka instance.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/alikafka_instance.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["deploy_type"] = deploy_type
        __props__["disk_size"] = disk_size
        __props__["disk_type"] = disk_type
        __props__["eip_max"] = eip_max
        __props__["io_max"] = io_max
        __props__["name"] = name
        __props__["paid_type"] = paid_type
        __props__["spec_type"] = spec_type
        __props__["tags"] = tags
        __props__["topic_quota"] = topic_quota
        __props__["vpc_id"] = vpc_id
        __props__["vswitch_id"] = vswitch_id
        __props__["zone_id"] = zone_id
        return Instance(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

