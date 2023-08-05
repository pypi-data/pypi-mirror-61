## AWS CodeStar CDK
A package used to deploy a lambda function into AWS CodeStar via CDK.

### Description

This package creates a lambda function, editable via commits to AWS CodeCommit and fully monitored using AWS CodeStar.
The function uses gradual code deployment Linear10PercentEvery3Minutes, which means any commits will gradually be deployed and 10 percent of the load will be sent to the new deployment every 3 minutes. If you want to change that, edit the line in 

```aws_codestar_cdk/files/source.zip/template.yml```

More info:
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/automating-updates-to-serverless-apps.html

The function's runtime is specified to python3.6 and the lambda handler (initially called code within your function) is specified to manage.runner (manage is the file name, a.k.a manage.py and runner is the function name within the file).
All that can also be changed by editing the template.yml file.

Deploying this package creates 2 CloudFormation stacks in total.

The first stack is the CodeStar stack, which specifies, what the project should create. It's contents can be edited by editing

```aws_codestar_cdk/files/toolchain.yml``` 

The second stack is the lambda function stack, which can be edited by editing the template.yml file.

### Prerequisites

In order to operate the package, you must first install it, using
 
```pip install aws-codestar-cdk```

You also need to have an AWS account with a confugured AWS CLI. Here's how to do it:

https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html

### How to use

Import the main file into your project and call the Main classes constructor in your own cdk stack.

You should have the CodeStar service role in your account or in your stack. It has to have permissions "events:RemoveTargets" and "events:DeleteRule"

The arguments for the constructor are the scope, your project name, name of s3 bucket to put function source code and toolchain to, list of subnet IDs where the function should be deployed, list of security group IDs for the function, function execution role, function invocation event type and event type arguments.

The subnet IDs specify, what subnets your function will be deployed to. Make sure they have NAT gateways, in order to access the internet. Read more:

https://docs.amazonaws.cn/en_us/vpc/latest/userguide/what-is-amazon-vpc.html

Function invocation event type can be "Api", "Schedule" or "None"

If the invocation type is schedule, argument schedule_expression is also required.

Is can be either:

rate(x units), meaning your function will be called every x units.
e.g. rate(5 minutes), in which case the function will be invoked every 5 minutes.

cron(Minutes Hours Day-of-month Month Day-of-week Year)
e.g. cron(0 0 * * ? *), which would mean, that the function will be invoked every day at midnight.

More info: https://docs.aws.amazon.com/lambda/latest/dg/tutorial-scheduled-events-schedule-expressions.html

Parameters are split into 3 groups - VPC parameters, deployment parameters and Lambda type parameters.

VPC parameters include subnet IDs and security group IDs.

Lambda type parameters include execution role, event type and optionally schedule expressions.

Deployment parameters include your project name and bucket name.

Your code should look something like this:
```from aws_cdk import core, aws_iam
from aws_codestar_cdk.main import LambdaCodeStar
from aws_codestar_cdk.cdk_stack.parameters import VpcParameters, LambdaTypeParameters, DeploymentParameters
class AwsCdkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        service_role = aws_iam.Role(
            self, 'CodeStarService',
            path='/service-role/',
            role_name='aws-codestar-service-role',
            assumed_by=aws_iam.ServicePrincipal('codestar.amazonaws.com'),
            inline_policies={
                'RemoveEvent': aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            actions=[
                                'events:RemoveTargets',
                                'events:DeleteRule'
                            ],
                            effect=aws_iam.Effect.ALLOW,
                            resources=['*']
                        )
                    ]
                )
            },
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSCodeStarServiceRole')
            ]
        )

        exec_role = aws_iam.Role(
            self, 'CodeStarExecution',
            path='/',
            role_name='CodeStarExecution',
            assumed_by=aws_iam.ServicePrincipal('lambda.amazonaws.com'),
            inline_policies={
                'LambdaExecutionRolePolicy': aws_iam.PolicyDocument(
                    statements=[
                        aws_iam.PolicyStatement(
                            actions=[
                                'ec2:*'
                            ],
                            effect=aws_iam.Effect.ALLOW,
                            resources=['*']
                        )
                    ]
                )
            },
            managed_policies=[
                aws_iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSLambdaBasicExecutionRole')
            ]
        )

        deployment_params = DeploymentParameters('TestCron', 'testLambdaBucketCron')
        lambda_params = LambdaTypeParameters(lambda_exec_role=exec_role, event_type="Schedule", schedule_expression="cron(0 0 * * ? *)")
        vpc_params = VpcParameters(['subnet-1'], ['sg-1'])

        main = LambdaCodeStar(self, vpc_params, deployment_params, lambda_params)

```
