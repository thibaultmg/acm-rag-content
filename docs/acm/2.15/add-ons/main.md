# Managed cluster advanced configuration

## Enabling klusterlet add-ons on clusters for cluster management

After you install Red Hat Advanced Cluster Management for Kubernetes and
then create or import clusters with multicluster engine operator you can
enable the klusterlet add-ons for those managed clusters. The klusterlet
add-ons are not enabled by default if you created or imported clusters
unless you create or import with the Red Hat Advanced Cluster Management
console. See the following available klusterlet add-ons:

- application-manager

- cert-policy-controller

- config-policy-controller

- governance-policy-framework

- search-collector

Complete the following steps to enable the klusterlet add-ons for the
managed clusters after Red Hat Advanced Cluster Management is installed:

1.  Create a YAML file that is similar to the following
    `KlusterletAddonConfig`, with the `spec` value that represents the
    add-ons:

    ``` yaml
    apiVersion: agent.open-cluster-management.io/v1
    kind: KlusterletAddonConfig
    metadata:
      name: <cluster_name>
      namespace: <cluster_name>
    spec:
      applicationManager:
        enabled: true
      certPolicyController:
        enabled: true
      policyController: 
        enabled: true
      searchCollector:
        enabled: true
    ```

    - The `policy-controller` add-on is divided into two add-ons: The
      `governance-policy-framework` and the `config-policy-controller`.
      As a result, the `policyController` controls the
      `governance-policy-framework` and the `config-policy-controller`
      `managedClusterAddons`.

2.  Save the file as `klusterlet-addon-config.yaml`.

3.  Apply the YAML by running the following command on the hub cluster:

        oc apply -f klusterlet-addon-config.yaml

4.  To verify whether the enabled `managedClusterAddons` are created
    after the `KlusterletAddonConfig` is created, run the following
    command:

        oc get managedclusteraddons -n <cluster namespace>

## Configuring klusterlet add-ons

In Red Hat Advanced Cluster Management, you can configure the following
klusterlet add-ons to improve the performance and functionality of your
managed clusters:

- application-manager

- cert-policy-controller

- cluster-proxy

- config-policy-controller

- governance-policy-framework

- hypershift-addon

- managed-serviceaccount

- observability-controller

- search-collector

- submariner

- volsync

- work-manager

**Important:** You cannot configure `resourceRequirements` for the
`observability-controller` add-on.

### Setting up the *AddOnDeploymentConfig* to configure klusterlet add-ons

When you configure the klusterlet add-ons, you can apply specifications
to any of the add-ons on each of your managed clusters, such as the
`nodeSelector` and `tolerations`. To configure the klusterlet add-on,
complete the following steps:

1.  Use the `AddonDeploymentConfig` API to create an add-on
    configuration in any namespace on the hub cluster.

2.  Create a file named `addondeploymentconfig.yaml` with the following
    template:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: AddOnDeploymentConfig
    metadata:
      name: config-name 
      namespace: config-namespace 
    spec:
      nodePlacement:
        nodeSelector: {<node-selector>} 
        tolerations: {<tolerations>} 
      resourceRequirements: 
      - containerID: "<workload-kind>:<workload-name>:<container-name>" 
        resources:
          requests:
            memory: 75Mi
          limits:
            memory: 150Mi
    ```

    - Replace `config-name` with the name of the `AddonDeploymentConfig`
      that you created.

    - Replace `config-namespace` with the namespace of the
      `AddonDeploymentConfig` that you created.

    - Replace `<node-selector>` with your node selector.

    - Replace `<tolerations>` with your tolerations.

    - List resource requirements here to override the `resources` of the
      add-on workload containers. If an add-on container matches more
      than one of the items in the list, the last matching configuration
      is applied.

    - Replace `<workload-kind>` with the kind of workload, for example:
      `deployment`. Replace `<workload-name>` with the name of the
      workload. Replace `<container-name>` with the name of the
      container.

      1.  For any of these values, you can use `*` attribute to apply
          the configuration to all objects managed by the add-on. For
          example, if you used the `*:*:*` attribute , it would apply
          the configuration to every container of every workload kind in
          any add-on the configuration is attached to.

          A completed `AddOnDeploymentConfig` resembles the following
          example:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: AddOnDeploymentConfig
    metadata:
      name: deploy-config
      namespace: open-cluster-management-hub
    spec:
      nodePlacement:
        nodeSelector:
          "node-dedicated": "acm-addon"
        tolerations:
          - effect: NoSchedule
            key: node-dedicated
            value: acm-addon
            operator: Equal
    ```

### Configuring a klusterlet add-on for all managed clusters

After you set up the `AddOnDeploymentConfig`, you can configure it with
the `ClusterManagementAddOn` which then applies this add-on
configuration to all your managed clusters that are attached to the hub
cluster. To configure a klusterlet add-on for all managed clusters,
complete the following steps:

1.  Apply the `AddOnDeploymentConfig` file to your klusterlet add-on by
    running the following command:

    ``` bash
    oc apply -f addondeploymentconfig.yaml
    ```

2.  Connect the new configuration that you created to an add-on for all
    of your managed clusters by patching the `ClusterManagementAddOn`
    resource. Run the following command to patch the
    `spec.supportedConfigs` parameter in the `ClusterManagementAddOn` to
    point to the new configuration:

    ``` bash
    oc patch clustermanagementaddons <addon-name> --type='json' -p='[{
      "op":"add",
      "path":"/spec/supportedConfigs",
      "value":[{
        "group":"addon.open-cluster-management.io",
        "resource":"addondeploymentconfigs",
        "defaultConfig":{"name":"<config-name>","namespace":"<config-namespace>"}
      }]
    }]'
    ```

    - Replace `<addon-name>` with your add-on name.

    - Replace `<config-name>` with the name of the
      `AddonDeploymentConfig` that you created.

    - Replace `<config-namespace>` with the namespace of the
      `AddonDeploymentConfig` that you created.

### Configuring a klusterlet add-on for a single managed cluster

You can also override the global default `AddonDeploymentConfig`
configuration for your add-on on a certain managed cluster. By
overriding, you can configure a klusterlet add-on for a single managed
cluster because the add-on configuration only applies to a the
particular managed cluster attached to that namespace of the hub
cluster. To override configurations, complete the following steps:

1.  Use the `AddonDeploymentConfig` API to create another configuration
    to specify the `nodeSelector` and `tolerations` on the hub cluster.

2.  Connect the new configuration that you created to your
    `ManagedClusterAddOn` add-on on the hub cluster in the managed
    cluster namespace. Run the following command to patch the
    `spec.configs` parameter in the `ManagedClusterAddOn` to point to
    the new configuration:

    ``` bash
    oc -n <managed-cluster> patch managedclusteraddons <addon-name> --type='json' -p='[{
      "op":"add",
      "path":"/spec/configs",
      "value":[{
        "group":"addon.open-cluster-management.io",
        "resource":"addondeploymentconfigs",
        "namespace":"<config-namespace>",
        "name":"<config-name>"
      }]
    }]'
    ```

    - Replace `managed-cluster` with your managed cluster name

    - Replace `addon-name` with your add-on name

    - Replace `config-namespace` with the namespace of the
      `AddonDeploymentConfig` that you created

    - Replace `config-name` with the name of the `AddonDeploymentConfig`
      that you created

The new configuration that you referenced in the `ManagedClusterAddOn`
add-on overrides the global default configuration that you defined
earlier in the `ClusterManagementAddOn` add-on.

To make sure that you can deploy your content to the correct nodes, see
Optional: Configuring the klusterlet to run on specific nodes.

## Enabling cluster-wide proxy on existing cluster add-ons

You can configure the `KlusterletAddonConfig` in the cluster namespace
to add the proxy environment variables to all the klusterlet add-on pods
of the managed Red Hat OpenShift Container Platform clusters. Complete
the following steps to configure the `KlusterletAddonConfig` to add the
three environment variables to the pods of the klusterlet add-ons:

1.  Edit the `KlusterletAddonConfig` file that is in the namespace of
    the cluster that needs the proxy. You can use the console to find
    the resource, or you can edit from the terminal with the following
    command:

        oc -n <my-cluster-name> edit klusterletaddonconfig <my-cluster-name>

    **Note:** If you are working with only one cluster, you do not need
    `<my-cluster-name>` at the end of your command. See the following
    command:

        oc -n <my-cluster-name> edit klusterletaddonconfig

2.  Edit the `.spec.proxyConfig` section of the file so it resembles the
    following example. The `spec.proxyConfig` is an optional section:

    ``` yaml
    spec
      proxyConfig:
        httpProxy: "<proxy_not_secure>" 
        httpsProxy: "<proxy_secure>" 
        noProxy: "<no_proxy>" 
    ```

    - Replace `proxy_not_secure` with the address of the proxy server
      for `http` requests. For example, use
      `http://192.168.123.145:3128`.

    - Replace `proxy_secure` with the address of the proxy server for
      `https` requests. For example, use `https://192.168.123.145:3128`.

    - Replace `no_proxy` with a comma delimited list of IP addresses,
      hostnames, and domain names where traffic is not routed through
      the proxy. For example, use
      `.cluster.local,.svc,10.128.0.0/14,example.com`.

      If the OpenShift Container Platform cluster is created with
      cluster wide proxy configured on the hub cluster, the cluster wide
      proxy configuration values are added to the pods of the klusterlet
      add-ons as environment variables when the following conditions are
      met:

      - The `.spec.policyController.proxyPolicy` in the `addon` section
        is enabled and set to `OCPGlobalProxy`.

      - The `.spec.applicationManager.proxyPolicy` is enabled and set to
        `CustomProxy`.

        **Note:** The default value of `proxyPolicy` in the `addon`
        section is `Disabled`.

        See the following examples of `proxyPolicy` entries:

        ``` yaml
        apiVersion: agent.open-cluster-management.io/v1
            kind: KlusterletAddonConfig
            metadata:
              name: clusterName
              namespace: clusterName
            spec:
              proxyConfig:
                httpProxy: http://pxuser:12345@10.0.81.15:3128
                httpsProxy: http://pxuser:12345@10.0.81.15:3128
                noProxy: .cluster.local,.svc,10.128.0.0/14, example.com
              applicationManager:
                enabled: true
                proxyPolicy: CustomProxy
              policyController:
                enabled: true
                proxyPolicy: OCPGlobalProxy
              searchCollector:
                enabled: true
                proxyPolicy: Disabled
              certPolicyController:
                enabled: true
                proxyPolicy: Disabled
        ```

**Important:** Global proxy settings do not impact alert forwarding. To
set up alert forwarding for Red Hat Advanced Cluster Management hub
clusters with a cluster-wide proxy, see Forwarding alerts for more
details.

## Modifying the klusterlet add-ons settings of your cluster

You can modify the settings of `KlusterletAddonConfig` to change your
configuration using the hub cluster.

The `KlusterletAddonConfig` controller manages the functions that are
enabled and disabled according to the settings in the
`klusterletaddonconfigs.agent.open-cluster-management.io` Kubernetes
resource. View the following example of the `KlusterletAddonConfig`,
where the value for `<2.x.0>` is replaced with supported version you are
using:

``` yaml
apiVersion: agent.open-cluster-management.io/v1
kind: KlusterletAddonConfig
metadata:
  name: <cluster-name>
  namespace: <cluster-name>
spec:
  clusterName: <cluster-name>
  clusterNamespace: <cluster-name>
  clusterLabels:
    cloud: auto-detect
    vendor: auto-detect
  applicationManager:
    enabled: true
  certPolicyController:
    enabled: true
  policyController:
    enabled: true
  searchCollector:
    enabled: false
  version: <2.x.0>
```

### Description of klusterlet add-ons settings

The following settings can be updated in the
`klusterletaddonconfigs.agent.open-cluster-management.io` Kubernetes
resource:

- Setting name: applicationmanager - Value: true or false - Description:
  This controller manages the application subscription lifecycle on the
  managed cluster.

- Setting name: certPolicyController - Value: true or false -
  Description: This controller enforces certificate-based policies on
  the managed cluster.

- Setting name: policyController - Value: true or false - Description:
  This controller enforces all other policy rules on the managed
  cluster.

- Setting name: searchCollector - Value: true or false - Description:
  This controller is used to periodically push the resource index data
  back to the hub cluster.

### Modify using the console on the hub cluster

You can modify the settings of the
`klusterletaddonconfigs.agent.open-cluster-management.io` resource by
using the hub cluster. Complete the following steps to change the
settings:

1.  Log in to the Red Hat Advanced Cluster Management for Kubernetes
    console of the hub cluster.

2.  From the header menu of the hub cluster console, select the
    **Search** icon.

3.  In the search parameters, enter the following value:
    `kind:klusterletaddonconfigs`

4.  Select the endpoint resource that you want to update.

5.  Find the `spec` section and select **Edit** to edit the content.

6.  Modify your settings.

7.  Select **Save** to apply your changes.

### Modify using the command line on the hub cluster

You must have access to the `cluster-name` namespace to modify your
settings by using the hub cluster. Complete the following steps:

1.  Log in to the hub cluster.

2.  Enter the following command to edit the resource:

        kubectl edit klusterletaddonconfigs.agent.open-cluster-management.io <cluster-name> -n <cluster-name>

3.  Find the `spec` section.

4.  Modify your settings, as necessary.
