# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

__config__ = pulumi.Config('alicloud')

access_key = __config__.get('accessKey') or utilities.get_env('ALICLOUD_ACCESS_KEY')
"""
The access key for API operations. You can retrieve this from the 'Security Management' section of the Alibaba Cloud
console.
"""

account_id = __config__.get('accountId') or utilities.get_env('ALICLOUD_ACCOUNT_ID')
"""
The account ID for some service API operations. You can retrieve this from the 'Security Settings' section of the
Alibaba Cloud console.
"""

assume_role = __config__.get('assumeRole')

configuration_source = __config__.get('configurationSource')
"""
Use this to mark a terraform configuration file source.
"""

ecs_role_name = __config__.get('ecsRoleName') or utilities.get_env('ALICLOUD_ECS_ROLE_NAME')
"""
The RAM Role Name attached on a ECS instance for API operations. You can retrieve this from the 'Access Control' section
of the Alibaba Cloud console.
"""

endpoints = __config__.get('endpoints')

fc = __config__.get('fc')

log_endpoint = __config__.get('logEndpoint')

mns_endpoint = __config__.get('mnsEndpoint')

ots_instance_name = __config__.get('otsInstanceName')

profile = __config__.get('profile') or utilities.get_env('ALICLOUD_PROFILE')
"""
The profile for API operations. If not set, the default profile created with `aliyun configure` will be used.
"""

region = __config__.get('region') or utilities.get_env('ALICLOUD_REGION')
"""
The region where Alibaba Cloud operations will take place. Examples are cn-beijing, cn-hangzhou, eu-central-1, etc.
"""

secret_key = __config__.get('secretKey') or utilities.get_env('ALICLOUD_SECRET_KEY')
"""
The secret key for API operations. You can retrieve this from the 'Security Management' section of the Alibaba Cloud
console.
"""

security_token = __config__.get('securityToken') or utilities.get_env('ALICLOUD_SECURITY_TOKEN')
"""
security token. A security token is only required if you are using Security Token Service.
"""

shared_credentials_file = __config__.get('sharedCredentialsFile') or utilities.get_env('ALICLOUD_SHARED_CREDENTIALS_FILE')
"""
The path to the shared credentials file. If not set this defaults to ~/.aliyun/config.json
"""

skip_region_validation = __config__.get('skipRegionValidation')
"""
Skip static validation of region ID. Used by users of alternative AlibabaCloud-like APIs or users w/ access to regions
that are not public (yet).
"""

