# GitOps overview

Red Hat OpenShift Container Platform GitOps and Argo CD is integrated
with Red Hat Advanced Cluster Management for Kubernetes, with advanced
features compared to the previous Application Lifecycle *Channel* and
*Subscription* model.

GitOps integration with Argo CD development is active, as well as the
large community that contributes feature enhancements and updates to
Argo CD. By utilizing the OpenShift Container Platform GitOps Operator,
you can use the latest advancements in Argo CD development and receive
support from the GitOps Operator subscription.

## GitOps console

Learn more about integrated OpenShift Container Platform GitOps console
features. Create and view applications, such as *ApplicationSet*, and
*Argo CD* types. An `ApplicationSet` represents Argo applications that
are generated from the controller.

- You click **Launch resource in Search** to search for related
  resources.

- Use *Search* to find application resources by the component `kind` for
  each resource.

**Important:** Available actions are based on your assigned role. Learn
about access requirements from the Role-based access control
documentation.

### Prerequisites

See the following prerequisites and requirements:

- For an Argo CD `ApplicationSet` to be created, you need to enable
  `Automatically sync when cluster state changes` from the
  `Sync policy`.

- For Flux with the `kustomization` controller, find Kubernetes
  resources with the label
  `kustomize.toolkit.fluxcd.io/name=<app_name>`.

- For Flux with the `helm` controller, find Kubernetes resources with
  the label `helm.toolkit.fluxcd.io/name=<app_name>`.

- You need GitOps cluster resources and the GitOps operator installed to
  create an `ApplicationSet`. Without these prerequisites, you will see
  no **Argo server** options in the console to create an
  `ApplicationSet`.

### Querying Argo CD applications

When you search for an Argo CD application, you are directed to the
*Applications* page. Complete the following steps to access the Argo CD
application from the *Search* page:

1.  Log in to your Red Hat Advanced Cluster Management hub cluster.

2.  From the console header, select the *Search* icon.

3.  Filter your query with the following values: `kind:application` and
    `apigroup:argoproj.io`.

4.  Select an application to view. The *Application* page displays an
    overview of information for the application.

For more information about search, see Search service.

## Deploying the Argo CD *ApplicationSet* resource in any namespace for pull model (Technology Preview)

With the Argo CD pull model, you can create `ApplicationSet` resources
in any namespace on your hub clusters.

To fully manage your Argo CD `ApplicationSet` resources, complete the
following sections:

**Required access:** Cluster administrator

### Deploying the *ApplicationSet* resource for standard configurations

If you have limited support for role-based access control (RBAC), then
you might want to deploy the `ApplicationSet` resource for standard
configurations.

For simple RBAC management, you can deploy the `ApplicationSet` resource
for standard configurations, giving you the following benefits:

- Namespaces are not specified in the GitHub repository resources.

- The destination of the workload namespace is specified in the
  `Application` template.

- The `ApplicationSet` resource uses the default `AppProject` resource.

To deploy the `ApplicationSet` resource for standard configurations,
complete the following steps:

1.  In the `openshift-gitops` namespace, create a `Placement` resource.

2.  Create the `ApplicationSet` resource in the `appset-2` namespace
    with the default `AppProject` resource by adding the following YAML
    file sample:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      annotations:
      name: appset-2
    ```

3.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f namespace-example.yaml
    ```

4.  Create the `ApplicationSet` resource in the `appset-2` namespace
    with the default `AppProject` resource by adding the following YAML
    file sample:

    ``` yaml
    apiVersion: argoproj.io/v1alpha1
    kind: ApplicationSet
    metadata:
      name: helloworld
      namespace: appset-2
    spec:
      generators:
      - clusterDecisionResource:
          configMapRef: acm-placement
          labelSelector:
            matchLabels:
              cluster.open-cluster-management.io/placement: all-openshift-clusters
          requeueAfterSeconds: 30
      template:
        metadata:
          annotations:
            apps.open-cluster-management.io/ocm-managed-cluster: '{{name}}'
            argocd.argoproj.io/skip-reconcile: "true"
          labels:
            apps.open-cluster-management.io/pull-to-ocm-managed-cluster: "true"
          name: '{{name}}-helloworld'
        spec:
          destination:
            namespace: helloworld
            server: https://kubernetes.default.svc
          project: default
          source:
            path: helloworld
            repoURL: https://github.com/stolostron/application-samples.git
            targetRevision: HEAD
          syncPolicy:
            automated: {}
    ```

5.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f applicationset-example.yaml
    ```

    - The `ApplicationSet` resource gets created in the `appset-2`
      namespace on your hub cluster.

    - The `Application` resources get deployed to the `appset-2`
      namespace on your managed clusters.

    - The `Application` resource deploys its workloads to the
      `Helloworld` namespace on your managed clusters.

    - The default Argo CD `AppProject` resource configuration gets
      applied

    - All the `Application` resources defined in the specified path of
      the GitHub repository are not namespace specific.

### Deploying the *ApplicationSet* resource for advanced configurations

If you have support for role-based access control (RBAC), then you have
the option to deploy the `ApplicationSet` resource for advanced
configurations.

You can deploy the `ApplicationSet` resource for advanced configurations
with more RBAC management, giving you the following benefits:

- The `Application` resource workload namespaces specified in the GitHub
  repository resources.

- The destination of the workload namespace that is specified in the
  `ApplicationSet` resource matches the GitHub repository.

- The `ApplicationSet` resource uses the custom Argo CD `AppProject`
  resource for RBAC control.

To deploy the `ApplicationSet` resource for advanced configurations,
complete the following steps:

1.  In the `openshift-gitops` namespace, create a `Placement` resource.

2.  Create the `ApplicationSet` resource in the `bgdk` namespace with
    the custom `bgdk` `AppProject` resource by adding the following YAML
    file sample:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      annotations:
      name: bgdk
    ```

3.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f namespace-example.yaml
    ```

4.  Set the `bgdk` `AppProject` resource configuration in the OpenShift
    GitOps namespace by adding the following YAML file sample:

    ``` yaml
    apiVersion: argoproj.io/v1alpha1
    kind: AppProject
    metadata:
      name: bgdk
      namespace: openshift-gitops
    spec:
      sourceNamespaces:
      - bgdk
      sourceRepos:
      - https://github.com/redhat-developer-demos/openshift-gitops-examples.git
      destinations:
      - namespace: bgdk
        server: https://kubernetes.default.svc
      clusterResourceWhitelist:
      - group: ''
        kind: Namespace
    ```

    - `sourceNamespaces` is the namespace where the `Application` itself
      gets created.

    - `sourceRepos` is the repository that the `Application` template
      uses.

    - `destinations` is the namespace where the `Application` deploys
      its workloads.

    - `clusterResourceWhitelist` is a cluster scoped resource list that
      the `Application` is allowed to deploy. In this scenario, this
      namespace kind is mandatory because the `Application` must create
      a new namespace.

5.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f appproject-example.yaml
    ```

6.  Apply the customized Argo CD `AppProject` resource configuration to
    the `ApplicationSet` resource. by adding the following YAML file
    sample:

    ``` yaml
    apiVersion: argoproj.io/v1alpha1
    kind: ApplicationSet
    metadata:
      name: bgdk-2
      namespace: bgdk
    spec:
      generators:
      - clusterDecisionResource:
          configMapRef: acm-placement
          labelSelector:
            matchLabels:
              cluster.open-cluster-management.io/placement: all-openshift-clusters
          requeueAfterSeconds: 30
      template:
        metadata:
          annotations:
            apps.open-cluster-management.io/ocm-managed-cluster: '{{name}}'
            argocd.argoproj.io/skip-reconcile: "true"
          labels:
            apps.open-cluster-management.io/pull-to-ocm-managed-cluster: "true"
          name: '{{name}}-bgdk'
        spec:
          destination:
            namespace: bgdk
            server: https://kubernetes.default.svc
          project: bgdk
          source:
            path: apps/bgd/overlays/bgdk
            repoURL: https://github.com/redhat-developer-demos/openshift-gitops-examples.git
            targetRevision: HEAD
          syncPolicy:
            automated: {}
    ```

7.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f applicationset-example.yaml
    ```

<div class="formalpara">

<div class="title">

Additional resources

</div>

To learn more about the `ArgoCD` `ApplicationSet`, see the following
resources:

</div>

## Enabling the *ApplicationSet* resource in any namespace

You can enable the `ApplicationSet` resources in any namespace on your
hub clusters.

To enable your Argo CD `ApplicationSet` resources, complete the
following sections:

**Required access:** Cluster administrator

### Enabling the *ApplicationSet* resource in any namespace on the hub cluster

To enable the Argo CD `ApplicationSet` resource in any namespace on your
hub cluster, complete the following steps:

1.  From your command-line interface, clone the GitHub repository by
    running the following command:

    ``` bash
    git clone https://github.com/stolostron/multicloud-integrations
    ```

2.  Go to the GitHub repository that you cloned by running the following
    command:

    ``` bash
    cd multicloud-integrations/deploy/appset-any-namespace
    ```

3.  Enable the `ApplicationSet` resource in any namespace by running the
    following command:

    ``` bash
     ./setup-appset-any-namespace.sh --namespace openshift-gitops --argocd-name openshift-gitops
    ```

4.  Verify that the OpenShift GitOps instance restarted and is running
    on your hub cluster. Run the following command on your hub cluster:

    ``` bash
    oc get pods -n openshift-gitops
    ```

### Enabling the *Application* resource in any namespace on the managed clusters

The Red Hat Advanced Cluster Management OpenShift GitOps add-on launches
a OpenShift GitOps instance that you can use to enable the `Application`
resource in any namespace on your managed cluster. To enable the Argo CD
`Application` resource in any namespace on the managed clusters,
complete the following steps:

1.  Create a global `ManagedClusterSetBinding` resource by adding the
    following YAML file sample:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    apiVersion: cluster.open-cluster-management.io/v1beta2
    kind: ManagedClusterSetBinding
    metadata:
      name: global
      namespace: openshift-gitops
    spec:
      clusterSet: global
    ```

2.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f managedclustersetbinding-example.yaml
    ```

3.  Create a `Placement` custom resource for selecting the managed
    clusters where the (gitops-short) add-on gets enabled. Add the
    following YAML file sample:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: Placement
    metadata:
      name: all-openshift-clusters
      namespace: openshift-gitops
    spec:
      tolerations:
      - key: cluster.open-cluster-management.io/unreachable
        operator: Exists
      - key: cluster.open-cluster-management.io/unavailable
        operator: Exists
      predicates:
      - requiredClusterSelector:
          labelSelector:
            matchExpressions:
            - key: vendor
              operator: "In"
              values:
              - OpenShift
    ```

4.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f placement-example.yaml
    ```

5.  Create the `GitOpsCluster` resource and add the `gitopsAddon`
    specification. Your YAML file might resemble the following sample:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: argo-acm-importer
      namespace: openshift-gitops
    spec:
      argoServer:
        cluster: notused
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters
        namespace: openshift-gitops
      gitopsAddon:
        enabled: true
        overrideExistingConfigs: true
        reconcileScope: All-Namespaces
    ```

6.  Apply the YAML file sample by running the following command:

    ``` bash
    oc apply -f gitopscluster-example.yaml
    ```

7.  Verify that the OpenShift GitOps instance restarted and is running
    on your managed clusters by running the following command on your
    managed clusters:

    ``` bash
    oc get pods -n openshift-gitops
    ```

<div class="formalpara">

<div class="title">

Additional resources

</div>

Continue to fully manage your Argo CD `ApplicationSet` resources by
deploying them. For directions, see Deploying the Argo CD ApplicationSet
resource in any namespace for pull model (Technology Preview).

</div>

## Registering managed clusters to Red Hat OpenShift GitOps operator

To configure OpenShift GitOps with the Push model, you can register a
set of one or more Red Hat Advanced Cluster Management for Kubernetes
managed clusters to an instance of OpenShift GitOps operator. After
registering, you can deploy applications to those clusters. Set up a
continuous OpenShift GitOps environment to automate application
consistency across clusters in development, staging, and production
environments.

### Prerequisites

1.  You need to install the Red Hat OpenShift GitOps operator on your
    Red Hat Advanced Cluster Management for Kubernetes.

2.  Import one or more managed clusters.

3.  To register managed clusters to OpenShift GitOps, complete the
    Creating a ManagedClusterSet documentation.

4.  Enable the `ManagedServiceAccount` addon to rotate the token that is
    used for the Argo CD push and pull model to connect to the managed
    cluster. For help enabling the addon, see Configuring klusterlet
    add-ons.

### Registering managed clusters to Red Hat OpenShift GitOps

Complete the following steps to register managed clusters to OpenShift
GitOps:

1.  Create a managed cluster set by binding it to the namespace where
    OpenShift GitOps is deployed.

    1.  For more general information about creating a
        `ManagedClusterSetBinding`, go to the *Additional resources*
        section and see *Creating a ManagedClusterSetBinding resource* .

    2.  For placement information, see Filtering with ManagedCluster
        objects.

2.  In the namespace that is used in managed cluster set binding, create
    a `Placement` custom resource to select a set of managed clusters to
    register to an OpenShift GitOps operator instance. Use the
    `multicloud-integration` placement example as a template. See *Using
    ManagedClusterSets with Placement* for placement information.

    **Notes:**

    - Only OpenShift Container Platform clusters are registered to an
      OpenShift GitOps operator instance, not other Kubernetes clusters.

    - In some unstable network scenarios, the managed clusters might be
      temporarily placed in `unavailable` or `unreachable` state. See
      *Configuring placement tolerations for Red Hat Advanced Cluster
      Management and OpenShift GitOps* for more details.

3.  Create a `GitOpsCluster` custom resource to register the set of
    managed clusters from the placement decision to the specified
    instance of OpenShift GitOps. This enables the OpenShift GitOps
    instance to deploy applications to any of those Red Hat Advanced
    Cluster Management managed clusters. Use the
    `multicloud-integrations` OpenShift GitOps cluster example.

    **Note:** The referenced `Placement` resource must be in the same
    namespace as the `GitOpsCluster` resource. See the following
    example:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: gitops-cluster-sample
      namespace: dev
    spec:
      argoServer:
        cluster: <your-local-cluster-name>
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters 
    ```

    - The `placementRef.name` value is `all-openshift-clusters`, and is
      specified as target clusters for the OpenShift GitOps instance
      that is installed in `argoNamespace: openshift-gitops`. The
      `argoServer.cluster` specification requires the
      `<your-local-cluster-name>` value.

4.  Save your changes. You can now follow the OpenShift GitOps workflow
    to manage your applications.

### Registering non-OpenShift Container Platform clusters to Red Hat OpenShift GitOps

You can now use the Red Hat Advanced Cluster Management `GitOpsCluster`
resource to register a non-OpenShift Container Platform cluster to a
OpenShift GitOps cluster. With this capability, you can deploy
application resources to the non-OpenShift Container Platform cluster by
using the OpenShift GitOps console. To register a non-OpenShift
Container Platform cluster to a OpenShift GitOps cluster, complete the
following steps:

1.  Go to the API server URL in the non-OpenShift Container Platform
    `ManagedCluster` resource `spec` and validate it by running the
    following command:

    ``` bash
    oc get managedclusters eks-1
    ```

2.  Verify that your output resembles the following information:

    ``` bash
    NAME    HUB ACCEPTED   MANAGED CLUSTER URLS                                                      JOINED   AVAILABLE   AGE
    eks-1   true           https://5E336C922AB16684A332C10535B8D407.gr7.us-east-2.eks.amazonaws.com  True     True        37m
    ```

3.  If the API server URL in the non-OpenShift Container Platform
    `MangedCluster` resource `spec` is empty, update it manually by
    completing the following steps:

    1.  To complete the API server URL, edit the `MangedCluster`
        resource `spec` by running the following command:

        ``` bash
        oc edit managedclusters eks-1
        ```

    2.  Verify that your YAML resembles the following file:

        ``` bash
        spec:
          managedClusterClientConfigs:
          - caBundle: ZW1wdHlDQWJ1bmRsZQo=
            url: https://5E336C922AB16684A332C10535B8D407.gr7.us-east-2.eks.amazonaws.com
        ```

    3.  Save the changes then validate that the API server is completed
        by running the following command:

        ``` bash
        oc get managedclusters eks-1
        ```

    4.  Verify that your output resembles the following information:

    ``` bash
    NAME     HUB ACCEPTED  MANAGED CLUSTER URLS                                                      JOINED   AVAILABLE   AGE
    eks-1    true          https://5E336C922AB16684A332C10535B8D407.gr7.us-east-2.eks.amazonaws.com  True     True        37m
    ```

4.  To verify that the cluster secret is generated, go to the
    `openshift-gitops` namespace and confirm that that `GitOpsCluster`
    resource status reports, `successful`.

    **Notes:**

    - The API server URL for all types of non-OpenShift Container
      Platform `ManagedCluster` resources renders automatically if you
      use the following importing modes:

      - Entering your server URL and API token for the existing cluster.

      - Entering the `kubeconfig` file for the existing cluster.

    - The following cases can make the API server URL empty for one of
      the `ManagedClusters` resources:

      - The non-OpenShift Container Platform cluster is imported to the
        Red Hat Advanced Cluster Management hub cluster before version
        2.12.

      - The non-OpenShift Container Platform cluster is manually
        imported to the Red Hat Advanced Cluster Management hub cluster
        through the import mode, `Run import commands`.

### Red Hat OpenShift GitOps token

When you integrate with the OpenShift GitOps operator, for every managed
cluster that is bound to the OpenShift GitOps namespace through the
placement and `ManagedClusterSetBinding` custom resources, a secret with
a token to access the `ManagedCluster` is created in the OpenShift
GitOps instance server namespace.

The OpenShift GitOps controller needs this secret to sync resources to
the managed cluster. By default, the service account application manager
works with the cluster administrator permissions on the managed cluster
to generate the OpenShift GitOps cluster secret in the OpenShift GitOps
instance server namespace. The default namespace is `openshift-gitops`.

If you do not want this default, create a service account with
customized permissions on the managed cluster for generating the
OpenShift GitOps cluster secret in the OpenShift GitOps instance server
namespace. The default namespace is still, `openshift-gitops`. For more
information, see Creating a customized service account for Argo CD push
model.

## Configuring application placement tolerations for GitOps

Red Hat Advanced Cluster Management provides a way for you to register
managed clusters that deploy applications to Red Hat OpenShift GitOps.

In some unstable network scenarios, the managed clusters might be
temporarily placed in `Unavailable` state. If a `Placement` resource is
being used to facilitate the deployment of applications, add the
following tolerations for the `Placement` resource to continue to
include unavailable clusters. The following example shows a `Placement`
resource with tolerations:

``` yaml
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name: placement
  namespace: ns1
spec:
  tolerations:
    - key: cluster.open-cluster-management.io/unreachable
      operator: Exists
    - key: cluster.open-cluster-management.io/unavailable
      operator: Exists
```

## Deploying Argo CD with Push and Pull model

Using a *Push model*, The Argo CD server on the hub cluster deploys the
application resources on the managed clusters. For the *Pull model*, the
application resources are propagated by the *Propagation controller* to
the managed clusters by using `manifestWork`.

For both models, the same `ApplicationSet` CRD is used to deploy the
application to the managed cluster.

**Required access:** Cluster administrator

### Prerequisites

View the following prerequisites for the Argo CD Pull model:

**Important:**

- If your `openshift-gitops-ArgoCD-application-controller` service
  account is *not* assigned as a cluster administrator, the Red Hat
  OpenShift GitOps application controller might not deploy resources.
  The application status might send an error similar to the following
  error:

<!-- -->

    cannot create resource "services" in API group "" in the namespace
    "mortgage",deployments.apps is forbidden: User
    "system:serviceaccount:openshift-gitops:openshift-gitops-Argo CD-application-controller"

- After you install the `OpenShift Gitops` operator on the managed
  clusters, you must create the `ClusterRoleBinding` cluster
  administrator privileges on the same managed clusters.

- To add the `ClusterRoleBinding` cluster administrator privileges to
  your managed clusters, see the following example YAML:

  ``` yaml
  kind: ClusterRoleBinding
  apiVersion: rbac.authorization.k8s.io/v1
  metadata:
    name: argo-admin
  subjects:
    - kind: ServiceAccount
      name: openshift-gitops-argocd-application-controller
      namespace: openshift-gitops
  roleRef:
    apiGroup: rbac.authorization.k8s.io
    kind: ClusterRole
    name: cluster-admin
  ```

- If you are not a cluster administrator and need to resolve this issue,
  complete the following steps:

  1.  Create all namespaces on each managed cluster where the Argo CD
      application will be deployed.

  2.  Add the `managed-by` label to each namespace. If an Argo CD
      application is deployed to multiple namespaces, each namespace
      should be managed by Argo CD.

      See the following example with the `managed-by` label:

  ``` yaml
  apiVersion: v1
  kind: Namespace
  metadata:
    name: mortgage2
    labels:
      argocd.argoproj.io/managed-by: openshift-gitops
  ```

  1.  You must declare all application destination namespaces in the
      repository for the application and include the `managed-by` label
      in the namespaces. Refer to *Additional resources* to learn how to
      declare a namespace.

See the following requirements to use the Argo CD *Pull* model:

- The Red Hat OpenShift GitOps operator must be installed on the hub
  cluster and the target managed clusters in the `openshift-gitops`
  namespace.

- The required hub cluster OpenShift Container Platform OpenShift GitOps
  operator must be version 1.9.0 or later.

- The version of the Red Hat OpenShift GitOps Operator on the hub
  cluster must be equal to or more recent than the version of the
  operator on the managed clusters.

- You need the *ApplicationSet controller* to propagate the Argo CD
  application template for a managed cluster.

- Every managed cluster must have a cluster secret in the Argo CD server
  namespace on the hub cluster, which is required by the ArgoCD
  application set controller to propagate the Argo CD application
  template for a managed cluster.

  To create the cluster secret, create a `gitOpsCluster` resource that
  contains a reference to a `placement` resource. The `placement`
  resource selects all the managed clusters that need to support the
  Pull model. When the OpenShift GitOps cluster controller reconciles,
  it creates the cluster secrets for the managed clusters in the Argo CD
  server namespace.

### Architecture

For both Push and Pull model, the *Argo CD ApplicationSet controller* on
the hub cluster reconciles to create application resources for each
target managed cluster. See the following information about architecture
for both models:

#### Architecture Push model

- With Push model, OpenShift Container Platform GitOps applies resources
  *directly* from a centralized hub cluster to the managed clusters.

- An Argo CD application that is running on the hub cluster communicates
  with the GitHub repository and deploys the manifests directly to the
  managed clusters.

- Push model implementation only contains the Argo CD application on the
  hub cluster, which has credentials for managed clusters. The Argo CD
  application on the hub cluster can deploy the applications to the
  managed clusters.

- **Important:** With a large number of managed clusters that require
  resource application, consider potential strain on the OpenShift
  GitOps GitOps controller memory and CPU usage. To optimize resource
  management, see Configuring resource quota or requests in the Red Hat
  OpenShift GitOps documentation.

- By default, the Push model is used to deploy the application unless
  you add the `apps.open-cluster-management.io/ocm-managed-cluster` and
  `apps.open-cluster-management.io/pull-to-ocm-managed-cluster`
  annotations to the template section of the `ApplicationSet`.

#### Architecture Pull model

- Pull model can provide scalability relief compared to the push model
  by reducing stress on the controller in the hub cluster, but with more
  requests and status reporting required.

- With Pull model, OpenShift Container Platform OpenShift GitOps *does
  not* apply resources directly from a centralized hub cluster to the
  managed clusters. The Argo CD Application is propagated from the hub
  cluster to the managed clusters.

- Pull model implementation applies OpenShift Cluster Manager
  registration, placement, and `manifestWork` APIs so that the hub
  cluster can use the secure communication channel between the hub
  cluster and the managed cluster to deploy resources.

- Each managed cluster individually communicates with the GitHub
  repository to deploy the resource manifests locally, so you must
  install and configure OpenShift GitOps operators on each managed
  cluster.

- An Argo CD server must be running on each target managed cluster. The
  Argo CD application resources are replicated on the managed clusters,
  which are then deployed by the local Argo CD server. The distributed
  Argo CD applications on the managed clusters are created with a single
  Argo CD `ApplicationSet` resource on the hub cluster.

- The managed cluster is determined by the value of the
  `ocm-managed-cluster` annotation.

- For successful implementation of Pull model, the Argo CD application
  controller must *ignore* Push model application resources with the
  `argocd.argoproj.io/skip-reconcile` annotation in the template section
  of the `ApplicationSet`.

- For Pull model, the *Argo CD Application controller* on the managed
  cluster reconciles to deploy the application.

- The Pull model *Resource sync controller* on the hub cluster queries
  the OpenShift Cluster Manager search V2 component on each managed
  cluster periodically to retrieve the resource list and error messages
  for each Argo CD application.

- The *Aggregation controller* on the hub cluster creates and updates
  the `MulticlusterApplicationSetReport` from across clusters by using
  the data from the Resource sync controller, and the status information
  from `manifestWork`.

- The status of the deployments is gathered back to the hub cluster, but
  not all the detailed information is transmitted. Additional status
  updates are periodically scraped to provide an overview. The status
  feedback is not real-time, and each managed cluster OpenShift GitOps
  operator needs to communicate with the Git repository, which results
  in multiple requests.

### Creating the *ApplicationSet* custom resource

The Argo CD `ApplicationSet` resource is used to deploy applications on
the managed clusters by using the Push or Pull model with a `placement`
resource in the generator field that is used to get a list of managed
clusters.

1.  For the Pull model, set the destination for the application to the
    default local Kubernetes server, as displayed in the following
    example. The application is deployed locally by the application
    controller on the managed cluster.

2.  Add the annotations that are required to override the default Push
    model, as displayed in the following example `ApplicationSet` YAML,
    which uses the Pull model with template annotations:

    ``` yaml
    apiVersion: argoproj.io/v1alpha1
    kind: `ApplicationSet`
    metadata:
      name: guestbook-allclusters-app-set
      namespace: openshift-gitops
    spec:
      generators:
      - clusterDecisionResource:
          configMapRef: ocm-placement-generator
          labelSelector:
            matchLabels:
              cluster.open-cluster-management.io/placement: aws-app-placement
          requeueAfterSeconds: 30
      template:
        metadata:
          annotations:
            apps.open-cluster-management.io/ocm-managed-cluster: '{{name}}'
            apps.open-cluster-management.io/ocm-managed-cluster-app-namespace: openshift-gitops
            argocd.argoproj.io/skip-reconcile: "true" 
          labels:
            apps.open-cluster-management.io/pull-to-ocm-managed-cluster: "true" 
          name: '{{name}}-guestbook-app'
        spec:
          destination:
            namespace: guestbook
            server: https://kubernetes.default.svc
          project: default
          sources: [
          {
            repoURL: https://github.com/argoproj/argocd-example-apps.git
            targetRevision: main
            path: guestbook
             }
          ]
          syncPolicy:
            automated: {}
            syncOptions:
            - CreateNamespace=true
    ```

    - The `apps.open-cluster-management.io/ocm-managed-cluster` is
      needed for the Pull model.

    - The `argocd.argoproj.io/skip-reconcile` is needed to ignore the
      Push model resources.

    - The
      `apps.open-cluster-management.io/pull-to-ocm-managed-cluster: "true"`
      is also needed for the Pull model.

### *MulticlusterApplicationSetReport*

- For the Pull model, the `MulticlusterApplicationSetReport` aggregates
  application status from across your managed clusters.

- The report includes the list of resources and the overall status of
  the application from each managed cluster.

- A separate report resource is created for each Argo CD ApplicationSet
  resource. The report is created in the same namespace as the
  `ApplicationSet`.

- The report includes the following items:

  1.  A list of resources for the Argo CD application

  2.  The overall sync and health status for each Argo CD application

  3.  An error message for each cluster where the overall status is
      `out of sync` or `unhealthy`

  4.  A summary status all the states of your managed clusters

- The *Resource sync controller* and the *Aggregation controller* both
  run every 10 seconds to create the report.

- The two controllers, along with the Propagation controller, run in
  separate containers in the same `multicluster-integrations` pod, as
  shown in the following example output:

      NAMESPACE               NAME                                       READY   STATUS
      open-cluster-management multicluster-integrations-7c46498d9-fqbq4  3/3     Running

The following is an example `MulticlusterApplicationSetReport` YAML file
for the `guestbook` application:

``` yaml
apiVersion: apps.open-cluster-management.io/v1alpha1
kind: MulticlusterApplicationSetReport
metadata:
  labels:
    apps.open-cluster-management.io/hosting-applicationset: openshift-gitops.guestbook-allclusters-app-set
  name: guestbook-allclusters-app-set
  namespace: openshift-gitops
statuses:
  clusterConditions:
  - cluster: cluster1
    conditions:
    - message: 'Failed sync attempt: one or more objects failed to apply, reason: services is forbidden: User "system:serviceaccount:openshift-gitops:openshift-gitops-Argo CD-application-controller" cannot create resource "services" in API group "" in the namespace "guestbook",deployments.apps is forbidden: User <name> cannot create resource "deployments" in API group "apps" in the namespace "guestboo...'
      type: SyncError
    healthStatus: Missing
    syncStatus: OutOfSync
  - cluster: pcluster1
    healthStatus: Progressing
    syncStatus: Synced
  - cluster: pcluster2
    healthStatus: Progressing
    syncStatus: Synced
  summary:
    clusters: "3"
    healthy: "0"
    inProgress: "2"
    notHealthy: "3"
    notSynced: "1"
    synced: "2"
```

**Note:** If a resource fails to deploy, the resource is not included in
the resource list. See error messages for information.

## Managing policy definitions with Red Hat OpenShift GitOps

With the `ArgoCD` resource, you can use Red Hat OpenShift GitOps to
manage policy definitions by granting OpenShift GitOps access to create
policies on the Red Hat Advanced Cluster Management hub cluster.

### Prerequisites

You must log in to your hub cluster.

**Required access:** Cluster administrator

**Deprecated:** `PlacementRule`

### Creating a *ClusterRole* resource for OpenShift GitOps

To create a `ClusterRole` resource for OpenShift GitOps, with access to
create, read, update, and delete policies and placements:

1.  Create a `ClusterRole` from the console. Your `ClusterRole` might
    resemble the following example:

    ``` yaml
    kind: ClusterRole
    apiVersion: rbac.authorization.k8s.io/v1
    metadata:
      name: openshift-gitops-policy-admin
    rules:
      - verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        apiGroups:
          - policy.open-cluster-management.io
        resources:
          - policies
          - configurationpolicies
          - certificatepolicies
          - operatorpolicies
          - policysets
          - placementbindings
      - verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        apiGroups:
          - apps.open-cluster-management.io
        resources:
          - placementrules
      - verbs:
          - get
          - list
          - watch
          - create
          - update
          - patch
          - delete
        apiGroups:
          - cluster.open-cluster-management.io
        resources:
          - placements
          - placements/status
          - placementdecisions
          - placementdecisions/status
    ```

2.  Create a `ClusterRoleBinding` object to grant the OpenShift GitOps
    service account access to the `openshift-gitops-policy-admin`
    `ClusterRole` object. Your `ClusterRoleBinding` might resemble the
    following example:

    ``` yaml
    kind: ClusterRoleBinding
    apiVersion: rbac.authorization.k8s.io/v1
    metadata:
      name: openshift-gitops-policy-admin
    subjects:
      - kind: ServiceAccount
        name: openshift-gitops-argocd-application-controller
        namespace: openshift-gitops
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: openshift-gitops-policy-admin
    ```

    **Notes:** - When a Red Hat Advanced Cluster Management policy
    definition is deployed with OpenShift GitOps, a copy of the policy
    is created in each managed cluster namespace for resolving hub
    template differences. These copies are called replicated policies. -
    To prevent OpenShift GitOps from repeatedly deleting this replicated
    policy or show that the Argo CD `Application` is out of sync, the
    `argocd.argoproj.io/compare-options: IgnoreExtraneous` annotation is
    automatically set on each replicated policy by the Red Hat Advanced
    Cluster Management policy framework.

3.  There are labels and annotations used by Argo CD to track objects.
    For replicated policies to not show up at all in Argo CD, disable
    the Argo CD tracking labels and annotations by setting
    `spec.copyPolicyMetadata` to `false` on the Red Hat Advanced Cluster
    Management policy definition.

### Integrating the Policy Generator with OpenShift GitOps

You can use OpenShift GitOps to generate policies by using the Policy
Generator through GitOps. Since the Policy Generator does not come
preinstalled in the OpenShift GitOps container image, you must complete
customizations.

#### Prerequisites

- You must install OpenShift GitOps on your Red Hat Advanced Cluster
  Management hub cluster.

- You must log in to the hub cluster.

#### Accessing the Policy Generator from OpenShift GitOps

To access the Policy Generator from OpenShift GitOps, you must configure
the Init Container to copy the Policy Generator binary from the Red Hat
Advanced Cluster Management Application Subscription container image.
You must also configure OpenShift GitOps by providing the
`--enable-alpha-plugins` flag when it runs Kustomize.

To create, read, update, and delete policies and placements with the
Policy Generator, grant access to the Policy Generator from OpenShift
GitOps. Complete the following steps:

1.  Edit the OpenShift GitOps `argocd` object with the following
    command:

    ``` bash
    oc -n openshift-gitops edit argocd openshift-gitops
    ```

2.  To update the Policy Generator to a newer version, add the
    `registry.redhat.io/rhacm2/multicluster-operators-subscription-rhel9`
    image used by the Init Container to a newer tag. Replace the
    `<version>` parameter with the latest Red Hat Advanced Cluster
    Management version in your `ArgoCD` resource.

    Your `ArgoCD` resource might resemble the following YAML file:

    ``` yaml
    apiVersion: argoproj.io/v1beta1
    kind: ArgoCD
    metadata:
      name: openshift-gitops
      namespace: openshift-gitops
    spec:
      kustomizeBuildOptions: --enable-alpha-plugins
      repo:
        env:
        - name: KUSTOMIZE_PLUGIN_HOME
          value: /etc/kustomize/plugin
        initContainers:
        - args:
          - -c
          - cp /policy-generator/PolicyGenerator-not-fips-compliant /policy-generator-tmp/PolicyGenerator
          command:
          - /bin/bash
          image: registry.redhat.io/rhacm2/multicluster-operators-subscription-rhel9:v<version>
          name: policy-generator-install
          volumeMounts:
          - mountPath: /policy-generator-tmp
            name: policy-generator
        volumeMounts:
        - mountPath: /etc/kustomize/plugin/policy.open-cluster-management.io/v1/policygenerator
          name: policy-generator
        volumes:
        - emptyDir: {}
          name: policy-generator
    ```

    **Note:** Alternatively, you can create a `ConfigurationPolicy`
    resource that contains the `ArgoCD` manifest and template the
    version to match the version set in the `MulticlusterHub`:

    ``` yaml
    image: '{{ (index (lookup "apps/v1" "Deployment" "open-cluster-management" "multicluster-operators-hub-subscription").spec.template.spec.containers 0).image }}'
    ```

3.  If you want to enable the processing of Helm charts within the
    Kustomize directory before generating policies, set the
    `POLICY_GEN_ENABLE_HELM` environment variable to `"true"` in the
    `spec.repo.env` field:

    ``` yaml
    env:
    - name: POLICY_GEN_ENABLE_HELM
      value: "true"
    ```

4.  To create, read, update, and delete policies and placements, create
    a `ClusterRoleBinding` object to grant the OpenShift GitOps service
    account access to Red Hat Advanced Cluster Management hub cluster.
    Your `ClusterRoleBinding` might resemble the following resource:

    ``` yaml
    kind: ClusterRoleBinding
    apiVersion: rbac.authorization.k8s.io/v1
    metadata:
      name: openshift-gitops-policy-admin
    subjects:
      - kind: ServiceAccount
        name: openshift-gitops-argocd-application-controller
        namespace: openshift-gitops
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: openshift-gitops-policy-admin
    ```

### Configuring policy health checks in OpenShift GitOps

Use OpenShift GitOps with the `ArgoCD` resource to define a custom logic
that sets the health status of a resource based on the resource state by
adding to the `resourceHealthChecks` field. For example, you can define
custom health checks that only report a policy as healthy if your policy
is compliant.

**Important:** To verify that you did not download something malicious
from the Internet, review every policy before you apply it.

To define health checks for your resource kinds complete the following
steps:

1.  Add a health check to your `CertificatePolicy`,
    `ConfigurationPolicy`, `OperatorPolicy`, and `Policy` resources by
    downloading the `argocd-policy-healthchecks.yaml`. Run the following
    command:

    ``` bash
    wget https://raw.githubusercontent.com/open-cluster-management-io/policy-collection/main/stable/CM-Configuration-Management/argocd-policy-healthchecks.yaml
    ```

2.  Apply the `argocd-policy-healthchecks.yaml` policy by going to
    **Governance** \> **Create policy** in the console and pasting the
    content into the YAML editor.

    **Note:** You can add Placement information in the YAML editor to
    determine which clusters have the policy active.

3.  Verify that the health checks work as expected by viewing the
    *Summary* tab of the `ArgoCD` resource. View the health details from
    the Argo CD console.

## Generating a policy to install GitOps Operator

A common use of Red Hat Advanced Cluster Management policies is to
install an Operator on one or more managed Red Hat OpenShift Container
Platform clusters. Continue reading to learn how to generate policies by
using the Policy Generator, and to install the OpenShift Container
Platform GitOps Operator with a generated policy:

### Generating a policy that installs OpenShift Container Platform GitOps

You can generate a policy that installs OpenShift Container Platform
GitOps by using the Policy Generator. The OpenShift Container Platform
GitOps operator offers the *all namespaces* installation mode, which you
can view in the following example. Create a `Subscription` manifest file
called `openshift-gitops-subscription.yaml`, similar to the following
example:

``` yaml
apiVersion: operators.coreos.com/v1alpha1
kind: Subscription
metadata:
  name: openshift-gitops-operator
  namespace: openshift-operators
spec:
  channel: stable
  name: openshift-gitops-operator
  source: redhat-operators
  sourceNamespace: openshift-marketplace
```

To pin to a specific version of the operator, add the following
parameter and value:
`spec.startingCSV: openshift-gitops-operator.v<version>`. Replace
`<version>` with your preferred version.

A `PolicyGenerator` configuration file is required. Use the
configuration file named `policy-generator-config.yaml` to generate a
policy to install OpenShift Container Platform GitOps on all OpenShift
Container Platform managed clusters. See the following example:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: PolicyGenerator
metadata:
  name: install-openshift-gitops
policyDefaults:
  namespace: policies
  placement:
    clusterSelectors:
      vendor: "OpenShift"
  remediationAction: enforce
policies:
  - name: install-openshift-gitops
    manifests:
      - path: openshift-gitops-subscription.yaml
```

The last required file is `kustomization.yaml`, which requires the
following configuration:

``` yaml
generators:
  - policy-generator-config.yaml
```

The generated policy might resemble the following file with
`PlacementRule`(Deprecated):

``` yaml
apiVersion: apps.open-cluster-management.io/v1
kind: PlacementRule
metadata:
  name: placement-install-openshift-gitops
  namespace: policies
spec:
  clusterSelector:
    matchExpressions:
      - key: vendor
        operator: In
        values:
          - OpenShift
---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
  name: binding-install-openshift-gitops
  namespace: policies
placementRef:
  apiGroup: apps.open-cluster-management.io
  kind: PlacementRule
  name: placement-install-openshift-gitops
subjects:
  - apiGroup: policy.open-cluster-management.io
    kind: Policy
    name: install-openshift-gitops
---
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  annotations:
    policy.open-cluster-management.io/categories: CM Configuration Management
    policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
    policy.open-cluster-management.io/standards: NIST SP 800-53
    policy.open-cluster-management.io/description:
  name: install-openshift-gitops
  namespace: policies
spec:
  disabled: false
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name: install-openshift-gitops
        spec:
          object-templates:
            - complianceType: musthave
              objectDefinition:
                apiVersion: operators.coreos.com/v1alpha1
                kind: Subscription
                metadata:
                  name: openshift-gitops-operator
                  namespace: openshift-operators
                spec:
                  channel: stable
                  name: openshift-gitops-operator
                  source: redhat-operators
                  sourceNamespace: openshift-marketplace
          remediationAction: enforce
          severity: low
```

Generated policies from manifests in the OpenShift Container Platform
documentation is supported. Any configuration guidance from the
OpenShift Container Platform documentation can be applied using the
Policy Generator.

### Using policy dependencies with *OperatorGroups*

When you install an operator with an `OperatorGroup` manifest, the
`OperatorGroup` must exist on the cluster before the `Subscription` is
created. Use the policy dependency feature along with the Policy
Generator to ensure that the `OperatorGroup` policy is compliant before
you enforce the `Subscription` policy.

Set up policy dependencies by listing the manifests in the order that
you want. For example, you might want to create the namespace policy
first, create the `OperatorGroup` next, and create the `Subscription`
last.

Enable the `policyDefaults.orderManifests` parameter and disable
`policyDefaults.consolidateManifests` in the Policy Generator
configuration manifest to automatically set up dependencies between the
manifests.

### Additional resources

- See Generating a policy that installs the Compliance Operator.

- See Deploying policies by using GitOps for more details.

- See OpenShift GitOps and the Operator documentation for more details.

- See Adding Operators to a cluster.

- See the Compliance Operator documentation for more details.

- See Using Init Containers to perform tasks before a pod is deployed.

- See Argo CD.

- 

## Creating a customized service account for Argo CD push model

Create a service account on a managed cluster by creating a
`ManagedServiceAccount` resource on the hub cluster. Use the
`ClusterPermission` resource to grant specific permissions to the
service account.

Creating a customzied service account for use with the Argo CD push
model includes the following benefits:

- An Application manager add-on runs on each managed cluster. By
  default, the Argo CD controller uses the service account Application
  manager to push these resources to the managed cluster.

- The Application manager service account has a large set of permissions
  because the application subscription add-on uses the Application
  manager service to deploy applications on the managed cluster. Do not
  use the Application manager service account if you want a limited set
  of permissions.

- You can specify a different service account that you want the Argo CD
  push model to use. When the Argo CD controller pushes resources from
  the centralized hub cluster to the managed cluster, you can use a
  different service account than the default Application manager. By
  using a different service account, you can control the permissions
  that are granted to this service account.

- The service account must exist on the managed cluster. To facilitate
  the creation of the service account with the associated permissions,
  use the `ManagedServiceAccount` resource and the new
  `ClusterPermission` resource on the centralized hub cluster.

After completing all the following procedures, you can grant cluster
permissions to your managed service account. Having the cluster
permissions, your managed service account has the necessary permissions
to deploy your application resources on the managed clusters. Complete
the following procedures:

### Creating a managed service account

The `ManagedServiceAccount` custom resource on the hub provides a
convenient way to create a `ServiceAccount` on the managed clusters.
When a `ManagedServiceAccount` custom resource is created in the
`<managed-cluster>` namespace on the hub cluster, a `ServiceAccount` is
created on the managed cluster.

To create a managed service account, see Enabling ManagedServiceAccount
add-ons.

### Using a managed service account in the *GitOpsCluster* resource

The `GitOpsCluster` resource uses placement to import selected managed
clusters into the Argo CD, including the creation of the Argo CD cluster
secrets which contains information used to access the clusters. By
default, the Argo CD cluster secret uses the application manager service
account to access the managed clusters.

1.  To update the `GitOpsCluster` resource to use the managed service
    account, add the `ManagedServiceAccountRef` property with the name
    of the managed service account.

2.  Save the following sample as a `gitops.yaml` file to create a
    `GitOpsCluster` custom resource:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: argo-acm-importer
      namespace: openshift-gitops
    spec:
      managedServiceAccountRef: <managed-sa-sample>
      argoServer:
        cluster: notused
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters
        namespace: openshift-gitops
    ```

3.  Run `oc apply -f gitops.yaml` to apply the file.

4.  Go to the `openshift-gitops` namespace and verify that there is a
    new Argo CD cluster secret with the name
    `<managed cluster-managed-sa-sample-cluster-secret>`. Run the
    following command:

    ``` bash
    oc get secrets -n openshift-gitops <managed cluster-managed-sa-sample-cluster-secret>
    ```

5.  See the following output to verify:

    ``` bash
    NAME                                        TYPE     DATA   AGE
    <managed cluster-managed-sa-sample-cluster-secret>   Opaque   3      4m2s
    ```

### Creating an Argo CD application

Deploy an Argo CD application from the Argo CD console by using the
pushing model. The Argo CD application is deployed with the managed
service account, `<managed-sa-sample>`.

1.  Log in to the Argo CD console.

2.  Click **Create a new application**.

3.  Choose the cluster URL.

4.  Go to your Argo CD application and verify that it has the given
    permissions, like roles and cluster roles, that you propagated to
    `<managed cluster>`.

### Using policy to create managed service accounts and cluster permissions

When the GitOpsCluster resource is updated with the
`ManagedServiceAccountRef`, each managed cluster in the placement of
this GitOpsCluster needs to have the service account. If you have
several managed clusters, it becomes tedious for you to create the
managed service account and cluster permission for each managed cluster.
You can simply this process by using a policy to create the managed
service account and cluster permission for all your managed clusters

When you apply the `ManagedServiceAccount` and `ClusterPermission`
resources to the hub cluster, the placement of this policy is bound to
the local cluster. Replicate those resources to the managed cluster
namespace for all of the managed clusters in the placement of the
GitOpsCluster resource.

Using a policy to create the `ManagedServiceAccount` and
`ClusterPermission` resources include the following attributes:

- Updating the `ManagedServiceAccount` and `ClusterPermission` object
  templates in the policy results in updates to all of the
  `ManagedServiceAccount` and `ClusterPermission` resources in all of
  the managed clusters.

- Updating directly to the `ManagedServiceAccount` and
  `ClusterPermission` resources becomes reverted back to the original
  state because it is enforced by the policy.

- If the placement decision for the GitOpsCluster placement changes, the
  policy manages the creation and deletion of the resources in the
  managed cluster namespaces.

  1.  To create a policy for a YAML to create a managed service account
      and cluster permission, create a YAML with the following content:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: Policy
  metadata:
    name: policy-gitops
    namespace: openshift-gitops
    annotations:
      policy.open-cluster-management.io/standards: NIST-CSF
      policy.open-cluster-management.io/categories: PR.PT Protective Technology
      policy.open-cluster-management.io/controls: PR.PT-3 Least Functionality
  spec:
    remediationAction: enforce
    disabled: false
    policy-templates:

      - objectDefinition:
          apiVersion: policy.open-cluster-management.io/v1
          kind: ConfigurationPolicy
          metadata:
            name: policy-gitops-sub
          spec:
            pruneObjectBehavior: None
            remediationAction: enforce
            severity: low
            object-templates-raw: |
              {{ range $placedec := (lookup "cluster.open-cluster-management.io/v1beta1" "PlacementDecision" "openshift-gitops" "" "cluster.open-cluster-management.io/placement=aws-app-placement").items }}
              {{ range $clustdec := $placedec.status.decisions }}
              - complianceType: musthave
                objectDefinition:
                  apiVersion: authentication.open-cluster-management.io/v1alpha1
                  kind: ManagedServiceAccount
                  metadata:
                    name: <managed-sa-sample>
                    namespace: {{ $clustdec.clusterName }}
                  spec:
                    rotation: {}
              - complianceType: musthave
                objectDefinition:
                  apiVersion: rbac.open-cluster-management.io/v1alpha1
                  kind: ClusterPermission
                  metadata:
                    name: <clusterpermission-msa-subject-sample>
                    namespace: {{ $clustdec.clusterName }}
                  spec:
                    roles:
                    - namespace: default
                      rules:
                      - apiGroups: ["apps"]
                        resources: ["deployments"]
                        verbs: ["get", "list", "create", "update", "delete"]
                      - apiGroups: [""]
                        resources: ["configmaps", "secrets", "pods", "podtemplates", "persistentvolumeclaims", "persistentvolumes"]
                        verbs: ["get", "update", "list", "create", "delete"]
                      - apiGroups: ["storage.k8s.io"]
                        resources: ["*"]
                        verbs: ["list"]
                    - namespace: mortgage
                      rules:
                      - apiGroups: ["apps"]
                        resources: ["deployments"]
                        verbs: ["get", "list", "create", "update", "delete"]
                      - apiGroups: [""]
                        resources: ["configmaps", "secrets", "pods", "services", "namespace"]
                        verbs: ["get", "update", "list", "create", "delete"]
                    clusterRole:
                      rules:
                      - apiGroups: ["*"]
                        resources: ["*"]
                        verbs: ["get", "list"]
                    roleBindings:
                    - namespace: default
                      roleRef:
                        kind: Role
                      subject:
                        apiGroup: authentication.open-cluster-management.io
                        kind: ManagedServiceAccount
                        name: <managed-sa-sample>
                    - namespace: mortgage
                      roleRef:
                        kind: Role
                      subject:
                        apiGroup: authentication.open-cluster-management.io
                        kind: ManagedServiceAccount
                        name: <managed-sa-sample>
                    clusterRoleBinding:
                      subject:
                        apiGroup: authentication.open-cluster-management.io
                        kind: ManagedServiceAccount
                        name: <managed-sa-sample>
              {{ end }}
              {{ end }}
  ---
  apiVersion: policy.open-cluster-management.io/v1
  kind: PlacementBinding
  metadata:
    name: binding-policy-gitops
    namespace: openshift-gitops
  placementRef:
    name: lc-app-placement
    kind: Placement
    apiGroup: cluster.open-cluster-management.io
  subjects:
    - name: policy-gitops
      kind: Policy
      apiGroup: policy.open-cluster-management.io
  ---
  apiVersion: cluster.open-cluster-management.io/v1beta1
  kind: Placement
  metadata:
    name: lc-app-placement
    namespace: openshift-gitops
  spec:
    numberOfClusters: 1
    predicates:
    - requiredClusterSelector:
        labelSelector:
          matchLabels:
            name: <your-local-cluster-name>
  ```

  1.  Save the YAML file in a file called, `policy.yaml`.

  2.  Run `oc apply -f policy.yaml`.

  3.  In the object template of the policy, it iterates through the
      placement decision of the GitOpsCluster associated placement and
      applies the following `ManagedServiceAccount` and
      `ClusterPermission` templates:

## Managing the Red Hat OpenShift GitOps add-on

The OpenShift GitOps add-on automates the deployment and lifecycle
management of the managed clusters. Based on your architecture and
connectivity requirements, decide if you want to deploy the GitOps
add-on with the `ArgoCD` agent component. Otherwise, you can deploy the
OpenShift GitOps add-on without the `ArgoCD` agent.

**Important:** If you enable the OpenShift GitOps add-on by using the
`GitOpsCluster` custom resource, then the `GitOpsCluster` disables the
`Push Model` for all applications.

When you enable the OpenShift GitOps add-on, you have the following
deployment modes:

- `Basic` mode: Deploys the OpenShift GitOps operator and the `ArgoCD`
  instance on managed clusters through the `GitOpsCluster` custom
  resource.

- `Agent` mode: Includes all basic mode components along with the
  `ArgoCD` agent for enhanced pull-based architecture.

To enable the OpenShift GitOps add-on for your selected managed
clusters, reference your `Placement` and use the `GitOpsCluster` custom
resource as the interface for enabling.

<div class="formalpara">

<div class="title">

Prerequisites

</div>

If you want to enable the OpenShift GitOps add-on with the `ArgoCD`
agent, use the `Agent` mode. See Enabling Red Hat OpenShift GitOps
add-on with ArgoCD agent

</div>

If you want to enable the OpenShift GitOps add-on without the `ArgoCD`
agent, use the `Basic` mode. See Enabling Red Hat OpenShift GitOps
add-on without the ArgoCD agent

### Configuring OpenShift GitOps add-on settings

The OpenShift GitOps add-on supports various configuration options to
customize the deployment according to your requirements.

The OpenShift GitOps add-on supports the following configuration options
in the `gitopsAddon` specification:

- `enabled`: Enable or disable the GitOps add-on. The default is
  `false`.

- `gitOpsOperatorImage`: Custom container image for the GitOps operator.

- `gitOpsImage`: Custom container image for `ArgoCD` components.

- `redisImage`: Custom container image for `Redis`.

- `gitOpsOperatorNamespace`: Namespace where the GitOps operator is
  deployed. The default is `openshift-gitops-operator`.

- `gitOpsNamespace`: Namespace where `ArgoCD` instance is deployed. The
  default is\`openshift-gitops\`.

- `reconcileScope`: Control `ArgoCD` reconciliation scope that includes
  `All-Namespaces` or `Single-Namespace`. The default:
  `Single-Namespaces`.

- `overrideExistingConfigs`: Override existing `AddOnDeploymentConfig`
  values with new values from `GitOpsCluster` specification. Must be set
  to `true` when performing any uninstall operation. The default is
  `false`.

- `argoCDAgent`: `ArgoCD` agent configuration sub-section.

The Argo CD Agent supports the following configuration options in the
`argoCDAgent` specification:

- `enabled`: Enable or disable the agent. The default `false`.

- `propagateHubCA`: Propagate hub certified authority (CA) certificate
  to managed clusters. The default is `true`.

- `image`: Custom agent container image.

- `serverAddress`: Override the `ArgoCD` agent principal server address.

- `serverPort`: Override the `ArgoCD` agent principal server port.

- `mode`: Agent operation mode. The default is `managed`.

To configure the OpenShift GitOps add-on setting, complete the following
steps on your hub cluster:

1.  Customize your container images for the OpenShift GitOps components
    by adding the YAML sample with the `GitOpsCluster`:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: gitops-custom-images
      namespace: openshift-gitops
    spec:
      argoServer:
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters
        namespace: openshift-gitops
      gitopsAddon:
        enabled: true
        gitOpsOperatorImage: "registry.redhat.io/openshift-gitops-1/gitops-operator@sha256:..."
        gitOpsImage: "registry.redhat.io/openshift-gitops-1/argocd@sha256:..."
        redisImage: "registry.redhat.io/rhel8/redis-6@sha256:..."
    ```

2.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f gitopscluster-example.yaml
    ```

3.  Customize the namespaces where you deploy the the OpenShift GitOps
    components by adding the following YAML with the `GitOpsCluster`:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: gitops-custom-namespaces
      namespace: openshift-gitops
    spec:
      argoServer:
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters
        namespace: openshift-gitops
      gitopsAddon:
        enabled: true
        gitOpsOperatorNamespace: openshift-gitops-operator
        gitOpsNamespace: openshift-gitops
    ```

4.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f gitopscluster-example.yaml
    ```

5.  Specify if the `ArgoCD` agent can reconcile application in all
    namespaces by adding the following YAML with the `GitOpsCluster`:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: gitops-reconcile-scope
      namespace: openshift-gitops
    spec:
      argoServer:
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters
        namespace: openshift-gitops
      gitopsAddon:
        enabled: true
        reconcileScope:
    ```

    1.  For the `reconcileScope` field, give it the `All-Namespaces`
        value if you want the `ArgoCD` instance to reconcile
        applications in all namespaces.

    2.  For the `reconcileScope` field, give it the `Single-Namespace`
        value if you want the the `ArgoCD` instance to only reconcile
        applications in its own namespace.

6.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f gitopscluster-example.yaml
    ```

<div class="formalpara">

<div class="title">

Additional resources

</div>

You can skip specific OpenShift GitOps add-on functionalities that you
do not want. See Skipping the OpenShift GitOps add-on enforcement.

</div>

To verify that your OpenShift GitOps add-on works, see Verifying the
{gitops-short) add-on functions.

To verify that your `ArgoCD` agent works, see Verifying the ArgoCD agent
function.

## Enabling Red Hat OpenShift GitOps add-on with *ArgoCD* agent

The `Agent` mode for the pull model enables the OpenShift GitOps add-on
for `Advanced` pull model with the `ArgoCD` agent to get detailed
statuses on the health of your application. Use this `Agent` mode in
environments with network restrictions, enhanced security requirements,
or when you implement a pull model for application delivery. The
advanced pull model is powered by the `ArgoCD` agent and gives you a
fully automated OpenShift GitOps experience.

To enable the OpenShift GitOps add-on with the `ArgoCD` agent, complete
the following sections:

<div>

<div class="title">

Prerequisites

</div>

- Red Hat Advanced Cluster Management hub cluster installed

- Managed clusters registered with Red Hat Advanced Cluster Management

- OpenShift GitOps operator installed on the hub cluster

- A `Placement` resource to select target managed clusters

- `ManagedClusterSet` bound to the target namespace

- OpenShift GitOps operator subscription configured with the `ArgoCD`
  agent environment

- The `ArgoCD` custom resource that are configured for the `Agent` mode

</div>

### Configuring subscriptions and resources

To enable the `ArgoCD` agent, you must configure the OpenShift GitOps
operator subscription and the `ArgoCD` custom resource. To configure the
necessary subscriptions and resources, complete the following steps:

1.  On the hub cluster only, modify the OpenShift GitOps operator
    subscription to include the required environment variables by
    running the following command:

    ``` bash
    oc edit subscription gitops-operator -n openshift-gitops-operator
    ```

2.  Add the following environment variables to the `spec.config.env`
    file by adding the following YAML sample:

    ``` yaml
    spec:
      config:
        env:
        - name: ARGOCD_CLUSTER_CONFIG_NAMESPACES
          value: openshift-gitops
        - name: ARGOCD_PRINCIPAL_TLS_SERVER_ALLOW_GENERATE
          value: "false"
        - name: ARGOCD_PRINCIPAL_REDIS_SERVER_ADDRESS
          value: openshift-gitops-redis:6379
    ```

3.  Replace the existing `ArgoCD` custom resource with the compatible
    `Agent` mode configuration by adding the following YAML sample:

    ``` yaml
    apiVersion: argoproj.io/v1beta1
    kind: ArgoCD
    metadata:
      name: openshift-gitops
      namespace: openshift-gitops
    spec:
      controller:
        enabled: false
      argoCDAgent:
        principal:
          allowedNamespaces:
          - '*'
          auth: mtls:CN=system:open-cluster-management:cluster:([^:]+):addon:gitops-addon:agent:gitops-addon-agent
          enabled: true
    ```

4.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f argocd-example.yaml
    ```

    - **Note:** On the hub cluster only, this configuration disables the
      traditional `ArgoCD` controller and enables the agent principal
      with mutual TLS authentication.

### Enabling *ArgoCD* agent

Create a `GitOpsCluster` resource to manage the `ArgoCD` agent add-on
deployment. The controller controller automatically creates the
following resources for each managed cluster selected by the `Placement`

The `GitOpsCluster` controller performs the following operations:

- Creates and automated PKI management

- Creates `ArgoCD` cluster secrets configured for agent mode

- Deploys the Argo CD Agent on each selected managed cluster

To enable the advanced pull model Argo CD Agent architecture, complete
the following steps:

1.  On your managed cluster, create a `` GitOpsCluster` `` resource with
    the `ArgoCD` agent enabled by adding the following YAML sample:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: gitops-agent-clusters
      namespace: openshift-gitops
    spec:
      argoServer:
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: production-clusters
        namespace: openshift-gitops
      gitopsAddon:
        enabled: true
        argoCDAgent:
          enabled: true
    ```

2.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f gitopscluster-example.yaml
    ```

### Verifying the *ArgoCD* installation

After the `ArgoCD` agent is successfully deployed, verify the advanced
`Pull Model` workflow is completed by creating an application on the hub
cluster and confirming it works on the managed cluster.

To verify the necessary installations and resources for successful
deployment, complete the following steps:

1.  Check the `GitOpsCluster` status for specific `Agent` conditions by
    running the following command:

    ``` bash
    oc get gitopscluster gitops-agent-clusters -n openshift-gitops -o jsonpath='{.status.conditions}' | jq
    ```

2.  Confirm that you see the following condition types in the status:

    - `Ready`: The `GitOpsCluster` is ready and all the components are
      functioning.

    - `PlacementResolved`: The `Placement` reference is resolved and the
      managed clusters are retrieved.

    - `ClustersRegistered`: The managed clusters are successfully
      registered with the `ArgoCD` server.

    - `AddOnDeploymentConfigsReady`: The `AddOnDeploymentConfigs` are
      created for all the managed clusters.

    - `ManagedClusterAddOnsReady`: The `ManagedClusterAddons` creates
      and updates the managed clusters.

    - `AddOnTemplateReady`: The dynamic `AddOnTemplate` created for the
      `ArgoCD` agent mode.

    - `ArgoCDAgentPrereqsReady`: The agent prerequisites are set up.

    - `CertificatesReady`: The TLS certificates are signed.

    - `ManifestWorksApplied`: The CA certificates propagated to managed
      clusters.

3.  Create an `ArgoCD` application resource in the managed cluster
    namespace by adding the following YAML file:

    ``` yaml
    apiVersion: argoproj.io/v1alpha1
    kind: Application
    metadata:
      name: guestbook
      namespace: <managed cluster name>
    spec:
      project: default
      source:
        repoURL: https://github.com/argoproj/argocd-example-apps.git
        targetRevision: HEAD
        path: guestbook
      destination:
        server: https://<principal-external-ip:port>?agentName=<managed cluster name>
        namespace: guestbook
      syncPolicy:
        automated:
          prune: true
          selfHeal: true
    ```

4.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f application-example.yaml
    ```

5.  On the managed cluster, verify that the application resources are
    deployed by running the following command:

    ``` bash
    oc get all -n guestbook
    ```

6.  On the hub cluster, verify the application status is reflected back
    to you by running the following command:

    ``` bash
    oc get application guestbook -n <managed cluster name>
    ```

7.  Confirm that the status shows `Synced` when the application is
    successfully deployed.

<div class="formalpara">

<div class="title">

Additional resources

</div>

Continue setting up the OpenShift GitOps add-on by completing Managing
the Red Hat OpenShift GitOps add-on.

</div>

## Enabling Red Hat OpenShift GitOps add-on without the *ArgoCD* agent

The `Basic` mode for pull model does not include the `ArgoCD` agent, so
the pull model gives you a simpler setup for your hub cluster management
and only gives you the necessary statuses of the health of your hub
clusters. This mode enables the OpenShift GitOps add-on to the managed
clusters that you selected with the `Placement`.

After enabling the add-on, the `Basic` mode deploys the OpenShift GitOps
`ArgoCD` components that are suitable for the cluster workflows.

<div>

<div class="title">

Prerequisites

</div>

- Red Hat Advanced Cluster Management hub cluster installed

- Managed clusters that are registered with Red Hat Advanced Cluster
  Management

- OpenShift GitOps operator that is installed on the hub cluster

- A `Placement` resource that is defined to select target managed
  clusters

- `ManagedClusterSet` that is bound to the target namespace

</div>

To enable a OpenShift GitOps add-on without the `ArgoCD` agent, complete
the following sections:

### Creating a `GitOpsCluster` resource

To enable basic pull model, create a `GitOpsCluster` resource. The
controller automatically creates the following resources for each
managed cluster selected by the `Placement` policy:

- `AddOnDeploymentConfig` resource in the managed cluster namespace

- `ManagedClusterAddOn` resource in the managed cluster namespace

The Red Hat OpenShift GitOps add-on deploys to each selected managed
cluster and installs the following resources:

- OpenShift GitOps operator in the `openshift-gitops-operator` namespace

- ArgoCD instance in the `openshift-gitops` namespace

To create a `GitOpsCluster` resource, complete the following steps:

1.  On your hub cluster, create a `GitOpsCluster` resource to enable the
    Red Hat OpenShift GitOps add-on by adding the following YAML sample:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: gitops-clusters
      namespace: openshift-gitops
    spec:
      argoServer:
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters
        namespace: openshift-gitops
      gitopsAddon:
        enabled: true
    ```

2.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f gitopscluster-example.yaml
    ```

### Verifying the installation

To verify the necessary installations and resources for successful
deployment, complete the following steps:

1.  Verify that the `GitOpsCluster` resource has a status for successful
    deployment by running the following command:

    ``` bash
    oc get gitopscluster gitops-clusters -n openshift-gitops -o yaml
    ```

2.  Verify that the OpenShift GitOps add-on controller is working by
    running the following command:

    ``` bash
    oc get pods -n open-cluster-management-agent-addon
    ```

3.  Verify the OpenShift GitOps operator is working by running the
    following command:

    ``` bash
    oc get pods -n openshift-gitops-operator
    ```

4.  Verify the `` ArgoCD` `` instance is working by running the
    following command:

    ``` bash
    oc get pods -n openshift-gitops
    ```

<div class="formalpara">

<div class="title">

Additional resources

</div>

Continue setting up the OpenShift GitOps add-on by completing Managing
the Red Hat OpenShift GitOps add-on.

</div>

## Skipping the OpenShift GitOps add-on enforcement

The OpenShift GitOps add-on enforces certain resources on the managed
clusters to maintain consistency. You can skip enforcement for specific
resources by adding the `gitops-addon.open-cluster-management.io/skip`
annotation to those specific resources on the managed cluster. Skipping
enforcements helps you when you need to customize the `ArgoCD` custom
resource or other OpenShift GitOps components that the add-on manages.

When a resource on the managed cluster has the skip annotation, the
OpenShift GitOps add-on does not update or manage that resource. The
add-on checks for this annotation before applying any changes, allowing
you to maintain custom configurations that are different from the
default settings for the add-on.

**Note:** When using the skip annotation, ensure that your custom
configurations are compatible with the OpenShift GitOps add-on
requirements. Skipping enforcement means the OpenShift GitOps add-on
does not manage or reconcile these resources, so you are responsible for
maintaining their consistency and correctness.

To skip enforcement for a resource, add the following annotation to the
`ArgoCD` custom resource on the managed cluster:

``` yaml
metadata:
  Annotations:
    gitops-addon.open-cluster-management.io/skip: "true"
```

For managing skip annotations across many managed clusters at scale, use
the Red Hat Advanced Cluster Management `Policy` to apply the annotation
across the fleet.

### Skipping enforcements by customizing the *ArgoCD* custom resource

Customizing the `ArgoCD` custom resource is a common use case to adjust
resource limits, configure specific settings, or enable additional
features.

To skip enforcement by customizing the `ArgoCD` custom resource,
complete the following steps:

1.  On the managed cluster, edit the `ArgoCD` custom resource:

    ``` bash
    oc edit argocd openshift-gitops -n openshift-gitops
    ```

2.  Add the `gitops-addon.open-cluster-management.io/skip` annotation
    and set to `true`, as displayed in the following YAML:

    ``` yaml
    apiVersion: argoproj.io/v1beta1
    kind: ArgoCD
    metadata:
      name: openshift-gitops
      namespace: openshift-gitops
      annotations:
        gitops-addon.open-cluster-management.io/skip: "true"
    ```

3.  Apply the YAML sample by running the following command:

    ``` bash
    oc apply -f argocd-example.yaml
    ```

4.  **Optional**: Override the existing configuration values that the
    `GitOpsCluster` maintains in the `AddOnDeploymentConfig`
    specification by adding the following YAML sample:

    ``` yaml
    apiVersion: apps.open-cluster-management.io/v1beta1
    kind: GitOpsCluster
    metadata:
      name: gitops-override-config
      namespace: openshift-gitops
    spec:
      argoServer:
        argoNamespace: openshift-gitops
      placementRef:
        kind: Placement
        apiVersion: cluster.open-cluster-management.io/v1beta1
        name: all-openshift-clusters
        namespace: openshift-gitops
      gitopsAddon:
        enabled: true
        overrideExistingConfigs: true
        gitOpsImage: "registry.redhat.io/openshift-gitops-1/argocd@sha256:..."
    ```

5.  Apply the YAML sample by running the following command

    ``` bash
    oc apply -f gitopscluster-example.yaml
    ```

<div class="formalpara">

<div class="title">

Additional resources

</div>

If you want to completely uninstall the OpenShift GitOps add-on, see
Uninstalling the OpenShift GitOps add-on.

</div>

## Uninstalling the OpenShift GitOps add-on

To completely uninstall the OpenShift GitOps add-on, including the
operator and the `GitOpsCluster` resource, complete the following steps:

1.  Delete the `GitOpsCluster` resource by running the following
    command:

    ``` bash
    oc delete gitopscluster gitops-clusters -n openshift-gitops
    ```

2.  Delete the `ManagedClusterAddOn` resource by running the following
    command:

    ``` bash
    oc -n <managed_cluster_namespace> delete managedclusteraddon gitops-addon
    ```

3.  Verify that the `ManagedClusterAddOn` resources are removed from
    managed cluster namespaces by running the following command:

    ``` bash
    oc get managedclusteraddon gitops-addon -n <managed-cluster-name>
    ```

## Verifying the {gitops-short) add-on functions

You can verify that your OpenShift GitOps add-on functions work by
completing the following sections:

### Verifying the *GitOpsCluster* status

To check the `GitOpsCluster` status, complete the following steps:

1.  View the `GitOpsCluster` resource status by running the following
    command:

    ``` bash
    oc get gitopscluster <gitopscluster-name> -n openshift-gitops -o yaml
    ```

2.  Check the status conditions for specific failure information by
    running the following command:

    ``` bash
    oc get gitopscluster <gitopscluster-name> -n openshift-gitops -o jsonpath='{.status.conditions}' | jq
    ```

See the following common condition types to check:

- `Ready` : Overall `GitOpsCluster` health

- `PlacementResolved` : `Placement` resource status

- `ClustersRegistered` : Cluster registration status

- `ArgoCDAgentPrereqsReady` : Agent prerequisites, if you have enabled
  the agent

- `CertificatesReady` : TLS certificate status, if you have enabled the
  agent.

- `ManifestWorksApplied` : `ManifestWork` propagation status if you have
  enabled the agent.

### Verifying the OpenShift GitOps add-on controller logs

To check the OpenShift GitOps add-on controller logs, complete the
following steps:

1.  Go to the managed cluster.

2.  Check the OpenShift GitOps add-on controller logs by running the
    following command:

    ``` bash
    oc logs -n open-cluster-management-agent-addon -l app=gitops-addon
    ```

### Verifying the OpenShift GitOps operator

To confirm that the OpenShift GitOps operator works, complete the
following steps:

1.  Verify the operator is working by running the following command:

    ``` bash
    oc get pods -n openshift-gitops-operator
    ```

2.  Check operator logs by running the following command:

    ``` bash
    oc logs -n openshift-gitops-operator -l control-plane=controller-manager
    ```

## Verifying the *ArgoCD* agent function

When you use the `ArgoCD` agent, you need to check that it works. To
check that the `ArgoCD` instance is working, complete the following
steps:

1.  Verify Argo CD components are working by running the following
    command:

    ``` bash
    oc get pods -n openshift-gitops
    ```

2.  Check `ArgoCD` application controller logs by running the following
    command:

    ``` bash
    oc logs -n openshift-gitops -l app.kubernetes.io/name=argocd-application-controller
    ```

If you have enabled the `ArgoCD` agent, check that it is working by
completing the following steps:

1.  Verify the agent is working by running the following command:

    ``` bash
    oc get pods -n openshift-gitops
    ```

2.  Check that the agent logs are working by running the following
    command:

    ``` bash
    oc logs -n openshift-gitops
    ```

3.  Verify that the `ManifestWork` status is set for the certificate
    authorization (CA) propagation by running the following command:

    ``` bash
    oc get manifestwork -n <managed-cluster-name> argocd-agent-ca-propagation -o yaml
    ```

## Implementing progressive rollout strategy by using *ApplicationSet* resource (Technology Preview)

By implementing the progressive rollout strategy to your application in
your cluster fleet for both the push and pull model, you have a Red Hat
OpenShift GitOps-based process that makes changes safely across your
entire cluster fleet. With the rollout strategy, you can orchestrate
staged updates across different clusters. Additionally, you can promote
changes throughout your label defined groups, such as development and
product clusters.

When you use the `ApplicationSet` resource for the progressive rollout
strategy to your application, the `ApplicationSet` controller organizes
the clusters for your application into groups. The controller processes
one group at a time through the Argo CD health cycle, then only makes
the group available if there is a `Healthy` status.

### Enabling the progressive rollout strategy by using the *ApplicationSet* resource

To enable the progressive rollout strategy with your `ApplicationSet`
resource, complete the following steps:

1.  On your hub cluster, update the OpenShift GitOps operator instance
    configuration in the `openshift-gitops` namespace.

2.  Enable the progressive syncs for the `ApplicationSet` resource by
    running the following command:

    ``` bash
    oc -n openshift-gitops patch argocd openshift-gitops --type='merge' -p '{"spec":{"applicationSet":{"extraCommandArgs":["--enable-progressive-syncs"]}}}'
    ```

3.  Restart the `openshift-gitops-applicationset-controller` deployment
    in the `openshift-gitops` namespace.

4.  Apply the updated OpenShift GitOps operator instance configuration
    to create a new rollout by running the following command:

    ``` bash
    oc -n openshift-gitops rollout restart deployment openshift-gitops-applicationset-controller
    ```

### Understanding a sample *ApplicationSet* resource for the progressive rollout strategy

Understand a sample `ApplicationSet` with the Argo CD pull model that
implements the progressive rollout strategy by viewing a strategy
specification. This YAML activates the progressive rollout strategy. By
adding the `strategy` parameter section on your hub cluster, your
clusters can update fully and simultaneously instead of individually.

For example, see how a strategy is defined in the following
`ApplicationSet` resource:

``` yaml
apiVersion: argoproj.io/v1alpha1
kind: ApplicationSet
metadata:
  name: guestbook-allclusters-app-set
  namespace: openshift-gitops
spec:
  generators:
  - clusterDecisionResource:
      configMapRef: ocm-placement-generator
      labelSelector:
        matchLabels:
          cluster.open-cluster-management.io/placement: aws-app-placement
      requeueAfterSeconds: 30
  strategy:
    type: RollingSync
    rollingSync:
      steps:
      - name: dev-stage
        matchExpressions:
        - key: envLabel
          operator: In
          values: [env-dev]
        maxUpdate: 100%
      - name: qa-stage
        matchExpressions:
        - key: envLabel
          operator: In
          values: [env-qa]
        maxUpdate: 100%
      - name: prod-stage
        matchExpressions:
        - key: envLabel
          operator: In
          values: [env-prod]
        maxUpdate: 100%
  template:
    preserveFields: 
    - metadata.labels.envLabel
    metadata:
      annotations:
        apps.open-cluster-management.io/ocm-managed-cluster: '{{name}}'
        apps.open-cluster-management.io/ocm-managed-cluster-app-namespace: openshift-gitops
        argocd.argoproj.io/skip-reconcile: "true"
      labels:
        apps.open-cluster-management.io/pull-to-ocm-managed-cluster: "true"
      name: '{{name}}-guestbook-app'
    spec:
      destination:
        namespace: guestbook
        server: https://kubernetes.default.svc
      project: default
      sources:
      - repoURL: https://github.com/argoproj/argocd-example-apps.git
        targetRevision: main
        path: guestbook
      syncPolicy:
        syncOptions:
        - CreateNamespace=true
```

- Use the `preserveFields` parameter to list the labels that need to be
  ignored by the `ApplicationSet` controller. You can manually apply a
  label that you want, for example, `envLabel=env-qa`. Without this
  field, the `ApplicationSet` controller overwrites or deletes labels
  that are not defined in the template.

### Understanding labels for applications that use the progressive rollout strategy

The rollout strategy is used to process one group of applications at a
time through the Argo CD health cycle. The controller organizes these
groups of applications by matching labels that you set on the
application objects.

Ensure that there is a unique label that specifies the promotion order
that you need for every application, which is using the rollout
strategy. See the following examples:

- For example, you can give your applications a unique label by running
  the following command on your hub cluster:

  ``` bash
  oc -n openshift-gitops label application/cluster1-guestbook-app envLabel=env-dev
  ```

- If you want to specify an application for quality assurance, run the
  following command:

  ``` bash
  oc -n openshift-gitops label application/cluster2-guestbook-app envLabel=env-qa
  ```

- If you want to specify an application group for product, run the
  following command:

``` bash
oc -n openshift-gitops label application/cluster3-guestbook-app envLabel=env-prod
```

### Understanding changes to the Git repository that uses the progressive rollout strategy

To start the progressive rollout strategy for your `ApplicationSet`
resource on your cluster fleet, the Argo CD application checks your Git
repository for committed changes. When there are committed changes, the
progressive rollout strategy begins.

When Argo CD starts the rollout strategy, the `ApplicationSet`
controller detects the applications that have the `OutOfSync` status and
schedules applications for a staged rollout. Based on the labels you use
for your application groups, the `ApplicationSet` controller starts the
first `RollingSync` step with the `env-dev` application group.

From the Argo CD health cycle, you can watch each application group move
from `OutOfSync` to a `Healthy` status. After all your application
groups have a `Healthy` status, the `ApplicationSet` controller syncs
the application group with the `env-qa` label, then the application
group with the `env-prod` label. After your last `env-prod` application
group has a `Healthy` status, the progressive rollout strategy completes
automatically and fully runs its strategy on your cluster fleet.
