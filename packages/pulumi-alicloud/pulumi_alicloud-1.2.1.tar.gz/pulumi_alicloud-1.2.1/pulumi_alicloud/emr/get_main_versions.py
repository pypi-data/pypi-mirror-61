# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetMainVersionsResult:
    """
    A collection of values returned by getMainVersions.
    """
    def __init__(__self__, cluster_types=None, emr_version=None, ids=None, main_versions=None, output_file=None, id=None):
        if cluster_types and not isinstance(cluster_types, list):
            raise TypeError("Expected argument 'cluster_types' to be a list")
        __self__.cluster_types = cluster_types
        if emr_version and not isinstance(emr_version, str):
            raise TypeError("Expected argument 'emr_version' to be a str")
        __self__.emr_version = emr_version
        """
        The version of the emr cluster instance.
        """
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        __self__.ids = ids
        """
        A list of emr instance types IDs. 
        """
        if main_versions and not isinstance(main_versions, list):
            raise TypeError("Expected argument 'main_versions' to be a list")
        __self__.main_versions = main_versions
        """
        A list of versions of the emr cluster instance. Each element contains the following attributes:
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
class AwaitableGetMainVersionsResult(GetMainVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMainVersionsResult(
            cluster_types=self.cluster_types,
            emr_version=self.emr_version,
            ids=self.ids,
            main_versions=self.main_versions,
            output_file=self.output_file,
            id=self.id)

def get_main_versions(cluster_types=None,emr_version=None,output_file=None,opts=None):
    """
    The `emr.getMainVersions` data source provides a collection of emr 
    main versions available in Alibaba Cloud account when create a emr cluster.
    
    > **NOTE:** Available in 1.59.0+
    
    :param list cluster_types: The supported clusterType of this emr version.
           Possible values may be any one or combination of these: ["HADOOP", "DRUID", "KAFKA", "ZOOKEEPER", "FLINK", "CLICKHOUSE"]
    :param str emr_version: The version of the emr cluster instance. Possible values: `EMR-4.0.0`, `EMR-3.23.0`, `EMR-3.22.0`.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-alicloud/blob/master/website/docs/d/emr_main_versions.html.markdown.
    """
    __args__ = dict()

    __args__['clusterTypes'] = cluster_types
    __args__['emrVersion'] = emr_version
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:emr/getMainVersions:getMainVersions', __args__, opts=opts).value

    return AwaitableGetMainVersionsResult(
        cluster_types=__ret__.get('clusterTypes'),
        emr_version=__ret__.get('emrVersion'),
        ids=__ret__.get('ids'),
        main_versions=__ret__.get('mainVersions'),
        output_file=__ret__.get('outputFile'),
        id=__ret__.get('id'))
