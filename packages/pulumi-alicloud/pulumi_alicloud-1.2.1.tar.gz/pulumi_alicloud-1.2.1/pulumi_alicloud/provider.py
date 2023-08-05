# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class Provider(pulumi.ProviderResource):
    def __init__(__self__, resource_name, opts=None, access_key=None, account_id=None, assume_role=None, configuration_source=None, ecs_role_name=None, endpoints=None, fc=None, log_endpoint=None, mns_endpoint=None, ots_instance_name=None, profile=None, region=None, secret_key=None, security_token=None, shared_credentials_file=None, skip_region_validation=None, __props__=None, __name__=None, __opts__=None):
        """
        The provider type for the alicloud package. By default, resources use package-wide configuration
        settings, however an explicit `Provider` instance may be created and passed during resource
        construction to achieve fine-grained programmatic control over provider settings. See the
        [documentation](https://www.pulumi.com/docs/reference/programming-model/#providers) for more information.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        
        The **assume_role** object supports the following:
        
          * `policy` (`pulumi.Input[str]`)
          * `roleArn` (`pulumi.Input[str]`)
          * `sessionExpiration` (`pulumi.Input[float]`)
          * `sessionName` (`pulumi.Input[str]`)
        
        The **endpoints** object supports the following:
        
          * `actiontrail` (`pulumi.Input[str]`)
          * `alikafka` (`pulumi.Input[str]`)
          * `apigateway` (`pulumi.Input[str]`)
          * `bssopenapi` (`pulumi.Input[str]`)
          * `cas` (`pulumi.Input[str]`)
          * `cdn` (`pulumi.Input[str]`)
          * `cen` (`pulumi.Input[str]`)
          * `cms` (`pulumi.Input[str]`)
          * `cr` (`pulumi.Input[str]`)
          * `cs` (`pulumi.Input[str]`)
          * `datahub` (`pulumi.Input[str]`)
          * `ddosbgp` (`pulumi.Input[str]`)
          * `ddoscoo` (`pulumi.Input[str]`)
          * `dds` (`pulumi.Input[str]`)
          * `dns` (`pulumi.Input[str]`)
          * `drds` (`pulumi.Input[str]`)
          * `ecs` (`pulumi.Input[str]`)
          * `elasticsearch` (`pulumi.Input[str]`)
          * `emr` (`pulumi.Input[str]`)
          * `ess` (`pulumi.Input[str]`)
          * `fc` (`pulumi.Input[str]`)
          * `gpdb` (`pulumi.Input[str]`)
          * `kms` (`pulumi.Input[str]`)
          * `kvstore` (`pulumi.Input[str]`)
          * `location` (`pulumi.Input[str]`)
          * `log` (`pulumi.Input[str]`)
          * `market` (`pulumi.Input[str]`)
          * `mns` (`pulumi.Input[str]`)
          * `nas` (`pulumi.Input[str]`)
          * `ons` (`pulumi.Input[str]`)
          * `oss` (`pulumi.Input[str]`)
          * `ots` (`pulumi.Input[str]`)
          * `polardb` (`pulumi.Input[str]`)
          * `pvtz` (`pulumi.Input[str]`)
          * `ram` (`pulumi.Input[str]`)
          * `rds` (`pulumi.Input[str]`)
          * `slb` (`pulumi.Input[str]`)
          * `sts` (`pulumi.Input[str]`)
          * `vpc` (`pulumi.Input[str]`)

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/index.html.markdown.
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

            if access_key is None:
                access_key = utilities.get_env('ALICLOUD_ACCESS_KEY')
            __props__['access_key'] = access_key
            if account_id is None:
                account_id = utilities.get_env('ALICLOUD_ACCOUNT_ID')
            __props__['account_id'] = account_id
            __props__['assume_role'] = pulumi.Output.from_input(assume_role).apply(json.dumps) if assume_role is not None else None
            __props__['configuration_source'] = configuration_source
            if ecs_role_name is None:
                ecs_role_name = utilities.get_env('ALICLOUD_ECS_ROLE_NAME')
            __props__['ecs_role_name'] = ecs_role_name
            __props__['endpoints'] = pulumi.Output.from_input(endpoints).apply(json.dumps) if endpoints is not None else None
            __props__['fc'] = fc
            __props__['log_endpoint'] = log_endpoint
            __props__['mns_endpoint'] = mns_endpoint
            __props__['ots_instance_name'] = ots_instance_name
            if profile is None:
                profile = utilities.get_env('ALICLOUD_PROFILE')
            __props__['profile'] = profile
            if region is None:
                region = utilities.get_env('ALICLOUD_REGION')
            __props__['region'] = region
            if secret_key is None:
                secret_key = utilities.get_env('ALICLOUD_SECRET_KEY')
            __props__['secret_key'] = secret_key
            if security_token is None:
                security_token = utilities.get_env('ALICLOUD_SECURITY_TOKEN')
            __props__['security_token'] = security_token
            if shared_credentials_file is None:
                shared_credentials_file = utilities.get_env('ALICLOUD_SHARED_CREDENTIALS_FILE')
            __props__['shared_credentials_file'] = shared_credentials_file
            __props__['skip_region_validation'] = pulumi.Output.from_input(skip_region_validation).apply(json.dumps) if skip_region_validation is not None else None
        super(Provider, __self__).__init__(
            'alicloud',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None):
        """
        Get an existing Provider resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/index.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        return Provider(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

