# Release notes for Red Hat Advanced Cluster Management

Learn about Red Hat Advanced Cluster Management 2.15 new features and
enhancements, support, deprecations, removals, and fixed issues for
errata releases.

**Important:** Cluster lifecycle components and features are within the
multicluster engine operator, which is a software operator that enhances
cluster fleet management. Release notes for multicluster engine
operator-specific features are found in at Release notes for Cluster
lifecycle with multicluster engine operator.

Access the Red Hat Advanced Cluster Management Support Matrix to learn
about hub cluster and managed cluster requirements and support for each
component. For lifecycle information, see Red Hat OpenShift Container
Platform Life Cycle policy.

**Important:** OpenShift Container Platform release notes are not
documented in this product documentation. For your OpenShift Container
Platform cluster, see OpenShift Container Platform release notes.

**Deprecated:** Red Hat Advanced Cluster Management 2.9 and earlier
versions are no longer supported. The documentation might remain
available, but without any errata releases for fixed issues or other
updates.

**Best practice:** Upgrade to the most recent version.

- The documentation references the earliest supported Red Hat OpenShift
  Container Platform versions, unless the component in the documentation
  is created and tested with only a specific version of OpenShift
  Container Platform.

- For full support information, see the Red Hat Advanced Cluster
  Management Support Matrix and the Lifecycle and update policies for
  Red Hat Advanced Cluster Management for Kubernetes.

- If you experience issues with one of the currently supported releases,
  or the product documentation, go to Red Hat Support where you can
  troubleshoot, view Knowledgebase articles, connect with the Support
  Team, or open a case. You must log in with your credentials.

- You can also learn more about the Customer Portal documentation at Red
  Hat Customer Portal FAQ.

## New features and enhancements for Red Hat Advanced Cluster Management

Red Hat Advanced Cluster Management for Kubernetes 2.15 provides
visibility of your entire Kubernetes domain with built-in governance,
cluster lifecycle management, and application lifecycle management with
GitOps, along with observability.

Red Hat Advanced Cluster Management version 2.15 is released with the
multicluster engine operator version 2.10 for Cluster lifecycle
management. To learn about cluster management this release, see the
Release notes for Cluster lifecycle with multicluster engine operator.

Access the Red Hat Advanced Cluster Management Support Matrix to learn
about hub cluster and managed cluster requirements and support for each
component. For lifecycle information, see Red Hat OpenShift Container
Platform Life Cycle policy.

**Important:**

- Red Hat Advanced Cluster Management supports all providers that are
  certified through the Cloud Native Computing Foundation (CNCF)
  Kubernetes Conformance Program. Choose a vendor that is recognized by
  CNCF for your hybrid cloud multicluster management. See the following
  information about using CNCF providers:

- Learn how CNCF providers are certified at Certified Kubernetes
  Conformance.

- For Red Hat support information about CNCF third-party providers, see
  Red Hat support with third party components, or Contact Red Hat
  support.

- If you bring your own CNCF conformance certified cluster, you need to
  change the OpenShift Container Platform CLI `oc` command to the
  Kubernetes CLI command, `kubectl`.

### General announcements for this release

Red Hat Advanced Cluster Management is now available on the AWS
Marketplace with either on-demand or annual pricing and a simplified
billing option for running Red Hat Advanced Cluster Management on Red
Hat OpenShift Service on AWS clusters. Red Hat Advanced Cluster
Management on the AWS Marketplace offers billing consistency, flexible
resource consumption, and cost efficiency.

### New features and enhancements for each component

Some features and components are identified and released as Technology
Preview.

### Installation

Learn about Red Hat Advanced Cluster Management installation features
and enhancements.

**Important:** multicluster engine operator installation release notes
are in the *Cluster lifecycle with multicluster engine operator*
documentation that is linked earlier in this topic.

- The Red Hat OpenShift Software Catalog replaces the earlier
  OperatorHub console. When you install an Red Hat Advanced Cluster
  Management Operator or an multicluster engine operator Operator, you
  select those operators from the new Red Hat OpenShift Software
  Catalog.

- The Red Hat Advanced Cluster Management upgrade process is improved to
  provide more accuracy and dependability for upgrading versions of
  OpenShift Container Platform on your hub cluster at the level of
  support that is required. See Upgrading your hub cluster from the
  console for more information about the upgrade process.

Learn about Red Hat Advanced Cluster Management advanced configuration
options at MultiClusterHub advanced configuration in the documentation.

### Console

Learn about what is new in the Red Hat Advanced Cluster Management
integrated console, which includes Search capability.

- For Argo CD `ApplicationSet` resources, you now can manually select
  **Sync** to reconcile your deployed applications and sources.

- Access Red Hat Advanced Cluster Management within the OpenShift
  Container Platform console from the perspective selector by selecting
  **Fleet Management**. For more information, see Accessing your
  console.

See Web console for more information about the Console.

### Clusters

For new features that are related to multicluster engine operator, see
New features and enhancements for Cluster lifecycle with multicluster
engine operator in the *Cluster* section of the documentation.

View other cluster management tasks and support information at Cluster
lifecycle with multicluster engine operator overview.

### multicluster global hub

Learn what is new for multicluster global hub this release.

### Applications

Learn about new features for application management.

### Observability

See Observability service to learn more.

### Governance

- With the Gatekeeper operator, you have new operator configurations,
  including separate options for changing webhooks. To learn more, see
  Configuring the Gatekeeper operator.

- You can use the `lookupClusterClaim` function to detect an empty
  string, which you can complete by adding in your preferred templating
  functions. For more information, see lookupClusterClaim.

- **Technology Preview:** Use the `--lint` argument when you resolve
  templates to display linting issues that the policy tool found in the
  policy.

- Enable the `--from-cluster` flag to test a policy against your actual
  cluster state without manually exporting and supporting resource
  files. For more information, see Policy command-line tool.

- See Governance to learn more about the dashboard and the policy
  framework.

### Business continuity

Learn about new features for *Back up and restore* and *VolSync*
components.

To learn about VolSync, which enables asynchronous replication of
persistent volumes within a cluster, see VolSync persistent volume
replication service

To learn about Backup and restore, see Backup and restore.

### Networking

See Networking.

### Virtualization

See Virtualization.

### Learn more about this release

See more information about the release, as well as support information
for the product.

## Fixed issues for Red Hat Advanced Cluster Management

By default, fixed issues for *errata* releases are automatically applied
when released. The details are published here when the release is
available. If no release notes are listed, the product does not have an
errata release at this time.

**Important:** For reference, Jira links and Jira numbers might be added
to the content and used internally. Links that require access might not
be available for the user. Learn about the types of errata releases from
Red Hat.

See Upgrading by using the operator for more information about upgrades.

**Important:** Cluster lifecycle components and features are within the
multicluster engine operator, which is a software operator that enhances
cluster fleet management. Release notes for multicluster engine
operator-specific features are found in at Release notes for Cluster
lifecycle with multicluster engine operator.

## Known issues Red Hat Advanced Cluster Management

Review the known issues for application management. The following list
contains known issues for this release, or known issues that continued
from the previous release.

**Important:** Cluster lifecycle components and features are within the
multicluster engine operator, which is a software operator that enhances
cluster fleet management. Release notes for multicluster engine
operator-specific features are found in at Release notes for Cluster
lifecycle with multicluster engine operator.

**Important:** OpenShift Container Platform release notes are not
documented in this product documentation. For your OpenShift Container
Platform cluster, see OpenShift Container Platform release notes.

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

### Installation known issues

Review the known issues for installing and upgrading. The following list
contains known issues for this release, or known issues that continued
from the previous release.

For your Red Hat OpenShift Container Platform cluster, see OpenShift
Container Platform known issues.

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

#### Uninstalling and reinstalling earlier versions with an upgrade can fail

Uninstalling Red Hat Advanced Cluster Management from OpenShift
Container Platform can cause issues if you later want to install earlier
versions and then upgrade. For instance, when you uninstall Red Hat
Advanced Cluster Management, then install an earlier version of Red Hat
Advanced Cluster Management and upgrade that version, the upgrade might
fail. The upgrade fails if the custom resources were not removed.

Follow the Cleaning up artifacts before reinstalling procedure to
prevent this problem.

ACM-14343

#### Cannot remove data image resources after a cluster reinstallation with Image-Based Break/Fix

If you change the `spec.nodes.<node-id>.bmcAddress` field while
reinstalling a cluster with the Image-Based Break/Fix, the SiteConfig
operator is unable to contact the original machine nd cannot delete the
data image resources from the original cluster. To work around this
issue, remove the finalizer from the data image resources before
reinstalling a cluster with Image-Based Break/Fix.

- To remove the finalizer from the data image resources, run the
  following command:

  ``` bash
  $ oc patch dataimages.metal3.io -n target-0 target-0-0 --patch '{"metadata":{"finalizers":[]}}' --type merge
  dataimage.metal3.io/target-0-0 patched
  ```

ACM-21889

### Business continuity known issues

Review the known issues for Red Hat Advanced Cluster Management for
Kubernetes. The following list contains known issues for this release,
or known issues that continued from the previous release.

For your Red Hat OpenShift Container Platform cluster, see OpenShift
Container Platform known issues.

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

#### Backup and restore known issues

Backup and restore known issues and limitations are listed here, along
with workarounds if they are available.

##### Velero restore limitations

A new hub cluster can have a different configuration than the active hub
cluster if the new hub cluster, where the data is restored, has
user-created resources. For example, this can include an existing policy
that was created on the new hub cluster before the backup data is
restored on the new hub cluster.

Velero skips existing resources if they are not part of the restored
backup, so the policy on the new hub cluster remains unchanged,
resulting in a different configuration between the new hub cluster and
active hub cluster.

To address this limitation, the cluster backup and restore operator runs
a post restore operation to clean up the resources created by the user
or a different restore operation when a
`restore.cluster.open-cluster-management.io` resource is created.

For more information, see the Cleaning the hub cluster after restore
topic.

ACM-21861

##### Passive configurations do not display managed clusters

Managed clusters are only displayed when the activation data is restored
on the passive hub cluster.

ACM-22098

##### Managed cluster resource not restored

When you restore the settings for the `local-cluster` managed cluster
resource and overwrite the `local-cluster` data on a new hub cluster,
the settings are misconfigured. Content from the previous hub cluster
`local-cluster` is not backed up because the resource contains
`local-cluster` specific information, such as the cluster URL details.

You must manually apply any configuration changes that are related to
the `local-cluster` resource on the restored cluster. See *Prepare the
new hub cluster* in the Installing the backup and restore operator
topic.

ACM-21054

##### Restored Hive managed clusters might not be able to connect with the new hub cluster

When you restore the backup of the changed or rotated certificate of
authority (CA) for the Hive managed cluster, on a new hub cluster, the
managed cluster fails to connect to the new hub cluster. The connection
fails because the `admin` `kubeconfig` secret for this managed cluster,
available with the backup, is no longer valid.

You must manually update the restored `admin` `kubeconfig` secret of the
managed cluster on the new hub cluster.

ACM-25461

##### Imported managed clusters show a *Pending Import* status

Managed clusters that are manually imported on the primary hub cluster
show a `Pending Import` status when the activation data is restored on
the passive hub cluster. For more information, see Connecting clusters
by using a Managed Service Account.

ACM-1890

##### The *appliedmanifestwork* is not removed from managed clusters after restoring the hub cluster

When the hub cluster data is restored on the new hub cluster, the
`appliedmanifestwork` is not removed from managed clusters that have a
placement rule for an application subscription that is not a fixed
cluster set.

See the following example of a placement rule for an application
subscription that is not a fixed cluster set:

``` yaml
spec:
  clusterReplicas: 1
  clusterSelector:
    matchLabels:
      environment: dev
```

As a result, the application is orphaned when the managed cluster is
detached from the restored hub cluster.

To avoid the issue, specify a fixed cluster set in the placement rule.
See the following example:

``` yaml
spec:
  clusterSelector:
    matchLabels:
      environment: dev
```

You can also delete the remaining `appliedmanifestwork` manually by
running the folowing command:

    oc delete appliedmanifestwork <the-left-appliedmanifestwork-name>

ACM-27129

#### Volsync known issues

##### Restoring the connection of a managed cluster with custom CA certificates to its restored hub cluster might fail

After you restore the backup of a hub cluster that manages a cluster
with custom CA certificates, the connection between the managed cluster
and the hub cluster might fail. This is because the CA certificate was
not backed up on the restored hub cluster. To restore the connection,
copy the custom CA certificate information that is in the namespace of
your managed cluster to the `<managed_cluster>-admin-kubeconfig` secret
on the restored hub cluster.

**Note:** If you copy this CA certificate to the hub cluster before
creating the backup copy, the backup copy includes the secret
information. When you use the backup copy to restore in the future, the
connection between the hub cluster and managed cluster automatically
completes.

ACM-19481

### Console known issues

Review the known issues for the console. The following list contains
known issues for this release, or known issues that continued from the
previous release.

For your Red Hat OpenShift Container Platform cluster, see OpenShift
Container Platform known issues.

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

#### *klusterlet-addon-search* pod fails

The `klusterlet-addon-search` pod fails because the memory limit is
reached. You must update the memory request and limit by customizing the
`klusterlet-addon-search` deployment on your managed cluster. Edit the
`ManagedclusterAddon` custom resource named `search-collector`, on your
hub cluster. Add the following annotations to the `search-collector` and
update the memory,
`addon.open-cluster-management.io/search_memory_request=512Mi` and
`addon.open-cluster-management.io/ search_memory_limit=1024Mi`.

For example, if you have a managed cluster named `foobar`, run the
following command to change the memory request to `512Mi` and the memory
limit to `1024Mi`:

    oc annotate managedclusteraddon search-collector -n foobar \
    addon.open-cluster-management.io/search_memory_request=512Mi \
    addon.open-cluster-management.io/search_memory_limit=1024Mi

ACM-27173

#### Search does not display node information from the managed cluster

Search maps RBAC for resources in the hub cluster. Depending on user
RBAC settings, users might not see node data from the managed cluster.
Results from search might be different from what is displayed on the
*Nodes* page for a cluster.

ACM-4598

#### Cannot upgrade OpenShift Dedicated in console

From the console you can request an upgrade for OpenShift Dedicated
clusters, but the upgrade fails with the
`Cannot upgrade non openshift cluster` error message. Currently there is
no workaround.

ACM-10143

#### Search PostgreSQL pod is in CrashLoopBackoff state

The `search-postgres` pod is in `CrashLoopBackoff` state. If Red Hat
Advanced Cluster Management is deployed in a cluster with nodes that
have the `hugepages` parameter enabled and the `search-postgres` pod
gets scheduled in these nodes, then the pod does not start.

Complete the following steps to increase the memory of the
`search-postgres` pod:

1.  Pause the `search-operator` pod with the following command:

    ``` bash
    oc annotate search search-v2-operator search-pause=true
    ```

2.  Update the `search-postgres` deployment with a limit for the
    `hugepages` parameter. Run the following command to set the
    `hugepages` parameter to `512Mi`:

    ``` bash
    oc patch deployment search-postgres --type json -p '[{"op": "add", "path": "/spec/template/spec/containers/0/resources/limits/hugepages-2Mi", "value":"512Mi"}]'
    ```

3.  Before you verify the memory usage for the pod, make sure your
    `search-postgres` pod is in the `Running` state. Run the following
    command:

    ``` bash
    oc get pod <your-postgres-pod-name>  -o jsonpath="Status: {.status.phase}"
    ```

4.  Run the following command to verify the memory usage of the
    `search-postgres` pod:

    ``` bash
    oc get pod <your-postgres-pod-name> -o jsonpath='{.spec.containers[0].resources.limits.hugepages-2Mi}'
    ```

The following value appears: `512Mi`.

ACM-7467

#### Cannot edit namespace bindings for cluster set

When you edit namespace bindings for a cluster set with the `admin` role
or `bind` role, you might encounter an error that resembles the
following message:

`ResourceError: managedclustersetbindings.cluster.open-cluster-management.io "<cluster-set>" is forbidden: User "<user>" cannot create/delete resource "managedclustersetbindings" in API group "cluster.open-cluster-management.io" in the namespace "<namespace>".`

To resolve the issue, make sure you also have permission to create or
delete a `ManagedClusterSetBinding` resource in the namespace you want
to bind. The role bindings only allow you to bind the cluster set to the
namespace.

ACM-25389

#### Horizontal scrolling does not work after provisioning hosted control plane cluster

After provisioning a hosted control plane cluster, you might not be able
to scroll horizontally in the cluster overview of the Red Hat Advanced
Cluster Management console if the `ClusterVersionUpgradeable` parameter
is too long. You cannot view the hidden data as a result.

To work around the issue, zoom out by using your browser zoom controls,
increase your Red Hat Advanced Cluster Management console window size,
or copy and paste the text to a different location.

ACM-27107

#### Issues with entering the *cluster-ID* in the OpenShift Cloud Manager console

If you did not access the `cluster-ID` in the OpenShift Cloud Manager
console, you can still get a description of your Red Hat OpenShift
Service on AWS `cluster-ID` from the terminal. You need the Red Hat
OpenShift Service on AWS command line interface. See Getting started
with the Red Hat OpenShift Service on AWS CLI documentation.

To get the `cluster-ID`, run the following command from the Red Hat
OpenShift Service on AWS command line interface:

``` bash
rosa describe cluster --cluster=<cluster-name> | grep -o ’^ID:.*
```

ACM-10651

### Cluster management known issues and limitations

Review the known issues for *Cluster management* with Red Hat Advanced
Cluster Management. The following list contains Known issues this
release, or known issues that continued from the previous release.

For Cluster management with the stand-alone multicluster engine operator
known issues and limitations, see Cluster lifecycle known issues and
limitations in the multicluster engine operator documentation.

#### Hub cluster communication limitations

The following limitations occur if the hub cluster is not able to reach
or communicate with the managed cluster:

- You cannot create a new managed cluster by using the console. You are
  still able to import a managed cluster manually by using the command
  line interface or by using the **Run import commands manually** option
  in the console.

- If you deploy an Application or ApplicationSet by using the console,
  or if you import a managed cluster into ArgoCD, the hub cluster ArgoCD
  controller calls the managed cluster API server. You can use AppSub or
  the ArgoCD pull model to work around the issue.

ACM-6292

#### The local-cluster might not be automatically recreated

If the local-cluster is deleted while `disableHubSelfManagement` is set
to `false`, the local-cluster is recreated by the `MulticlusterHub`
operator. After you detach a local-cluster, the local-cluster might not
be automatically recreated.

- To resolve this issue, modify a resource that is watched by the
  `MulticlusterHub` operator. See the following example:

      oc delete deployment multiclusterhub-repo -n <namespace>

- To properly detach the local-cluster, set the
  `disableHubSelfManagement` to true in the `MultiClusterHub`.

ACM-17790

#### Local-cluster status offline after reimporting with a different name

When you accidentally try to reimport the cluster named `local-cluster`
as a cluster with a different name, the status for `local-cluster` and
for the reimported cluster display `offline`.

To recover from this case, complete the following steps:

1.  Run the following command on the hub cluster to edit the setting for
    self-management of the hub cluster temporarily:

        oc edit mch -n open-cluster-management multiclusterhub

2.  Add the setting `spec.disableSelfManagement=true`.

3.  Run the following command on the hub cluster to delete and redeploy
    the local-cluster:

        oc delete managedcluster local-cluster

4.  Enter the following command to remove the `local-cluster` management
    setting:

        oc edit mch -n open-cluster-management multiclusterhub

5.  Remove `spec.disableSelfManagement=true` that you previously added.

ACM-16977

#### Hub cluster and managed clusters clock not synced

Hub cluster and manage cluster time might become out-of-sync, displaying
in the console `unknown` and eventually `available` within a few
minutes. Ensure that the OpenShift Container Platform hub cluster time
is configured correctly. See Customizing nodes.

ACM-5636

### Application known issues and limitations

Review the known issues for application management. The following list
contains known issues for this release, or known issues that continued
from the previous release.

For your Red Hat OpenShift Container Platform cluster, see OpenShift
Container Platform known issues.

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

See the following known issues for the Application lifecycle component.

#### Upgrading to Red Hat OpenShift GitOps 1.17 causes permission errors

When you upgrade your OpenShift GitOps operator to version 1.17, you get
permission errors in your `ApplicationSet` resource status.

To workaround this issue, complete the following steps:

1.  Go to the `openshift-gitops` namespace and delete the `RoleBinding`
    resource named
    `openshift-gitops-applicationset-controller-placement`.

2.  Restart the `multicluster-operators-application-\*\` pod in the
    `open-cluster-management` namespace.

ACM-23907

#### Subscription application displays incorrect warning message

When you deploy the Subscription application (Deprecated), it displays a
warning message for the Subscription node in the *Application Topology*
page. If you check the Subscription node details, it incorrectly shows
the `local-cluster` is offline.

Check the real status of the `local-cluster` by clicking
**Infrastructure** \> **Clusters** from the Console navigation.

ACM-18544

#### The console menu of the Application table can be difficult to click

When Application resources get updated in the hub cluster, the
Application page table also gets updated. If you have the menu of the
Application table opened, then it gets closed with every update to the
Application page table. Because the menu can close often, it can be
difficult for you to click the menu.

To workaround this issue, click the Application name to go to the
Application details page where you can click the same action menu
without it closing with every update.

ACM-18543

#### Application topology displays invalid expression

When you use the `Exist` or `DoesNotExist` operators in the `Placement`
resource, the application topology node details display the expressions
as `\#invalidExpr`. This display is wrong, and the expression is still
valid and works in the `Placement` resource. To workaround this issue,
edit the expression inside the `Placement` resource YAML.

ACM-15077

#### Editing subscription applications with *PlacementRule* does not display the subscription YAML in editor

After you create a subscription application that references a
`PlacementRule` resource, the subscription YAML does not display in the
YAML editor in the console. Use your terminal to edit your subscription
YAML file.

ACM-8889

#### Helm Chart with secret dependencies cannot be deployed by the Red Hat Advanced Cluster Management subscription

Using Helm Chart, you can define privacy data in a Kubernetes secret and
refer to this secret within the `value.yaml` file of the Helm Chart.

The username and password are given by the referred Kubernetes secret
resource `dbsecret`. For example, see the following sample `value.yaml`
file:

``` yaml
credentials:
  secretName: dbsecret
  usernameSecretKey: username
  passwordSecretKey: password
```

The Helm Chart with secret dependencies is only supported in the Helm
binary CLI. It is not supported in the operator SDK Helm library. The
Red Hat Advanced Cluster Management subscription controller applies the
operator SDK Helm library to install and upgrade the Helm Chart.
Therefore, the Red Hat Advanced Cluster Management subscription cannot
deploy the Helm Chart with secret dependencies.

ACM-8727

#### Topology does not correctly display for Argo CD pull model `ApplicationSet` application

When you use the Argo CD pull model to deploy `ApplicationSet`
applications and the application resource names are customized, the
resource names might appear different for each cluster. When this
happens, the topology does not display your application correctly.

ACM-6954

#### Local cluster is excluded as a managed cluster for pull model

The hub cluster application set deploys to target managed clusters, but
the local cluster, which is a managed hub cluster, is excluded as a
target managed cluster.

As a result, if the Argo CD application is propagated to the local
cluster by the Argo CD pull model, the local cluster Argo CD application
is not cleaned up, even though the local cluster is removed from the
placement decision of the Argo CD `ApplicationSet` resource.

To work around the issue and clean up the local cluster Argo CD
application, remove the `skip-reconcile` annotation from the local
cluster Argo CD application. See the following annotation:

``` yaml
annotations:
    argocd.argoproj.io/skip-reconcile: "true"
```

Additionally, if you manually refresh the pull model Argo CD application
in the **Applications** section of the Argo CD console, the refresh is
not processed and the **REFRESH** button in the Argo CD console is
disabled.

To work around the issue, remove the `refresh` annotation from the Argo
CD application. See the following annotation:

``` yaml
annotations:
    argocd.argoproj.io/refresh: normal
```

ACM-7843

#### Argo CD controller and the propagation controller might reconcile simultaneously

Both the Argo CD controller and the propagation controller might
reconcile on the same application resource and cause the duplicate
instances of application deployment on the managed clusters, but from
the different deployment models.

For deploying applications by using the pull model, the Argo CD
controllers ignore these application resources when the Argo CD
`argocd.argoproj.io/skip-reconcile` annotation is added to the template
section of the `ApplicationSet`.

The `argocd.argoproj.io/skip-reconcile` annotation is only available in
the GitOps operator version 1.9.0, or later. To prevent conflicts, wait
until the hub cluster and all the managed clusters are upgraded to
GitOps operator version 1.9.0 before implementing the pull model.

ACM-3404

#### Resource fails to deploy

All the resources listed in the `MulticlusterApplicationSetReport` are
actually deployed on the managed clusters. If a resource fails to
deploy, the resource is not included in the resource list, but the cause
is listed in the error message.

ACM-3910

#### Resource allocation might take several minutes

For large environments with over 1000 managed clusters and Argo CD
application sets that are deployed to hundreds of managed clusters, Argo
CD application creation on the hub cluster might take several minutes.
You can set the `requeueAfterSeconds` to `zero` in the
`clusterDecisionResource` generator of the application set, as it is
displayed in the following example file:

``` yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: cm-allclusters-app-set
  namespace: openshift-gitops
spec:
  generators:
  - clusterDecisionResource:
      configMapRef: ocm-placement-generator
      labelSelector:
        matchLabels:
          cluster.open-cluster-management.io/placement: app-placement
      requeueAfterSeconds: 0
```

ACM-5177

#### Application ObjectBucket channel type cannot use allow and deny lists

You cannot specify allow and deny lists with ObjectBucket channel type
in the `subscription-admin` role. In other channel types, the allow and
deny lists in the subscription indicates which Kubernetes resources can
be deployed, and which Kubernetes resources should not be deployed.

ACM-22763

#### Changes to the multicluster_operators_subscription image do not take effect automatically

The `application-manager` add-on that is running on the managed clusters
is now handled by the subscription operator, when it was previously
handled by the klusterlet operator. The subscription operator is not
managed the `multicluster-hub`, so changes to the
`multicluster_operators_subscription` image in the `multicluster-hub`
image manifest ConfigMap do not take effect automatically.

If the image that is used by the subscription operator is overrided by
changing the `multicluster_operators_subscription` image in the
`multicluster-hub` image manifest ConfigMap, the `application-manager`
add-on on the managed clusters does not use the new image until the
subscription operator pod is restarted. You need to restart the pod.

ACM-21013

#### Policy resource not deployed unless by subscription administrator

The `policy.open-cluster-management.io/v1` resources are no longer
deployed by an application subscription by default for Red Hat Advanced
Cluster Management version 2.4.

A subscription administrator needs to deploy the application
subscription to change this default behavior.

See Creating an allow and deny list as subscription administrator for
information. `policy.open-cluster-management.io/v1` resources that were
deployed by existing application subscriptions in previous Red Hat
Advanced Cluster Management versions remain, but are no longer
reconciled with the source repository unless the application
subscriptions are deployed by a subscription administrator.

ACM-893

#### Application Ansible hook stand-alone mode

Ansible hook stand-alone mode is not supported. To deploy Ansible hook
on the hub cluster with a subscription, you might use the following
subscription YAML:

``` yaml
apiVersion: apps.open-cluster-management.io/v1
kind: Subscription
metadata:
  name: sub-rhacm-gitops-demo
  namespace: hello-openshift
annotations:
  apps.open-cluster-management.io/github-path: myapp
  apps.open-cluster-management.io/github-branch: master
spec:
  hooksecretref:
      name: toweraccess
  channel: rhacm-gitops-demo/ch-rhacm-gitops-demo
  placement:
     local: true
```

However, this configuration might never create the Ansible instance,
since the `spec.placement.local:true` has the subscription running on
`standalone` mode. You need to create the subscription in hub mode.

1.  Create a placement rule that deploys to `local-cluster`. See the
    following sample where `local-cluster: "true"` refers to your hub
    cluster:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1
    kind: PlacementRule
    metadata:
      name: <towhichcluster>
      namespace: hello-openshift
    spec:
      clusterSelector:
        matchLabels:
          local-cluster: "true"
    ```

2.  Reference that placement rule in your subscription. See the
    following sample:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1
    kind: Subscription
    metadata:
      name: sub-rhacm-gitops-demo
      namespace: hello-openshift
    annotations:
      apps.open-cluster-management.io/github-path: myapp
      apps.open-cluster-management.io/github-branch: master
    spec:
      hooksecretref:
          name: toweraccess
      channel: rhacm-gitops-demo/ch-rhacm-gitops-demo
      placement:
         placementRef:
            name: <towhichcluster>
            kind: PlacementRule
    ```

After applying both, you should see the Ansible instance created in your
hub cluster.

ACM-8036

#### Application not deployed after an updated placement rule

If applications are not deploying after an update to a placement rule,
verify that the `application-manager` pod is running. The
`application-manager` is the subscription container that needs to run on
managed clusters.

You can run
`oc get pods -n open-cluster-management-agent-addon |grep application-manager`
to verify.

You can also search for `kind:pod cluster:yourcluster` in the console
and see if the `application-manager` is running.

If you cannot verify, attempt to import the cluster again and verify
again.

ACM-1449

#### Subscription operator does not create an SCC

Learn about Red Hat OpenShift Container Platform SCC at Managing
security context constraints, which is an additional configuration
required on the managed cluster.

Different deployments have different security context and different
service accounts. The subscription operator cannot create an SCC CR
automatically.. Administrators control permissions for pods. A Security
Context Constraints (SCC) CR is required to enable appropriate
permissions for the relative service accounts to create pods in the
non-default namespace. To manually create an SCC CR in your namespace,
complete the following steps:

1.  Find the service account that is defined in the deployments. For
    example, see the following `nginx` deployments:

        nginx-ingress-52edb
        nginx-ingress-52edb-backend

2.  Create an SCC CR in your namespace to assign the required
    permissions to the service account or accounts. See the following
    example, where `kind: SecurityContextConstraints` is added:

    ``` yaml
    apiVersion: security.openshift.io/v1
     defaultAddCapabilities:
     kind: SecurityContextConstraints
     metadata:
       name: ingress-nginx
       namespace: ns-sub-1
     priority: null
     readOnlyRootFilesystem: false
     requiredDropCapabilities:
     fsGroup:
       type: RunAsAny
     runAsUser:
       type: RunAsAny
     seLinuxContext:
       type: RunAsAny
     users:
     - system:serviceaccount:my-operator:nginx-ingress-52edb
     - system:serviceaccount:my-operator:nginx-ingress-52edb-backend
    ```

ACM-24248

#### Application channels require unique namespaces

Creating more than one channel in the same namespace can cause errors
with the hub cluster.

For instance, namespace `charts-v1` is used by the installer as a Helm
type channel, so do not create any additional channels in `charts-v1`.
Ensure that you create your channel in a unique namespace. All channels
need an individual namespace, except GitHub channels, which can share a
namespace with another GitHub channel.

ACM-2160

#### Ansible Automation Platform job fail

Ansible jobs fail to run when you select an incompatible option. Ansible
Automation Platform only works when the `-cluster-scoped` channel
options are chosen. This affects all components that need to perform
Ansible jobs.

ACM-14469

#### Ansible Automation Platform operator access Ansible Automation Platform outside of a proxy

The Red Hat Ansible Automation Platform operator cannot access Ansible
Automation Platform outside of a proxy-enabled OpenShift Container
Platform cluster. To resolve, you can install the Ansible Automation
Platform within the proxy. See install steps that are provided by
Ansible Automation Platform.

ACM-16821

#### Application name requirements

An application name cannot exceed 37 characters. The application
deployment displays the following error if the characters exceed this
amount.

``` yaml
status:
  phase: PropagationFailed
  reason: 'Deployable.apps.open-cluster-management.io "_long_lengthy_name_" is invalid: metadata.labels: Invalid value: "_long_lengthy_name_": must be no more than 63 characters/n'
```

ACM-14310

#### Application console table limitations

See the following limitations to various *Application* tables in the
console:

- From the *Applications* table on the *Overview* page and the
  *Subscriptions* table on the *Advanced configuration* page, the
  *Clusters* column displays a count of clusters where application
  resources are deployed. Since applications are defined by resources on
  the local cluster, the local cluster is included in the search
  results, whether actual application resources are deployed on the
  local cluster or not.

- From the *Advanced configuration* table for *Subscriptions*, the
  *Applications* column displays the total number of applications that
  use that subscription, but if the subscription deploys child
  applications, those are included in the search result, as well.

- From the *Advanced configuration* table for *Channels*, the
  *Subscriptions* column displays the total number of subscriptions on
  the local cluster that use that channel, but this does not include
  subscriptions that are deployed by other subscriptions, which are
  included in the search result.

ACM-12410

#### No Application console topology filtering

The *Console* and *Topology* for *Application* changes for the 2.15.
There is no filtering capability from the console Topology page.

ACM-20831

#### *ClusterPermission* resource fails when creating many role bindings

If you create a `ClusterPermission` resource that contains many role
bindings within the same namespace and do not set the optional `name`
field, it fails. This error occurs because the same name is used for the
role bindings in the namespace.

To workaround this issue, set the optional `name` field for each role
binding with a unique name.

ACM-21342

### Observability known issues

Review the known issues for Red Hat Advanced Cluster Management for
Kubernetes. The following list contains known issues for this release,
or known issues that continued from the previous release.

For your Red Hat OpenShift Container Platform cluster, see
link:https://docs.redhat.com/en/documentation/openshift_container_platform/4.18/html/release_notes#ocp-4-15-known-issues
\[OpenShift Container Platform known issues\].

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

#### Retention change causes data loss

The default retention for all resolution levels, such as
`retentionResolutionRaw`, `retentionResolution5m`, or
`retentionResolution1h`, is 365 days (`365d`). This `365d` default
retention means that the default retention for a 1 hour resolution has
decreased from indefinite, `0d` to `365d`. This retention change might
cause you to lose data. If you did not set an explicit value for the
resolution retention in your `MultiClusterObservability`
`spec.advanced.retentionConfig` parameter, you might lose data.

For more information, see Adding advanced configuration for retention.

ACM-11048

#### Observatorium API gateway pods in a restored hub cluster might have stale tenant data

The Observatorium API gateway pods in a restored hub cluster might
contain stale tenant data after a backup and restore procedure because
of a Kubernetes limitation. See Mounted ConfigMaps are updated
automatically for more about the limitation.

As a result, the Observatorium API and Thanos gateway rejects metrics
from collectors, and the Red Hat Advanced Cluster Management Grafana
dashboards do not display data.

See the following errors from the Observatorium API gateway pod logs:

    level=error name=observatorium caller=logchannel.go:129 msg="failed to forward metrics" returncode="500 Internal Server Error" response="no matching hashring to handle tenant\n"

Thanos receives pods logs with the following errors:

    caller=handler.go:551 level=error component=receive component=receive-handler tenant=xxxx err="no matching hashring to handle tenant" msg="internal server error"

See the following procedure to resolve this issue:

1.  Scale down the `observability-observatorium-api` deployment
    instances from `N` to `0`.

2.  Scale up the `observability-observatorium-api` deployment instances
    from `0` to `N`.

**Note:** `N` = `2` by default, but might be greater than `2` in some
custom configuration environments.

This restarts all Observatorium API gateway pods with the correct tenant
information, and the data from collectors start displaying in Grafana in
between 5-10 minutes.

ACM-9681

#### Permission to add *PrometheusRules* and *ServiceMonitors* in *openshift-monitoring* namespace denied

You must use a label in your defined Red Hat Advanced Cluster Management
hub cluster namespace. The label,
`openshift.io/cluster-monitoring: "true"` causes the Cluster Monitoring
Operator to scrape the namespace for metrics.

When Red Hat Advanced Cluster Management is deployed or an installation
is upgraded, the Red Hat Advanced Cluster Management Observability
`ServiceMonitors` and `PrometheusRule` resources are no longer present
in the `openshift-monitoring` namespace.

ACM-8499

#### Lack of support for proxy settings

The Prometheus `AdditionalAlertManagerConfig` resource of the
observability add-on does not support proxy settings. You must disable
the observability alert forwarding feature.

Complete the following steps to disable alert forwarding:

1.  Go to the `MultiClusterObservability` resource.

2.  Update the `mco-disabling-alerting` parameter value to `true`

The HTTPS proxy with a self-signed CA certificate is not supported.

ACM-7118

##### Grafana downsampled data mismatch

When you attempt to query historical data and there is a discrepancy
between the calculated step value and downsampled data, the result is
empty. For example, if the calculated step value is `5m` and the
downsampled data is in a one-hour interval, data does not appear from
Grafana.

This discrepancy occurs because a URL query parameter must be passed
through the Thanos Query front-end data source. Afterwards, the URL
query can perform additional queries for other downsampling levels when
data is missing.

You must manually update the Thanos Query front-end data source
configuration. Complete the following steps:

1.  Go to the Query front-end data source.

2.  To update your query parameters, click the *Misc* section.

3.  From the *Custom query parameters* field, select
    **`max_source_resolution=auto`**.

4.  To verify that the data is displayed, refresh your Grafana page.

Your query data appears from the Grafana dashboard.

ACM-3748

#### Limitations when using custom managed cluster Observatorium API or Alertmanager URLs

Custom Observatorium API and Alertmanager URLs only support intermediate
components with TLS passthrough. If both custom URLs are pointing to the
same intermediate component, you must use separate sub-domains because
OpenShift Container Platform routers do not support two separate route
objects with the same host.

ACM-11407

### Governance known issues

Review the known issues for Governance. The following list contains
known issues for this release, or known issues that continued from the
previous release.

For your Red Hat OpenShift Container Platform cluster, see OpenShift
Container Platform known issues.

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

#### The *ConfigurationPolicy* incorrectly processes *objectSelector* and *namespaceSelector* results

When you use both the `objectSelector` and the `namespaceSelector`
fields in a `ConfigurationPolicy` resource, the objects that the
`objectSelector` return get applied to all the namespaces that the
`namespaceSelector` return. The `ConfigurationPolicy` incorrectly
processes the results. To workaround this issue, apply the
`object-templates-raw` field to iterate over the objects.

ACM-22676

#### Configuration policy listed complaint when namespace is stuck in *Terminating* state

When you have a configuration policy that is configured with
`mustnothave` for the `complianceType` parameter and `enforce` for the
`remediationAction` parameter, the policy is listed as compliant when a
deletion request is made to the Kubernetes API. Therefore, the
Kubernetes object can be stuck in a `Terminating` state while the policy
is listed as compliant.

ACM-20715

#### ConfigurationPolicy custom resource definition is stuck in terminating

When you remove the `config-policy-controller` add-on from a managed
cluster by disabling the policy controller in the
`KlusterletAddonConfig` or by detaching the cluster, the
`ConfigurationPolicy` custom resource definition might get stuck in a
terminating state. If the `ConfigurationPolicy` custom resource
definition is stuck in a terminating state, new policies might not be
added to the cluster if the add-on is reinstalled later. You can also
receive the following error:

    template-error; Failed to create policy template: create not allowed while custom resource definition is terminating

Use the following command to check if the custom resource definition is
stuck:

    oc get crd configurationpolicies.policy.open-cluster-management.io -o=jsonpath='{.metadata.deletionTimestamp}'

If a deletion timestamp is on the resource, the custom resource
definition is stuck. To resolve the issue, remove all finalizers from
configuration policies that remain on the cluster. Use the following
command on the managed cluster and replace `<cluster-namespace>` with
the managed cluster namespace:

    oc get configurationpolicy -n <cluster-namespace> -o name | xargs oc patch -n <cluster-namespace> --type=merge -p '{"metadata":{"finalizers": []}}'

The configuration policy resources are automatically removed from the
cluster and the custom resource definition exits its terminating state.
If the add-on has already been reinstalled, the custom resource
definition is recreated automatically without a deletion timestamp.

ACM-25139

#### Policy status shows repeated updates when enforced

If a policy is set to `remediationAction: enforce` and is repeatedly
updated, the Red Hat Advanced Cluster Management console shows repeated
violations with successful updates. Repeated updates produce multiple
policy events, which can cause the `governance-policy-framework-addon`
pod to run out of memory and crash. See the following two possible
causes and solutions for the error:

- Another controller or process is also updating the object with
  different values.

  To resolve the issue, disable the policy and compare the differences
  between `objectDefinition` in the policy and the object on the managed
  cluster. If the values are different, another controller or process
  might be updating them. Check the `metadata` of the object to help
  identify why the values are different.

- The `objectDefinition` in the `ConfigurationPolicy` does not match
  because of Kubernetes processing the object when the policy is
  applied.

  To resolve the issue, disable the policy and compare the differences
  between `objectDefinition` in the policy and the object on the managed
  cluster. If the keys are different or missing, Kubernetes might have
  processed the keys before applying them to the object, such as
  removing keys containing default or empty values.

ACM-3109

#### Duplicate policy template names create inconsistent results

When you create a policy with identical policy template names, you
receive inconsistent results that are not detected, but you might not
know the cause. For example, defining a policy with multiple
configuration policies named `create-pod` causes inconsistent results.
**Best practice:** Avoid using duplicate names for policy templates.

ACM-5754

#### Kyverno policies no longer report a status for the latest version

Kyverno policies generated by the Policy Generator report the following
message in your Red Hat Advanced Cluster Management cluster:

    violation - couldn't find mapping resource with kind ClusterPolicyReport, please check if you have CRD deployed;
    violation - couldn't find mapping resource with kind PolicyReport, please check if you have CRD deployed

The cause is that the `PolicyReport` API version is incorrect in the
generator and does not match what Kyverno has deployed.

ACM-12743

### Networking known issues

Review the known issues for Submariner. The following list contains
known issues for this release, or known issues that continued from the
previous release.

For your Red Hat OpenShift Container Platform cluster, see OpenShift
Container Platform known issues.

For more about deprecations and removals, see Deprecations and removals
for Red Hat Advanced Cluster Management.

#### Submariner known issues

See the following known issues and limitations that might occur while
using networking features.

##### Source IP not retained for applications on OpenShift Container Platform with OVN-Kubernetes

If you are using OpenShift Container Platform versions between 4.18 and
versions earlier than 4.19.5 with OVN-Kubernetes for Submariner, the
source IP is not retained when packets reach the destination pod. As a
result, applications that rely on the source IP, such as
`NetworkPolicy`, might not work correctly.

ACM-18680

##### Without *ClusterManagementAddon* submariner add-on fails

For versions 2.8 and earlier, when you install Red Hat Advanced Cluster
Management, you also deploy the `submariner-addon` component with the
Operator Lifecycle Manager. If you did not create a `MultiClusterHub`
custom resource, the `submariner-addon` pod sends an error and prevents
the operator from installing.

The following notification occurs because the `ClusterManagementAddon`
custom resource definition is missing:

    graceful termination failed, controllers failed with error: the server could not find the requested resource (post clustermanagementaddons.addon.open-cluster-management.io)

The `ClusterManagementAddon` resource is created by the
`cluster-manager` deployment, however, this deployment becomes available
when the `MultiClusterEngine` components are installed on the cluster.

If there is not a `MultiClusterEngine` resource that is already
available on the cluster when the `MultiClusterHub` custom resource is
created, the `MultiClusterHub` operator deploys the `MultiClusterEngine`
instance and the operator that is required, which resolves the previous
error.

ACM-24159

##### Submariner add-on resources not cleaned up properly when managed clusters are imported

If the `submariner-addon` component is set to `false` within
`MultiClusterHub` (MCH) operator, then the `submariner-addon` finalizers
are not cleaned up properly for the managed cluster resources. Since the
finalizers are not cleaned up properly, this prevents the
`submariner-addon` component from being disabled within the hub cluster.

ACM-8549

##### Submariner install plan limitation

The Submariner install plan does not follow the overall install plan
settings. Therefore, the operator management screen cannot control the
Submariner install plan. By default, Submariner install plans are
applied automatically, and the Submariner add-on is always updated to
the latest available version corresponding to the installed Red Hat
Advanced Cluster Management version. To change this behavior, you must
use a customized Submariner subscription.

ACM-8260

##### Limited headless services support

Service discovery is not supported for headless services without
selectors when using Globalnet.

ACM-24159

##### Deployments that use VXLAN when NAT is enabled are not supported

Only non-NAT deployments support Submariner deployments with the VXLAN
cable driver.

ACM-24258

##### Self-signed certificates might prevent connection to broker

Self-signed certificates on the broker might prevent joined clusters
from connecting to the broker. The connection fails with certificate
validation errors. You can disable broker certificate validation by
setting `InsecureBrokerConnection` to `true` in the relevant
`SubmarinerConfig` object. See the following example:

``` yaml
apiVersion: submarineraddon.open-cluster-management.io/v1alpha1
kind: SubmarinerConfig
metadata:
   name: submariner
   namespace: <managed-cluster-namespace>
spec:
   insecureBrokerConnection: true
```

ACM-27008

##### Submariner only supports OpenShift SDN or OVN Kubernetes

Submariner only supports Red Hat OpenShift Container Platform clusters
that use the OpenShift SDN or the OVN-Kubernetes Container Network
Interface (CNI) network provider.

ACM-5306

##### Command limitation on Microsoft Azure clusters

The `subctl diagnose firewall inter-cluster` command does not work on
Microsoft Azure clusters.

ACM-5327

##### Automatic upgrade not working with custom *CatalogSource* or *Subscription*

Submariner is automatically upgraded when Red Hat Advanced Cluster
Management for Kubernetes is upgraded. The automatic upgrade might fail
if you are using a custom `CatalogSource` or `Subscription`.

To make sure automatic upgrades work when installing Submariner on
managed clusters, you must set the `spec.subscriptionConfig.channel`
field to `stable-0.15` in the `SubmarinerConfig` custom resource for
each managed cluster.

ACM-6068

##### Uninstall Submariner before removing *ManagedCluster* from a *ManageClusterSet*

If you remove a cluster from a `ClusterSet`, or move a cluster to a
different `ClusterSet`, the Submariner installation is no longer valid.

You must uninstall Submariner before moving or removing a
`ManagedCluster` from a `ManageClusterSet`. If you don’t uninstall
Submariner, you cannot uninstall or reinstall Submariner anymore and
Submariner stops working on your `ManagedCluster`.

ACM-8847

### Multicluster global hub Operator known issues

Review the known issues for the multicluster global hub Operator. The
following list contains known issues for this release, or known issues
that continued from the previous release. For your OpenShift Container
Platform cluster, see OpenShift Container Platform known issues.

#### The *ManagedClusterMigration* resources error

When you upgrade multicluster global hub and there are some
`ManagedClusterMigration` resources in the multicluster global hub
cluster, you might get the following error:

``` bash
error validating existing CRs against new CRD''s schema for "managedclustermigrations.global-hub.open-cluster-management.io":
      error validating global-hub.open-cluster-management.io/v1alpha1, Kind=ManagedClusterMigration
      "multicluster-global-hub/xxx": updated validation is
      too restrictive: [].spec.from: Required value'
```

To workaround this issue, delete all the `ManagedClusterMigration`
resources before you upgrade multicluster global hub. Run the following
command:

``` bash
oc delete mcm --all
```

ACM-25679

#### The detached managed hub cluster deletes and recreates the namespace and resources

If you import a managed hub cluster in the hosted mode and detach this
managed hub cluster, then it deletes and recreates the
`open-cluster-management-agent-addon` namespace. The detached managed
hub cluster also deletes and recreates all the related `addon` resources
within this namespace.

There is currently no workaround for this issue.

ACM-15014

#### Kafka operator keeps restarting

In the Federal Information Processing Standard (FIPS) environment, the
Kafka operator keeps restarting because of the out-of-memory (OOM)
state. To fix this issue, set the resource limit to at least `512M`. For
detailed steps on how to set this limit, see amq stream doc.

ACM-12592

#### The standard group filter cannot pass to the new page

In the *Global Hub Policy Group Compliancy Overview* hub dashboards, you
can check one data point by clicking **View Offending Policies for
standard group**, but after you click this link to go to the offending
page, the standard group filter cannot pass to the new page.

This is also an issue for the **Cluster Group Compliancy Overview**.

ACM-7461

## Deprecations and removals for Red Hat Advanced Cluster Management

Learn when parts of the product are deprecated or removed from Red Hat
Advanced Cluster Management for Kubernetes. Consider the alternative
actions in the *Recommended action* and details, which display in the
tables for the current release and for two prior releases.

**Deprecated:** Red Hat Advanced Cluster Management 2.10 and earlier
versions are no longer supported. The documentation might remain
available, but without any errata releases for fixed issues or other
updates.

**Best practice:** Upgrade to the most recent version.

**Important:** Cluster lifecycle components and features are within the
multicluster engine operator, which is a software operator that enhances
cluster fleet management. Release notes for multicluster engine
operator-specific features are found in at Release notes for Cluster
lifecycle with multicluster engine operator.

### Product deprecations and removals

A *deprecated* component, feature, or service is supported, but no
longer recommended for use and might become obsolete in future releases.
Consider the alternative actions in the *Recommended action* and details
that are provided in the following table:

- Product or category: Documentation for APIs - Affected item: The Red
  Hat Advanced Cluster Management API documentation - Version: Red Hat
  Advanced Cluster Management 2.13 - Recommended action: View current
  and supported APIs from the console or the terminal instead of the
  documentation. - More details and links: None

- Product or category: Application management - Affected item:
  Subscription - Version: Red Hat Advanced Cluster Management 2.13 -
  Recommended action: Use Red Hat Advanced Cluster Management with
  OpenShift GitOps instead. - More details and links: The deprecation is
  extended for five releases before removal. See GitOps overview for
  updated function.

- Product or category: Applications and Governance - Affected item:
  PlacementRule - Version: 2.8 - Recommended action: Use Placement
  anywhere that you might use PlacementRule. - More details and links:
  While PlacementRule is still available, it is not supported and the
  console displays Placement by default.

- Product or category: multicluster global hub - Affected item:
  PostgreSQL manual upgrade process - Version: Red Hat Advanced Cluster
  Management 2.14 - Recommended action: None - More details and links:
  Automatic database upgrades are supported for multicluster global hub
  version 1.5 and later.

A *removed* item is typically function that was deprecated in previous
releases and is no longer available in the product. You must use
alternatives for the removed function. Consider the alternative actions
in the *Recommended action* and details that are provided in the
following table:

- Product or category: multicluster global hub - Affected item: You are
  not required to migrate the resources, ConfigMaps and Secrets when you
  migrate managed clusters. - Version: 2.15 - Recommended action:
  Migrate the managed clusters. - More details and links: See Migrating
  managed clusters.

- Product or category: Red Hat Advanced Cluster Management for
  Kubernetes Search service - Affected item: Enabling virtual machine
  actions (Technology Preview) - Version: 2.14 - Recommended action: Use
  fine-grained role-base access control instead. - More details and
  links: See Role-based access control.

- Product or category: Red Hat Advanced Cluster Management for
  Kubernetes console - Affected item: Importing OpenShift Container
  Platform 3.11 clusters from the console - Version: 2.14 - Recommended
  action: Upgrade to a supported version of OpenShift Container
  Platform. See the OpenShift Container Platform documentation. - More
  details and links: The support for the deprecated custom resource
  definition v1beta1 APIs is removed. The v1beta1 APIs were only needed
  for OpenShift Container Platform 3.11.

- Product or category: Original Overview page - Affected item: Red Hat
  Advanced Cluster Management for Kubernetes search console - Version:
  2.13 - Recommended action: Enable the Fleet view switch to view the
  new default Overview page. - More details and links: The previous
  layout of the Red Hat Advanced Cluster Management Overview page is
  redesigned.

- Product or category: Policy compliance history API - Affected item:
  Governance - Version: 2.13 - Recommended action: Use the existing
  policy metrics to see the compliance status changes. You can also view
  the config-policy-controller and cert-policy-controller pod logs to
  get a detailed compliance history for each managed cluster. - More
  details and links: For more information, see Policy controller
  advanced configuration.

## Red Hat Advanced Cluster Management platform considerations for GDPR readiness

### Notice

This document is intended to help you in your preparations for General
Data Protection Regulation (GDPR) readiness. It provides information
about features of the Red Hat Advanced Cluster Management for Kubernetes
platform that you can configure, and aspects of the product’s use, that
you should consider to help your organization with GDPR readiness.

This information is not an exhaustive list, due to the many ways that
clients can choose and configure features, and the large variety of ways
that the product can be used in itself and with third-party clusters and
systems.

**Clients are responsible for ensuring their own compliance with various
laws and regulations, including the European Union General Data
Protection Regulation.**

**Clients are solely responsible for obtaining advice of competent legal
counsel as to the identification and interpretation of any relevant laws
and regulations that may affect the clients' business and any actions
the clients may need to take to comply with such laws and regulations.**

**The products, services, and other capabilities described herein are
not suitable for all client situations and may have restricted
availability. Red Hat does not provide legal, accounting, or auditing
advice or represent or warrant that its services or products will ensure
that clients are in compliance with any law or regulation.**

### GDPR

General Data Protection Regulation (GDPR) has been adopted by the
European Union (EU) and applies from May 25, 2018.

#### Why is GDPR important?

GDPR establishes a stronger data protection regulatory framework for
processing personal data of individuals. GDPR brings:

- New and enhanced rights for individuals

- Widened definition of personal data

- New obligations for processors

- Potential for significant financial penalties for non-compliance

- Compulsory data breach notification

### Product Configuration for GDPR

The following sections describe aspects of data management within the
Red Hat Advanced Cluster Management for Kubernetes platform and provide
information on capabilities to help clients with GDPR requirements.

### Data Life Cycle

Red Hat Advanced Cluster Management for Kubernetes is an application
platform for developing and managing on-premises, containerized
applications. It is an integrated environment for managing containers
that includes the container orchestrator Kubernetes, cluster lifecycle,
application lifecycle, and security frameworks (governance, risk, and
compliance).

As such, the Red Hat Advanced Cluster Management for Kubernetes platform
deals primarily with technical data that is related to the configuration
and management of the platform, some of which might be subject to GDPR.
The Red Hat Advanced Cluster Management for Kubernetes platform also
deals with information about users who manage the platform. This data
will be described throughout this document for the awareness of clients
responsible for meeting GDPR requirements.

This data is persisted on the platform on local or remote file systems
as configuration files or in databases. Applications that are developed
to run on the Red Hat Advanced Cluster Management for Kubernetes
platform might deal with other forms of personal data subject to GDPR.
The mechanisms that are used to protect and manage platform data are
also available to applications that run on the platform. Additional
mechanisms might be required to manage and protect personal data that is
collected by applications run on the Red Hat Advanced Cluster Management
for Kubernetes platform.

To best understand the Red Hat Advanced Cluster Management for
Kubernetes platform and its data flows, you must understand how
Kubernetes, Docker, and the Operator work. These open source components
are fundamental to the Red Hat Advanced Cluster Management for
Kubernetes platform. You use Kubernetes deployments to place instances
of applications, which are built into Operators that reference Docker
images. The Operator contain the details about your application, and the
Docker images contain all the software packages that your applications
need to run.

#### What types of data flow through Red Hat Advanced Cluster Management for Kubernetes platform

As a platform, Red Hat Advanced Cluster Management for Kubernetes deals
with several categories of technical data that could be considered as
personal data, such as an administrator user ID and password, service
user IDs and passwords, IP addresses, and Kubernetes node names. The Red
Hat Advanced Cluster Management for Kubernetes platform also deals with
information about users who manage the platform. Applications that run
on the platform might introduce other categories of personal data
unknown to the platform.

Information on how this technical data is collected/created, stored,
accessed, secured, logged, and deleted is described in later sections of
this document.

#### Personal data used for online contact

Customers can submit online comments, feedback, and requests for
information about in a variety of ways, primarily:

- The public Slack community if there is a Slack channel

- The public comments or tickets on the product documentation

- The public conversations in a technical community

Typically, only the client name and email address are used, to enable
personal replies for the subject of the contact, and the use of personal
data conforms to the Red Hat Online Privacy Statement.

### Data Collection

The Red Hat Advanced Cluster Management for Kubernetes platform does not
collect sensitive personal data. It does create and manage technical
data, such as an administrator user ID and password, service user IDs
and passwords, IP addresses, and Kubernetes node names, which might be
considered personal data. The Red Hat Advanced Cluster Management for
Kubernetes platform also deals with information about users who manage
the platform. All such information is only accessible by the system
administrator through a management console with role-based access
control or by the system administrator though login to a Red Hat
Advanced Cluster Management for Kubernetes platform node.

Applications that run on the Red Hat Advanced Cluster Management for
Kubernetes platform might collect personal data.

When you assess the use of the Red Hat Advanced Cluster Management for
Kubernetes platform running containerized applications and your need to
meet the requirements of GDPR, you must consider the types of personal
data that are collected by the application and aspects of how that data
is managed, such as:

- How is the data protected as it flows to and from the application? Is
  the data encrypted in transit?

- How is the data stored by the application? Is the data encrypted at
  rest?

- How are credentials that are used to access the application collected
  and stored?

- How are credentials that are used by the application to access data
  sources collected and stored?

- How is data collected by the application removed as needed?

This is not a definitive list of the types of data that are collected by
the Red Hat Advanced Cluster Management for Kubernetes platform. It is
provided as an example for consideration. If you have any questions
about the types of data, contact Red Hat.

### Data storage

The Red Hat Advanced Cluster Management for Kubernetes platform persists
technical data that is related to configuration and management of the
platform in stateful stores on local or remote file systems as
configuration files or in databases. Consideration must be given to
securing all data at rest. The Red Hat Advanced Cluster Management for
Kubernetes platform supports encryption of data at rest in stateful
stores that use `dm-crypt`.

The following items highlight the areas where data is stored, which you
might want to consider for GDPR.

- **Platform Configuration Data:** The Red Hat Advanced Cluster
  Management for Kubernetes platform configuration can be customized by
  updating a configuration YAML file with properties for general
  settings, Kubernetes, logs, network, Docker, and other settings. This
  data is used as input to the Red Hat Advanced Cluster Management for
  Kubernetes platform installer for deploying one or more nodes. The
  properties also include an administrator user ID and password that are
  used for bootstrap.

- **Kubernetes Configuration Data:** Kubernetes cluster state data is
  stored in a distributed key-value store, `etcd`.

- **User Authentication Data, including User IDs and passwords:** User
  ID and password management are handled through a client enterprise
  LDAP directory. Users and groups that are defined in LDAP can be added
  to Red Hat Advanced Cluster Management for Kubernetes platform teams
  and assigned access roles. Red Hat Advanced Cluster Management for
  Kubernetes platform stores the email address and user ID from LDAP,
  but does not store the password. Red Hat Advanced Cluster Management
  for Kubernetes platform stores the group name and upon login, caches
  the available groups to which a user belongs. Group membership is not
  persisted in any long-term way. Securing user and group data at rest
  in the enterprise LDAP must be considered. Red Hat Advanced Cluster
  Management for Kubernetes platform also includes an authentication
  service, Open ID Connect (OIDC) that interacts with the enterprise
  directory and maintains access tokens. This service uses ETCD as a
  backing store.

- **Service authentication data, including user IDs and passwords:**
  Credentials that are used by Red Hat Advanced Cluster Management for
  Kubernetes platform components for inter-component access are defined
  as Kubernetes Secrets. All Kubernetes resource definitions are
  persisted in the `etcd` key-value data store. Initial credentials
  values are defined in the platform configuration data as Kubernetes
  Secret configuration YAML files. For more information, see Secrets in
  the Kubernetes documentation.

### Data access

Red Hat Advanced Cluster Management for Kubernetes platform data can be
accessed through the following defined set of product interfaces.

- Web user interface (the console)

- Kubernetes `kubectl` CLI

- Red Hat Advanced Cluster Management for Kubernetes CLI

- oc CLI

These interfaces are designed to allow you to make administrative
changes to your Red Hat Advanced Cluster Management for Kubernetes
cluster. Administration access to Red Hat Advanced Cluster Management
for Kubernetes can be secured and involves three logical, ordered stages
when a request is made: authentication, role-mapping, and authorization.

#### Authentication

The Red Hat Advanced Cluster Management for Kubernetes platform
authentication manager accepts user credentials from the console and
forwards the credentials to the backend OIDC provider, which validates
the user credentials against the enterprise directory. The OIDC provider
then returns an authentication cookie (`auth-cookie`) with the content
of a JSON Web Token (`JWT`) to the authentication manager. The JWT token
persists information such as the user ID and email address, in addition
to group membership at the time of the authentication request. This
authentication cookie is then sent back to the console. The cookie is
refreshed during the session. It is valid for 12 hours after you sign
out of the console or close your web browser.

For all subsequent authentication requests made from the console, the
front-end NGINX server decodes the available authentication cookie in
the request and validates the request by calling the authentication
manager.

The Red Hat Advanced Cluster Management for Kubernetes platform CLI
requires the user to provide credentials to log in.

The `kubectl` and `oc` CLI also requires credentials to access the
cluster. These credentials can be obtained from the management console
and expire after 12 hours. Access through service accounts is supported.

#### Role Mapping

Red Hat Advanced Cluster Management for Kubernetes platform supports
role-based access control (RBAC). In the role mapping stage, the user
name that is provided in the authentication stage is mapped to a user or
group role. The roles are used when authorizing which administrative
activities can be carried out by the authenticated user.

#### Authorization

Red Hat Advanced Cluster Management for Kubernetes platform roles
control access to cluster configuration actions, to catalog and Helm
resources, and to Kubernetes resources. Several IAM (Identity and Access
Management) roles are provided, including Cluster Administrator,
Administrator, Operator, Editor, Viewer. A role is assigned to users or
user groups when you add them to a team. Team access to resources can be
controlled by namespace.

#### Pod Security

Pod security policies are used to set up cluster-level control over what
a pod can do or what it can access.

### Data Processing

Users of Red Hat Advanced Cluster Management for Kubernetes can control
the way that technical data that is related to configuration and
management is processed and secured through system configuration.

**Role-based access control** (RBAC) controls what data and functions
can be accessed by users.

**Data-in-transit** is protected by using `TLS`. `HTTPS` (`TLS`
underlying) is used for secure data transfer between user client and
back end services. Users can specify the root certificate to use during
installation.

**Data-at-rest** protection is supported by using `dm-crypt` to encrypt
data.

These same platform mechanisms that are used to manage and secure Red
Hat Advanced Cluster Management for Kubernetes platform technical data
can be used to manage and secure personal data for user-developed or
user-provided applications. Clients can develop their own capabilities
to implement further controls.

### Data Deletion

Red Hat Advanced Cluster Management for Kubernetes platform provides
commands, application programming interfaces (APIs), and user interface
actions to delete data that is created or collected by the product.
These functions enable users to delete technical data, such as service
user IDs and passwords, IP addresses, Kubernetes node names, or any
other platform configuration data, as well as information about users
who manage the platform.

Areas of Red Hat Advanced Cluster Management for Kubernetes platform to
consider for support of data deletion:

- All technical data that is related to platform configuration can be
  deleted through the management console or the Kubernetes `kubectl`
  API.

Areas of Red Hat Advanced Cluster Management for Kubernetes platform to
consider for support of account data deletion:

- All technical data that is related to platform configuration can be
  deleted through the Red Hat Advanced Cluster Management for Kubernetes
  or the Kubernetes `kubectl` API.

Function to remove user ID and password data that is managed through an
enterprise LDAP directory would be provided by the LDAP product used
with Red Hat Advanced Cluster Management for Kubernetes platform.

### Capability for Restricting Use of Personal Data

Using the facilities summarized in this document, Red Hat Advanced
Cluster Management for Kubernetes platform enables an end user to
restrict usage of any technical data within the platform that is
considered personal data.

Under GDPR, users have rights to access, modify, and restrict
processing. Refer to other sections of this document to control the
following:

- Right to access

  - Red Hat Advanced Cluster Management for Kubernetes platform
    administrators can use Red Hat Advanced Cluster Management for
    Kubernetes platform features to provide individuals access to their
    data.

  - Red Hat Advanced Cluster Management for Kubernetes platform
    administrators can use Red Hat Advanced Cluster Management for
    Kubernetes platform features to provide individuals information
    about what data Red Hat Advanced Cluster Management for Kubernetes
    platform holds about the individual.

- Right to modify

  - Red Hat Advanced Cluster Management for Kubernetes platform
    administrators can use Red Hat Advanced Cluster Management for
    Kubernetes platform features to allow an individual to modify or
    correct their data.

  - Red Hat Advanced Cluster Management for Kubernetes platform
    administrators can use Red Hat Advanced Cluster Management for
    Kubernetes platform features to correct an individual’s data for
    them.

- Right to restrict processing

  - Red Hat Advanced Cluster Management for Kubernetes platform
    administrators can use Red Hat Advanced Cluster Management for
    Kubernetes platform features to stop processing an individual’s
    data.

### Appendix

As a platform, Red Hat Advanced Cluster Management for Kubernetes deals
with several categories of technical data that could be considered as
personal data, such as an administrator user ID and password, service
user IDs and passwords, IP addresses, and Kubernetes node names. Red Hat
Advanced Cluster Management for Kubernetes platform also deals with
information about users who manage the platform. Applications that run
on the platform might introduce other categories of personal data that
are unknown to the platform.

This appendix includes details on data that is logged by the platform
services.

## FIPS readiness

Red Hat Advanced Cluster Management for Kubernetes is designed for
Federal Information Processing Standards (FIPS). When running on Red Hat
OpenShift Container Platform in FIPS mode, OpenShift Container Platform
uses the Red Hat Enterprise Linux cryptographic libraries submitted to
NIST for FIPS Validation on only the architectures that are supported by
OpenShift Container Platform.

For more information about the NIST validation program, see
Cryptographic Module Validation Program.

For the latest NIST status for the individual versions of the RHEL
cryptographic libraries submitted for validation, see Compliance
Activities and Government Standards.

If you plan to manage clusters with FIPS enabled, you must install Red
Hat Advanced Cluster Management on an OpenShift Container Platform
cluster that is configured to operate in FIPS mode. The hub cluster must
be in FIPS mode because cryptography that is created on the hub cluster
is used on managed clusters.

To enable FIPS mode on your managed clusters, set `fips: true` when you
provision your OpenShift Container Platform managed cluster. You cannot
enable FIPS after you provision your cluster.

For more information, see Do you need extra security for your cluster?
in the OpenShift Container Platform documentation.

### FIPS readiness limitations

Read the following limitations with Red Hat Advanced Cluster Management
components and features for FIPS readiness.

- Persistent Volume Claim (PVC) and S3 storage that is used by the
  search and observability components must be encrypted when you
  configure the provided storage. Red Hat Advanced Cluster Management
  does not provide storage encryption, see the OpenShift Container
  Platform documentation, Configuring persistent storage.

- When you provision managed clusters using the Red Hat Advanced Cluster
  Management console, select the following checkbox in the *Cluster
  details* section of the managed cluster creation to enable the FIPS
  standards:

      FIPS with information text: Use the Federal Information Processing Standards (FIPS) modules provided with Red Hat Enterprise Linux CoreOS instead of the default Kubernetes cryptography suite file before you deploy the new managed cluster.

- The Red Hat Edge Manager (Technolgy Preview) component that is
  integrated with Red Hat Advanced Cluster Management is not developed
  for FIPS readiness.

## Observability support

- Red Hat Advanced Cluster Management is tested with and fully supported
  by Red Hat OpenShift Data Foundation, formerly Red Hat OpenShift
  Container Platform.

- Red Hat Advanced Cluster Management supports the function of the
  multicluster observability operator on user-provided third-party
  object storage that is S3 API compatible. The observability service
  uses Thanos supported, stable object stores.

- Red Hat Advanced Cluster Management support efforts include reasonable
  efforts to identify root causes. If you open a support ticket and the
  root cause is the S3 compatible object storage that you provided, then
  you must open an issue using the customer support channels.
