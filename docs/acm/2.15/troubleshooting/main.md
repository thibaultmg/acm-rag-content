# Troubleshooting

View troubleshooting topics for Red Hat Advanced Cluster Management
components. Before using the *Troubleshooting* guides, you can run a
`must-gather` command to gather details, logs, and take steps in
debugging issues.

For more information about the `must-gather` command, see the Gathering
data about your cluster in the OpenShift Container Platform
documentation.

Additionally, check your role-based access. See Role-based access
control for details.

## Documented troubleshooting

View the list of troubleshooting topics for Red Hat Advanced Cluster
Management for Kubernetes:

**Installation**

To view the main documentation for the installing tasks, see Installing
and upgrading.

**Backup and restore**

To view the main documentation for backup and restore, see Backup and
restore.

**Cluster management**

To view the main documentation about managing your clusters, see The
multicluster engine operator cluster lifecycle overview.

**multicluster global hub**

To view the main documentation about the multicluster global hub, see
multicluster global hub.

**Application management**

To view the main documentation about application management, see
Managing applications.

**Governance**

**Console observability**

Console observability includes *Search*, along with header and
navigation function. To view the Observability guide, see Observability
in the console.

**Submariner networking and service discovery**

This section lists the Submariner troubleshooting procedures that can
occur when using Submariner with Red Hat Advanced Cluster Management or
multicluster engine operator. For general Submariner troubleshooting
information, see Troubleshooting in the Submariner documentation.

To view the main documentation for the Submariner networking service and
service discovery, see Submariner multicluster networking and service
discovery.

## Running the must-gather command to troubleshoot Red Hat Advanced Cluster Management components

To get started with troubleshooting, learn about the troubleshooting
scenarios for users to run the `must-gather` command to debug the
issues, then see the procedures to start using the command.

**Required access:** Cluster administrator

### Must-gather scenarios

- **Scenario one:** Use the Documented troubleshooting section to see if
  a solution to your problem is documented. The guide is organized by
  the major functions of the product.

  With this scenario, you check the guide to see if your solution is in
  the documentation. For instance, for trouble with creating a cluster,
  you might find a solution in the *Manage cluster* section.

- **Scenario two:** If your problem is not documented with steps to
  resolve, run the `must-gather` command and use the output to debug the
  issue.

- **Scenario three:** If you cannot debug the issue using your output
  from the `must-gather` command, then share your output with Red Hat
  Support.

### Must-gather procedure

See the following procedure to start using the `must-gather` command:

1.  Learn about the `must-gather` command and install the prerequisites
    that you need at Gathering data about your cluster in the Red Hat
    OpenShift Container Platform documentation.

2.  Log in to your cluster. Add the Red Hat Advanced Cluster Management
    for Kubernetes image that is used for gathering data and the
    directory. Run the following command, where you insert the image and
    the directory for the output:

        oc adm must-gather --image=registry.redhat.io/rhacm2/acm-must-gather-rhel9:v2.15 --dest-dir=<directory>

3.  For the usual use-case, you should run the `must-gather` while you
    are logged into your *hub* cluster.

    **Note:** If you want to check your managed clusters, find the
    `gather-managed.log` file that is located in the
    `cluster-scoped-resources` directory:

        <your-directory>/cluster-scoped-resources/gather-managed.log>

    Check for managed clusters that are not set `True` for the JOINED
    and AVAILABLE column. You can run the `must-gather` command on those
    clusters that are not connected with `True` status.

4.  Go to your specified directory to see your output, which is
    organized in the following levels:

    - Two peer levels: `cluster-scoped-resources` and `namespace`
      resources.

    - Sub-level for each: API group for the custom resource definitions
      for both cluster-scope and namespace-scoped resources.

    - Next level for each: YAML file sorted by `kind`.

### Must-gather in a disconnected environment

Complete the following steps to run the `must-gather` command in a
disconnected environment:

1.  In a disconnected environment, mirror the Red Hat operator catalog
    images into their mirror registry. For more information, see
    Installing in disconnected network environments.

2.  Run the following commands to collect all of the information,
    replacing `<2.x>` with the supported version for both
    `<acm-must-gather>`, for example `2.14`, and
    `<multicluster-engine/must-gather>`, for example `2.9`.

        REGISTRY=<internal.repo.address:port>
        IMAGE1=$REGISTRY/rhacm2/acm-must-gather-rhel9:v<2.x>
        oc adm must-gather --image=$IMAGE1 --dest-dir=<directory>

If you experience issues with one of the currently supported releases,
or the product documentation, go to Red Hat Support where you can
troubleshoot further, view Knowledgebase articles, connect with the
Support Team, or open a case. You must log in with your Red Hat
credentials.

## Running the *must-gather* command to troubleshoot issues with multicluster global hub

You can run the `must-gather` command for troubleshooting issues with
multicluster global hub. Run the must-gather command to gather details,
logs, and take steps in debugging issues. This debugging information is
also useful when you open a support request.

The `oc adm must-gather` command collects the information from your
cluster that is often needed for debugging issues, including information
for the following items:

- Resource definitions

- Service logs

### Prerequisites

You must meet the following prerequisites to run the `must-gather`
command:

- Access to the global hub and managed hub clusters as a user with the
  `cluster-admin` role.

- Install the OpenShift Container Platform command-line interface on
  your local machine. For more information, see the Getting started with
  the OpenShift CLI in the OpenShift Container Platform documentation.

- Learn about the `must-gather` command and install the prerequisites
  that you need by reading the Gathering data about your cluster in the
  OpenShift Container Platform documentation.

### Running the must-gather command

Complete the following procedure to collect information by using the
must-gather command:

1.  Log in to your global hub cluster

2.  Run the following command:

    ``` bash
    oc adm must-gather --image=registry.redhat.io/rhacm2/acm-must-gather-rhel9:v2.15 --dest-dir=<directory>
    ```

3.  If you want to check your managed hub clusters, run the
    `must-gather` command on those clusters.

Information is collected for the following resources:

- Two peer levels: `cluster-scoped-resources` and `namespaces`
  resources.

- Sub-level for each: API group for the custom resource definitions for
  both cluster-scope and namespace-scoped resources.

- Next level for each: YAML file sorted by `kind`.

- For the multicluster global hub cluster, you can check the
  `PostgresCluster` and `Kafka` in the `namespaces` resources.

- For the global hub cluster, you can check the multicluster global hub
  related pods and logs in `pods` of `namespaces` resources.

- For the managed hub cluster, you can check the multicluster global hub
  agent pods and logs in `pods` of `namespaces` resources.

## Must-gather procedure for the Red Hat Edge Manager agent

To debug the Red Hat Edge Manager agent on your devices, you can use the
`flightctl-must-gather` command.

**Required access:** Cluster administrator

See the following procedure:

1.  Run the following command on the device that you want to debug:

``` bash
sudo flightctl-must-gather
```

## Troubleshooting installation status stuck in installing or pending

When installing Red Hat Advanced Cluster Management, the
`MultiClusterHub` remains in `Installing` phase, or multiple pods
maintain a `Pending` status.

### Symptom: Stuck in Pending status

More than ten minutes passed since you installed `MultiClusterHub` and
one or more components from the `status.components` field of the
`MultiClusterHub` resource report `ProgressDeadlineExceeded`. Resource
constraints on the cluster might be the issue.

Check the pods in the namespace where `Multiclusterhub` was installed.
You might see `Pending` with a status similar to the following:

    reason: Unschedulable
    message: '0/6 nodes are available: 3 Insufficient cpu, 3 node(s) had taint {node-role.kubernetes.io/master:
            }, that the pod didn't tolerate.'

In this case, the worker nodes resources are not sufficient in the
cluster to run the product.

### Resolving the problem: Adjust worker node sizing

If you have this problem, then your cluster needs to be updated with
either larger or more worker nodes. See Sizing your cluster for
guidelines on sizing your cluster.

## Troubleshooting an offline cluster

There are a few common causes for a cluster showing an offline status.

### Symptom: Cluster status is offline

After you complete the procedure for creating a cluster, you cannot
access it from the Red Hat Advanced Cluster Management console, and it
shows a status of `offline`.

### Resolving the problem: Cluster status is offline

1.  Determine if the managed cluster is available. You can check this in
    the *Clusters* area of the Red Hat Advanced Cluster Management
    console.

    If it is not available, try restarting the managed cluster.

2.  If the managed cluster status is still offline, complete the
    following steps:

    1.  Run the `oc get managedcluster <cluster_name> -o yaml` command
        on the hub cluster. Replace `<cluster_name>` with the name of
        your cluster.

    2.  Find the `status.conditions` section.

    3.  Check the messages for `type: ManagedClusterConditionAvailable`
        and resolve any problems.

## Troubleshooting a managed cluster import failure

If your cluster import fails, there are a few steps that you can take to
determine why the cluster import failed.

### Symptom: Imported cluster not available

After you complete the procedure for importing a cluster, you cannot
access it from the Red Hat Advanced Cluster Management for Kubernetes
console.

### Resolving the problem: Imported cluster not available

There can be a few reasons why an imported cluster is not available
after an attempt to import it. If the cluster import fails, complete the
following steps, until you find the reason for the failed import:

1.  On the Red Hat Advanced Cluster Management hub cluster, run the
    following command to ensure that the Red Hat Advanced Cluster
    Management import controller is running.

        kubectl -n multicluster-engine get pods -l app=managedcluster-import-controller-v2

    You should see two pods that are running. If either of the pods is
    not running, run the following command to view the log to determine
    the reason:

        kubectl -n multicluster-engine logs -l app=managedcluster-import-controller-v2 --tail=-1

2.  On the Red Hat Advanced Cluster Management hub cluster, run the
    following command to determine if the managed cluster import secret
    was generated successfully by the Red Hat Advanced Cluster
    Management import controller:

        kubectl -n <managed_cluster_name> get secrets <managed_cluster_name>-import

    If the import secret does not exist, run the following command to
    view the log entries for the import controller and determine why it
    was not created:

        kubectl -n multicluster-engine logs -l app=managedcluster-import-controller-v2 --tail=-1 | grep importconfig-controller

3.  On the Red Hat Advanced Cluster Management hub cluster, if your
    managed cluster is the `local-cluster`, which is provisioned by
    Hive, or has an auto-import secret, run the following command to
    check the import status of the managed cluster.

        kubectl get managedcluster <managed_cluster_name> -o=jsonpath='{range .status.conditions[*]}{.type}{"\t"}{.status}{"\t"}{.message}{"\n"}{end}' | grep ManagedClusterImportSucceeded

    If the condition `ManagedClusterImportSucceeded` is not `true`, the
    result of the command indicates the reason for the failure.

4.  Check the Klusterlet status of the managed cluster for a degraded
    condition. See Troubleshooting Klusterlet with degraded conditions
    to find the reason that the Klusterlet is degraded.

## Troubleshooting cluster with pending import status

If you receive *Pending import* continually on the console of your
cluster, follow the procedure to troubleshoot the problem.

### Symptom: Cluster with pending import status

After importing a cluster by using the Red Hat Advanced Cluster
Management console, the cluster appears in the console with a status of
*Pending import*.

### Identifying the problem: Cluster with pending import status

1.  Run the following command on the managed cluster to view the
    Kubernetes pod names that are having the issue:

        kubectl get pod -n open-cluster-management-agent | grep klusterlet-agent

2.  Run the following command on the managed cluster to find the log
    entry for the error:

        kubectl logs <klusterlet_agent_pod> -n open-cluster-management-agent

    Replace *klusterlet_agent_pod* with the pod name that you identified
    in step 1.

3.  Search the returned results for text that indicates there was a
    networking connectivity problem. Example includes: `no such host`.

### Resolving the problem: Cluster with pending import status

1.  Retrieve the port number that is having the problem by entering the
    following command on the hub cluster:

        oc get infrastructure cluster -o yaml | grep apiServerURL

2.  Ensure that the hostname from the managed cluster can be resolved,
    and that outbound connectivity to the host and port is occurring.

    If the communication cannot be established by the managed cluster,
    the cluster import is not complete. The cluster status for the
    managed cluster is *Pending import*.

## Troubleshooting cluster with already exists error

If you are unable to import an OpenShift Container Platform cluster into
Red Hat Advanced Cluster Management `MultiClusterHub` and receive an
`AlreadyExists` error, follow the procedure to troubleshoot the problem.

### Symptom

An error log shows up when importing an OpenShift Container Platform
cluster into Red Hat Advanced Cluster Management `MultiClusterHub`:

    error log:
    Warning: apiextensions.k8s.io/v1beta1 CustomResourceDefinition is deprecated in v1.16+, unavailable in v1.22+; use apiextensions.k8s.io/v1 CustomResourceDefinition
    Error from server (AlreadyExists): error when creating "STDIN": customresourcedefinitions.apiextensions.k8s.io "klusterlets.operator.open-cluster-management.io" already exists
    The cluster cannot be imported because its Klusterlet CRD already exists.
    Either the cluster was already imported, or it was not detached completely during a previous detach process.
    Detach the existing cluster before trying the import again."

### Identifying the problem

Check if there are any Red Hat Advanced Cluster Management-related
resources on the cluster that you want to import to new the Red Hat
Advanced Cluster Management `MultiClusterHub` by running the following
commands:

    oc get all -n open-cluster-management-agent
    oc get all -n open-cluster-management-agent-addon

### Resolving the problem: Already exists when importing OpenShift Container Platform cluster

Remove the `klusterlet` custom resource by using the following command:

``` bash
oc get klusterlet | grep klusterlet | awk '{print $1}' | xargs oc patch klusterlet --type=merge -p '{"metadata":{"finalizers": []}}'
```

Run the following commands to remove pre-existing resources:

    oc delete namespaces open-cluster-management-agent open-cluster-management-agent-addon --wait=false
    oc get crds | grep open-cluster-management.io | awk '{print $1}' | xargs oc delete crds --wait=false
    oc get crds | grep open-cluster-management.io | awk '{print $1}' | xargs oc patch crds --type=merge -p '{"metadata":{"finalizers": []}}'

## Troubleshooting cluster creation on VMware vSphere

If you experience a problem when creating a Red Hat OpenShift Container
Platform cluster on VMware vSphere, see the following troubleshooting
information to see if one of them addresses your problem.

**Note:** Sometimes when the cluster creation process fails on VMware
vSphere, the link is not enabled for you to view the logs. If this
happens, you can identify the problem by viewing the log of the
`hive-controllers` pod. The `hive-controllers` log is in the `hive`
namespace.

### Managed cluster creation fails with certificate IP SAN error

#### Symptom: Managed cluster creation fails with certificate IP SAN error

After creating a new Red Hat OpenShift Container Platform cluster on
VMware vSphere, the cluster fails with an error message that indicates a
certificate IP SAN error.

#### Identifying the problem: Managed cluster creation fails with certificate IP SAN error

The deployment of the managed cluster fails and returns the following
errors in the deployment log:

    time="2020-08-07T15:27:55Z" level=error msg="Error: error setting up new vSphere SOAP client: Post https://147.1.1.1/sdk: x509: cannot validate certificate for xx.xx.xx.xx because it doesn't contain any IP SANs"
    time="2020-08-07T15:27:55Z" level=error

#### Resolving the problem: Managed cluster creation fails with certificate IP SAN error

Use the VMware vCenter server fully-qualified host name instead of the
IP address in the credential. You can also update the VMware vCenter CA
certificate to contain the IP SAN.

### Managed cluster creation fails with unknown certificate authority

#### Symptom: Managed cluster creation fails with unknown certificate authority

After creating a new Red Hat OpenShift Container Platform cluster on
VMware vSphere, the cluster fails because the certificate is signed by
an unknown authority.

#### Identifying the problem: Managed cluster creation fails with unknown certificate authority

The deployment of the managed cluster fails and returns the following
errors in the deployment log:

    Error: error setting up new vSphere SOAP client: Post https://vspherehost.com/sdk: x509: certificate signed by unknown authority"

#### Resolving the problem: Managed cluster creation fails with unknown certificate authority

Ensure you entered the correct certificate from the certificate
authority when creating the credential.

### Managed cluster creation fails with expired certificate

#### Symptom: Managed cluster creation fails with expired certificate

After creating a new Red Hat OpenShift Container Platform cluster on
VMware vSphere, the cluster fails because the certificate is expired or
is not yet valid.

#### Identifying the problem: Managed cluster creation fails with expired certificate

The deployment of the managed cluster fails and returns the following
errors in the deployment log:

    x509: certificate has expired or is not yet valid

#### Resolving the problem: Managed cluster creation fails with expired certificate

Ensure that the time on your ESXi hosts is synchronized.

### Managed cluster creation fails with insufficient privilege for tagging

#### Symptom: Managed cluster creation fails with insufficient privilege for tagging

After creating a new Red Hat OpenShift Container Platform cluster on
VMware vSphere, the cluster fails because there is insufficient
privilege to use tagging.

#### Identifying the problem: Managed cluster creation fails with insufficient privilege for tagging

The deployment of the managed cluster fails and returns the following
errors in the deployment log:

    time="2020-08-07T19:41:58Z" level=debug msg="vsphere_tag_category.category: Creating..."
    time="2020-08-07T19:41:58Z" level=error
    time="2020-08-07T19:41:58Z" level=error msg="Error: could not create category: POST https://vspherehost.com/rest/com/vmware/cis/tagging/category: 403 Forbidden"
    time="2020-08-07T19:41:58Z" level=error
    time="2020-08-07T19:41:58Z" level=error msg="  on ../tmp/openshift-install-436877649/main.tf line 54, in resource \"vsphere_tag_category\" \"category\":"
    time="2020-08-07T19:41:58Z" level=error msg="  54: resource \"vsphere_tag_category\" \"category\" {"

#### Resolving the problem: Managed cluster creation fails with insufficient privilege for tagging

Ensure that your VMware vCenter required account privileges are correct.
See Installer-provisioned infrastructure for more information.

### Managed cluster creation fails with invalid dnsVIP

#### Symptom: Managed cluster creation fails with invalid dnsVIP

After creating a new Red Hat OpenShift Container Platform cluster on
VMware vSphere, the cluster fails because there is an invalid dnsVIP.

#### Identifying the problem: Managed cluster creation fails with invalid dnsVIP

If you see the following message when trying to deploy a new managed
cluster with VMware vSphere, it is because you have an older OpenShift
Container Platform release image that does not support VMware Installer
Provisioned Infrastructure (IPI):

    failed to fetch Master Machines: failed to load asset \\\"Install Config\\\": invalid \\\"install-config.yaml\\\" file: platform.vsphere.dnsVIP: Invalid value: \\\"\\\": \\\"\\\" is not a valid IP

#### Resolving the problem: Managed cluster creation fails with invalid dnsVIP

Select a release image from a later version of OpenShift Container
Platform that supports VMware Installer Provisioned Infrastructure.

### Managed cluster creation fails with incorrect network type

#### Symptom: Managed cluster creation fails with incorrect network type

After creating a new Red Hat OpenShift Container Platform cluster on
VMware vSphere, the cluster fails because there is an incorrect network
type specified.

#### Identifying the problem: Managed cluster creation fails with incorrect network type

If you see the following message when trying to deploy a new managed
cluster with VMware vSphere, it is because you have an older OpenShift
Container Platform image that does not support VMware Installer
Provisioned Infrastructure (IPI):

    time="2020-08-11T14:31:38-04:00" level=debug msg="vsphereprivate_import_ova.import: Creating..."
    time="2020-08-11T14:31:39-04:00" level=error
    time="2020-08-11T14:31:39-04:00" level=error msg="Error: rpc error: code = Unavailable desc = transport is closing"
    time="2020-08-11T14:31:39-04:00" level=error
    time="2020-08-11T14:31:39-04:00" level=error
    time="2020-08-11T14:31:39-04:00" level=fatal msg="failed to fetch Cluster: failed to generate asset \"Cluster\": failed to create cluster: failed to apply Terraform: failed to complete the change"

#### Resolving the problem: Managed cluster creation fails with incorrect network type

Select a valid VMware vSphere network type for the specified VMware
cluster.

### Managed cluster creation fails with an error processing disk changes

#### Symptom: Adding the VMware vSphere managed cluster fails due to an error processing disk changes

After creating a new Red Hat OpenShift Container Platform cluster on
VMware vSphere, the cluster fails because there is an error when
processing disk changes.

#### Identifying the problem: Adding the VMware vSphere managed cluster fails due to an error processing disk changes

A message similar to the following is displayed in the logs:

    ERROR
    ERROR Error: error reconfiguring virtual machine: error processing disk changes post-clone: disk.0: ServerFaultCode: NoPermission: RESOURCE (vm-71:2000), ACTION (queryAssociatedProfile): RESOURCE (vm-71), ACTION (PolicyIDByVirtualDisk)

#### Resolving the problem: Adding the VMware vSphere managed cluster fails due to an error processing disk changes

Use the VMware vSphere client to give the user **All privileges** for
*Profile-driven Storage Privileges*.

## Troubleshooting managed cluster creation fails on Red Hat OpenStack Platform with unknown authority error

If you experience a problem when creating a Red Hat OpenShift Container
Platform cluster on Red Hat OpenStack Platform, see the following
troubleshooting information to see if one of them addresses your
problem.

### Symptom: Managed cluster creation fails with unknown authority error

After creating a new Red Hat OpenShift Container Platform cluster on Red
Hat OpenStack Platform using self-signed certificates, the cluster fails
with an error message that indicates an unknown authority error.

### Identifying the problem: Managed cluster creation fails with unknown authority error

The deployment of the managed cluster fails and returns the following
error message:

`x509: certificate signed by unknown authority`

### Resolving the problem: Managed cluster creation fails with unknown authority error

Verify that the following files are configured correctly:

1.  The `clouds.yaml` file must specify the path to the `ca.crt` file in
    the `cacert` parameter. The `cacert` parameter is passed to the
    OpenShift installer when generating the ignition shim. See the
    following example:

    ``` yaml
    clouds:
      openstack:
        cacert: "/etc/pki/ca-trust/source/anchors/ca.crt"
    ```

2.  The `certificatesSecretRef` paremeter must reference a secret with a
    file name matching the `ca.crt` file. See the following example:

    ``` yaml
    spec:
      baseDomain: dev09.red-chesterfield.com
      clusterName: txue-osspoke
      platform:
        openstack:
          cloud: openstack
          credentialsSecretRef:
            name: txue-osspoke-openstack-creds
          certificatesSecretRef:
            name: txue-osspoke-openstack-certificatebundle
    ```

    To create a secret with a matching file name, run the following
    command:

        oc create secret generic txue-osspoke-openstack-certificatebundle --from-file=ca.crt=ca.crt.pem -n $CLUSTERNAME

3.  The size of the `ca.cert` file must be less than 63 thousand bytes.

## Troubleshooting imported clusters offline after certificate change

Installing a custom `apiserver` certificate is supported, but one or
more clusters that were imported before you changed the certificate
information are in `offline` status.

### Symptom: Clusters offline after certificate change

After you complete the procedure for updating a certificate secret, one
or more of your clusters that were online now display `offline` status
in the console.

### Identifying the problem: Clusters offline after certificate change

After updating the information for a custom API server certificate,
clusters that were imported and running before the new certificate are
now in an `offline` state.

The errors that indicate that the certificate is the problem are found
in the logs for the pods in the `open-cluster-management-agent`
namespace of the offline managed cluster. The following examples are
similar to the errors that are displayed in the logs:

See the following `klusterlet-agent` log:

    E0917 02:58:26.315984       1 reflector.go:127] k8s.io/client-go@v0.19.0/tools/cache/reflector.go:156: Failed to watch *v1beta1.CertificateSigningRequest: Get "https://api.aaa-ocp.dev02.location.com:6443/apis/cluster.management.io/v1/managedclusters?allowWatchBookmarks=true&fieldSelector=metadata.name%3Dtest-1&resourceVersion=607408&timeout=9m33s&timeoutSeconds=573&watch=true"": x509: certificate signed by unknown authority
    E0917 02:58:26.598343       1 reflector.go:127] k8s.io/client-go@v0.19.0/tools/cache/reflector.go:156: Failed to watch *v1.ManagedCluster: Get "https://api.aaa-ocp.dev02.location.com:6443/apis/cluster.management.io/v1/managedclusters?allowWatchBookmarks=true&fieldSelector=metadata.name%3Dtest-1&resourceVersion=607408&timeout=9m33s&timeoutSeconds=573&watch=true": x509: certificate signed by unknown authority
    E0917 02:58:27.613963       1 reflector.go:127] k8s.io/client-go@v0.19.0/tools/cache/reflector.go:156: Failed to watch *v1.ManagedCluster: failed to list *v1.ManagedCluster: Get "https://api.aaa-ocp.dev02.location.com:6443/apis/cluster.management.io/v1/managedclusters?allowWatchBookmarks=true&fieldSelector=metadata.name%3Dtest-1&resourceVersion=607408&timeout=9m33s&timeoutSeconds=573&watch=true"": x509: certificate signed by unknown authority
    E0917 03:04:05.874759       1 manifestwork_controller.go:179] Reconcile work test-1-klusterlet-addon-workmgr fails with err: Failed to update work status with err Get "https://api.aaa-ocp.dev02.location.com:6443/apis/cluster.management.io/v1/namespaces/test-1/manifestworks/test-1-klusterlet-addon-workmgr": x509: certificate signed by unknown authority
    E0917 03:04:05.874887       1 base_controller.go:231] "ManifestWorkAgent" controller failed to sync "test-1-klusterlet-addon-workmgr", err: Failed to update work status with err Get "api.aaa-ocp.dev02.location.com:6443/apis/cluster.management.io/v1/namespaces/test-1/manifestworks/test-1-klusterlet-addon-workmgr": x509: certificate signed by unknown authority
    E0917 03:04:37.245859       1 reflector.go:127] k8s.io/client-go@v0.19.0/tools/cache/reflector.go:156: Failed to watch *v1.ManifestWork: failed to list *v1.ManifestWork: Get "api.aaa-ocp.dev02.location.com:6443/apis/cluster.management.io/v1/namespaces/test-1/manifestworks?resourceVersion=607424": x509: certificate signed by unknown authority

### Resolving the problem: Clusters offline after certificate change

If you want to recover a managed cluster, complete the following steps
to import the managed cluster again:

1.  On the hub cluster, recreate the managed cluster import secret by
    running the following command:

        oc delete secret -n <cluster_name> <cluster_name>-import

    Replace `<cluster_name>` with the name of the managed cluster that
    you want to import.

2.  On the hub cluster, expose the managed cluster import secret to a
    YAML file by running the following command:

        oc get secret -n <cluster_name> <cluster_name>-import -ojsonpath='{.data.import\.yaml}' | base64 --decode  > import.yaml

    Replace `<cluster_name>` with the name of the managed cluster that
    you want to import.

3.  On the managed cluster, apply the `import.yaml` file by running the
    following command:

        oc apply -f import.yaml

**Note:** The previous steps do not detach the managed cluster from the
hub cluster. The steps update the required manifests with current
settings on the managed cluster, including the new certificate
information.

## Namespace remains after deleting a cluster

When you remove a managed cluster, the namespace is normally removed as
part of the cluster removal process. In rare cases, the namespace
remains with some artifacts in it. In that case, you must manually
remove the namespace.

### Symptom: Namespace remains after deleting a cluster

After removing a managed cluster, the namespace is not removed.

### Resolving the problem: Namespace remains after deleting a cluster

Complete the following steps to remove the namespace manually:

1.  Run the following command to produce a list of the resources that
    remain in the \<cluster_name\> namespace:

        oc api-resources --verbs=list --namespaced -o name | grep -E '^secrets|^serviceaccounts|^managedclusteraddons|^roles|^rolebindings|^manifestworks|^leases|^managedclusterinfo|^appliedmanifestworks'|^clusteroauths' | xargs -n 1 oc get --show-kind --ignore-not-found -n <cluster_name>

    Replace `cluster_name` with the name of the namespace for the
    cluster that you attempted to remove.

2.  Delete each identified resource on the list that does not have a
    status of `Delete` by entering the following command to edit the
    list:

        oc edit <resource_kind> <resource_name> -n <namespace>

    Replace `resource_kind` with the kind of the resource. Replace
    `resource_name` with the name of the resource. Replace `namespace`
    with the name of the namespace of the resource.

3.  Locate the `finalizer` attribute in the in the metadata.

4.  Delete the non-Kubernetes finalizers by using the vi editor `dd`
    command.

5.  Save the list and exit the `vi` editor by entering the `:wq`
    command.

6.  Delete the namespace by entering the following command:

        oc delete ns <cluster-name>

    Replace `cluster-name` with the name of the namespace that you are
    trying to delete.

## Auto-import-secret-exists error when importing a cluster

Your cluster import fails with an error message that reads: auto import
secret exists.

### Symptom: Auto import secret exists error when importing a cluster

When importing a hive cluster for management, an
`auto-import-secret already exists` error is displayed.

### Resolving the problem: Auto-import-secret-exists error when importing a cluster

This problem occurs when you attempt to import a cluster that was
previously managed by Red Hat Advanced Cluster Management. When this
happens, the secrets conflict when you try to reimport the cluster.

To work around this problem, complete the following steps:

1.  To manually delete the existing `auto-import-secret`, run the
    following command on the hub cluster:

        oc delete secret auto-import-secret -n <cluster-namespace>

    Replace `cluster-namespace` with the namespace of your cluster.

2.  Import your cluster again by using the procedure in Cluster import
    introduction.

## Troubleshooting the cinder Container Storage Interface (CSI) driver for VolSync

If you use VolSync or use a default setting in a cinder Container
Storage Interface (CSI) driver, you might encounter errors for the PVC
that is in use.

### Symptom: `Volumesnapshot` error state

You can configure a VolSync `ReplicationSource` or
`ReplicationDestination` to use snapshots. Also, you can configure the
`storageclass` and `volumesnapshotclass` in the `ReplicationSource` and
`ReplicationDestination`. There is a parameter on the cinder
`volumesnapshotclass` called `force-create` with a default value of
`false`. This `force-create` parameter on the `volumesnapshotclass`
means cinder does not allow the `volumesnapshot` to be taken of a PVC in
use. As a result, the `volumesnapshot` is in an error state.

### Resolving the problem: Setting the parameter to `true`

1.  Create a new `volumesnapshotclass` for the cinder CSI driver.

2.  Change the paramater, `force-create`, to `true`. See the following
    sample YAML:

    ``` yaml
    apiVersion: snapshot.storage.k8s.io/v1
    deletionPolicy: Delete
    driver: cinder.csi.openstack.org
    kind: VolumeSnapshotClass
    metadata:
      annotations:
        snapshot.storage.kubernetes.io/is-default-class: 'true'
      name: standard-csi
    parameters:
      force-create: 'true'
    ```

## Troubleshooting by accessing the PostgreSQL database

### Symptom: Errors with multicluster global hub

You might experience various errors with multicluster global hub. You
can access the provisioned PostgreSQL database to view messages that
might be helpful for troubleshooting issues with multicluster global
hub.

### Resolving the problem: Accessing the PostgresSQL database

    There are two ways to access the provisioned PostgreSQL database.

- Using the `ClusterIP` service

      oc exec -it multicluster-global-hub-postgresql-0 -c multicluster-global-hub-postgresql -n multicluster-global-hub -- psql -U postgres -d hoh

      # Or access the database installed by crunchy operator
      oc exec -it $(kubectl get pods -n multicluster-global-hub -l postgres-operator.crunchydata.com/role=master -o jsonpath='{.items..metadata.name}') -c database -n multicluster-global-hub -- psql -U postgres -d hoh -c "SELECT 1"

- `LoadBalancer`

  - Expose the service type to `LoadBalancer` provisioned by default:

        cat <<EOF | oc apply -f -
        apiVersion: v1
        kind: Service
        metadata:
          name: multicluster-global-hub-postgresql-lb
          namespace: multicluster-global-hub
        spec:
          ports:
          - name: postgres
            port: 5432
            protocol: TCP
            targetPort: 5432
          selector:
            name: multicluster-global-hub-postgresql
          type: LoadBalancer
        EOF

    Run the following command to get your the credentials:

        # Host
        oc get svc multicluster-global-hub-postgresql-lb -n multicluster-global-hub -ojsonpath='{.status.loadBalancer.ingress[0].hostname}'

        # Database URI
        oc get secret storage-config -n multicluster-global-hub -ojsonpath='{.data.database-url}' | base64 -d

        # Database CA
        oc get secret storage-config -ojsonpath='{.data.ca\.crt}' | base64 -d

  - Expose the service type to `LoadBalancer` provisioned by crunchy
    operator:

        oc patch postgrescluster postgres -n multicluster-global-hub -p '{"spec":{"service":{"type":"LoadBalancer"}}}'  --type merge

    Run the following command to get your the credentials:

        # Host
        oc get svc -n multicluster-global-hub postgres-ha -ojsonpath='{.status.loadBalancer.ingress[0].hostname}'

        # Username
        oc get secrets -n multicluster-global-hub postgres-pguser-postgres -o go-template='{{index (.data) "user" | base64decode}}'

        # Password
        oc get secrets -n multicluster-global-hub postgres-pguser-postgres -o go-template='{{index (.data) "password" | base64decode}}'

        # Database
        oc get secrets -n multicluster-global-hub postgres-pguser-postgres -o go-template='{{index (.data) "dbname" | base64decode}}'

## Troubleshooting by using the database dump and restore

In a production environment, back up your PostgreSQL database regularly
as a database management task. The backup can also be used for debugging
the multicluster global hub.

### Symptom: Errors with multicluster global hub

You might experience various errors with multicluster global hub. You
can use the database dump and restore for troubleshooting issues with
multicluster global hub.

### Resolving the problem: Dumping the output of the database for dubugging

Sometimes you need to dump the output in the multicluster global hub
database to debug a problem. The PostgreSQL database provides the
`pg_dump` command line tool to dump the contents of the database. To
dump data from localhost database server, run the following command:

    pg_dump hoh > hoh.sql

To dump the multicluster global hub database located on a remote server
with compressed format, use the command-line options to control the
connection details, as shown in the following example:

    pg_dump -h my.host.com -p 5432 -U postgres -F t hoh -f hoh-$(date +%d-%m-%y_%H-%M).tar

### Resolving the problem: Restore database from dump

To restore a PostgreSQL database, you can use the `psql` or `pg_restore`
command line tools. The `psql` tool is used to restore plain text files
created by `pg_dump`:

    psql -h another.host.com -p 5432 -U postgres -d hoh < hoh.sql

The `pg_restore` tool is used to restore a PostgreSQL database from an
archive created by `pg_dump` in one of the non-plain-text formats
(custom, tar, or directory):

    pg_restore -h another.host.com -p 5432 -U postgres -d hoh hoh-$(date +%d-%m-%y_%H-%M).tar

## Troubleshooting cluster status changing from offline to available

The status of the managed cluster alternates between `offline` and
`available` without any manual change to the environment or cluster.

### Symptom: Cluster status changing from offline to available

When the network that connects the managed cluster to the hub cluster is
unstable, the status of the managed cluster that is reported by the hub
cluster cycles between `offline` and `available`.

The connection between the hub cluster and managed cluster is maintained
through a lease that is validated at the `leaseDurationSeconds` interval
value. If the lease is not validated within five consecutive attempts of
the `leaseDurationSeconds` value, then the cluster is marked `offline`.

For example, the cluster is marked `offline` after five minutes with a
`leaseDurationSeconds` interval of `60 seconds`. This configuration can
be inadequate for reasons such as connectivity issues or latency,
causing instability.

### Resolving the problem: Cluster status changing from offline to available

The five validation attempts is default and cannot be changed, but you
can change the `leaseDurationSeconds` interval.

Determine the amount of time, in minutes, that you want the cluster to
be marked as `offline`, then multiply that value by 60 to convert to
seconds. Then divide by the default five number of attempts. The result
is your `leaseDurationSeconds` value.

1.  Edit your `ManagedCluster` specification on the hub cluster by
    entering the following command, but replace `cluster-name` with the
    name of your managed cluster:

        oc edit managedcluster <cluster-name>

2.  Increase the value of `leaseDurationSeconds` in your
    `ManagedCluster` specification, as seen in the following sample
    YAML:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1
    kind: ManagedCluster
    metadata:
      name: <cluster-name>
    spec:
      hubAcceptsClient: true
      leaseDurationSeconds: 60
    ```

3.  Save and apply the file.

## Troubleshooting cluster in console with pending or failed status

If you observe *Pending* status or *Failed* status in the console for a
cluster you created, follow the procedure to troubleshoot the problem.

### Symptom: Cluster in console with pending or failed status

After creating a new cluster by using the Red Hat Advanced Cluster
Management for Kubernetes console, the cluster does not progress beyond
the status of *Pending* or displays *Failed* status.

### Identifying the problem: Cluster in console with pending or failed status

If the cluster displays *Failed* status, navigate to the details page
for the cluster and follow the link to the logs provided. If no logs are
found or the cluster displays *Pending* status, continue with the
following procedure to check for logs:

- Procedure 1

  1.  Run the following command on the hub cluster to view the names of
      the Kubernetes pods that were created in the namespace for the new
      cluster:

          oc get pod -n <new_cluster_name>

      Replace `new_cluster_name` with the name of the cluster that you
      created.

  2.  If no pod that contains the string `provision` in the name is
      listed, continue with Procedure 2. If there is a pod with
      `provision` in the title, run the following command on the hub
      cluster to view the logs of that pod:

          oc logs <new_cluster_name_provision_pod_name> -n <new_cluster_name> -c hive

      Replace `new_cluster_name_provision_pod_name` with the name of the
      cluster that you created, followed by the pod name that contains
      `provision`.

  3.  Search for errors in the logs that might explain the cause of the
      problem.

- Procedure 2

  If there is not a pod with `provision` in its name, the problem
  occurred earlier in the process. Complete the following procedure to
  view the logs:

  1.  Run the following command on the hub cluster:

          oc describe clusterdeployments -n <new_cluster_name>

      Replace `new_cluster_name` with the name of the cluster that you
      created. For more information about cluster installation logs, see
      Gathering installation logs in the Red Hat OpenShift
      documentation.

  2.  See if there is additional information about the problem in the
      *Status.Conditions.Message* and *Status.Conditions.Reason* entries
      of the resource.

### Resolving the problem: Cluster in console with pending or failed status

After you identify the errors in the logs, determine how to resolve the
errors before you destroy the cluster and create it again.

The following example provides a possible log error of selecting an
unsupported zone, and the actions that are required to resolve it:

    No subnets provided for zones

When you created your cluster, you selected one or more zones within a
region that are not supported. Complete one of the following actions
when you recreate your cluster to resolve the issue:

- Select a different zone within the region.

- Omit the zone that does not provide the support, if you have other
  zones listed.

- Select a different region for your cluster.

After determining the issues from the log, destroy the cluster and
recreate it.

See Creating clusters for more information about creating a cluster.

## Troubleshooting Grafana

When you query some time-consuming metrics in the Grafana explorer, you
might encounter a `Gateway Time-out` error.

### Symptom: Grafana explorer gateway timeout

If you hit the `Gateway Time-out` error when you query some
time-consuming metrics in the Grafana explorer, it is possible that the
timeout is caused by the Grafana in the
`open-cluster-management-observability` namespace.

### Resolving the problem: Configure the Grafana

If you have this problem, complete the following steps:

1.  Verify that the default configuration of Grafana has expected
    timeout settings:

    1.  To verify that the default timeout setting of Grafana, run the
        following command:

            oc get secret grafana-config -n open-cluster-management-observability -o jsonpath="{.data.grafana\.ini}" | base64 -d | grep dataproxy -A 4

        The following timeout settings should be displayed:

            [dataproxy]
            timeout = 300
            dial_timeout = 30
            keep_alive_seconds = 300

    2.  To verify the default data source query timeout for Grafana, run
        the following command:

            oc get secret/grafana-datasources -n open-cluster-management-observability -o jsonpath="{.data.datasources\.yaml}" | base64 -d | grep queryTimeout

        The following timeout settings should be displayed:

            queryTimeout: 300s

2.  If you verified the default configuration of Grafana has expected
    timeout settings, then you can configure the Grafana in the
    `open-cluster-management-observability` namespace by running the
    following command:

        oc annotate route grafana -n open-cluster-management-observability --overwrite haproxy.router.openshift.io/timeout=300s

Refresh the Grafana page and try to query the metrics again. The
`Gateway Time-out` error is no longer displayed.

## Troubleshooting local cluster not selected with placement rule

The managed clusters are selected with a placement rule, but the
`local-cluster`, which is a hub cluster that is also managed, is not
selected. The placement rule user is not granted permission to get the
`managedcluster` resources in the `your-local-cluster-name` namespace.

### Symptom: Troubleshooting local cluster not selected as a managed cluster

All managed clusters are selected with a placement rule, but the
`local-cluster` is not. The placement rule user is not granted
permission to get the `managedcluster` resources in the
`your-local-cluster-name` namespace.

### Resolving the problem: Troubleshooting local cluster not selected as a managed cluster

**Deprecated:** `PlacementRule`

To resolve this issue, you need to grant the `managedcluster`
administrative permission in the `your-local-cluster-name` namespace.
Complete the following steps:

1.  Confirm that the list of managed clusters does include
    `local-cluster`, and that the placement rule `decisions` list does
    not display the `local-cluster`. Run the following command and view
    the results:

        % oc get managedclusters

    See in the sample output that `local-cluster` is joined, but it is
    not in the YAML for `PlacementRule`:

        NAME            HUB ACCEPTED   MANAGED CLUSTER URLS   JOINED   AVAILABLE   AGE
        local-cluster   true                                  True     True        56d
        cluster1        true                                  True     True        16h

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1
    kind: PlacementRule
    metadata:
      name: all-ready-clusters
      namespace: default
    spec:
      clusterSelector: {}
    status:
      decisions:
      - clusterName: cluster1
        clusterNamespace: cluster1
    ```

2.  Create a `Role` in your YAML file to grant the `managedcluster`
    administrative permission in the `<your-local-cluster-name>`
    namespace. See the following example:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: Role
    metadata:
      name: managedcluster-admin-user-zisis
      namespace: <your-local-cluster-name>
    rules:
    - apiGroups:
      - cluster.open-cluster-management.io
      resources:
      - managedclusters
      verbs:
      - get
    ```

3.  Create a `RoleBinding` resource to grant the placement rule user
    access to the `<your-local-cluster-name>` namespace. See the
    following example:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: managedcluster-admin-user-zisis
      namespace: <your-local-cluster-name>
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: Role
      name: managedcluster-admin-user-zisis
      namespace: <your-local-cluster-name>
    subjects:
    - kind: User
      name: zisis
      apiGroup: rbac.authorization.k8s.io
    ```

## Troubleshooting application Kubernetes deployment version

A managed cluster with a deprecated Kubernetes `apiVersion` might not be
supported. See the Kubernetes issue for more details about the
deprecated API version.

### Symptom: Application deployment version

If one or more of your application resources in the Subscription YAML
file uses the deprecated API, you might receive an error similar to the
following error:

    failed to install release: unable to build kubernetes objects from release manifest: unable to recognize "": no matches for
    kind "Deployment" in version "extensions/v1beta1"

Or with new Kubernetes API version in your YAML file named `old.yaml`
for instance, you might receive the following error:

    error: unable to recognize "old.yaml": no matches for kind "Deployment" in version "deployment/v1beta1"

### Resolving the problem: Application deployment version

1.  Update the `apiVersion` in the resource. For example, if the error
    displays for *Deployment* kind in the subscription YAML file, you
    need to update the `apiVersion` from `extensions/v1beta1` to
    `apps/v1`.

    See the following example:

    ``` yaml
    apiVersion: apps/v1
    kind: Deployment
    ```

2.  Verify the available versions by running the following command on
    the managed cluster:

        kubectl explain <resource>

3.  Check for `VERSION`.

## Troubleshooting Klusterlet with degraded conditions

The Klusterlet degraded conditions can help to diagnose the status of
the klusterlet agent on managed cluster. If a Klusterlet is in the
degraded condition, the klusterlet agent on managed cluster might have
errors that need to be troubleshooted. See the following information for
Klusterlet degraded conditions that are set to `True`.

### Symptom: Klusterlet is in the degraded condition

After deploying a Klusterlet on managed cluster, the
`KlusterletRegistrationDegraded` or `KlusterletWorkDegraded` condition
displays a status of *True*.

### Identifying the problem: Klusterlet is in the degraded condition

1.  Run the following command on the managed cluster to view the
    Klusterlet status:

        kubectl get klusterlets klusterlet -oyaml

2.  Check `KlusterletRegistrationDegraded` or `KlusterletWorkDegraded`
    to see if the condition is set to `True`. Proceed to *Resolving the
    problem* for any degraded conditions that are listed.

### Resolving the problem: Klusterlet is in the degraded condition

See the following list of degraded statuses and how you can attempt to
resolve those issues:

- If the `KlusterletRegistrationDegraded` condition with a status of
  *True* and the condition reason is: *BootStrapSecretMissing*, you need
  create a bootstrap secret on `open-cluster-management-agent`
  namespace.

- If the `KlusterletRegistrationDegraded` condition displays *True* and
  the condition reason is a *BootstrapSecretError*, or
  *BootstrapSecretUnauthorized*, then the current bootstrap secret is
  invalid. Delete the current bootstrap secret and recreate a valid
  bootstrap secret on `open-cluster-management-agent` namespace.

- If the `KlusterletRegistrationDegraded` and `KlusterletWorkDegraded`
  displays *True* and the condition reason is
  *HubKubeConfigSecretMissing*, delete the Klusterlet and recreate it.

- If the `KlusterletRegistrationDegraded` and `KlusterletWorkDegraded`
  displays *True* and the condition reason is: *ClusterNameMissing*,
  *KubeConfigMissing*, *HubConfigSecretError*, or
  *HubConfigSecretUnauthorized*, delete the hub cluster kubeconfig
  secret from `open-cluster-management-agent` namespace. The klusterlet
  agent creates a new hub cluster kubeconfig secret.

- If the `KlusterletRegistrationDegraded` displays *True* and the
  condition reason is *GetRegistrationDeploymentFailed*, or
  *UnavailableRegistrationPod*, you can check the condition message to
  get the problem details and attempt to resolve.

- If the `KlusterletWorkDegraded` displays *True* and the condition
  reason is *GetWorkDeploymentFailed* ,or *UnavailableWorkPod*, you can
  check the condition message to get the problem details and attempt to
  resolve.

## Troubleshooting Object storage channel secret

If you change the `SecretAccessKey`, the subscription of an Object
storage channel cannot pick up the updated secret automatically and you
receive an error.

### Symptom: Object storage channel secret

The subscription of an Object storage channel cannot pick up the updated
secret automatically. This prevents the subscription operator from
reconciliation and deploys resources from Object storage to the managed
cluster.

### Resolving the problem: Object storage channel secret

You need to manually input the credentials to create a secret, then
refer to the secret within a channel.

1.  Annotate the subscription CR in order to generate a reconcile single
    to subscription operator. See the following `data` specification:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1
    kind: Channel
    metadata:
      name: deva
      namespace: ch-obj
      labels:
        name: obj-sub
    spec:
      type: ObjectBucket
      pathname: http://ec2-100-26-232-156.compute-1.amazonaws.com:9000/deva
      sourceNamespaces:
        - default
      secretRef:
        name: dev
    ---
    apiVersion: v1
    kind: Secret
    metadata:
      name: dev
      namespace: ch-obj
      labels:
        name: obj-sub
    data:
      AccessKeyID: YWRtaW4=
      SecretAccessKey: cGFzc3dvcmRhZG1pbg==
    ```

2.  Run `oc annotate` to test:

        oc annotate appsub -n <subscription-namespace> <subscription-name> test=true

After you run the command, you can go to the Application console to
verify that the resource is deployed to the managed cluster. Or you can
log in to the managed cluster to see if the application resource is
created at the given namespace.

## Troubleshooting observability

After you install the observability component, the component might be
stuck and an `Installing` status is displayed.

### Symptom: MultiClusterObservability resource status stuck

If the observability status is stuck in an `Installing` status after you
install and create the Observability custom resource definition (CRD),
it is possible that there is no value defined for the
`spec:storageConfig:storageClass` parameter. Alternatively, the
observability component automatically finds the default `storageClass`,
but if there is no value for the storage, the component remains stuck
with the `Installing` status.

### Resolving the problem: MultiClusterObservability resource status stuck

If you have this problem, complete the following steps:

1.  Verify that the observability components are installed:

    1.  To verify that the `multicluster-observability-operator`, run
        the following command:

            kubectl get pods -n open-cluster-management|grep observability

    2.  To verify that the appropriate CRDs are present, run the
        following command:

            kubectl get crd|grep observ

        The following CRDs must be displayed before you enable the
        component:

            multiclusterobservabilities.observability.open-cluster-management.io
            observabilityaddons.observability.open-cluster-management.io
            observatoria.core.observatorium.io

2.  If you create your own storageClass for a Bare Metal cluster, see
    Persistent storage using NFS.

3.  To ensure that the observability component can find the default
    storageClass, update the `storageClass` parameter in the
    `multicluster-observability-operator` custom resource definition.
    Your parameter might resemble the following value:

<!-- -->

    storageclass.kubernetes.io/is-default-class: "true"

The observability component status is updated to a *Ready* status when
the installation is complete. If the installation fails to complete, the
*Fail* status is displayed.

## Troubleshooting OpenShift monitoring service

Observability service in a managed cluster needs to scrape metrics from
the OpenShift Container Platform monitoring stack. The
`metrics-collector` is not installed if the OpenShift Container Platform
monitoring stack is not ready.

### Symptom: OpenShift monitoring service is not ready

The `endpoint-observability-operator-x` pod checks if the
`prometheus-k8s` service is available in the `openshift-monitoring`
namespace. If the service is not present in the `openshift-monitoring`
namespace, then the `metrics-collector` is not deployed. You might
receive the following error message:
`Failed to get prometheus resource`.

### Resolving the problem: OpenShift monitoring service is not ready

If you have this problem, complete the following steps:

1.  Log in to your OpenShift Container Platform cluster.

2.  Access the `openshift-monitoring` namespace to verify that the
    `prometheus-k8s` service is available.

3.  Restart `endpoint-observability-operator-x` pod in the
    `open-cluster-management-addon-observability` namespace of the
    managed cluster.

## Troubleshooting metrics-collector

When the `observability-client-ca-certificate` secret is not refreshed
in the managed cluster, you might receive an internal server error.

### Symptom: metrics-collector cannot verify observability-client-ca-certificate

There might be a managed cluster, where the metrics are unavailable. If
this is the case, you might receive the following error from the
`metrics-collector` deployment:

    error: response status code is 500 Internal Server Error, response body is x509: certificate signed by unknown authority (possibly because of "crypto/rsa: verification error" while trying to verify candidate authority certificate "observability-client-ca-certificate")

### Resolving the problem: metrics-collector cannot verify observability-client-ca-certificate

If you have this problem, complete the following steps:

1.  Log in to your managed cluster.

2.  Delete the secret named,
    `observability-controller-open-cluster-management.io-observability-signer-client-cert`
    that is in the `open-cluster-management-addon-observability`
    namespace. Run the following command:

        oc delete secret observability-controller-open-cluster-management.io-observability-signer-client-cert -n open-cluster-management-addon-observability

    **Note:** The
    `observability-controller-open-cluster-management.io-observability-signer-client-cert`
    is automatically recreated with new certificates.

The `metrics-collector` deployment is recreated and the
`observability-controller-open-cluster-management.io-observability-signer-client-cert`
secret is updated.

## Troubleshooting Thanos compactor halts

You might receive an error message that the compactor is halted. This
can occur when there are corrupted blocks or when there is insufficient
space on the Thanos compactor persistent volume claim (PVC).

### Symptom: Thanos compactor halts

The Thanos compactor halts because there is no space left on your
persistent volume claim (PVC). You receive the following message:

``` terminal
ts=2024-01-24T15:34:51.948653839Z caller=compact.go:491 level=error msg="critical error detected; halting" err="compaction: group 0@5827190780573537664: compact blocks [ /var/thanos/compact/compact/0@15699422364132557315/01HKZGQGJCKQWF3XMA8EXAMPLE]: 2 errors: populate block: add series: write series data: write /var/thanos/compact/compact/0@15699422364132557315/01HKZGQGJCKQWF3XMA8EXAMPLE.tmp-for-creation/index: no space left on device; write /var/thanos/compact/compact/0@15699422364132557315/01HKZGQGJCKQWF3XMA8EXAMPLE.tmp-for-creation/index: no space left on device"
```

### Resolving the problem: Thanos compactor halts

To resolve the problem, increase the storage space of the Thanos
compactor PVC. Complete the following steps:

1.  Increase the storage space for the
    `data-observability-thanos-compact-0` PVC. See Increasing and
    decreasing persistent volumes and persistent volume claims for more
    information.

2.  Restart the `observability-thanos-compact` pod by deleting the pod.
    The new pod is automatically created and started.

    ``` bash
    oc delete pod observability-thanos-compact-0 -n open-cluster-management-observability
    ```

3.  After you restart the `observability-thanos-compact` pod, check the
    `acm_thanos_compact_todo_compactions` metric. As the Thanos
    compactor works through the backlog, the metric value decreases.

4.  Confirm that the metric changes in a consistent cycle and check the
    disk usage. Then you can reattempt to decrease the PVC again.

    **Note:** This might take several weeks.

### Symptom: Thanos compactor halts

The Thanos compactor halts because you have corrupted blocks. You might
receive the following output where the `01HKZYEZ2DVDQXF1STVEXAMPLE`
block is corrupted:

``` terminal
ts=2024-01-24T15:34:51.948653839Z caller=compact.go:491 level=error msg="critical error detected; halting" err="compaction: group 0@15699422364132557315: compact blocks [/var/thanos/compact/compact/0@15699422364132557315/01HKZGQGJCKQWF3XMA8EXAMPLE /var/thanos/compact/compact/0@15699422364132557315/01HKZQK7TD06J2XWGR5EXAMPLE /var/thanos/compact/compact/0@15699422364132557315/01HKZYEZ2DVDQXF1STVEXAMPLE /var/thanos/compact/compact/0@15699422364132557315/01HM05APAHXBQSNC0N5EXAMPLE]: populate block: chunk iter: cannot populate chunk 8 from block 01HKZYEZ2DVDQXF1STVEXAMPLE: segment index 0 out of range"
```

### Resolving the problem: Thanos compactor halts

Add the `thanos bucket verify` command to the object storage
configuration. Complete the following steps:

1.  Resolve the block error by adding the `thanos bucket verify` command
    to the object storage configuration. Set the configuration in the
    `observability-thanos-compact` pod by using the following commands:

    ``` bash
    oc rsh observability-thanos-compact-0
    [..]
    thanos tools bucket verify -r --objstore.config="$OBJSTORE_CONFIG" --objstore-backup.config="$OBJSTORE_CONFIG" --id=01HKZYEZ2DVDQXF1STVEXAMPLE
    ```

2.  If the previous command does not work, you must mark the block for
    deletion because it might be corrupted. Run the following commands:

    ``` bash
    thanos tools bucket mark --id "01HKZYEZ2DVDQXF1STVEXAMPLE" --objstore.config="$OBJSTORE_CONFIG" --marker=deletion-mark.json --details=DELETE
    ```

3.  If you are blocked for deletion, clean up the marked blocks by
    running the following command:

    ``` bash
    thanos tools bucket cleanup --objstore.config="$OBJSTORE_CONFIG"
    ```

## Troubleshooting PostgreSQL shared memory error

If you have a large environment, you might encounter a PostgreSQL shared
memory error that impacts search results and the topology view for
applications.

### Symptom: PostgreSQL shared memory error

An error message resembling the following appears in the `search-api`
logs:
`ERROR: could not resize shared memory segment "/PostgreSQL.1083654800" to 25031264 bytes: No space left on device (SQLSTATE 53100)`

### Resolving the problem: PostgreSQL shared memory error

To resolve the issue, update the PostgreSQL resources found in the
`search-postgres` ConfigMap. Complete the following steps to update the
resources:

1.  Run the following command to switch to the `open-cluster-management`
    project:

    ``` bash
    oc project open-cluster-management
    ```

2.  Increase the `search-postgres` pod memory. The following command
    increases the memory to `16Gi`:

    ``` bash
    oc patch search -n open-cluster-management search-v2-operator --type json -p '[{"op": "add", "path": "/spec/deployments/database/resources", "value": {"limits": {"memory": "16Gi"}, "requests": {"memory": "32Mi", "cpu": "25m"}}}]'
    ```

3.  Run the following command to prevent the search operator from
    overwriting your changes:

    ``` bash
    oc annotate search search-v2-operator search-pause=true
    ```

4.  Run the following command to update the resources in the
    `search-postgres` YAML file:

    ``` bash
    oc edit cm search-postgres -n open-cluster-management
    ```

    See the following example for increasing resources:

    ``` yaml
      postgresql.conf: |-
        work_mem = '128MB' # Higher values allocate more memory
        max_parallel_workers_per_gather = '0' # Disables parallel queries
        shared_buffers = '1GB' # Higher values allocate more memory
    ```

    Make sure to save your changes before exiting.

5.  Run the following command to restart the `postgres` and `api` pod.

    ``` bash
    oc delete pod search-postgres-xyz search-api-xzy
    ```

6.  To verify your changes, open the `search-postgres` YAML file and
    confirm that the changes you made to `postgresql.conf:` are present
    by running the following command:

    ``` bash
    oc get cm search-postgres -n open-cluster-management -o yaml
    ```

See Search customization and configurations for more information on
adding environment variables.

## Troubleshooting Submariner not connecting after installation

If Submariner does not run correctly after you configure it, complete
the following steps to diagnose the issue.

### Symptom: Submariner not connecting after installation

Your Submariner network is not communicating after installation.

### Identifying the problem: Submariner not connecting after installation

If the network connectivity is not established after deploying
Submariner, begin the troubleshooting steps. Note that it might take
several minutes for the processes to complete when you deploy
Submariner.

### Resolving the problem: Submariner not connecting after installation

When Submariner does not run correctly after deployment, complete the
following steps:

1.  Check for the following requirements to determine whether the
    components of Submariner deployed correctly:

    - The `submariner-addon` pod is running in the
      `open-cluster-management` namespace of your hub cluster.

    - The following pods are running in the `submariner-operator`
      namespace of each managed cluster:

      - submariner-addon

      - submariner-gateway

      - submariner-routeagent

      - submariner-operator

      - submariner-globalnet (only if Globalnet is enabled in the
        ClusterSet)

      - submariner-lighthouse-agent

      - submariner-lighthouse-coredns

      - submariner-networkplugin-syncer (only if the specified CNI value
        is `OVNKubernetes`)

      - submariner-metrics-proxy

2.  Run the `subctl diagnose all` command to check the status of the
    required pods, with the exception of the `submariner-addon` pods.

3.  Make sure to run the `must-gather` command to collect logs that can
    help with debugging issues.

## Troubleshooting Submariner end-to-end test failures

After running Submariner end-to-end tests, you might get failures. Use
the following sections to help you troubleshoot these end-to-end test
failures.

### Symptom: Submariner end-to-end data plane test fails

When the end-to-end data plane test fails, the Submariner tests show
that the `connector` pod can connect to the `listener` pod, but later
the `connector` pod gets stuck in the `listening` phase.

### Resolving the problem: Submariner end-to-end data plane test fails

The maximum transmission unit (MTU) can cause the end-to-end data plane
test failure. For example, the MTU might cause the `inter-cluster`
traffic over the Internet Protocol Security (IPsec) to fail. Verify if
the MTU causes the failure by running an end-to-end data plane test that
uses a small packet size.

To run this type of test, run the following command in your Submariner
workspace:

``` bash
subctl verify --verbose --only connectivity --context <from_context> --tocontext <to_context> --image-override submariner-nettest=quay.io/submariner/nettest:devel --packet-size 200
```

If the test succeeds with this small packet size, you can resolve the
connection issues by setting the transmission control protocol (TCP)
maximum segment size (MSS). Set the TCP MSS by completing the following
steps:

1.  Set the TCP MSS `clamping` value by annotating the gateway node. For
    example, run the following command with a value of `1200`:

    ``` bash
    oc annotate node <node_name> submariner.io/tcp-clamp-mss=1200
    ```

2.  Restart all the `RouteAgent` pods by running the following command:

    ``` bash
    oc delete pod -n submariner-operator -l app=submariner-routeagent
    ```

### Symptom: Submariner end-to-end test fails for bare-metal clusters

The end-to-end data plane tests might fail for the bare-metal cluster if
the container network interface (CNI) is OpenShiftSDN, or if the virtual
extensible local-area network (VXLAN) is used for the `inter-cluster`
tunnels.

### Resolving the problem: Submariner end-to-end test fails for bare-metal clusters

A bug in the User Datagram Protocal (UDP) checksum calculation by the
hardware can be the root cause for the end-to-end data plane test
failures for bare-metal clusters. To troubleshoot this bug, disable the
hardware offloading by applying the following YAML file:

``` yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: disable-offload
  namespace: submariner-operator
spec:
  selector:
    matchLabels:
      app: disable-offload
  template:
    metadata:
      labels:
        app: disable-offload
    spec:
      tolerations:
      - operator: Exists
      containers:
        - name: disable-offload
          image: nicolaka/netshoot
          imagePullPolicy: IfNotPresent
          securityContext:
            allowPrivilegeEscalation: true
            capabilities:
              add:
              - net_admin
              drop:
              - all
            privileged: true
            readOnlyRootFilesystem: false
            runAsNonRoot: false
          command: ["/bin/sh", "-c"]
          args:
            - ethtool --offload vxlan-tunnel rx off tx off;
              ethtool --offload vx-submariner rx off tx off;
sleep infinity
      restartPolicy: Always
      securityContext: {}
      serviceAccount: submariner-routeagent
      serviceAccountName: submariner-routeagent
      hostNetwork: true
```

## Troubleshooting restore status finishes with errors

After you restore a backup, resources are restored correctly but the Red
Hat Advanced Cluster Management restore resource shows a
`FinishedWithErrors` status.

### Symptom: Troubleshooting restore status finishes with errors

Red Hat Advanced Cluster Management shows a `FinishedWithErrors` status
and one or more of the Velero restore resources created by the Red Hat
Advanced Cluster Management restore show a `PartiallyFailed` status.

### Resolving the problem: Troubleshooting restore status finishes with errors

If you restore from a backup that is empty, you can safely ignore the
`FinishedWithErrors` status.

Red Hat Advanced Cluster Management for Kubernetes restore shows a
cumulative status for all Velero restore resources. If one status is
`PartiallyFailed` and the others are `Completed`, the cumulative status
you see is `PartiallyFailed` to notify you that there is at least one
issue.

To resolve the issue, check the status for all individual Velero restore
resources with a `PartiallyFailed` status and view the logs for more
details. You can get the log from the object storage directly, or
download it from the OADP Operator by using the `DownloadRequest` custom
resource.

To create a `DownloadRequest` from the console, complete the following
steps:

1.  Navigate to **Operators** \> **Installed Operators** \> **Create
    DownloadRequest**.

2.  Select `BackupLog` as your **Kind** and follow the console
    instructions to complete the `DownloadRequest` creation.

## Troubleshooting multiline YAML parsing

When you want to use the `fromSecret` function to add contents of a
`Secret` resource into a `Route` resource, the contents are displayed
incorrectly.

### Symptom: Troubleshooting multiline YAML parsing

When the managed cluster and hub cluster are the same cluster the
certificate data is redacted, so the contents are not parsed as a
template JSON string. You might receive the following error messages:

``` json
message: >-
            [spec.tls.caCertificate: Invalid value: "redacted ca certificate
            data": failed to parse CA certificate: data does not contain any
            valid RSA or ECDSA certificates, spec.tls.certificate: Invalid
            value: "redacted certificate data": data does not contain any valid
            RSA or ECDSA certificates, spec.tls.key: Invalid value: "": no key specified]
```

### Resolving the problem: Troubleshooting multiline YAML parsing

Configure your certificate policy to retrieve the hub cluster and
managed cluster `fromSecret` values. Use the `autoindent` function to
update your certificate policy with the following content:

``` yaml
                 tls:
                    certificate: |
                      {{ print "{{hub fromSecret "open-cluster-management" "minio-cert" "tls.crt" hub}}" | base64dec | autoindent }}
```

## Troubleshooting *ClusterCurator* automatic template failure to deploy

If you are using the `ClusterCurator` automatic template and it fails to
deploy, follow the procedure to troubleshoot the problem.

### Symptom: *ClusterCurator* automatic template failure to deploy

You are unable to deploy managed clusters by using the `ClusterCurator`
automatic template. The process might become stuck on the posthooks and
might not create any logs.

### Resolving the problem: *ClusterCurator* automatic template failure to deploy

Complete the following steps to identify and resolve the problem:

1.  Check the `ClusterCurator` resource status in the cluster namespace
    for any messages or errors.

2.  In the `Job` resource named, `curator-job-*`, which is in the same
    cluster namespace as the previous step, check the pod log for any
    errors.

**Note:** The job is removed after one hour due to a one hour time to
live (TTL) setting.
