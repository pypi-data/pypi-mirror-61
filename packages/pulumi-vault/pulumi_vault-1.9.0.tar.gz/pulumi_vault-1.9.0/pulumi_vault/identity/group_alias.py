# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from .. import utilities, tables

class GroupAlias(pulumi.CustomResource):
    canonical_id: pulumi.Output[str]
    """
    ID of the group to which this is an alias.
    """
    mount_accessor: pulumi.Output[str]
    """
    Mount accessor of the authentication backend to which this alias belongs to.
    """
    name: pulumi.Output[str]
    """
    Name of the group alias to create.
    """
    def __init__(__self__, resource_name, opts=None, canonical_id=None, mount_accessor=None, name=None, __props__=None, __name__=None, __opts__=None):
        """
        Creates an Identity Group Alias for Vault. The [Identity secrets engine](https://www.vaultproject.io/docs/secrets/identity/index.html) is the identity management solution for Vault.
        
        Group aliases allows entity membership in external groups to be managed semi-automatically. External group serves as a mapping to a group that is outside of the identity store. External groups can have one (and only one) alias. This alias should map to a notion of group that is outside of the identity store. For example, groups in LDAP, and teams in GitHub. A username in LDAP, belonging to a group in LDAP, can get its entity ID added as a member of a group in Vault automatically during logins and token renewals. This works only if the group in Vault is an external group and has an alias that maps to the group in LDAP. If the user is removed from the group in LDAP, that change gets reflected in Vault only upon the subsequent login or renewal operation.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] canonical_id: ID of the group to which this is an alias.
        :param pulumi.Input[str] mount_accessor: Mount accessor of the authentication backend to which this alias belongs to.
        :param pulumi.Input[str] name: Name of the group alias to create.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/identity_group_alias.html.markdown.
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

            if canonical_id is None:
                raise TypeError("Missing required property 'canonical_id'")
            __props__['canonical_id'] = canonical_id
            if mount_accessor is None:
                raise TypeError("Missing required property 'mount_accessor'")
            __props__['mount_accessor'] = mount_accessor
            if name is None:
                raise TypeError("Missing required property 'name'")
            __props__['name'] = name
        super(GroupAlias, __self__).__init__(
            'vault:identity/groupAlias:GroupAlias',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, canonical_id=None, mount_accessor=None, name=None):
        """
        Get an existing GroupAlias resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] canonical_id: ID of the group to which this is an alias.
        :param pulumi.Input[str] mount_accessor: Mount accessor of the authentication backend to which this alias belongs to.
        :param pulumi.Input[str] name: Name of the group alias to create.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-vault/blob/master/website/docs/r/identity_group_alias.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["canonical_id"] = canonical_id
        __props__["mount_accessor"] = mount_accessor
        __props__["name"] = name
        return GroupAlias(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

