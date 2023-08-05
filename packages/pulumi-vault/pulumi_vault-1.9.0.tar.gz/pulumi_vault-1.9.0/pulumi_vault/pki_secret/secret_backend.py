# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class SecretBackend(pulumi.CustomResource):
    default_lease_ttl_seconds: pulumi.Output[float]
    """
    The default TTL for credentials issued by this backend.
    """
    description: pulumi.Output[str]
    """
    A human-friendly description for this backend.
    """
    max_lease_ttl_seconds: pulumi.Output[float]
    """
    The maximum TTL that can be requested for credentials issued by this backend.
    """
    path: pulumi.Output[str]
    """
    The unique path this backend should be mounted at. Must not begin or end with a `/`.
    """
    def __init__(__self__, resource_name, opts=None, default_lease_ttl_seconds=None, description=None, max_lease_ttl_seconds=None, path=None, __props__=None, __name__=None, __opts__=None):
        """
        Creates an PKI Secret Backend for Vault. PKI secret backends can then issue certificates, once a role has been added to
        the backend.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] default_lease_ttl_seconds: The default TTL for credentials issued by this backend.
        :param pulumi.Input[str] description: A human-friendly description for this backend.
        :param pulumi.Input[float] max_lease_ttl_seconds: The maximum TTL that can be requested for credentials issued by this backend.
        :param pulumi.Input[str] path: The unique path this backend should be mounted at. Must not begin or end with a `/`.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/pki_secret_backend.html.markdown.
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

            __props__['default_lease_ttl_seconds'] = default_lease_ttl_seconds
            __props__['description'] = description
            __props__['max_lease_ttl_seconds'] = max_lease_ttl_seconds
            if path is None:
                raise TypeError("Missing required property 'path'")
            __props__['path'] = path
        super(SecretBackend, __self__).__init__(
            'vault:pkiSecret/secretBackend:SecretBackend',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, default_lease_ttl_seconds=None, description=None, max_lease_ttl_seconds=None, path=None):
        """
        Get an existing SecretBackend resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[float] default_lease_ttl_seconds: The default TTL for credentials issued by this backend.
        :param pulumi.Input[str] description: A human-friendly description for this backend.
        :param pulumi.Input[float] max_lease_ttl_seconds: The maximum TTL that can be requested for credentials issued by this backend.
        :param pulumi.Input[str] path: The unique path this backend should be mounted at. Must not begin or end with a `/`.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/pki_secret_backend.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["default_lease_ttl_seconds"] = default_lease_ttl_seconds
        __props__["description"] = description
        __props__["max_lease_ttl_seconds"] = max_lease_ttl_seconds
        __props__["path"] = path
        return SecretBackend(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

