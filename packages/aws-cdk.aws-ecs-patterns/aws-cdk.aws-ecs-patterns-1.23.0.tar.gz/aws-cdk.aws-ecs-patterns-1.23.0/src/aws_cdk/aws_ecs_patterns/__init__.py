"""
# CDK Construct library for higher-level ECS Constructs

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This library provides higher-level Amazon ECS constructs which follow common architectural patterns. It contains:

* Application Load Balanced Services
* Network Load Balanced Services
* Queue Processing Services
* Scheduled Tasks (cron jobs)
* Additional Examples

## Application Load Balanced Services

To define an Amazon ECS service that is behind an application load balancer, instantiate one of the following:

* `ApplicationLoadBalancedEc2Service`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balanced_ecs_service = ecs_patterns.ApplicationLoadBalancedEc2Service(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("test"),
        "environment": {
            "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
            "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
        }
    },
    desired_count=2
)
```

* `ApplicationLoadBalancedFargateService`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balanced_fargate_service = ecs_patterns.ApplicationLoadBalancedFargateService(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    }
)
```

Instead of providing a cluster you can specify a VPC and CDK will create a new ECS cluster.
If you deploy multiple services CDK will only create one cluster per VPC.

You can omit `cluster` and `vpc` to let CDK create a new VPC with two AZs and create a cluster inside this VPC.

Additionally, if more than one application target group are needed, instantiate one of the following:

* `ApplicationMultipleTargetGroupsEc2Service`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# One application load balancer with one listener and two target groups.
load_balanced_ec2_service = ApplicationMultipleTargetGroupsEc2Service(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=256,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    },
    target_groups=[{
        "container_port": 80
    }, {
        "container_port": 90,
        "path_pattern": "a/b/c",
        "priority": 10
    }
    ]
)
```

* `ApplicationMultipleTargetGroupsFargateService`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# One application load balancer with one listener and two target groups.
load_balanced_fargate_service = ApplicationMultipleTargetGroupsFargateService(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    },
    target_groups=[{
        "container_port": 80
    }, {
        "container_port": 90,
        "path_pattern": "a/b/c",
        "priority": 10
    }
    ]
)
```

## Network Load Balanced Services

To define an Amazon ECS service that is behind a network load balancer, instantiate one of the following:

* `NetworkLoadBalancedEc2Service`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balanced_ecs_service = ecs_patterns.NetworkLoadBalancedEc2Service(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("test"),
        "environment": {
            "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
            "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
        }
    },
    desired_count=2
)
```

* `NetworkLoadBalancedFargateService`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
load_balanced_fargate_service = ecs_patterns.NetworkLoadBalancedFargateService(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    cpu=512,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    }
)
```

The CDK will create a new Amazon ECS cluster if you specify a VPC and omit `cluster`. If you deploy multiple services the CDK will only create one cluster per VPC.

If `cluster` and `vpc` are omitted, the CDK creates a new VPC with subnets in two Availability Zones and a cluster within this VPC.

Additionally, if more than one network target group is needed, instantiate one of the following:

* NetworkMultipleTargetGroupsEc2Service

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Two network load balancers, each with their own listener and target group.
load_balanced_ec2_service = NetworkMultipleTargetGroupsEc2Service(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=256,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    },
    load_balancers=[{
        "name": "lb1",
        "listeners": [{
            "name": "listener1"
        }
        ]
    }, {
        "name": "lb2",
        "listeners": [{
            "name": "listener2"
        }
        ]
    }
    ],
    target_groups=[{
        "container_port": 80,
        "listener": "listener1"
    }, {
        "container_port": 90,
        "listener": "listener2"
    }
    ]
)
```

* NetworkMultipleTargetGroupsFargateService

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Two network load balancers, each with their own listener and target group.
load_balanced_fargate_service = NetworkMultipleTargetGroupsFargateService(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    },
    load_balancers=[{
        "name": "lb1",
        "listeners": [{
            "name": "listener1"
        }
        ]
    }, {
        "name": "lb2",
        "listeners": [{
            "name": "listener2"
        }
        ]
    }
    ],
    target_groups=[{
        "container_port": 80,
        "listener": "listener1"
    }, {
        "container_port": 90,
        "listener": "listener2"
    }
    ]
)
```

## Queue Processing Services

To define a service that creates a queue and reads from that queue, instantiate one of the following:

* `QueueProcessingEc2Service`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
queue_processing_ec2_service = QueueProcessingEc2Service(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={
        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
    },
    queue=queue,
    max_scaling_capacity=5
)
```

* `QueueProcessingFargateService`

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
queue_processing_fargate_service = QueueProcessingFargateService(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=512,
    image=ecs.ContainerImage.from_registry("test"),
    command=["-c", "4", "amazon.com"],
    enable_logging=False,
    desired_task_count=2,
    environment={
        "TEST_ENVIRONMENT_VARIABLE1": "test environment variable 1 value",
        "TEST_ENVIRONMENT_VARIABLE2": "test environment variable 2 value"
    },
    queue=queue,
    max_scaling_capacity=5
)
```

## Scheduled Tasks

To define a task that runs periodically, instantiate an `ScheduledEc2Task`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
# Instantiate an Amazon EC2 Task to run at a scheduled interval
ecs_scheduled_task = ScheduledEc2Task(stack, "ScheduledTask",
    cluster=cluster,
    scheduled_ec2_task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample"),
        "memory_limit_mi_b": 256,
        "environment": {"name": "TRIGGER", "value": "CloudWatch Events"}
    },
    schedule=events.Schedule.expression("rate(1 minute)")
)
```

## Additional Examples

In addition to using the constructs, users can also add logic to customize these constructs:

### Add Schedule-Based Auto-Scaling to an ApplicationLoadBalancedFargateService

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from aws_cdk.aws_applicationautoscaling import Schedule
from ..application_load_balanced_fargate_service import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedFargateServiceProps

load_balanced_fargate_service = ApplicationLoadBalancedFargateService(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    }
)

scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
    min_capacity=5,
    max_capacity=20
)

scalable_target.scale_on_schedule("DaytimeScaleDown",
    schedule=Schedule.cron(hour="8", minute="0"),
    min_capacity=1
)

scalable_target.scale_on_schedule("EveningRushScaleUp",
    schedule=Schedule.cron(hour="20", minute="0"),
    min_capacity=10
)
```

### Add Metric-Based Auto-Scaling to an ApplicationLoadBalancedFargateService

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from ..application_load_balanced_fargate_service import ApplicationLoadBalancedFargateService

load_balanced_fargate_service = ApplicationLoadBalancedFargateService(stack, "Service",
    cluster=cluster,
    memory_limit_mi_b=1024,
    desired_count=1,
    cpu=512,
    task_image_options={
        "image": ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")
    }
)

scalable_target = load_balanced_fargate_service.service.auto_scale_task_count(
    min_capacity=1,
    max_capacity=20
)

scalable_target.scale_on_cpu_utilization("CpuScaling",
    target_utilization_percent=50
)

scalable_target.scale_on_memory_utilization("MemoryScaling",
    target_utilization_percent=50
)
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

import aws_cdk.aws_applicationautoscaling
import aws_cdk.aws_certificatemanager
import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_events
import aws_cdk.aws_events_targets
import aws_cdk.aws_iam
import aws_cdk.aws_route53
import aws_cdk.aws_route53_targets
import aws_cdk.aws_servicediscovery
import aws_cdk.aws_sqs
import aws_cdk.core

__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecs-patterns", "1.23.0", __name__, "aws-ecs-patterns@1.23.0.jsii.tgz")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationListenerProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'certificate': 'certificate', 'port': 'port', 'protocol': 'protocol'})
class ApplicationListenerProps():
    def __init__(self, *, name: str, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, port: typing.Optional[jsii.Number]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None):
        """Properties to define an application listener.

        :param name: Name of the listener.
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param port: The port on which the listener listens for requests. Default: - Determined from protocol if known.
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: ApplicationProtocol.HTTP. If a certificate is specified, the protocol will be set by default to ApplicationProtocol.HTTPS.
        """
        self._values = {
            'name': name,
        }
        if certificate is not None: self._values["certificate"] = certificate
        if port is not None: self._values["port"] = port
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def name(self) -> str:
        """Name of the listener."""
        return self._values.get('name')

    @builtins.property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.
        """
        return self._values.get('certificate')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: - Determined from protocol if known.
        """
        return self._values.get('port')

    @builtins.property
    def protocol(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        ApplicationProtocol.HTTP. If a certificate is specified, the protocol will be
        set by default to ApplicationProtocol.HTTPS.
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationLoadBalancedServiceBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedServiceBase"):
    """The base class for ApplicationLoadBalancedEc2Service and ApplicationLoadBalancedFargateService services."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ApplicationLoadBalancedServiceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ApplicationLoadBalancedServiceBase class.

        :param scope: -
        :param id: -
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ApplicationLoadBalancedServiceBaseProps(certificate=certificate, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, protocol=protocol, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationLoadBalancedServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """Adds service as a target of the target group.

        :param service: -
        """
        return jsii.invoke(self, "addServiceAsTarget", [service])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> aws_cdk.aws_ecs.AwsLogDriver:
        """
        :param prefix: -
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: aws_cdk.core.Construct, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_ecs.Cluster:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster that hosts the service."""
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service."""
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationListener:
        """The listener for the service."""
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer:
        """The Application Load Balancer for the service."""
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup:
        """The target group for the service."""
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="certificate")
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer."""
        return jsii.get(self, "certificate")


class _ApplicationLoadBalancedServiceBaseProxy(ApplicationLoadBalancedServiceBase):
    pass

class ApplicationLoadBalancedEc2Service(ApplicationLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedEc2Service"):
    """An EC2 service running on an ECS cluster fronted by an application load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ApplicationLoadBalancedEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ApplicationLoadBalancedEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, certificate=certificate, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, protocol=protocol, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationLoadBalancedEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The EC2 service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.Ec2TaskDefinition:
        """The EC2 Task Definition in this construct."""
        return jsii.get(self, "taskDefinition")


class ApplicationLoadBalancedFargateService(ApplicationLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedFargateService"):
    """A Fargate service running on an ECS cluster fronted by an application load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ApplicationLoadBalancedFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ApplicationLoadBalancedFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, task_definition=task_definition, certificate=certificate, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, protocol=protocol, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationLoadBalancedFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        """Determines whether the service will be assigned a public IP address."""
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        """The Fargate task definition in this construct."""
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedServiceBaseProps", jsii_struct_bases=[], name_mapping={'certificate': 'certificate', 'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'protocol': 'protocol', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class ApplicationLoadBalancedServiceBaseProps():
    def __init__(self, *, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The properties for the base ApplicationLoadBalancedEc2Service or ApplicationLoadBalancedFargateService service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if certificate is not None: self._values["certificate"] = certificate
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if protocol is not None: self._values["protocol"] = protocol
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.
        """
        return self._values.get('certificate')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the application load balancer that will serve traffic to the service.

        default
        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
          port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]:
        """The application load balancer that will serve traffic to the service.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def protocol(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.
        """
        return self._values.get('protocol')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        default
        :default: none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedEc2ServiceProps", jsii_struct_bases=[ApplicationLoadBalancedServiceBaseProps], name_mapping={'certificate': 'certificate', 'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'protocol': 'protocol', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class ApplicationLoadBalancedEc2ServiceProps(ApplicationLoadBalancedServiceBaseProps):
    def __init__(self, *, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None):
        """The properties for the ApplicationLoadBalancedEc2Service service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if certificate is not None: self._values["certificate"] = certificate
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if protocol is not None: self._values["protocol"] = protocol
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.
        """
        return self._values.get('certificate')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the application load balancer that will serve traffic to the service.

        default
        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
          port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]:
        """The application load balancer that will serve traffic to the service.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def protocol(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.
        """
        return self._values.get('protocol')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        default
        :default: none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: none
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both..

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedFargateServiceProps", jsii_struct_bases=[ApplicationLoadBalancedServiceBaseProps], name_mapping={'certificate': 'certificate', 'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'protocol': 'protocol', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'task_definition': 'taskDefinition'})
class ApplicationLoadBalancedFargateServiceProps(ApplicationLoadBalancedServiceBaseProps):
    def __init__(self, *, certificate: typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, protocol: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None):
        """The properties for the ApplicationLoadBalancedFargateService service.

        :param certificate: Certificate Manager certificate to associate with the load balancer. Setting this option will set the load balancer protocol to HTTPS. Default: - No certificate associated with the load balancer, if using the HTTP protocol. For HTTPS, a DNS-validated certificate will be created for the load balancer's specified domain name.
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the application load balancer that will serve traffic to the service. Default: - The default listener port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        :param load_balancer: The application load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param protocol: The protocol for connections from clients to the load balancer. The load balancer port is determined from the protocol (port 80 for HTTP, port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS. Default: HTTP. If a certificate is specified, the protocol will be set by default to HTTPS.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. TaskDefinition or TaskImageOptions must be specified, but not both. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if certificate is not None: self._values["certificate"] = certificate
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if protocol is not None: self._values["protocol"] = protocol
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def certificate(self) -> typing.Optional[aws_cdk.aws_certificatemanager.ICertificate]:
        """Certificate Manager certificate to associate with the load balancer.

        Setting this option will set the load balancer protocol to HTTPS.

        default
        :default:

        - No certificate associated with the load balancer, if using
          the HTTP protocol. For HTTPS, a DNS-validated certificate will be
          created for the load balancer's specified domain name.
        """
        return self._values.get('certificate')

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the application load balancer that will serve traffic to the service.

        default
        :default:

        - The default listener port is determined from the protocol (port 80 for HTTP,
          port 443 for HTTPS). A domain name and zone must be also be specified if using HTTPS.
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer]:
        """The application load balancer that will serve traffic to the service.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def protocol(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationProtocol]:
        """The protocol for connections from clients to the load balancer.

        The load balancer port is determined from the protocol (port 80 for
        HTTP, port 443 for HTTPS).  A domain name and zone must be also be
        specified if using HTTPS.

        default
        :default:

        HTTP. If a certificate is specified, the protocol will be
        set by default to HTTPS.
        """
        return self._values.get('protocol')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        TaskDefinition or TaskImageOptions must be specified, but not both.

        default
        :default: none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedTaskImageOptions", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_port': 'containerPort', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class ApplicationLoadBalancedTaskImageOptions():
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """
        :param image: The image used to start a container. Image or taskDefinition must be specified, not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: 80
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_port is not None: self._values["container_port"] = container_port
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        Image or taskDefinition must be specified, not both.

        default
        :default: - none
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - none
        """
        return self._values.get('container_name')

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: 80
        """
        return self._values.get('container_port')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedTaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancedTaskImageProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_ports': 'containerPorts', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class ApplicationLoadBalancedTaskImageProps():
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, container_name: typing.Optional[str]=None, container_ports: typing.Optional[typing.List[jsii.Number]]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Options for configuring a new container.

        :param image: The image used to start a container. Image or taskDefinition must be specified, not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - web
        :param container_ports: A list of port numbers on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: - [80]
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secrets to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_ports is not None: self._values["container_ports"] = container_ports
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        Image or taskDefinition must be specified, not both.

        default
        :default: - none
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - web
        """
        return self._values.get('container_name')

    @builtins.property
    def container_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        """A list of port numbers on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: - [80]
        """
        return self._values.get('container_ports')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secrets to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancedTaskImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationLoadBalancerProps", jsii_struct_bases=[], name_mapping={'listeners': 'listeners', 'name': 'name', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'public_load_balancer': 'publicLoadBalancer'})
class ApplicationLoadBalancerProps():
    def __init__(self, *, listeners: typing.List["ApplicationListenerProps"], name: str, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, public_load_balancer: typing.Optional[bool]=None):
        """Properties to define an application load balancer.

        :param listeners: Listeners (at least one listener) attached to this load balancer.
        :param name: Name of the load balancer.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        """
        self._values = {
            'listeners': listeners,
            'name': name,
        }
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer

    @builtins.property
    def listeners(self) -> typing.List["ApplicationListenerProps"]:
        """Listeners (at least one listener) attached to this load balancer."""
        return self._values.get('listeners')

    @builtins.property
    def name(self) -> str:
        """Name of the load balancer."""
        return self._values.get('name')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ApplicationMultipleTargetGroupsServiceBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsServiceBase"):
    """The base class for ApplicationMultipleTargetGroupsEc2Service and ApplicationMultipleTargetGroupsFargateService classes."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ApplicationMultipleTargetGroupsServiceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ApplicationMultipleTargetGroupsServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ApplicationMultipleTargetGroupsServiceBaseProps(cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationMultipleTargetGroupsServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addPortMappingForTargets")
    def _add_port_mapping_for_targets(self, container: aws_cdk.aws_ecs.ContainerDefinition, targets: typing.List["ApplicationTargetProps"]) -> None:
        """
        :param container: -
        :param targets: -
        """
        return jsii.invoke(self, "addPortMappingForTargets", [container, targets])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> aws_cdk.aws_ecs.AwsLogDriver:
        """
        :param prefix: -
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="findListener")
    def _find_listener(self, name: typing.Optional[str]=None) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationListener:
        """
        :param name: -
        """
        return jsii.invoke(self, "findListener", [name])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: aws_cdk.core.Construct, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_ecs.Cluster:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @jsii.member(jsii_name="registerECSTargets")
    def _register_ecs_targets(self, service: aws_cdk.aws_ecs.BaseService, container: aws_cdk.aws_ecs.ContainerDefinition, targets: typing.List["ApplicationTargetProps"]) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup:
        """
        :param service: -
        :param container: -
        :param targets: -
        """
        return jsii.invoke(self, "registerECSTargets", [service, container, targets])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster that hosts the service."""
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service."""
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationListener:
        """The default listener for the service (first added listener)."""
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationLoadBalancer:
        """The default Application Load Balancer for the service (first added load balancer)."""
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def _listeners(self) -> typing.List[aws_cdk.aws_elasticloadbalancingv2.ApplicationListener]:
        return jsii.get(self, "listeners")

    @_listeners.setter
    def _listeners(self, value: typing.List[aws_cdk.aws_elasticloadbalancingv2.ApplicationListener]):
        jsii.set(self, "listeners", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroups")
    def _target_groups(self) -> typing.List[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup]:
        return jsii.get(self, "targetGroups")

    @_target_groups.setter
    def _target_groups(self, value: typing.List[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup]):
        jsii.set(self, "targetGroups", value)

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def _log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        return jsii.get(self, "logDriver")

    @_log_driver.setter
    def _log_driver(self, value: typing.Optional[aws_cdk.aws_ecs.LogDriver]):
        jsii.set(self, "logDriver", value)


class _ApplicationMultipleTargetGroupsServiceBaseProxy(ApplicationMultipleTargetGroupsServiceBase):
    pass

class ApplicationMultipleTargetGroupsEc2Service(ApplicationMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsEc2Service"):
    """An EC2 service running on an ECS cluster fronted by an application load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ApplicationMultipleTargetGroupsEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ApplicationMultipleTargetGroupsEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationMultipleTargetGroupsEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The EC2 service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup:
        """The default target group for the service."""
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.Ec2TaskDefinition:
        """The EC2 Task Definition in this construct."""
        return jsii.get(self, "taskDefinition")


class ApplicationMultipleTargetGroupsFargateService(ApplicationMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsFargateService"):
    """A Fargate service running on an ECS cluster fronted by an application load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ApplicationMultipleTargetGroupsFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ApplicationMultipleTargetGroupsFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(ApplicationMultipleTargetGroupsFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        """Determines whether the service will be assigned a public IP address."""
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup:
        """The default target group for the service."""
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        """The Fargate task definition in this construct."""
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsServiceBaseProps", jsii_struct_bases=[], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class ApplicationMultipleTargetGroupsServiceBaseProps():
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The properties for the base ApplicationMultipleTargetGroupsEc2Service or ApplicationMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["ApplicationLoadBalancerProps"]]:
        """The application load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["ApplicationTargetProps"]]:
        """Properties to specify ALB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationMultipleTargetGroupsServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsEc2ServiceProps", jsii_struct_bases=[ApplicationMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class ApplicationMultipleTargetGroupsEc2ServiceProps(ApplicationMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None):
        """The properties for the ApplicationMultipleTargetGroupsEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["ApplicationLoadBalancerProps"]]:
        """The application load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["ApplicationTargetProps"]]:
        """Properties to specify ALB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        Valid values, which determines your range of valid values for the memory parameter:

        default
        :default: - No minimum CPU units reserved.
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        Note that this setting will be ignored if TaskImagesOptions is specified

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationMultipleTargetGroupsEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationMultipleTargetGroupsFargateServiceProps", jsii_struct_bases=[ApplicationMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'task_definition': 'taskDefinition'})
class ApplicationMultipleTargetGroupsFargateServiceProps(ApplicationMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["ApplicationLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["ApplicationTargetProps"]]=None, task_image_options: typing.Optional["ApplicationLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None):
        """The properties for the ApplicationMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The application load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify ALB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = ApplicationLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["ApplicationLoadBalancerProps"]]:
        """The application load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["ApplicationTargetProps"]]:
        """Properties to specify ALB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["ApplicationLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationMultipleTargetGroupsFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ApplicationTargetProps", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'host_header': 'hostHeader', 'listener': 'listener', 'path_pattern': 'pathPattern', 'priority': 'priority', 'protocol': 'protocol'})
class ApplicationTargetProps():
    def __init__(self, *, container_port: jsii.Number, host_header: typing.Optional[str]=None, listener: typing.Optional[str]=None, path_pattern: typing.Optional[str]=None, priority: typing.Optional[jsii.Number]=None, protocol: typing.Optional[aws_cdk.aws_ecs.Protocol]=None):
        """Properties to define an application target group.

        :param container_port: The port number of the container. Only applicable when using application/network load balancers.
        :param host_header: Rule applies if the requested host matches the indicated host. May contain up to three '*' wildcards. Requires that priority is set. Default: No host condition
        :param listener: Name of the listener the target group attached to. Default: - default listener (first added listener)
        :param path_pattern: Rule applies if the requested path matches the given path pattern. May contain up to three '*' wildcards. Requires that priority is set. Default: No path condition
        :param priority: Priority of this target group. The rule with the lowest priority will be used for every request. If priority is not given, these target groups will be added as defaults, and must not have conditions. Priorities must be unique. Default: Target groups are used as defaults
        :param protocol: The protocol used for the port mapping. Only applicable when using application load balancers. Default: ecs.Protocol.TCP
        """
        self._values = {
            'container_port': container_port,
        }
        if host_header is not None: self._values["host_header"] = host_header
        if listener is not None: self._values["listener"] = listener
        if path_pattern is not None: self._values["path_pattern"] = path_pattern
        if priority is not None: self._values["priority"] = priority
        if protocol is not None: self._values["protocol"] = protocol

    @builtins.property
    def container_port(self) -> jsii.Number:
        """The port number of the container.

        Only applicable when using application/network load balancers.
        """
        return self._values.get('container_port')

    @builtins.property
    def host_header(self) -> typing.Optional[str]:
        """Rule applies if the requested host matches the indicated host.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No host condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#host-conditions
        """
        return self._values.get('host_header')

    @builtins.property
    def listener(self) -> typing.Optional[str]:
        """Name of the listener the target group attached to.

        default
        :default: - default listener (first added listener)
        """
        return self._values.get('listener')

    @builtins.property
    def path_pattern(self) -> typing.Optional[str]:
        """Rule applies if the requested path matches the given path pattern.

        May contain up to three '*' wildcards.

        Requires that priority is set.

        default
        :default: No path condition

        see
        :see: https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-listeners.html#path-conditions
        """
        return self._values.get('path_pattern')

    @builtins.property
    def priority(self) -> typing.Optional[jsii.Number]:
        """Priority of this target group.

        The rule with the lowest priority will be used for every request.
        If priority is not given, these target groups will be added as
        defaults, and must not have conditions.

        Priorities must be unique.

        default
        :default: Target groups are used as defaults
        """
        return self._values.get('priority')

    @builtins.property
    def protocol(self) -> typing.Optional[aws_cdk.aws_ecs.Protocol]:
        """The protocol used for the port mapping.

        Only applicable when using application load balancers.

        default
        :default: ecs.Protocol.TCP
        """
        return self._values.get('protocol')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ApplicationTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkListenerProps", jsii_struct_bases=[], name_mapping={'name': 'name', 'port': 'port'})
class NetworkListenerProps():
    def __init__(self, *, name: str, port: typing.Optional[jsii.Number]=None):
        """Properties to define an network listener.

        :param name: Name of the listener.
        :param port: The port on which the listener listens for requests. Default: 80
        """
        self._values = {
            'name': name,
        }
        if port is not None: self._values["port"] = port

    @builtins.property
    def name(self) -> str:
        """Name of the listener."""
        return self._values.get('name')

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        """The port on which the listener listens for requests.

        default
        :default: 80
        """
        return self._values.get('port')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkListenerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkLoadBalancedServiceBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedServiceBase"):
    """The base class for NetworkLoadBalancedEc2Service and NetworkLoadBalancedFargateService services."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _NetworkLoadBalancedServiceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the NetworkLoadBalancedServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = NetworkLoadBalancedServiceBaseProps(cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkLoadBalancedServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addServiceAsTarget")
    def _add_service_as_target(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """Adds service as a target of the target group.

        :param service: -
        """
        return jsii.invoke(self, "addServiceAsTarget", [service])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> aws_cdk.aws_ecs.AwsLogDriver:
        """
        :param prefix: -
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: aws_cdk.core.Construct, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_ecs.Cluster:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster that hosts the service."""
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service."""
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkListener:
        """The listener for the service."""
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer:
        """The Network Load Balancer for the service."""
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup:
        """The target group for the service."""
        return jsii.get(self, "targetGroup")


class _NetworkLoadBalancedServiceBaseProxy(NetworkLoadBalancedServiceBase):
    pass

class NetworkLoadBalancedEc2Service(NetworkLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedEc2Service"):
    """An EC2 service running on an ECS cluster fronted by a network load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the NetworkLoadBalancedEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = NetworkLoadBalancedEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkLoadBalancedEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The ECS service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.Ec2TaskDefinition:
        """The EC2 Task Definition in this construct."""
        return jsii.get(self, "taskDefinition")


class NetworkLoadBalancedFargateService(NetworkLoadBalancedServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedFargateService"):
    """A Fargate service running on an ECS cluster fronted by a network load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the NetworkLoadBalancedFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = NetworkLoadBalancedFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, domain_name=domain_name, domain_zone=domain_zone, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, listener_port=listener_port, load_balancer=load_balancer, max_healthy_percent=max_healthy_percent, min_healthy_percent=min_healthy_percent, propagate_tags=propagate_tags, public_load_balancer=public_load_balancer, service_name=service_name, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkLoadBalancedFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        """The Fargate task definition in this construct."""
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedServiceBaseProps", jsii_struct_bases=[], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class NetworkLoadBalancedServiceBaseProps():
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The properties for the base NetworkLoadBalancedEc2Service or NetworkLoadBalancedFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the network load balancer that will serve traffic to the service.

        default
        :default: 80
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]:
        """The network load balancer that will serve traffic to the service.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        default
        :default: - none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedEc2ServiceProps", jsii_struct_bases=[NetworkLoadBalancedServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class NetworkLoadBalancedEc2ServiceProps(NetworkLoadBalancedServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None):
        """The properties for the NetworkLoadBalancedEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the network load balancer that will serve traffic to the service.

        default
        :default: 80
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]:
        """The network load balancer that will serve traffic to the service.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        default
        :default: - none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: none
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both..

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedFargateServiceProps", jsii_struct_bases=[NetworkLoadBalancedServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'listener_port': 'listenerPort', 'load_balancer': 'loadBalancer', 'max_healthy_percent': 'maxHealthyPercent', 'min_healthy_percent': 'minHealthyPercent', 'propagate_tags': 'propagateTags', 'public_load_balancer': 'publicLoadBalancer', 'service_name': 'serviceName', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'task_definition': 'taskDefinition'})
class NetworkLoadBalancedFargateServiceProps(NetworkLoadBalancedServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, listener_port: typing.Optional[jsii.Number]=None, load_balancer: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]=None, max_healthy_percent: typing.Optional[jsii.Number]=None, min_healthy_percent: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, public_load_balancer: typing.Optional[bool]=None, service_name: typing.Optional[str]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageOptions"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None):
        """The properties for the NetworkLoadBalancedFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param listener_port: Listener port of the network load balancer that will serve traffic to the service. Default: 80
        :param load_balancer: The network load balancer that will serve traffic to the service. [disable-awslint:ref-via-interface] Default: - a new load balancer will be created.
        :param max_healthy_percent: The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment. Default: - 100 if daemon, otherwise 200
        :param min_healthy_percent: The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment. Default: - 0 if daemon, otherwise 50
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param task_image_options: The properties required to create a new task definition. One of taskImageOptions or taskDefinition must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageOptions(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if listener_port is not None: self._values["listener_port"] = listener_port
        if load_balancer is not None: self._values["load_balancer"] = load_balancer
        if max_healthy_percent is not None: self._values["max_healthy_percent"] = max_healthy_percent
        if min_healthy_percent is not None: self._values["min_healthy_percent"] = min_healthy_percent
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer
        if service_name is not None: self._values["service_name"] = service_name
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        """Listener port of the network load balancer that will serve traffic to the service.

        default
        :default: 80
        """
        return self._values.get('listener_port')

    @builtins.property
    def load_balancer(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer]:
        """The network load balancer that will serve traffic to the service.

        [disable-awslint:ref-via-interface]

        default
        :default: - a new load balancer will be created.
        """
        return self._values.get('load_balancer')

    @builtins.property
    def max_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The maximum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that can run in a service during a deployment.

        default
        :default: - 100 if daemon, otherwise 200
        """
        return self._values.get('max_healthy_percent')

    @builtins.property
    def min_healthy_percent(self) -> typing.Optional[jsii.Number]:
        """The minimum number of tasks, specified as a percentage of the Amazon ECS service's DesiredCount value, that must continue to run and remain healthy during a deployment.

        default
        :default: - 0 if daemon, otherwise 50
        """
        return self._values.get('min_healthy_percent')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageOptions"]:
        """The properties required to create a new task definition.

        One of taskImageOptions or taskDefinition must be specified.

        default
        :default: - none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]:
        """The task definition to use for tasks in the service. TaskDefinition or TaskImageOptions must be specified, but not both.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedTaskImageOptions", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_port': 'containerPort', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class NetworkLoadBalancedTaskImageOptions():
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, container_name: typing.Optional[str]=None, container_port: typing.Optional[jsii.Number]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """
        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_port: The port number on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: 80
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_port is not None: self._values["container_port"] = container_port
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - none
        """
        return self._values.get('container_name')

    @builtins.property
    def container_port(self) -> typing.Optional[jsii.Number]:
        """The port number on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: 80
        """
        return self._values.get('container_port')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedTaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancedTaskImageProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'container_name': 'containerName', 'container_ports': 'containerPorts', 'enable_logging': 'enableLogging', 'environment': 'environment', 'execution_role': 'executionRole', 'family': 'family', 'log_driver': 'logDriver', 'secrets': 'secrets', 'task_role': 'taskRole'})
class NetworkLoadBalancedTaskImageProps():
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, container_name: typing.Optional[str]=None, container_ports: typing.Optional[typing.List[jsii.Number]]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, execution_role: typing.Optional[aws_cdk.aws_iam.IRole]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, task_role: typing.Optional[aws_cdk.aws_iam.IRole]=None):
        """Options for configuring a new container.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param container_name: The container name value to be specified in the task definition. Default: - none
        :param container_ports: A list of port numbers on the container that is bound to the user-specified or automatically assigned host port. If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort. If you are using containers in a task with the bridge network mode and you specify a container port and not a host port, your container automatically receives a host port in the ephemeral port range. Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance. For more information, see `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_. Default: - [80]
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. Default: - No environment variables.
        :param execution_role: The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf. Default: - No value
        :param family: The name of a family that this task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secrets to expose to the container as an environment variable. Default: - No secret environment variables.
        :param task_role: The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf. Default: - A task role is automatically created for you.
        """
        self._values = {
            'image': image,
        }
        if container_name is not None: self._values["container_name"] = container_name
        if container_ports is not None: self._values["container_ports"] = container_ports
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if execution_role is not None: self._values["execution_role"] = execution_role
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if task_role is not None: self._values["task_role"] = task_role

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none
        """
        return self._values.get('image')

    @builtins.property
    def container_name(self) -> typing.Optional[str]:
        """The container name value to be specified in the task definition.

        default
        :default: - none
        """
        return self._values.get('container_name')

    @builtins.property
    def container_ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        """A list of port numbers on the container that is bound to the user-specified or automatically assigned host port.

        If you are using containers in a task with the awsvpc or host network mode, exposed ports should be specified using containerPort.
        If you are using containers in a task with the bridge network mode and you specify a container port and not a host port,
        your container automatically receives a host port in the ephemeral port range.

        Port mappings that are automatically assigned in this way do not count toward the 100 reserved ports limit of a container instance.

        For more information, see
        `hostPort <https://docs.aws.amazon.com/AmazonECS/latest/APIReference/API_PortMapping.html#ECS-Type-PortMapping-hostPort>`_.

        default
        :default: - [80]
        """
        return self._values.get('container_ports')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: - No environment variables.
        """
        return self._values.get('environment')

    @builtins.property
    def execution_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task execution IAM role that grants the Amazon ECS container agent permission to call AWS APIs on your behalf.

        default
        :default: - No value
        """
        return self._values.get('execution_role')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that this task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secrets to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def task_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        """The name of the task IAM role that grants containers in the task permission to call AWS APIs on your behalf.

        default
        :default: - A task role is automatically created for you.
        """
        return self._values.get('task_role')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancedTaskImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkLoadBalancerProps", jsii_struct_bases=[], name_mapping={'listeners': 'listeners', 'name': 'name', 'domain_name': 'domainName', 'domain_zone': 'domainZone', 'public_load_balancer': 'publicLoadBalancer'})
class NetworkLoadBalancerProps():
    def __init__(self, *, listeners: typing.List["NetworkListenerProps"], name: str, domain_name: typing.Optional[str]=None, domain_zone: typing.Optional[aws_cdk.aws_route53.IHostedZone]=None, public_load_balancer: typing.Optional[bool]=None):
        """Properties to define an network load balancer.

        :param listeners: Listeners (at least one listener) attached to this load balancer. Default: - none
        :param name: Name of the load balancer.
        :param domain_name: The domain name for the service, e.g. "api.example.com.". Default: - No domain name.
        :param domain_zone: The Route53 hosted zone for the domain, e.g. "example.com.". Default: - No Route53 hosted domain zone.
        :param public_load_balancer: Determines whether the Load Balancer will be internet-facing. Default: true
        """
        self._values = {
            'listeners': listeners,
            'name': name,
        }
        if domain_name is not None: self._values["domain_name"] = domain_name
        if domain_zone is not None: self._values["domain_zone"] = domain_zone
        if public_load_balancer is not None: self._values["public_load_balancer"] = public_load_balancer

    @builtins.property
    def listeners(self) -> typing.List["NetworkListenerProps"]:
        """Listeners (at least one listener) attached to this load balancer.

        default
        :default: - none
        """
        return self._values.get('listeners')

    @builtins.property
    def name(self) -> str:
        """Name of the load balancer."""
        return self._values.get('name')

    @builtins.property
    def domain_name(self) -> typing.Optional[str]:
        """The domain name for the service, e.g. "api.example.com.".

        default
        :default: - No domain name.
        """
        return self._values.get('domain_name')

    @builtins.property
    def domain_zone(self) -> typing.Optional[aws_cdk.aws_route53.IHostedZone]:
        """The Route53 hosted zone for the domain, e.g. "example.com.".

        default
        :default: - No Route53 hosted domain zone.
        """
        return self._values.get('domain_zone')

    @builtins.property
    def public_load_balancer(self) -> typing.Optional[bool]:
        """Determines whether the Load Balancer will be internet-facing.

        default
        :default: true
        """
        return self._values.get('public_load_balancer')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkLoadBalancerProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class NetworkMultipleTargetGroupsServiceBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsServiceBase"):
    """The base class for NetworkMultipleTargetGroupsEc2Service and NetworkMultipleTargetGroupsFargateService classes."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _NetworkMultipleTargetGroupsServiceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the NetworkMultipleTargetGroupsServiceBase class.

        :param scope: -
        :param id: -
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = NetworkMultipleTargetGroupsServiceBaseProps(cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkMultipleTargetGroupsServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="addPortMappingForTargets")
    def _add_port_mapping_for_targets(self, container: aws_cdk.aws_ecs.ContainerDefinition, targets: typing.List["NetworkTargetProps"]) -> None:
        """
        :param container: -
        :param targets: -
        """
        return jsii.invoke(self, "addPortMappingForTargets", [container, targets])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> aws_cdk.aws_ecs.AwsLogDriver:
        """
        :param prefix: -
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="findListener")
    def _find_listener(self, name: typing.Optional[str]=None) -> aws_cdk.aws_elasticloadbalancingv2.NetworkListener:
        """
        :param name: -
        """
        return jsii.invoke(self, "findListener", [name])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: aws_cdk.core.Construct, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_ecs.Cluster:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @jsii.member(jsii_name="registerECSTargets")
    def _register_ecs_targets(self, service: aws_cdk.aws_ecs.BaseService, container: aws_cdk.aws_ecs.ContainerDefinition, targets: typing.List["NetworkTargetProps"]) -> aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup:
        """
        :param service: -
        :param container: -
        :param targets: -
        """
        return jsii.invoke(self, "registerECSTargets", [service, container, targets])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster that hosts the service."""
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service."""
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="listener")
    def listener(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkListener:
        """The listener for the service."""
        return jsii.get(self, "listener")

    @builtins.property
    @jsii.member(jsii_name="loadBalancer")
    def load_balancer(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkLoadBalancer:
        """The Network Load Balancer for the service."""
        return jsii.get(self, "loadBalancer")

    @builtins.property
    @jsii.member(jsii_name="listeners")
    def _listeners(self) -> typing.List[aws_cdk.aws_elasticloadbalancingv2.NetworkListener]:
        return jsii.get(self, "listeners")

    @_listeners.setter
    def _listeners(self, value: typing.List[aws_cdk.aws_elasticloadbalancingv2.NetworkListener]):
        jsii.set(self, "listeners", value)

    @builtins.property
    @jsii.member(jsii_name="targetGroups")
    def _target_groups(self) -> typing.List[aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup]:
        return jsii.get(self, "targetGroups")

    @_target_groups.setter
    def _target_groups(self, value: typing.List[aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup]):
        jsii.set(self, "targetGroups", value)

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def _log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        return jsii.get(self, "logDriver")

    @_log_driver.setter
    def _log_driver(self, value: typing.Optional[aws_cdk.aws_ecs.LogDriver]):
        jsii.set(self, "logDriver", value)


class _NetworkMultipleTargetGroupsServiceBaseProxy(NetworkMultipleTargetGroupsServiceBase):
    pass

class NetworkMultipleTargetGroupsEc2Service(NetworkMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsEc2Service"):
    """An EC2 service running on an ECS cluster fronted by a network load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the NetworkMultipleTargetGroupsEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = NetworkMultipleTargetGroupsEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkMultipleTargetGroupsEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The EC2 service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup:
        """The default target group for the service."""
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.Ec2TaskDefinition:
        """The EC2 Task Definition in this construct."""
        return jsii.get(self, "taskDefinition")


class NetworkMultipleTargetGroupsFargateService(NetworkMultipleTargetGroupsServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsFargateService"):
    """A Fargate service running on an ECS cluster fronted by a network load balancer."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the NetworkMultipleTargetGroupsFargateService class.

        :param scope: -
        :param id: -
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = NetworkMultipleTargetGroupsFargateServiceProps(assign_public_ip=assign_public_ip, cpu=cpu, memory_limit_mib=memory_limit_mib, task_definition=task_definition, cloud_map_options=cloud_map_options, cluster=cluster, desired_count=desired_count, enable_ecs_managed_tags=enable_ecs_managed_tags, health_check_grace_period=health_check_grace_period, load_balancers=load_balancers, propagate_tags=propagate_tags, service_name=service_name, target_groups=target_groups, task_image_options=task_image_options, vpc=vpc)

        jsii.create(NetworkMultipleTargetGroupsFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="assignPublicIp")
    def assign_public_ip(self) -> bool:
        """Determines whether the service will be assigned a public IP address."""
        return jsii.get(self, "assignPublicIp")

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="targetGroup")
    def target_group(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup:
        """The default target group for the service."""
        return jsii.get(self, "targetGroup")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        """The Fargate task definition in this construct."""
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsServiceBaseProps", jsii_struct_bases=[], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc'})
class NetworkMultipleTargetGroupsServiceBaseProps():
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The properties for the base NetworkMultipleTargetGroupsEc2Service or NetworkMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["NetworkLoadBalancerProps"]]:
        """The network load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """Name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["NetworkTargetProps"]]:
        """Properties to specify NLB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: - none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkMultipleTargetGroupsServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsEc2ServiceProps", jsii_struct_bases=[NetworkMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB', 'task_definition': 'taskDefinition'})
class NetworkMultipleTargetGroupsEc2ServiceProps(NetworkMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]=None):
        """The properties for the NetworkMultipleTargetGroupsEc2Service service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The minimum number of CPU units to reserve for the container. Valid values, which determines your range of valid values for the memory parameter: Default: - No minimum CPU units reserved.
        :param memory_limit_mib: The amount (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under heavy contention, Docker attempts to keep the container memory to this soft limit. However, your container can consume more memory when it needs to, up to either the hard limit specified with the memory parameter (if applicable), or all of the available memory on the container instance, whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required. Note that this setting will be ignored if TaskImagesOptions is specified. Default: - No memory reserved.
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["NetworkLoadBalancerProps"]]:
        """The network load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """Name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["NetworkTargetProps"]]:
        """Properties to specify NLB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: - none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        Valid values, which determines your range of valid values for the memory parameter:

        default
        :default: - No minimum CPU units reserved.
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under heavy contention, Docker attempts to keep the
        container memory to this soft limit. However, your container can consume more
        memory when it needs to, up to either the hard limit specified with the memory
        parameter (if applicable), or all of the available memory on the container
        instance, whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required.

        Note that this setting will be ignored if TaskImagesOptions is specified.

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.Ec2TaskDefinition]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkMultipleTargetGroupsEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkMultipleTargetGroupsFargateServiceProps", jsii_struct_bases=[NetworkMultipleTargetGroupsServiceBaseProps], name_mapping={'cloud_map_options': 'cloudMapOptions', 'cluster': 'cluster', 'desired_count': 'desiredCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'health_check_grace_period': 'healthCheckGracePeriod', 'load_balancers': 'loadBalancers', 'propagate_tags': 'propagateTags', 'service_name': 'serviceName', 'target_groups': 'targetGroups', 'task_image_options': 'taskImageOptions', 'vpc': 'vpc', 'assign_public_ip': 'assignPublicIp', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'task_definition': 'taskDefinition'})
class NetworkMultipleTargetGroupsFargateServiceProps(NetworkMultipleTargetGroupsServiceBaseProps):
    def __init__(self, *, cloud_map_options: typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]=None, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, health_check_grace_period: typing.Optional[aws_cdk.core.Duration]=None, load_balancers: typing.Optional[typing.List["NetworkLoadBalancerProps"]]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, service_name: typing.Optional[str]=None, target_groups: typing.Optional[typing.List["NetworkTargetProps"]]=None, task_image_options: typing.Optional["NetworkLoadBalancedTaskImageProps"]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, assign_public_ip: typing.Optional[bool]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, task_definition: typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]=None):
        """The properties for the NetworkMultipleTargetGroupsFargateService service.

        :param cloud_map_options: The options for configuring an Amazon ECS service to use service discovery. Default: - AWS Cloud Map service discovery is not enabled.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_count: The desired number of instantiations of the task definition to keep running on the service. The minimum value is 1 Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param health_check_grace_period: The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started. Default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        :param load_balancers: The network load balancer that will serve traffic to the service. Default: - a new load balancer with a listener will be created.
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param service_name: Name of the service. Default: - CloudFormation-generated name.
        :param target_groups: Properties to specify NLB target groups. Default: - default portMapping registered as target group and attached to the first defined listener
        :param task_image_options: The properties required to create a new task definition. Only one of TaskDefinition or TaskImageOptions must be specified. Default: - none
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param assign_public_ip: Determines whether the service will be assigned a public IP address. Default: false
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU) 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU) 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU) Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU) Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param task_definition: The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified. [disable-awslint:ref-via-interface] Default: - none
        """
        if isinstance(cloud_map_options, dict): cloud_map_options = aws_cdk.aws_ecs.CloudMapOptions(**cloud_map_options)
        if isinstance(task_image_options, dict): task_image_options = NetworkLoadBalancedTaskImageProps(**task_image_options)
        self._values = {
        }
        if cloud_map_options is not None: self._values["cloud_map_options"] = cloud_map_options
        if cluster is not None: self._values["cluster"] = cluster
        if desired_count is not None: self._values["desired_count"] = desired_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if health_check_grace_period is not None: self._values["health_check_grace_period"] = health_check_grace_period
        if load_balancers is not None: self._values["load_balancers"] = load_balancers
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if service_name is not None: self._values["service_name"] = service_name
        if target_groups is not None: self._values["target_groups"] = target_groups
        if task_image_options is not None: self._values["task_image_options"] = task_image_options
        if vpc is not None: self._values["vpc"] = vpc
        if assign_public_ip is not None: self._values["assign_public_ip"] = assign_public_ip
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if task_definition is not None: self._values["task_definition"] = task_definition

    @builtins.property
    def cloud_map_options(self) -> typing.Optional[aws_cdk.aws_ecs.CloudMapOptions]:
        """The options for configuring an Amazon ECS service to use service discovery.

        default
        :default: - AWS Cloud Map service discovery is not enabled.
        """
        return self._values.get('cloud_map_options')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1

        default
        :default: 1
        """
        return self._values.get('desired_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def health_check_grace_period(self) -> typing.Optional[aws_cdk.core.Duration]:
        """The period of time, in seconds, that the Amazon ECS service scheduler ignores unhealthy Elastic Load Balancing target health checks after a task has first started.

        default
        :default: - defaults to 60 seconds if at least one load balancer is in-use and it is not already set
        """
        return self._values.get('health_check_grace_period')

    @builtins.property
    def load_balancers(self) -> typing.Optional[typing.List["NetworkLoadBalancerProps"]]:
        """The network load balancer that will serve traffic to the service.

        default
        :default: - a new load balancer with a listener will be created.
        """
        return self._values.get('load_balancers')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """Name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def target_groups(self) -> typing.Optional[typing.List["NetworkTargetProps"]]:
        """Properties to specify NLB target groups.

        default
        :default: - default portMapping registered as target group and attached to the first defined listener
        """
        return self._values.get('target_groups')

    @builtins.property
    def task_image_options(self) -> typing.Optional["NetworkLoadBalancedTaskImageProps"]:
        """The properties required to create a new task definition.

        Only one of TaskDefinition or TaskImageOptions must be specified.

        default
        :default: - none
        """
        return self._values.get('task_image_options')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def assign_public_ip(self) -> typing.Optional[bool]:
        """Determines whether the service will be assigned a public IP address.

        default
        :default: false
        """
        return self._values.get('assign_public_ip')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        512 (0.5 GB), 1024 (1 GB), 2048 (2 GB) - Available cpu values: 256 (.25 vCPU)

        1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB) - Available cpu values: 512 (.5 vCPU)

        2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB) - Available cpu values: 1024 (1 vCPU)

        Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB) - Available cpu values: 2048 (2 vCPU)

        Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB) - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def task_definition(self) -> typing.Optional[aws_cdk.aws_ecs.FargateTaskDefinition]:
        """The task definition to use for tasks in the service. Only one of TaskDefinition or TaskImageOptions must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkMultipleTargetGroupsFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.NetworkTargetProps", jsii_struct_bases=[], name_mapping={'container_port': 'containerPort', 'listener': 'listener'})
class NetworkTargetProps():
    def __init__(self, *, container_port: jsii.Number, listener: typing.Optional[str]=None):
        """Properties to define a network load balancer target group.

        :param container_port: The port number of the container. Only applicable when using application/network load balancers.
        :param listener: Name of the listener the target group attached to. Default: - default listener (first added listener)
        """
        self._values = {
            'container_port': container_port,
        }
        if listener is not None: self._values["listener"] = listener

    @builtins.property
    def container_port(self) -> jsii.Number:
        """The port number of the container.

        Only applicable when using application/network load balancers.
        """
        return self._values.get('container_port')

    @builtins.property
    def listener(self) -> typing.Optional[str]:
        """Name of the listener the target group attached to.

        default
        :default: - default listener (first added listener)
        """
        return self._values.get('listener')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'NetworkTargetProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class QueueProcessingServiceBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingServiceBase"):
    """The base class for QueueProcessingEc2Service and QueueProcessingFargateService services."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _QueueProcessingServiceBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, image: aws_cdk.aws_ecs.ContainerImage, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the QueueProcessingServiceBase class.

        :param scope: -
        :param id: -
        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = QueueProcessingServiceBaseProps(image=image, cluster=cluster, command=command, desired_task_count=desired_task_count, enable_ecs_managed_tags=enable_ecs_managed_tags, enable_logging=enable_logging, environment=environment, family=family, log_driver=log_driver, max_scaling_capacity=max_scaling_capacity, propagate_tags=propagate_tags, queue=queue, scaling_steps=scaling_steps, secrets=secrets, service_name=service_name, vpc=vpc)

        jsii.create(QueueProcessingServiceBase, self, [scope, id, props])

    @jsii.member(jsii_name="configureAutoscalingForService")
    def _configure_autoscaling_for_service(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """Configure autoscaling based off of CPU utilization as well as the number of messages visible in the SQS queue.

        :param service: the ECS/Fargate service for which to apply the autoscaling rules to.
        """
        return jsii.invoke(self, "configureAutoscalingForService", [service])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: aws_cdk.core.Construct, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_ecs.Cluster:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @jsii.member(jsii_name="grantPermissionsToService")
    def _grant_permissions_to_service(self, service: aws_cdk.aws_ecs.BaseService) -> None:
        """Grant SQS permissions to an ECS service.

        :param service: the ECS/Fargate service to which to grant SQS permissions.
        """
        return jsii.invoke(self, "grantPermissionsToService", [service])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The cluster where your service will be deployed."""
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredCount")
    def desired_count(self) -> jsii.Number:
        """The minimum number of tasks to run."""
        return jsii.get(self, "desiredCount")

    @builtins.property
    @jsii.member(jsii_name="environment")
    def environment(self) -> typing.Mapping[str,str]:
        """Environment variables that will include the queue name."""
        return jsii.get(self, "environment")

    @builtins.property
    @jsii.member(jsii_name="maxCapacity")
    def max_capacity(self) -> jsii.Number:
        """The maximum number of instances for autoscaling to scale up to."""
        return jsii.get(self, "maxCapacity")

    @builtins.property
    @jsii.member(jsii_name="scalingSteps")
    def scaling_steps(self) -> typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]:
        """The scaling interval for autoscaling based off an SQS Queue size."""
        return jsii.get(self, "scalingSteps")

    @builtins.property
    @jsii.member(jsii_name="sqsQueue")
    def sqs_queue(self) -> aws_cdk.aws_sqs.IQueue:
        """The SQS queue that the service will process from."""
        return jsii.get(self, "sqsQueue")

    @builtins.property
    @jsii.member(jsii_name="logDriver")
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The AwsLogDriver to use for logging if logging is enabled."""
        return jsii.get(self, "logDriver")

    @builtins.property
    @jsii.member(jsii_name="secrets")
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret environment variables."""
        return jsii.get(self, "secrets")


class _QueueProcessingServiceBaseProxy(QueueProcessingServiceBase):
    pass

class QueueProcessingEc2Service(QueueProcessingServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingEc2Service"):
    """Class to create a queue processing EC2 service."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None, image: aws_cdk.aws_ecs.ContainerImage, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the QueueProcessingEc2Service class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = QueueProcessingEc2ServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, memory_reservation_mib=memory_reservation_mib, image=image, cluster=cluster, command=command, desired_task_count=desired_task_count, enable_ecs_managed_tags=enable_ecs_managed_tags, enable_logging=enable_logging, environment=environment, family=family, log_driver=log_driver, max_scaling_capacity=max_scaling_capacity, propagate_tags=propagate_tags, queue=queue, scaling_steps=scaling_steps, secrets=secrets, service_name=service_name, vpc=vpc)

        jsii.create(QueueProcessingEc2Service, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.Ec2Service:
        """The EC2 service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.Ec2TaskDefinition:
        """The EC2 task definition in this construct."""
        return jsii.get(self, "taskDefinition")


class QueueProcessingFargateService(QueueProcessingServiceBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingFargateService"):
    """Class to create a queue processing Fargate service."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, image: aws_cdk.aws_ecs.ContainerImage, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the QueueProcessingFargateService class.

        :param scope: -
        :param id: -
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = QueueProcessingFargateServiceProps(cpu=cpu, memory_limit_mib=memory_limit_mib, image=image, cluster=cluster, command=command, desired_task_count=desired_task_count, enable_ecs_managed_tags=enable_ecs_managed_tags, enable_logging=enable_logging, environment=environment, family=family, log_driver=log_driver, max_scaling_capacity=max_scaling_capacity, propagate_tags=propagate_tags, queue=queue, scaling_steps=scaling_steps, secrets=secrets, service_name=service_name, vpc=vpc)

        jsii.create(QueueProcessingFargateService, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> aws_cdk.aws_ecs.FargateService:
        """The Fargate service in this construct."""
        return jsii.get(self, "service")

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        """The Fargate task definition in this construct."""
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingServiceBaseProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'cluster': 'cluster', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'enable_logging': 'enableLogging', 'environment': 'environment', 'family': 'family', 'log_driver': 'logDriver', 'max_scaling_capacity': 'maxScalingCapacity', 'propagate_tags': 'propagateTags', 'queue': 'queue', 'scaling_steps': 'scalingSteps', 'secrets': 'secrets', 'service_name': 'serviceName', 'vpc': 'vpc'})
class QueueProcessingServiceBaseProps():
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The properties for the base QueueProcessingEc2Service or QueueProcessingFargateService service.

        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        self._values = {
            'image': image,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if queue is not None: self._values["queue"] = queue
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if secrets is not None: self._values["secrets"] = secrets
        if service_name is not None: self._values["service_name"] = service_name
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container."""
        return self._values.get('image')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        default
        :default: 'QUEUE_NAME: queue.queueName'
        """
        return self._values.get('environment')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)
        """
        return self._values.get('max_scaling_capacity')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        default
        :default: 'SQSQueue with CloudFormation-generated name'
        """
        return self._values.get('queue')

    @builtins.property
    def scaling_steps(self) -> typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingServiceBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingEc2ServiceProps", jsii_struct_bases=[QueueProcessingServiceBaseProps], name_mapping={'image': 'image', 'cluster': 'cluster', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'enable_logging': 'enableLogging', 'environment': 'environment', 'family': 'family', 'log_driver': 'logDriver', 'max_scaling_capacity': 'maxScalingCapacity', 'propagate_tags': 'propagateTags', 'queue': 'queue', 'scaling_steps': 'scalingSteps', 'secrets': 'secrets', 'service_name': 'serviceName', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB'})
class QueueProcessingEc2ServiceProps(QueueProcessingServiceBaseProps):
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None):
        """The properties for the QueueProcessingEc2Service service.

        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        """
        self._values = {
            'image': image,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if queue is not None: self._values["queue"] = queue
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if secrets is not None: self._values["secrets"] = secrets
        if service_name is not None: self._values["service_name"] = service_name
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container."""
        return self._values.get('image')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        default
        :default: 'QUEUE_NAME: queue.queueName'
        """
        return self._values.get('environment')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)
        """
        return self._values.get('max_scaling_capacity')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        default
        :default: 'SQSQueue with CloudFormation-generated name'
        """
        return self._values.get('queue')

    @builtins.property
    def scaling_steps(self) -> typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: none
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingEc2ServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.QueueProcessingFargateServiceProps", jsii_struct_bases=[QueueProcessingServiceBaseProps], name_mapping={'image': 'image', 'cluster': 'cluster', 'command': 'command', 'desired_task_count': 'desiredTaskCount', 'enable_ecs_managed_tags': 'enableECSManagedTags', 'enable_logging': 'enableLogging', 'environment': 'environment', 'family': 'family', 'log_driver': 'logDriver', 'max_scaling_capacity': 'maxScalingCapacity', 'propagate_tags': 'propagateTags', 'queue': 'queue', 'scaling_steps': 'scalingSteps', 'secrets': 'secrets', 'service_name': 'serviceName', 'vpc': 'vpc', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB'})
class QueueProcessingFargateServiceProps(QueueProcessingServiceBaseProps):
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, command: typing.Optional[typing.List[str]]=None, desired_task_count: typing.Optional[jsii.Number]=None, enable_ecs_managed_tags: typing.Optional[bool]=None, enable_logging: typing.Optional[bool]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, family: typing.Optional[str]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, max_scaling_capacity: typing.Optional[jsii.Number]=None, propagate_tags: typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]=None, queue: typing.Optional[aws_cdk.aws_sqs.IQueue]=None, scaling_steps: typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, service_name: typing.Optional[str]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None):
        """The properties for the QueueProcessingFargateService service.

        :param image: The image used to start a container.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param enable_ecs_managed_tags: Specifies whether to enable Amazon ECS managed tags for the tasks within the service. For more information, see `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_ Default: false
        :param enable_logging: Flag to indicate whether to enable logging. Default: true
        :param environment: The environment variables to pass to the container. The variable ``QUEUE_NAME`` with value ``queue.queueName`` will always be passed. Default: 'QUEUE_NAME: queue.queueName'
        :param family: The name of a family that the task definition is registered to. A family groups multiple versions of a task definition. Default: - Automatically generated name.
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param max_scaling_capacity: Maximum capacity to scale to. Default: (desiredTaskCount * 2)
        :param propagate_tags: Specifies whether to propagate the tags from the task definition or the service to the tasks in the service. Tags can only be propagated to the tasks within the service during service creation. Default: - none
        :param queue: A queue for which to process items from. If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_ Default: 'SQSQueue with CloudFormation-generated name'
        :param scaling_steps: The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric. Maps a range of metric values to a particular scaling behavior. See `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_ Default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param service_name: The name of the service. Default: - CloudFormation-generated name.
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The amount (in MiB) of memory used by the task. This field is required and you must use one of the following values, which determines your range of valid values for the cpu parameter: 0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU) 1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU) 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU) Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU) Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU) This default is set in the underlying FargateTaskDefinition construct. Default: 512
        """
        self._values = {
            'image': image,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if command is not None: self._values["command"] = command
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if enable_ecs_managed_tags is not None: self._values["enable_ecs_managed_tags"] = enable_ecs_managed_tags
        if enable_logging is not None: self._values["enable_logging"] = enable_logging
        if environment is not None: self._values["environment"] = environment
        if family is not None: self._values["family"] = family
        if log_driver is not None: self._values["log_driver"] = log_driver
        if max_scaling_capacity is not None: self._values["max_scaling_capacity"] = max_scaling_capacity
        if propagate_tags is not None: self._values["propagate_tags"] = propagate_tags
        if queue is not None: self._values["queue"] = queue
        if scaling_steps is not None: self._values["scaling_steps"] = scaling_steps
        if secrets is not None: self._values["secrets"] = secrets
        if service_name is not None: self._values["service_name"] = service_name
        if vpc is not None: self._values["vpc"] = vpc
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container."""
        return self._values.get('image')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def enable_ecs_managed_tags(self) -> typing.Optional[bool]:
        """Specifies whether to enable Amazon ECS managed tags for the tasks within the service.

        For more information, see
        `Tagging Your Amazon ECS Resources <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-using-tags.html>`_

        default
        :default: false
        """
        return self._values.get('enable_ecs_managed_tags')

    @builtins.property
    def enable_logging(self) -> typing.Optional[bool]:
        """Flag to indicate whether to enable logging.

        default
        :default: true
        """
        return self._values.get('enable_logging')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        The variable ``QUEUE_NAME`` with value ``queue.queueName`` will
        always be passed.

        default
        :default: 'QUEUE_NAME: queue.queueName'
        """
        return self._values.get('environment')

    @builtins.property
    def family(self) -> typing.Optional[str]:
        """The name of a family that the task definition is registered to.

        A family groups multiple versions of a task definition.

        default
        :default: - Automatically generated name.
        """
        return self._values.get('family')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def max_scaling_capacity(self) -> typing.Optional[jsii.Number]:
        """Maximum capacity to scale to.

        default
        :default: (desiredTaskCount * 2)
        """
        return self._values.get('max_scaling_capacity')

    @builtins.property
    def propagate_tags(self) -> typing.Optional[aws_cdk.aws_ecs.PropagatedTagSource]:
        """Specifies whether to propagate the tags from the task definition or the service to the tasks in the service.

        Tags can only be propagated to the tasks within the service during service creation.

        default
        :default: - none
        """
        return self._values.get('propagate_tags')

    @builtins.property
    def queue(self) -> typing.Optional[aws_cdk.aws_sqs.IQueue]:
        """A queue for which to process items from.

        If specified and this is a FIFO queue, the queue name must end in the string '.fifo'. See
        `CreateQueue <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_CreateQueue.html>`_

        default
        :default: 'SQSQueue with CloudFormation-generated name'
        """
        return self._values.get('queue')

    @builtins.property
    def scaling_steps(self) -> typing.Optional[typing.List[aws_cdk.aws_applicationautoscaling.ScalingInterval]]:
        """The intervals for scaling based on the SQS queue's ApproximateNumberOfMessagesVisible metric.

        Maps a range of metric values to a particular scaling behavior. See
        `Simple and Step Scaling Policies for Amazon EC2 Auto Scaling <https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scaling-simple-step.html>`_

        default
        :default: [{ upper: 0, change: -1 },{ lower: 100, change: +1 },{ lower: 500, change: +5 }]
        """
        return self._values.get('scaling_steps')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def service_name(self) -> typing.Optional[str]:
        """The name of the service.

        default
        :default: - CloudFormation-generated name.
        """
        return self._values.get('service_name')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The amount (in MiB) of memory used by the task.

        This field is required and you must use one of the following values, which determines your range of valid values
        for the cpu parameter:

        0.5GB, 1GB, 2GB - Available cpu values: 256 (.25 vCPU)

        1GB, 2GB, 3GB, 4GB - Available cpu values: 512 (.5 vCPU)

        2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB - Available cpu values: 1024 (1 vCPU)

        Between 4GB and 16GB in 1GB increments - Available cpu values: 2048 (2 vCPU)

        Between 8GB and 30GB in 1GB increments - Available cpu values: 4096 (4 vCPU)

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 512
        """
        return self._values.get('memory_limit_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'QueueProcessingFargateServiceProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskDefinitionOptions", jsii_struct_bases=[], name_mapping={'task_definition': 'taskDefinition'})
class ScheduledEc2TaskDefinitionOptions():
    def __init__(self, *, task_definition: aws_cdk.aws_ecs.Ec2TaskDefinition):
        """The properties for the ScheduledEc2Task using a task definition.

        :param task_definition: The task definition to use for tasks in the service. One of image or taskDefinition must be specified. [disable-awslint:ref-via-interface] Default: - none
        """
        self._values = {
            'task_definition': task_definition,
        }

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.Ec2TaskDefinition:
        """The task definition to use for tasks in the service. One of image or taskDefinition must be specified.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledEc2TaskDefinitionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTaskDefinitionOptions", jsii_struct_bases=[], name_mapping={'task_definition': 'taskDefinition'})
class ScheduledFargateTaskDefinitionOptions():
    def __init__(self, *, task_definition: aws_cdk.aws_ecs.FargateTaskDefinition):
        """The properties for the ScheduledFargateTask using a task definition.

        :param task_definition: The task definition to use for tasks in the service. Image or taskDefinition must be specified, but not both. [disable-awslint:ref-via-interface] Default: - none
        """
        self._values = {
            'task_definition': task_definition,
        }

    @builtins.property
    def task_definition(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        """The task definition to use for tasks in the service. Image or taskDefinition must be specified, but not both.

        [disable-awslint:ref-via-interface]

        default
        :default: - none
        """
        return self._values.get('task_definition')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledFargateTaskDefinitionOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


class ScheduledTaskBase(aws_cdk.core.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskBase"):
    """The base class for ScheduledEc2Task and ScheduledFargateTask tasks."""
    @builtins.staticmethod
    def __jsii_proxy_class__():
        return _ScheduledTaskBaseProxy

    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, schedule: aws_cdk.aws_applicationautoscaling.Schedule, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_task_count: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ScheduledTaskBase class.

        :param scope: -
        :param id: -
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ScheduledTaskBaseProps(schedule=schedule, cluster=cluster, desired_task_count=desired_task_count, vpc=vpc)

        jsii.create(ScheduledTaskBase, self, [scope, id, props])

    @jsii.member(jsii_name="addTaskDefinitionToEventTarget")
    def _add_task_definition_to_event_target(self, task_definition: aws_cdk.aws_ecs.TaskDefinition) -> aws_cdk.aws_events_targets.EcsTask:
        """Create an ECS task using the task definition provided and add it to the scheduled event rule.

        :param task_definition: the TaskDefinition to add to the event rule.
        """
        return jsii.invoke(self, "addTaskDefinitionToEventTarget", [task_definition])

    @jsii.member(jsii_name="createAWSLogDriver")
    def _create_aws_log_driver(self, prefix: str) -> aws_cdk.aws_ecs.AwsLogDriver:
        """Create an AWS Log Driver with the provided streamPrefix.

        :param prefix: the Cloudwatch logging prefix.
        """
        return jsii.invoke(self, "createAWSLogDriver", [prefix])

    @jsii.member(jsii_name="getDefaultCluster")
    def _get_default_cluster(self, scope: aws_cdk.core.Construct, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> aws_cdk.aws_ecs.Cluster:
        """Returns the default cluster.

        :param scope: -
        :param vpc: -
        """
        return jsii.invoke(self, "getDefaultCluster", [scope, vpc])

    @builtins.property
    @jsii.member(jsii_name="cluster")
    def cluster(self) -> aws_cdk.aws_ecs.ICluster:
        """The name of the cluster that hosts the service."""
        return jsii.get(self, "cluster")

    @builtins.property
    @jsii.member(jsii_name="desiredTaskCount")
    def desired_task_count(self) -> jsii.Number:
        """The desired number of instantiations of the task definition to keep running on the service.

        The minimum value is 1
        """
        return jsii.get(self, "desiredTaskCount")

    @builtins.property
    @jsii.member(jsii_name="eventRule")
    def event_rule(self) -> aws_cdk.aws_events.Rule:
        """The CloudWatch Events rule for the service."""
        return jsii.get(self, "eventRule")


class _ScheduledTaskBaseProxy(ScheduledTaskBase):
    pass

class ScheduledEc2Task(ScheduledTaskBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2Task"):
    """A scheduled EC2 task that will be initiated off of CloudWatch Events."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, scheduled_ec2_task_definition_options: typing.Optional["ScheduledEc2TaskDefinitionOptions"]=None, scheduled_ec2_task_image_options: typing.Optional["ScheduledEc2TaskImageOptions"]=None, schedule: aws_cdk.aws_applicationautoscaling.Schedule, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_task_count: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ScheduledEc2Task class.

        :param scope: -
        :param id: -
        :param scheduled_ec2_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param scheduled_ec2_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ScheduledEc2TaskProps(scheduled_ec2_task_definition_options=scheduled_ec2_task_definition_options, scheduled_ec2_task_image_options=scheduled_ec2_task_image_options, schedule=schedule, cluster=cluster, desired_task_count=desired_task_count, vpc=vpc)

        jsii.create(ScheduledEc2Task, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.Ec2TaskDefinition:
        """The EC2 task definition in this construct."""
        return jsii.get(self, "taskDefinition")


class ScheduledFargateTask(ScheduledTaskBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTask"):
    """A scheduled Fargate task that will be initiated off of CloudWatch Events."""
    def __init__(self, scope: aws_cdk.core.Construct, id: str, *, scheduled_fargate_task_definition_options: typing.Optional["ScheduledFargateTaskDefinitionOptions"]=None, scheduled_fargate_task_image_options: typing.Optional["ScheduledFargateTaskImageOptions"]=None, schedule: aws_cdk.aws_applicationautoscaling.Schedule, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_task_count: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None) -> None:
        """Constructs a new instance of the ScheduledFargateTask class.

        :param scope: -
        :param id: -
        :param scheduled_fargate_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param scheduled_fargate_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        props = ScheduledFargateTaskProps(scheduled_fargate_task_definition_options=scheduled_fargate_task_definition_options, scheduled_fargate_task_image_options=scheduled_fargate_task_image_options, schedule=schedule, cluster=cluster, desired_task_count=desired_task_count, vpc=vpc)

        jsii.create(ScheduledFargateTask, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="taskDefinition")
    def task_definition(self) -> aws_cdk.aws_ecs.FargateTaskDefinition:
        """The Fargate task definition in this construct."""
        return jsii.get(self, "taskDefinition")


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskBaseProps", jsii_struct_bases=[], name_mapping={'schedule': 'schedule', 'cluster': 'cluster', 'desired_task_count': 'desiredTaskCount', 'vpc': 'vpc'})
class ScheduledTaskBaseProps():
    def __init__(self, *, schedule: aws_cdk.aws_applicationautoscaling.Schedule, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_task_count: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None):
        """The properties for the base ScheduledEc2Task or ScheduledFargateTask task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        self._values = {
            'schedule': schedule,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if vpc is not None: self._values["vpc"] = vpc

    @builtins.property
    def schedule(self) -> aws_cdk.aws_applicationautoscaling.Schedule:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.
        """
        return self._values.get('schedule')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledTaskBaseProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskProps", jsii_struct_bases=[ScheduledTaskBaseProps], name_mapping={'schedule': 'schedule', 'cluster': 'cluster', 'desired_task_count': 'desiredTaskCount', 'vpc': 'vpc', 'scheduled_ec2_task_definition_options': 'scheduledEc2TaskDefinitionOptions', 'scheduled_ec2_task_image_options': 'scheduledEc2TaskImageOptions'})
class ScheduledEc2TaskProps(ScheduledTaskBaseProps):
    def __init__(self, *, schedule: aws_cdk.aws_applicationautoscaling.Schedule, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_task_count: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, scheduled_ec2_task_definition_options: typing.Optional["ScheduledEc2TaskDefinitionOptions"]=None, scheduled_ec2_task_image_options: typing.Optional["ScheduledEc2TaskImageOptions"]=None):
        """The properties for the ScheduledEc2Task task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param scheduled_ec2_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        :param scheduled_ec2_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both. Default: none
        """
        if isinstance(scheduled_ec2_task_definition_options, dict): scheduled_ec2_task_definition_options = ScheduledEc2TaskDefinitionOptions(**scheduled_ec2_task_definition_options)
        if isinstance(scheduled_ec2_task_image_options, dict): scheduled_ec2_task_image_options = ScheduledEc2TaskImageOptions(**scheduled_ec2_task_image_options)
        self._values = {
            'schedule': schedule,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if vpc is not None: self._values["vpc"] = vpc
        if scheduled_ec2_task_definition_options is not None: self._values["scheduled_ec2_task_definition_options"] = scheduled_ec2_task_definition_options
        if scheduled_ec2_task_image_options is not None: self._values["scheduled_ec2_task_image_options"] = scheduled_ec2_task_image_options

    @builtins.property
    def schedule(self) -> aws_cdk.aws_applicationautoscaling.Schedule:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.
        """
        return self._values.get('schedule')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def scheduled_ec2_task_definition_options(self) -> typing.Optional["ScheduledEc2TaskDefinitionOptions"]:
        """The properties to define if using an existing TaskDefinition in this construct.

        ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both.

        default
        :default: none
        """
        return self._values.get('scheduled_ec2_task_definition_options')

    @builtins.property
    def scheduled_ec2_task_image_options(self) -> typing.Optional["ScheduledEc2TaskImageOptions"]:
        """The properties to define if the construct is to create a TaskDefinition.

        ScheduledEc2TaskDefinitionOptions or ScheduledEc2TaskImageOptions must be defined, but not both.

        default
        :default: none
        """
        return self._values.get('scheduled_ec2_task_image_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledEc2TaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTaskProps", jsii_struct_bases=[ScheduledTaskBaseProps], name_mapping={'schedule': 'schedule', 'cluster': 'cluster', 'desired_task_count': 'desiredTaskCount', 'vpc': 'vpc', 'scheduled_fargate_task_definition_options': 'scheduledFargateTaskDefinitionOptions', 'scheduled_fargate_task_image_options': 'scheduledFargateTaskImageOptions'})
class ScheduledFargateTaskProps(ScheduledTaskBaseProps):
    def __init__(self, *, schedule: aws_cdk.aws_applicationautoscaling.Schedule, cluster: typing.Optional[aws_cdk.aws_ecs.ICluster]=None, desired_task_count: typing.Optional[jsii.Number]=None, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc]=None, scheduled_fargate_task_definition_options: typing.Optional["ScheduledFargateTaskDefinitionOptions"]=None, scheduled_fargate_task_image_options: typing.Optional["ScheduledFargateTaskImageOptions"]=None):
        """The properties for the ScheduledFargateTask task.

        :param schedule: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_ in the Amazon CloudWatch User Guide.
        :param cluster: The name of the cluster that hosts the service. If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc. Default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        :param desired_task_count: The desired number of instantiations of the task definition to keep running on the service. Default: 1
        :param vpc: The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed. If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster. Default: - uses the VPC defined in the cluster or creates a new VPC.
        :param scheduled_fargate_task_definition_options: The properties to define if using an existing TaskDefinition in this construct. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        :param scheduled_fargate_task_image_options: The properties to define if the construct is to create a TaskDefinition. ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both. Default: none
        """
        if isinstance(scheduled_fargate_task_definition_options, dict): scheduled_fargate_task_definition_options = ScheduledFargateTaskDefinitionOptions(**scheduled_fargate_task_definition_options)
        if isinstance(scheduled_fargate_task_image_options, dict): scheduled_fargate_task_image_options = ScheduledFargateTaskImageOptions(**scheduled_fargate_task_image_options)
        self._values = {
            'schedule': schedule,
        }
        if cluster is not None: self._values["cluster"] = cluster
        if desired_task_count is not None: self._values["desired_task_count"] = desired_task_count
        if vpc is not None: self._values["vpc"] = vpc
        if scheduled_fargate_task_definition_options is not None: self._values["scheduled_fargate_task_definition_options"] = scheduled_fargate_task_definition_options
        if scheduled_fargate_task_image_options is not None: self._values["scheduled_fargate_task_image_options"] = scheduled_fargate_task_image_options

    @builtins.property
    def schedule(self) -> aws_cdk.aws_applicationautoscaling.Schedule:
        """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

        For more information, see
        `Schedule Expression Syntax for Rules <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html>`_
        in the Amazon CloudWatch User Guide.
        """
        return self._values.get('schedule')

    @builtins.property
    def cluster(self) -> typing.Optional[aws_cdk.aws_ecs.ICluster]:
        """The name of the cluster that hosts the service.

        If a cluster is specified, the vpc construct should be omitted. Alternatively, you can omit both cluster and vpc.

        default
        :default: - create a new cluster; if both cluster and vpc are omitted, a new VPC will be created for you.
        """
        return self._values.get('cluster')

    @builtins.property
    def desired_task_count(self) -> typing.Optional[jsii.Number]:
        """The desired number of instantiations of the task definition to keep running on the service.

        default
        :default: 1
        """
        return self._values.get('desired_task_count')

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        """The VPC where the container instances will be launched or the elastic network interfaces (ENIs) will be deployed.

        If a vpc is specified, the cluster construct should be omitted. Alternatively, you can omit both vpc and cluster.

        default
        :default: - uses the VPC defined in the cluster or creates a new VPC.
        """
        return self._values.get('vpc')

    @builtins.property
    def scheduled_fargate_task_definition_options(self) -> typing.Optional["ScheduledFargateTaskDefinitionOptions"]:
        """The properties to define if using an existing TaskDefinition in this construct.

        ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both.

        default
        :default: none
        """
        return self._values.get('scheduled_fargate_task_definition_options')

    @builtins.property
    def scheduled_fargate_task_image_options(self) -> typing.Optional["ScheduledFargateTaskImageOptions"]:
        """The properties to define if the construct is to create a TaskDefinition.

        ScheduledFargateTaskDefinitionOptions or ScheduledFargateTaskImageOptions must be defined, but not both.

        default
        :default: none
        """
        return self._values.get('scheduled_fargate_task_image_options')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledFargateTaskProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledTaskImageProps", jsii_struct_bases=[], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'log_driver': 'logDriver', 'secrets': 'secrets'})
class ScheduledTaskImageProps():
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None):
        """
        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: none
        """
        return self._values.get('environment')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledTaskImageProps(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskImageOptions", jsii_struct_bases=[ScheduledTaskImageProps], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'log_driver': 'logDriver', 'secrets': 'secrets', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB', 'memory_reservation_mib': 'memoryReservationMiB'})
class ScheduledEc2TaskImageOptions(ScheduledTaskImageProps):
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None, memory_reservation_mib: typing.Optional[jsii.Number]=None):
        """The properties for the ScheduledEc2Task using an image.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param cpu: The minimum number of CPU units to reserve for the container. Default: none
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
        :param memory_reservation_mib: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib
        if memory_reservation_mib is not None: self._values["memory_reservation_mib"] = memory_reservation_mib

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: none
        """
        return self._values.get('environment')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The minimum number of CPU units to reserve for the container.

        default
        :default: none
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory limit.
        """
        return self._values.get('memory_limit_mib')

    @builtins.property
    def memory_reservation_mib(self) -> typing.Optional[jsii.Number]:
        """The soft limit (in MiB) of memory to reserve for the container.

        When system memory is under contention, Docker attempts to keep the
        container memory within the limit. If the container requires more memory,
        it can consume up to the value specified by the Memory property or all of
        the available memory on the container instance—whichever comes first.

        At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

        default
        :default: - No memory reserved.
        """
        return self._values.get('memory_reservation_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledEc2TaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledFargateTaskImageOptions", jsii_struct_bases=[ScheduledTaskImageProps], name_mapping={'image': 'image', 'command': 'command', 'environment': 'environment', 'log_driver': 'logDriver', 'secrets': 'secrets', 'cpu': 'cpu', 'memory_limit_mib': 'memoryLimitMiB'})
class ScheduledFargateTaskImageOptions(ScheduledTaskImageProps):
    def __init__(self, *, image: aws_cdk.aws_ecs.ContainerImage, command: typing.Optional[typing.List[str]]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, log_driver: typing.Optional[aws_cdk.aws_ecs.LogDriver]=None, secrets: typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]=None, cpu: typing.Optional[jsii.Number]=None, memory_limit_mib: typing.Optional[jsii.Number]=None):
        """The properties for the ScheduledFargateTask using an image.

        :param image: The image used to start a container. Image or taskDefinition must be specified, but not both. Default: - none
        :param command: The command that is passed to the container. If you provide a shell command as a single string, you have to quote command-line arguments. Default: - CMD value built into container image.
        :param environment: The environment variables to pass to the container. Default: none
        :param log_driver: The log driver to use. Default: - AwsLogDriver if enableLogging is true
        :param secrets: The secret to expose to the container as an environment variable. Default: - No secret environment variables.
        :param cpu: The number of cpu units used by the task. Valid values, which determines your range of valid values for the memory parameter: 256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB 512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB 1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB 2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments 4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments This default is set in the underlying FargateTaskDefinition construct. Default: 256
        :param memory_limit_mib: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. Default: 512
        """
        self._values = {
            'image': image,
        }
        if command is not None: self._values["command"] = command
        if environment is not None: self._values["environment"] = environment
        if log_driver is not None: self._values["log_driver"] = log_driver
        if secrets is not None: self._values["secrets"] = secrets
        if cpu is not None: self._values["cpu"] = cpu
        if memory_limit_mib is not None: self._values["memory_limit_mib"] = memory_limit_mib

    @builtins.property
    def image(self) -> aws_cdk.aws_ecs.ContainerImage:
        """The image used to start a container.

        Image or taskDefinition must be specified, but not both.

        default
        :default: - none
        """
        return self._values.get('image')

    @builtins.property
    def command(self) -> typing.Optional[typing.List[str]]:
        """The command that is passed to the container.

        If you provide a shell command as a single string, you have to quote command-line arguments.

        default
        :default: - CMD value built into container image.
        """
        return self._values.get('command')

    @builtins.property
    def environment(self) -> typing.Optional[typing.Mapping[str,str]]:
        """The environment variables to pass to the container.

        default
        :default: none
        """
        return self._values.get('environment')

    @builtins.property
    def log_driver(self) -> typing.Optional[aws_cdk.aws_ecs.LogDriver]:
        """The log driver to use.

        default
        :default: - AwsLogDriver if enableLogging is true
        """
        return self._values.get('log_driver')

    @builtins.property
    def secrets(self) -> typing.Optional[typing.Mapping[str,aws_cdk.aws_ecs.Secret]]:
        """The secret to expose to the container as an environment variable.

        default
        :default: - No secret environment variables.
        """
        return self._values.get('secrets')

    @builtins.property
    def cpu(self) -> typing.Optional[jsii.Number]:
        """The number of cpu units used by the task.

        Valid values, which determines your range of valid values for the memory parameter:

        256 (.25 vCPU) - Available memory values: 0.5GB, 1GB, 2GB

        512 (.5 vCPU) - Available memory values: 1GB, 2GB, 3GB, 4GB

        1024 (1 vCPU) - Available memory values: 2GB, 3GB, 4GB, 5GB, 6GB, 7GB, 8GB

        2048 (2 vCPU) - Available memory values: Between 4GB and 16GB in 1GB increments

        4096 (4 vCPU) - Available memory values: Between 8GB and 30GB in 1GB increments

        This default is set in the underlying FargateTaskDefinition construct.

        default
        :default: 256
        """
        return self._values.get('cpu')

    @builtins.property
    def memory_limit_mib(self) -> typing.Optional[jsii.Number]:
        """The hard limit (in MiB) of memory to present to the container.

        If your container attempts to exceed the allocated memory, the container
        is terminated.

        default
        :default: 512
        """
        return self._values.get('memory_limit_mib')

    def __eq__(self, rhs) -> bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs) -> bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return 'ScheduledFargateTaskImageOptions(%s)' % ', '.join(k + '=' + repr(v) for k, v in self._values.items())


__all__ = ["ApplicationListenerProps", "ApplicationLoadBalancedEc2Service", "ApplicationLoadBalancedEc2ServiceProps", "ApplicationLoadBalancedFargateService", "ApplicationLoadBalancedFargateServiceProps", "ApplicationLoadBalancedServiceBase", "ApplicationLoadBalancedServiceBaseProps", "ApplicationLoadBalancedTaskImageOptions", "ApplicationLoadBalancedTaskImageProps", "ApplicationLoadBalancerProps", "ApplicationMultipleTargetGroupsEc2Service", "ApplicationMultipleTargetGroupsEc2ServiceProps", "ApplicationMultipleTargetGroupsFargateService", "ApplicationMultipleTargetGroupsFargateServiceProps", "ApplicationMultipleTargetGroupsServiceBase", "ApplicationMultipleTargetGroupsServiceBaseProps", "ApplicationTargetProps", "NetworkListenerProps", "NetworkLoadBalancedEc2Service", "NetworkLoadBalancedEc2ServiceProps", "NetworkLoadBalancedFargateService", "NetworkLoadBalancedFargateServiceProps", "NetworkLoadBalancedServiceBase", "NetworkLoadBalancedServiceBaseProps", "NetworkLoadBalancedTaskImageOptions", "NetworkLoadBalancedTaskImageProps", "NetworkLoadBalancerProps", "NetworkMultipleTargetGroupsEc2Service", "NetworkMultipleTargetGroupsEc2ServiceProps", "NetworkMultipleTargetGroupsFargateService", "NetworkMultipleTargetGroupsFargateServiceProps", "NetworkMultipleTargetGroupsServiceBase", "NetworkMultipleTargetGroupsServiceBaseProps", "NetworkTargetProps", "QueueProcessingEc2Service", "QueueProcessingEc2ServiceProps", "QueueProcessingFargateService", "QueueProcessingFargateServiceProps", "QueueProcessingServiceBase", "QueueProcessingServiceBaseProps", "ScheduledEc2Task", "ScheduledEc2TaskDefinitionOptions", "ScheduledEc2TaskImageOptions", "ScheduledEc2TaskProps", "ScheduledFargateTask", "ScheduledFargateTaskDefinitionOptions", "ScheduledFargateTaskImageOptions", "ScheduledFargateTaskProps", "ScheduledTaskBase", "ScheduledTaskBaseProps", "ScheduledTaskImageProps", "__jsii_assembly__"]

publication.publish()
