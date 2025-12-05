# Business continuity

## Backup and restore

The cluster backup and restore operator runs on the hub cluster and
provides disaster recovery solutions for Red Hat Advanced Cluster
Management for Kubernetes hub cluster failures. When the hub cluster
fails, some features stop working, even if all managed clusters still
work. When the hub cluster is unavailable, you need a recovery plan to
decide if recovery is possible, or if you need to recover the data on a
newly deployed hub cluster.

The cluster backup and restore operator supports backups of any
third-party resources that extend the hub cluster installation. With
this backup solution, you can define cron-based backup schedules that
run at specified time intervals. When the hub cluster fails, you can
deploy a new hub cluster and move the backed up data to that new hub
cluster.

### Backup and restore operator architecture

The backup and restore operator manages the backup and restore processes
for Red Hat Advanced Cluster Management hub clusters. The operator
implements the following custom resources:

- `BackupSchedule.cluster.open-cluster-management.io` to set up Red Hat
  Advanced Cluster Management backup schedules.

- `restore.cluster.open-cluster-management.io` to process and restore
  these backups.

With the operator, you have Velero resources to define the options that
you need to back up remote and hub cluster resources that need to be
restored.

For a visual of this process, see the following architecture diagram:

The backup and restore component gives a set of policies for reporting
issues. Use the policy templates to create an alert to the hub cluster
administrator if the backup solution is not functioning.

The cluster backup and restore operator depends on the OADP Operator to
install Velero, and to create a connection from the hub cluster to the
backup storage location where the data is stored. Velero is the
component that runs the backup and restore operations. The cluster
backup and restore operator solution provides backup and restore support
for all Red Hat Advanced Cluster Management hub cluster resources,
including managed clusters, applications, and policies.

#### Resources that are backed up

The cluster backup and restore operator solution provides backup and
restore support for all hub cluster resources such as managed clusters,
applications, and policies. Use the solution to back up any third-party
resources extending the basic hub cluster installation. With this backup
solution, define a cron-based backup schedule, which runs at specified
time intervals and continuously backs up the latest version of the hub
cluster content.

When the hub cluster needs to be replaced or is in a disaster scenario
when the hub cluster fails, a new hub cluster can be deployed and backed
up data is moved to the new hub cluster.

View the following list of the cluster backup and restore process, and
how they back up or exclude resources and groups to identify backup
data:

- Exclude all resources in the `MultiClusterHub` namespace. This is to
  avoid backing up installation resources that are linked to the current
  hub cluster identity and should not be backed up.

- Back up all resources with an API version suffixed by
  `.open-cluster-management.io` and `.hive.openshift.io`. These suffixes
  indicate that all Red Hat Advanced Cluster Management resources are
  backed up.

- Back up all resources from the following API groups: `argoproj.io`,
  `app.k8s.io`, `core.observatorium.io`, `hive.openshift.io`. The
  resources are backed up within the `acm-resources-schedule` backup,
  with the exception of the resources from the
  `agent-install.openshift.io` API group. Resources from the
  `agent-install.openshift.io` API group are backed up within the
  `acm-managed-clusters-schedule` backup. The following resources from
  `hive.openshift.io` and `hiveinternal.openshift.io` API groups are
  also backed up by the `acm-managed-clusters-schedule` backup:

  - `clusterdeployment.hive.openshift.io`

  - `machinepool.hive.openshift.io`

  - `clusterpool.hive.openshift.io`

  - `clusterclaim.hive.openshift.io`

  - `clusterimageset.hive.openshift.io`

  - `clustersync.hiveinternal.openshift.io`

- Exclude all resources from the following API groups:

  - `internal.open-cluster-management.io`

  - `operator.open-cluster-management.io`

  - `work.open-cluster-management.io`

  - `search.open-cluster-management.io`

  - `admission.hive.openshift.io`

  - `proxy.open-cluster-management.io`

  - `action.open-cluster-management.io`

  - `view.open-cluster-management.io`

  - `clusterview.open-cluster-management.io`

  - `velero.io`

- Exclude all of the following resources that are a part of the included
  API groups, but are either not needed or are being recreated by owner
  resources that are also backed up:

  - `clustermanagementaddon.addon.open-cluster-management.io`

  - `backupschedule.cluster.open-cluster-management.io`

  - `restore.cluster.open-cluster-management.io`

  - `clusterclaim.cluster.open-cluster-management.io`

  - `discoveredcluster.discovery.open-cluster-management.io`

- Back up secrets and ConfigMaps with one of the following labels:
  `cluster.open-cluster-management.io/type`,
  `hive.openshift.io/secret-type`,
  `cluster.open-cluster-management.io/backup`.

- Use the `cluster.open-cluster-management.io/backup` label for any
  other resources that you want to be backed up and are not included in
  the previously mentioned criteria or are part of the excluded API
  groups. See the following example:

  ``` yaml
  apiVersion: my.group/v1alpha1
  kind: MyResource
   metadata:
     labels:
      cluster.open-cluster-management.io/backup: ""
  ```

  **Note:** Secrets used by the `hive.openshift.io.ClusterDeployment`
  resource need to be backed up, and are automatically annotated with
  the `cluster.open-cluster-management.io/backup` label only when you
  create the cluster by using the console. If you deploy the Hive
  cluster by using GitOps instead, you must manually add the
  `cluster.open-cluster-management.io/backup` label to the secrets used
  by the `ClusterDeployment` resource. Secret and config map resources
  with the
  `cluster.open-cluster-management.io/backup: cluster-activation` label
  are restored at cluster activation time.

- Exclude specific resources that you do not want backed up. See the
  following example to exclude Velero resources from the backup process:

  ``` yaml
  apiVersion: my.group/v1alpha1
  kind: MyResource
   metadata:
    labels:
      velero.io/exclude-from-backup: "true"
  ```

#### Backup files created by a Red Hat Advanced Cluster Management schedule

You can use a Red Hat Advanced Cluster Management schedule to backup hub
cluster resources, which are grouped in separate backup files, based on
the resource type or label annotations.

The `BackupSchedule.cluster.open-cluster-management.io` resource creates
a set of four `schedule.velero.io` resources. These `schedule.velero.io`
resources generate the backup files, which are also called resources.

To view the list of scheduled backup files, run the following command:
`oc get schedules -A | grep acm`.

The scheduled backup files are `backup.velero.io`. See the following
table to view the descriptions of these scheduled backup files:

- Scheduled backup: Credentials backup - Description: Stores the
  following: Hive credentials, Red Hat Advanced Cluster Management,
  user-created credentials, and ConfigMaps. The name of this backup file
  is acm-credentials-schedule-\<timestamp\>.

- Scheduled backup: Resources backup - Description: Contains one backup
  for the Red Hat Advanced Cluster Management resources,
  acm-resources-schedule-\<timestamp\> backup and one for generic
  resources, acm-resources-generic-schedule-\<timestamp\>. Any resources
  annotated with the backup label,
  cluster.open-cluster-management.io/backup, are stored under the
  backup, acm-resources-generic-schedule- backup. The exceptions are
  Secrets or ConfigMap resources which are stored under the backup
  acm-credentials-schedule-\<timestamp\>.

- Scheduled backup: Managed clusters backup - Description: Contains only
  resources that activate the managed cluster connection to the hub
  cluster, where the backup is restored. The name of this backup file is
  acm-managed-clusters-schedule-\<timestamp\>.

#### Resources restored at managed clusters activation time

When you add the `cluster.open-cluster-management.io/backup` label to a
resource, the resource is automatically backed up in the
`acm-resources-generic-schedule` backup, except for the `Secrets` and
`ConfigMap` resources which are backed up in the
`backup acm-credentials-schedule-`. Set the label value to
`cluster-activation` if you need to restore any of the resources after
you move the managed clusters to the new hub cluster, and when you use
the `veleroManagedClustersBackupName:latest` on the restored resource.

When you set the `cluster.open-cluster-management.io/backup` label to
`cluster-activation`, you ensure that the resource is not restored
unless you activate the managed cluster. View the following example:

``` yaml
apiVersion: my.group/v1alpha1
kind: MyResource
 metadata:
  labels:
    cluster.open-cluster-management.io/backup: cluster-activation
```

**Note:** For any managed cluster namespace, or any resource in it, you
must restore either one at the cluster activation step. Therefore, if
you need to add to the backup resource created in the managed cluster
namespace, then use the `cluster-activation` value for the
`cluster.open-cluster-management.io/backup` label. To understand the
restore process, see the following information:

- If you restore the namespace, then the
  `managedcluster-import-controller` deletes the namespace.

- If you restore the `managedCluster` custom resource, then the
  `cluster-manager-registration-controller` creates the namespace.

Aside from the activation data resources that are identified by using
the `cluster.open-cluster-management.io/backup: cluster-activation`
label and stored by the `acm-resources-generic-schedule` backup, the
cluster backup and restore operator includes a few resources in the
activation set by default. The following resources are backed up by the
`acm-managed-clusters-schedule` backup:

- `managedcluster.cluster.open-cluster-management.io`

- `klusterletaddonconfig.agent.open-cluster-management.io`

- `managedclusteraddon.addon.open-cluster-management.io`

- `managedclusterset.cluster.open-cluster-management.io`

- `managedclusterset.clusterview.open-cluster-management.io`

- `managedclustersetbinding.cluster.open-cluster-management.io`

- `clusterpool.hive.openshift.io`

- `clusterclaim.hive.openshift.io`

- `clustercurator.cluster.open-cluster-management.io`

#### *Backup* label function

You can backup third-party resources with cluster backup and restore by
adding the `cluster.open-cluster-management.io/backup` label to the
resources. The value of the label can be any string, including an empty
string. Use a value that can help you identify the component that you
are backing up. For example, use the
`cluster.open-cluster-management.io/backup: idp` label if the components
are provided by an IDP solution.

**Note:** Use the `cluster-activation` value for the
`cluster.open-cluster-management.io/backup` label if you want the
resources to be restored when the managed clusters activation resources
are restored. When you restore the managed clusters activation
resources, the restore starts for the managed clusters that are actively
managed by the hub cluster.

#### Additional resources

Learn more about the policies and capabilities of the backup and restore
component by going to Validating your backup or restore configurations.

### Configuring active-passive hub cluster

Configure an active-passive hub cluster configuration, where the initial
hub cluster backs up data and the passive hub clusters control the
managed clusters when the active cluster becomes unavailable.

#### Active-passive configuration

In an active-passive configuration, there is one active hub cluster and
passive hub clusters. An active hub cluster is also considered the
primary hub cluster, which manages clusters and backs up resources at
defined time intervals, using the
`BackupSchedule.cluster.open-cluster-management.io` resource.

**Note:** To backup the primary hub cluster data, you do not need an
`active-passive` configuration. You can simply backup and store the hub
cluster data. This way, if there is an issue or failure, you can deploy
a new hub cluster and restore your primary hub cluster data on this new
hub cluster. To reduce the time to recover the primary hub cluster data,
you can use an `active-passive` configuration; however, this is not
necessary.

Passive hub clusters continuously retrieve the latest backups and
restore the passive data. Passive hubs use the
`Restore.cluster.open-cluster-management.io` resource to restore passive
data from the primary hub cluster when new backup data is available.
These hub clusters are on standby to become a primary hub when the
primary hub cluster fails.

Active and passive hub clusters are connected to the same storage
location, where the primary hub cluster backs up data for passive hub
clusters to access the primary hub cluster backups. For more details on
how to set up this automatic restore configuration, see *Restoring
passive resources while checking for backups*.

In the following diagram, the active hub cluster manages the local
clusters and backs up the hub cluster data at regular intervals:

The passive hub cluster restores this data, except for the managed
cluster activation data, which moves the managed clusters to the passive
hub cluster. The passive hub clusters can restore the passive data
continuously. Passive hub clusters can restore passive data as a
one-time operation. See *Restoring passive resources* for more details.

#### Disaster recovery

When the primary hub cluster fails, as a hub administrator, you can
select a passive hub cluster to take over the managed clusters. In the
following *Disaster recovery diagram*, see how you can use *Hub cluster
N* as the new primary hub cluster:

*Hub cluster N* restores the managed cluster activation data. The
managed clusters connect to *Hub cluster N*. You activate a backup on
the new primary hub cluster, *Hub cluster N*, by creating a
`BackupSchedule.cluster.open-cluster-management.io` resource, and
storing the backups at the same storage location as the initial primary
hub cluster.

All other passive hub clusters now restore passive data by using the
backup data that is created by the new primary hub cluster. *Hub N* is
now the primary hub cluster, managing clusters and backing up data.

**Important:**

- The first process in the earlier *Disaster recovery diagram* is not
  automated because of the following reasons:

  - You must decide if the primary hub cluster has failed and needs to
    be replaced, or if there is a network communication error between
    the hub cluster and the managed clusters.

  - You must decide which passive hub cluster becomes the primary hub
    cluster. The policy integration with Red Hat Ansible Automation
    Platform jobs can help you automate this step by making a job run
    when the backup policy reports backup errors.

- The second process in the earlier *Disaster recovery diagram* is
  manual. If you did not create a backup schedule on the new primary hub
  cluster, the `backup-restore-enabled` policy shows a violation by
  using the `backup-schedule-cron-enabled` policy template. In this
  second process, you can do the following actions:

  - Use the `backup-schedule-cron-enabled` policy template to validate
    if the new primary hub cluster has backups running as a cron job.

  - Use the policy integration with `Ansible` and define an `Ansible`
    job that can run when the `backup-schedule-cron-enabled` policy
    template reports violations.

- For more details about the `backup-restore-enabled` policy templates,
  see Validating your backup or restore configurations.

### Installing the backup and restore operator

#### Prerequisites

- From your Red Hat OpenShift Container Platform cluster, install the
  Red Hat Advanced Cluster Management operator version 2.15. The
  `MultiClusterHub` resource is automatically created when you install
  Red Hat Advanced Cluster Management, and displays the following
  status: `Running`.

#### Enabling the backup operator for your hub clusters

To enable the backup operator for your active and passive hub clusters,
complete the following steps:

1.  Enable the cluster backup and restore operator, `cluster-backup`, by
    updating the `MultiClusterHub` resource and setting the
    `cluster-backup` parameter to `true`.

    1.  For the OpenShift APIs for Data Protection (OADP) operator
        installation, the automatic installation is the default. In this
        default situation, the OADP operator automatically installs in
        the same namespace where you enabled the `cluster-backup`
        component.

    2.  In certain cases, you must manually install the OADP operator.
        If your hub cluster runs on AWS cloud and uses AWS Security
        Token Service (STS) authentication, you must manually install
        the OADP operator before you enable the backup component. The
        STS configurations require an Amazon Resource Name (ARN) token
        that you must configure during the OADP operator installation.

2.  Ensure that the restore hub cluster uses the same Red Hat Advanced
    Cluster Management version that the backup hub cluster uses. You
    cannot restore a backup on a hub cluster with a version earlier than
    the one used by the backup hub cluster.

3.  Manually configure the restore hub cluster by completing the
    following steps:

    1.  Install all operators that are installed on the active hub
        cluster and in the same namespace as the active hub cluster.

    2.  Verify that the new hub cluster is configured the same way as
        the backup hub cluster.

    3.  Use the same namespace name as the backup hub cluster when you
        install the backup and restore operator and any operators that
        are configured on the backup hub cluster.

4.  Create the `DataProtectionApplication` resource on the passive hub
    cluster by completing the following steps:

    1.  Create the `DataProtectionApplication` resource on both the
        active and passive hub cluster.

    2.  For the restore hub cluster, when you create the
        `DataProtectionApplication` resource, use the same storage
        location as the backup hub.

#### Creating the storage location secret

To create a storage location secret, complete the following steps:

1.  Complete the steps for Creating a default Secret for the cloud
    storage where the backups are saved.

2.  Create the secret resource in the OADP Operator namespace, which is
    located in the backup component namespace.

#### Installing the OADP operator

For hub clusters where you enabled the AWS Security Token Service (STS)
option, the OADP operator is not installed when you installed the
cluster backup and restore operator on the hub cluster. To pass the STS
`role_arn` to the OADP operator, you must manually install the OADP
operator.

For hub clusters where you did not enable the STS option, the OADP
operator is automatically installed when you install the cluster backup
and restore operator on the hub cluster.

When you enable the backup option from the `MultiClusterHub` resource,
the backup option remains in the `Pending` state until you install the
OADP operator in the `open-cluster-management-backup` namespace. If you
have not enabled the AWS STS option on your hub cluster, then the OADP
operator is automatically installed with the backup chart. Otherwise,
you must manually install the OADP operator.

When the cluster is in the STS mode, the backup chart creates a config
map named `acm-redhat-oadp-operator-subscription` in the
`open-cluster-management-backup` namespace. This config map also
contains the OADP channel and environment information. Use this config
map to get the OADP version that you need to install and to get any
environment options to be set on the OADP subscription.

To learn more about installing the OADP operator with the STS option,
see Backing up workload on OADP ROSA, with an optional backup in the
OpenShift Container Platform documentation.

**Important:**

When you install the OADP operator, see the following notes:

- Custom resource definitions are cluster-scoped, so you cannot have two
  different versions of OADP or Velero installed on the same cluster. If
  you have two different versions, one version runs with the wrong
  custom resource definitions.

- When you create the `MultiClusterHub` resource, the Velero custom
  resource definitions (CRDs) do not automatically install on the hub
  cluster. When you install the OADP operator, the Velero CRDs are
  installed on the hub cluster. As a result, the Velero CRD resources
  are no longer reconciled and updated by the `MultiClusterHub`
  resource.

- The backup component works with the OADP Operator that is installed in
  the component namespace.

- If you manually install the OADP operator, the custom resource
  definition version of the OADP operator and Velereo must exactly
  match. If these versions do not exactly match one another, you get
  problems.

- Velero is installed with the OADP Operator on the Red Hat Advanced
  Cluster Management for Kubernetes hub cluster. It is used to backup
  and restore Red Hat Advanced Cluster Management hub cluster resources.

- For a list of supported storage providers for Velero, see About
  installing OADP.

#### Installing a custom OADP version

Setting an annotation on your `MultiClusterHub` resource allows you to
customize the OADP version for your specific needs. Complete the
following steps:

1.  To override the OADP version installed by the backup and restore
    operator, use the following annotation on the `MultiClusterHub`
    resource:

    ``` yaml
    installer.open-cluster-management.io/oadp-subscription-spec: '{"channel": "stable-1.4"}'
    ```

    **Important:** If you use this option to get a different OADP
    version than the one installed by default by the backup and restore
    operator, make sure this version is supported on the Red Hat
    OpenShift Container Platform version used by the hub cluster. Use
    this override option with caution because it can result in
    unsupported configurations.

2.  **Optional:** To install a specific OADP version of the operator,
    set your annotation. For example, if you want to install OADP from
    the `stable-1.5` channel and select a specific version of the
    operator, set the `startingCSV` property on the
    `installer.open-cluster-management.io/oadp-subscription-spec`
    annotation. Your `MultiClusterHub` resource might resemble the
    following example:

    ``` yaml
    apiVersion: operator.open-cluster-management.io/v1
    kind: MultiClusterHub
    metadata:
      annotations:
        installer.open-cluster-management.io/oadp-subscription-spec: '{"channel": "stable-1.5","installPlanApproval": "Automatic","name":
          "redhat-oadp-operator","source": "redhat-operators","sourceNamespace": "openshift-marketplace" "startingCSV": “oadp-operator.v5.0.2”}'
      name: multiclusterhub
    spec: {}
    ```

3.  Enable the `cluster-backup` option on the `MultiClusterHub` resource
    by setting `cluster-back` to `true`.

4.  To verify that the OADP operator uses the `oadp-subscription-spec`
    annotation properties, confirm that the subscription YAML for the
    OADP operator includes the properties that are specified by the
    annotation.

#### Creating a *DataProtectionApplication* resource

To create an instance of the `DataProtectionApplication` resource for
your active and passive hub clusters, complete the following steps:

1.  From the Red Hat OpenShift Container Platform console, select
    **Operators** \> **Installed Operators**.

2.  Click `Create instance` under DataProtectionApplication.

3.  Create the Velero instance by selecting configurations using the
    OpenShift Container Platform console or by using a YAML file as
    mentioned in the `DataProtectionApplication` example.

4.  Set the `DataProtectionApplication` namespace to
    `open-cluster-management-backup`.

5.  Set the specification (`spec:`) values appropriately for the
    `DataProtectionApplication` resource. Then click **Create**.

    If you intend on using the default backup storage location, set the
    following value, `default: true` in the `backupStorageLocations`
    section. View the following `DataProtectionApplication` resource
    sample:

    ``` yaml
    apiVersion: oadp.openshift.io/v1alpha1
    kind: DataProtectionApplication
    metadata:
      name: dpa-sample
    spec:
      configuration:
        velero:
          defaultPlugins:
          - openshift
          - aws
        restic:
          enable: true
      backupLocations:
        - name: default
          velero:
            provider: aws
            default: true
            objectStorage:
              bucket: my-bucket
              prefix: my-prefix
            config:
              region: us-east-1
              profile: "default"
            credential:
              name: cloud-credentials
              key: cloud
      snapshotLocations:
        - name: default
          velero:
            provider: aws
            config:
              region: us-west-2
              profile: "default"
    ```

#### Enabling the backup and restore component in a disconnected environment

To enable the backup and restore component with Red Hat OpenShift
Container Platform in a disconnected environment, complete the following
steps:

1.  Update the `MultiClusterHub` resource with the following annotation
    to override the source from which the OADP operator is installed.
    Create the annotation before the `cluster-backup` component is
    enabled on the `MultiClusterHub` resource:

    ``` yaml
    apiVersion: operator.open-cluster-management.io/v1
    kind: MultiClusterHub
    metadata:
      annotations:
        installer.open-cluster-management.io/oadp-subscription-spec: '{"source": "redhat-operator-index"}'
    ```

2.  The `redhat-operator-index` is a custom name and represents the name
    of the `CatalogSource` resource that you define and use to access
    Red Hat OpenShift Operators in the disconnected environment. Run the
    following command to retrieve the `catalogsource`:

    ``` bash
    oc get catalogsource -A
    ```

    The output might resemble the following:

    ``` bash
    NAMESPACE               NAME                         DISPLAY                       TYPE   PUBLISHER   AGE
    openshift-marketplace   acm-custom-registry          Advanced Cluster Management   grpc   Red Hat     42h
    openshift-marketplace   multiclusterengine-catalog   MultiCluster Engine           grpc   Red Hat     42h
    openshift-marketplace   redhat-operator-index                                      grpc               42h
    ```

#### Enabling the backup and restore operator

The cluster backup and restore operator can be enabled when the
`MultiClusterHub` resource is created for the first time. The
`cluster-backup` parameter is set to `true`. When the operator is
enabled, the operator resources are installed.

If the `MultiClusterHub` resource is already created, you can install or
uninstall the cluster backup operator by editing the `MultiClusterHub`
resource. Set `cluster-backup` to `false`, if you want to uninstall the
cluster backup operator.

When the backup and restore operator is enabled, your `MultiClusterHub`
resource might resemble the following YAML file:

``` yaml
apiVersion: operator.open-cluster-management.io/v1
  kind: MultiClusterHub
  metadata:
    name: multiclusterhub
    namespace: open-cluster-management
  spec:
    availabilityConfig: High
    enableClusterBackup: false
    imagePullSecret: multiclusterhub-operator-pull-secret
    ingress:
      sslCiphers:
        - ECDHE-ECDSA-AES256-GCM-SHA384
        - ECDHE-RSA-AES256-GCM-SHA384
        - ECDHE-ECDSA-AES128-GCM-SHA256
        - ECDHE-RSA-AES128-GCM-SHA256
    overrides:
      components:
        - enabled: true
          name: multiclusterhub-repo
        - enabled: true
          name: search
        - enabled: true
          name: management-ingress
        - enabled: true
          name: console
        - enabled: true
          name: insights
        - enabled: true
          name: grc
        - enabled: true
          name: cluster-lifecycle
        - enabled: true
          name: volsync
        - enabled: true
          name: multicluster-engine
        - enabled: true
          name: cluster-backup
    separateCertificateManagement: false
```

### Scheduling backups

By scheduling a backup, you help ensure your data remains protected and
accessible. Complete the following steps to schedule backups:

1.  Run the following command to create a
    `backupschedule.cluster.open-cluster-management.io` resource:

    ``` bash
    oc create -f cluster_v1beta1_backupschedule.yaml
    ```

    Your `cluster_v1beta1_backupschedule.yaml` resource might resemble
    the following file:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: BackupSchedule
    metadata:
      name: schedule-acm
      namespace: open-cluster-management-backup
    spec:
      veleroSchedule: 0 */2 * * * 
      veleroTtl: 120h 
      useManagedServiceAccount: true 
      paused: false 
    ```

    - The `veleroSchedule` is a required property and defines a cron job
      for scheduling the backups. In the earlier example, it creates a
      backup every 2 hours.

    - **Optional:** `veleroTtl` is an optional property and defines the
      expiration time for a scheduled backup resource. If not specified,
      the maximum default value set by Velero is used, which is `720h`.
      It deletes scheduled backups after `120h`.

    - **Optional:** `useManagedServiceAccount` is an optional property
      which can enable the automatic import feature, importing clusters
      in a restore operation. If you set it to `true`, it enables the
      automatic import feature, importing clusters in a restore
      operation.

    - **Optional:** `paused` is an optional property which can pause the
      backup schedule. If you set it to `true`, it pauses the backup
      schedule, deleting all Velero schedules created by this resource.

2.  Check the status of your
    `backupschedule.cluster.open-cluster-management.io` resource, which
    displays the definition for the three `schedule.velero.io`
    resources. Run the following command:

    ``` bash
    oc get BackupSchedule -n open-cluster-management-backup
    ```

3.  As a reminder, the restore operation is run on a different hub
    cluster for restore scenarios. To initiate a restore operation,
    create a `restore.cluster.open-cluster-management.io` resource on
    the hub cluster where you want to restore backups.

    **Note:** When you restore a backup on a new hub cluster, make sure
    that you shut down the previous hub cluster where the backup was
    created. If it is running, the previous hub cluster tries to
    reimport the managed clusters as soon as the managed cluster
    reconciliation finds that the managed clusters are no longer
    available.

The `backupschedule.cluster.open-cluster-management.io` resource creates
six `schedule.velero.io` resources, which are used to generate backups.
Run the following command to view the list of the backups that are
scheduled:

    oc get schedules -A | grep acm

Resources are separately backed up in the groups as seen in the
following table:

- Resource: Credentials backup - Description: Backup file that stores
  Hive credentials, Red Hat Advanced Cluster Management, and
  user-created credentials and ConfigMaps.

- Resource: Resources backup - Description: Contains one backup for the
  Red Hat Advanced Cluster Management resources and one for generic
  resources. These resources use the
  cluster.open-cluster-management.io/backup label.

- Resource: ManagedClusters backup - Description: Contains only
  resources that activate the managed cluster connection to the hub
  cluster, where the backup is restored.

**Note:** The *resources backup* file contains managed cluster-specific
resources, but does not contain the subset of resources that connect
managed clusters to the hub cluster. The resources that connect managed
clusters are called activation resources and are contained in the
managed clusters backup. When you restore backups only for the
*credentials* and *resources* backup on a new hub cluster, the new hub
cluster shows all managed clusters that are created by using the Hive
API in a detached state. The managed clusters that are imported on the
primary hub cluster by using the import operation appear only when the
activation data is restored on the passive hub cluster. The managed
clusters are still connected to the original hub cluster that created
the backup files.

When the activation data is restored, only managed clusters created by
using the Hive API are automatically connected with the new hub cluster.
All other managed clusters appear in a *Pending* state. You need to
manually reattach them to the new cluster.

For descriptions of the various `BackupSchedule` statuses, see the
following table:

- BackupSchedule status: Enabled - Description: The BackupSchedule is
  running and generating backups.

- BackupSchedule status: FailedValidation - Description: An error
  prevents the BackupSchedule from running. As a result, the
  BackupSchedule is not generating backups, but instead, it is
  reconciling and waiting for the error to be fixed. Look at the
  BackupSchedule status section for the reason why the resource is not
  valid. After the error is addressed, the BackupSchedule status changes
  to Enabled, and the resource starts generating backups.

- BackupSchedule status: BackupCollision - Description: The
  BackupSchedule is not generating backups. Look at the BackupSchedule
  status section for the reason why the resource status is
  BackupCollision. To start creating backups, delete this resource and
  create a new one.

- BackupSchedule status: Paused - Description: If you paused the Red Hat
  Advanced Cluster Management backup schedule by using the
  BackupSchedule.paused property, the Velero schedules created by the
  BackupSchedule resources get deleted and no new hub backups get
  generated. If you update the BackupSchedule.paused property to False,
  the BackupSchedule resource status returns to Enabled and the Velero
  schedules get recreated.

#### Understanding backup collisions

Backup collisions might occur if the hub cluster changes status from
passive to primary hub cluster, or from primary to passive, and
different hub clusters back up data at the same storage location.

As a result, the latest backups are generated by a hub cluster that is
no longer set as the primary hub cluster. This hub cluster still
produces backups because the
`BackupSchedule.cluster.open-cluster-management.io` resource is still
enabled.

When you run a restore operation in a controlled environment, such as a
disaster recovery test operation, you can prevent a backup collision
when you use the `BackupSchedule` `paused` property on the backup hub
cluster. Before you restore the resources on the new hub cluster, pause
the `BackupSchedule` resource on the backup hub by setting the
`paused=true` property on the `BackupSchedule` resource.

See the following list to learn about two scenarios that might cause a
backup collision:

1.  The primary hub cluster fails unexpectedly, which is caused by the
    following conditions:

    - Communication from the primary hub cluster to the initial hub
      cluster fails.

    - The initial hub cluster backup data is restored on a secondary hub
      cluster, called secondary hub cluster.

    - The administrator creates the
      `BackupSchedule.cluster.open-cluster-management.io` resource on
      the secondary hub cluster, which is now the primary hub cluster
      and generates backup data to the common storage location.

    - The initial hub cluster unexpectedly starts working again.

      Since the `BackupSchedule.cluster.open-cluster-management.io`
      resource is still enabled on the initial hub cluster, the initial
      hub cluster resumes writing backups to the same storage location
      as the secondary hub cluster. Both hub clusters are now writing
      backup data at the same storage location. Any hub cluster
      restoring the latest backups from this storage location might use
      the initial hub cluster data instead of the secondary hub cluster
      data.

2.  The administrator tests a disaster scenario by making the secondary
    hub cluster a primary hub cluster, which is caused by the following
    conditions:

    - The initial hub cluster is stopped.

    - The initial hub cluster backup data is restored on the secondary
      hub cluster.

    - The administrator creates the
      `BackupSchedule.cluster.open-cluster-management.io` resource on
      the secondary hub cluster, which is now the primary hub cluster
      and generates backup data to the common storage location.

    - After the disaster test is completed, the administrator reverts to
      the earlier state and makes the initial hub cluster the primary
      hub cluster again.

    - The initial hub cluster starts while the secondary hub cluster is
      still active.

      Since the `BackupSchedule.cluster.open-cluster-management.io`
      resource is still enabled on the secondary hub cluster, it writes
      backups at the same storage location that corrupts the backup
      data. Any hub cluster that restores the latest backups from this
      location might use the secondary hub cluster data instead of the
      initial hub cluster data. In this scenario, stop the secondary hub
      cluster first or pause the
      `BackupSchedule.cluster.open-cluster-management.io` resource on
      the secondary hub cluster before you start the initial hub cluster
      to avoid the backup collision issue.

3.  The administrator tests a disaster scenario by making the secondary
    hub cluster a primary hub cluster, without stopping the initial hub
    cluster first, causing the following conditions:

    - The initial hub cluster is still running.

    - The initial hub cluster backup data is restored on the secondary
      hub cluster, including managed clusters backup. Therefore, the
      secondary hub cluster is now the active cluster.

    - Since the `BackupSchedule.cluster.open-cluster-management.io`
      resource is still enabled on the initial hub cluster, it writes
      backups at the same storage location which corrupts the backup
      data. For example, any hub cluster restoring the latest backups
      from this location might use the initial hub cluster data instead
      of the secondary hub cluster data. To avoid data corruption, the
      initial hub cluster `BackupSchedule` resource status automatically
      changes to `BackupCollision`. In this scenario, to avoid getting
      into this backup collision state, stop the initial hub cluster
      first or delete the
      `BackupSchedule.cluster.open-cluster-management.io` resource on
      the initial hub cluster before restoring managed clusters data on
      the secondary hub cluster.

#### Preventing backup collisions

To prevent and report backup collisions, use the `BackupCollision` state
in the `BackupSchedule.cluster.open-cluster-management.io` resource. The
controller checks regularly if the latest backup in the storage location
has been generated from the current hub cluster. If not, a different hub
cluster has recently written backup data to the storage location,
indicating that the hub cluster is colliding with a different hub
cluster.

In the backup collision scenario, the current hub cluster
`BackupSchedule.cluster.open-cluster-management.io` resource status is
set to `BackupCollision`. To prevent data corruption, this resource
deletes the `Schedule.velero.io` resources. The backup policy reports
the `BackupCollision`.

In this same scenario, the administrator verifies which hub cluster
writes to the storage location. The administrator does this verification
before removing the `BackupSchedule.cluster.open-cluster-management.io`
resource from the invalid hub cluster. Then, the administrator can
create a new `BackupSchedule.cluster.open-cluster-management.io`
resource on the valid primary hub cluster, resuming the backup.

To check if there is a backup collision, run the following command:

    oc get backupschedule -A

If there is a backup collision, the output might resemble the following
example:

    NAMESPACE       NAME               PHASE             MESSAGE
    openshift-adp   schedule-hub-1   BackupCollision   Backup acm-resources-schedule-20220301234625, from cluster with id [be97a9eb-60b8-4511-805c-298e7c0898b3] is using the same storage location. This is a backup collision with current cluster [1f30bfe5-0588-441c-889e-eaf0ae55f941] backup. Review and resolve the collision then create a new BackupSchedule resource to  resume backups from this cluster.

### Restoring a backup

In a typical restore situation, the hub cluster where the backups run
becomes unavailable, and you need to move the backed up data to a new
hub cluster. Run the cluster restore operation on the new hub cluster.
In this case, the restore operation runs on a different hub cluster than
where the backup is created.

If you want to restore the data on the same hub cluster where the backup
was collected, recover the data from an earlier snapshot. In this case,
both restore and backup operations run on the same hub cluster.

#### Using the restore operation for backup types

Use the restore operation to restore all three backup types that the
backup operation creates. Choose to install only a certain type of
backup, such as only managed clusters, only user credentials, or only
hub cluster resources.

The restore defines the following three required `spec` properties,
where the restore logic is defined for the types of backed up files:

- `veleroManagedClustersBackupName` is used to define the restore option
  for the managed clusters activation resources.

- `veleroCredentialsBackupName` is used to define the restore option for
  the user credentials.

- `veleroResourcesBackupName` is used to define the restore option for
  the hub cluster resources (`Applications`, `Policy`, and other hub
  cluster resources like managed cluster passive data).

  The valid options for the previously mentioned properties are
  following values:

  - `latest` - This property restores the last available backup file for
    this type of backup.

  - `skip` - This property does not attempt to restore this type of
    backup with the current restore operation.

  - `<backup_name>` - This property restores the specified backup
    pointing to it by name.

The name of the `restore.velero.io` resources that are created by the
`restore.cluster.open-cluster-management.io` is generated using the
following template rule,
`<restore.cluster.open-cluster-management.io name>-<velero-backup-resource-name>`.
View the following descriptions:

- `restore.cluster.open-cluster-management.io name` is the name of the
  current `restore.cluster.open-cluster-management.io` resource, which
  initiates the restore.

- `velero-backup-resource-name` is the name of the Velero backup file
  that is used for restoring the data. For example, the
  `restore.cluster.open-cluster-management.io` resource named
  `restore-acm` creates `restore.velero.io` restore resources. View the
  following examples for the format:

  - `restore-acm-acm-managed-clusters-schedule-20210902205438` is used
    for restoring managed cluster activation data backups. In this
    sample, the `backup.velero.io` backup name used to restore the
    resource is `acm-managed-clusters-schedule-20210902205438`.

  - `restore-acm-acm-credentials-schedule-20210902206789` is used for
    restoring credential backups. In this sample, the `backup.velero.io`
    backup name used to restore the resource is
    `acm-managed-clusters-schedule-20210902206789`.

  - `restore-acm-acm-resources-schedule-20210902201234` is used for
    restoring application, policy, and other hub cluster resources like
    managed cluster passive data backups. In this sample, the
    `backup.velero.io` backup name used to restore the resource is
    `acm-managed-clusters-schedule-20210902201234`.

**Note:** If `skip` is used for a backup type, `restore.velero.io` is
not created.

View the following YAML sample of the cluster `Restore` resource. In
this sample, all three types of backed up files are being restored,
using the latest available backed up files:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Restore
metadata:
  name: restore-acm
  namespace: open-cluster-management-backup
spec:
  veleroManagedClustersBackupName: latest
  veleroCredentialsBackupName: latest
  veleroResourcesBackupName: latest
```

**Note:** Only managed clusters created by the Hive API are
automatically connected with the new hub cluster when the
`acm-managed-clusters` backup from the managed clusters backup is
restored on another hub cluster. All other managed clusters remain in
the `Pending Import` state and must be imported back onto the new hub
cluster. For more information, see Restoring imported managed clusters.

#### Preparing the new hub cluster

To restore a hub cluster and ensure that it is the same as the initial
hub cluster, use a new hub cluster when you run the hub restore
operation.

When you use a new hub cluster, you prevent any pre-existing user data
from interfering with the restoration. You also ensure that the new hub
cluster only has the backup data, making the cluster the same as the
initial hub cluster.

In a disaster recovery simulation, you might need to return back to your
initial hub cluster instead of using a new hub cluster. To return to
your initial hub cluster, complete the steps in Returning to the primary
hub cluster.

**Important:** To prevent managed clusters from switching back and forth
between the old and new hub clusters, stop the initial hub cluster
before running the restore operation and the new cluster becomes the
active hub cluster. To keep the initial hub cluster active during or
after the restore operation, complete the steps in Preparing the primary
hub cluster.

Before running the restore operation on a new hub cluster, you need to
manually configure the hub cluster and install the same operators as on
the initial hub cluster. You must install the Red Hat Advanced Cluster
Management operator in the same namespace as the initial hub cluster,
create the *DataProtectionApplication* resource, and then connect to the
same storage location where the initial hub cluster previously backed up
data.

Use the same configuration as on the initial hub cluster for the
`MultiClusterHub` resource created by the Red Hat Advanced Cluster
Management operator, including any changes to the `MultiClusterEngine`
resource.

For example, if the initial hub cluster has any other operators
installed, such as Ansible Automation Platform, Red Hat OpenShift
GitOps, `cert-manager`, you have to install them before running the
restore operation. This ensures that the new hub cluster is configured
in the same way as the initial hub cluster.

#### Running a restore operation on a hub cluster with a newer version

Run the restore operation on the hub cluster that uses the same Red Hat
Advanced Cluster Management operator version as the hub cluster where
you backed up the data. If you want to run the restore operation on a
hub cluster that uses a newer Red Hat Advanced Cluster Management
operator version, complete the following steps:

1.  On the restore hub cluster, install the Red Hat Advanced Cluster
    Management operator at the same version as the hub cluster where you
    created the backup.

2.  Restore the backup data on the restore hub cluster.

3.  On the restore hub cluster, use the upgrade operation to upgrade to
    the Red Hat Advanced Cluster Managementoperator version that you
    want to use.

#### Cleaning the hub cluster after restore

Velero updates existing resources if they have changed with the
currently restored backup. Velero does not clean up delta resources,
which are resources created by a previous restore and not part of the
currently restored backup. This limits the scenarios you can use when
restoring hub cluster data on a new hub cluster. Unless the restore is
applied only once, you cannot reliably use the new hub cluster as a
passive configuration. The data on the hub cluster does not reflect the
data available with the restored resources.

To address this limitation, when a
`Restore.cluster.open-cluster-management.io` resource is created, the
backup operator runs a post restore operation that cleans up the hub
cluster. The operation removes any resources created by a previous Red
Hat Advanced Cluster Management restore that are not part of the
currently restored backup.

The post restore cleanup uses the `cleanupBeforeRestore` property to
identify the subset of objects to clean up. You can use the following
options for the post restore cleanup:

- `None`: No clean up necessary, just begin Velero restore. Use `None`
  on a brand new hub cluster.

- `CleanupRestored`: Clean up all resources created by a previous Red
  Hat Advanced Cluster Management restore that are not part of the
  currently restored backup.

- `CleanupAll`: Clean up all resources on the hub cluster that might be
  part of a Red Hat Advanced Cluster Management backup, even if they
  were not created as a result of a restore operation.

  **Important:** The `CleanupAll` option removes all hub cluster data,
  including the content that the user creates.

  **Important:** Always use the `cleanupBeforeRestore = None` to avoid
  losing restored resources that you filter out with the restore options
  `excludedResource`, `excludedNamespaces`, `excludedResources`, or
  other options that filter out the restored resources.

  **Best Practice:** Avoid using the `CleanupAll` option. Only use it as
  a last resort with extreme caution. `CleanupAll` also cleans up
  resources on the hub cluster created by the user, in addition to
  resources created by a previously restored backup. Instead, use the
  `CleanupRestored` option to prevent updating the hub cluster content
  when the hub cluster is designated as a passive candidate for a
  disaster scenario. Use a clean hub cluster as a passive cluster.

**Notes:**

- Velero sets the status, `PartiallyFailed`, for a velero restore
  resource if the restored backup has no resources. This means that a
  `restore.cluster.open-cluster-management.io` resource can be in
  `PartiallyFailed` status if any of the created `restore.velero.io`
  resources do not restore any resources because the corresponding
  backup is empty.

- The `restore.cluster.open-cluster-management.io` resource is run once,
  unless you use the `syncRestoreWithNewBackups:true` to keep restoring
  passive data when new backups are available. For this case, follow the
  restore passive with sync sample. See Restoring passive resources
  while checking for backups. After the restore operation is complete
  and you want to run another restore operation on the same hub cluster,
  you have to create a new `restore.cluster.open-cluster-management.io`
  resource.

- Although you can create multiple
  `restore.cluster.open-cluster-management.io` resources, only one can
  be active at any moment in time.

#### Restoring passive resources while checking for backups

Use the `restore-passive-sync` sample to restore passive data, while
continuing to check if new backups are available and restore them
automatically. To automatically restore new backups, you must set the
`syncRestoreWithNewBackups` parameter to `true`. You must also only
restore the latest passive data. You can find the sample example at the
end of this section.

Set the `VeleroResourcesBackupName` and `VeleroCredentialsBackupName`
parameters to `latest`, and the `VeleroManagedClustersBackupName`
parameter to `skip`. Immediately after the
`VeleroManagedClustersBackupName` is set to `latest`, the managed
clusters are activated on the new hub cluster and is now the primary hub
cluster.

When the activated managed cluster becomes the primary hub cluster, the
restore resource is set to `Finished` and the
`syncRestoreWithNewBackups` is ignored, even if set to `true`.

By default, the controller checks for new backups every 30 minutes when
the `syncRestoreWithNewBackups` is set to `true`. If new backups are
found, it restores the backed up resources. You can change the duration
of the check by updating the `restoreSyncInterval` parameter.

If you want to run the same restore operation again after the restore
operation is complete, you must create a new
`restore.cluster.open-cluster-management.io` resource with the same
`spec` options.

For example, see the following resource that checks for backups every 10
minutes:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Restore
metadata:
  name: restore-acm-passive-sync
  namespace: open-cluster-management-backup
spec:
  syncRestoreWithNewBackups: true # restore again when new backups are available
  restoreSyncInterval: 10m # check for new backups every 10 minutes
  cleanupBeforeRestore: CleanupRestored
  veleroManagedClustersBackupName: skip
  veleroCredentialsBackupName: latest
  veleroResourcesBackupName: latest
```

#### Restoring passive resources

Use the `restore-acm-passive` sample to restore hub cluster resources in
a passive configuration. Passive data is backup data such as secrets,
ConfigMaps, applications, policies, and all the managed cluster custom
resources, which do not activate a connection between managed clusters
and hub clusters. The backup resources are restored on the hub cluster
by the credentials backup and restore resources.

See the following sample:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Restore
metadata:
  name: restore-acm-passive
  namespace: open-cluster-management-backup
spec:
  cleanupBeforeRestore: CleanupRestored
  veleroManagedClustersBackupName: skip
  veleroCredentialsBackupName: latest
  veleroResourcesBackupName: latest
```

#### Restoring activation resources

Before you restore the activation data on the passive hub cluster, shut
down the previous hub cluster where the backup was created. If the
primary hub cluster is still running, it attempts to reconnect with the
managed clusters that are no longer available, based on the
reconciliation procedure running on this hub cluster.

Use the `restore-acm-passive-activate` sample when you want the hub
cluster to manage the clusters. In this case it is assumed that the
other data has been restored already on the hub cluster that using the
passive resource.

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Restore
metadata:
  name: restore-acm-passive-activate
  namespace: open-cluster-management-backup
spec:
  cleanupBeforeRestore: CleanupRestored
  veleroManagedClustersBackupName: latest
  veleroCredentialsBackupName: skip
  veleroResourcesBackupName: skip
```

You have some options to restore activation resources, depending on how
you restored the passive resources:

- If you used the
  `restore-acm-passive-sync cluster.open-cluster-management.io` resource
  as documented in the *Restore passive resources while checking for
  backups to restore passive data* section, update the
  `veleroManagedClustersBackupName` value to `latest` on this resource.
  As a result, the managed cluster resources and the
  `restore-acm-passive-sync` resource are restored.

- If you restored the passive resources as a one time operation, or did
  not restore any resources yet, choose to restore all resources as
  specified in the *Restoring all resources* section.

#### Restoring managed cluster activation data

Managed cluster activation data or other activation data resources are
stored by the managed clusters backup and by the resource-generic
backups, when you use the
`cluster.open-cluster-management.io/backup: cluster-activation` label.
When the activation data is restored on a new hub cluster, managed
clusters are being actively managed by the hub cluster where the restore
is run. See *Scheduling and restoring backups* to learn how you can use
the operator.

#### Restoring all resources

To restore all the data, use the following `restore-acm` sample:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Restore
metadata:
  name: restore-acm
  namespace: open-cluster-management-backup
spec:
  cleanupBeforeRestore: None
  veleroManagedClustersBackupName: latest
  veleroCredentialsBackupName: latest
  veleroResourcesBackupName: latest
```

After you create the `restore.cluster.open-cluster-management.io`
resource on the hub cluster, get the status of the restore operation by
running the following command:

``` bash
oc describe -n open-cluster-management-backup restore-acm
```

#### Restoring imported managed clusters

Only managed clusters connected with the primary hub cluster using the
Hive API are automatically connected with the new hub cluster, where the
activation data is restored. These clusters have been created on the
primary hub cluster by the Hive API, using the **Create cluster** button
in the **Clusters** tab or through the CLI. Managed clusters connected
with the initial hub cluster using the **Import cluster** button appear
as `Pending Import` when the activation data is restored, and must be
imported back on the new hub cluster.

The Hive managed clusters can be connected with the new hub cluster
because Hive stores the managed cluster `kubeconfig` in the managed
cluster namespace on the hub cluster. This is backed up and restored on
the new hub cluster. The import controller then updates the bootstrap
`kubeconfig` on the managed cluster using the restored configuration,
which is only available for managed clusters created using the Hive API.
It is not available for imported clusters.

To reconnect imported clusters on the new hub cluster during a restore
operation, enable the automatic import feature on the `BackupSchedule`.
For more information, see Enabling automatic import.

#### Using other restore samples

View the following YAML examples to restore different types of backed up
files:

- Restore all three types of backed up resources:

  ``` yaml
  apiVersion: cluster.open-cluster-management.io/v1beta1
  kind: Restore
  metadata:
    name: restore-acm
    namespace: open-cluster-management-backup
  spec:
    veleroManagedClustersBackupSchedule: latest
    veleroCredentialsBackupSchedule: latest
    veleroResourcesBackupSchedule: latest
  ```

- Restore only managed cluster resources:

  ``` yaml
  apiVersion: cluster.open-cluster-management.io/v1beta1
  kind: Restore
  metadata:
    name: restore-acm
    namespace: open-cluster-management-backup
  spec:
    veleroManagedClustersBackupName: latest
    veleroCredentialsBackupName: skip
    veleroResourcesBackupName: skip
  ```

- Restore the resources for managed clusters only, using the
  `acm-managed-clusters-schedule-20210902205438` backup:

  ``` yaml
  apiVersion: cluster.open-cluster-management.io/v1beta1
  kind: Restore
  metadata:
    name: restore-acm
    namespace: open-cluster-management-backup
  spec:
    veleroManagedClustersBackupName: acm-managed-clusters-schedule-20210902205438
    veleroCredentialsBackupName: skip
    veleroResourcesBackupName: skip
  ```

  **Notes:**

  - The `restore.cluster.open-cluster-management.io` resource is still
    active if the phase is `Enabled` or `Running`. The resource run is
    completed if the phase changes to `Finished`. After the restore
    operation is completed, you can run another restore operation on the
    same hub cluster.

  - Only one `restore.cluster.open-cluster-management.io` can run at one
    time.

- Use the advanced options with `velero.io.restore` to filer out
  resources you want to restore. Use the following sample with
  `velero.io.restore` `spec` options to restore resources only from the
  `vb-managed-cls-2` managed cluster namespace and to exclude global
  `MultiCluster` resources:

  ``` yaml
  apiVersion: cluster.open-cluster-management.io/v1beta1
  kind: Restore
  metadata:
    name: restore-filter-sample
    namespace: open-cluster-management-backup
  spec:
    cleanupBeforeRestore: None
    veleroCredentialsBackupName: latest
    veleroResourcesBackupName: latest
    veleroManagedClustersBackupName: latest
  excludedResources:
    - ManagedCluster
  orLabelSelectors:
    - matchExpressions:
    - values:
    - vb-managed-cls-2
  key: name
  operator: In
  ```

- Set the following `velero.io.restore` `spec` options when you create
  the Red Hat Advanced Cluster Management restore resource:

  ``` yaml
  spec:
    includedResources
    includedNamespaces
    excludedResources
    excludedNamespaces
    LabelSelector
    OrLabelSelector
  ```

  **Note:**

  - When you set any of these Velero restore filters, set the
    `cleanupBeforeRestore` to `None` to avoid cleaning up hub cluster
    resources that are part of the restored backup but are not being
    restored because of the applied filter.

#### Using advanced restore options

There are advanced restore options that are defined by the
`velero.io.restore` specification. You can use these advanced restore
options to filter out resources that you want to restore.

For example, you can use the following YAML sample to restore resources
only from the `vb-managed-cls-2` managed cluster namespace and to
exclude the global `Managedluster` resources:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Restore
metadata:
  name: restore-filter-sample
  namespace: open-cluster-management-backup
spec:
  cleanupBeforeRestore: None
  veleroCredentialsBackupName: latest
  veleroResourcesBackupName: latest
  veleroManagedClustersBackupName: latest
  excludedResources:
    - ManagedCluster
  includedNamespaces:
    - vb-managed-cls-2
```

If you want more options for the `velero.io.restore` specification when
you create the Red Hat Advanced Cluster Management for Kubernetes
restore resource, see the following restore filters:

``` yaml
spec:
  includedResources
  includedNamespaces
  excludedResources
  excludedNamespaces
  LabelSelector
  OrLabelSelector
```

**Note:** For any of the Velero restore filters, set the
`cleanupBeforeRestore` field to `None` to prevent having to clean up hub
cluster resources that are part of the restored backup, but are not
being restored because of the applied filter.

#### Viewing restore events

Use the following command to get information about restore events:

    oc describe -n open-cluster-management-backup <restore-name>

Your list of events might resemble the following sample:

``` yaml
Spec:
  Cleanup Before Restore:               CleanupRestored
  Restore Sync Interval:                4m
  Sync Restore With New Backups:        true
  Velero Credentials Backup Name:       latest
  Velero Managed Clusters Backup Name:  skip
  Velero Resources Backup Name:         latest
Status:
  Last Message:                     Velero restores have run to completion, restore will continue to sync with new backups
  Phase:                            Enabled
  Velero Credentials Restore Name:  example-acm-credentials-schedule-20220406171919
  Velero Resources Restore Name:    example-acm-resources-schedule-20220406171920
Events:
  Type    Reason                   Age   From                Message
  ----    ------                   ----  ----                -------
  Normal  Prepare to restore:      76m   Restore controller  Cleaning up resources for backup acm-credentials-hive-schedule-20220406155817
  Normal  Prepare to restore:      76m   Restore controller  Cleaning up resources for backup acm-credentials-cluster-schedule-20220406155817
  Normal  Prepare to restore:      76m   Restore controller  Cleaning up resources for backup acm-credentials-schedule-20220406155817
  Normal  Prepare to restore:      76m   Restore controller  Cleaning up resources for backup acm-resources-generic-schedule-20220406155817
  Normal  Prepare to restore:      76m   Restore controller  Cleaning up resources for backup acm-resources-schedule-20220406155817
  Normal  Velero restore created:  74m   Restore controller  example-acm-credentials-schedule-20220406155817
  Normal  Velero restore created:  74m   Restore controller  example-acm-resources-generic-schedule-20220406155817
  Normal  Velero restore created:  74m   Restore controller  example-acm-resources-schedule-20220406155817
  Normal  Velero restore created:  74m   Restore controller  example-acm-credentials-cluster-schedule-20220406155817
  Normal  Velero restore created:  74m   Restore controller  example-acm-credentials-hive-schedule-20220406155817
  Normal  Prepare to restore:      64m   Restore controller  Cleaning up resources for backup acm-resources-schedule-20220406165328
  Normal  Prepare to restore:      62m   Restore controller  Cleaning up resources for backup acm-credentials-hive-schedule-20220406165328
  Normal  Prepare to restore:      62m   Restore controller  Cleaning up resources for backup acm-credentials-cluster-schedule-20220406165328
  Normal  Prepare to restore:      62m   Restore controller  Cleaning up resources for backup acm-credentials-schedule-20220406165328
  Normal  Prepare to restore:      62m   Restore controller  Cleaning up resources for backup acm-resources-generic-schedule-20220406165328
  Normal  Velero restore created:  61m   Restore controller  example-acm-credentials-cluster-schedule-20220406165328
  Normal  Velero restore created:  61m   Restore controller  example-acm-credentials-schedule-20220406165328
  Normal  Velero restore created:  61m   Restore controller  example-acm-resources-generic-schedule-20220406165328
  Normal  Velero restore created:  61m   Restore controller  example-acm-resources-schedule-20220406165328
  Normal  Velero restore created:  61m   Restore controller  example-acm-credentials-hive-schedule-20220406165328
  Normal  Prepare to restore:      38m   Restore controller  Cleaning up resources for backup acm-resources-generic-schedule-20220406171920
  Normal  Prepare to restore:      38m   Restore controller  Cleaning up resources for backup acm-resources-schedule-20220406171920
  Normal  Prepare to restore:      36m   Restore controller  Cleaning up resources for backup acm-credentials-hive-schedule-20220406171919
  Normal  Prepare to restore:      36m   Restore controller  Cleaning up resources for backup acm-credentials-cluster-schedule-20220406171919
  Normal  Prepare to restore:      36m   Restore controller  Cleaning up resources for backup acm-credentials-schedule-20220406171919
  Normal  Velero restore created:  36m   Restore controller  example-acm-credentials-cluster-schedule-20220406171919
  Normal  Velero restore created:  36m   Restore controller  example-acm-credentials-schedule-20220406171919
  Normal  Velero restore created:  36m   Restore controller  example-acm-resources-generic-schedule-20220406171920
  Normal  Velero restore created:  36m   Restore controller  example-acm-resources-schedule-20220406171920
  Normal  Velero restore created:  36m   Restore controller  example-acm-credentials-hive-schedule-20220406171919
```

### Connecting clusters for backup by using a ManagedServiceAccount

The backup controller automatically connects imported clusters to the
new hub cluster by using the Managed Service Account component. The
Managed Service Account creates a token that is backed up for each
imported cluster in each managed cluster namespace.

The token uses a `klusterlet-bootstrap-kubeconfig` `ClusterRole`
binding, allowing an automatic import operation to implement the token.
The `klusterlet-bootstrap-kubeconfig` `ClusterRole` can only get or
update the `bootstrap-hub-kubeconfig` secret.

When the activation data is restored on the new hub cluster, the restore
controller runs a post restore operation and looks for all managed
clusters in the `Pending Import` state. If a valid token generated by
the Managed Service Account is found, the controller creates an
`auto-import-secret` using the token that reconnects import component to
the managed cluster. If the cluster is accessible, the operation is
successful.

#### Enabling automatic import

The automatic import feature using the Managed Service Account component
is disabled by default. To enable the automatic import feature, complete
the following steps:

1.  Enable the Managed Service Account component by setting the
    `managedserviceaccount` `enabled` parameter to `true` in the
    `MultiClusterEngine` resource. See the following example:

    ``` yaml
    apiVersion: multicluster.openshift.io/v1
    kind: MultiClusterEngine
    metadata:
      name: multiclusterengine
    spec:
      overrides:
        components:
          - enabled: true
            name: managedserviceaccount
    ```

2.  Enable the automatic import feature for the
    `BackupSchedule.cluster.open-cluster-management.io` resource by
    setting the `useManagedServiceAccount` parameter to `true`. See the
    following example:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: BackupSchedule
    metadata:
      name: schedule-acm-msa
      namespace: open-cluster-management-backup
    spec:
      veleroSchedule:
      veleroTtl: 120h
      useManagedServiceAccount: true
    ```

    The default token validity duration is set to twice the value of
    `veleroTtl` to increase the chance of the token being valid for all
    backups storing the token for their entire lifecycle. In some cases,
    you might need to control how long a token is valid by setting a
    value for the optional `managedServiceAccountTTL` property.

    Use `managedServiceAccountTTL` with caution if you need to update
    the default token expiration time for the generated tokens. Changing
    the token expiration time from the default value might result in
    producing backups with tokens set to expire during the lifecycle of
    the backup. As a result, the import feature does not work for the
    managed clusters.

    **Important**: Do not use `managedServiceAccountTTL` unless you need
    to control how long the token is valid.

    See the following example for using the `managedServiceAccountTTL`
    property:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: BackupSchedule
    metadata:
      name: schedule-acm-msa
      namespace: open-cluster-management-backup
    spec:
      veleroSchedule:
      veleroTtl: 120h
      useManagedServiceAccount: true
      managedServiceAccountTTL: 300h
    ```

After you enable the automatic import feature, the backup component
starts processing imported managed clusters by creating the following:

- A `ManagedServiceAddon` named `managed-serviceaccount`.

- A `ManagedServiceAccount` named `auto-import-account`.

- A `ManifestWork` for each `ManagedServiceAccount` to set up a
  `klusterlet-bootstrap-kubeconfig` `RoleBinding` for the
  `ManagedServiceAccount` token on the managed cluster.

The token is only created if the managed cluster is accessible when you
create the Managed Service Account, otherwise it is created later once
the managed cluster becomes available.

#### Automatic import considerations

The following scenarios can prevent the managed cluster from being
automatically imported when moving to a new hub cluster:

- When running a hub backup without a `ManagedServiceAccount` token, for
  example when you create the `ManagedServiceAccount` resource while the
  managed cluster is not accessible, the backup does not contain a token
  to auto import the managed cluster.

- The auto import operation fails if the `auto-import-account` secret
  token is valid and is backed up but the restore operation is run when
  the token available with the backup has already expired. The
  `restore.cluster.open-cluster-management.io` resource reports invalid
  token issues for each managed cluster.

- Since the `auto-import-secret` created on restore uses the
  `ManagedServiceAccount` token to connect to the managed cluster, the
  managed cluster must also provide the kube `apiserver` information.
  The `apiserver` must be set on the `ManagedCluster` resource. See the
  following example:

  ``` yaml
  apiVersion: cluster.open-cluster-management.io/v1
  kind: ManagedCluster
  metadata:
    name: managed-cluster-name
  spec:
    hubAcceptsClient: true
    leaseDurationSeconds: 60
    managedClusterClientConfigs:
        url: <apiserver>
  ```

  When a cluster is imported on the hub cluster, the `apiserver` is only
  set up automatically on OpenShift Container Platform clusters. You
  must set the `apiserver` manually on other types of managed clusters,
  such as EKS clusters, otherwise the automatic import feature ignores
  the clusters. As a result, the clusters remain in the `Pending Import`
  state when you move them to the restore hub cluster.

- It is possible that a `ManagedServiceAccount` secret might not be
  included in a backup if the backup schedule runs before the backup
  label is set on the `ManagedServiceAccount` secret.
  `ManagedServiceAccount` secrets don’t have the cluster
  `open-cluster-management.io/backup` label set on creation. For this
  reason, the backup controller regularly searches for
  `ManagedServiceAccount` secrets under the managed cluster’s
  namespaces, and adds the backup label if not found.

#### Disabling automatic import

You can disable the automatic import cluster feature by setting the
`useManagedServiceAccount` parameter to `false` in the `BackupSchedule`
resource. See the following example:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: BackupSchedule
metadata:
  name: schedule-acm-msa
  namespace: open-cluster-management-backup
spec:
  veleroSchedule:
  veleroTtl: 120h
  useManagedServiceAccount: false
```

The default value is `false`. After setting the value to `false`, the
backup operator removes all created resources, including
`ManagedServiceAddon`, `ManagedServiceAccount`, and `ManifestWork`.
Removing the resources deletes the automatic import token on the hub
cluster and managed cluster.

### Validating your backup or restore configurations

When you set the `cluster-backup` option to `true` on the
`MultiClusterHub` resource, multicluster engine operator installs the
cluster backup and restore operator Helm chart that is named the
`cluster-backup-chart`. This chart installs the `backup-restore-enabled`
and `backup-restore-auto-import` policies. Use these policies to view
information about issues with your backup and restore components.

**Important:** A hub cluster is automatically imported and self-managed
as the `local-cluster`. If you disable self-management by setting
`disableHubSelfManagement` to `true` on the `MultiClusterHub` resource,
the local cluster feature is disabled, the `backup-restore-enabled`
policy is not placed on the hub cluster, and the policy templates do not
produce any reports.

If a hub cluster is managed by a global hub cluster, or if it is
installed on a managed cluster instance, the self-management option is
disabled by setting the `disableHubSelfManagement` to `true`. In this
instance, you can still enable the `backup-restore-enabled` policy on
the hub cluster. Set the `is-hub=true` label on the `ManagedCluster`
resource that represents the local cluster.

The `backup-restore-enabled` policy includes a set of templates that
check for the following constraints:

- **OADP channel validation**

  - When you enable the backup component on the `MultiClusterHub`, the
    cluster backup and restore operator Helm chart can automatically
    install the OADP operator in the `open-cluster-management-backup`
    namespace. You can also manually install the OADP operator in the
    namespace.

  - The `OADP-channel` that you selected for manual installation must
    match or exceed the version set by the Red Hat Advanced Cluster
    Management backup and restore operator Helm chart.

  - Since the OADP Operator and Velero Custom Resource Definitions
    (CRDs) are `cluster-scoped`, you cannot have multiple versions on
    the same cluster. You must install the same version in the
    `open-cluster-management-backup` namespace and any other namespaces.

  - Use the following templates to check for availability and validate
    the OADP installation:

    - `oadp-operator-exists`: Use this template to verify if the OADP
      operator is installed in the `open-cluster-management-backup`
      namespace.

    - `oadp-channel-validation`: Use this template to ensure the OADP
      operator version in the `open-cluster-management-backup` namespace
      matches or exceeds the version set by the Red Hat Advanced Cluster
      Management backup and restore operator.

    - `custom-oadp-channel-validation`: Use this template to check if
      OADP operators in other namespaces match the version in the
      `open-cluster-management-backup` namespace.

- **Pod validation**

  The following templates check the pod status for the backup component
  and dependencies:

  - `acm-backup-pod-running` template checks if the backup and restore
    operator pod is running.

  - `oadp-pod-running` template checks if the OADP operator pod is
    running.

  - `velero-pod-running` template checks if the Velero pod is running.

- **Data Protection Application validation**

  - `data-protection-application-available` template checks if a
    `DataProtectioApplicatio.oadp.openshift.io` resource is created.
    This OADP resource sets up Velero configurations.

- **Backup storage validation**

  - `backup-storage-location-available` template checks if a
    `BackupStorageLocation.velero.io` resource is created and if the
    status value is `Available`. This implies that the connection to the
    backup storage is valid.

- **`BackupSchedule` collision validation**

  - `acm-backup-clusters-collision-report` template verifies that the
    status is not `BackupCollision`, if a
    `BackupSchedule.cluster.open-cluster-management.io` exists on the
    current hub cluster. This verifies that the current hub cluster is
    not in collision with any other hub cluster when you write backup
    data to the storage location.

    For a definition of the `BackupCollision`, see Preventing backup
    collisions.

- **`BackupSchedule` and restore status validation**

  - `acm-backup-phase-validation` template checks that the status is not
    in `Failed`, or `Empty` state, if a
    `BackupSchedule.cluster.open-cluster-management.io` exists on the
    current cluster. This ensures that if this cluster is the primary
    hub cluster and is generating backups, the
    `BackupSchedule.cluster.open-cluster-management.io` status is
    healthy.

  - The same template checks that the status is not in a `Failed`, or
    `Empty` state, if a `Restore.cluster.open-cluster-management.io`
    exists on the current cluster. This ensures that if this cluster is
    the secondary hub cluster and is restoring backups, the
    `Restore.cluster.open-cluster-management.io` status is healthy.

- **Backups exist validation**

  - `acm-managed-clusters-schedule-backups-available` template checks if
    `Backup.velero.io` resources are available at the location specified
    by the `BackupStorageLocation.velero.io`, and if the backups are
    created by a `BackupSchedule.cluster.open-cluster-management.io`
    resource. This validates that the backups have been run at least
    once, using the backup and restore operator.

- **Backups for completion**

  - An `acm-backup-in-progress-report` template checks if
    `Backup.velero.io` resources are stuck in the `InProgress` state.
    This validation is added because with a large number of resources,
    the velero pod restarts as the backup runs, and the backup stays in
    progress without proceeding to completion. During a normal backup,
    the backup resources are in progress at some point when it is run,
    but are not stuck and run to completion. It is normal to see the
    `acm-backup-in-progress-report` template report a warning during the
    time the schedule is running and backups are in progress.

- **Backup schedules generate backups on the primary hub cluster**

  - The `backup-schedule-cron-enabled` policy template notifies the hub
    cluster administrator that the primary hub cluster is not creating
    new backups. The policy shows that the
    `BackupSchedule.cluster.open-cluster-management.io` resource is
    disabled on the primary hub cluster or is not able to create
    scheduled backups.

  - The `backup-schedule-cron-enabled` policy template is in violation
    if the backup schedule on the primary hub cluster did not generate
    new backups when the `BackupSchedule` cron job definition expects
    new backups. This might happen if the `BackupSchedule` does not
    exist, is paused, or the `BackupSchedule` cron job property updated
    and the time to run the backups increased. The template is in
    violation until a new set of backups is created.

  - The template validation works in the following ways:

    - A `BackupSchedule.cluster.open-cluster-management.io` actively
      runs and saves new backups at the storage location. The
      `backup-schedule-cron-enabled` policy template completes this
      validation. The template checks that there is a `Backup.velero.io`
      with a `velero.io/schedule-name: acm-validation-policy-schedule`
      label at the storage location.

    - The `acm-validation-policy-schedule` backups are set to expire
      after you set a time for the backups cron schedule. If no cron job
      is running to create backups, the old
      `acm-validation-policy-schedule` backup is deleted because it
      expired and a new one is not created. As a result, if no
      `acm-validation-policy-schedule` backups exists, there are no
      active cron jobs generating backups.

The `backup-restore-auto-import` policy includes a set of templates that
check for the following constraints:

- **Auto import secret validation**

  - The `auto-import-account-secret` template checks whether a
    `ManagedServiceAccount` secret is created in the managed cluster
    namespaces other than the `<your-local-cluster-name>` namespace. The
    backup controller regularly scans for imported managed clusters. As
    soon as a managed cluster is discovered, the backup controller
    creates the `ManagedServiceAccount` resource in the managed cluster
    namespace. This process initiates token creation on the managed
    cluster. However, if the managed cluster is not accessible at the
    time of this operation, the `ManagedServiceAccount` is unable to
    create the token. For example, if the managed cluster is
    hibernating, it is unable to create the token. So, if a hub backup
    is executed during this period, the backup then lacks a token for
    auto-importing the managed cluster.

- **Auto import backup label validation**

  - The `auto-import-backup-label` template verifies the existence of a
    `ManagedServiceAccount` secret in the managed cluster namespaces
    other than the `<your-local-cluster-name>` namespace. If the
    template finds the `ManagedServiceAccount` secret, then the template
    enforces the `cluster.open-cluster-management.io/backup` label on
    the secret. This label is crucial for including the
    `ManagedServiceAccount` secrets in Red Hat Advanced Cluster
    Management backups.

#### Protecting data using server-side encryption

Server-side encryption is data encryption for the application or service
that receives the data at the storage location. The backup mechanism
itself does not encrypt data while in-transit (as it travels to and from
backup storage location), or at rest (while it is stored on disks at
backup storage location). Instead it relies on the native mechanisms in
the object and snapshot systems.

**Best practice**: Encrypt the data at the destination using the
available backup storage server-side encryption. The backup contains
resources, such as credentials and configuration files that need to be
encrypted when stored outside of the hub cluster.

You can use `serverSideEncryption` and `kmsKeyId` parameters to enable
encryption for the backups stored in Amazon S3. For more details, see
the *Backup Storage Location YAML*. The following sample specifies an
AWS KMS key ID when setting up the `DataProtectionApplication` resource:

``` yaml
spec:
  backupLocations:
    - velero:
        config:
          kmsKeyId: 502b409c-4da1-419f-a16e-eif453b3i49f
          profile: default
          region: us-east-1
```

Refer to *Velero supported storage providers* to find out about all of
the configurable parameters of other storage providers.

### Running the restore operation while the primary hub cluster is active

In a typical disaster recovery restore operation, the primary hub
cluster is inactive, and there is no conflict with the restore hub
cluster. You might need to keep the original hub cluster active during
or after your restore operation, for example, you would typically need
to do this if you run a disaster recovery simulation test.

When you restore data to a new hub cluster while your primary hub
cluster is still active, both hub clusters try to manage the same
cluster fleet. If the primary hub cluster takes control of the managed
clusters, it might override the policy or application changes that you
made to your new hub cluster.

#### Preparing the primary hub cluster

Before running the restore operation and keeping the hub cluster active,
you must prepare the primary hub cluster.

To prepare the primary hub cluster, complete the following steps:

1.  Pause the `BackupSchedule` resource by setting the `paused` property
    to `true`. See the following example:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: BackupSchedule
    metadata:
     name: schedule-acm-msa
     namespace: open-cluster-management-backup
    spec:
     veleroSchedule: 0 */1 * * *
     veleroTtl: 120h
     useManagedServiceAccount: true
     paused: true
    ```

    **Notes:** - If you do not pause the backup schedule on the primary
    hub cluster before continuing to the next step, you might back up
    the `ManagedCluster` resource with the
    `import.open-cluster-management.io/disable-auto-import` annotation
    set if a backup is running while the annotation is set on the
    resource.

    - If you back up the `ManagedCluster` resource with the
      `import.open-cluster-management.io/disable-auto-import`
      annotation, the managed cluster cannot automatically import when
      you restore the backup data on a new hub cluster.

2.  Tag the primary hub cluster resources with the backup annotation.
    Complete the following steps:

    1.  Create a file named `restore-acm.yaml`.

    2.  Add the following content to the file:

        ``` yaml
        apiVersion: cluster.open-cluster-management.io/v1beta1
        kind: Restore
        metadata:
         name: restore-acm
         namespace: open-cluster-management-backup
        spec:
         cleanupBeforeRestore: None
         veleroManagedClustersBackupName: latest
         veleroCredentialsBackupName: latest
         veleroResourcesBackupName: latest
        ```

    3.  Apply the file and run the restore operation by running the
        following command:

        ``` bash
        oc -f apply restore-acm.yaml
        ```

        **Note:** When you run the `Restore` resource, it tags all hub
        cluster resources that would be backed up if you enabled the
        `BackupSchedule`. The resources are tagged with the
        `velero.io/backup-name: backupName` label, where `backupName` is
        the name of the latest backup created by the primary hub
        cluster.

        As a result, any restore operation that runs on the primary
        cluster by using a `Restore` resource with the
        `cleanupBeforeRestore` option set to `CleanupRestored` processes
        these resources, and deletes all resources if they are not part
        of the latest backup.

3.  Disable the automatic import for managed clusters.

    1.  Set the following annotation on the `ManagedCluster` global
        resource for all managed clusters that you want to move to the
        restore hub cluster. By setting the annotation, you prevent the
        backup hub cluster from recovering any managed cluster after the
        managed cluster moves to the restore hub cluster:

    ``` yaml
    annotations:
       import.open-cluster-management.io/disable-auto-import: ''
    ```

#### Running the restore operation on the new hub cluster

After you prepare the primary hub cluster, run the restore operation on
the new hub cluster and move your managed clusters. The managed clusters
connect to the new hub cluster and do not move back to the initial hub
cluster because the automatic import feature is now disabled on the
backup hub cluster.

Run the restore operation on the new hub cluster by completing the
following steps:

1.  Add the following content the `restore-acm.yaml` file:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: Restore
    metadata:
     name: restore-acm
     namespace: open-cluster-management-backup
    spec:
     cleanupBeforeRestore: None
     veleroManagedClustersBackupName: latest
     veleroCredentialsBackupName: latest
     veleroResourcesBackupName: latest
    ```

    **Note:** Setting `veleroManagedClustersBackupName` to `latest`
    restores managed clusters and connects them with the secondary hub
    cluster.

2.  Apply the file and run the restore operation by running the
    following command:

    ``` bash
    oc -f apply restore-acm.yaml
    ```

#### Cleaning up managed cluster resources on the backup hub cluster

After the restore and after the managed clusters successfully connect to
the new hub cluster, clean up the managed cluster resources from the
initial backup hub cluster. If you want to restore the data to the
backup after your recovery test completes, skip cleaning the resources

To clean up the managed clusters from the backup hub cluster, complete
the following steps:

1.  Make sure that the managed cluster status is `Unknown` on the
    primary hub before deleting the `ManagedCluster` global resource. If
    the status is not `Unknown`, your workloads are uninstalled from the
    managed cluster.

2.  Decide if you want to remove the `ManagedCluster` global resource.
    Doing so deletes the managed cluster namespace.

3.  Delete the `ManagedCluster` global resource from the backup hub
    cluster for each of the managed clusters that you moved to the new
    hub cluster by using the restore operation.

**Important:**

- Make sure that the managed cluster status is `Unknown` on the primary
  hub before deleting the `ManagedCluster` global resource. If the
  status is not `Unknown`, your workloads are uninstalled from the
  managed cluster.

- Removing the `ManagedCluster` global resource also deletes the managed
  cluster namespace.

### Configuring Velero resource requests and limits

When you install the backup and restore operator, a
`DataProtectionApplication` resource is created to manage the Velero
deployment on the hub cluster.

The Velero pod is set to the default CPU and memory limits. If your
cluster backs up a large number of resources, you might need to update
the Velero resource requests and limits. If you do not update the
values, the Velero pod might fail due to an out-of-memory error.

#### Increasing resources to support more clusters

1.  Update the `DataProtectionApplication` resource and add the
    following `resourceAllocations` template. The following example
    works with 2000 clusters:

    ``` yaml
    apiVersion: oadp.openshift.io/v1alpha1
    kind: DataProtectionApplication
    metadata:
      name: velero
      namespace: open-cluster-management-backup
    spec:
    ...
      configuration:
    ...
        velero:
          podConfig:
            resourceAllocations:
              limits:
                cpu: "2"
                memory: 1Gi
              requests:
                cpu: 500m
                memory: 256Mi
    ```

### Scenarios when using an existing hub cluster as a restore hub cluster

If you use an existing hub cluster as a restore hub cluster with
resources that you created before the restore operation, consider the
following scenarios:

- The existing managed cluster might detach during the restore process.

- There might be more resources on the restore hub cluster than the
  backup hub cluster.

#### Existing managed clusters are detached during the restore process

If the hub cluster you plan to use for the restore operation already
manages clusters, and you run a restore operation with the
`cleanupBeforeRestore` option set to `CleanupRestored`, expect the
following outcomes:

- If the `ManagedCluster` resources are created by a restored backup,
  then the resources have the `velero.io/backup-name: backupName` label
  annotation set. If a user runs a restore operation and uses the
  `cleanupBeforeRestore=CleanupRestored` option, the managed clusters
  are detached from the hub cluster and workloads are cleaned up on
  these managed clusters.

- If a user created the `ManagedCluster` resources, then the resources
  do not have the `velero.io/backup-name: backupName` label annotation
  set. If you run a restore operation and use the
  `cleanupBeforeRestore=CleanupRestored` option, the managed cluster
  resources are not cleaned up even if the resources are not part of the
  current restored backup.

#### Restore hub cluster has more resources than the backup hub cluster

When you restore data on a hub cluster that includes user-created data,
and the `cleanupBeforeRestore` option is set to `CleanupRestored` for
the restore operation, that data is not cleaned up. This is because the
data is created by the user and not by an earlier restore.

Even when the user-created resources do not get cleaned up, you can
still use an existing hub cluster for a restore hub cluster
configuration. You can make the content in the backup and restore hub
cluster match one another. Tag the resources with the
`cluster.open-cluster-management.io/backup` label to make all the
user-created resources appear the same, as if they were generated by an
earlier restore operation.

To learn how to tag resources, complete Tagging user resources with the
backup label for more information.

### Tagging user resources with the backup label

When you use an existing hub cluster for a restore hub cluster
configuration, decide what user-created resource that you want to
include in the hub cluster, then tag that resource with the
`velero.io/backup-name: backupName` label. If you tag these resources
with the Velero annotation, it looks like the resources were generated
by an earlier restore.

Because of the Velero annotation, when you run a hub restore operation
and set the `cleanupBeforeRestore` option to `CleanupRestored` on the
restore resource, user resources that are not part of your current
restored backup would get cleaned up. As a result, you can restore hub
data on an existing cluster and produce a cluster that is the same as
the initial hub.

#### Prerequisites

- Review the scenarios of using an existing hub cluster as a restore hub
  cluster with resources that you created before the restore operation.
  See Scenarios when using an existing hub cluster as a restore hub
  cluster.

- On the restore hub cluster, update the `DataProtectionApplication`
  resource and set the storage location to a new, temporary location.
  You do not want to create the backup used to tag the restore hub
  cluster resources in the same storage location with the backup hub
  cluster.

- Before you tag the resources, make sure you set the storage location
  to a different location than the backup hub cluster.

#### Tagging resources with the velero label

To tag user created resources on the restore hub cluster with the
`velero.io/backup-name: backupName` label, on the restore hub cluster
complete the following steps:

1.  Create a `BackupSchedule` resource to generate a backup that has all
    these hub cluster resources by using the following YAML:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: BackupSchedule
    metadata:
      name: schedule-acm-msa
      namespace: open-cluster-management-backup
    spec:
      veleroSchedule: 0 */1 * * *
      veleroTtl: 120h
      useManagedServiceAccount: true
      paused: false
    ```

2.  Verify that the `BackupSchedule` created the hub cluster backup
    resources and the resource status is `Completed`.

3.  Pause the `BackupSchedule` schedule and stop generating backups by
    setting the property `paused=true` on the
    `schedule-acm-msa BackupSchedule`.

    **Note:** You cannot run a restore operation on the hub cluster if
    the `BackupSchedule` is enabled.

4.  Run a restore operation by using the following YAML:

    ``` yaml
    kind: Restore
    metadata:
      name: restore-acm
      namespace: open-cluster-management-backup
    spec:
      cleanupBeforeRestore: None
      veleroManagedClustersBackupName: latest
      veleroCredentialsBackupName: latest
      veleroResourcesBackupName: latest
      excludedResources: 
        - ManagedCluster
      excludedNamespaces: 
        - managed-cls-1
        - managed-cls-2
        - managed-cls-n
    ```

    - Resources that you want to exclude. For this example, managed
      cluster resources are excluded.

    - Namespaces that you want to exclude. For this example, managed
      cluster namespaces are excluded.

The operator goes through each resource that is part of the hub cluster
backup and tags it with the `velero.io/backup-name: backupName`, where
`backupName` is the name of the latest backup.

After you tag the resources, you can use the hub cluster as a restore
cluster. You can now restore the data from the primary hub cluster by
updating the `DataProtectionApplication` storage location to point to
the storage location of the backup hub cluster, so you can run a restore
operation that uses the hub cluster backup resources.

All the restore hub cluster resources are tagged with the
`velero.io/backup-name label`, so the hub clusters show as being
generated by an earlier restore. Therefore, any restore operation that
you run on the existing hub cluster using the `cleanupBeforeRestore`
option set to `CleanupRestored` cleans up the data that is not part of
the restored backup.

**Important:**

- If you have managed clusters on the restore hub cluster created by an
  earlier restore operation that are not part of the restored backup, do
  not use the restore operation with the `cleanupBeforeRestore` option
  set to `CleanupRestored`. Otherwise, the managed clusters on the
  restore hub cluster get detached from the hub cluster and the managed
  cluster resources are deleted.

- When there are more resources on the restore hub cluster than the
  backup hub cluster, you can use an existing hub cluster as a restore
  hub cluster in the following situations:

  - There are no managed clusters on this restore hub cluster.

  - There are managed clusters on the restore hub cluster and you do not
    expect the restore hub cluster user data to be the same with the one
    available with the restored backup.

  - The names of the managed clusters from the restore hub cluster do
    not collide with any of the managed cluster names from the backup
    hub cluster.

### Restoring data to the initial hub cluster

After you run a hub cluster disaster recovery simulation, you can
restore your data to the initial hub cluster, then use it as your
primary hub cluster.

When you conduct a disaster recovery operation test, you simulate a
primary hub cluster failure and restore its data to a new hub cluster,
verifying that your backup and restore process works. After your
disaster recovery test simulation completes, return to the primary hub
cluster and make it the active hub cluster that manages the cluster
fleet.

Complete the following sections to restore your data to the initial hub
cluster after running a disaster recovery simulation.

#### Preparing the primary hub cluster

To prepare the primary hub cluster to stay active during the restore
process, complete the following task, Running the restore operation
while the primary hub cluster is active.

#### Making the new hub cluster the active hub cluster

To begin the simulation, you must make the new hub cluster the active
hub cluster by completing the following steps:

1.  Run the restore operation on the new hub cluster to make it the
    active hub cluster.

2.  To verify that the managed clusters are now connected to the new hub
    cluster, check the status of the managed clusters from the cluster
    console.

3.  Run your disaster recovery simulation tests on the new hub cluster.

#### Returning to the primary hub cluster

After your disaster recovery tests finishes, complete the following
steps to return to the primary hub cluster and make it the active hub
cluster that manages the cluster fleet.

1.  Create a backup on the restore hub cluster by applying the following
    resource:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: BackupSchedule
    metadata:
     name: schedule-acm-msa
     namespace: open-cluster-management-backup
    spec:
     veleroSchedule: "0 */1 * * *"
     veleroTtl: 120h
     useManagedServiceAccount: true
     paused: false
    ```

2.  Make sure the Red Hat Advanced Cluster Management backups are
    generated and have the `Completed` status.

3.  Pause the backup schedule by setting the `paused=true` property on
    the `schedule-acm-msa BackupSchedule` resource.

4.  To ensure the `ManagedCluster` resources do not connect back to the
    initial hub cluster after getting moved back to the primary hub
    cluster, add the
    `import.open-cluster-management.io/disable-auto-import: ''`
    annotation to all `ManagedCluster` resources.

5.  Restore all the resources from the secondary hub cluster backup by
    applying the following restore resource:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: Restore
    metadata:
     name: restore-acm
     namespace: open-cluster-management-backup
    spec:
     cleanupBeforeRestore: CleanupRestored
     veleroManagedClustersBackupName: latest
     veleroCredentialsBackupName: latest
     veleroResourcesBackupName: latest
    ```

    **Note:** When you set the `cleanupBeforeRestore` property to
    `CleanupRestored`, a cleanup operation runs after all resources are
    restored. This cleanup operation removes any hub resource that is
    not part of the restored backup.

#### Enabling the backup schedule on the primary hub cluster

Now that the initial hub cluster is the primary hub cluster again,
enable the backup schedule on the primary hub cluster by completing the
following steps:

1.  Go to the primary hub cluster.

2.  Apply the following `BackupSchedule` resource:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: BackupSchedule
    metadata:
     name: schedule-acm-msa
     namespace: open-cluster-management-backup
    spec:
     veleroSchedule: "0 */1 * * *"
     veleroTtl: 120h
     useManagedServiceAccount: true
     paused: false
    ```

    **Note:** The second hub cluster can be used again as the secondary
    hub cluster in the `active-passive` configuration.

### Backup and restore for hosted control planes and hosted clusters

See the OpenShift Container Platform hosted control plane disaster
recovery documentation to help you install the OpenShift APIs for Data
Protection operator, create OpenShift APIs for Data Protection
resources, and use the OpenShift APIs for Data Protection to backup and
restore hosted clusters. Then, note the differences in the Red Hat
Advanced Cluster Management process.

See the following information for backing up and restoring hosted
clusters with Red Hat Advanced Cluster Management:

- Restore the hosted clusters before you restore the Red Hat Advanced
  Cluster Management hub cluster. For instructions, see OpenShift Hosted
  Control Plane Disaster Recovery documentation.

- For Red Hat Advanced Cluster Management, enable backup and restore and
  use the OpenShift APIs for Data Protection operator that is installed
  by the backup and restore component.

- OpenShift APIs for Data Protection resources, such as
  `DataProtectionApplication`, `BackupSchedule`, `Backup` and `Restore`
  for your hosted clusters, are created in the
  `open-cluster-management-backup` namespace.

- For more information, see the Overview of Hosted Cluster backup and
  restore process.

### Backup and restore configuration for Observability

The Observability service uses an S3-compatible object store to keep all
time-series data collected from managed clusters. Because Observability
is a stateful service, it is sensitive to active and passive backup
patterns. You must configure Oservability to ensure that your data stays
safe and keeps its continuity during the hub cluster migration or
backup.

**Notes:**

- When a managed cluster is detached from the primary hub cluster and
  reattached to the backup hub cluster, metrics are not collected. To
  help connect the metrics, you can script the cluster migration for
  large fleets.

- For product backup and restore, the Observability service
  automatically labels its resources with the
  `cluster.open-cluster-management.io/backup` label.

<!-- -->

- Resource type: ConfigMaps - Resource name:
  observability-metrics-custom-allowlist, thanos-ruler-custom-rules,
  alertmanager-config, policy-acs-central-status, Any ConfigMap labeled
  with grafana-custom-dashboard

- Resource type: Secrets - Resource name: thanos-object-storage,
  observability-server-ca-certs, observability-client-ca-certs,
  observability-server-certs, observability-grafana-certs,
  alertmanager-byo-ca, alertmanager-byo-cert, proxy-byo-ca,
  proxy-byo-cert

### Backing up and restoring Observability service

Backup and restore the Observability service to keep data safe and to
support continuity during the hub cluster migration or backup. To help
with disruption in metric data collection, use the same S3-compatible
object store for both the primary and backup hub clusters.

<div class="formalpara">

<div class="title">

Procedure

</div>

Complete the following steps to backup and restore the Observability
service:

</div>

1.  To ensure the Observability service recognizes the hub cluster as
    the `local-cluster`, a managed hub cluster, change the
    `spec.disableHubSelfManagement` parameter in the `MultiClusterHub`
    custom resource to `false`.

    **Note:** If you change the default name of your `local-cluster` to
    another value, the results appear within the changed local cluster
    name.

2.  To preserve the tenant ID of the `observatorium` resource as you
    manually back up and restore the `observatorium` resource, run the
    following command:

    ``` bash
    oc get observatorium -n open-cluster-management-observability -o yaml > observatorium-backup.yaml
    ```

3.  To backup the `observability` deployment, run the following command:

    ``` bash
    oc get mco observability -o yaml > mco-cr-backup.yaml
    ```

4.  Shut down the Thanos compactor on your primary hub cluster by
    running the following command:

    ``` bash
    oc scale statefulset observability-thanos-compact -n open-cluster-management-observability --replicas=0
    ```

    1.  Verify the compactor is not active by running the following
        command:

    ``` bash
    oc get pods observability-thanos-compact-0 -n open-cluster-management-observability
    ```

5.  Restore the `backup` resources such as the automatically backed-up
    ConfigMaps and Secrets listed in the backup and restore
    configuration for Observability.

6.  To preserve the tenant ID for maintaing continuity in the metrics
    ingestion and querying, restore the `observatorium` resource to the
    backup hub cluster. Run the following command:

    ``` bash
    oc apply -f observatorium-backup.yaml
    ```

7.  Apply the backed up `MultiClusterObservability` custom resource to
    start the Observability service on the new restored hub cluster. Run
    the following command:

    ``` bash
    oc apply -f mco-cr-backup.yaml
    ```

    The operator starts the Observability service and detects the
    existing `observatorium` resource, reusing the preserved tenant ID
    instead of creating a new one.

8.  Verify that the Observability service runs on your new hub cluster.
    Run the following command:

    ``` bash
    oc get pods -n open-cluster-management-observability
    ```

9.  Verify that the `observability-controller` `managedclusteraddon`
    does not have a status in the `DEGRADED` column, and that the
    `PROGRESSING` status is not set to `False`. Run the following
    command:

    ``` bash
    oc get managedclusteraddons -A | awk 'NR==1 || /observability-controller/
    ```

10. Verify metrics collection from your managed clusters by accesing
    Grafana.

11. Verify that your managed clusters are connected to your new hub
    cluster by checking for the `Available` status for each managed
    cluster.

12. Shut down the Observability service on your previous hub cluster by
    removing the resources. Run the following command:

    ``` bash
    oc delete mco observability
    ```

## VolSync persistent volume replication service

VolSync is a Kubernetes operator that enables asynchronous replication
of persistent volumes within a cluster, or across clusters with storage
types that are not otherwise compatible for replication. It uses the
Container Storage Interface (CSI) to overcome the compatibility
limitation. After deploying the VolSync operator in your environment,
you can leverage it to create and maintain copies of your persistent
data.

**Important:** VolSync only supports replicating persistent volume
claims with the `volumeMode` of `Filesystem`. If you do not select the
`volumeMode`, it defaults to `Filesystem`.

### Replicating persistent volumes with VolSync

You can use three supported methods to replicate persistent volumes with
VolSync, which depend on the number of synchronization locations that
you have: rsync, rsync-tls, restic, or Rclone.

#### Prerequisites

Before installing VolSync on your clusters, you must have the following
requirements:

- A configured Red Hat OpenShift Container Platform environment on a
  supported Red Hat Advanced Cluster Management hub cluster

- The storage driver that you use for your source persistent volume must
  be CSI-compatible and able to support snapshots.

- If you want to use the `rsync-tls` mover to replicate data between
  clusters, you must have the following requirements:

  - At least two managed clusters for the same Red Hat Advanced Cluster
    Management hub cluster

  - Network connectivity between the clusters that you are configuring
    with VolSync. If the clusters are not on the same network, you can
    configure the Submariner multicluster networking and service
    discovery and use the `ClusterIP` value for `ServiceType` to network
    the clusters, or use a load balancer with the `LoadBalancer` value
    for `ServiceType`.

#### Installing VolSync on the managed clusters

To enable VolSync to replicate the persistent volume claim on one
cluster to the persistent volume claim of another cluster, you must
install VolSync on both the source and the target managed clusters.

When you install VolSync from Red Hat Advanced Cluster Management on the
managed cluster, it gets installed into the `volsync-system` namespace
on the managed cluster. Doing this provides support for non-OpenShift
managed clusters.

If in an earlier Red Hat Advanced Cluster Management version, you
installed VolSync as an Operator Lifecycle Manager operator on an
OpenShift Container Platform managed cluster, then the VolSync Operator
Lifecycle Manager operator gets removed and replaced with the VolSync
deployment in the `volsync-system` namespace.

You can use either of two methods to install VolSync on two clusters in
your environment. You can either add a label to each of the managed
clusters in the hub cluster, or you can manually create and apply a
`ManagedClusterAddOn`, as they are described in the following sections:

##### Installing VolSync by using labels

To install VolSync on the managed cluster by adding a label.

- Complete the following steps from the Red Hat Advanced Cluster
  Management console:

  1.  Select one of the managed clusters from the `Clusters` page in the
      hub cluster console to view its details.

  2.  In the **Labels** field, add the following label:

          addons.open-cluster-management.io/volsync=true

      The VolSync service pod is installed on the managed cluster.

  3.  Add the same label the other managed cluster.

  4.  Run the following command on the hub to confirm that the VolSync
      operator is installed:

      ``` bash
      oc -n <managed-cluster-name> get ManagedClusterAddOn volsync
      ```

  5.  Verify that the command output shows that the
      `managedclusteraddon` has a `Ready` status.

  6.  Run the following command on the managed cluster to confirm that
      the VolSync operator is installed:

          kubectl -n volsync-system get deployment volsync

- Complete the following steps from the command-line interface:

  1.  Start a command-line session on the hub cluster.

  2.  Enter the following command to add the label to the first cluster:

          oc label managedcluster <managed-cluster-1> "addons.open-cluster-management.io/volsync"="true"

      Replace `managed-cluster-1` with the name of one of your managed
      clusters.

  3.  Enter the following command to add the label to the second
      cluster:

          oc label managedcluster <managed-cluster-2> "addons.open-cluster-management.io/volsync"="true"

      Replace `managed-cluster-2` with the name of your other managed
      cluster.

      A `ManagedClusterAddOn` resource should be created automatically
      on your hub cluster in the namespace of each corresponding managed
      cluster.

##### Installing VolSync by using a ManagedClusterAddOn

To install VolSync on the managed cluster by adding a
`ManagedClusterAddOn` manually, complete the following steps:

1.  On the hub cluster, create a YAML file called `volsync-mcao.yaml`
    that contains content that is similar to the following example:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: ManagedClusterAddOn
    metadata:
      name: volsync
      namespace: <managed-cluster-1-namespace>
    spec: {}
    ```

    Replace `managed-cluster-1-namespace` with the namespace of one of
    your managed clusters. This namespace is the same as the name of the
    managed cluster.

    **Note:** The name must be `volsync`.

2.  Apply the file to your configuration by entering a command similar
    to the following example:

        oc apply -f volsync-mcao.yaml

3.  Repeat the procedure for the other managed cluster.

    A `ManagedClusterAddOn` resource should be created automatically on
    your hub cluster in the namespace of each corresponding managed
    cluster.

#### Configuring an Rsync-TLS replication

You can create a 1:1 asynchronous replication of persistent volumes by
using an Rsync-TLS replication. You can use Rsync-TLS-based replication
for disaster recovery or sending data to a remote site. When using
Rsync-TLS, VolSync synchronizes data by using Rsync across a
TLS-protected tunnel provided by stunnel. See the stunnel documentation
for more information.

The following example shows how to configure by using the Rsync-TLS
method. For additional information about Rsync-TLS, see Usage in the
VolSync documentation.

##### Configuring Rsync-TLS replication across managed clusters

For Rsync-TLS-based replication, configure custom resources on the
source and destination clusters. The custom resources use the `address`
value to connect the source to the destination, and a TLS-protected
tunnel provided by stunnel to ensure that the transferred data is
secure.

See the following information and examples to configure an Rsync-TLS
replication from a persistent volume claim on the `source` cluster in
the `source-ns` namespace to a persistent volume claim on a
`destination` cluster in the `destination-ns` namespace. Replace the
values where necessary:

1.  Configure your destination cluster.

    1.  Run the following command on the destination cluster to create
        the namespace:

            oc create ns <destination-ns>

        Replace `destination-ns` with the namespace where your
        replication destination is located.

    2.  Create a new YAML file called `replication_destination` and copy
        the following content:

        ``` yaml
        apiVersion: volsync.backube/v1alpha1
        kind: ReplicationDestination
        metadata:
          name: <destination>
          namespace: <destination-ns>
        spec:
          rsyncTLS:
            serviceType: LoadBalancer 
            copyMethod: Snapshot
            capacity: 2Gi 
            accessModes: [ReadWriteOnce]
            storageClassName: gp2-csi
            volumeSnapshotClassName: csi-aws-vsc
        ```

        - For this example, the `ServiceType` value of `LoadBalancer` is
          used. The load balancer service is created by the source
          cluster to enable your source managed cluster to transfer
          information to a different destination managed cluster. You
          can use `ClusterIP` as the service type if your source and
          destinations are on the same cluster, or if you have
          Submariner network service configured. Note the address and
          the name of the secret to refer to when you configure the
          source cluster.Make sure that the `capacity` value matches the
          capacity of the persistent volume claim that is being
          replicated.

        - Make sure that the `capacity` value matches the capacity of
          the persistent volume claim that is being replicated.

          **Optional:** Specify the values of the `storageClassName` and
          `volumeSnapshotClassName` parameters if you are using a
          storage class and volume snapshot class name that are
          different than the default values for your environment.

    3.  Run the following command on the destination cluster to create
        the `replicationdestination` resource:

            oc create -n <destination-ns> -f replication_destination.yaml

        Replace `destination-ns` with the name of the namespace where
        your destination is located.

        After the `replicationdestination` resource is created, the
        following parameters and values are added to the resource:

        - Parameter: .status.rsyncTLS.address - Value: IP address of the
          destination cluster that is used to enable the source and
          destination clusters to communicate.

        - Parameter: .status.rsyncTLS.keySecret - Value: Name of the
          secret containing the TLS key that authenticates the
          connection with the source cluster.

    4.  Run the following command to copy the value of
        `.status.rsyncTLS.address` to use on the source cluster. Replace
        `destination` with the name of your replication destination
        custom resource. Replace `destination-ns` with the name of the
        namespace where your destination is located:

            ADDRESS=`oc get replicationdestination <destination> -n <destination-ns> --template={{.status.rsyncTLS.address}}`
            echo $ADDRESS

        The output appears similar to the following, which is for an
        Amazon Web Services environment:

            a831264645yhrjrjyer6f9e4a02eb2-5592c0b3d94dd376.elb.us-east-1.amazonaws.com

    5.  Run the following command to copy the name of the secret:

            KEYSECRET=`oc get replicationdestination <destination> -n <destination-ns> --template={{.status.rsyncTLS.keySecret}}`
            echo $KEYSECRET

        Replace `destination` with the name of your replication
        destination custom resource.

        Replace `destination-ns` with the name of the namespace where
        your destination is located.

        You will have to enter it on the source cluster when you
        configure the source. The output should be the name of your SSH
        keys secret file, which might resemble the following name:

            volsync-rsync-tls-destination-name

    6.  Copy the key secret from the destination cluster by entering the
        following command against the destination cluster:

            oc get secret -n <destination-ns> $KEYSECRET -o yaml > /tmp/secret.yaml

        Replace `destination-ns` with the namespace where your
        replication destination is located.

    7.  Open the secret file in the `vi` editor by entering the
        following command:

            vi /tmp/secret.yaml

    8.  In the open secret file on the destination cluster, make the
        following changes:

        - Change the namespace to the namespace of your source cluster.
          For this example, it is `source-ns`.

        - Remove the owner references (`.metadata.ownerReferences`).

    9.  On the source cluster, create the secret file by entering the
        following command on the source cluster:

            oc create -f /tmp/secret.yaml

2.  Identify the source persistent volume claim that you want to
    replicate.

    **Note:** The source persistent volume claim must be on a CSI
    storage class.

3.  Create the `ReplicationSource` items.

    1.  Create a new YAML file called `replication_source` on the source
        cluster and copy the following content:

        ``` yaml
        apiVersion: volsync.backube/v1alpha1
        kind: ReplicationSource
        metadata:
          name: <source> 
          namespace: <source-ns> 
        spec:
          sourcePVC: <persistent_volume_claim> 
          trigger:
            schedule: "*/3 * * * *" #/*
          rsyncTLS:
            keySecret: <mykeysecret> 
            address: <my.host.com> 
            copyMethod: Snapshot
            storageClassName: gp2-csi
            volumeSnapshotClassName: csi-aws-vsc
        ```

        - Replace `source` with the name for your replication source
          custom resource. See step *3-vi* of this procedure for
          instructions on how to replace this automatically.

        - Replace `source-ns` with the namespace of the persistent
          volume claim where your source is located. See step *3-vi* of
          this procedure for instructions on how to replace this
          automatically.

        - Replace `persistent_volume_claim` with the name of your source
          persistent volume claim.

        - Replace `mykeysecret` with the name of the secret that you
          copied from the destination cluster to the source cluster (the
          value of `$KEYSECRET`).

        - Replace `my.host.com` with the host address that you copied
          from the `.status.rsyncTLS.address` field of the
          `ReplicationDestination` when you configured it. You can find
          examples of `sed` commands in the next step.

          If your storage driver supports cloning, using `Clone` as the
          value for `copyMethod` might be a more streamlined process for
          the replication.

          **Optional:** Specify the values of the `storageClassName` and
          `volumeSnapshotClassName` parameters if you are using a
          storage class and volume snapshot class name that are
          different than the default values for your environment.

          You can now set up the synchronization method of the
          persistent volume.

    2.  On the source cluster, modify the `replication_source.yaml` file
        by replacing the value of the `address` and `keySecret` in the
        `ReplicationSource` object with the values that you noted from
        the destination cluster by entering the following commands:

            sed -i "s/<my.host.com>/$ADDRESS/g" replication_source.yaml
            sed -i "s/<mykeysecret>/$KEYSECRET/g" replication_source.yaml
            oc create -n <source> -f replication_source.yaml

        Replace `my.host.com` with the host address that you copied from
        the `.status.rsyncTLS.address` field of the
        `ReplicationDestination` when you configured it.

        Replace `keySecret` with the keys that you copied from the
        `.status.rsyncTLS.keySecret` field of the
        `ReplicationDestination` when you configured it.

        Replace `source` with the name of the persistent volume claim
        where your source is located.

        **Note:** You must create the file in the same namespace as the
        persistent volume claim that you want to replicate.

    3.  Verify that the replication completed by running the following
        command on the `ReplicationSource` object:

            oc describe ReplicationSource -n <source-ns> <source>

        Replace `source-ns` with the namespace of the persistent volume
        claim where your source is located.

        Replace `source` with the name of your replication source custom
        resource.

        If the replication was successful, the output should be similar
        to the following example:

            Status:
              Conditions:
                Last Transition Time:  2021-10-14T20:48:00Z
                Message:               Synchronization in-progress
                Reason:                SyncInProgress
                Status:                True
                Type:                  Synchronizing
                Last Transition Time:  2021-10-14T20:41:41Z
                Message:               Reconcile complete
                Reason:                ReconcileComplete
                Status:                True
                Type:                  Reconciled
              Last Sync Duration:      5m20.764642395s
              Last Sync Time:          2021-10-14T20:47:01Z
              Next Sync Time:          2021-10-14T20:48:00Z

        If the `Last Sync Time` has no time listed, then the replication
        is not complete.

You have a replica of your original persistent volume claim.

#### Configuring an Rsync replication

**Important:** Use Rsync-TLS instead of Rsync for enhanced security. By
using Rsync-TLS, you can avoid using elevated user permissions that are
not required for replicating persistent volumes.

You can create a 1:1 asynchronous replication of persistent volumes by
using an Rsync replication. You can use Rsync-based replication for
disaster recovery or sending data to a remote site.

The following example shows how to configure by using the Rsync method.

##### Configuring Rsync replication across managed clusters

For Rsync-based replication, configure custom resources on the source
and destination clusters. The custom resources use the `address` value
to connect the source to the destination, and the `sshKeys` to ensure
that the transferred data is secure.

**Note:** You must copy the values for `address` and `sshKeys` from the
destination to the source, so configure the destination before you
configure the source.

This example provides the steps to configure an Rsync replication from a
persistent volume claim on the `source` cluster in the `source-ns`
namespace to a persistent volume claim on a `destination` cluster in the
`destination-ns` namespace. You can replace those values with other
values, if necessary.

1.  Configure your destination cluster.

    1.  Run the following command on the destination cluster to create
        the namespace:

            oc create ns <destination-ns>

        Replace `destination-ns` with a name for the namespace that will
        contain your destination persistent volume claim.

    2.  Copy the following YAML content to create a new file called
        `replication_destination.yaml`:

        ``` yaml
        apiVersion: volsync.backube/v1alpha1
        kind: ReplicationDestination
        metadata:
          name: <destination>
          namespace: <destination-ns>
        spec:
          rsync:
            serviceType: LoadBalancer
            copyMethod: Snapshot
            capacity: 2Gi
            accessModes: [ReadWriteOnce]
            storageClassName: gp2-csi
            volumeSnapshotClassName: csi-aws-vsc
        ```

        **Note:** The `capacity` value should match the capacity of the
        persistent volume claim that is being replicated.

        Replace `destination` with the name of your replication
        destination CR.

        Replace `destination-ns` with the name of the namespace where
        your destination is located.

        For this example, the `ServiceType` value of `LoadBalancer` is
        used. The load balancer service is created by the source cluster
        to enable your source managed cluster to transfer information to
        a different destination managed cluster. You can use `ClusterIP`
        as the service type if your source and destinations are on the
        same cluster, or if you have Submariner network service
        configured. Note the address and the name of the secret to refer
        to when you configure the source cluster.

        The `storageClassName` and `volumeSnapshotClassName` are
        optional parameters. Specify the values for your environment,
        particularly if you are using a storage class and volume
        snapshot class name that are different than the default values
        for your environment.

    3.  Run the following command on the destination cluster to create
        the `replicationdestination` resource:

            oc create -n <destination-ns> -f replication_destination.yaml

        Replace `destination-ns` with the name of the namespace where
        your destination is located.

        After the `replicationdestination` resource is created,
        following parameters and values are added to the resource:

        - Parameter: .status.rsync.address - Value: IP address of the
          destination cluster that is used to enable the source and
          destination clusters to communicate.

        - Parameter: .status.rsync.sshKeys - Value: Name of the SSH key
          file that enables secure data transfer from the source cluster
          to the destination cluster.

    4.  Run the following command to copy the value of
        `.status.rsync.address` to use on the source cluster:

            ADDRESS=`oc get replicationdestination <destination> -n <destination-ns> --template={{.status.rsync.address}}`
            echo $ADDRESS

        Replace `destination` with the name of your replication
        destination custom resource.

        Replace `destination-ns` with the name of the namespace where
        your destination is located.

        The output should appear similar to the following output, which
        is for an Amazon Web Services environment:

            a831264645yhrjrjyer6f9e4a02eb2-5592c0b3d94dd376.elb.us-east-1.amazonaws.com

    5.  Run the following command to copy the name of the secret:

            SSHKEYS=`oc get replicationdestination <destination> -n <destination-ns> --template={{.status.rsync.sshKeys}}`
            echo $SSHKEYS

        Replace `destination` with the name of your replication
        destination custom resource.

        Replace `destination-ns` with the name of the namespace where
        your destination is located.

        You will have to enter it on the source cluster when you
        configure the source. The output should be the name of your SSH
        keys secret file, which might resemble the following name:

            volsync-rsync-dst-src-destination-name

    6.  Copy the SSH secret from the destination cluster by entering the
        following command against the destination cluster:

            oc get secret -n <destination-ns> $SSHKEYS -o yaml > /tmp/secret.yaml

        Replace `destination-ns` with the namespace of the persistent
        volume claim where your destination is located.

    7.  Open the secret file in the `vi` editor by entering the
        following command:

            vi /tmp/secret.yaml

    8.  In the open secret file on the destination cluster, make the
        following changes:

        - Change the namespace to the namespace of your source cluster.
          For this example, it is `source-ns`.

        - Remove the owner references (`.metadata.ownerReferences`).

    9.  On the source cluster, create the secret file by entering the
        following command on the source cluster:

            oc create -f /tmp/secret.yaml

2.  Identify the source persistent volume claim that you want to
    replicate.

    **Note:** The source persistent volume claim must be on a CSI
    storage class.

3.  Create the `ReplicationSource` items.

    1.  Copy the following YAML content to create a new file called
        `replication_source.yaml` on the source cluster:

        ``` yaml
        apiVersion: volsync.backube/v1alpha1
        kind: ReplicationSource
        metadata:
          name: <source>
          namespace: <source-ns>
        spec:
          sourcePVC: <persistent_volume_claim>
          trigger:
            schedule: "*/3 * * * *" #/*
          rsync:
            sshKeys: <mysshkeys>
            address: <my.host.com>
            copyMethod: Snapshot
            storageClassName: gp2-csi
            volumeSnapshotClassName: csi-aws-vsc
        ```

        Replace `source` with the name for your replication source
        custom resource. See step *3-vi* of this procedure for
        instructions on how to replace this automatically.

        Replace `source-ns` with the namespace of the persistent volume
        claim where your source is located. See step *3-vi* of this
        procedure for instructions on how to replace this automatically.

        Replace `persistent_volume_claim` with the name of your source
        persistent volume claim.

        Replace `mysshkeys` with the keys that you copied from the
        `.status.rsync.sshKeys` field of the `ReplicationDestination`
        when you configured it.

        Replace `my.host.com` with the host address that you copied from
        the `.status.rsync.address` field of the
        `ReplicationDestination` when you configured it.

        If your storage driver supports cloning, using `Clone` as the
        value for `copyMethod` might be a more streamlined process for
        the replication.

        `StorageClassName` and `volumeSnapshotClassName` are optional
        parameters. If you are using a storage class and volume snapshot
        class name that are different than the defaults for your
        environment, specify those values.

        You can now set up the synchronization method of the persistent
        volume.

    2.  On the source cluster, modify the `replication_source.yaml` file
        by replacing the value of the `address` and `sshKeys` in the
        `ReplicationSource` object with the values that you noted from
        the destination cluster by entering the following commands:

            sed -i "s/<my.host.com>/$ADDRESS/g" replication_source.yaml
            sed -i "s/<mysshkeys>/$SSHKEYS/g" replication_source.yaml
            oc create -n <source> -f replication_source.yaml

        Replace `my.host.com` with the host address that you copied from
        the `.status.rsync.address` field of the
        `ReplicationDestination` when you configured it.

        Replace `mysshkeys` with the keys that you copied from the
        `.status.rsync.sshKeys` field of the `ReplicationDestination`
        when you configured it.

        Replace `source` with the name of the persistent volume claim
        where your source is located.

        **Note:** You must create the file in the same namespace as the
        persistent volume claim that you want to replicate.

    3.  Verify that the replication completed by running the following
        command on the `ReplicationSource` object:

            oc describe ReplicationSource -n <source-ns> <source>

        Replace `source-ns` with the namespace of the persistent volume
        claim where your source is located.

        Replace `source` with the name of your replication source custom
        resource.

        If the replication was successful, the output should be similar
        to the following example:

            Status:
              Conditions:
                Last Transition Time:  2021-10-14T20:48:00Z
                Message:               Synchronization in-progress
                Reason:                SyncInProgress
                Status:                True
                Type:                  Synchronizing
                Last Transition Time:  2021-10-14T20:41:41Z
                Message:               Reconcile complete
                Reason:                ReconcileComplete
                Status:                True
                Type:                  Reconciled
              Last Sync Duration:      5m20.764642395s
              Last Sync Time:          2021-10-14T20:47:01Z
              Next Sync Time:          2021-10-14T20:48:00Z

        If the `Last Sync Time` has no time listed, then the replication
        is not complete.

You have a replica of your original persistent volume claim.

#### Configuring a restic backup

A restic-based backup copies a restic-based backup copy of the
persistent volume to a location that is specified in your
`restic-config.yaml` secret file. A restic backup does not synchronize
data between the clusters, but provides data backup.

Complete the following steps to configure a restic-based backup:

1.  Specify a repository where your backup images are stored by creating
    a secret that resembles the following YAML content:

    ``` yaml
    apiVersion: v1
    kind: Secret
    metadata:
      name: restic-config
    type: Opaque
    stringData:
      RESTIC_REPOSITORY: <my-restic-repository>
      RESTIC_PASSWORD: <my-restic-password>
      AWS_ACCESS_KEY_ID: access
      AWS_SECRET_ACCESS_KEY: password
    ```

    Replace `my-restic-repository` with the location of the S3 bucket
    repository where you want to store your backup files.

    Replace `my-restic-password` with the encryption key that is
    required to access the repository.

    Replace `access` and `password` with the credentials for your
    provider, if required.

    If you need to prepare a new repository, see Preparing a new
    repository for the procedure. If you use that procedure, skip the
    step that requires you to run the `restic init` command to
    initialize the repository. VolSync automatically initializes the
    repository during the first backup.

    **Important:** When backing up multiple persistent volume claims to
    the same S3 bucket, the path to the bucket must be unique for each
    persistent volume claim. Each persistent volume claim is backed up
    with a separate `ReplicationSource`, and each requires a separate
    restic-config secret.

    By sharing the same S3 bucket, each `ReplicationSource` has write
    access to the entire S3 bucket.

2.  Configure your backup policy by creating a `ReplicationSource`
    object that resembles the following YAML content:

    ``` yaml
    apiVersion: volsync.backube/v1alpha1
    kind: ReplicationSource
    metadata:
      name: mydata-backup
    spec:
      sourcePVC: <source>
      trigger:
        schedule: "*/30 * * * *" #\*
      restic:
        pruneIntervalDays: 14
        repository: <restic-config>
        retain:
          hourly: 6
          daily: 5
          weekly: 4
          monthly: 2
          yearly: 1
        copyMethod: Clone
      # The StorageClass to use when creating the PiT copy (same as source PVC if omitted)
      #storageClassName: my-sc-name
      # The VSC to use if the copy method is Snapshot (default if omitted)
      #volumeSnapshotClassName: my-vsc-name
    ```

    Replace `source` with the persistent volume claim that you are
    backing up.

    Replace the value for `schedule` with how often to run the backup.
    This example has the schedule for every 30 minutes. See Scheduling
    your synchronization for more information about setting up your
    schedule.

    Replace the value of `PruneIntervalDays` to the number of days that
    elapse between instances of repacking the data to save space. The
    prune operation can generate significant I/O traffic while it is
    running.

    Replace `restic-config` with the name of the secret that you created
    in step 1.

    Set the values for `retain` to your retention policy for the backed
    up images.

    Best practice: Use `Clone` for the value of `CopyMethod` to ensure
    that a point-in-time image is saved.

**Note:** Restic movers run without root permissions by default. If you
want to run restic movers as root, run the following command to add the
elevated permissions annotation to your namespace.

    oc annotate namespace <namespace> volsync.backube/privileged-movers=true

Replace `<namespace>` with the name of your namespace.

##### Restoring a restic backup

You can restore the copied data from a restic backup into a new
persistent volume claim. **Best practice:** Restore only one backup into
a new persistent volume claim. To restore the restic backup, complete
the following steps:

1.  Create a new persistent volume claim to contain the new data similar
    to the following example:

    ``` yaml
    kind: PersistentVolumeClaim
    apiVersion: v1
    metadata:
      name: <pvc-name>
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 3Gi
    ```

    Replace `pvc-name` with the name of the new persistent volume claim.

2.  Create a `ReplicationDestination` custom resource that resembles the
    following example to specify where to restore the data:

    ``` yaml
    apiVersion: volsync.backube/v1alpha1
    kind: ReplicationDestination
    metadata:
      name: <destination>
    spec:
      trigger:
        manual: restore-once
      restic:
        repository: <restic-repo>
        destinationPVC: <pvc-name>
        copyMethod: Direct
    ```

    Replace `destination` with the name of your replication destination
    CR.

    Replace `restic-repo` with the path to your repository where the
    source is stored.

    Replace `pvc-name` with the name of the new persistent volume claim
    where you want to restore the data. Use an existing persistent
    volume claim for this, rather than provisioning a new one.

The restore process only needs to be completed once, and this example
restores the most recent backup. For more information about restore
options, see Restore options in the VolSync documentation.

#### Configuring an Rclone replication

An Rclone backup copies a single persistent volume to multiple locations
by using Rclone through an intermediate object storage location, like
AWS S3. It can be helpful when distributing data to multiple locations.

Complete the following steps to configure an Rclone replication:

1.  Create a `ReplicationSource` custom resource that resembles the
    following example:

    ``` yaml
    apiVersion: volsync.backube/v1alpha1
    kind: ReplicationSource
    metadata:
      name: <source>
      namespace: <source-ns>
    spec:
      sourcePVC: <source-pvc>
      trigger:
        schedule: "*/6 * * * *" #\*
      rclone:
        rcloneConfigSection: <intermediate-s3-bucket>
        rcloneDestPath: <destination-bucket>
        rcloneConfig: <rclone-secret>
        copyMethod: Snapshot
        storageClassName: <my-sc-name>
        volumeSnapshotClassName: <my-vsc>
    ```

    Replace `source-pvc` with the name for your replication source
    custom resource.

    Replace `source-ns` with the namespace of the persistent volume
    claim where your source is located.

    Replace `source` with the persistent volume claim that you are
    replicating.

    Replace the value of `schedule` with how often to run the
    replication. This example has the schedule for every 6 minutes. This
    value must be within quotation marks. See Scheduling your
    synchronization for more information.

    Replace `intermediate-s3-bucket` with the path to the configuration
    section of the Rclone configuration file.

    Replace `destination-bucket` with the path to the object bucket
    where you want your replicated files copied.

    Replace `rclone-secret` with the name of the secret that contains
    your Rclone configuration information.

    Set the value for `copyMethod` as `Clone`, `Direct`, or `Snapshot`.
    This value specifies whether the point-in-time copy is generated,
    and if so, what method is used for generating it.

    Replace `my-sc-name` with the name of the storage class that you
    want to use for your point-in-time copy. If not specified, the
    storage class of the source volume is used.

    Replace `my-vsc` with the name of the `VolumeSnapshotClass` to use,
    if you specified `Snapshot` as your `copyMethod`. This is not
    required for other types of `copyMethod`.

2.  Create a `ReplicationDestination` custom resource that resembles the
    following example:

    ``` yaml
    apiVersion: volsync.backube/v1alpha1
    kind: ReplicationDestination
    metadata:
      name: database-destination
      namespace: dest
    spec:
      trigger:
        schedule: "3,9,15,21,27,33,39,45,51,57 * * * *" #/*
      rclone:
        rcloneConfigSection: <intermediate-s3-bucket>
        rcloneDestPath: <destination-bucket>
        rcloneConfig: <rclone-secret>
        copyMethod: Snapshot
        accessModes: [ReadWriteOnce]
        capacity: 10Gi
        storageClassName: <my-sc>
        volumeSnapshotClassName: <my-vsc>
    ```

    Replace the value for `schedule` with how often to move the
    replication to the destination. The schedules for the source and
    destination must be offset to allow the data to finish replicating
    before it is pulled from the destination. This example has the
    schedule for every 6 minutes, offset by 3 minutes. This value must
    be within quotation marks. See Scheduling your synchronization for
    more information about scheduling.

    Replace `intermediate-s3-bucket` with the path to the configuration
    section of the Rclone configuration file.

    Replace `destination-bucket` with the path to the object bucket
    where you want your replicated files copied.

    Replace `rclone-secret` with the name of the secret that contains
    your Rclone configuration information.

    Set the value for `copyMethod` as `Clone`, `Direct`, or `Snapshot`.
    This value specifies whether the point-in-time copy is generated,
    and if so, which method is used for generating it.

    The value for `accessModes` specifies the access modes for the
    persistent volume claim. Valid values are `ReadWriteOnce` or
    `ReadWriteMany`.

    The `capacity` specifies the size of the destination volume, which
    must be large enough to contain the incoming data.

    Replace `my-sc` with the name of the storage class that you want to
    use as the destination for your point-in-time copy. If not
    specified, the system storage class is used.

    Replace `my-vsc` with the name of the `VolumeSnapshotClass` to use,
    if you specified `Snapshot` as your `copyMethod`. This is not
    required for other types of `copyMethod`. If not included, the
    system default `VolumeSnapshotClass` is used.

**Note:** Rclone movers run without root permissions by default. If you
want to run Rclone movers as root, run the following command to add the
elevated permissions annotation to your namespace.

    oc annotate namespace <namespace> volsync.backube/privileged-movers=true

Replace `<namespace>` with the name of your namespace.

### Converting a replicated image to a usable persistent volume claim

You might need to convert the replicated image to a persistent volume
claim to recover data.

When you replicate or restore a pesistent volume claim from a
`ReplicationDestination` location by using a `VolumeSnapshot`, a
`VolumeSnapshot` is created. The `VolumeSnapshot` contains the
`latestImage` from the last successful synchronization. The copy of the
image must be converted to a persistent volume claim before it can be
used. The VolSync `ReplicationDestination` volume populator can be used
to convert a copy of the image to a usable persistent volume claim.

1.  Create a persistent volume claim with a `dataSourceRef` that
    references the `ReplicationDestination` where you want to restore a
    persistent volume claim. This persistent volume claim is populated
    with the contents of the `VolumeSnapshot` that is specified in the
    `status.latestImage` setting of the `ReplicationDestination` custom
    resource definition.

    The following YAML content shows a sample persistent volume claim
    that might be used:

    ``` yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: <pvc-name>
      namespace: <destination-ns>
    spec:
      accessModes:
        - ReadWriteOnce
      dataSourceRef:
        kind: ReplicationDestination
        apiGroup: volsync.backube
        name: <replicationdestination_to_replace>
      resources:
        requests:
          storage: 2Gi
    ```

    Replace `pvc-name` with a name for your new persistent volume claim.

    Replace `destination-ns` with the namespace where the persistent
    volume claim and `ReplicationDestination` are located.

    Replace `replicationdestination_to_replace` with the
    `ReplicationDestination` name.

    **Best practice:** You can update `resources.requests.storage` with
    a different value when the value is at least the same size as the
    initial source persistent volume claim.

2.  Validate that your persistent volume claim is running in the
    environment by entering the following command:

        $ kubectl get pvc -n <destination-ns>

**Note:**

If no `latestImage` exists, the persistent volume claim remains in a
pending state until the `ReplicationDestination` completes and a
snapshot is available. You can create a `ReplicationDestination` and a
persistent volume controller that use the `ReplicationDestination` at
the same time. The persistent volume claim only starts the volume
population process after the `ReplicationDestination` completed a
replication and a snapshot is available. You can find the snapshot in
`.status.latestImage`.

Additionally, if the storage class that is used has a
`volumeBindingMode` value of `WaitForFirstConsumer`, the volume
populator waits until there is a consumer of the persistent volume claim
before it is populated. When a consumer requires access, such as a pod
that wants to mount the persistent volume claim, then the volume is
populated. The VolSync volume populator controller uses the
`latestImage` from the `ReplicationDestination`. The `latestImage` is
updated each time a replication completes after the persistent volume
control was created.

### Scheduling your synchronization

Select from three options when determining how you start your
replications: always running, on a schedule, or manually. Scheduling
your replications is an option that is often selected.

The **Schedule** option runs replications at scheduled times. A schedule
is defined by a `cronspec`, so the schedule can be configured as
intervals of time or as specific times. The order of the schedule values
are:

`"minute (0-59) hour (0-23) day-of-month (1-31) month (1-12) day-of-week (0-6)"`

The replication starts when the scheduled time occurs. Your setting for
this replication option might resemble the following content:

``` yaml
spec:
  trigger:
    schedule: "*/6 * * * *"
```

After enabling one of these methods, your synchronization schedule runs
according to the method that you configured.

See the VolSync documentation for additional information and options.

### VolSync advanced configuration

You can further configure VolSync when replicating persistent volumes,
such as creating your own secret.

#### Creating a secret for Rsync-TLS replication

The source and destination must have access to the shared key for the
TLS connection. You can find the key location in the `keySecret` field.
If you do not provide a secret name in `.spec.rsyncTLS.keySecret`, the
secret name is automatically generated and added to
`.status.rsyncTLS.keySecret`.

To create your own secret, complete the following steps:

1.  Use the following format for the secret:
    `<id>:<at_least_32_hex_digits>`

    See the following example: `1:23b7395fafc3e842bd8ac0fe142e6ad1`

2.  See the following `secret.yaml` example which corresponds to the
    previous example:

    ``` yaml
    apiVersion: v1
    data:
      # echo -n 1:23b7395fafc3e842bd8ac0fe142e6ad1 | base64
      psk.txt: MToyM2I3Mzk1ZmFmYzNlODQyYmQ4YWMwZmUxNDJlNmFkMQ==
    kind: Secret
    metadata:
      name: tls-key-secret
    type: Opaque
    ```
