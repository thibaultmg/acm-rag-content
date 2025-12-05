# multicluster engine operator with Red Hat Advanced Cluster Management integration

## Discovering multicluster engine operator hosted clusters in Red Hat Advanced Cluster Management

If you have multicluster engine operator clusters that are hosting
multiple *hosted clusters*, you can bring those hosted clusters to a Red
Hat Advanced Cluster Management hub cluster to manage with Red Hat
Advanced Cluster Management components, such as *Application lifecycle*
and *Governance*.

Those hosted clusters can be automatically discovered and imported as
managed clusters.

**Note:** Since the hosted control planes run on the managed
multicluster engine operator cluster nodes, the number of hosted control
planes that the cluster can host is determined by the resource
availability of managed multicluster engine operator cluster nodes, as
well as the number of managed multicluster engine operator clusters. You
can add more nodes or managed clusters to host more hosted control
planes.

**Required access:** Cluster administrator

<div>

<div class="title">

Prerequisites

</div>

- You need one or more multicluster engine operator clusters.

- You need a Red Hat Advanced Cluster Management cluster that is set as
  your hub cluster.

- Install the `clusteradm` CLI by running the following command:

  ``` bash
  curl -L https://raw.githubusercontent.com/open-cluster-management-io/clusteradm/main/install.sh | bash
  ```

</div>

### Configuring Red Hat Advanced Cluster Management to import multicluster engine operator clusters

multicluster engine operator has a `local-cluster`, which is a hub
cluster that is managed. The following default addons are enabled for
this `local-cluster` in the `open-cluster-management-agent-addon`
namespace:

- `cluster-proxy`

- `managed-serviceaccount`

- `work-manager`

Next you can configure add-ons. When your multicluster engine operator
is imported into Red Hat Advanced Cluster Management, Red Hat Advanced
Cluster Management enables the same set of add-ons to manage the
multicluster engine operator.

Install those add-ons in a different multicluster engine operator
namespace so that the multicluster engine operator can self-manage with
the `local-cluster` add-ons while Red Hat Advanced Cluster Management
manages multicluster engine operator at the same time. Complete the
following procedure:

1.  Log in to your Red Hat Advanced Cluster Management with the CLI.

2.  Create the `AddOnDeploymentConfig` resource to specify a different
    add-on installation namespace. See the following example where
    `agentInstallNamespace` references
    `open-cluster-management-agent-addon-discovery`:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: AddOnDeploymentConfig
    metadata:
      name: addon-ns-config
      namespace: multicluster-engine
    spec:
      agentInstallNamespace: open-cluster-management-agent-addon-discovery
    ```

3.  Run `oc apply -f <filename>.yaml` to apply the file.

4.  Update the existing `ClusterManagementAddOn` resources for the
    add-ons so that the add-ons are installed in the
    `open-cluster-management-agent-addon-discovery` namespace that is
    specified in the `AddOnDeploymentConfig` resource that you created.
    See the following example with `open-cluster-management-global-set`
    as the namespace:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: ClusterManagementAddOn
    metadata:
      name: work-manager
    spec:
      addonMeta:
        displayName: work-manager
      installStrategy:
        placements:
        - name: global
          namespace: open-cluster-management-global-set
          rolloutStrategy:
            type: All
        type: Placements
    ```

    1.  Add the `addonDeploymentConfigs` to the
        `ClusterManagementAddOn`. See the following example:

        ``` yaml
        apiVersion: addon.open-cluster-management.io/v1alpha1
        kind: ClusterManagementAddOn
        metadata:
          name: work-manager
        spec:
          addonMeta:
            displayName: work-manager
          installStrategy:
            placements:
            - name: global
              namespace: open-cluster-management-global-set
              rolloutStrategy:
                type: All
              configs:
              - group: addon.open-cluster-management.io
                name: addon-ns-config
                namespace: multicluster-engine
                resource: addondeploymentconfigs
            type: Placements
        ```

    2.  Add the `AddOnDeploymentConfig` to the `managed-serviceaccount`.
        See the following example:

        ``` yaml
        apiVersion: addon.open-cluster-management.io/v1alpha1
        kind: ClusterManagementAddOn
        metadata:
          name: managed-serviceaccount
        spec:
          addonMeta:
            displayName: managed-serviceaccount
          installStrategy:
            placements:
            - name: global
              namespace: open-cluster-management-global-set
              rolloutStrategy:
                type: All
              configs:
              - group: addon.open-cluster-management.io
                name: addon-ns-config
                namespace: multicluster-engine
                resource: addondeploymentconfigs
            type: Placements
        ```

    3.  Add the `addondeploymentconfigs` value to the
        `ClusterManagementAddOn` resource named, `cluster-proxy`. See
        the following example:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: ClusterManagementAddOn
    metadata:
      name: cluster-proxy
    spec:
      addonMeta:
        displayName: cluster-proxy
      installStrategy:
        placements:
        - name: global
          namespace: open-cluster-management-global-set
          rolloutStrategy:
            type: All
          configs:
          - group: addon.open-cluster-management.io
            name: addon-ns-config
            namespace: multicluster-engine
            resource: addondeploymentconfigs
        type: Placements
    ```

5.  Run the following command to verify that the add-ons for the Red Hat
    Advanced Cluster Management `local-cluster` are re-installed into
    the namespace that you specified:

    ``` bash
    oc get deployment -n open-cluster-management-agent-addon-discovery
    ```

    See the following output example:

    ``` bash
    NAME                                 READY   UP-TO-DATE   AVAILABLE    AGE
    cluster-proxy-proxy-agent            1/1     1            1           24h
    klusterlet-addon-workmgr             1/1     1            1           24h
    managed-serviceaccount-addon-agent   1/1     1            1           24h
    ```

Create a *KlusterletConfig* resource. multicluster engine operator has a
local-cluster, which is a hub cluster that is managed. A resource named
`klusterlet` is created for this local-cluster.

When your multicluster engine operator is imported into Red Hat Advanced
Cluster Management, Red Hat Advanced Cluster Management installs the
klusterlet with the same name, `klusterlet`, to manage the multicluster
engine operator. This conflicts with the multicluster engine operator
local-cluster klusterlet.

You need to create a `KlusterletConfig` resource that is used by
`ManagedCluster` resources to import multicluster engine operator
clusters so that the klusterlet is installed with a different name to
avoid the conflict. Complete the following procedure:

1.  Create a `KlusterletConfig` resource using the following example.
    When this `KlusterletConfig` resource is referenced in a managed
    cluster, the value in the `spec.installMode.noOperator.postfix`
    field is used as a suffix to the klusterlet name, such as
    `klusterlet-mce-import`:

    ``` yaml
    kind: KlusterletConfig
    apiVersion: config.open-cluster-management.io/v1alpha1
    metadata:
      name: mce-import-klusterlet-config
    spec:
      installMode:
        type: noOperator
        noOperator:
           postfix: mce-import
    ```

2.  Run `oc apply -f <filename>.yaml` to apply the file.

Configure for backup and restore.

Since you installed Red Hat Advanced Cluster Management, you can also
use the *Backup and restore* feature.

If the hub cluster is restored in a disaster recovery scenario, the
imported multicluster engine operator clusters and hosted clusters are
imported to the newer Red Hat Advanced Cluster Management hub cluster.

In this scenario, you need to restore the previous configurations as
part of Red Hat Advanced Cluster Management hub cluster restore.

Add the `backup=true` label to enable backup. See the following steps
for each add-on:

- For your `addon-ns-config`, run the following command:

  ``` bash
  oc label addondeploymentconfig addon-ns-config -n multicluster-engine cluster.open-cluster-management.io/backup=true
  ```

- For your `hypershift-addon-deploy-config`, run the following command:

  ``` bash
  oc label addondeploymentconfig hypershift-addon-deploy-config -n multicluster-engine cluster.open-cluster-management.io/backup=true
  ```

- For your `work-manager`, run the following command:

  ``` bash
  oc label clustermanagementaddon work-manager cluster.open-cluster-management.io/backup=true
  ```

- For your \`cluster-proxy \`, run the following command:

  ``` bash
  oc label clustermanagementaddon cluster-proxy cluster.open-cluster-management.io/backup=true
  ```

- For your `managed-serviceaccount`, run the following command:

  ``` bash
  oc label clustermanagementaddon managed-serviceaccount cluster.open-cluster-management.io/backup=true
  ```

- For your `mce-import-klusterlet-config`, run the following command:

  ``` bash
  oc label KlusterletConfig mce-import-klusterlet-config cluster.open-cluster-management.io/backup=true
  ```

### Importing multicluster engine operator manually

To manually import an multicluster engine operator cluster from your Red
Hat Advanced Cluster Management cluster, complete the following
procedure:

1.  From your Red Hat Advanced Cluster Management cluster, create a
    `ManagedCluster` resource manually to import an multicluster engine
    operator cluster. See the following file example:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1
    kind: ManagedCluster
    metadata:
      annotations:
        agent.open-cluster-management.io/klusterlet-config: mce-import-klusterlet-config 
      labels:
        cloud: auto-detect
        vendor: auto-detect
      name: mce-a 
    spec:
      hubAcceptsClient: true
      leaseDurationSeconds: 60
    ```

    - The `mce-import-klusterlet-config` annotation references the
      `KlusterletConfig` resource that you created in the previous step
      to install the Red Hat Advanced Cluster Management klusterlet with
      a different name in multicluster engine operator.

    - The example imports an multicluster engine operator managed
      cluster named `mce-a`.

2.  Run `oc apply -f <filename>.yaml` to apply the file.

3.  Create the `auto-import-secret` secret that references the
    `kubeconfig` of the multicluster engine operator cluster. Go to
    *Importing a cluster by using the auto import secret* in Importing a
    managed cluster by using the CLI to add the auto import secret to
    complete the multicluster engine operator auto-import process.

    After you create the auto import secret in the multicluster engine
    operator managed cluster namespace in the Red Hat Advanced Cluster
    Management cluster, the managed cluster is registered.

4.  Run the following command to get the status:

    ``` bash
    oc get managedcluster
    ```

    See following example output with the status and example URLs of
    managed clusters:

    ``` bash
    NAME           HUB ACCEPTED   MANAGED CLUSTER URLS            JOINED   AVAILABLE   AGE
    local-cluster  true           https://<api.acm-hub.com:port>  True     True        44h
    mce-a          true           https://<api.mce-a.com:port>    True     True        27s
    ```

**Important:** Do not enable any other Red Hat Advanced Cluster
Management add-ons for the imported multicluster engine operator.

### Discovering hosted clusters

After all your multicluster engine operator clusters are imported into
Red Hat Advanced Cluster Management, you need to enable the
`hypershift-addon` for those managed multicluster engine operator
clusters to discover the hosted clusters.

Default add-ons are installed into a different namespace in the previous
procedures. Similarly, you install the `hypershift-addon` into a
different namespace in multicluster engine operator so that the add-ons
agent for multicluster engine operator local-cluster and the agent for
Red Hat Advanced Cluster Management can work in multicluster engine
operator.

**Important:** For all the following commands, replace
`<managed-cluster-names>` with comma-separated managed cluster names for
multicluster engine operator.

1.  Run the following command to set the `agentInstallNamespace`
    namespace of the add-on to
    `open-cluster-management-agent-addon-discovery`:

    ``` bash
    oc patch addondeploymentconfig hypershift-addon-deploy-config -n multicluster-engine --type=merge -p '{"spec":{"agentInstallNamespace":"open-cluster-management-agent-addon-discovery"}}'
    ```

2.  Run the following command to disable metrics and to disable the
    HyperShift operator management:

    ``` bash
    oc patch addondeploymentconfig hypershift-addon-deploy-config -n multicluster-engine --type=merge -p '{"spec":{"customizedVariables":[{"name":"disableMetrics","value": "true"},{"name":"disableHOManagement","value": "true"}]}}'
    ```

3.  **Optional:** Configure your naming convention. By default, imported
    hosted clusters use the `<mce-cluster-name>-<hosted-cluster-name>`
    naming pattern, but you can customize your naming pattern.

    1.  Remove the default prefix by running the following command:

        ``` bash
        oc patch addondeploymentconfig hypershift-addon-deploy-config \
          -n multicluster-engine \
          --type=merge \
          -p '{"spec":{"customizedVariables":[{"name":"disableMetrics","value":"true"},{"name":"disableHOManagement","value":"true"},{"name":"discoveryPrefix","value":"custom-prefix"}]}}'
        ```

    2.  Change `custom-prefix` to your new prefix. The hosted cluster
        names are created with the
        `<custom-prefix>-<hosted-cluster-name>` pattern. Run the
        following command:

        ``` bash
        oc patch addondeploymentconfig hypershift-addon-deploy-config \
          -n multicluster-engine \
          --type=merge \
          -p '{"spec":{"customizedVariables":[{"name":"disableMetrics","value":"true"},{"name":"disableHOManagement","value":"true"},{"name":"discoveryPrefix","value":"custom-prefix"}]}}'
        ```

    3.  If you need to remove the discovery prefix entirely, first
        ensure all hosted clusters are detached from the respective
        clusters. **Important:** Using an empty string as the custom
        prefix can cause klusterlet naming collisions within the
        multicluster engine operator cluster. Run the following command:

    ``` bash
    oc patch addondeploymentconfig hypershift-addon-deploy-config \
       -n multicluster-engine \
       --type=json \
       -p='[{"op":"add","path":"/spec/customizedVariables/-","value":{"name":"autoImportDisabled","value":"true"}}]'
    ```

4.  Run the following command to enable the `hypershift-addon` for
    multicluster engine operator:

    ``` bash
    clusteradm addon enable --names hypershift-addon --clusters <managed-cluster-names>
    ```

5.  You can get the multicluster engine operator managed cluster names
    by running the following command in Red Hat Advanced Cluster
    Management.

    ``` bash
    oc get managedcluster
    ```

6.  Log into multicluster engine operator clusters and verify that the
    `hypershift-addon` is installed in the namespace that you specified.
    Run the following command:

    ``` bash
    oc get deployment -n open-cluster-management-agent-addon-discovery
    ```

    See the following example output that lists the add-ons:

    ``` bash
    NAME                                READY   UP-TO-DATE   AVAILABLE   AGE
    cluster-proxy-proxy-agent           1/1     1            1           24h
    klusterlet-addon-workmgr            1/1     1            1           24h
    hypershift-addon-agent              1/1     1            1           24h
    managed-serviceaccount-addon-agent  1/1     1            1           24h
    ```

Red Hat Advanced Cluster Management deploys the `hypershift-addon`,
which is the discovery agent that discovers hosted clusters from
multicluster engine operator. The agent creates the corresponding
`DiscoveredCluster` custom resource in the multicluster engine operator
managed cluster namespace in the Red Hat Advanced Cluster Management hub
cluster when the hosted cluster `kube-apiserver` becomes available.

You can view your discovered clusters in the console.

1.  Log in to hub cluster console and click **Fleet Management** \>
    **Infrastructure** \> **Clusters**.

    **Note:** For OpenShift Container Platform versions earlier than
    version 4.20, select **All Clusters** from the cluster switcher.

2.  Find the *Discovered clusters* tab to view all discovered hosted
    clusters from multicluster engine operator with type
    `MultiClusterEngineHCP`.

Next, visit Automating import for discovered hosted clusters to learn
how to automatically import clusters.

## Automating import for discovered hosted clusters

Automate the import of hosted clusters by using the `DiscoveredCluster`
resource for faster cluster management, without manually importing
individual clusters.

When you automatically import a discovered hosted cluster into Red Hat
Advanced Cluster Management, all Red Hat Advanced Cluster Management
add-ons are enabled so that you can start managing the hosted clusters
with the available management tools.

The hosted cluster is also *auto-imported* into multicluster engine
operator. Through the multicluster engine operator console, you can
manage the hosted cluster lifecycle. However, you cannot manage the
hosted cluster lifecycle from the Red Hat Advanced Cluster Management
console.

**Required access:** Cluster administrator

### Configuring settings for automatic import

Discovered hosted clusters from managed multicluster engine operator
clusters are represented in `DiscoveredCluster` custom resources, which
are located in the managed multicluster engine operator cluster
namespace in Red Hat Advanced Cluster Management. See the following
`DiscoveredCluster` resource and namespace example:

``` yaml
apiVersion: discovery.open-cluster-management.io/v1
kind: DiscoveredCluster
metadata:
  creationTimestamp: "2024-05-30T23:05:39Z"
  generation: 1
  labels:
    hypershift.open-cluster-management.io/hc-name: hosted-cluster-1
    hypershift.open-cluster-management.io/hc-namespace: clusters
  name: hosted-cluster-1
  namespace: mce-1
  resourceVersion: "1740725"
  uid: b4c36dca-a0c4-49f9-9673-f561e601d837
spec:
  apiUrl: https://a43e6fe6dcef244f8b72c30426fb6ae3-ea3fec7b113c88da.elb.us-west-1.amazonaws.com:6443
  cloudProvider: aws
  creationTimestamp: "2024-05-30T23:02:45Z"
  credential: {}
  displayName: mce-1-hosted-cluster-1
  importAsManagedCluster: false
  isManagedCluster: false
  name: hosted-cluster-1
  openshiftVersion: 0.0.0
  status: Active
  type: MultiClusterEngineHCP
```

Discovered hosted clusters are not automatically imported into Red Hat
Advanced Cluster Management until the `spec.importAsManagedCluster`
field is changed from `false` to `true`. Learn how to use a Red Hat
Advanced Cluster Management policy to automatically set this field to
`true` for all `type.MultiClusterEngineHCP` within `DiscoveredCluster`
resources so that discovered hosted clusters are immediately and
automatically imported into Red Hat Advanced Cluster Management.

Configure your Policy to import all your discovered hosted clusters.

1.  Log in to your hub cluster from the CLI to complete the following
    procedure:

2.  Create a YAML file for your `DiscoveredCluster` custom resource and
    edit the configuration that is referenced in the following example:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: Policy
    metadata:
      name: policy-mce-hcp-autoimport
      namespace: open-cluster-management-global-set
      annotations:
        policy.open-cluster-management.io/standards: NIST SP 800-53
        policy.open-cluster-management.io/categories: CM Configuration Management
        policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
        policy.open-cluster-management.io/description: Discovered clusters that are of
          type MultiClusterEngineHCP can be automatically imported into ACM as managed clusters.
          This policy configure those discovered clusters so they are automatically imported.
          Fine tuning MultiClusterEngineHCP clusters to be automatically imported
          can be done by configure filters at the configMap or add annotation to the discoverd cluster.
    spec:
      disabled: false
      policy-templates:
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: mce-hcp-autoimport-config
            spec:
              object-templates:
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: v1
                    kind: ConfigMap
                    metadata:
                      name: discovery-config
                      namespace: open-cluster-management-global-set
                    data:
                      rosa-filter: ""
              remediationAction: enforce 
              severity: low
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: policy-mce-hcp-autoimport
            spec:
              remediationAction: enforce
              severity: low
              object-templates-raw: |
                {{- /* find the MultiClusterEngineHCP DiscoveredClusters */ -}}
                {{- range $dc := (lookup "discovery.open-cluster-management.io/v1" "DiscoveredCluster" "" "").items }}
                  {{- /* Check for the flag that indicates the import should be skipped */ -}}
                  {{- $skip := "false" -}}
                  {{- range $key, $value := $dc.metadata.annotations }}
                    {{- if and (eq $key "discovery.open-cluster-management.io/previously-auto-imported")
                               (eq $value "true") }}
                      {{- $skip = "true" }}
                    {{- end }}
                  {{- end }}
                  {{- /* if the type is MultiClusterEngineHCP and the status is Active */ -}}
                  {{- if and (eq $dc.spec.status "Active")
                             (contains (fromConfigMap "open-cluster-management-global-set" "discovery-config" "mce-hcp-filter") $dc.spec.displayName)
                             (eq $dc.spec.type "MultiClusterEngineHCP")
                             (eq $skip "false") }}
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: discovery.open-cluster-management.io/v1
                    kind: DiscoveredCluster
                    metadata:
                      name: {{ $dc.metadata.name }}
                      namespace: {{ $dc.metadata.namespace }}
                    spec:
                      importAsManagedCluster: true 
                  {{- end }}
                {{- end }}
    ```

    - To enable automatic import, change the `spec.remediationAction` to
      `enforce`.

    - To enable automatic import, change `spec.importAsManagedCluster`
      to `true`.

3.  Run `oc apply -f <filename>.yaml -n <namespace>` to apply the file.

### Creating the placement definition

You need to create a placement definition that specifies the managed
cluster for the policy deployment. Complete the following procedure:

1.  Create the `Placement` definition that selects only the
    `local-cluster`, which is a hub cluster that is managed. Use the
    following YAML sample:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: Placement
    metadata:
      name: policy-mce-hcp-autoimport-placement
      namespace: open-cluster-management-global-set
    spec:
      tolerations:
        - key: cluster.open-cluster-management.io/unreachable
          operator: Exists
        - key: cluster.open-cluster-management.io/unavailable
          operator: Exists
      clusterSets:
        - global
      predicates:
        - requiredClusterSelector:
            labelSelector:
              matchExpressions:
                - key: local-cluster
                  operator: In
                  values:
                    - "true"
    ```

2.  Run `oc apply -f placement.yaml -n <namespace>`, where `namespace`
    matches the namespace that you used for the policy that you
    previously created.

### Binding the import policy to a placement definition

After you create the policy and the placement, you need to connect the
two resources. Complete the following steps:

1.  Connect the resources by using a `PlacementBinding` resource. See
    the following example where `placementRef` references the
    `Placement` that you created, and `subjects` references the `Policy`
    that you created:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: PlacementBinding
    metadata:
      name: policy-mce-hcp-autoimport-placement-binding
      namespace: open-cluster-management-global-set
    placementRef:
      name: policy-mce-hcp-autoimport-placement
      apiGroup: cluster.open-cluster-management.io
      kind: Placement
    subjects:
      - name: policy-mce-hcp-autoimport
        apiGroup: policy.open-cluster-management.io
        kind: Policy
    ```

2.  To verify, run the following command:

    ``` bash
    oc get policies.policy.open-cluster-management.io policy-mce-hcp-autoimport -n <namespace>
    ```

**Important:** You can *detach* a hosted cluster from Red Hat Advanced
Cluster Management by using the **Detach** option in the Red Hat
Advanced Cluster Management console, or by removing the corresponding
`ManagedCluster` custom resource from the command line.

For best results, detach the managed hosted cluster before *destroying*
the hosted cluster.

When a discovered cluster is detached, the following annotation is added
to the `DiscoveredCluster` resource to prevent the policy to import the
discovered cluster again.

``` bash
  annotations:
    discovery.open-cluster-management.io/previously-auto-imported: "true"
```

If you want the detached discovered cluster to be reimported, remove
this annotation.

## Automating import for discovered Red Hat OpenShift Service on AWS clusters

Automate the import of Red Hat OpenShift Service on AWS clusters by
using Red Hat Advanced Cluster Management policy enforcement for faster
cluster management, without manually importing individual clusters.

**Required access:** Cluster administrator

### Creating the automatic import policy

The following policy and procedure is an example of how to import all
your discovered Red Hat OpenShift Service on AWS clusters automatically.

Log in to your hub cluster from the CLI to complete the following
procedure:

1.  Create a YAML file with the following example and apply the changes
    that are referenced:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: Policy
    metadata:
      name: policy-rosa-autoimport
      annotations:
        policy.open-cluster-management.io/standards: NIST SP 800-53
        policy.open-cluster-management.io/categories: CM Configuration Management
        policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
        policy.open-cluster-management.io/description: OpenShift Service on AWS discovered clusters can be automatically imported into
    Red Hat Advanced Cluster Management as managed clusters with this policy. You can select and configure those managed clusters so you can import. Configure filters or add an annotation if you do not want all of your OpenShift Service on AWS clusters to be automatically imported.
    spec:
      remediationAction: inform 
      disabled: false
      policy-templates:
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: rosa-autoimport-config
            spec:
              object-templates:
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: v1
                    kind: ConfigMap
                    metadata:
                      name: discovery-config
                      namespace: open-cluster-management-global-set
                    data:
                      rosa-filter: "" 
              remediationAction: enforce
              severity: low
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: policy-rosa-autoimport
            spec:
              remediationAction: enforce
              severity: low
              object-templates-raw: |
                {{- /* find the ROSA DiscoveredClusters */ -}}
                {{- range $dc := (lookup "discovery.open-cluster-management.io/v1" "DiscoveredCluster" "" "").items }}
                  {{- /* Check for the flag that indicates the import should be skipped */ -}}
                  {{- $skip := "false" -}}
                  {{- range $key, $value := $dc.metadata.annotations }}
                    {{- if and (eq $key "discovery.open-cluster-management.io/previously-auto-imported")
                               (eq $value "true") }}
                      {{- $skip = "true" }}
                    {{- end }}
                  {{- end }}
                  {{- /* if the type is ROSA and the status is Active */ -}}
                  {{- if and (eq $dc.spec.status "Active")
                             (contains (fromConfigMap "open-cluster-management-global-set" "discovery-config" "rosa-filter") $dc.spec.displayName)
                             (eq $dc.spec.type "ROSA")
                             (eq $skip "false") }}
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: discovery.open-cluster-management.io/v1
                    kind: DiscoveredCluster
                    metadata:
                      name: {{ $dc.metadata.name }}
                      namespace: {{ $dc.metadata.namespace }}
                    spec:
                      importAsManagedCluster: true
                  {{- end }}
                {{- end }}
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: policy-rosa-managedcluster-status
            spec:
              remediationAction: enforce
              severity: low
              object-templates-raw: |
                {{- /* Use the same DiscoveredCluster list to check ManagedCluster status */ -}}
                {{- range $dc := (lookup "discovery.open-cluster-management.io/v1" "DiscoveredCluster" "" "").items }}
                  {{- /* Check for the flag that indicates the import should be skipped */ -}}
                  {{- $skip := "false" -}}
                  {{- range $key, $value := $dc.metadata.annotations }}
                    {{- if and (eq $key "discovery.open-cluster-management.io/previously-auto-imported")
                               (eq $value "true") }}
                      {{- $skip = "true" }}
                    {{- end }}
                  {{- end }}
                  {{- /* if the type is ROSA and the status is Active */ -}}
                  {{- if and (eq $dc.spec.status "Active")
                             (contains (fromConfigMap "open-cluster-management-global-set" "discovery-config" "rosa-filter") $dc.spec.displayName)
                             (eq $dc.spec.type "ROSA")
                             (eq $skip "false") }}
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: cluster.open-cluster-management.io/v1
                    kind: ManagedCluster
                    metadata:
                      name: {{ $dc.spec.displayName }}
                      namespace: {{ $dc.spec.displayName }}
                    status:
                      conditions:
                        - type: ManagedClusterConditionAvailable
                          status: "True"
                  {{- end }}
                {{- end }}
    ```

    - To enable automatic import, change the `spec.remediationAction` to
      `enforce`.

    - Optional: Specify a value here to select a subset of the matching
      Red Hat OpenShift Service on AWS clusters, which are based on
      *discovered* cluster names. The `rosa-filter` has no value by
      default, so the filter does not restrict cluster names without a
      subset value.

2.  Run `oc apply -f <filename>.yaml -n <namespace>` to apply the file.

### Creating the placement definition

You need to create a placement definition that specifies the managed
cluster for the policy deployment.

1.  Create the placement definition that selects only the
    `local-cluster`, which is a hub cluster that is managed. Use the
    following YAML sample:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: Placement
    metadata:
      name: placement-openshift-plus-hub
    spec:
      predicates:
      - requiredClusterSelector:
          labelSelector:
            matchExpressions:
            - key: name
                operator: In
                values:
                - local-cluster
    ```

2.  Run `oc apply -f placement.yaml -n <namespace>`, where `namespace`
    matches the namespace that you used for the policy that you
    previously created.

### Binding the import policy to a placement definition

After you create the policy and the placement, you need to connect the
two resources.

1.  Connect the resources by using a `PlacementBinding`. See the
    following example where `placementRef` references the `Placement`
    that you created, and `subjects` references the `Policy` that you
    created:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: PlacementBinding
    metadata:
      name: binding-policy-rosa-autoimport
    placementRef:
      apiGroup: cluster.open-cluster-management.io
      kind: Placement
      name: placement-policy-rosa-autoimport
    subjects:
    - apiGroup: policy.open-cluster-management.io
      kind: Policy
      name: policy-rosa-autoimport
    ```

2.  To verify, run the following command:

        oc get policies.policy.open-cluster-management.io policy-rosa-autoimport -n <namespace>

# Observability integration

With the Red Hat Advanced Cluster Management Observability feature, you
can view health and utilization of clusters across your fleet. You can
install Red Hat Advanced Cluster Management and enable Observability.

## Observing hosted control planes

To enable, see Observability service.

# SiteConfig

The SiteConfig operator offers a template-driven cluster provisioning
solution with a unified `ClusterInstance` API, which comes from the
`SiteConfig` API of the `SiteConfig` generator kustomize plugin.

For advanced topics, see SiteConfig advanced topics.

## About the SiteConfig operator

The SiteConfig operator offers a template-driven cluster provisioning
solution, which allows you to provision clusters with various
installation methods.

The SiteConfig operator introduces the unified `ClusterInstance` API,
which comes from the `SiteConfig` API of the `SiteConfig` generator
kustomize plugin.

The `ClusterInstance` API decouples parameters that define a cluster
from the manner in which the cluster is deployed.

This separation removes certain limitations that are presented by the
`SiteConfig` kustomize plugin in the current GitOps Zero Touch
Provisioning (ZTP) flow, such as agent cluster installations and
scalability constraints that are related to Argo CD.

Using the unified `ClusterInstance` API, the SiteConfig operator offers
the following improvements:

Isolation  
Separates the cluster definition from the installation method. The
`ClusterInstance` custom resource captures the cluster definition, while
installation templates capture the cluster architecture and installation
methods.

Unification  
The SiteConfig operator unifies both Git and non-Git workflows. You can
apply the `ClusterInstance` custom resource directly on the hub cluster,
or synchronize resources through a GitOps solution, such as ArgoCD.

Consistency  
Maintains a consistent API across installation methods, whether you are
using the Assisted Installer, the Image Based Install Operator, or any
other custom template-based approach.

Scalability  
Achieves greater scalability for each cluster than the `SiteConfig`
kustomize plugin.

Flexibility  
Provides you with more power to deploy and install clusters by using
custom templates.

Troubleshooting  
Offers insightful information regarding cluster deployment status and
rendered manifests, significantly enhancing the troubleshooting
experience.

For more information about the Image Based Install Operator, see Image
Based Install Operator.

For more information about the Assisted Installer, see Installing an
on-premise cluster using the Assisted Installer

### The SiteConfig operator flow

The SiteConfig operator dynamically generates installation manifests
based on user-defined templates that are instantiated from the data in
the `ClusterInstance` custom resource.

You can source the `ClusterInstance` custom resource from your Git
repository through Argo CD, or you can create it directly on the hub
cluster manually or through external tools and workflows.

The following is a high-level overview of the process:

1.  You create one or more sets of installation templates on the hub
    cluster.

2.  You create a `ClusterInstance` custom resource that references those
    installation templates and supporting manifests.

3.  After the resources are created, the SiteConfig operator reconciles
    the `ClusterInstance` custom resource by populating the templated
    fields that are referenced in the custom resource.

4.  The SiteConfig operator validates and renders the installation
    manifests, then the Operator performs a dry run.

5.  If the dry run is successful, the manifests are created, then the
    underlying Operators consume and process the manifests.

6.  The installation begins.

7.  The SiteConfig operator continuously monitors for changes in the
    associated `ClusterDeployment` resource and updates the `status`
    field of the `ClusterInstance` custom resource accordingly.

## Installation templates overview

Installation templates are data-driven templates that are used to
generate the set of installation artifacts. These templates follow the
Golang `text/template` format, and are instantiated by using data from
the `ClusterInstance` custom resource. This enables dynamic creation of
installation manifests for each target cluster that has similar
configurations, but with different values.

You can also create multiple sets based on the different installation
methods or cluster topologies. The SiteConfig operator supports the
following types of installation templates:

Cluster-level  
Templates that must reference only cluster-specific fields.

Node-level  
Templates that can reference both cluster-specific and node-specific
fields.

### Template functions

You can customize the templated fields. The SiteConfig operator supports
all Sprig library functions.

Additionally, the `ClusterInstance` API provides the following function
that you can use while creating your custom manifests:

`toYaml`  
The `toYaml` function encodes an item into a YAML string. If the item
cannot be converted to YAML, the function returns an empty string.

See the following example of the `.toYaml` specification in the
`ClusterInstance.Spec.Proxy` field:

``` yaml
{{ if .Spec.Proxy }}
  proxy:
{{ .Spec.Proxy | toYaml | indent 4 }}
{{ end }}
```

### Default set of templates

The SiteConfig operator provides the following default, validated, and
immutable set of templates in the same namespace in which the operator
is installed:

- Installation method: Assisted Installer - Template type: Cluster-level
  templates - File name: ai-cluster-templates-v1.yaml - Template
  content: AgentClusterInstall ClusterDeployment InfraEnv
  KlusterletAddonConfig ManagedCluster

- Installation method: Node-level templates - Template type:
  ai-node-templates-v1.yaml - File name: BareMetalHost NMStateConfig

- Installation method: Image-based Install Operator - Template type:
  Cluster-level templates - File name: ibi-cluster-templates-v1.yaml -
  Template content: ClusterDeployment KlusterletAddonConfig
  ManagedCluster

- Installation method: Node-level templates - Template type:
  ibi-node-templates-v1.yaml - File name: BareMetalHost
  ImageClusterInstall NetworkSecret

For more information about the `ClusterInstance` API, see
ClusterInstance API.

### Special template variables

The SiteConfig operator provides a set of special template variables
that you can use in your templates. See the following list:

`CurrentNode`  
The SiteConfig operator explicitly controls the iteration of the node
objects and exposes this variable to access all the content for the
current node being handled in templating.

`InstallConfigOverrides`  
Contains the merged `networkType`, `cpuPartitioningMode` and
`installConfigOverrides` content.

`ControlPlaneAgents`  
Consists of the number of control plane agents and it is automatically
derived from the `ClusterInstance` node objects.

`WorkerAgents`  
Consists of the number of worker agents and it is automatically derived
from the `ClusterInstance` node objects.

Capitalize the field name in the text template to create a custom
templated field.

For example, the `ClusterInstance` `spec` field is referenced with the
`.Spec` prefix. However, you must reference special variable fields with
the `.SpecialVars` prefix.

**Important:** Instead of using the `.Spec.Nodes` prefix for the
`spec.nodes` field, you must reference it with the
`.SpecialVars.CurrentNode` special template variable.

For example, if you want to specify the `name` and `namespace` for your
current node by using the `CurrentNode` special template variable, use
the field names in the following form:

``` yaml
name: "{{ .SpecialVars.CurrentNode.HostName }}"
namespace: "{{ .Spec.ClusterName }}"
```

### Customization of the manifests order

You can control the order in which manifests are created, updated, and
deleted by using the `siteconfig.open-cluster-management.io/sync-wave`
annotation. The annotation takes an integer as a value, and that integer
constitutes as a *wave*.

You can add one or several manifests to a single wave. If you do not
specify a value, the annotation takes the default value of `0`.

The SiteConfig operator reconciles the manifests in ascending order when
creating or updating resources and it deletes resources in descending
order.

In the following example, if the SiteConfig operator creates or updates
the manifests, the `AgentClusterInstall` and `ClusterDeployment` custom
resources are reconciled in the first wave, while
`KlusterletAddonConfig` and `ManagedCluster` custom resources are
reconciled in the third wave:

``` yaml
apiVersion: v1
data:
  AgentClusterInstall: |-
    ...
        siteconfig.open-cluster-management.io/sync-wave: "1"
    ...
  ClusterDeployment: |-
    ...
        siteconfig.open-cluster-management.io/sync-wave: "1"
    ...
  InfraEnv: |-
    ...
        siteconfig.open-cluster-management.io/sync-wave: "2"
    ...
  KlusterletAddonConfig: |-
    ...
        siteconfig.open-cluster-management.io/sync-wave: "3"
    ...
  ManagedCluster: |-
    ...
        siteconfig.open-cluster-management.io/sync-wave: "3"
    ...
kind: ConfigMap
metadata:
  name: assisted-installer-templates
  namespace: example-namespace
```

If the SiteConfig operator deletes the resources,
`KlusterletAddonConfig` and `ManagedCluster` custom resources are the
first to be deleted, while the `AgentClusterInstall` and
`ClusterDeployment` custom resources are the last.

### Configuration of additional annotations and labels

You can configure additional annotations and labels to both
cluster-level and node-level installation manifests by using the
`extraAnnotations` and `extraLabels` fields in the `ClusterInstance`
API. The SiteConfig operator applies your additional annotations and
labels to the manifests that you specify in the `ClusterInstance`
resource.

When creating your additional annotations and labels, you must specify a
manifest type to allow the SiteConfig operator to apply them to all the
matching manifests. However, the annotations and labels are arbitrary
and you can set any key and value pairs that are meaningful to your
applications.

**Note:** The additional annotations and labels are only applied to the
resources that were rendered through the referenced templates.

View the following example application of `extraAnnotations` and
`extraLabels`:

``` yaml
apiVersion: siteconfig.open-cluster-management.io/v1alpha1
kind: ClusterInstance
metadata:
  name: "example-sno"
  namespace: "example-sno"
spec:
  [...]
  clusterName: "example-sno"
  extraAnnotations: 
    ClusterDeployment:
      myClusterAnnotation: success
  extraLabels: 
    ManagedCluster:
      common: "true"
      group-du: ""
  nodes:
    - hostName: "example-sno.example.redhat.com"
      role: "master"
      extraAnnotations: 
        BareMetalHost:
          myNodeAnnotation: success
      extraLabels: 
        BareMetalHost:
          "testExtraLabel": "success"
```

- This field supports cluster-level annotations and labels that the
  SiteConfig operator applies to the the `ManagedCluster` and
  `ClusterDeployment` manifests.

- This field supports node-level annotations and labels that the
  SiteConfig operator applies to the `BareMetalHost` manifest.

- The `extraAnnotations` in this `BareMetalHost` example is
  `myNodeAnnotation`.

- The `extraLabels` in this `BareMetalHost` example is `testExtraLabel`.

You can verify that your additional labels are applied by running the
following command:

``` terminal
oc get managedclusters example-sno -ojsonpath='{.metadata.labels}' | jq
```

View the following example of applied labels:

``` json
{
  "common": "true",
  "group-du": "",
  ...
}
```

You can verify that your additional annotations are applied by running
the following command:

``` terminal
oc get bmh example-sno.example.redhat.com -n example-sno -ojsonpath='{.metadata.annotations}' | jq
```

View the following example of applied annotations:

``` json
{
  "myNodeAnnotation": "success",
  ...
}
```

### Permissible changes after provisioning

You might want to change your cluster configuration but making changes
to your cluster is not allowed during provisioning. However, after a
cluster is provisioned, you can modify the following fields:

- `spec.extraAnnotations`

- `spec.extraLabels`

- `spec.suppressedManifests`

- `spec.pruneManifests`

- `spec.clusterImageSetNameRef`

- `spec.nodes.<node-id>.extraAnnotations`

- `spec.nodes.<node-id>.extraLabels`

- `spec.nodes.<node-id>.suppressedManifests`

- `spec.nodes.<node-id>.pruneManifests`

**Note:** `<node-id>` represents the updated `NodeSpec` object.

## Enabling the SiteConfig operator

Enable the SiteConfig operator to use the default installation templates
and install single-node OpenShift clusters at scale.

**Required access:** Cluster administrator

### Prerequisites

- You need a Red Hat Advanced Cluster Management hub cluster.

### Enabling the SiteConfig operator from the `MultiClusterHub` resource

Patch the `MultiClusterHub` resource, then verify that SiteConfig
operator is enabled. Complete the following procedure:

1.  Set an environment variable that matches the namespace of the
    `MultiClusterHub` operator by running the following command:

    ``` terminal
    export MCH_NAMESPACE=<namespace>
    ```

2.  Set the `enabled` field to `true` in the `siteconfig` entry of
    `spec.overrides.components` in the `Multiclusterhub` resource by
    running the following command:

    ``` terminal
    oc patch multiclusterhubs.operator.open-cluster-management.io multiclusterhub -n ${MCH_NAMESPACE} --type json --patch '[{"op": "add", "path":"/spec/overrides/components/-", "value": {"name":"siteconfig","enabled": true}}]'
    ```

3.  Verify that the SiteConfig operator is enabled by running the
    following command on the hub cluster:

    ``` terminal
    oc -n ${MCH_NAMESPACE} get po | grep siteconfig
    ```

    See the following example output:

    ``` terminal
    siteconfig-controller-manager-6fdd86cc64-sdg87                    2/2     Running   0             43s
    ```

4.  **Optional:** Verify that you have the default installation
    templates by running the following command on the hub cluster:

    ``` terminal
    oc -n ${MCH_NAMESPACE} get cm
    ```

    See the following list of templates in the output example:

    ``` terminal
    NAME                                DATA   AGE
    ai-cluster-templates-v1             5      97s
    ai-node-templates-v1                2      97s
    ...
    ibi-cluster-templates-v1            3      97s
    ibi-node-templates-v1               3      97s
    ...
    ```

# Image Based Install Operator

Install the Image Based Install Operator so that you can complete and
manage image-based cluster installations by using the same APIs as
existing installation methods.

For more information about, and to learn how to enable the Image Based
Install Operator, see Image-based installations for single-node
OpenShift.

## Installing single-node OpenShift clusters with the SiteConfig operator

Install your clusters with the SiteConfig operator by using the default
installation templates. Use the installation templates for the
Image-Based Install Operator to complete the procedure.

**Required access:** Cluster administrator

### Prerequisites

- If you are using GitOps ZTP, configure your GitOps ZTP environment. To
  configure your environment, see Preparing the hub cluster for GitOps
  ZTP.

- You have the default installation templates. To get familiar with the
  default templates, see Default set of templates

- Install and configure the underlying operator of your choice.

Complete the following steps to install a cluster with the SiteConfig
operator:

1.  Creating the target namespace

2.  Creating the pull secret

3.  Creating the BMC secret

4.  Optional: Creating the extra manifests

5.  Rendering the installation manifests

### Creating the target namespace

You need a target namespace when you create the pull secret, the BMC
secret, extra manifest `ConfigMap` objects, and the `ClusterInstance`
custom resource.

Complete the following steps to create the target namespace:

1.  Create a YAML file for the target namespace. See the following
    example file that is named `clusterinstance-namespace.yaml`:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: example-sno
    ```

2.  Apply your file to create the resource. Run the following command on
    the hub cluster:

    ``` terminal
    oc apply -f clusterinstance-namespace.yaml
    ```

### Creating the pull secret

You need a pull secret to enable your clusters to pull images from
container registries. Complete the following steps to create a pull
secret:

1.  Create a YAML file to pull images. See the following example of a
    file that is named `pull-secret.yaml`:

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: pull-secret
      namespace: example-sno 
    data:
      .dockerconfigjson: <encoded_docker_configuration> 
    type: kubernetes.io/dockerconfigjson
    ```

    - Ensure that the `namespace` value matches the target namespace.

    - Specify the base64-encoded configuration file as the value.

2.  Apply the file to create the resource. Run the following command on
    the hub cluster:

    ``` terminal
    oc apply -f pull-secret.yaml
    ```

### Creating the BMC secret

You need a secret to connect to your baseboard management controller
(BMC). Complete the following steps to create a secret:

1.  Create a YAML file for the BMC secret. See the following sample file
    that is named `example-bmc-secret.yaml`:

    ``` yaml
    apiVersion: v1
    data:
      password: <password>
      username: <username>
    kind: Secret
    metadata:
      name: example-bmh-secret
      namespace: "example-sno" 
    type: Opaque
    ```

    - Ensure that the `namespace` value matches the target namespace.

2.  Apply the file to create the resource. Run the following command on
    the hub cluster:

    ``` terminal
    oc apply -f example-bmc-secret.yaml
    ```

### Optional: Creating the extra manifests

You can create extra manifests that you need to reference in the
`ClusterInstance` custom resource. Complete the following steps to
create an extra manifest:

1.  Create a YAML file for an extra manifest `ConfigMap` object, for
    example named `enable-crun.yaml`:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: enable-crun
      namespace: example-sno 
    data:
      enable-crun-master.yaml: |
        apiVersion: machineconfiguration.openshift.io/v1
        kind: ContainerRuntimeConfig
        metadata:
          name: enable-crun-master
        spec:
          machineConfigPoolSelector:
            matchLabels:
              pools.operator.machineconfiguration.openshift.io/master: ""
          containerRuntimeConfig:
            defaultRuntime: crun
      enable-crun-worker.yaml: |
        apiVersion: machineconfiguration.openshift.io/v1
        kind: ContainerRuntimeConfig
        metadata:
          name: enable-crun-worker
        spec:
          machineConfigPoolSelector:
            matchLabels:
              pools.operator.machineconfiguration.openshift.io/worker: ""
          containerRuntimeConfig:
            defaultRuntime: crun
    ```

    - Ensure that the `namespace` value matches the target namespace.

2.  Create the resource by running the following command on the hub
    cluster:

    ``` terminal
    oc apply -f enable-crun.yaml
    ```

### Rendering the installation manifests

Reference the templates and supporting manifests in the
`ClusterInstance` custom resource. Complete the following steps to
render the installation manifests by using the default cluster and node
templates:

1.  In the `example-sno` namespace, create the `ClusterInstance` custom
    resource that is named `clusterinstance-ibi.yaml` in the following
    example:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "example-clusterinstance"
      namespace: "example-sno" 
    spec:
      #clusterType: "SNO" 
      holdInstallation: false
      extraManifestsRefs: 
        - name: extra-machine-configs
        - name: enable-crun
      pullSecretRef:
        name: "pull-secret" 
      [...]
      clusterName: "example-sno" 
      [...]
      clusterImageSetNameRef: "img4.17-x86-64"
      [...]
      reference: 
      [...]
        namespace: 
        [...]
      templateRefs: 
        - name: ibi-cluster-templates-v1
          namespace: rhacm
          hostRef: 
            - name: example-bmh
              namespace: example-sno
      [...]
      nodes:
          [...]
          bmcCredentialsName: 
            name: "example-bmh-secret"
          [...]
          templateRefs: 
            - name: ibi-node-templates-v1
              namespace: rhacm
          [...]
    ```

    - Ensure that the `namespace` in the `ClusterInstance` custom
      resource matches the target namespace that you defined.

    - **Optional:** If you want to scale out or scale in your
      single-node OpenShift clusters, you must set the
      `spec.clusterType` field to `"SNO"`.

    - Reference the `name` of one or more extra manifests `ConfigMap`
      objects.

    - Reference the `name` of your pull secret.

    - Ensure that the value of the `clusterName` field in the
      `ClusterInstance` custom resource matches the value of the
      `namespace` field.

    - Specify dependencies or related objects in different namespaces.

    - Specify the namespace of the reference object.

    - Reference the `name` of the cluster-level templates in the
      `spec.templateRefs` field. If you are using a default installation
      template, the `namespace` must match the namespace where the
      Operator is installed.

    - Specify a reference to a `BareMetalHost` resource that is in a
      different namespace.

    - Reference the `name` of the BMC secret.

    - Reference the `name` of the node-level templates in the
      `spec.nodes.templateRefs` field. If you are using a default
      installation template, the `namespace` must match the namespace
      where the Operator is installed.

2.  Apply the file and create the resource by running the following
    command:

    ``` terminal
    oc apply -f clusterinstance-ibi.yaml
    ```

    After you create the custom resource, the SiteConfig operator starts
    reconciling the `ClusterInstance` custom resource, then validates
    and renders the installation manifests.

    The SiteConfig operator continues to monitor for changes in the
    `ClusterDeployment` custom resources to update the cluster
    installation progress of the corresponding `ClusterInstance` custom
    resource.

3.  Monitor the process by running the following command:

    ``` terminal
    oc get clusterinstance <cluster_name> -n <target_namespace> -o yaml
    ```

    See the following example output from the `status.conditions`
    section for successful manifest generation:

    ``` terminal
    message: Applied site config manifests
    reason: Completed
    status: "True"
    type: RenderedTemplatesApplied
    ```

4.  Check the manifests that SiteConfig operator rendered by running the
    following command:

    ``` terminal
    oc get clusterinstance <cluster_name> -n <target_namespace> -o jsonpath='{.status.manifestsRendered}'
    ```

For more information about status conditions, see ClusterInstance API.

## Deprovisioning single-node OpenShift clusters with the SiteConfig operator

Deprovision your clusters with the SiteConfig operator to delete all
resources and accesses associated with that cluster.

**Required access:** Cluster administrator

### Prerequisites

- Deploy your clusters with the SiteConfig operator by using the default
  installation templates.

### Deprovisioning single-node OpenShift clusters

Complete the following steps to delete your clusters:

1.  Delete the `ClusterInstance` custom resource by running the
    following command:

    ``` bash
    oc delete clusterinstance <cluster_name> -n <target_namespace>
    ```

2.  Verify that the deletion was successful by running the following
    command:

    ``` bash
    oc get clusterinstance <cluster_name> -n <target_namespace>
    ```

    See the following example output where the `(NotFound)` error
    indicates that your cluster is deprovisioned.

    ``` terminal
    Error from server (NotFound): clusterinstances.siteconfig.open-cluster-management.io "<cluster_name>" not found
    ```

## SiteConfig advanced topics

### Creating custom templates with the SiteConfig operator

Create user-defined templates that are not provided in the default set
of templates.

**Required access:** Cluster administrator

Complete the following steps to a create custom template:

1.  Create a YAML file named `my-custom-secret.yaml` that contains the
    cluster-level template in a `ConfigMap` object:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: my-custom-secret
      namespace: rhacm
    data:
      MySecret: |-
        apiVersion: v1
        kind: Secret
        metadata:
          name: "{{ .Spec.ClusterName }}-my-custom-secret-key"
          namespace: "clusters"
          annotations:
            siteconfig.open-cluster-management.io/sync-wave: "1" 
        type: Opaque
        data:
          key: <key>
    ```

    - The `siteconfig.open-cluster-management.io/sync-wave` annotation
      controls in which order manifests are created, updated, or
      deleted.

2.  Apply the custom template on the hub cluster by running the
    following command:

    ``` terminal
    oc apply -f my-custom-secret.yaml
    ```

3.  Reference your template in the `ClusterInstance` custom resource
    named `clusterinstance-my-custom-secret.yaml`:

    ``` yaml
    spec:
        ...
      templateRefs:
        - name: ai-cluster-templates-v1.yaml
          namespace: rhacm
        - name: my-custom-secret.yaml
          namespace: rhacm
        ...
    ```

4.  Apply the `ClusterInstance` custom resource by running the following
    command:

    ``` terminal
    oc apply -f clusterinstance-my-custom-secret.yaml
    ```

### Scaling in a single-node OpenShift cluster with the SiteConfig operator

Scale in your managed cluster that was installed by the SiteConfig
operator. You can scale in your cluster by removing a worker node.

**Required access:** Cluster administrator

#### Prerequisites

- If you are using GitOps ZTP, you have configured your GitOps ZTP
  environment. To configure your environment, see Preparing the hub
  cluster for GitOps ZTP.

- You have the default templates. To get familiar with the default
  templates, see Default set of templates

- You have installed your cluster with the SiteConfig operator. To
  install a cluster with the SiteConfig operator, see Installing
  single-node OpenShift clusters with the SiteConfig operator

- You have set the `spec.clusterType` to `"SNO"`.

#### Adding an annotation to your worker node

Add an annotation to your worker node for removal.

Complete the following steps to annotate worker node from the managed
cluster:

1.  Add an annotation in the `extraAnnotations` field of the worker node
    entry in the `ClusterInstance` custom resource that is used to
    provision your cluster:

    ``` yaml
    spec:
       ...
       nodes:
       - hostName: "worker-node2.example.com"
          role: "worker"
          ironicInspect: ""
          extraAnnotations:
            BareMetalHost:
              bmac.agent-install.openshift.io/remove-agent-and-node-on-delete: "true"
    ...
    ```

2.  Apply the changes. See the following options:

    1.  If you are using Red Hat Advanced Cluster Management without Red
        Hat OpenShift GitOps, run the following command on the hub
        cluster:

        ``` terminal
        oc apply -f <clusterinstance>.yaml
        ```

    2.  If you are using GitOps ZTP, push to your Git repository and
        wait for Argo CD to synchronize the changes.

3.  Verify that the annotation is applied to the `BaremetalHost` worker
    resource by running the following command on the hub cluster:

    ``` terminal
    oc get bmh -n <clusterinstance_namespace> worker-node2.example.com -ojsonpath='{.metadata.annotations}' | jq
    ```

    See the following example output for successful application of the
    annotation:

    ``` terminal
    {
      "baremetalhost.metal3.io/detached": "assisted-service-controller",
      "bmac.agent-install.openshift.io/hostname": "worker-node2.example.com",
      "bmac.agent-install.openshift.io/remove-agent-and-node-on-delete": "true"
      "bmac.agent-install.openshift.io/role": "master",
      "inspect.metal3.io": "disabled",
      "siteconfig.open-cluster-management.io/sync-wave": "1",
    }
    ```

#### Deleting the `BareMetalHost` resource of the worker node

Delete the `BareMetalHost` resource of the worker node that you want to
be removed.

Complete the following steps to remove a worker node from the managed
cluster:

1.  Update the node object that you want to delete in your existing
    `ClusterInstance` custom resource with the following configuration:

    ``` yaml
    ...
    spec:
       ...
       nodes:
         - hostName: "worker-node2.example.com"
           ...
           pruneManifests:
             - apiVersion: metal3.io/v1alpha1
               kind: BareMetalHost
    ...
    ```

2.  Apply the changes. See the following options:

    1.  If you are using Red Hat Advanced Cluster Management without Red
        Hat OpenShift GitOps, run the following command on the hub
        cluster:

        ``` terminal
        oc apply -f <clusterinstance>.yaml
        ```

    2.  If you are using GitOps ZTP, push to your Git repository and
        wait for Argo CD to synchronize the changes.

3.  Verify that the `BareMetalHost` resources are removed by running the
    following command on the hub cluster:

    ``` terminal
    oc get bmh -n <clusterinstance_namespace> --watch --kubeconfig <hub_cluster_kubeconfig_filename>
    ```

    See the following example output:

    ``` terminal
    NAME                        STATE                        CONSUMER         ONLINE   ERROR   AGE
    master-node1.example.com    provisioned                  true             81m
    worker-node2.example.com    deprovisioning               true             44m
    worker-node2.example.com    powering off before delete   true             20h
    worker-node2.example.com    deleting                     true             50m
    ```

4.  Verify that the `Agent` resources are removed by running the
    following command on the hub cluster:

    ``` terminal
    oc get agents -n <clusterinstance_namespace> --kubeconfig <hub_cluster_kubeconfig_filename>
    ```

    See the following example output:

    ``` terminal
    NAME                       CLUSTER                  APPROVED   ROLE     STAGE
    master-node1.example.com   <managed_cluster_name>   true       master   Done
    master-node2.example.com   <managed_cluster_name>   true       master   Done
    master-node3.example.com   <managed_cluster_name>   true       master   Done
    worker-node1.example.com   <managed_cluster_name>   true       worker   Done
    ```

5.  Verify that the `Node` resources are removed by running the
    following command on the managed cluster:

    ``` terminal
    oc get nodes --kubeconfig <managed_cluster_kubeconfig_filename>
    ```

    See the following example output:

    ``` terminal
    NAME                       STATUS                        ROLES                  AGE   VERSION
    worker-node2.example.com   NotReady,SchedulingDisabled   worker                 19h   v1.30.5
    worker-node1.example.com   Ready                         worker                 19h   v1.30.5
    master-node1.example.com   Ready                         control-plane,master   19h   v1.30.5
    master-node2.example.com   Ready                         control-plane,master   19h   v1.30.5
    master-node3.example.com   Ready                         control-plane,master   19h   v1.30.5
    ```

6.  After the `BareMetalHost` object of the worker node is successfully
    deleted, remove the associated worker node definition from the
    `spec.nodes` section in the `ClusterInstance` resource.

### Scaling out a single-node OpenShift cluster with the SiteConfig operator

Scale out your managed cluster that was installed by the SiteConfig
operator. You can scale out your cluster by adding a worker node.

**Required access:** Cluster administrator

#### Prerequisites

- If using GitOps ZTP, you have configured your GitOps ZTP environment.
  To configure your environment, see Preparing the hub cluster for
  GitOps ZTP.

- You have the default installation templates. To get familiar with the
  default templates, see Default set of templates.

- You have installed your cluster with the SiteConfig operator. To
  install a cluster with the SiteConfig operator, see Installing
  single-node OpenShift clusters with the SiteConfig operator.

- You have set the `spec.clusterType` to `"SNO"`.

#### Adding a worker node

Add a worker node by updating your `ClusterInstance` custom resource
that is used to provision your cluster.

Complete the following steps to add a worker node to the managed
cluster:

1.  Define a new node object in the existing `ClusterInstance` custom
    resource:

    ``` yaml
    spec:
      ...
      nodes:
        - hostName: "<host_name>"
          role: "worker"
          templateRefs:
            - name: ai-node-templates-v1
              namespace: rhacm
          bmcAddress: "<bmc_address>"
          bmcCredentialsName:
            name: "<bmc_credentials_name>"
          bootMACAddress: "<boot_mac_address>"
    ...
    ```

2.  Apply the changes. See the following options:

    1.  If you are using Red Hat Advanced Cluster Management without Red
        Hat OpenShift GitOps, run the following command on the hub
        cluster:

    ``` terminal
    oc apply -f <clusterinstance>.yaml
    ```

    1.  If you are using GitOps ZTP, push to your Git repository and
        wait for Argo CD to synchronize the changes.

3.  Verify that a new `BareMetalHost` resource is added by running the
    following command on the hub cluster:

    ``` terminal
    oc get bmh -n <clusterinstance_namespace> --watch --kubeconfig <hub_cluster_kubeconfig_filename>
    ```

    See the following example output:

    ``` terminal
    NAME                        STATE          CONSUMER   ONLINE   ERROR   AGE
    master-node1.example.com    provisioned               true             81m
    worker-node2.example.com    provisioning              true             44m
    ```

4.  Verify that a new `Agent` resource is added by running the following
    command on the hub cluster:

    ``` terminal
    oc get agents -n <clusterinstance_namespace> --kubeconfig <hub_cluster_kubeconfig_filename>
    ```

    See the following example output:

    ``` terminal
    NAME                       CLUSTER                   APPROVED    ROLE     STAGE
    master-node1.example.com   <managed_cluster_name>    true        master   Done
    master-node2.example.com   <managed_cluster_name>    true        master   Done
    master-node3.example.com   <managed_cluster_name>    true        master   Done
    worker-node1.example.com   <managed_cluster_name>    false       worker
    worker-node2.example.com   <managed_cluster_name>    true        worker   Starting installation
    worker-node2.example.com   <managed_cluster_name>    true        worker   Installing
    worker-node2.example.com   <managed_cluster_name>    true        worker   Writing image to disk
    worker-node2.example.com   <managed_cluster_name>    true        worker   Waiting for control plane
    worker-node2.example.com   <managed_cluster_name>    true        worker   Rebooting
    worker-node2.example.com   <managed_cluster_name>    true        worker   Joined
    worker-node2.example.com   <managed_cluster_name>    true        worker   Done
    ```

5.  Verify that a new `Node` resource is added by running the following
    command on the managed cluster:

    ``` terminal
    oc get nodes --kubeconfig <managed_cluster_kubeconfig_filename>
    ```

    See the following example output:

    ``` terminal
    NAME                       STATUS    ROLES                  AGE   VERSION
    worker-node2.example.com   Ready     worker                 1h    v1.30.5
    worker-node1.example.com   Ready     worker                 19h   v1.30.5
    master-node1.example.com   Ready     control-plane,master   19h   v1.30.5
    master-node2.example.com   Ready     control-plane,master   19h   v1.30.5
    master-node3.example.com   Ready     control-plane,master   19h   v1.30.5
    ```

### Mirroring images for disconnected environments

You can deploy a cluster with the SiteConfig operator operator by using
the Image Based Install Operator as your underlying operator. If you
deploy your clusters with the Image Based Install Operator in a
disconnected environment, you must supply your mirror images as extra
manifests in the `ClusterInstance` custom resource.

**Required access:** Cluster administrator

Complete the following steps to mirror images for disconnected
environments:

1.  Create a YAML file named `idms-configmap.yaml` for your
    `ImageDigestMirrorSet` object that contains your mirror registry
    locations:

    ``` yaml
    kind: ConfigMap
    apiVersion: v1
    metadata:
      name: "idms-configmap"
      namespace: "example-sno"
    data:
      99-example-idms.yaml: |
        apiVersion: config.openshift.io/v1
        kind: ImageDigestMirrorSet
        metadata:
          name: example-idms
        spec:
          imageDigestMirrors:
          - mirrors:
            - mirror.registry.example.com/image-repo/image
            source: registry.example.com/image-repo/image
    ```

    **Important:** Define the `ConfigMap` resource that contains the
    extra manifest in the same namespace as the `ClusterInstance`
    resource.

2.  Create the resource by running the following command on the hub
    cluster:

    ``` terminal
    oc apply -f idms-configmap.yaml
    ```

3.  Reference your `ImageDigestMirrorSet` object in the
    `ClusterInstance` custom resource:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: ClusterInstance
    metadata:
      name: "example-sno"
      namespace: "example-sno"
    spec:
      ...
      extraManifestsRefs:
        - name: idms-configmap
    ...
    ```

### Cluster reinstallation with the SiteConfig operator (Technology Preview)

The SiteConfig operator simplifies OpenShift cluster reinstallation
through the `ClusterInstance` API while preserving critical
configuration data.

With a GitOps-compatible, declarative approach, users can begin
reinstallations by updating the `ClusterInstance` resource. The operator
also includes a backup and restore mechanism for hub-side `Secret` and
`ConfigMap` resources, ensuring essential cluster data, such as
authentication credentials and configuration resources, remains intact.

#### Cluster identity preservation

Cluster reinstallation supports both single-node OpenShift and
multi-node OpenShift clusters. However, cluster identity preservation is
only supported for single-node OpenShift clusters installed using the
Image Based Install provisioning method.

For more information about the Image Based Install, see Image-based
installation for single-node OpenShift.

#### Cluster reinstallation workflow

See the following steps of the cluster reinstallation workflow:

- Label resources for preservation. This is optional if you do not want
  to preserve resources. You can label your resources well before
  initiating the cluster reinstallation.

- Initiate a cluster reinstallation.

- Monitor the reinstallation progress and verify that the reinstalled
  cluster is available. This is optional.

#### Resource labeling for preservation

If you want to retain essential cluster configuration data after
reinstallation, the SiteConfig operator provides a backup and restore
mechanism for hub-side `Secret` and `ConfigMap` resources within the
`ClusterInstance` namespace.

You can control data preservation by setting the `preservationMode` in
the `ClusterInstance` resource and adding the appropriate preservation
label to your resources. The following preservation modes are available:

- Preservation mode: None - Behavior: ConfigMap or Secret resources are
  not preserved. - Usage: Select the None mode if data preservation is
  unnecessary for the cluster during reinstallation. - Label
  requirement: None

- Preservation mode: All - Behavior: All labeled ConfigMap and Secret
  resources in the same namespace as the ClusterInstance resource are
  backed up. If the SiteConfig operator does not find any labeled
  resources, the operator proceeds with the reinstallation without data
  preservation. The original resources are stored as immutable
  Kubernetes secrets. - Usage: Select the All mode if you want to
  preserve labeled resources, if any. - Label requirement: Add the
  siteconfig.open-cluster-management.io/preserve: "\<arbitrary-value\>"
  label with any value, for example,
  siteconfig.open-cluster-management.io/preserve: "". The label
  indicates to the operator to back up resources with the specified
  label only when the preservation mode is set to All.

- Preservation mode: ClusterIdentity - Behavior: Only ConfigMap and
  Secret resources that are labeled with the
  siteconfig.open-cluster-management.io/preserve: "cluster-identity"
  label in the same namespace as the ClusterInstance CR are backed up.
  If the SiteConfig operator does not find any labeled resources, the
  operator stops the reinstallation process and displays an error
  message. The original CRs of these resources are stored as immutable
  Kubernetes secrets. - Usage: Select the ClusterIdentity mode if you
  want the operator to verify that you labeled at least one resource. -
  Label requirement: Add the
  siteconfig.open-cluster-management.io/preserve: "cluster-identity"
  label to indicate to the operator to back up resources with the label
  when the preservation mode is set to All or ClusterIdentity. If the
  preservation mode is set to ClusterIdentity and the operator does not
  find at least one resource with the
  siteconfig.open-cluster-management.io/preserve: "cluster-identity"
  label, the reinstallation stops.

You can label your resources well before initiating the reinstallation.

#### Cluster reinstallation monitoring

The reinstallation has two phases:

Phase 1 - Reinstallation request handling  
- Request validation: The SiteConfig operator validates the request.

- Data preservation: The SiteConfig operator backs up labeled resources.

- Cleanup: The SiteConfig operator removes existing installation
  manifests. If this step times out, the reinstallation stops and the
  `ClusterInstance` resource is paused.

- Data restoration: The SiteConfig operator restores preserved data.

Phase 2 - Cluster provisioning  
- Manifest regeneration: The SiteConfig operator generates new manifests
  from templates.

- Cluster installation: The cluster is provisioned using the new
  manifests.

You can track progress in the `status.reinstall.conditions` and
`status.conditions` fields for phase 1 and 2, respectively. To track the
cluster reinstallation progress, the SiteConfig operator provides the
following status conditions:

- Condition - Description - Reasons

- ReinstallRequestProcessed - Indicates the overall status of the
  reinstallation request. - InProgress: The reinstallation process is
  ongoing. Completed: The reinstallation process successfully completed,
  and the cluster is ready for reprovisioning. Failed: The
  reinstallation process encountered an error and failed. TimedOut: The
  reinstallation process exceeded the expected time limit and did not
  complete successfully.

- ReinstallRequestValidated - Confirms the validity of the
  reinstallation request. - Completed: The reinstallation request is
  valid. Failed: The reinstallation request is invalid.

- ReinstallPreservationDataBackedUp - Tracks the backup status of
  preserved data. - PreservationNotRequired: No backup required as
  spec.reinstall.preservationMode: None is set. DataUnavailable: No
  Secret or ConfigMap objects with the preservation label are found in
  the ClusterInstance namespace. Completed: Secret and ConfigMap objects
  are successfully backed up. Failed: One or more Secret and ConfigMap
  objects are not backed up.

- ReinstallClusterIdentityDataDetected - Determines whether cluster
  identity data is available for preservation. -
  PreservationNotRequired: Data preservation is not required. The
  preservationMode field is set to None. DataAvailable: Cluster identity
  Secret and ConfigMap objects are successfully located.
  DataUnavailable: No cluster identity Secret or ConfigMap objects are
  detected. Failed: The preservation mode is set to ClusterIdentity but
  no cluster identity data is found.

- ReinstallRenderedManifestsDeleted - Monitors the deletion of rendered
  manifests associated with the ClusterInstance resource. - InProgress:
  Deleting rendered manifests is in progress. Completed: Successfully
  deleted all rendered manifests. Failed: Failed to delete one or more
  rendered manifests. TimedOut: Timed out while waiting for rendered
  manifests to be deleted.

- ReinstallPreservationDataRestored - Tracks the restoration status of
  preserved data. - PreservationNotRequired: Preservation is not
  required because the preservationMode field is set to None.
  DataUnavailable: No preserved Secret or ConfigMap objects detected for
  restoration. Completed: Secret and ConfigMap objects are successfully
  restored. Failed: Failed to restore one or more Secret and ConfigMap
  objects.

The `status.reinstall` field provides further information about the
reinstallation process with the following fields:

- `InProgressGeneration`: Identifies the active generation being
  processed for reinstallation.

- `ObservedGeneration`: Indicates the last successfully processed
  reinstallation request.

- `RequestStartTime`: Indicates the time when the reinstallation request
  was initiated.

- `RequestEndTime`: Indicates the time when the reinstallation process
  was completed.

- `History`: Displays past reinstallation attempts, including generation
  details, timestamps, and specification changes to the
  `ClusterInstance` resource.

### Reinstalling a cluster with the SiteConfig operator (Technology Preview)

Reinstall your clusters by using the SiteConfig operator. After enabling
the reinstallation, you can define your desired preservation mode and if
applicable, label your resources.

**Required access:** Cluster administrator

Complete the following steps to reinstall a cluster:

1.  Enabling cluster reinstallation

2.  Labeling resources for preservation

3.  Initiating a cluster reinstallation

4.  Monitoring the cluster reinstallation

#### Enabling cluster reinstallation

You must explicitly enable cluster reinstallation in the
`siteconfig-operator-configuration` `ConfigMap` resource, which you can
complete well before initiating the process. By default, reinstallation
is disabled.

Complete the following steps:

1.  Set the `NAMESPACE` environment variable to match the namespace
    where the SiteConfig operator is installed. Run the following
    command:

    ``` bash
    NAMESPACE=<namespace>
    ```

2.  Verify the current configuration by running the following command:

    ``` bash
    oc get configmap siteconfig-operator-configuration -n $NAMESPACE -o yaml
    ```

    **Example output:**

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
        name: siteconfig-operator-configuration
        namespace: <namespace> 
    data:
        allowReinstalls: false 
        ...
    ```

    - The namespace where the SiteConfig operator is installed.

    - Set to `true` to enable reinstallation.

    **Note:** The operator continuously monitors the
    `siteconfig-operator-configuration` `ConfigMap` resource for
    changes.

3.  To enable cluster reinstallation, update the `ConfigMap` resource by
    setting the `data.allowReinstalls` field to `true`. Run the
    following command:

    ``` bash
    oc patch configmap siteconfig-operator-configuration \
        -n $NAMESPACE \
        --type=json \
        -p '[{"op": "replace", "path": "/data/allowReinstalls", "value": "true"}]'
    ```

4.  Verify the update by running the following command:

    ``` bash
    oc get configmap siteconfig-operator-configuration -n $NAMESPACE -o yaml
    ```

#### Labeling resources for preservation

You can set the desired preservation mode in your `ClusterInstance`
custom resource and if applicable, label your resources accordingly. By
default, the `preservationMode` field is set to `None`. For more
information, see Resource labeling for preservation.

Complete the following example step:

- Label a resource for the `All` preservation mode by running the
  following command:

  ``` bash
  oc label configmap <your_configmap> "siteconfig.open-cluster-management.io/preserve=all"
  ```

The `ClusterInstance` custom resource is updated with the correct
`preservationMode` corresponding to the applied labels.

#### Initiating a cluster reinstallation

To start the reinstallation, update the `ClusterInstance` resource with
a new `spec.reinstall.generation` value.

1.  Modify the `spec.reinstall.generation` value in the
    `ClusterInstance` resource:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: `ClusterInstance`
    metadata:
      name: clusterinstance-example
      namespace: some-namespace
    spec:
      reinstall:
        generation: "unique-generation-string"
        preservationMode: "<your-preservation-mode>"
    ```

    **Note:** Ensure you set the appropriate preservation mode when you
    modify the `ClusterInstance` resource. `"None"`, `"All"`, or
    `"ClusterIdentity"` are valid values.

2.  **Optional:** When defining the `spec.reinstall` object, you can
    modify the following additional fields in the `ClusterInstance`
    resource:

    - `spec.extraAnnotations`

    - `spec.extraLabels`

    - `spec.suppressedManifests`

    - `spec.pruneManifests`

    - `spec.nodes.<node-id>.extraAnnotations`

    - `spec.nodes.<node-id>.extraLabels`

    - `spec.nodes.<node-id>.suppressedManifests`

    - `spec.nodes.<node-id>.pruneManifests`

    - `spec.nodes.<node-id>.bmcAddress`

    - `spec.nodes.<node-id>.bootMACAddress`

    - `spec.nodes.<node-id>.nodeNetwork.interfaces.macAddress`

    - `spec.nodes.<node-id>.rootDeviceHints`

    **Note:** `<node-id>` represents the updated `NodeSpec` object.

3.  Apply the changes. See the following options:

    1.  If you are using OpenShift GitOps ZTP, push to your Git
        repository and wait for Argo CD to synchronize the changes.

    2.  To manually apply your changes, run the following command on the
        hub cluster:

    ``` bash
    oc apply -f clusterinstance-example.yaml
    ```

#### Monitoring the cluster reinstallation

You can monitor the cluster reinstallation progress. Complete the
following steps:

1.  Verify that the reinstallation request is being processed:

    ``` bash
    oc get clusterinstance clusterinstance-example -n some-namespace -o json | jq -r '.status.reinstall.conditions[] | select(.type=="ReinstallRequestProcessed")'
    ```

    See the following example output:

    ``` json
    {
    "type": "ReinstallRequestProcessed"
    "reason": "InProgress",
    "status": "False",
    ...
    }
    ```

2.  Verify that the cluster reinstallation request is validated
    successfully:

    ``` bash
    oc get clusterinstance clusterinstance-example -n some-namespace -o json | jq -r '.status.reinstall.conditions[] | select(.type=="ReinstallRequestValidated")'
    ```

    See the following example output:

    ``` json
    {
    "type": "ReinstallRequestValidated"
    "reason": "Completed",
    "status": "True",
    ...
    }
    ```

3.  Optional. If you set the `spec.reinstall.preservationMode` field to
    `All` or `ClusterIdentity`, verify that the cluster identity data is
    preserved:

    ``` bash
    oc get clusterinstance clusterinstance-example -n some-namespace -o json | jq -r '.status.reinstall.conditions[] | select(.type=="ReinstallPreservationDataBackedup")'
    ```

    See the following example output:

    ``` json
    {
    "type": "ReinstallPreservationDataBackedup"
    "reason": "Completed",
    "status": "True",
    ...
    }
    ```

4.  Optional. If you set the `spec.reinstall.preservationMode` field to
    `All` or `ClusterIdentity`, verify that the cluster identity data is
    detected:

    ``` bash
    oc get clusterinstance clusterinstance-example -n some-namespace -o json | jq -r '.status.reinstall.conditions[] | select(.type=="ReinstallClusterIdentityDataDetected")'
    ```

    See the following example output:

    ``` json
    {
    "type": "ReinstallClusterIdentityDataDetected"
    "reason": "DataAvailable",
    "status": "True",
    ...
    }
    ```

5.  Verify that the installation manifests are deleted. The deletion can
    take several minutes to complete.

    ``` bash
    oc get clusterinstance clusterinstance-example -n some-namespace -o json | jq -r '.status.reinstall.conditions[] | select(.type=="ReinstallRenderedManifestsDeleted")'
    ```

    See the following example output:

    ``` json
    {
    "type": "ReinstallRenderedManifestsDeleted"
    "reason": "Completed",
    "status": "True",
    ...
    }
    ```

6.  Optional. If you set the `preseservationMode` field to `All` or
    `ClusterIdentity`, verify that the data preserved earlier are
    restored:

    ``` bash
    oc get clusterinstance clusterinstance-example -n some-namespace -o json | jq -r '.status.reinstall.conditions[] | select(.type=="ReinstallPreservationDataRestored")'
    ```

    See the following example output:

    ``` json
    {
    "type": "ReinstallPreservationDataRestored"
    "reason": "Completed",
    "status": "True",
    ...
    }
    ```

7.  After you verified the previous steps, ensure that the
    reinstallation request completed successfully:

    ``` bash
    oc get clusterinstance clusterinstance-example -n some-namespace -o json | jq -r '.status.reinstall.conditions[] | select(.type=="ReinstallRequestProcessed")'
    ```

    See the following example output:

    ``` json
    {
    "type": "ReinstallRequestProcessed"
    "reason": "Completed",
    "status": "True",
    ...
    }
    ```

8.  Confirm that the cluster is successfully reinstalled and is
    operational by running an `oc` command with the `kubeconfig` file
    that is associated with the reinstalled cluster.

### Replacing hardware with Image-Based Break/Fix for single-node OpenShift (Technology Preview)

The Image-Based Break/Fix feature utilizes the cluster reinstallation
mechanism of the SiteConfig operator to simplify single-node OpenShift
hardware replacement. The feature minimizes downtime by preserving the
original identity of the cluster. The Image-Based Break/Fix feature
retains critical cluster details, including identifiers, cryptographic
keys, such as `kubeconfig`, and authentication credentials, which
enables the replacement node to seamlessly assume the identity of the
failed hardware.

Designed for identical hardware replacements in single-node OpenShift
clusters installed using the Image Based Install method, Image-Based
Break/Fix introduces a GitOps-compatible, declarative API. Users can
initiate hardware replacement with a single Git commit. Powered by the
SiteConfig operator and Image Based Install Operator, Image-Based
Break/Fix enables cluster redeployment using the existing
`ClusterInstance` custom resource.

With Image-Based Break/Fix, OpenShift Container Platform users gain a
resilient, automated, and GitOps-native solution for quickly restoring
single-node OpenShift clusters after hardware failures.

#### Image-Based Break/Fix cluster reinstallation workflow

The Image-Based Break/Fix workflow is similar to the cluster
reinstallation workflow with certain differences. To familiarize
yourself with the differences in the workflows, see the high-level
overview of the Image-Based Break/Fix cluster reinstallation workflow:

- Enable the SiteConfig operator reinstallation service.

- Initiate a cluster reinstallation.

  - Set `spec.reinstall.preservationMode: "ClusterIdentity"`.

  - Update the `spec.nodes` object with the changed hardware
    information.

  - **Note**: The Image Based Install Operator automatically labels
    cluster identity resources.

- Monitor the reinstallation progress.

  - During cluster provisioning, the operators consuming the
    installation manifests provision the cluster using the newly
    generated manifests.

  - **Note**: The Image Based Install Operator detects the preserved
    cluster identity data and incorporates it into the configuration ISO
    image.

- Verify that the cluster is provisioned and available.

  - Use the `kubeconfig` that is associated with the failed hardware to
    access the reinstalled spoke cluster.

For more information, see Cluster reinstallation with the SiteConfig
operator (Technology Preview.

#### Prerequisites

- The cluster is a single-node OpenShift cluster installed using the
  Image Based Install provisioning method.

- The faulty hardware is replaced with a new node with identical
  specifications.

#### Initiating the Image-Based Break/Fix cluster reinstallation

To initiate the Image-Based Break/Fix cluster reinstallation, update the
`ClusterInstance` resource by setting the `spec.reinstall.generation`
field and updating the `spec.nodes` object with the changed hardware
information.

1.  Modify the `spec.reinstall.generation` field and update the
    `spec.nodes` object in the `ClusterInstance` resource with the new
    node details:

    ``` yaml
    apiVersion: siteconfig.open-cluster-management.io/v1alpha1
    kind: `ClusterInstance`
    metadata:
      name: clusterinstance-example
      namespace: some-namespace
    spec:
      ...
      reinstall:
        generation: "unique-generation-string"
        preservationMode: "ClusterIdentity"
      nodes:
        - bmcAddress: <new-node-bmcAddress>
          bootMACAddress: <new-node-bootMACAddress>
          rootDeviceHints: <new-node-rootDeviceHints>
          nodeNetwork:
            interfaces:
              macAddress: <new-node-macAddress>
              ...
          ...
    ```

2.  Apply the changes. See the following options:

    1.  If you are using OpenShift GitOps ZTP, push to your Git
        repository and wait for Argo CD to synchronize the changes.

    2.  To manually apply your changes, run the following command on the
        hub cluster:

    ``` bash
    oc apply -f clusterinstance-example.yaml
    ```
