# ccaaws

Python objects wrapped around [boto3](https://github.com/boto/boto3)

## botosession.py

Base class inherited by all the others.  Manages connections to AWS via
access keys or profiles.

## cfnclient.py

CloudFormation client

## cwclient.py

CloudWatch client

## iamclient.py

Access to IAM functions - mainly for user access key management.

Can raise an `AccessKeyError` exception on failure.

```
from ccaaws.iamclient import IamClient

iam = IamClient("iam.user")
newkey = iam.rotateKeys()
```

## paramstore.py

SSM ParameterStore client

[modeline]: # ( vim: set ft=markdown tw=74 fenc=utf-8 spell spl=en_gb mousemodel=popup: )
