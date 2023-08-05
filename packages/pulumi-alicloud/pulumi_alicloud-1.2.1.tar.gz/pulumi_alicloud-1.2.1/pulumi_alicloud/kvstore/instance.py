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
    auto_renew: pulumi.Output[bool]
    """
    Whether to renewal a DB instance automatically or not. It is valid when instance_charge_type is `PrePaid`. Default to `false`.
    """
    auto_renew_period: pulumi.Output[float]
    """
    Auto-renewal period of an instance, in the unit of the month. It is valid when instance_charge_type is `PrePaid`. Valid value:[1~12], Default to 1.
    """
    availability_zone: pulumi.Output[str]
    """
    The Zone to launch the DB instance.
    """
    backup_id: pulumi.Output[str]
    connection_domain: pulumi.Output[str]
    """
    Instance connection domain (only Intranet access supported).
    """
    engine_version: pulumi.Output[str]
    instance_charge_type: pulumi.Output[str]
    """
    Valid values are `PrePaid`, `PostPaid`, Default to `PostPaid`.
    """
    instance_class: pulumi.Output[str]
    instance_name: pulumi.Output[str]
    """
    The name of DB instance. It a string of 2 to 256 characters.
    * `password`- (Optional, Sensitive) The password of the DB instance. The password is a string of 8 to 30 characters and must contain uppercase letters, lowercase letters, and numbers.
    """
    instance_type: pulumi.Output[str]
    """
    The engine to use: `Redis` or `Memcache`. Defaults to `Redis`.
    """
    kms_encrypted_password: pulumi.Output[str]
    """
    An KMS encrypts password used to a instance. If the `password` is filled in, this field will be ignored.
    """
    kms_encryption_context: pulumi.Output[dict]
    """
    An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
    """
    maintain_end_time: pulumi.Output[str]
    """
    The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
    """
    maintain_start_time: pulumi.Output[str]
    """
    The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
    """
    parameters: pulumi.Output[list]
    """
    Set of parameters needs to be set after instance was launched. Available parameters can refer to the latest docs [Instance configurations table](https://www.alibabacloud.com/help/doc-detail/61209.htm) .
    
      * `name` (`str`)
      * `value` (`str`)
    """
    password: pulumi.Output[str]
    period: pulumi.Output[float]
    """
    The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. Default to 1.
    """
    private_ip: pulumi.Output[str]
    security_ips: pulumi.Output[list]
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    """
    vpc_auth_mode: pulumi.Output[str]
    vswitch_id: pulumi.Output[str]
    """
    The ID of VSwitch.
    * `engine_version`- (Optional, ForceNew) Engine version. Supported values: 2.8, 4.0 and 5.0. Default value: 2.8. Only 2.8 can be supported for Memcache Instance.
    * `security_ips`- (Optional) Set the instance's IP whitelist of the default security group.
    * `private_ip`- (Optional) Set the instance's private IP.
    * `backup_id`- (Optional) If an instance created based on a backup set generated by another instance is valid, this parameter indicates the ID of the generated backup set.
    * `vpc_auth_mode`- (Optional) Only meaningful if instance_type is `Redis` and network type is VPC. Valid values are `Close`, `Open`. Defaults to `Open`.  `Close` means the redis instance can be accessed without authentication. `Open` means authentication is required.
    """
    def __init__(__self__, resource_name, opts=None, auto_renew=None, auto_renew_period=None, availability_zone=None, backup_id=None, engine_version=None, instance_charge_type=None, instance_class=None, instance_name=None, instance_type=None, kms_encrypted_password=None, kms_encryption_context=None, maintain_end_time=None, maintain_start_time=None, parameters=None, password=None, period=None, private_ip=None, security_ips=None, tags=None, vpc_auth_mode=None, vswitch_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an ApsaraDB Redis / Memcache instance resource. A DB instance is an isolated database environment in the cloud. It can be associated with IP whitelists and backup configuration which are separate resource providers.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_renew: Whether to renewal a DB instance automatically or not. It is valid when instance_charge_type is `PrePaid`. Default to `false`.
        :param pulumi.Input[float] auto_renew_period: Auto-renewal period of an instance, in the unit of the month. It is valid when instance_charge_type is `PrePaid`. Valid value:[1~12], Default to 1.
        :param pulumi.Input[str] availability_zone: The Zone to launch the DB instance.
        :param pulumi.Input[str] instance_charge_type: Valid values are `PrePaid`, `PostPaid`, Default to `PostPaid`.
        :param pulumi.Input[str] instance_name: The name of DB instance. It a string of 2 to 256 characters.
               * `password`- (Optional, Sensitive) The password of the DB instance. The password is a string of 8 to 30 characters and must contain uppercase letters, lowercase letters, and numbers.
        :param pulumi.Input[str] instance_type: The engine to use: `Redis` or `Memcache`. Defaults to `Redis`.
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a instance. If the `password` is filled in, this field will be ignored.
        :param pulumi.Input[dict] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] maintain_end_time: The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] maintain_start_time: The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[list] parameters: Set of parameters needs to be set after instance was launched. Available parameters can refer to the latest docs [Instance configurations table](https://www.alibabacloud.com/help/doc-detail/61209.htm) .
        :param pulumi.Input[float] period: The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. Default to 1.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vswitch_id: The ID of VSwitch.
               * `engine_version`- (Optional, ForceNew) Engine version. Supported values: 2.8, 4.0 and 5.0. Default value: 2.8. Only 2.8 can be supported for Memcache Instance.
               * `security_ips`- (Optional) Set the instance's IP whitelist of the default security group.
               * `private_ip`- (Optional) Set the instance's private IP.
               * `backup_id`- (Optional) If an instance created based on a backup set generated by another instance is valid, this parameter indicates the ID of the generated backup set.
               * `vpc_auth_mode`- (Optional) Only meaningful if instance_type is `Redis` and network type is VPC. Valid values are `Close`, `Open`. Defaults to `Open`.  `Close` means the redis instance can be accessed without authentication. `Open` means authentication is required.
        
        The **parameters** object supports the following:
        
          * `name` (`pulumi.Input[str]`)
          * `value` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/kvstore_instance.html.markdown.
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

            __props__['auto_renew'] = auto_renew
            __props__['auto_renew_period'] = auto_renew_period
            __props__['availability_zone'] = availability_zone
            __props__['backup_id'] = backup_id
            __props__['engine_version'] = engine_version
            __props__['instance_charge_type'] = instance_charge_type
            if instance_class is None:
                raise TypeError("Missing required property 'instance_class'")
            __props__['instance_class'] = instance_class
            __props__['instance_name'] = instance_name
            __props__['instance_type'] = instance_type
            __props__['kms_encrypted_password'] = kms_encrypted_password
            __props__['kms_encryption_context'] = kms_encryption_context
            __props__['maintain_end_time'] = maintain_end_time
            __props__['maintain_start_time'] = maintain_start_time
            __props__['parameters'] = parameters
            __props__['password'] = password
            __props__['period'] = period
            __props__['private_ip'] = private_ip
            __props__['security_ips'] = security_ips
            __props__['tags'] = tags
            __props__['vpc_auth_mode'] = vpc_auth_mode
            __props__['vswitch_id'] = vswitch_id
            __props__['connection_domain'] = None
        super(Instance, __self__).__init__(
            'alicloud:kvstore/instance:Instance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, auto_renew=None, auto_renew_period=None, availability_zone=None, backup_id=None, connection_domain=None, engine_version=None, instance_charge_type=None, instance_class=None, instance_name=None, instance_type=None, kms_encrypted_password=None, kms_encryption_context=None, maintain_end_time=None, maintain_start_time=None, parameters=None, password=None, period=None, private_ip=None, security_ips=None, tags=None, vpc_auth_mode=None, vswitch_id=None):
        """
        Get an existing Instance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_renew: Whether to renewal a DB instance automatically or not. It is valid when instance_charge_type is `PrePaid`. Default to `false`.
        :param pulumi.Input[float] auto_renew_period: Auto-renewal period of an instance, in the unit of the month. It is valid when instance_charge_type is `PrePaid`. Valid value:[1~12], Default to 1.
        :param pulumi.Input[str] availability_zone: The Zone to launch the DB instance.
        :param pulumi.Input[str] connection_domain: Instance connection domain (only Intranet access supported).
        :param pulumi.Input[str] instance_charge_type: Valid values are `PrePaid`, `PostPaid`, Default to `PostPaid`.
        :param pulumi.Input[str] instance_name: The name of DB instance. It a string of 2 to 256 characters.
               * `password`- (Optional, Sensitive) The password of the DB instance. The password is a string of 8 to 30 characters and must contain uppercase letters, lowercase letters, and numbers.
        :param pulumi.Input[str] instance_type: The engine to use: `Redis` or `Memcache`. Defaults to `Redis`.
        :param pulumi.Input[str] kms_encrypted_password: An KMS encrypts password used to a instance. If the `password` is filled in, this field will be ignored.
        :param pulumi.Input[dict] kms_encryption_context: An KMS encryption context used to decrypt `kms_encrypted_password` before creating or updating instance with `kms_encrypted_password`. See [Encryption Context](https://www.alibabacloud.com/help/doc-detail/42975.htm). It is valid when `kms_encrypted_password` is set.
        :param pulumi.Input[str] maintain_end_time: The end time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[str] maintain_start_time: The start time of the operation and maintenance time period of the instance, in the format of HH:mmZ (UTC time).
        :param pulumi.Input[list] parameters: Set of parameters needs to be set after instance was launched. Available parameters can refer to the latest docs [Instance configurations table](https://www.alibabacloud.com/help/doc-detail/61209.htm) .
        :param pulumi.Input[float] period: The duration that you will buy DB instance (in month). It is valid when instance_charge_type is `PrePaid`. Valid values: [1~9], 12, 24, 36. Default to 1.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
        :param pulumi.Input[str] vswitch_id: The ID of VSwitch.
               * `engine_version`- (Optional, ForceNew) Engine version. Supported values: 2.8, 4.0 and 5.0. Default value: 2.8. Only 2.8 can be supported for Memcache Instance.
               * `security_ips`- (Optional) Set the instance's IP whitelist of the default security group.
               * `private_ip`- (Optional) Set the instance's private IP.
               * `backup_id`- (Optional) If an instance created based on a backup set generated by another instance is valid, this parameter indicates the ID of the generated backup set.
               * `vpc_auth_mode`- (Optional) Only meaningful if instance_type is `Redis` and network type is VPC. Valid values are `Close`, `Open`. Defaults to `Open`.  `Close` means the redis instance can be accessed without authentication. `Open` means authentication is required.
        
        The **parameters** object supports the following:
        
          * `name` (`pulumi.Input[str]`)
          * `value` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/kvstore_instance.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["auto_renew"] = auto_renew
        __props__["auto_renew_period"] = auto_renew_period
        __props__["availability_zone"] = availability_zone
        __props__["backup_id"] = backup_id
        __props__["connection_domain"] = connection_domain
        __props__["engine_version"] = engine_version
        __props__["instance_charge_type"] = instance_charge_type
        __props__["instance_class"] = instance_class
        __props__["instance_name"] = instance_name
        __props__["instance_type"] = instance_type
        __props__["kms_encrypted_password"] = kms_encrypted_password
        __props__["kms_encryption_context"] = kms_encryption_context
        __props__["maintain_end_time"] = maintain_end_time
        __props__["maintain_start_time"] = maintain_start_time
        __props__["parameters"] = parameters
        __props__["password"] = password
        __props__["period"] = period
        __props__["private_ip"] = private_ip
        __props__["security_ips"] = security_ips
        __props__["tags"] = tags
        __props__["vpc_auth_mode"] = vpc_auth_mode
        __props__["vswitch_id"] = vswitch_id
        return Instance(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

