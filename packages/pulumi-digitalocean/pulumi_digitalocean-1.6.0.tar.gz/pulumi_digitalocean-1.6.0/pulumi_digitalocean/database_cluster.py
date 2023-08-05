# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import json
import warnings
import pulumi
import pulumi.runtime
from typing import Union
from . import utilities, tables

class DatabaseCluster(pulumi.CustomResource):
    database: pulumi.Output[str]
    """
    Name of the cluster's default database.
    """
    engine: pulumi.Output[str]
    """
    Database engine used by the cluster (ex. `pg` for PostreSQL, `mysql` for MySQL, or `redis` for Redis).
    """
    eviction_policy: pulumi.Output[str]
    """
    A string specifying the eviction policy for a Redis cluster. Valid values are: `noeviction`, `allkeys_lru`, `allkeys_random`, `volatile_lru`, `volatile_random`, or `volatile_ttl`.
    """
    host: pulumi.Output[str]
    """
    Database cluster's hostname.
    """
    maintenance_windows: pulumi.Output[list]
    """
    Defines when the automatic maintenance should be performed for the database cluster.
    
      * `day` (`str`) - The day of the week on which to apply maintenance updates.
      * `hour` (`str`) - The hour in UTC at which maintenance updates will be applied in 24 hour format.
    """
    name: pulumi.Output[str]
    """
    The name of the database cluster.
    """
    node_count: pulumi.Output[float]
    """
    Number of nodes that will be included in the cluster.
    """
    password: pulumi.Output[str]
    """
    Password for the cluster's default user.
    """
    port: pulumi.Output[float]
    """
    Network port that the database cluster is listening on.
    """
    private_host: pulumi.Output[str]
    """
    Same as `host`, but only accessible from resources within the account and in the same region.
    """
    private_uri: pulumi.Output[str]
    """
    Same as `uri`, but only accessible from resources within the account and in the same region.
    """
    region: pulumi.Output[str]
    """
    DigitalOcean region where the cluster will reside.
    """
    size: pulumi.Output[str]
    """
    Database Droplet size associated with the cluster (ex. `db-s-1vcpu-1gb`).
    """
    sql_mode: pulumi.Output[str]
    """
    A comma separated string specifying the  SQL modes for a MySQL cluster.
    """
    tags: pulumi.Output[list]
    """
    A list of tag names to be applied to the database cluster.
    """
    uri: pulumi.Output[str]
    """
    The full URI for connecting to the database cluster.
    """
    urn: pulumi.Output[str]
    """
    The uniform resource name of the database cluster.
    """
    user: pulumi.Output[str]
    """
    Username for the cluster's default user.
    """
    version: pulumi.Output[str]
    """
    Engine version used by the cluster (ex. `11` for PostgreSQL 11).
    """
    def __init__(__self__, resource_name, opts=None, engine=None, eviction_policy=None, maintenance_windows=None, name=None, node_count=None, region=None, size=None, sql_mode=None, tags=None, version=None, __props__=None, __name__=None, __opts__=None):
        """
        Provides a DigitalOcean database cluster resource.
        
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] engine: Database engine used by the cluster (ex. `pg` for PostreSQL, `mysql` for MySQL, or `redis` for Redis).
        :param pulumi.Input[str] eviction_policy: A string specifying the eviction policy for a Redis cluster. Valid values are: `noeviction`, `allkeys_lru`, `allkeys_random`, `volatile_lru`, `volatile_random`, or `volatile_ttl`.
        :param pulumi.Input[list] maintenance_windows: Defines when the automatic maintenance should be performed for the database cluster.
        :param pulumi.Input[str] name: The name of the database cluster.
        :param pulumi.Input[float] node_count: Number of nodes that will be included in the cluster.
        :param pulumi.Input[str] region: DigitalOcean region where the cluster will reside.
        :param pulumi.Input[str] size: Database Droplet size associated with the cluster (ex. `db-s-1vcpu-1gb`).
        :param pulumi.Input[str] sql_mode: A comma separated string specifying the  SQL modes for a MySQL cluster.
        :param pulumi.Input[list] tags: A list of tag names to be applied to the database cluster.
        :param pulumi.Input[str] version: Engine version used by the cluster (ex. `11` for PostgreSQL 11).
        
        The **maintenance_windows** object supports the following:
        
          * `day` (`pulumi.Input[str]`) - The day of the week on which to apply maintenance updates.
          * `hour` (`pulumi.Input[str]`) - The hour in UTC at which maintenance updates will be applied in 24 hour format.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-digitalocean/blob/master/website/docs/r/database_cluster.html.markdown.
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

            if engine is None:
                raise TypeError("Missing required property 'engine'")
            __props__['engine'] = engine
            __props__['eviction_policy'] = eviction_policy
            __props__['maintenance_windows'] = maintenance_windows
            __props__['name'] = name
            if node_count is None:
                raise TypeError("Missing required property 'node_count'")
            __props__['node_count'] = node_count
            if region is None:
                raise TypeError("Missing required property 'region'")
            __props__['region'] = region
            if size is None:
                raise TypeError("Missing required property 'size'")
            __props__['size'] = size
            __props__['sql_mode'] = sql_mode
            __props__['tags'] = tags
            __props__['version'] = version
            __props__['database'] = None
            __props__['host'] = None
            __props__['password'] = None
            __props__['port'] = None
            __props__['private_host'] = None
            __props__['private_uri'] = None
            __props__['uri'] = None
            __props__['urn'] = None
            __props__['user'] = None
        super(DatabaseCluster, __self__).__init__(
            'digitalocean:index/databaseCluster:DatabaseCluster',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name, id, opts=None, database=None, engine=None, eviction_policy=None, host=None, maintenance_windows=None, name=None, node_count=None, password=None, port=None, private_host=None, private_uri=None, region=None, size=None, sql_mode=None, tags=None, uri=None, urn=None, user=None, version=None):
        """
        Get an existing DatabaseCluster resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.
        
        :param str resource_name: The unique name of the resulting resource.
        :param str id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: Name of the cluster's default database.
        :param pulumi.Input[str] engine: Database engine used by the cluster (ex. `pg` for PostreSQL, `mysql` for MySQL, or `redis` for Redis).
        :param pulumi.Input[str] eviction_policy: A string specifying the eviction policy for a Redis cluster. Valid values are: `noeviction`, `allkeys_lru`, `allkeys_random`, `volatile_lru`, `volatile_random`, or `volatile_ttl`.
        :param pulumi.Input[str] host: Database cluster's hostname.
        :param pulumi.Input[list] maintenance_windows: Defines when the automatic maintenance should be performed for the database cluster.
        :param pulumi.Input[str] name: The name of the database cluster.
        :param pulumi.Input[float] node_count: Number of nodes that will be included in the cluster.
        :param pulumi.Input[str] password: Password for the cluster's default user.
        :param pulumi.Input[float] port: Network port that the database cluster is listening on.
        :param pulumi.Input[str] private_host: Same as `host`, but only accessible from resources within the account and in the same region.
        :param pulumi.Input[str] private_uri: Same as `uri`, but only accessible from resources within the account and in the same region.
        :param pulumi.Input[str] region: DigitalOcean region where the cluster will reside.
        :param pulumi.Input[str] size: Database Droplet size associated with the cluster (ex. `db-s-1vcpu-1gb`).
        :param pulumi.Input[str] sql_mode: A comma separated string specifying the  SQL modes for a MySQL cluster.
        :param pulumi.Input[list] tags: A list of tag names to be applied to the database cluster.
        :param pulumi.Input[str] uri: The full URI for connecting to the database cluster.
        :param pulumi.Input[str] urn: The uniform resource name of the database cluster.
        :param pulumi.Input[str] user: Username for the cluster's default user.
        :param pulumi.Input[str] version: Engine version used by the cluster (ex. `11` for PostgreSQL 11).
        
        The **maintenance_windows** object supports the following:
        
          * `day` (`pulumi.Input[str]`) - The day of the week on which to apply maintenance updates.
          * `hour` (`pulumi.Input[str]`) - The hour in UTC at which maintenance updates will be applied in 24 hour format.

        > This content is derived from https://github.com/terraform-providers/terraform-provider-digitalocean/blob/master/website/docs/r/database_cluster.html.markdown.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = dict()
        __props__["database"] = database
        __props__["engine"] = engine
        __props__["eviction_policy"] = eviction_policy
        __props__["host"] = host
        __props__["maintenance_windows"] = maintenance_windows
        __props__["name"] = name
        __props__["node_count"] = node_count
        __props__["password"] = password
        __props__["port"] = port
        __props__["private_host"] = private_host
        __props__["private_uri"] = private_uri
        __props__["region"] = region
        __props__["size"] = size
        __props__["sql_mode"] = sql_mode
        __props__["tags"] = tags
        __props__["uri"] = uri
        __props__["urn"] = urn
        __props__["user"] = user
        __props__["version"] = version
        return DatabaseCluster(resource_name, opts=opts, __props__=__props__)
    def translate_output_property(self, prop):
        return tables._CAMEL_TO_SNAKE_CASE_TABLE.get(prop) or prop

    def translate_input_property(self, prop):
        return tables._SNAKE_TO_CAMEL_CASE_TABLE.get(prop) or prop

