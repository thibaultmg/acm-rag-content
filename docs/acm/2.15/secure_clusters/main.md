# Securing clusters

You might need to manually create and manage the access control on your
cluster. To do this, you must configure *authentication* service
requirements for Red Hat Advanced Cluster Management for Kubernetes to
onboard workloads to Identity and Access Management (IAM).

Use the role-based access control and authentication to identify the
user associated roles and cluster credentials. To create and manage your
cluster credentials, access the credentials by going to the Kubernetes
secrets where they are stored. See the following documentation for
information about access and credentials:

**Required access:** Cluster administrator

## Role-based access control

Red Hat Advanced Cluster Management for Kubernetes supports role-based
access control (RBAC). Your role determines the actions that you can
perform. RBAC is based on the authorization mechanisms in Kubernetes,
similar to Red Hat OpenShift Container Platform. For more information
about RBAC, see the OpenShift *RBAC* overview in the OpenShift Container
Platform documentation.

**Note:** Action buttons are disabled from the console if the user-role
access is impermissible.

### Overview of roles

Some product resources are cluster-wide and some are namespace-scoped.
You must apply cluster role bindings and namespace role bindings to your
users for consistent access controls. View the table list of the
following role definitions that are supported in Red Hat Advanced
Cluster Management for Kubernetes:

- Role - Definition

- cluster-admin - This is an OpenShift Container Platform default role.
  A user with cluster binding to the cluster-admin role is an OpenShift
  Container Platform super user, who has all access.

- open-cluster-management:cluster-manager-admin - A user with cluster
  binding to the open-cluster-management:cluster-manager-admin role is a
  Red Hat Advanced Cluster Management for Kubernetes super user, who has
  all access. This role allows the user to create a ManagedCluster
  resource.

- open-cluster-management:admin:\<managed_cluster_name\> - A user with
  cluster binding to the
  open-cluster-management:admin:\<managed_cluster_name\> role has
  administrator access to the ManagedCluster resource named,
  \<managed_cluster_name\>. When a user has a managed cluster, this role
  is automatically created.

- open-cluster-management:view:\<managed_cluster_name\> - A user with
  cluster binding to the
  open-cluster-management:view:\<managed_cluster_name\> role has view
  access to the ManagedCluster resource named, \<managed_cluster_name\>.

- open-cluster-management:managedclusterset:admin:\<managed_clusterset_name\> -
  A user with cluster binding to the
  open-cluster-management:managedclusterset:admin:\<managed_clusterset_name\>
  role has administrator access to ManagedCluster resource named
  \<managed_clusterset_name\>. The user also has administrator access to
  managedcluster.cluster.open-cluster-management.io,
  clusterclaim.hive.openshift.io, clusterdeployment.hive.openshift.io,
  and clusterpool.hive.openshift.io resources, which has the managed
  cluster set label:
  cluster.open-cluster-management.io/clusterset=\<managed_clusterset_name\>.
  A role binding is automatically generated when you are using a cluster
  set. See Creating a ManagedClusterSet to learn how to manage the
  resource.

- open-cluster-management:managedclusterset:view:\<managed_clusterset_name\> -
  A user with cluster binding to the
  open-cluster-management:managedclusterset:view:\<managed_clusterset_name\>
  role has view access to the ManagedCluster resource named,
  \<managed_clusterset_name\>\`. The user also has view access to
  managedcluster.cluster.open-cluster-management.io,
  clusterclaim.hive.openshift.io, clusterdeployment.hive.openshift.io,
  and clusterpool.hive.openshift.io resources, which has the managed
  cluster set labels: cluster.open-cluster-management.io,
  clusterset=\<managed_clusterset_name\>. For more details on how to
  manage managed cluster set resources, see Creating a
  ManagedClusterSet.

- open-cluster-management:subscription-admin - A user with the
  open-cluster-management:subscription-admin role can create Git
  subscriptions that deploy resources to multiple namespaces. The
  resources are specified in Kubernetes resource YAML files in the
  subscribed Git repository. Note: When a non-subscription-admin user
  creates a subscription, all resources are deployed into the
  subscription namespace regardless of specified namespaces in the
  resources. For more information, see the Application lifecycle RBAC
  section.

- admin, edit, view - Admin, edit, and view are OpenShift Container
  Platform default roles. A user with a namespace-scoped binding to
  these roles has access to open-cluster-management resources in a
  specific namespace, while cluster-wide binding to the same roles gives
  access to all of the open-cluster-management resources cluster-wide.

- open-cluster-management:managedclusterset:bind:\<managed_clusterset_name\> -
  A user with the
  open-cluster-management:managedclusterset:bind:\<managed_clusterset_name\>
  role has view access to the managed cluster resource called
  \<managed_clusterset_name\>. The user can bind
  \<managed_clusterset_name\> to a namespace. The user also has view
  access to managedcluster.cluster.open-cluster-management.io,
  clusterclaim.hive.openshift.io, clusterdeployment.hive.openshift.io,
  and clusterpool.hive.openshift.io resources, which have the following
  managed cluster set label:
  cluster.open-cluster-management.io/clusterset=\<managed_clusterset_name\>.
  See Creating a ManagedClusterSet to learn how to manage the resource.

**Important:**

- Any user can create projects from OpenShift Container Platform, which
  gives administrator role permissions for the namespace.

- If a user does not have role access to a cluster, the cluster name is
  not displayed. The cluster name might be displayed with the following
  symbol: `-`.

### Console and API RBAC tables

To understand the role-based access control of the components, view the
following console and API RBAC tables:

- Resource: Application - Admin: create, read, update, delete - Edit:
  create, read, update, delete - View: read

- Resource: Channel - Admin: create, read, update, delete - Edit:
  create, read, update, delete - View: read

- Resource: Subscription - Admin: create, read, update, delete - Edit:
  create, read, update, delete - View: read

<!-- -->

- API: applications.app.k8s.io - Admin: create, read, update, delete -
  Edit: create, read, update, delete - View: read

- API: channels.apps.open-cluster-management.io - Admin: create, read,
  update, delete - Edit: create, read, update, delete - View: read

- API: deployables.apps.open-cluster-management.io (Deprecated) - Admin:
  create, read, update, delete - Edit: create, read, update, delete -
  View: read

- API: helmreleases.apps.open-cluster-management.io - Admin: create,
  read, update, delete - Edit: create, read, update, delete - View: read

- API: placements.apps.open-cluster-management.io - Admin: create, read,
  update, delete - Edit: create, read, update, delete - View: read

- API: placementrules.apps.open-cluster-management.io (Deprecated) -
  Admin: create, read, update, delete - Edit: create, read, update,
  delete - View: read

- API: subscriptions.apps.open-cluster-management.io - Admin: create,
  read, update, delete - Edit: create, read, update, delete - View: read

- API: configmaps - Admin: create, read, update, delete - Edit: create,
  read, update, delete - View: read

- API: secrets - Admin: create, read, update, delete - Edit: create,
  read, update, delete - View: read

- API: namespaces - Admin: create, read, update, delete - Edit: create,
  read, update, delete - View: read

<!-- -->

- Resource: Policies - Admin: create, read, update, delete - Edit: read,
  update - View: read

- Resource: PlacementBindings - Admin: create, read, update, delete -
  Edit: read, update - View: read

- Resource: Placements - Admin: create, read, update, delete - Edit:
  read, update - View: read

- Resource: PlacementRules (deprecated) - Admin: create, read, update,
  delete - Edit: read, update - View: read

- Resource: PolicyAutomations - Admin: create, read, update, delete -
  Edit: read, update - View: read

<!-- -->

- API: policies.policy.open-cluster-management.io - Admin: create, read,
  update, delete - Edit: read, update - View: read

- API: placementbindings.policy.open-cluster-management.io - Admin:
  create, read, update, delete - Edit: read, update - View: read

- API: policyautomations.policy.open-cluster-management.io - Admin:
  create, read, update, delete - Edit: read, update - View: read

<!-- -->

- API - Admin - Edit - View

- multiclusterobservabilities.observability.open-cluster-management.io -
  create, read, update, and delete - read, update - read

- searchcustomizations.search.open-cluster-management.io - create, get,
  list, watch, update, delete, patch - - - -

- policyreports.wgpolicyk8s.io - get, list, watch - get, list, watch -
  get, list, watch

<!-- -->

- Role - Role description

- kubevirt.io:view - Only view all Red Hat OpenShift Virtualization
  resources in your cluster.

- kubevirt.io:edit - Create, view, edit, and delete Red Hat OpenShift
  Virtualization resources in your cluster.

- kubevirt.io:admin - Create, view, edit, and delete resources for Red
  Hat OpenShift Virtualization. You can also access the HyperConverged
  custom resource in the openshift-cnv namespace.

- kubevirt.io-acm-managed:admin - An extension of the default
  kubevirt.io roles, granting virtual machine administrators to view,
  edit, and delete virtual machine related resources. Troubleshoot
  issues and complete advanced configuration and administrative tasks.

- kubevirt.io-acm-managed:view - An extension of the default kubevirt.io
  roles, granting extra view-only privileges for virtual machine
  resources on your managed cluster. Monitor virtual machine operations,
  view configurations, and verify the status of virtual machine
  resources without making any changes.

- kubevirt.io-acm-hub:admin - Grants administrator privileges for
  virtual machine migrations across clusters. Grants prerequisite
  permissions to view virtual machines in the multicluster Red Hat
  OpenShift Virtualization console from your hub cluster.

- kubevirt.io-acm-hub:view - Grants view only privileges for virtual
  machine migrations across clusters. Grants prerequisite permissions to
  view virtual machines in the multicluster Red Hat OpenShift
  Virtualization console from your hub cluster.

## Implementing role-based access control

Red Hat Advanced Cluster Management for Kubernetes role-based access
control (RBAC) helps you to validate roles at the console level and at
the API level. You can enable or disable actions in the console based on
user access role permissions.

The multicluster engine operator is a prerequisite and the cluster
lifecycle function of Red Hat Advanced Cluster Management. To manage
RBAC for clusters with the multicluster engine operator, use the RBAC
guidance from the cluster lifecycle multicluster engine for Kubernetes
operator Role-based access control documentation.

### Enabling RBAC for cluster management

For cluster management actions, you need access to your managed cluster
and your hub cluster. If you want to create multiple cluster role
bindings, you can use the `clusterRoleBindings` field to create multiple
cluster role bindings in a single `ClusterPermission` resource.

Complete the following step to create a `ClusterPermission` resource for
creating multiple cluster role bindings:

1.  To create a `ClusterPermission` resource to have many cluster role
    bindings, run the following command:

    ``` bash
    oc create clusterpermission clusterpermission-multiple-clusterrolebindings -n <cluster-name>
    ```

    Your resource might resemble the following YAML with the specified
    `clusterRoleBindings` field:

    ``` yaml
    apiVersion: rbac.open-cluster-management.io/v1alpha1
    kind: ClusterPermission
    metadata:
      name: clusterpermission-multiple-clusterrolebindings
    spec:
      clusterRoleBindings:
        - name: multi-crb-binding1
          roleRef:
            apiGroup: rbac.authorization.k8s.io
            kind: ClusterRole
            name: argocd-application-controller-1
          subject:
            kind: User
            name: user1
        - name: multi-crb-binding2
          roleRef:
            apiGroup: rbac.authorization.k8s.io
            kind: ClusterRole
            name: argocd-application-controller-3
          subjects:
            - kind: User
              name: user2
            - kind: Group
              name: group1
    ```

### Enabling RBAC for Application lifecycle

When you create an application, the `subscription` namespace is created,
then the configuration map is created within the `subscription`
namespace. You must also have access to the `channel` namespace. When
you want to apply a subscription, you must be a subscription
administrator. For more information about managing applications, see
Creating an allow and deny list as subscription administrator.

View the following application lifecycle RBAC operations:

- Create and administer applications on all managed clusters with a user
  named `username`. You must create a cluster role binding and bind it
  to `username`. Run the following command:

  ``` bash
  oc create clusterrolebinding <role-binding-name> --clusterrole=open-cluster-management:cluster-manager-admin --user=<username>
  ```

  This role assigns superuser access to all resources and actions. As a
  superuser, you can create the namespace for the application and all
  application resources in the namespace with this role.

- Create applications that deploy resources to multiple namespaces. You
  must create a cluster role binding to the
  `open-cluster-management:subscription-admin` cluster role, and bind it
  to a user named `username`. Run the following command:

  ``` bash
  oc create clusterrolebinding <role-binding-name> --clusterrole=open-cluster-management:subscription-admin --user=<username>
  ```

- Create and administer applications in the `cluster-name` managed
  cluster, with the `username` user. You must create a cluster role
  binding to the `open-cluster-management:admin:<cluster-name>` cluster
  role and bind it to `username` by entering the following command:

  ``` bash
  oc create clusterrolebinding <role-binding-name> --clusterrole=open-cluster-management:admin:<cluster-name> --user=<username>
  ```

  This role has read and write access to all `application` resources on
  the managed cluster, `cluster-name`. Repeat this if access for other
  managed clusters is required.

- Create a namespace role binding to the `application` namespace using
  the `admin` role and bind it to `username` by entering the following
  command:

  ``` bash
  oc create rolebinding <role-binding-name> -n <application-namespace> --clusterrole=admin --user=<username>
  ```

  This role has read and write access to all `application` resources in
  the `application` namspace. Repeat this if access for other
  applications is required or if the application deploys to multiple
  namespaces.

- You can create applications that deploy resources to multiple
  namespaces. Create a cluster role binding to the
  `open-cluster-management:subscription-admin` cluster role and bind it
  to `username` by entering the following command:

  ``` bash
  oc create clusterrolebinding <role-binding-name> --clusterrole=open-cluster-management:subscription-admin --user=<username>
  ```

- To view an application on a managed cluster named `cluster-name` with
  the user named `username`, create a cluster role binding to the
  `open-cluster-management:view:` cluster role and bind it to
  `username`. Enter the following command:

  ``` bash
  oc create clusterrolebinding <role-binding-name> --clusterrole=open-cluster-management:view:<cluster-name> --user=<username>
  ```

  This role has read access to all `application` resources on the
  managed cluster, `cluster-name`. Repeat this if access for other
  managed clusters is required.

- Create a namespace role binding to the `application` namespace using
  the `view` role and bind it to `username`. Enter the following
  command:

  ``` bash
  oc create rolebinding <role-binding-name> -n <application-namespace> --clusterrole=view --user=<username>
  ```

  This role has read access to all `application` resources in the
  `application` namspace. Repeat this if access for other applications
  is required.

### Enabling RBAC for Governance

For Governance actions, you need access to the namespace where the
policy is created, along with access to the managed cluster where the
policy is applied. The managed cluster must also be part of a
`ManagedClusterSet` that is bound to the namespace. To continue to learn
about `ManagedClusterSet`, see ManagedClusterSets Introduction.

After you select a namespace, such as `rhacm-policies`, with one or more
bound `ManagedClusterSets`, and after you have access to create
`Placement` objects in the namespace, view the following operations:

- To create a `ClusterRole` named `rhacm-edit-policy` with `Policy`,
  `PlacementBinding`, and `PolicyAutomation` edit access, run the
  following command:

  ``` bash
  oc create clusterrole rhacm-edit-policy --resource=policies.policy.open-cluster-management.io,placementbindings.policy.open-cluster-management.io,policyautomations.policy.open-cluster-management.io,policysets.policy.open-cluster-management.io --verb=create,delete,get,list,patch,update,watch
  ```

- To create a policy in the `rhacm-policies` namespace, create a
  namespace `RoleBinding`, such as `rhacm-edit-policy`, to the
  `rhacm-policies` namespace using the `ClusterRole` created previously.
  Run the following command:

  ``` bash
  oc create rolebinding rhacm-edit-policy -n rhacm-policies --clusterrole=rhacm-edit-policy --user=<username>
  ```

- To view policy status of a managed cluster, you need permission to
  view policies in the managed cluster namespace on the hub cluster. If
  you do not have `view` access, such as through the OpenShift `view`
  `ClusterRole`, create a `ClusterRole`, such as `rhacm-view-policy`,
  with view access to policies with the following command:

  ``` bash
  oc create clusterrole rhacm-view-policy --resource=policies.policy.open-cluster-management.io --verb=get,list,watch
  ```

- To bind the new `ClusterRole` to the managed cluster namespace, run
  the following command to create a namespace `RoleBinding`:

  ``` bash
  oc create rolebinding rhacm-view-policy -n <cluster name> --clusterrole=rhacm-view-policy --user=<username>
  ```

### Enabling RBAC for Observability

To view the observability metrics for a managed cluster, you must have
`view` access to that managed cluster on the hub cluster. View the
following list of observability features:

- Access managed cluster metrics.

  Users are denied access to managed cluster metrics, if they are not
  assigned to the `view` role for the managed cluster on the hub
  cluster. Run the following command to verify if a user has the
  authority to create a `managedClusterView` role in the managed cluster
  namespace:

  ``` bash
  oc auth can-i create ManagedClusterView -n <managedClusterName> --as=<user>
  ```

  As a cluster administrator, create a `managedClusterView` role in the
  managed cluster namespace. Run the following command:

  ``` bash
  oc create role create-managedclusterview --verb=create --resource=managedclusterviews -n <managedClusterName>
  ```

  Then apply and bind the role to a user by creating a role bind. Run
  the following command:

  ``` bash
  oc create rolebinding user-create-managedclusterview-binding --role=create-managedclusterview --user=<user>  -n <managedClusterName>
  ```

- Search for resources.

  To verify if a user has access to resource types, use the following
  command:

  ``` bash
  oc auth can-i list <resource-type> -n <namespace> --as=<rbac-user>
  ```

  **Note:** `<resource-type>` must be plural.

- To view observability data in Grafana, you must have a `RoleBinding`
  resource in the same namespace of the managed cluster.

  View the following `RoleBinding` example:

  ``` yaml
  kind: RoleBinding
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
   name: <replace-with-name-of-rolebinding>
   namespace: <replace-with-name-of-managedcluster-namespace>
  subjects:
   - kind: <replace with User|Group|ServiceAccount>
     apiGroup: rbac.authorization.k8s.io
     name: <replace with name of User|Group|ServiceAccount>
  roleRef:
   apiGroup: rbac.authorization.k8s.io
   kind: ClusterRole
   name: view
  ```

See Role binding policy for more information. See Observability advanced
configuration to configure observability.

## Implementing fine-grained role-based access control with the console (Technology Preview)

**Technology Preview:** Red Hat Advanced Cluster Management for
Kubernetes supports fine-grained role-based access control (RBAC) for
virtual machines scenarios only. Manage and control permissions at the
namespace level and cluster level on your managed clusters. Grant
permissions to a virtual machine namespace within a cluster without
granting permission to the entire managed cluster.

Learn how to set up fine-grained RBAC from the console.

**Required access:** Cluster administrator

<div class="formalpara">

<div class="title">

Prerequisites

</div>

See the following requirements to begin using fine-grained role-based
access control:

</div>

### Assigning fine-grained role-based access control in the console

You can assign users to manage virtual machines with fine-grained
role-based access control. Actions are disabled in the console if the
user-role access is not permitted. Slide the **YAML** option on to see
the data that you enter populate in the YAML editor.

To assign permissions to a user, complete the following steps:

1.  Navigate to your `MultiClusterHub` custom resource to edit the
    resource and enable the feature.

    1.  From the **local-cluster** view, click **Operators** \>
        **Installed Operators** \> **Advanced Cluster Management for
        Kubernetes**.

    2.  Click the **MultiClusterHub** tab to edit the resource.

    3.  Slide the **YAML** option on to see the data in the YAML editor.

    4.  In your `MultiClusterHub` custom resource
        `spec.overrides.components` field, set
        `fine-grained-rbac-preview` to `true` to enable the feature.
        Change the `configOverrides` specification to `enabled: true` in
        the YAML editor and save your changes. See the following example
        with `fine-grained-rbac-preview` enabled:

    ``` yaml
        - configOverrides: {}
          enabled: true
          name: fine-grained-rbac-preview
    ```

2.  From the Fleet Management perspective, select **Infrastructure** \>
    **Clusters**.

3.  Select **`local-cluster`** from the cluster list.

4.  Click the **Edit** icon for the "Labels" detail field.

5.  Add the following label, `environment=virtualization`.

6.  Select the **Save** button to save your label changes.

7.  To create a `ClusterRoleBinding` resource for adding the
    `kubevirt.io-acm-hub:view` role, click **User Management** \>
    **Roles**. Your `ClusterRoleBinding` resource might resemble the
    following YAML file:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: kubevirt.io-acm-hub:view
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: <cluster-role-name>
    subjects:
    - kind: User
      apiGroup: rbac.authorization.k8s.io
      name: <user-name>
    ```

8.  **Optional:** If the `observability` service is enabled, create an
    additional `RoleBinding` resource on the hub cluster so that users
    can view virtual machine details in Grafana.

9.  Navigate to the **Identities** page from the console by clicking
    **User Management** \> **Identities**.

10. To view existing users or groups on your hub cluster, select either
    the *Users* or *Groups* tab.

11. To view your existing role assignments, click the **Role
    assignments** tab.

12. If you do not have any role assignments, create a role assignment by
    clicking the **Create role assignment** button.

13. Select the scope of your role assignment.

14. If you choose the **Select specific** option, a list of available
    clusters and namespaces appear.

15. Select the specific cluster set where you want to assign the role.

16. Move your selection to the *Chosen options* section.

17. Select the cluster set to see the list of *Select shared
    namespaces*.

18. Select the namespaces that you want to target.

19. Select the **Create** button to create the role assignment. Your
    role assignment appears from the **Role assignments** tab.

## Implementing fine-grained role-based access control in the terminal (Technology Preview)

**Technology Preview:** Red Hat Advanced Cluster Management for
Kubernetes supports fine-grained role-based access control (RBAC) for
virtual machine scenarios only. As a cluster administrator, you can
manage and control permissions at the namespace level and cluster level
on your managed clusters. Grant permissions to a virtual machine
namespace within a cluster without granting permission to the entire
managed cluster.

Learn how to set up for fine-grained role-based access control (RBAC)
from the terminal.

**Required access:** Cluster administrator

To learn about OpenShift Container Platform default and virtualization
roles and permissions, see Authorization in the OpenShift Container
Platform documentation.

See Implementing role-based access control for more details about Red
Hat Advanced Cluster Management role-based access.

<div class="formalpara">

<div class="title">

Prerequisites

</div>

See the following requirements to begin using fine-grained role-based
access control:

</div>

### Enabling fine-grained role-based access control in the terminal

When you enable fine-grained RBAC, the following roles for OpenShift
Virtualization are added automatically:

- `kubevirt.io:view`

- `kubevirt.io:edit`

- `kubevirt.io:admin`

- `kubevirt.io-acm-managed:admin`

- `kubevirt.io-acm-managed:view`

- `kubevirt.io-acm-hub:admin`

- `kubevirt.io-acm-hub:view`

**Note:** You must have access to the following roles to complete live
migration of your virtual machines: `kubevirt.io:admin`,
`kubevirt.io-acm-hub:admin`, and `kubevirt.io-acm-managed:view`.

Complete the following steps:

1.  Enable `fine-grained-rbac-preview` in the `MultiClusterHub`
    resource.

    1.  Run the following command:

        ``` bash
        oc edit mch -n open-cluster-management multiclusterhub
        ```

    2.  Edit to change the `configOverrides` specification from
        `enabled: false` to `enabled: true`. See the following example
        with the feature enabled:

        ``` yaml
            - configOverrides: {}
              enabled: true
              name: fine-grained-rbac-preview
        ```

    **Note:** Run `oc get mch -A` to get the name and namespace of the
    `MultiClusterHub` resource if you do not use the
    `open-cluster-management` namespace.

2.  Label your `local-cluster` with `environment=virtualization`. Run
    the following command:

    ``` bash
    oc label managedclusters local-cluster environment=virtualization
    ```

3.  Create a `ClusterRoleBinding` resource to add the
    `kubevirt.io-acm-hub:view` role. Run the following command:

    ``` bash
    oc create clusterrolebinding <cluster-role-binding-name> --clusterrole=kubevirt.io-acm-hub:view --user=<user-name>
    ```

    Your `ClusterRolebinding` resource might resemble the following YAML
    file:

    ``` yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRoleBinding
    metadata:
      name: kubevirt.io-acm-hub:view
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: <cluster-role-name>
    subjects:
    - kind: User
      apiGroup: rbac.authorization.k8s.io
      name: <user-name>
    ```

## Certificates

All certificates that are required by services that run on Red Hat
Advanced Cluster Management are created when you install Red Hat
Advanced Cluster Management. View the following list of certificates,
which are created and managed by the following components of Red Hat
OpenShift Container Platform:

- OpenShift Service Serving Certificates

- Red Hat Advanced Cluster Management webhook controllers

- Kubernetes Certificates API

- OpenShift default ingress

**Required access**: Cluster administrator

**Note:** Users are responsible for certificate rotations and updates.

### Red Hat Advanced Cluster Management hub cluster certificates

OpenShift Container Platform default ingress certificate is a type of
hub cluster certificate. After you install Red Hat Advanced Cluster
Management, Observability certificates are created and used by the
Observability components to give mutual TLS for traffic between the hub
and managed cluster. Access the Observability namespaces to retrieve and
implement the different Observability certificates.

- The following certificates are a part of the
  `open-cluster-management-observability` namespace:

  - `observability-server-ca-certs`: Has the CA certificate to sign
    server-side certificates

  - `observability-client-ca-certs`: Has the CA certificate to sign
    client-side certificates

  - `observability-server-certs`: Has the server certificate used by the
    `observability-observatorium-api` deployment

  - `observability-grafana-certs`: Has the client certificate used by
    the `observability-rbac-query-proxy` deployment

- The `open-cluster-management-addon-observability` namespace includes
  the following certificates on managed clusters:

  - `observability-managed-cluster-certs`: Has the same server CA
    certificate as `observability-server-ca-certs` in the hub server

  - `observability-controller-open-cluster-management.io-observability-signer-client-cert`:
    Has the client certificate used by the
    `metrics-collector-deployment`

The CA certificates are valid for five years and other certificates are
valid for one year. All Observability certificates are automatically
refreshed upon expiration. View the following list to understand the
effects when certificates are automatically renewed:

- Non-CA certificates are renewed automatically when the remaining valid
  time is no more than 73 days. After the certificate is renewed, the
  pods in the related deployments restart automatically to use the
  renewed certificates.

- CA certificates are renewed automatically when the remaining valid
  time is no more than one year. After the certificate is renewed, the
  old CA is not deleted but co-exist with the renewed ones. Both old and
  renewed certificates are used by related deployments, and continue to
  work. The old CA certificates are deleted when they expire.

- When a certificate is renewed, the traffic between the hub cluster and
  managed cluster is not interrupted.

View the following Red Hat Advanced Cluster Management hub cluster
certificates table:

- Namespace: open-cluster-management - Secret name:
  channels-apps-open-cluster-management-webhook-svc-ca - Pod label:
  app=multicluster-operators-channel

- Namespace: open-cluster-management - Secret name:
  channels-apps-open-cluster-management-webhook-svc-signed-ca - Pod
  label: app=multicluster-operators-channel

- Namespace: open-cluster-management - Secret name:
  multicluster-operators-application-svc-ca - Pod label:
  app=multicluster-operators-application

- Namespace: open-cluster-management - Secret name:
  multicluster-operators-application-svc-signed-ca - Pod label:
  app=multicluster-operators-application

- Namespace: open-cluster-management-hub - Secret name:
  registration-webhook-serving-cert signer-secret - Pod label: Not
  required

- Namespace: open-cluster-management-hub - Secret name:
  work-webhook-serving-cert - Pod label: Not required

### Red Hat Advanced Cluster Management managed certificates

Use Red Hat Advanced Cluster Management managed certificates to
authenticate managed clusters within your hub cluster. The following
managed cluster certificates get managed and refreshed automatically.

If you customize the hub cluster API server certificate, the managed
cluster automatically updates its certificates. View the following table
for a summarized list of the component pods that contain Red Hat
Advanced Cluster Management managed certificates and the related
secrets:

- Namespace: open-cluster-management-agent-addon - Secret name (if
  applicable):
  cluster-proxy-open-cluster-management.io-proxy-agent-signer-client-cert

- Namespace: open-cluster-management-agent-addon - Secret name (if
  applicable): cluster-proxy-service-proxy-server-certificates

## Managing certificates

Maintain the security and reliability of your cluster management
environment by managing your certificates. Continue reading to learn how
to refresh, replace, rotate, and list certificates.

### Refreshing a Red Hat Advanced Cluster Management webhook certificate

You can refresh Red Hat Advanced Cluster Management managed
certificates, which are certificates that are created and managed by Red
Hat Advanced Cluster Management services.

Complete the following steps to refresh certificates managed by Red Hat
Advanced Cluster Management:

1.  Delete the secret that is associated with the Red Hat Advanced
    Cluster Management managed certificate, and replace `<namespace>`
    and `<secret>` with the values that you want to use. Run the
    following command:

    ``` bash
    oc delete secret -n <namespace> <secret>
    ```

2.  Restart the services that are associated with the Red Hat Advanced
    Cluster Management managed certificates, and replace `<namespace>`
    and `<pod-label>` with the values for the Red Hat Advanced Cluster
    Management managed cluster certificates. Run the following command:

    ``` bash
    oc delete pod -n <namespace> -l <pod-label>
    ```

    **Note:** If a `pod-label` is not specified, there is no service
    that must be restarted. The secret is recreated and used
    automatically.

### Replacing certificates for *alertmanager* route

If you do not want to use the OpenShift Container Platform default
ingress certificate, replace observability `alertmanager` certificates
by updating the Alertmanager route. Complete the following steps:

1.  Examine the observability certificate with the following command:

    ``` bash
    openssl x509  -noout -text -in ./observability.crt
    ```

2.  Change the common name (`CN`) on the certificate to `alertmanager`.

3.  Change the SAN in the `csr.cnf` configuration file with the hostname
    for your `alertmanager` route.

4.  Create the `alertmanager-byo-ca` Secret resource in the
    `open-cluster-management-observability` namespace by running the
    following command:

    ``` bash
    oc -n open-cluster-management-observability create secret tls alertmanager-byo-ca --cert ./ca.crt --key ./ca.key
    ```

5.  Create the `alertmanager-byo-cert` `Secret` resource in the
    `open-cluster-management-observability` namespace by running the
    following command:

    ``` bash
    oc -n open-cluster-management-observability create secret tls alertmanager-byo-cert --cert ./ingress.crt --key ./ingress.key
    ```

### Rotating the Gatekeeper webhook certificate

Complete the following steps to rotate the Gatekeeper webhook
certificate:

1.  Edit the `Secret` resource that contains the Gatekeeper webhook
    certificate with the following command:

    ``` bash
    oc edit secret -n openshift-gatekeeper-system gatekeeper-webhook-server-cert
    ```

2.  Delete the following content in the `data` section: `ca.crt`,
    `ca.key`, `tls.crt`, and `tls.key`.

3.  Restart the Gatekeeper webhook service by deleting the
    `gatekeeper-controller-manager` pods with the following command:

    ``` bash
    oc delete pod -n openshift-gatekeeper-system -l control-plane=controller-manager
    ```

The Gatekeeper webhook certificate is rotated.

### Verifying certificate rotation

Verify that your certificates are rotated to prevent system outages that
can effect service communication. Complete the following steps:

1.  Identify the `Secret` resource that you want to check.

2.  Check the `tls.crt` key to verify that a certificate is available.

3.  Display the certificate information. Replace `<your-secret-name>`
    with the name of secret that you are verifying. If it is necessary,
    also update the namespace and JSON path. Run the following command:

    ``` bash
    oc get secret <your-secret-name> -n open-cluster-management -o jsonpath='{.data.tls\.crt}' | base64 -d | openssl x509 -text -noout
    ```

4.  Check the `Validity` details in the output. View the following
    `Validity` example:

    ``` bash
    Validity
                Not Before: Jul 13 15:17:50 2023 GMT 
                Not After : Jul 12 15:17:50 2024 GMT 
    ```

    - The `Not Before` value is the date and time that you rotated your
      certificate.

    - The `Not After` value is the date and time for the certificate
      expiration.

### Listing hub cluster managed certificates

You can view a list of hub cluster managed certificates that use
OpenShift Service Serving Certificates service internally. Run the
following command to list the certificates:

``` bash
for ns in multicluster-engine open-cluster-management ; do echo "$ns:" ; oc get secret -n $ns -o custom-columns=Name:.metadata.name,Expiration:.metadata.annotations.service\\.beta\\.openshift\\.io/expiry | grep -v '<none>' ; echo ""; done
```

For more information, see *OpenShift Service Serving Certificates* in
the *Additional resources* section.

**Note:** If observability is enabled, there are additional namespaces
where certificates are created.

## Bringing your own Certificate Authority (CA) certificates for Observability

When you install Red Hat Advanced Cluster Management for Kubernetes,
only Certificate Authority (CA) certificates for Observability are
provided by default. If you do not want to use the default Observability
CA certificates, you can choose to bring your own observability CA
certificates before you enable Observability.

<div class="formalpara">

<div class="title">

Prerequisites

</div>

**Required access:** Administrator

</div>

### Customizing your CA certificates for Observability

When you choose to bring your own Observability CA certificate,
customize it to make it help you with your specific development needs.
Customize your CA certificates for Observability with the following
steps:

1.  Generate CA certificates for the server-side and the client-side by
    using OpenSSL commands.

    1.  To generate your CA RSA private keys for the server-side, run
        the following command:

        ``` bash
        openssl genrsa -out serverCAKey.pem 2048
        ```

    2.  To generate your CA RSA private keys for the client-side, run
        the following command:

    ``` bash
    openssl genrsa -out clientCAKey.pem 2048
    ```

2.  Generate the self-signed CA certificates using the private keys.

    1.  To generate the self-signed CA certificates for the server-side,
        run the following command:

        ``` bash
        openssl req -x509 -sha256 -new -nodes -key serverCAKey.pem -days 1825 -out serverCACert.pem
        ```

    2.  To generate the self-signed CA certificates for the client-side,
        run the following command:

    ``` bash
    openssl req -x509 -sha256 -new -nodes -key clientCAKey.pem -days 1825 -out clientCACert.pem
    ```

3.  To store and manage your CA certificates for Observability, create
    `Secret` resources for each CA certificate.

    1.  Create the `observability-server-ca-certs` secret by using your
        certificate and private key. Run the following command:

        ``` bash
        oc -n open-cluster-management-observability create secret tls observability-server-ca-certs --cert ./serverCACert.pem --key ./serverCAKey.pem
        ```

    2.  Create the `observability-client-ca-certs` secret by using your
        certificate and private key. Run the following command:

    ``` bash
    oc -n open-cluster-management-observability create secret tls observability-client-ca-certs --cert ./clientCACert.pem --key ./clientCAKey.pem
    ```

### Replacing certificates for *rbac-query-proxy* route

You can replace certificates for the `rbac-query-proxy` route by
creating a Certificate Signing Request (CSR) by using the `csr.cnf`
file.

<div class="formalpara">

<div class="title">

Prerequisites

</div>

Generate CA certifates by using OpenSSL commands. See, Customizing your
CA certificates for Observability to create certificates.

</div>

Update the `DNS.1` field in the `subjectAltName` section to match the
host name of the `rbac-query-proxy` route. Complete the following steps:

1.  Retrieve the host name by running the following command:

    ``` bash
    oc get route rbac-query-proxy -n open-cluster-management-observability -o jsonpath="
    {.spec.host}"
    ```

2.  Create a `proxy-byo-ca` secret by using the generated certificates.
    Run the following command:

    ``` bash
    oc -n open-cluster-management-observability create secret tls proxy-byo-ca --cert ./ca.crt --key ./ca.key
    ```

3.  Run the following command to create a `proxy-byo-cert` secret by
    using the generated certificates:

    ``` bash
    oc -n open-cluster-management-observability create secret tls proxy-byo-cert --cert ./ingress.crt --key ./ingress.key
    ```

## Role-based access control for managed clusters with cluster permissions

Manage Kubernetes native resources such as `Roles`, `ClusterRoles`,
`RoleBindings`, and `ClusterRoleBindings` resources across multiple
managed clusters from a by using the cluster permission feature. The
`ClusterPermssion` resource automatically distributes role-based access
control (RBAC) resources to managed clusters and manage the resource
lifecycles.

With the cluster permssions API,
`clusterpermissions.rbac.open-cluster-management.io`, you can specify
the RBAC policies you want to apply to your managed clusters.

### Enabling validation for cluster permissions

Enable the `validate` specification within your `ClusterPermission`
resources to check the existence of your `Role` and `ClusterRole`
resources.

**Required access:** Cluster administrator

Complete the following steps:

1.  Create a `ClusterPermission` resource where you set the `validate`
    specification to `true`.Define the `roleBindings` and
    `clusterRoleBinding` that you want to validate.

    Your YAML file might resemble the following example where you
    configure the `ClusteerRole` to validate the `edit` `ClusterRole`
    for the `sa-sample-existing` `ServiceAccount`, and the `view`
    `ClusterRole` for `Group1`:

    ``` yaml
    apiVersion: rbac.open-cluster-management.io/v1alpha1
    kind: ClusterPermission
    metadata:
      name: clusterpermission-validate-sample
    spec:
      validate: true
      roleBindings:
        - name: default-existing
          namespace: default
          roleRef:
            apiGroup: rbac.authorization.k8s.io
            kind: ClusterRole
            name: edit
          subject:
            namespace: openshift-gitops
            kind: ServiceAccount
            name: sa-sample-existing
      clusterRoleBinding:
          name: crb-cluster1-argo-app-con-3-existing
          roleRef:
            apiGroup: rbac.authorization.k8s.io
            kind: ClusterRole
            name: view
          subject:
            apiGroup: rbac.authorization.k8s.io
            kind: Group
            name: group1
    ```

2.  Apply your `clusterpermission-validate-sample` `ClusterPermission`
    by running the following command:

    ``` bash
    oc apply clusterpermission-validate-sample.yaml
    ```
