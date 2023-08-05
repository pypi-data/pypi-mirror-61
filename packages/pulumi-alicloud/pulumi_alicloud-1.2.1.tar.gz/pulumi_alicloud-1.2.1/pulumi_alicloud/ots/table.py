# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class Table(pulumi.CustomResource):
    deviation_cell_version_in_sec: pulumi.Output[str]
    """
    The max version offset of the table. The valid value is 1-9223372036854775807. Defaults to 86400.
    """
    instance_name: pulumi.Output[str]
    """
    The name of the OTS instance in which table will located.
    """
    max_version: pulumi.Output[float]
    """
    The maximum number of versions stored in this table. The valid value is 1-2147483647.
    """
    primary_keys: pulumi.Output[list]
    """
    The property of `TableMeta` which indicates the structure information of a table. It describes the attribute value of primary key. The number of `primary_key` should not be less than one and not be more than four.
    
      * `name` (`str`) - Name for primary key.
      * `type` (`str`) - Type for primary key. Only `Integer`, `String` or `Binary` is allowed.
    """
    table_name: pulumi.Output[str]
    """
    The table name of the OTS instance. If changed, a new table would be created.
    """
    time_to_live: pulumi.Output[float]
    """
    The retention time of data stored in this table (unit: second). The value maximum is 2147483647 and -1 means never expired.
    """
    def __init__(__self__, resource_name, opts=None, deviation_cell_version_in_sec=None, instance_name=None, max_version=None, primary_keys=None, table_name=None, time_to_live=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an OTS table resource.
        
        > **NOTE:** From Provider version 1.10.0, the provider field 'ots_instance_name' has been deprecated and
        you should use resource alicloud_ots_table's new field 'instance_name' and 'table_name' to re-import this resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] deviation_cell_version_in_sec: The max version offset of the table. The valid value is 1-9223372036854775807. Defaults to 86400.
        :param pulumi.Input[str] instance_name: The name of the OTS instance in which table will located.
        :param pulumi.Input[float] max_version: The maximum number of versions stored in this table. The valid value is 1-2147483647.
        :param pulumi.Input[list] primary_keys: The property of `TableMeta` which indicates the structure information of a table. It describes the attribute value of primary key. The number of `primary_key` should not be less than one and not be more than four.
        :param pulumi.Input[str] table_name: The table name of the OTS instance. If changed, a new table would be created.
        :param pulumi.Input[float] time_to_live: The retention time of data stored in this table (unit: second). The value maximum is 2147483647 and -1 means never expired.
        
        The **primary_keys** object supports the following:
        
          * `name` (`pulumi.Input[str]`) - Name for primary key.
          * `type` (`pulumi.Input[str]`) - Type for primary key. Only `Integer`, `String` or `Binary` is allowed.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/ots_table.html.markdown.
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

            __props__['deviation_cell_version_in_sec'] = deviation_cell_version_in_sec
            if instance_name is None:
                raise TypeError("Missing required property 'instance_name'")
            __props__['instance_name'] = instance_name
            if max_version is None:
                raise TypeError("Missing required property 'max_version'")
            __props__['max_version'] = max_version
            if primary_keys is None:
                raise TypeError("Missing required property 'primary_keys'")
            __props__['primary_keys'] = primary_keys
            if table_name is None:
                raise TypeError("Missing required property 'table_name'")
            __props__['table_name'] = table_name
            if time_to_live is None:
                raise TypeError("Missing required property 'time_to_live'")
            __props__['time_to_live'] = time_to_live
        super(Table, __self__).__init__(
            'alicloud:ots/table:Table',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, deviation_cell_version_in_sec=None, instance_name=None, max_version=None, primary_keys=None, table_name=None, time_to_live=None):
        """
        Get an existing Table resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] deviation_cell_version_in_sec: The max version offset of the table. The valid value is 1-9223372036854775807. Defaults to 86400.
        :param pulumi.Input[str] instance_name: The name of the OTS instance in which table will located.
        :param pulumi.Input[float] max_version: The maximum number of versions stored in this table. The valid value is 1-2147483647.
        :param pulumi.Input[list] primary_keys: The property of `TableMeta` which indicates the structure information of a table. It describes the attribute value of primary key. The number of `primary_key` should not be less than one and not be more than four.
        :param pulumi.Input[str] table_name: The table name of the OTS instance. If changed, a new table would be created.
        :param pulumi.Input[float] time_to_live: The retention time of data stored in this table (unit: second). The value maximum is 2147483647 and -1 means never expired.
        
        The **primary_keys** object supports the following:
        
          * `name` (`pulumi.Input[str]`) - Name for primary key.
          * `type` (`pulumi.Input[str]`) - Type for primary key. Only `Integer`, `String` or `Binary` is allowed.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/r/ots_table.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["deviation_cell_version_in_sec"] = deviation_cell_version_in_sec
        __props__["instance_name"] = instance_name
        __props__["max_version"] = max_version
        __props__["primary_keys"] = primary_keys
        __props__["table_name"] = table_name
        __props__["time_to_live"] = time_to_live
        return Table(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

