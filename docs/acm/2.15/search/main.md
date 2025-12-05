# Search

## Search service

For Red Hat Advanced Cluster Management for Kubernetes, search provides
visibility into your Kubernetes resources across all of your clusters.
Search also indexes the Kubernetes resources and the relationships to
other resources.

### Search components

The search architecture is composed of the following components:

- Component name: search-collector - Description: Watches the Kubernetes
  resources, collects the resource metadata, computes relationships for
  resources across all of your managed clusters, and sends the collected
  data to the search-indexer. The search-collector on your managed
  cluster runs as a pod named, klusterlet-addon-search.

- Component name: search-indexerReceives resource metadata from the
  collectors and writes to PostgreSQL database. The search-indexer also
  watches resources in the hub cluster to keep track of active managed
  clusters. - Metrics: search_indexer_request_duration - Metric type:
  Histogram - Description: Time (seconds) the search indexer takes to
  process a request (from managed cluster).

- Component name: search_indexer_request_size - Metrics: Histogram -
  Metric type: Total changes (add, update, delete) in the search indexer
  request (from managed cluster).

- Component name: search_indexer_request_count - Metrics: Counter -
  Metric type: Total requests received by the search indexer (from
  managed clusters).

- Component name: search_indexer_requests_in_flight - Metrics: Gauge -
  Metric type: Total requests the search indexer is processing at a
  given time.

- Component name: search-apiProvides access to all cluster data in the
  search-indexer through GraphQL and enforces role-based access control
  (RBAC). - Metrics: search_api_requests - Metric type: Histogram -
  Description: Histogram of HTTP requests duration in seconds.

- Component name: search_dbquery_duration_seconds - Metrics: Histogram -
  Metric type: Latency of database requests in seconds.

- Component name: search_api_db_connection_failed_total - Metrics:
  Counter - Metric type: The total number of database connection
  attempts that failed.

- Component name: search-postgres - Description: Stores collected data
  from all managed clusters in an instance of the PostgreSQL database.

Search is configured by default on the hub cluster. When you provision
or manually import a managed cluster, the `klusterlet-addon-search` is
enabled. If you want to disable search on your managed cluster, see
Modifying the klusterlet add-ons settings of your cluster for more
information.

### Search customization and configurations

You can modify the default values in the `search-v2-operator` custom
resource. To view details of the custom resource, run the following
command:

``` bash
oc get search search-v2-operator -o yaml
```

The search operator watches the `search-v2-operator` custom resource,
reconciles the changes and updates active pods. View the following
descriptions of the configurations:

- PostgreSQL database storage:

  When you install Red Hat Advanced Cluster Management, the PostgreSQL
  database is configured to save the PostgreSQL data in an empty
  directory (`emptyDir`) volume. If the empty directory size is limited,
  you can save the PostgreSQL data on a Persistent Volume Claim (PVC) to
  improve search performance. You can select a storageclass from your
  Red Hat Advanced Cluster Management hub cluster to back up your search
  data. For example, if you select the `gp2` storageclass your
  configuration might resemble the following example:

  ``` yaml
  apiVersion: search.open-cluster-management.io/v1alpha1
  kind: Search
  metadata:
    name: search-v2-operator
    namespace: open-cluster-management
    labels:
      cluster.open-cluster-management.io/backup: ""
  spec:
    dbStorage:
      size: 10Gi
      storageClassName: gp2
  ```

  This configuration creates a PVC named `gp2-search` and is mounted to
  the `search-postgres` pod. By default, the storage size is `10Gi`. You
  can modify the storage size. For example, `20Gi` might be sufficient
  for about 200 managed clusters.

- Optimize cost by tuning the pod memory or CPU requirements, replica
  count, and update log levels for any of the four search pods
  (`indexer`, `database`, `queryapi`, or `collector` pod). Update the
  `deployment` section of the `search-v2-operator` custom resource.
  There are four deployments managed by the `search-v2-operator`, which
  can be updated individually. Your `search-v2-operator` custom resource
  might resemble the following file:

  ``` yaml
  apiVersion: search.open-cluster-management.io/v1alpha1
  kind: Search
  metadata:
    name: search-v2-operator
    namespace: open-cluster-management
  spec:
    deployments:
      collector:
        resources: 
          limits:
            cpu: 500m
            memory: 128Mi
          requests:
            cpu: 250m
            memory: 64Mi
      indexer:
        replicaCount: 3
      database: 
          envVar:
            - name: POSTGRESQL_EFFECTIVE_CACHE_SIZE
              value: 1024MB
            - name: POSTGRESQL_SHARED_BUFFERS
              value: 512MB
            - name: WORK_MEM
              value: 128MB
      queryapi:
        arguments: 
        - -v=3
  ```

  - You can apply resources to an `indexer`, `database`, `queryapi`, or
    `collector` pod.

  - You can add multiple environment variables in the `envVar` section
    to specify a value for each variable that you name.

  - You can control the log level verbosity for any of the previous four
    pods by adding the `- -v=3` argument.

    See the following example where memory resources are applied to the
    indexer pod:

    ``` yaml
        indexer:
          resources:
            limits:
              memory: 5Gi
            requests:
              memory: 1Gi
    ```

- You can define the node placement for search pods.

  You can update the `Placement` resource of search pods by using the
  `nodeSelector` parameter, or the `tolerations` parameter. View the
  following example configuration:

  ``` yaml
  spec:
   dbStorage:
    size: 10Gi
   deployments:
    collector: {}
    database: {}
    indexer: {}
    queryapi: {}
   nodeSelector:
    node-role.kubernetes.io/infra: ""
   tolerations:
   - effect: NoSchedule
    key: node-role.kubernetes.io/infra
    operator: Exists
  ```

- Specify your search query by selecting the **Advanced search**
  drop-down button to filter the *Column*, *Operator*, and *Value*
  options or add a search constraint.

### Search operations and data types

Specify your search query by using search operations as conditions.
Characters such as `>, >=, <, <=, !=` are supported. See the following
search operation table:

- Default operation: = - Data type: string, number - Description: This
  is the default operation.

- Default operation: ! or != - Data type: string, number - Description:
  This represents the NOT operation, which means to exclude from the
  search results.

- Default operation: \<, ⇐, \>, \>= - Data type: number

- Default operation: \> - Data type: date - Description: Dates matching
  the last hour, day, week, month, and year.

- Default operation: \* - Data type: string - Description: Partial
  string match.

## Creating search configurable collection

Define which Kubernetes resources are collected from the cluster by
creating a `search-collector-config` config map for each managed cluster
where you want to customize the resources that search collects.

**Required access:** Cluster administrator

Place the config map in the same namespace where the search add-on is
deployed. The default namespace is
`open-cluster-management-agent-addon`.

Complete the following steps:

1.  Run the following command to create the `search-collector-config`
    config map:

    ``` bash
    oc apply -f <your-search-collector-config>.yaml
    ```

2.  List the resources in the allow (`data.AllowedResources`) and deny
    list (`data.DeniedResources`) sections within the config map. Your
    config map might resemble the following YAML file:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
     name: search-collector-config
     namespace: <namespace where search-collector add-on is deployed>
    data:
     AllowedResources: |- 
       - apiGroups:
           - "*"
         resources:
           - services
           - pods
       - apiGroups:
           - admission.k8s.io
           - authentication.k8s.io
         resources:
           - "*"
     DeniedResources: |- 
       - apiGroups:
           - "*"
         resources:
           - secrets
       - apiGroups:
           - admission.k8s.io
         resources:
           - policies
           - iampolicies
           - certificatepolicies
    ```

    - The previous config map example displays `services` and `pods` to
      be collected from all `apiGroups`, while allowing all resources to
      be collected from the `admission.k8s.io` and
      `authentication.k8s.io` `apiGroups`.

    - The config map example also prevents the central collection of
      `secrets` from all `apiGroups` while preventing the collection of
      `policies`, `iampolicies`, and `certificatepolicies` from the
      `apiGroup` `admission.k8s.io`.

      **Note:** If you do not provide a config map, all resources are
      collected by default. If you only provide `AllowedResources`, all
      resources not listed in `AllowedResources` are automatically
      excluded. Resources listed in `AllowedResources` and
      `DeniedResources` at the same time are also excluded.

### Customizing the search console

Customize your search results and limits. Complete the following tasks
to perform the customization:

1.  Customize the search result limit from the OpenShift Container
    Platform console.

    1.  Update the `console-mce-config` in the `multicluster-engine`
        namespace. These settings apply to all users and might affect
        performance. View the following performance parameter
        descriptions:

        - `SAVED_SEARCH_LIMIT` - The maximum amount of saved searches
          for each user. By default, there is a limit of ten saved
          searches for each user. The default value is `10`. To update
          the limit, add the following key value to the `console-config`
          config map: `SAVED_SEARCH_LIMIT: x`.

        - `SEARCH_RESULT_LIMIT` - The maximum amount of search results
          displayed in the console. Default value is `1000`. To remove
          this limit set to `-1`.

        - `SEARCH_AUTOCOMPLETE_LIMIT` - The maximum number of
          suggestions retrieved for the search bar typeahead. Default
          value is `10,000`. To remove this limit set to `-1`.

    2.  Run the following `patch` command from the OpenShift Container
        Platform console to change the search result to 100 items:

    ``` bash
    oc patch configmap console-mce-config -n multicluster-engine --type merge -p '{"data":{"SEARCH_RESULT_LIMIT":"100"}}'
    ```

2.  To add, edit, or remove suggested searches, create a config map
    named `console-search-config` and configure the `suggestedSearches`
    section. Suggested searches that are listed are also displayed from
    the console. It is required to have an `id, name, and searchText`
    for each search object. View the following config map example:

    ``` yaml
    kind: ConfigMap
    apiVersion: v1
    metadata:
      name: console-search-config
      namespace: <acm-namespace> 
    data:
      suggestedSearches: |-
        [
          {
            "id": "search.suggested.workloads.name",
            "name": "Workloads",
            "description": "Show workloads running on your fleet",
            "searchText": "kind:DaemonSet,Deployment,Job,StatefulSet,ReplicaSet"
          },
          {
            "id": "search.suggested.unhealthy.name",
            "name": "Unhealthy pods",
            "description": "Show pods with unhealthy status",
            "searchText": "kind:Pod status:Pending,Error,Failed,Terminating,ImagePullBackOff,CrashLoopBackOff,RunContainerError,ContainerCreating"
          },
          {
            "id": "search.suggested.createdLastHour.name",
            "name": "Created last hour",
            "description": "Show resources created within the last hour",
            "searchText": "created:hour"
          },
          {
            "id": "search.suggested.virtualmachines.name",
            "name": "Virtual Machines",
            "description": "Show virtual machine resources",
            "searchText": "kind:VirtualMachine"
          }
        ]
    ```

    - Add the namespace where search is enabled.

### Querying in the console

You can type any text value in the *Search box* and results include
anything with that value from any property, such as a name or namespace.
Queries that contain an empty space are not supported.

**Required access:** Cluster administrator

For more specific search results, include the property selector in your
search. You can combine related values for the property for a more
precise scope of your search. For example, search for `cluster:dev red`
to receive results that match the string "red" in the `dev` cluster.

Complete the following steps to make queries with search:

1.  Click **Search** in the navigation menu.

2.  Type a word in the *Search box*, then Search finds your resources
    that contain that value.

    - As you search for resources, you receive other resources that are
      related to your original search result, which help you visualize
      how the resources interact with other resources in the system.

    - Search returns and lists each cluster with the resource that you
      search. For resources in the *hub* cluster, the cluster name is
      displayed as *local-cluster*.

    - Your search results are grouped by `kind`, and each resource
      `kind` is grouped in a table.

    - Your search options depend on your cluster objects.

    - You can refine your results with specific labels. Search is
      case-sensitive when you query labels. See the following examples
      that you can select for filtering: `name`, `namespace`, `status`,
      and other resource fields. Auto-complete provides suggestions to
      refine your search. See the following example:

    - Search for a single field, such as `kind:pod` to find all pod
      resources.

    - Search for multiple fields, such as `kind:pod namespace:default`
      to find the pods in the default namespace.

      **Notes:**

      - When you search for more than one property selector with
        multiple values, the search returns either of the values that
        were queried. View the following examples:

      - When you search for `kind:Pod name:a`, any pod named `a` is
        returned.

      - When you search for `kind:Pod name:a,b`, any pod named `a` or
        `b` are returned.

      - Search for `kind:pod status:!Running` to find all pod resources
        where the status is not `Running`.

      - Search for `kind:pod restarts:>1` to find all pods that
        restarted at least twice.

3.  If you want to save your search, click the **Save search** icon.

4.  To download your search results, select the **Export as CSV**
    button.

## Updating klusterlet-addon-search deployments

To collect the Kubernetes objects from the managed clusters, the
`klusterlet-addon-search` pod is run on all the managed clusters where
search is enabled. This deployment is run in the
`open-cluster-management-agent-addon` namespace. A managed cluster with
a high number of resources might require more memory for the
`klusterlet-addon-search` deployment to function.

**Required access:** Cluster administrator

Resource requirements for the `klusterlet-addon-search` pod in a managed
cluster can be specified in the `ManagedClusterAddon` custom resource in
your Red Hat Advanced Cluster Management hub cluster. There is a
namespace for each managed cluster with the managed cluster name.
Complete the following steps:

1.  Edit the `ManagedClusterAddon` custom resource from the namespace
    matching the managed cluster name. Run the following command to
    update the resource requirement in `xyz` managed cluster:

    ``` bash
    oc edit managedclusteraddon search-collector -n xyz
    ```

2.  Append the resource requirements as annotations. View the following
    example:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: ManagedClusterAddOn
    metadata:
      annotations: addon.open-cluster-management.io/search_memory_limit: 2048Mi
      addon.open-cluster-management.io/search_memory_request: 512Mi
    ```

The annotation overrides the resource requirements on the managed
clusters and automatically restarts the pod with new resource
requirements.

**Note:** You can discover all resources defined in your managed cluster
by using the API Explorer in the console. Alternatively, you can
discover all resources by running the following command:
`oc api-resources`
