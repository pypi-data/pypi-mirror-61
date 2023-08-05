# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class SecurityGroupRule(pulumi.CustomResource):
    cidr_ip: pulumi.Output[str]
    """
    The target IP address range. The default value is 0.0.0.0/0 (which means no restriction will be applied). Other supported formats include 10.159.6.18/12. Only IPv4 is supported.
    """
    description: pulumi.Output[str]
    """
    The description of the security group rule. The description can be up to 1 to 512 characters in length. Defaults to null.
    """
    ip_protocol: pulumi.Output[str]
    """
    The protocol. Can be `tcp`, `udp`, `icmp`, `gre` or `all`.
    """
    nic_type: pulumi.Output[str]
    """
    Network type, can be either `internet` or `intranet`, the default value is `internet`.
    """
    policy: pulumi.Output[str]
    """
    Authorization policy, can be either `accept` or `drop`, the default value is `accept`.
    """
    port_range: pulumi.Output[str]
    """
    The range of port numbers relevant to the IP protocol. Default to "-1/-1". When the protocol is tcp or udp, each side port number range from 1 to 65535 and '-1/-1' will be invalid.
    For example, `1/200` means that the range of the port numbers is 1-200. Other protocols' 'port_range' can only be "-1/-1", and other values will be invalid.
    """
    priority: pulumi.Output[float]
    """
    Authorization policy priority, with parameter values: `1-100`, default value: 1.
    """
    security_group_id: pulumi.Output[str]
    """
    The security group to apply this rule to.
    """
    source_group_owner_account: pulumi.Output[str]
    """
    The Alibaba Cloud user account Id of the target security group when security groups are authorized across accounts.  This parameter is invalid if `cidr_ip` has already been set.
    """
    source_security_group_id: pulumi.Output[str]
    """
    The target security group ID within the same region. If this field is specified, the `nic_type` can only select `intranet`.
    """
    type: pulumi.Output[str]
    """
    The type of rule being created. Valid options are `ingress` (inbound) or `egress` (outbound).
    """
    def __init__(__self__, resource_name, opts=None, cidr_ip=None, description=None, ip_protocol=None, nic_type=None, policy=None, port_range=None, priority=None, security_group_id=None, source_group_owner_account=None, source_security_group_id=None, type=None, __props__=None, __name__=None, __opts__=None):
        """
        Create a SecurityGroupRule resource with the given unique name, props, and options.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_ip: The target IP address range. The default value is 0.0.0.0/0 (which means no restriction will be applied). Other supported formats include 10.159.6.18/12. Only IPv4 is supported.
        :param pulumi.Input[str] description: The description of the security group rule. The description can be up to 1 to 512 characters in length. Defaults to null.
        :param pulumi.Input[str] ip_protocol: The protocol. Can be `tcp`, `udp`, `icmp`, `gre` or `all`.
        :param pulumi.Input[str] nic_type: Network type, can be either `internet` or `intranet`, the default value is `internet`.
        :param pulumi.Input[str] policy: Authorization policy, can be either `accept` or `drop`, the default value is `accept`.
        :param pulumi.Input[str] port_range: The range of port numbers relevant to the IP protocol. Default to "-1/-1". When the protocol is tcp or udp, each side port number range from 1 to 65535 and '-1/-1' will be invalid.
               For example, `1/200` means that the range of the port numbers is 1-200. Other protocols' 'port_range' can only be "-1/-1", and other values will be invalid.
        :param pulumi.Input[float] priority: Authorization policy priority, with parameter values: `1-100`, default value: 1.
        :param pulumi.Input[str] security_group_id: The security group to apply this rule to.
        :param pulumi.Input[str] source_group_owner_account: The Alibaba Cloud user account Id of the target security group when security groups are authorized across accounts.  This parameter is invalid if `cidr_ip` has already been set.
        :param pulumi.Input[str] source_security_group_id: The target security group ID within the same region. If this field is specified, the `nic_type` can only select `intranet`.
        :param pulumi.Input[str] type: The type of rule being created. Valid options are `ingress` (inbound) or `egress` (outbound).

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/security_group_rule.html.markdown.
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

            __props__['cidr_ip'] = cidr_ip
            __props__['description'] = description
            if ip_protocol is None:
                raise TypeError("Missing required property 'ip_protocol'")
            __props__['ip_protocol'] = ip_protocol
            __props__['nic_type'] = nic_type
            __props__['policy'] = policy
            __props__['port_range'] = port_range
            __props__['priority'] = priority
            if security_group_id is None:
                raise TypeError("Missing required property 'security_group_id'")
            __props__['security_group_id'] = security_group_id
            __props__['source_group_owner_account'] = source_group_owner_account
            __props__['source_security_group_id'] = source_security_group_id
            if type is None:
                raise TypeError("Missing required property 'type'")
            __props__['type'] = type
        super(SecurityGroupRule, __self__).__init__(
            'alicloud:ecs/securityGroupRule:SecurityGroupRule',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, cidr_ip=None, description=None, ip_protocol=None, nic_type=None, policy=None, port_range=None, priority=None, security_group_id=None, source_group_owner_account=None, source_security_group_id=None, type=None):
        """
        Get an existing SecurityGroupRule resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cidr_ip: The target IP address range. The default value is 0.0.0.0/0 (which means no restriction will be applied). Other supported formats include 10.159.6.18/12. Only IPv4 is supported.
        :param pulumi.Input[str] description: The description of the security group rule. The description can be up to 1 to 512 characters in length. Defaults to null.
        :param pulumi.Input[str] ip_protocol: The protocol. Can be `tcp`, `udp`, `icmp`, `gre` or `all`.
        :param pulumi.Input[str] nic_type: Network type, can be either `internet` or `intranet`, the default value is `internet`.
        :param pulumi.Input[str] policy: Authorization policy, can be either `accept` or `drop`, the default value is `accept`.
        :param pulumi.Input[str] port_range: The range of port numbers relevant to the IP protocol. Default to "-1/-1". When the protocol is tcp or udp, each side port number range from 1 to 65535 and '-1/-1' will be invalid.
               For example, `1/200` means that the range of the port numbers is 1-200. Other protocols' 'port_range' can only be "-1/-1", and other values will be invalid.
        :param pulumi.Input[float] priority: Authorization policy priority, with parameter values: `1-100`, default value: 1.
        :param pulumi.Input[str] security_group_id: The security group to apply this rule to.
        :param pulumi.Input[str] source_group_owner_account: The Alibaba Cloud user account Id of the target security group when security groups are authorized across accounts.  This parameter is invalid if `cidr_ip` has already been set.
        :param pulumi.Input[str] source_security_group_id: The target security group ID within the same region. If this field is specified, the `nic_type` can only select `intranet`.
        :param pulumi.Input[str] type: The type of rule being created. Valid options are `ingress` (inbound) or `egress` (outbound).

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/security_group_rule.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["cidr_ip"] = cidr_ip
        __props__["description"] = description
        __props__["ip_protocol"] = ip_protocol
        __props__["nic_type"] = nic_type
        __props__["policy"] = policy
        __props__["port_range"] = port_range
        __props__["priority"] = priority
        __props__["security_group_id"] = security_group_id
        __props__["source_group_owner_account"] = source_group_owner_account
        __props__["source_security_group_id"] = source_security_group_id
        __props__["type"] = type
        return SecurityGroupRule(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

