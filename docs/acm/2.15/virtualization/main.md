# Virtualization

Manage Red Hat OpenShift Virtualization virtual machine resources across
all the clusters that Red Hat Advanced Cluster Management manages.

To view `VirtualMachine` resources across all the clusters that Red Hat
Advanced Cluster Management manages, use the Search service to list and
filter the `VirtualMachine` resources that are created with the Red Hat
OpenShift Virtualization. You can also enable the following actions from
the Red Hat Advanced Cluster Management console on your `VirtualMachine`
resources:

- Start

- Stop

- Restart

- Pause

- Unpause

- Snapshot

## Viewing virtual machine metrics through Observability fields

If you have the Observability service installed on your hub cluster, you
can access the Observability fields on the Red Hat Advanced Cluster
Management console to view your virtual machine metrics.

Access the Observability fields by completing the following steps:

1.  On the Red Hat Advanced Cluster Management console, go to the
    `Virtual Machine` page.

2.  Select the `Observability dashboards` link to launch the `Grafana`
    dashboard.

    1.  **Optional:** Select the `Observability metrics` link in the
        `Launch links` table cell to launch the `Grafana` dashboard,

3.  From the `Grafana` dashboard, view the virtual machines and their
    individual metrics.

## Configuring backup and restore for Red Hat OpenShift Virtualization by using policies

Use OpenShift APIs for Data Protection (OADP) to backup and restore
virtual machines. After you back up the virtual machines, you can
restore it on the hub or managed clusters.

These Red Hat Advanced Cluster Management policies for OpenShift
Virtualization support the following backup and restore storage options:

- Container Storage Interface (CSI) backups

- Container Storage Interface (CSI) backups with DataMover

They do not support the following options:

- File system backup and restore

- Volume snapshot backups and restores

### Backing up and restoring a virtual machine

You can back up virtual machines that run on a cluster or restore a
virtual machine on a cluster by completing the following steps:

1.  Enable the backup component on the hub cluster by setting the
    `cluster-backup` parameter in `MultiClusterHub` to `true`.

2.  To place the policies on the `cluster-name` cluster, add the
    `acm-virt-config` label to the `ManagedCluster` resource by applying
    the following YAML sample:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1
    kind: ManagedCluster
    metadata:
     name: cluster-name
     labels:
       acm-virt-config: acm-dr-virt-config 
    ```

    - The `acm-dr-virt-config` that passes through the label annotation
      is a `acm-virt-config` ConfigMap. Read the `acm-dr-virt-config`
      ConfigMap section to understand how to configure OADP and backup
      storage location.

3.  Complete the following steps, depending on whether you want to
    backup or restore your virtual machine:

    1.  Back up your virtual machine by adding the
        `cluster.open-cluster-management.io/backup-vm` to the
        `kubevirt.io.VirtualMachine` resource. Your
        `kubevirt.io.VirtualMachine` resource might resemble the
        following YAML sample:

    ``` yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      name: vm-name
      labels:
        cluster.open-cluster-management.io/backup-vm: daily_8am
    ```

    1.  Restore your virtual machine by updating the
        `acm-dr-restore-config` ConfigMap as described in the
        `acm-dr-virt-restore-config` section.

### Virtualization policies installed on the hub cluster

When you enable the backup operator, a set of Red Hat Advanced Cluster
Management policies and `ConfigMaps`, get installed on the hub cluster.
When you disable the policy or remove it from the cluster, all the
resources the policy created gets removed. To learn more about the
different types of policies that are available, complete the following
sections:

#### Installation policy

The `acm-dr-virt-install` installation policy installs OADP and
configures the `oadp.openshift.io.DataProtectionApplication` resource on
the cluster where this policy is placed. If the cluster is a hub
cluster, it verifies that OADP is installed in the
`open-cluster-management-backup` namespace and that the
`DataProtectionApplication` resource exists and has the required
configuration. The policy does not attempt to install OADP or create the
`DataProtectionApplication` resource on the hub cluster.

When you enable the `cluster-backup` option on the `MultiClusterHub`
resource, the backup chart installs the OADP. When you enable the
`cluster-backup-option`, you create the `DataProtectionApplication` on
the hub cluster.

See the following installation policy templates and descriptions:

1.  Installation policy templates

- Template - Description

- check-config-file - Verifies that the ConfigMap that is defined by the
  acm-virt-config label set on the ManagedCluster resource exists on the
  hub cluster, in the open-cluster-management-backup namespace.

- check-oadp-channel - Verifies if there is an OADP version installed on
  the cluster, and that it matches the version installed by the policy.

- check-dpa-config - Verifies that the DataProtectionApplication
  resource exists, has the expected configuration, and has a status of
  Reconciled. Verifies that the BackupStorageLocation exists and is in
  the Available status phase.

- install-oadp-copy-config - Creates the namespace where OADP gets
  installed, if this namespace is not found. Copies the OADP secret and
  installs OADP, but only for managed clusters. Creates the
  DataProtectionApplication resource as defined by the acm-virt-config
  label, but only for the managed clusters. The user must manually
  create the OADP and DataPotectionApplication on the hub cluster.

#### Backup policy

The `acm-dr-virt-backup` backup policy backs up the
`kubevirt.io.VirtualMachine` resources that has the label,
`cluster.open-cluster-management.io/backup-vm: schedule_cron_name`.

See the following backup policy templates and descriptions:

1.  Backup policy templates

- Template - Description

- check-cron-schedule-valid - Shows a violation error if there is any
  cron schedule name used by a virtual machine
  cluster.open-cluster-management.io/backup-vm label which is not found
  in the ConfigMap for the cron schedules. The name of the ConfigMap for
  the cron schedules is defined by the schedule_hub_config_name property
  and is available within the open-cluster-management-backup namespace.

- check-backup-status-completed - If the schedule is not paused, it
  verifies that the status is Enabled. Finds the latest backup generated
  by this schedule and verifies that the status is Completed. If any
  DataUpload has been created for this backup, the status is Completed.
  Shows a violation if any of these conditions are not True.

- create-virt-backup - Creates Velero schedules for all virtual machine
  resources with a cluster.open-cluster-management.io/backup-vm label.
  Creates one schedule for each cron job schedule found with the virtual
  machines label. Backs up the virtual machine sharing the same cron job
  schedule within the same backup. Creates the Velero schedule resource
  only if the acm-dr-virt-install policy is compliant.

#### Restore policy

The `acm-dr-virt-restore` restore policy restores the
`kubevirt.io.VirtualMachine` resources by UID. The policy creates Velero
restore resources on clusters using the information from the ConfigMap
that is identified by the `restore_hub_config_name` property from the
`acm-dr-virt-config` ConfigMap.

See the following restore policy templates and descriptions:

1.  Restore policy templates

- Template - Description

- check-velero-restore-status - Verifies that the restore resource with
  the name defined by the clusterID_restoreName property exists and has
  a status of Completed.

- create-velero-restore - If the clusterID_restoreName property value is
  not empty, and the clusterID matches this cluster UID, it creates a
  Velero restore resources using the properties defined with the
  ConfigMap that is identified by the restore_hub_config_name. Creates
  the Velero restore resource only if the acm-dr-virt-install policy is
  compliant.

### Defining policies with *ConfigMaps*

When you install the policies on the hub cluster, the following
`ConfigMaps` are created on the hub cluster, in the
`open-cluster-management-backup` namespace. When you place the
virtualization policies on the hub or managed cluster, these
`ConfigMaps` define the backup and restore configuration for the
virtualization policies.

#### Defining the *acm-dr-virt-config* *ConfigMap*

The `acm-dr-virt-config` ConfigMap defines the OADP configuration and
other settings related to the backup or restore operation. You can use
the name of this resource as the value for the `acm-virt-config` label
which is set on the `ManagedCluter` where the policies are placed. You
can also create a new `ConfigMap` resource that uses the
`acm-dr-virt-config` as a sample, then use your new `ConfigMap` resource
to place the virtualization policies on the cluster.

To place the virtualization policies on a managed cluster or hub
cluster, complete the following steps:

1.  Use the `acm-dr-virt-config` or create a new `ConfigMap` resource on
    the hub cluster in the `open-cluster-management-backup` namespace,
    by using the `acm-dr-virt-config` ConfigMap as an example. For this
    example, the name of the ConfigMap is `acm-dr-virt-config-new`.

    1.  Update the `dpa_spec` section to match the storage location
        where you want to store the backups created by OADP. This is a
        required update.

    2.  **Optional:** Update other properties available with the
        `acm-dr-virt-config-new` ConfigMap, such as OADP version or
        channel.

2.  Add the `acm-virt-config=acm-dr-virt-config-new` label to the
    `ManagedCluster` resource. The value of the `acm-virt-config` label
    is the name of the ConfigMap that you created.

For an example of a `ManagedCluster` resource with a virtualization
backup label set to use the `acm-dr-virt-config-new` ConfigMap, see the
following YAML sample:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1
kind: ManagedCluster
metadata:
 name: managed-cluster-name
 labels:
   acm-virt-config: acm-dr-virt-config-new
```

To learn more, see the following tables:

1.  ConfigMap properties for the `acm-dr-virt-install` policy

- Name - Description - Type - Default value - Optional

- channel - The channel defaults to the supported OADP version, which is
  based on the version of the OpenShift Container Platform cluster. Use
  this property to overwrite the default value. - String - None - Yes

- channelName - OADP channel name. Set this property for custom
  installation, for example: offline install. - String -
  redhat-oadp-operator - Yes

- subscriptionSource - OADP subscription. Set this property for custom
  installation, for example: offline install. - String -
  redhat-operators - Yes

- subscriptionSourceNamespace - OADP subscription source. Set this
  property for custom installation, for example: offline install. -
  String - openshift-marketplace - Yes

- subscriptionStartingCSV - OADP subscription startingCSV. - String -
  None - Yes

- subscriptionInstallPlanApproval - OADP install plan. - String -
  Automatic - Yes

- backupNS - Namespace where OADP gets installed on the managed
  cluster. - String - None - No

- credentials_hub_secret_name - Name of the OADP secret that you use on
  the managed cluster. A Secret with this name must exist on the hub
  cluster in the open-cluster-management-backup namespace. The install
  policy moves this secret to the hub cluster within the specified
  backupNS namespace. - String - None - No

- credentials_name - Name of the secret used by the OADP
  DataProtectionApplication resource on the managed cluster, when
  setting the Velero credential name. - JSON - None - No

- dpa_name - Name of the DataProtectionApplication resource that gets
  created on the managed cluster. - String - None - No

- dpa_spec - Valid JSON defining the DataProtectionApplication spec when
  created on the managed cluster. - JSON - None - No

1.  ConfigMap properties for the `acm-dr-virt-backup` policy

- Name - Description - Type - Default value - Optional

- scheduleTTL - Backup expiration time. - String - 24h0m0s - Yes

- schedule_paused - Set to True to pause the virtualization backup
  schedule. - String - False - Yes

- schedule_hub_config_name - Name of the ConfigMap used to define the
  valid cron jobs schedules. A ConfigMap with this name must exist on
  the hub cluster in the open-cluster-management-backup namespace. -
  String - None - Yes

1.  ConfigMap properties for the `acm-dr-virt-restore` policy

- Name - Description - Type - Default value - Optional

- restore_hub_config_name - Name of the ConfigMap used to define the
  restore operation. A ConfigMap with this name must exist on the hub
  cluster in the open-cluster-management-backup namespace - String -
  None - No

#### Defining the *acm-dr-virt-schedule-cron* *ConfigMap*

Use the `acm-dr-virt-schedule-cron` ConfigMap to define the valid cron
job schedules to use when you are scheduling a virtual machine backup.
The `acm-dr-virt-schedule-cron` ConfigMap is created by the hub cluster
backup component in the `open-cluster-management-backup` namespace and
includes the following YAML:

``` yaml
apiVersion: v1
kind: ConfigMap
    metadata:
        name: acm-dr-virt-schedule-cron
        namespace: open-cluster-management-backup
    data:
        hourly: "0 */1 * * *"
        every_2_hours: "0 */2 * * *"
        every_3_hours: "0 */3 * * *"
        every_4_hours: "0 */4 * * *"
        every_5_hours: "0 */5 * * *"
        every_6_hours: "0 */6 * * *"
        twice_a_day: "0 */12 * * *"
        daily_8am: "0 8 * * *"
        every_sunday: "0 0 * * 0"
```

You can use any of the schedules created by the
`acm-dr-virt-schedule-cron` ConfigMap to set the backup schedule for a
`kubevirt.io.VirtualMachine`. For example, if you want to backup a
virtual machine every day at 8am, add the following label to the virtual
machine resource:

``` yaml
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: vm-name
  labels:
    cluster.open-cluster-management.io/backup-vm: daily_8am
```

Since this `acm-dr-virt-schedule-cron` ConfigMap is created and managed
by the hub cluster backup component, you cannot change any of the
existing cron properties or delete them. The properties are recreated
when the content is reconciled. You can only add new properties to the
existing ones. For example, if you want to create a cron job to run
every Saturday, add the following label to the existing
`acm-dr-virt-schedule-cron` properties: `every_sunday: "0 0 * * SAT"`.

#### Defining the *acm-dr-virt-restore-config* ConfigMap

Use the `acm-dr-virt-restore-config` ConfigMap to define the restore
operations to be implemented by the `acm-dr-virt-restore` policy. Use
the hub cluster backup component in the `open-cluster-management-backup`
namespace to create the ConfigMap.

For an example of a complete restore operation, see the following YAML
sample:

``` yaml
kind: ConfigMap
apiVersion: v1
metadata:
 name: acm-dr-virt-restore-config
 namespace: open-cluster-management-backup
data:
 2a054d24-3235-4249-9c81-f58ebc6110c7_backupName: acm-rho-virt-schedule-every-10-hours-20250120230438 
 2a054d24-3235-4249-9c81-f58ebc6110c7_restoreName: restore-20250120230438 
 2a054d24-3235-4249-9c81-f58ebc6110c7_vmsUID: 2a054d24-3235-4249-9c81-f58ebc6110c7 
 2a054d24-3235-4249-9c81-f58ebc6110c7_namespaceMapping: backup-ns-1=restore-ns-1{{ backup-ns-2=restore-ns-2}} 
```

- `2a054d24-3235-4249-9c81-f58ebc6110c7` is the cluster ID where the
  restore operation is complete.
  `acm-rho-virt-schedule-every-10-hours-20250120230438` is the name of
  the backup that is used for the restore operation example.

- `restore-20250120230438` is the name of the `Restore` resource that is
  created as a result of this restore operation.

- `2a054d24-3235-4249-9c81-f58ebc6110c7` is the UID of the virtual
  machine backed up with the
  `acm-rho-virt-schedule-every-10-hours-20250120230438` backup to be
  restored.

- `namespaceMapping` is an optional property and is used to restore
  resources in a different namespace than the initial resource. Any
  source namespaces not included in the map is restored into namespaces
  of the same name. `backup-ns-1=restore-ns-1 backup-ns-2=restore-ns-2`
  is a space separated list of namespace mapping. In this sample, backup
  resources created within the `backup-ns-1` namespace are restored
  within the `restore-ns-1` namespace. The `restore-ns-1` is created on
  the restore cluster if it does not exist. Similarly, resources created
  within the `backup-ns-2` are restored within the `restore-ns-2`
  namespace.

### Creating restore operations with restore policies

When you install virtualization policies for your restore operations,
consider the following scenarios:

- If you set the `clusterID_restoreName` property from the
  `acm-dr-virt-restore-config` ConfigMap to an empty value, then the
  restore resource created by the `acm-dr-virt-restore` policy on the
  cluster with `clusterID` gets deleted.

- If you set the `clusterID_restoreName` property from the
  `acm-dr-virt-restore-config` ConfigMap to a non-empty value, then the
  `acm-dr-virt-restore` policy creates a Velero `Restore` resource . The
  name of the Velero restore resource matches the
  `clusterID_restoreName` value. If the restore resource with this name
  is deleted from the restore cluster, the `acm-dr-virt-restore` policy
  recreates the resource, which results in the restore operation running
  again.

- Consider the following actions:

  - Do not delete the restore resource if you do not want to run the
    restore again.

  - Remove the value for the `clusterID_restoreName` parameter on the
    `acm-dr-virt-restore-config` ConfigMap when the restore operation
    gets verified to start. Doing this prevents you from having to rerun
    the restore operation if the `acm-dr-virt-restore` policy is
    disabled and enabled again. When you disable the
    `acm-dr-virt-restore` policy, all resources created by it on the
    restore cluster get cleaned up and recreated when you enable the
    policy again.

## Migrating virtual machines between clusters (Technology Preview)

Migrating virtual machines helps you move resources during cluster
upgrades, times when you need to clear a node for maintenance, or during
configuration changes. When you enable migration, the Red Hat OpenShift
Virtualization is automatically installed on your managed clusters with
the `acm/cnv-operator-install` label. The migration toolkit for
virtualization is also installed on your hub cluster.

**Required access:** Cluster administrator

<div>

<div class="title">

Prerequsites

</div>

- You must have access to the `openshift-cnv` namespace.

- You have the `kubevirt.io:admin` role as both a target and a source
  cluster

- You have the `kubevirt.io-acm-hub:admin` for your hub cluster and
  `kubevirt.io-acm-managed:admin` for your target managed cluster.

- You have the latest version of OpenShift Container Platform installed.
  See the OpenShift Container Platform Overview.

</div>

To start migration for virtual machines complete the following steps:

1.  Enable `cnv-mtv-integrations-preview` component for the integration
    of Red Hat OpenShift Virtualization.

    1.  Run the following command to edit your `multiclusterhub`
        instance:

    ``` bash
    oc edit MultiClusterHub multiclusterhub -n open-cluster-management
    ```

    1.  From the `components` specification, set the `enabled` parameter
        to `true` for the `cnv-mtv-integrations-preview` component.

2.  Verify that the migration toolkit for virtualization is available on
    your cluster. Run the following command:

    ``` bash
    oc get clustermanagementaddon mtv-operator  -o jsonpath='{.status.installProgressions[*].conditions[*].reason}
    ```

3.  Verify that the `kubevirt-hyperconverged` resource is available on
    your cluster with the following command:

    ``` bash
    oc get clustermanagementaddon kubevirt-hyperconverged -o jsonpath='{.status.installProgressions[*].conditions[*].reason}
    ```

4.  Verify that the `kubevirt-hyperconverged-operator` is available on
    your cluster with the following command:

        oc get clustermanagementaddon kubevirt-hyperconverged-operator -o jsonpath='{.status.installProgressions[*].conditions[*].reason}

5.  To designate a cluster as a source or target for the virtual machine
    migration, apply the following label to your clusters:
    `acm/cnv-operator-install: "true"`.

6.  Enable cross-cluster migration from the OpenShift Virtualization
    console. Complete the following steps:

    1.  From the navigation menu, select **Virtualization** \>
        **Overview**.

    2.  To access the preview features, click **Settings** \> **Preview
        Features**.

    3.  Set `Enable Kubevirt cross cluster migration` to `true`.

7.  **Optional:** Configure your network for the live migration within
    your `HyperConverged` resource by updating the `customizedVariables`
    specification. Add the network key and value to your
    `cnv-hco-config` `AddOnDeploymentConfig` resource. Your
    `AddOnDeployment` resource might resemble the following sample:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: AddOnDeploymentConfig
    metadata:
      name: cnv-hco-config
      namespace: open-cluster-management
    spec:
      agentInstallNamespace: openshift-cnv
      customizedVariables:
        - name: LIVE_NETWORK_KEY
          value: network
        - name: LIVE_NETWORK_VALUE
          value: {{ NetworkAttachmentDefinition name like lm-network }}
    ```
