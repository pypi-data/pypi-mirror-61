# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class ReadOnlyInstance(pulumi.CustomResource):
    connection_string: pulumi.Output[str]
    """
    RDS database connection string.
    """
    engine: pulumi.Output[str]
    """
    Database type.
    """
    engine_version: pulumi.Output[str]
    """
    Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/26228.htm) `EngineVersion`.
    """
    instance_name: pulumi.Output[str]
    """
    The name of DB instance. It a string of 2 to 256 characters.
    """
    instance_storage: pulumi.Output[float]
    """
    User-defined DB instance storage space. Value range: [5, 2000] for MySQL/SQL Server HA dual node edition. Increase progressively at a rate of 5 GB. For details, see [Instance type table](https://www.alibabacloud.com/help/doc-detail/26312.htm).
    """
    instance_type: pulumi.Output[str]
    """
    DB Instance type. For details, see [Instance type table](https://www.alibabacloud.com/help/doc-detail/26312.htm).
    """
    master_db_instance_id: pulumi.Output[str]
    """
    ID of the master instance.
    """
    parameters: pulumi.Output[list]
    """
    Set of parameters needs to be set after DB instance was launched. Available parameters can refer to the latest docs [View database parameter templates](https://www.alibabacloud.com/help/doc-detail/26284.htm).
    
      * `name` (`str`)
      * `value` (`str`)
    """
    port: pulumi.Output[str]
    """
    RDS database connection port.
    """
    tags: pulumi.Output[dict]
    """
    A mapping of tags to assign to the resource.
    - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
    - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
    """
    vswitch_id: pulumi.Output[str]
    """
    The virtual switch ID to launch DB instances in one VPC.
    """
    zone_id: pulumi.Output[str]
    """
    The Zone to launch the DB instance.
    """
    def __init__(__self__, resource_name, opts=None, engine_version=None, instance_name=None, instance_storage=None, instance_type=None, master_db_instance_id=None, parameters=None, tags=None, vswitch_id=None, zone_id=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an RDS readonly instance resource. 
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] engine_version: Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/26228.htm) `EngineVersion`.
        :param pulumi.Input[str] instance_name: The name of DB instance. It a string of 2 to 256 characters.
        :param pulumi.Input[float] instance_storage: User-defined DB instance storage space. Value range: [5, 2000] for MySQL/SQL Server HA dual node edition. Increase progressively at a rate of 5 GB. For details, see [Instance type table](https://www.alibabacloud.com/help/doc-detail/26312.htm).
        :param pulumi.Input[str] instance_type: DB Instance type. For details, see [Instance type table](https://www.alibabacloud.com/help/doc-detail/26312.htm).
        :param pulumi.Input[str] master_db_instance_id: ID of the master instance.
        :param pulumi.Input[list] parameters: Set of parameters needs to be set after DB instance was launched. Available parameters can refer to the latest docs [View database parameter templates](https://www.alibabacloud.com/help/doc-detail/26284.htm).
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
               - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
               - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
        :param pulumi.Input[str] vswitch_id: The virtual switch ID to launch DB instances in one VPC.
        :param pulumi.Input[str] zone_id: The Zone to launch the DB instance.
        
        The **parameters** object supports the following:
        
          * `name` (`pulumi.Input[str]`)
          * `value` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/db_readonly_instance.html.markdown.
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

            if engine_version is None:
                raise TypeError("Missing required property 'engine_version'")
            __props__['engine_version'] = engine_version
            __props__['instance_name'] = instance_name
            if instance_storage is None:
                raise TypeError("Missing required property 'instance_storage'")
            __props__['instance_storage'] = instance_storage
            if instance_type is None:
                raise TypeError("Missing required property 'instance_type'")
            __props__['instance_type'] = instance_type
            if master_db_instance_id is None:
                raise TypeError("Missing required property 'master_db_instance_id'")
            __props__['master_db_instance_id'] = master_db_instance_id
            __props__['parameters'] = parameters
            __props__['tags'] = tags
            __props__['vswitch_id'] = vswitch_id
            __props__['zone_id'] = zone_id
            __props__['connection_string'] = None
            __props__['engine'] = None
            __props__['port'] = None
        super(ReadOnlyInstance, __self__).__init__(
            'alicloud:rds/readOnlyInstance:ReadOnlyInstance',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, connection_string=None, engine=None, engine_version=None, instance_name=None, instance_storage=None, instance_type=None, master_db_instance_id=None, parameters=None, port=None, tags=None, vswitch_id=None, zone_id=None):
        """
        Get an existing ReadOnlyInstance resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] connection_string: RDS database connection string.
        :param pulumi.Input[str] engine: Database type.
        :param pulumi.Input[str] engine_version: Database version. Value options can refer to the latest docs [CreateDBInstance](https://www.alibabacloud.com/help/doc-detail/26228.htm) `EngineVersion`.
        :param pulumi.Input[str] instance_name: The name of DB instance. It a string of 2 to 256 characters.
        :param pulumi.Input[float] instance_storage: User-defined DB instance storage space. Value range: [5, 2000] for MySQL/SQL Server HA dual node edition. Increase progressively at a rate of 5 GB. For details, see [Instance type table](https://www.alibabacloud.com/help/doc-detail/26312.htm).
        :param pulumi.Input[str] instance_type: DB Instance type. For details, see [Instance type table](https://www.alibabacloud.com/help/doc-detail/26312.htm).
        :param pulumi.Input[str] master_db_instance_id: ID of the master instance.
        :param pulumi.Input[list] parameters: Set of parameters needs to be set after DB instance was launched. Available parameters can refer to the latest docs [View database parameter templates](https://www.alibabacloud.com/help/doc-detail/26284.htm).
        :param pulumi.Input[str] port: RDS database connection port.
        :param pulumi.Input[dict] tags: A mapping of tags to assign to the resource.
               - Key: It can be up to 64 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It cannot be a null string.
               - Value: It can be up to 128 characters in length. It cannot begin with "aliyun", "acs:", "http://", or "https://". It can be a null string.
        :param pulumi.Input[str] vswitch_id: The virtual switch ID to launch DB instances in one VPC.
        :param pulumi.Input[str] zone_id: The Zone to launch the DB instance.
        
        The **parameters** object supports the following:
        
          * `name` (`pulumi.Input[str]`)
          * `value` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/db_readonly_instance.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["connection_string"] = connection_string
        __props__["engine"] = engine
        __props__["engine_version"] = engine_version
        __props__["instance_name"] = instance_name
        __props__["instance_storage"] = instance_storage
        __props__["instance_type"] = instance_type
        __props__["master_db_instance_id"] = master_db_instance_id
        __props__["parameters"] = parameters
        __props__["port"] = port
        __props__["tags"] = tags
        __props__["vswitch_id"] = vswitch_id
        __props__["zone_id"] = zone_id
        return ReadOnlyInstance(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

