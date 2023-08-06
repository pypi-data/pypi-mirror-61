## AWS Key Management Service Construct Library

<!--BEGIN STABILITY BANNER-->---


![Stability: Stable](https://img.shields.io/badge/stability-Stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

Define a KMS key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import aws_cdk.aws_kms as kms

kms.Key(self, "MyKey",
    enable_key_rotation=True
)
```

Add a couple of aliases:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
key = kms.Key(self, "MyKey")
key.add_alias("alias/foo")
key.add_alias("alias/bar")
```

### Sharing keys between stacks

To use a KMS key in a different stack in the same CDK application,
pass the construct to the other stack:

```python
# Example automatically generated. See https://github.com/aws/jsii/issues/826
#
# Stack that defines the key
#
class KeyStack(cdk.Stack):

    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags)
        self.key = kms.Key(self, "MyKey", removal_policy=cdk.RemovalPolicy.DESTROY)

#
# Stack that uses the key
#
class UseStack(cdk.Stack):
    def __init__(self, scope, id, *, key, description=None, env=None, stackName=None, tags=None):
        super().__init__(scope, id, key=key, description=description, env=env, stackName=stackName, tags=tags)

        # Use the IKey object here.
        kms.Alias(self, "Alias",
            alias_name="alias/foo",
            target_key=key
        )

key_stack = KeyStack(app, "KeyStack")
UseStack(app, "UseStack", key=key_stack.key)
```

### Importing existing keys

To use a KMS key that is not defined in this CDK app, but is created through other means, use
`Key.fromKeyArn(parent, name, ref)`:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_key_imported = kms.Key.from_key_arn(self, "MyImportedKey", "arn:aws:...")

# you can do stuff with this imported key.
my_key_imported.add_alias("alias/foo")
```

Note that a call to `.addToPolicy(statement)` on `myKeyImported` will not have
an affect on the key's policy because it is not owned by your stack. The call
will be a no-op.
