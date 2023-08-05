import json
import setuptools

kwargs = json.loads("""
{
    "name": "mbonig.secure-bucket",
    "version": "1.0.8",
    "description": "An AWS CDK Construct that enforces encryption on an S3 bucket",
    "license": "MIT",
    "url": "https://github.com/mbonig/secure-bucket.git",
    "long_description_content_type": "text/markdown",
    "author": "Matthew Bonig<matthew.bonig@gmail.com>",
    "project_urls": {
        "Source": "https://github.com/mbonig/secure-bucket.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mbonig.secure_bucket",
        "mbonig.secure_bucket._jsii"
    ],
    "package_data": {
        "mbonig.secure_bucket._jsii": [
            "secure-bucket@1.0.8.jsii.tgz"
        ],
        "mbonig.secure_bucket": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "jsii~=0.21.2",
        "publication>=0.0.3",
        "aws-cdk.aws-s3>=1.22.0, <2.0.0",
        "aws-cdk.core>=1.22.0, <2.0.0"
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
        "License :: OSI Approved"
    ]
}
""")

with open('README.md') as fp:
    kwargs['long_description'] = fp.read()


setuptools.setup(**kwargs)
