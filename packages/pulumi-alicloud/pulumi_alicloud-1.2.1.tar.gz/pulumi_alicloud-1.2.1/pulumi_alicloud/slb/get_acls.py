# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetAclsResult:
    """
    A collection of values returned by getAcls.
    """
    def __init__(__self__, acls=None, ids=None, name_regex=None, names=None, output_file=None, resource_group_id=None, tags=None, id=None):
        if acls and not isinstance(acls, list):
            raise TypeError("Expected argument 'acls' to be a list")
        __self__.acls = acls
        """
        A list of SLB  acls. Each element contains the following attributes:
        """
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        __self__.ids = ids
        """
        A list of SLB acls IDs.
        """
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        __self__.name_regex = name_regex
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        __self__.names = names
        """
        A list of SLB acls names.
        """
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        __self__.output_file = output_file
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        __self__.resource_group_id = resource_group_id
        """
        Resource group ID.
        """
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        __self__.tags = tags
        """
        A mapping of tags to assign to the resource.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetAclsResult(GetAclsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAclsResult(
            acls=self.acls,
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            resource_group_id=self.resource_group_id,
            tags=self.tags,
            id=self.id)

def get_acls(ids=None,name_regex=None,output_file=None,resource_group_id=None,tags=None,opts=None):
    """
    This data source provides the acls in the region.
    
    ## Entry Block
    
    The entry mapping supports the following:
    
    * `entry`   - An IP addresses or CIDR blocks.
    * `comment` - the comment of the entry.
    
    ## Listener Block
    
    The Listener mapping supports the following:
    
    * `load_balancer_id` - the id of load balancer instance, the listener belongs to.
    * `frontend_port` - the listener port.
    * `protocol`      - the listener protocol (such as tcp/udp/http/https, etc).
    * `acl_type`      - the type of acl (such as white/black).
    
    :param list ids: A list of acls IDs to filter results.
    :param str name_regex: A regex string to filter results by acl name.
    :param str resource_group_id: The Id of resource group which acl belongs.
    :param dict tags: A mapping of tags to assign to the resource.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/d/slb_acls.html.markdown.
    """
    __args__ = dict()

    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['resourceGroupId'] = resource_group_id
    __args__['tags'] = tags
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:slb/getAcls:getAcls', __args__, opts=opts).value

    return AwaitableGetAclsResult(
        acls=__ret__.get('acls'),
        ids=__ret__.get('ids'),
        name_regex=__ret__.get('nameRegex'),
        names=__ret__.get('names'),
        output_file=__ret__.get('outputFile'),
        resource_group_id=__ret__.get('resourceGroupId'),
        tags=__ret__.get('tags'),
        id=__ret__.get('id'))
