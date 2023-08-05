# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetNetworksResult:
    """
    A collection of values returned by getNetworks.
    """
    def __init__(__self__, ids=None, name_regex=None, names=None, networks=None, output_file=None, id=None):
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        __self__.ids = ids
        """
        A list of CCN instances IDs.
        """
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        __self__.name_regex = name_regex
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        __self__.names = names
        """
        A list of CCN instances names. 
        """
        if networks and not isinstance(networks, list):
            raise TypeError("Expected argument 'networks' to be a list")
        __self__.networks = networks
        """
        A list of CCN instances. Each element contains the following attributes:
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
class AwaitableGetNetworksResult(GetNetworksResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetNetworksResult(
            ids=self.ids,
            name_regex=self.name_regex,
            names=self.names,
            networks=self.networks,
            output_file=self.output_file,
            id=self.id)

def get_networks(ids=None,name_regex=None,output_file=None,opts=None):
    """
    This data source provides Cloud Connect Networks available to the user.
    
    > **NOTE:** Available in 1.59.0+
    
    > **NOTE:** Only the following regions support create Cloud Connect Network. [`cn-shanghai`, `cn-shanghai-finance-1`, `cn-hongkong`, `ap-southeast-1`, `ap-southeast-2`, `ap-southeast-3`, `ap-southeast-5`, `ap-northeast-1`, `eu-central-1`]
    
    :param list ids: A list of CCN instances IDs.
    :param str name_regex: A regex string to filter CCN instances by name.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/d/cloud_connect_networks.html.markdown.
    """
    __args__ = dict()

    __args__['ids'] = ids
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:cloudconnect/getNetworks:getNetworks', __args__, opts=opts).value

    return AwaitableGetNetworksResult(
        ids=__ret__.get('ids'),
        name_regex=__ret__.get('nameRegex'),
        names=__ret__.get('names'),
        networks=__ret__.get('networks'),
        output_file=__ret__.get('outputFile'),
        id=__ret__.get('id'))
