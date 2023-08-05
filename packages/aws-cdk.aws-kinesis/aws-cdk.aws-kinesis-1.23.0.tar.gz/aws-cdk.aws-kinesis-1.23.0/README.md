## Amazon Kinesis Construct Library

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

Define an unencrypted Kinesis stream.

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
Stream(self, "MyFirstStream")
```

### Encryption

Define a KMS-encrypted stream:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
stream = Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.Kms
)

# you can access the encryption key:
assert(stream.encryption_key instanceof kms.Key)
```

You can also supply your own key:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
my_kms_key = kms.Key(self, "MyKey")

stream = Stream(self, "MyEncryptedStream",
    encryption=StreamEncryption.Kms,
    encryption_key=my_kms_key
)

assert(stream.encryption_key === my_kms_key)
```
