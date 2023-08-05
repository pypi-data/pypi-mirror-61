# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class AccessKey(pulumi.CustomResource):
    encrypted_secret: pulumi.Output[str]
    """
    The encrypted secret, base64 encoded, if `pgp_key` was specified.
    > **NOTE:** The encrypted secret may be decrypted using the command line,
    for example: `... | base64 --decode | keybase pgp decrypt`.
    """
    key_fingerprint: pulumi.Output[str]
    """
    The fingerprint of the PGP key used to encrypt
    the secret
    """
    pgp_key: pulumi.Output[str]
    """
    Either a base-64 encoded PGP public key, or a
    keybase username in the form `keybase:some_person_that_exists`, for use
    in the `encrypted_secret` output attribute.
    """
    secret: pulumi.Output[str]
    """
    The secret access key. Note that this will be written
    to the state file. If you use this, please protect your backend state file
    judiciously. Alternatively, you may supply a `pgp_key` instead, which will
    prevent the secret from being stored in plaintext, at the cost of preventing
    the use of the secret key in automation.
    """
    ses_smtp_password: pulumi.Output[str]
    """
    The secret access key converted into an SES SMTP
    password by applying [AWS's documented conversion
    algorithm](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-convert).
    """
    status: pulumi.Output[str]
    """
    The access key status to apply. Defaults to `Active`.
    Valid values are `Active` and `Inactive`.
    """
    user: pulumi.Output[str]
    """
    The IAM user to associate with this access key.
    """
    def __init__(__self__, resource_name, opts=None, pgp_key=None, status=None, user=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides an IAM access key. This is a set of credentials that allow API requests to be made as an IAM user.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a
               keybase username in the form `keybase:some_person_that_exists`, for use
               in the `encrypted_secret` output attribute.
        :param pulumi.Input[str] status: The access key status to apply. Defaults to `Active`.
               Valid values are `Active` and `Inactive`.
        :param pulumi.Input[str] user: The IAM user to associate with this access key.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/iam_access_key.html.markdown.
        """
        if __name__ is not None:
            warnings.warn("explicit use of __name__ is deprecated", DeprecationWarning)
            resource_name = __name__
        if __opts__ is not None:
            warnings.warn("explicit use of __opts__ is deprecated, use 'opts' instead", DeprecationWarning)
            opts = __opts__
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = dict()

            __props__['pgp_key'] = pgp_key
            __props__['status'] = status
            if user is None:
                raise TypeError("Missing required property 'user'")
            __props__['user'] = user
            __props__['encrypted_secret'] = None
            __props__['key_fingerprint'] = None
            __props__['secret'] = None
            __props__['ses_smtp_password'] = None
        super(AccessKey, __self__).__init__(
            'aws:iam/accessKey:AccessKey',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, encrypted_secret=None, key_fingerprint=None, pgp_key=None, secret=None, ses_smtp_password=None, status=None, user=None):
        """
        Get an existing AccessKey resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] encrypted_secret: The encrypted secret, base64 encoded, if `pgp_key` was specified.
               > **NOTE:** The encrypted secret may be decrypted using the command line,
               for example: `... | base64 --decode | keybase pgp decrypt`.
        :param pulumi.Input[str] key_fingerprint: The fingerprint of the PGP key used to encrypt
               the secret
        :param pulumi.Input[str] pgp_key: Either a base-64 encoded PGP public key, or a
               keybase username in the form `keybase:some_person_that_exists`, for use
               in the `encrypted_secret` output attribute.
        :param pulumi.Input[str] secret: The secret access key. Note that this will be written
               to the state file. If you use this, please protect your backend state file
               judiciously. Alternatively, you may supply a `pgp_key` instead, which will
               prevent the secret from being stored in plaintext, at the cost of preventing
               the use of the secret key in automation.
        :param pulumi.Input[str] ses_smtp_password: The secret access key converted into an SES SMTP
               password by applying [AWS's documented conversion
               algorithm](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/smtp-credentials.html#smtp-credentials-convert).
        :param pulumi.Input[str] status: The access key status to apply. Defaults to `Active`.
               Valid values are `Active` and `Inactive`.
        :param pulumi.Input[str] user: The IAM user to associate with this access key.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-aws/blob/master/website/docs/r/iam_access_key.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["encrypted_secret"] = encrypted_secret
        __props__["key_fingerprint"] = key_fingerprint
        __props__["pgp_key"] = pgp_key
        __props__["secret"] = secret
        __props__["ses_smtp_password"] = ses_smtp_password
        __props__["status"] = status
        __props__["user"] = user
        return AccessKey(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

