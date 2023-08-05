# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetApisResult:
    """
    A collection of values returned by getApis.
    """
    def __init__(__self__, api_id=None, apis=None, group_id=None, ids=None, name_regex=None, names=None, output_file=None, id=None):
        if api_id and not isinstance(api_id, str):
            raise TypeError("Expected argument 'api_id' to be a str")
        __self__.api_id = api_id
        if apis and not isinstance(apis, list):
            raise TypeError("Expected argument 'apis' to be a list")
        __self__.apis = apis
        """
        A list of apis. Each element contains the following attributes:
        """
        if group_id and not isinstance(group_id, str):
            raise TypeError("Expected argument 'group_id' to be a str")
        __self__.group_id = group_id
        """
        The group id that the apis belong to.
        """
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        __self__.ids = ids
        """
        A list of api IDs. 
        """
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        __self__.name_regex = name_regex
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        __self__.names = names
        """
        A list of api names. 
        """
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        __self__.output_file = output_file
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetApisResult(GetApisResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetApisResult(
            api_id=self.api_id,
            apis=self.apis,
            group_id=self.group_id,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            id=self.id)

def get_apis(api_id=None,group_id=None,ids=None,name_regex=None,output_file=None,opts=None):
    """
    This data source provides the apis of the current Alibaba Cloud user.
    
    :param str api_id: (It has been deprecated from version 1.52.2, and use field 'ids' to replace.) ID of the specified API.
    :param str group_id: ID of the specified group.
    :param list ids: A list of api IDs. 
    :param str name_regex: A regex string to filter api gateway apis by name.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/d/api_gateway_apis.html.markdown.
    """
    __args__ = dict()

    __args__['apiId'] = api_id
    __args__['groupId'] = group_id
    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:apigateway/getApis:getApis', __args__, opts=opts).value

    return AwaitableGetApisResult(
        api_id=__ret__.get('apiId'),
        apis=__ret__.get('apis'),
        group_id=__ret__.get('groupId'),
        ids=__ret__.get('ids'),
        name_regex=__ret__.get('nameRegex'),
        names=__ret__.get('names'),
        output_file=__ret__.get('outputFile'),
        id=__ret__.get('id'))
