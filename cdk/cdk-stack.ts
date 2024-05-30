import {
  App,
  CfnOutput,
  Duration,
  Stack,
} from "aws-cdk-lib";
import * as path from "path";
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { DockerImageCode } from "aws-cdk-lib/aws-lambda";
import { HttpApi, HttpMethod } from "@aws-cdk/aws-apigatewayv2-alpha";
import { HttpLambdaIntegration } from "@aws-cdk/aws-apigatewayv2-integrations-alpha";


const rootPath = path.join(__dirname, "..");

const app = new App();

const stack = new Stack(app, "LambdaMLStack", {
  env: {
    region: "your-aws-region",
    account: "your-aws-account-number",
  },
});

const entry = path.join(rootPath, "lambda");


const lambdaFn = new lambda.DockerImageFunction(
    stack,
    "SentimentLambda",
    {
      code: DockerImageCode.fromImageAsset(entry),
      memorySize: 3008,
      timeout: Duration.seconds(40),
      architecture: lambda.Architecture.ARM_64 // verify your architecture which built the docker image
    }
  );

const sentimentIntegration =  new HttpLambdaIntegration('sentimentIntegration', lambdaFn)

const api = new HttpApi(stack, "SentimentApi");

api.addRoutes({
  path: '/qa',
  methods: [ HttpMethod.POST ],
  integration: sentimentIntegration,
});

new CfnOutput(stack, "SentimentEndpoint", {
  value: api.url || "",
});
