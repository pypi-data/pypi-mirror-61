# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GetDetectorResult:
    """
    A collection of values returned by getDetector.
    """
    def __init__(__self__, finding_publishing_frequency=None, id=None, service_role_arn=None, status=None):
        if finding_publishing_frequency and not isinstance(finding_publishing_frequency, str):
            raise TypeError("Expected argument 'finding_publishing_frequency' to be a str")
        __self__.finding_publishing_frequency = finding_publishing_frequency
        """
        The frequency of notifications sent about subsequent finding occurrences.
        """
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        __self__.id = id
        if service_role_arn and not isinstance(service_role_arn, str):
            raise TypeError("Expected argument 'service_role_arn' to be a str")
        __self__.service_role_arn = service_role_arn
        """
        The service-linked role that grants GuardDuty access to the resources in the AWS account.
        """
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        __self__.status = status
        """
        The current status of the detector.
        """
class AwaitableGetDetectorResult(GetDetectorResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDetectorResult(
            finding_publishing_frequency=self.finding_publishing_frequency,
            id=self.id,
            service_role_arn=self.service_role_arn,
            status=self.status)

def get_detector(id=None,opts=None):
    """
    Retrieve information about a GuardDuty detector.
    
    :param str id: The ID of the detector.

    > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/d/guardduty_detector.html.markdown.
    """
    __args__ = dict()

    __args__['id'] = id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = utilities.get_version()
    __ret__ = pulumi.runtime.invoke('aws:guardduty/getDetector:getDetector', __args__, opts=opts).value

    return AwaitableGetDetectorResult(
        finding_publishing_frequency=__ret__.get('findingPublishingFrequency'),
        id=__ret__.get('id'),
        service_role_arn=__ret__.get('serviceRoleArn'),
        status=__ret__.get('status'))
