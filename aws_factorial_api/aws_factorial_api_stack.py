from aws_cdk import (
    core as cdk,
    aws_ecs_patterns as ecs_patterns,
    aws_ecs as ecs,
    aws_route53 as route53,
    aws_elasticloadbalancingv2 as elbv2,
)


class AwsFactorialApiStack(cdk.Stack):
    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Hardcoding the ID for simplicity - normally I'd pass it as a parameter into this
        hosted_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "assignmentHostedZone",
            hosted_zone_id="Z07337312G9QMEMQI78P8",
            zone_name="to-assignment.net",
        )

        # TODO Add alerting
        factorial_api = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "factorialApiService",
            service_name="factorialApiService",
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset(directory="./container"),
                container_port=5000,
                container_name="factorialApi",
            ),
            domain_name="factorial.to-assignment.net",
            domain_zone=hosted_zone,
            protocol=elbv2.ApplicationProtocol.HTTPS,
            redirect_http=True,
            desired_count=2,
        )

        factorial_api.target_group.configure_health_check(path="/status", port="5000")
