"""
# Targets for AWS Elastic Load Balancing V2

<!--BEGIN STABILITY BANNER-->---


![Stability: Experimental](https://img.shields.io/badge/stability-Experimental-important.svg?style=for-the-badge)

> **This is a *developer preview* (public beta) module. Releases might lack important features and might have
> future breaking changes.**
>
> This API is still under active development and subject to non-backward
> compatible changes or removal in any future version. Use of the API is not recommended in production
> environments. Experimental APIs are not subject to the Semantic Versioning model.

---
<!--END STABILITY BANNER-->

This package contains targets for ELBv2. See the README of the `@aws-cdk/aws-elasticloadbalancingv2` library.
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.assets
import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticloadbalancingv2-targets", "1.23.0", __name__, "aws-elasticloadbalancingv2-targets@1.23.0.jsii.tgz")


@jsii.implements(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget)
class InstanceIdTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.InstanceIdTarget"):
    """An EC2 instance that is the target for load balancing.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can connect to the instance.

    stability
    :stability: experimental
    """
    def __init__(self, instance_id: str, port: typing.Optional[jsii.Number]=None) -> None:
        """Create a new Instance target.

        :param instance_id: Instance ID of the instance to register to.
        :param port: Override the default port for the target group.

        stability
        :stability: experimental
        """
        jsii.create(InstanceIdTarget, self, [instance_id, port])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


class InstanceTarget(InstanceIdTarget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.InstanceTarget"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, instance: aws_cdk.aws_ec2.Instance, port: typing.Optional[jsii.Number]=None) -> None:
        """Create a new Instance target.

        :param instance: Instance to register to.
        :param port: Override the default port for the target group.

        stability
        :stability: experimental
        """
        jsii.create(InstanceTarget, self, [instance, port])


@jsii.implements(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget)
class IpTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.IpTarget"):
    """An IP address that is a target for load balancing.

    Specify IP addresses from the subnets of the virtual private cloud (VPC) for
    the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and
    192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify
    publicly routable IP addresses.

    If you register a target of this type, you are responsible for making
    sure the load balancer's security group can send packets to the IP address.

    stability
    :stability: experimental
    """
    def __init__(self, ip_address: str, port: typing.Optional[jsii.Number]=None, availability_zone: typing.Optional[str]=None) -> None:
        """Create a new IPAddress target.

        The availabilityZone parameter determines whether the target receives
        traffic from the load balancer nodes in the specified Availability Zone
        or from all enabled Availability Zones for the load balancer.

        This parameter is not supported if the target type of the target group
        is instance. If the IP address is in a subnet of the VPC for the target
        group, the Availability Zone is automatically detected and this
        parameter is optional. If the IP address is outside the VPC, this
        parameter is required.

        With an Application Load Balancer, if the IP address is outside the VPC
        for the target group, the only supported value is all.

        Default is automatic.

        :param ip_address: The IP Address to load balance to.
        :param port: Override the group's default port.
        :param availability_zone: Availability zone to send traffic from.

        stability
        :stability: experimental
        """
        jsii.create(IpTarget, self, [ip_address, port, availability_zone])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


@jsii.implements(aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget)
class LambdaTarget(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticloadbalancingv2-targets.LambdaTarget"):
    """
    stability
    :stability: experimental
    """
    def __init__(self, fn: aws_cdk.aws_lambda.IFunction) -> None:
        """Create a new Lambda target.

        :param fn: -

        stability
        :stability: experimental
        """
        jsii.create(LambdaTarget, self, [fn])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.IApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.INetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Register this instance target with a load balancer.

        Don't call this, it is called automatically when you add the target to a
        load balancer.

        :param target_group: -

        stability
        :stability: experimental
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])


__all__ = ["InstanceIdTarget", "InstanceTarget", "IpTarget", "LambdaTarget", "__jsii_assembly__"]

publication.publish()
