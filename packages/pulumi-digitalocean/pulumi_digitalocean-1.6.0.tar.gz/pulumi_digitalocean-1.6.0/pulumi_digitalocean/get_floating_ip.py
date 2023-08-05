# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class GetFloatingIpResult:
    """
    A collection of values returned by getFloatingIp.
    """
    def __init__(__self__, droplet_id=None, ip_address=None, region=None, urn=None, id=None):
        if droplet_id and not isinstance(droplet_id, float):
            raise TypeError("Expected argument 'droplet_id' to be a float")
        __self__.droplet_id = droplet_id
        if ip_address and not isinstance(ip_address, str):
            raise TypeError("Expected argument 'ip_address' to be a str")
        __self__.ip_address = ip_address
        if region and not isinstance(region, str):
            raise TypeError("Expected argument 'region' to be a str")
        __self__.region = region
        if urn and not isinstance(urn, str):
            raise TypeError("Expected argument 'urn' to be a str")
        __self__.urn = urn
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        """
        id is the provider-assigned unique ID for this managed resource.
        """
class AwaitableGetFloatingIpResult(GetFloatingIpResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetFloatingIpResult(
            droplet_id=self.droplet_id,
            ip_address=self.ip_address,
            region=self.region,
            urn=self.urn,
            id=self.id)

def get_floating_ip(ip_address=None,opts=None):
    """
    Use this data source to access information about an existing resource.
    
    :param str ip_address: The allocated IP address of the specific floating IP to retrieve.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-digitalocean/blob/master/website/docs/d/floating_ip.html.markdown.
    """
    __args__ = dict()

    __args__['ipAddress'] = ip_address
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('digitalocean:index/getFloatingIp:getFloatingIp', __args__, opts=opts).value

    return AwaitableGetFloatingIpResult(
        droplet_id=__ret__.get('dropletId'),
        ip_address=__ret__.get('ipAddress'),
        region=__ret__.get('region'),
        urn=__ret__.get('urn'),
        id=__ret__.get('id'))
