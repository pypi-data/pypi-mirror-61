import json
import setuptools

kwargs = json.loads("""
{
    "name": "aws-cdk.aws-sqs",
    "version": "1.23.0",
    "description": "CDK Constructs for AWS SQS",
    "license": "Apache-2.0",
    "url": "https://github.com/aws/aws-cdk",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "project_urls": {
        "Source": "https://github.com/aws/aws-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "aws_cdk.aws_sqs",
        "aws_cdk.aws_sqs._jsii"
    ],
    "package_data": {
        "aws_cdk.aws_sqs._jsii": [
            "aws-sqs@1.23.0.jsii.tgz"
        ],
        "aws_cdk.aws_sqs": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.21.2",
        "publication>=0.0.3",
        "aws-cdk.aws-cloudwatch==1.23.0",
        "aws-cdk.aws-iam==1.23.0",
        "aws-cdk.aws-kms==1.23.0",
        "aws-cdk.core==1.23.0"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
