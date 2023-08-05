# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class AuthBackendRole(pulumi.CustomResource):
    allow_instance_migration: pulumi.Output[bool]
    """
    If set to `true`, allows migration of
    the underlying instance where the client resides.
    """
    auth_type: pulumi.Output[str]
    """
    The auth type permitted for this role. Valid choices
    are `ec2` and `iam`. Defaults to `iam`.
    """
    backend: pulumi.Output[str]
    bound_account_ids: pulumi.Output[list]
    """
    If set, defines a constraint on the EC2
    instances that can perform the login operation that they should be using the
    account ID specified by this field. `auth_type` must be set to `ec2` or
    `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
    """
    bound_ami_ids: pulumi.Output[list]
    """
    If set, defines a constraint on the EC2 instances
    that can perform the login operation that they should be using the AMI ID
    specified by this field. `auth_type` must be set to `ec2` or
    `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
    """
    bound_ec2_instance_ids: pulumi.Output[list]
    bound_iam_instance_profile_arns: pulumi.Output[list]
    """
    If set, defines a constraint on
    the EC2 instances that can perform the login operation that they must be
    associated with an IAM instance profile ARN which has a prefix that matches
    the value specified by this field. The value is prefix-matched as though it
    were a glob ending in `*`. `auth_type` must be set to `ec2` or
    `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
    """
    bound_iam_principal_arns: pulumi.Output[list]
    """
    If set, defines the IAM principal that
    must be authenticated when `auth_type` is set to `iam`. Wildcards are
    supported at the end of the ARN.
    """
    bound_iam_role_arns: pulumi.Output[list]
    """
    If set, defines a constraint on the EC2
    instances that can perform the login operation that they must match the IAM
    role ARN specified by this field. `auth_type` must be set to `ec2` or
    `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
    """
    bound_regions: pulumi.Output[list]
    """
    If set, defines a constraint on the EC2 instances
    that can perform the login operation that the region in their identity
    document must match the one specified by this field. `auth_type` must be set
    to `ec2` or `inferred_entity_type` must be set to `ec2_instance` to use this
    constraint.
    """
    bound_subnet_ids: pulumi.Output[list]
    """
    If set, defines a constraint on the EC2
    instances that can perform the login operation that they be associated with
    the subnet ID that matches the value specified by this field. `auth_type`
    must be set to `ec2` or `inferred_entity_type` must be set to `ec2_instance`
    to use this constraint.
    """
    bound_vpc_ids: pulumi.Output[list]
    """
    If set, defines a constraint on the EC2 instances
    that can perform the login operation that they be associated with the VPC ID
    that matches the value specified by this field. `auth_type` must be set to
    `ec2` or `inferred_entity_type` must be set to `ec2_instance` to use this
    constraint.
    """
    disallow_reauthentication: pulumi.Output[bool]
    """
    IF set to `true`, only allows a
    single token to be granted per instance ID. This can only be set when
    `auth_type` is set to `ec2`.
    """
    inferred_aws_region: pulumi.Output[str]
    """
    When `inferred_entity_type` is set, this
    is the region to search for the inferred entities. Required if
    `inferred_entity_type` is set. This only applies when `auth_type` is set to
    `iam`.
    """
    inferred_entity_type: pulumi.Output[str]
    """
    If set, instructs Vault to turn on
    inferencing. The only valid value is `ec2_instance`, which instructs Vault to
    infer that the role comes from an EC2 instance in an IAM instance profile.
    This only applies when `auth_type` is set to `iam`.
    """
    max_ttl: pulumi.Output[float]
    """
    The maximum allowed lifetime of tokens
    issued using this role, provided as a number of seconds.
    """
    period: pulumi.Output[float]
    """
    If set, indicates that the
    token generated using this role should never expire. The token should be renewed within the
    duration specified by this value. At each renewal, the token's TTL will be set to the
    value of this field. Specified in seconds.
    """
    policies: pulumi.Output[list]
    """
    An array of strings
    specifying the policies to be set on tokens issued using this role.
    """
    resolve_aws_unique_ids: pulumi.Output[bool]
    """
    If set to `true`, the
    `bound_iam_principal_arns` are resolved to [AWS Unique
    IDs](http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-unique-ids)
    for the bound principal ARN. This field is ignored when a
    `bound_iam_principal_arn` ends in a wildcard. Resolving to unique IDs more
    closely mimics the behavior of AWS services in that if an IAM user or role is
    deleted and a new one is recreated with the same name, those new users or
    roles won't get access to roles in Vault that were permissioned to the prior
    principals of the same name. Defaults to `true`.
    Once set to `true`, this cannot be changed to `false` without recreating the role.
    """
    role: pulumi.Output[str]
    """
    The name of the role.
    """
    role_tag: pulumi.Output[str]
    """
    If set, enable role tags for this role. The value set
    for this field should be the key of the tag on the EC2 instance. `auth_type`
    must be set to `ec2` or `inferred_entity_type` must be set to `ec2_instance`
    to use this constraint.
    """
    token_bound_cidrs: pulumi.Output[list]
    """
    List of CIDR blocks; if set, specifies blocks of IP
    addresses which can authenticate successfully, and ties the resulting token to these blocks
    as well.
    """
    token_explicit_max_ttl: pulumi.Output[float]
    """
    If set, will encode an
    [explicit max TTL](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls)
    onto the token in number of seconds. This is a hard cap even if `token_ttl` and
    `token_max_ttl` would otherwise allow a renewal.
    """
    token_max_ttl: pulumi.Output[float]
    """
    The maximum lifetime for generated tokens in number of seconds.
    Its current value will be referenced at renewal time.
    """
    token_no_default_policy: pulumi.Output[bool]
    """
    If set, the default policy will not be set on
    generated tokens; otherwise it will be added to the policies set in token_policies.
    """
    token_num_uses: pulumi.Output[float]
    """
    The
    [period](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls),
    if any, in number of seconds to set on the token.
    """
    token_period: pulumi.Output[float]
    """
    If set, indicates that the
    token generated using this role should never expire. The token should be renewed within the
    duration specified by this value. At each renewal, the token's TTL will be set to the
    value of this field. Specified in seconds.
    """
    token_policies: pulumi.Output[list]
    """
    List of policies to encode onto generated tokens. Depending
    on the auth method, this list may be supplemented by user/group/other values.
    """
    token_ttl: pulumi.Output[float]
    """
    The incremental lifetime for generated tokens in number of seconds.
    Its current value will be referenced at renewal time.
    """
    token_type: pulumi.Output[str]
    """
    The type of token that should be generated. Can be `service`,
    `batch`, or `default` to use the mount's tuned default (which unless changed will be
    `service` tokens). For token store roles, there are two additional possibilities:
    `default-service` and `default-batch` which specify the type to return unless the client
    requests a different type at generation time.
    """
    ttl: pulumi.Output[float]
    """
    The TTL period of tokens issued
    using this role, provided as a number of seconds.
    """
    def __init__(__self__, resource_name, opts=None, allow_instance_migration=None, auth_type=None, backend=None, bound_account_ids=None, bound_ami_ids=None, bound_ec2_instance_ids=None, bound_iam_instance_profile_arns=None, bound_iam_principal_arns=None, bound_iam_role_arns=None, bound_regions=None, bound_subnet_ids=None, bound_vpc_ids=None, disallow_reauthentication=None, inferred_aws_region=None, inferred_entity_type=None, max_ttl=None, period=None, policies=None, resolve_aws_unique_ids=None, role=None, role_tag=None, token_bound_cidrs=None, token_explicit_max_ttl=None, token_max_ttl=None, token_no_default_policy=None, token_num_uses=None, token_period=None, token_policies=None, token_ttl=None, token_type=None, ttl=None, __props__=None, __name__=None, __opts__=None):
        """
        Manages an AWS auth backend role in a Vault server. Roles constrain the
        instances or principals that can perform the login operation against the
        backend. See the [Vault
        documentation](https://www.vaultproject.io/docs/auth/aws.html) for more
        information.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_instance_migration: If set to `true`, allows migration of
               the underlying instance where the client resides.
        :param pulumi.Input[str] auth_type: The auth type permitted for this role. Valid choices
               are `ec2` and `iam`. Defaults to `iam`.
        :param pulumi.Input[list] bound_account_ids: If set, defines a constraint on the EC2
               instances that can perform the login operation that they should be using the
               account ID specified by this field. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_ami_ids: If set, defines a constraint on the EC2 instances
               that can perform the login operation that they should be using the AMI ID
               specified by this field. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_iam_instance_profile_arns: If set, defines a constraint on
               the EC2 instances that can perform the login operation that they must be
               associated with an IAM instance profile ARN which has a prefix that matches
               the value specified by this field. The value is prefix-matched as though it
               were a glob ending in `*`. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_iam_principal_arns: If set, defines the IAM principal that
               must be authenticated when `auth_type` is set to `iam`. Wildcards are
               supported at the end of the ARN.
        :param pulumi.Input[list] bound_iam_role_arns: If set, defines a constraint on the EC2
               instances that can perform the login operation that they must match the IAM
               role ARN specified by this field. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_regions: If set, defines a constraint on the EC2 instances
               that can perform the login operation that the region in their identity
               document must match the one specified by this field. `auth_type` must be set
               to `ec2` or `inferred_entity_type` must be set to `ec2_instance` to use this
               constraint.
        :param pulumi.Input[list] bound_subnet_ids: If set, defines a constraint on the EC2
               instances that can perform the login operation that they be associated with
               the subnet ID that matches the value specified by this field. `auth_type`
               must be set to `ec2` or `inferred_entity_type` must be set to `ec2_instance`
               to use this constraint.
        :param pulumi.Input[list] bound_vpc_ids: If set, defines a constraint on the EC2 instances
               that can perform the login operation that they be associated with the VPC ID
               that matches the value specified by this field. `auth_type` must be set to
               `ec2` or `inferred_entity_type` must be set to `ec2_instance` to use this
               constraint.
        :param pulumi.Input[bool] disallow_reauthentication: IF set to `true`, only allows a
               single token to be granted per instance ID. This can only be set when
               `auth_type` is set to `ec2`.
        :param pulumi.Input[str] inferred_aws_region: When `inferred_entity_type` is set, this
               is the region to search for the inferred entities. Required if
               `inferred_entity_type` is set. This only applies when `auth_type` is set to
               `iam`.
        :param pulumi.Input[str] inferred_entity_type: If set, instructs Vault to turn on
               inferencing. The only valid value is `ec2_instance`, which instructs Vault to
               infer that the role comes from an EC2 instance in an IAM instance profile.
               This only applies when `auth_type` is set to `iam`.
        :param pulumi.Input[float] max_ttl: The maximum allowed lifetime of tokens
               issued using this role, provided as a number of seconds.
        :param pulumi.Input[float] period: If set, indicates that the
               token generated using this role should never expire. The token should be renewed within the
               duration specified by this value. At each renewal, the token's TTL will be set to the
               value of this field. Specified in seconds.
        :param pulumi.Input[list] policies: An array of strings
               specifying the policies to be set on tokens issued using this role.
        :param pulumi.Input[bool] resolve_aws_unique_ids: If set to `true`, the
               `bound_iam_principal_arns` are resolved to [AWS Unique
               IDs](http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-unique-ids)
               for the bound principal ARN. This field is ignored when a
               `bound_iam_principal_arn` ends in a wildcard. Resolving to unique IDs more
               closely mimics the behavior of AWS services in that if an IAM user or role is
               deleted and a new one is recreated with the same name, those new users or
               roles won't get access to roles in Vault that were permissioned to the prior
               principals of the same name. Defaults to `true`.
               Once set to `true`, this cannot be changed to `false` without recreating the role.
        :param pulumi.Input[str] role: The name of the role.
        :param pulumi.Input[str] role_tag: If set, enable role tags for this role. The value set
               for this field should be the key of the tag on the EC2 instance. `auth_type`
               must be set to `ec2` or `inferred_entity_type` must be set to `ec2_instance`
               to use this constraint.
        :param pulumi.Input[list] token_bound_cidrs: List of CIDR blocks; if set, specifies blocks of IP
               addresses which can authenticate successfully, and ties the resulting token to these blocks
               as well.
        :param pulumi.Input[float] token_explicit_max_ttl: If set, will encode an
               [explicit max TTL](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls)
               onto the token in number of seconds. This is a hard cap even if `token_ttl` and
               `token_max_ttl` would otherwise allow a renewal.
        :param pulumi.Input[float] token_max_ttl: The maximum lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[bool] token_no_default_policy: If set, the default policy will not be set on
               generated tokens; otherwise it will be added to the policies set in token_policies.
        :param pulumi.Input[float] token_num_uses: The
               [period](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls),
               if any, in number of seconds to set on the token.
        :param pulumi.Input[float] token_period: If set, indicates that the
               token generated using this role should never expire. The token should be renewed within the
               duration specified by this value. At each renewal, the token's TTL will be set to the
               value of this field. Specified in seconds.
        :param pulumi.Input[list] token_policies: List of policies to encode onto generated tokens. Depending
               on the auth method, this list may be supplemented by user/group/other values.
        :param pulumi.Input[float] token_ttl: The incremental lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[str] token_type: The type of token that should be generated. Can be `service`,
               `batch`, or `default` to use the mount's tuned default (which unless changed will be
               `service` tokens). For token store roles, there are two additional possibilities:
               `default-service` and `default-batch` which specify the type to return unless the client
               requests a different type at generation time.
        :param pulumi.Input[float] ttl: The TTL period of tokens issued
               using this role, provided as a number of seconds.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/aws_auth_backend_role.html.markdown.
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

            __props__['allow_instance_migration'] = allow_instance_migration
            __props__['auth_type'] = auth_type
            __props__['backend'] = backend
            __props__['bound_account_ids'] = bound_account_ids
            __props__['bound_ami_ids'] = bound_ami_ids
            __props__['bound_ec2_instance_ids'] = bound_ec2_instance_ids
            __props__['bound_iam_instance_profile_arns'] = bound_iam_instance_profile_arns
            __props__['bound_iam_principal_arns'] = bound_iam_principal_arns
            __props__['bound_iam_role_arns'] = bound_iam_role_arns
            __props__['bound_regions'] = bound_regions
            __props__['bound_subnet_ids'] = bound_subnet_ids
            __props__['bound_vpc_ids'] = bound_vpc_ids
            __props__['disallow_reauthentication'] = disallow_reauthentication
            __props__['inferred_aws_region'] = inferred_aws_region
            __props__['inferred_entity_type'] = inferred_entity_type
            __props__['max_ttl'] = max_ttl
            __props__['period'] = period
            __props__['policies'] = policies
            __props__['resolve_aws_unique_ids'] = resolve_aws_unique_ids
            if role is None:
                raise TypeError("Missing required property 'role'")
            __props__['role'] = role
            __props__['role_tag'] = role_tag
            __props__['token_bound_cidrs'] = token_bound_cidrs
            __props__['token_explicit_max_ttl'] = token_explicit_max_ttl
            __props__['token_max_ttl'] = token_max_ttl
            __props__['token_no_default_policy'] = token_no_default_policy
            __props__['token_num_uses'] = token_num_uses
            __props__['token_period'] = token_period
            __props__['token_policies'] = token_policies
            __props__['token_ttl'] = token_ttl
            __props__['token_type'] = token_type
            __props__['ttl'] = ttl
        super(AuthBackendRole, __self__).__init__(
            'vault:aws/authBackendRole:AuthBackendRole',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, allow_instance_migration=None, auth_type=None, backend=None, bound_account_ids=None, bound_ami_ids=None, bound_ec2_instance_ids=None, bound_iam_instance_profile_arns=None, bound_iam_principal_arns=None, bound_iam_role_arns=None, bound_regions=None, bound_subnet_ids=None, bound_vpc_ids=None, disallow_reauthentication=None, inferred_aws_region=None, inferred_entity_type=None, max_ttl=None, period=None, policies=None, resolve_aws_unique_ids=None, role=None, role_tag=None, token_bound_cidrs=None, token_explicit_max_ttl=None, token_max_ttl=None, token_no_default_policy=None, token_num_uses=None, token_period=None, token_policies=None, token_ttl=None, token_type=None, ttl=None):
        """
        Get an existing AuthBackendRole resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] allow_instance_migration: If set to `true`, allows migration of
               the underlying instance where the client resides.
        :param pulumi.Input[str] auth_type: The auth type permitted for this role. Valid choices
               are `ec2` and `iam`. Defaults to `iam`.
        :param pulumi.Input[list] bound_account_ids: If set, defines a constraint on the EC2
               instances that can perform the login operation that they should be using the
               account ID specified by this field. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_ami_ids: If set, defines a constraint on the EC2 instances
               that can perform the login operation that they should be using the AMI ID
               specified by this field. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_iam_instance_profile_arns: If set, defines a constraint on
               the EC2 instances that can perform the login operation that they must be
               associated with an IAM instance profile ARN which has a prefix that matches
               the value specified by this field. The value is prefix-matched as though it
               were a glob ending in `*`. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_iam_principal_arns: If set, defines the IAM principal that
               must be authenticated when `auth_type` is set to `iam`. Wildcards are
               supported at the end of the ARN.
        :param pulumi.Input[list] bound_iam_role_arns: If set, defines a constraint on the EC2
               instances that can perform the login operation that they must match the IAM
               role ARN specified by this field. `auth_type` must be set to `ec2` or
               `inferred_entity_type` must be set to `ec2_instance` to use this constraint.
        :param pulumi.Input[list] bound_regions: If set, defines a constraint on the EC2 instances
               that can perform the login operation that the region in their identity
               document must match the one specified by this field. `auth_type` must be set
               to `ec2` or `inferred_entity_type` must be set to `ec2_instance` to use this
               constraint.
        :param pulumi.Input[list] bound_subnet_ids: If set, defines a constraint on the EC2
               instances that can perform the login operation that they be associated with
               the subnet ID that matches the value specified by this field. `auth_type`
               must be set to `ec2` or `inferred_entity_type` must be set to `ec2_instance`
               to use this constraint.
        :param pulumi.Input[list] bound_vpc_ids: If set, defines a constraint on the EC2 instances
               that can perform the login operation that they be associated with the VPC ID
               that matches the value specified by this field. `auth_type` must be set to
               `ec2` or `inferred_entity_type` must be set to `ec2_instance` to use this
               constraint.
        :param pulumi.Input[bool] disallow_reauthentication: IF set to `true`, only allows a
               single token to be granted per instance ID. This can only be set when
               `auth_type` is set to `ec2`.
        :param pulumi.Input[str] inferred_aws_region: When `inferred_entity_type` is set, this
               is the region to search for the inferred entities. Required if
               `inferred_entity_type` is set. This only applies when `auth_type` is set to
               `iam`.
        :param pulumi.Input[str] inferred_entity_type: If set, instructs Vault to turn on
               inferencing. The only valid value is `ec2_instance`, which instructs Vault to
               infer that the role comes from an EC2 instance in an IAM instance profile.
               This only applies when `auth_type` is set to `iam`.
        :param pulumi.Input[float] max_ttl: The maximum allowed lifetime of tokens
               issued using this role, provided as a number of seconds.
        :param pulumi.Input[float] period: If set, indicates that the
               token generated using this role should never expire. The token should be renewed within the
               duration specified by this value. At each renewal, the token's TTL will be set to the
               value of this field. Specified in seconds.
        :param pulumi.Input[list] policies: An array of strings
               specifying the policies to be set on tokens issued using this role.
        :param pulumi.Input[bool] resolve_aws_unique_ids: If set to `true`, the
               `bound_iam_principal_arns` are resolved to [AWS Unique
               IDs](http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-unique-ids)
               for the bound principal ARN. This field is ignored when a
               `bound_iam_principal_arn` ends in a wildcard. Resolving to unique IDs more
               closely mimics the behavior of AWS services in that if an IAM user or role is
               deleted and a new one is recreated with the same name, those new users or
               roles won't get access to roles in Vault that were permissioned to the prior
               principals of the same name. Defaults to `true`.
               Once set to `true`, this cannot be changed to `false` without recreating the role.
        :param pulumi.Input[str] role: The name of the role.
        :param pulumi.Input[str] role_tag: If set, enable role tags for this role. The value set
               for this field should be the key of the tag on the EC2 instance. `auth_type`
               must be set to `ec2` or `inferred_entity_type` must be set to `ec2_instance`
               to use this constraint.
        :param pulumi.Input[list] token_bound_cidrs: List of CIDR blocks; if set, specifies blocks of IP
               addresses which can authenticate successfully, and ties the resulting token to these blocks
               as well.
        :param pulumi.Input[float] token_explicit_max_ttl: If set, will encode an
               [explicit max TTL](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls)
               onto the token in number of seconds. This is a hard cap even if `token_ttl` and
               `token_max_ttl` would otherwise allow a renewal.
        :param pulumi.Input[float] token_max_ttl: The maximum lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[bool] token_no_default_policy: If set, the default policy will not be set on
               generated tokens; otherwise it will be added to the policies set in token_policies.
        :param pulumi.Input[float] token_num_uses: The
               [period](https://www.vaultproject.io/docs/concepts/tokens.html#token-time-to-live-periodic-tokens-and-explicit-max-ttls),
               if any, in number of seconds to set on the token.
        :param pulumi.Input[float] token_period: If set, indicates that the
               token generated using this role should never expire. The token should be renewed within the
               duration specified by this value. At each renewal, the token's TTL will be set to the
               value of this field. Specified in seconds.
        :param pulumi.Input[list] token_policies: List of policies to encode onto generated tokens. Depending
               on the auth method, this list may be supplemented by user/group/other values.
        :param pulumi.Input[float] token_ttl: The incremental lifetime for generated tokens in number of seconds.
               Its current value will be referenced at renewal time.
        :param pulumi.Input[str] token_type: The type of token that should be generated. Can be `service`,
               `batch`, or `default` to use the mount's tuned default (which unless changed will be
               `service` tokens). For token store roles, there are two additional possibilities:
               `default-service` and `default-batch` which specify the type to return unless the client
               requests a different type at generation time.
        :param pulumi.Input[float] ttl: The TTL period of tokens issued
               using this role, provided as a number of seconds.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/aws_auth_backend_role.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["allow_instance_migration"] = allow_instance_migration
        __props__["auth_type"] = auth_type
        __props__["backend"] = backend
        __props__["bound_account_ids"] = bound_account_ids
        __props__["bound_ami_ids"] = bound_ami_ids
        __props__["bound_ec2_instance_ids"] = bound_ec2_instance_ids
        __props__["bound_iam_instance_profile_arns"] = bound_iam_instance_profile_arns
        __props__["bound_iam_principal_arns"] = bound_iam_principal_arns
        __props__["bound_iam_role_arns"] = bound_iam_role_arns
        __props__["bound_regions"] = bound_regions
        __props__["bound_subnet_ids"] = bound_subnet_ids
        __props__["bound_vpc_ids"] = bound_vpc_ids
        __props__["disallow_reauthentication"] = disallow_reauthentication
        __props__["inferred_aws_region"] = inferred_aws_region
        __props__["inferred_entity_type"] = inferred_entity_type
        __props__["max_ttl"] = max_ttl
        __props__["period"] = period
        __props__["policies"] = policies
        __props__["resolve_aws_unique_ids"] = resolve_aws_unique_ids
        __props__["role"] = role
        __props__["role_tag"] = role_tag
        __props__["token_bound_cidrs"] = token_bound_cidrs
        __props__["token_explicit_max_ttl"] = token_explicit_max_ttl
        __props__["token_max_ttl"] = token_max_ttl
        __props__["token_no_default_policy"] = token_no_default_policy
        __props__["token_num_uses"] = token_num_uses
        __props__["token_period"] = token_period
        __props__["token_policies"] = token_policies
        __props__["token_ttl"] = token_ttl
        __props__["token_type"] = token_type
        __props__["ttl"] = ttl
        return AuthBackendRole(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

