# Observability service

Observability can help you identify and assess performance problems
without additional tests and support. The Red Hat Advanced Cluster
Management for Kubernetes observability component is a service you can
use to understand the health and utilization of clusters, and workloads
across your fleet. By using the observability service, you are able to
automate and manage the components that are within observability.

Observability service uses existing and widely-adopted observability
tools from the open source community. By default, multicluster
observability operator is enabled during the installation of Red Hat
Advanced Cluster Management. Thanos is deployed within the hub cluster
for long-term metrics storage. The `observability-endpoint-operator` is
automatically deployed to each imported or created managed cluster. This
controller starts a metrics collector that collects the data from Red
Hat OpenShift Container Platform Prometheus, then sends the data to the
Red Hat Advanced Cluster Management hub cluster.

## Observability architecture

The `multiclusterhub-operator` enables the
`multicluster-observability-operator` pod by default. You must configure
the `multicluster-observability-operator` pod.

### Observability open source components

Observability service uses open source observability tools from
community. View the following descriptions of the tools that are apart
of the product Observability service:

Thanos  
A toolkit of components that you can use to perform global querying
across multiple Prometheus instances. For long-term storage of
Prometheus data, persist it in any S3-compatible storage. You can also
compose a highly-available and scalable metrics system.

Prometheus  
A monitoring and alerting tool that you can use to collect metrics from
your application and store these metrics as time-series data. Store all
scraped samples locally, run rules to aggregate and record new time
series from existing data, and generate alerts.

Alertmanager  
A tool to manage and receive alerts from Prometheus. Deduplicate, group,
and route alerts to your integrations such as email, Slack, and
PagerDuty. Configure Alertmanager to silence and inhibit specific
alerts.

### Observability component versions

See the following list to learn which component versions Oberservability
uses in Red Hat Advanced Cluster Management for Kubernetes 2.15:

- Component: Grafana - Version: 12.2.0

- Component: Thanos - Version: 0.39.2

- Component: Prometheus Alertmanager - Version: 0.28.1

- Component: Prometheus - Version: 3.5.0

- Component: Prometheus operator - Version: 0.85.0

- Component: Kube State Metrics - Version: 2.17.0

- Component: Node Exporter - Version: 1.9.1

- Component: Memcached Exporter - Version: 0.15.3

### Observability architecture diagram

The following diagram shows the components of Observability:

The components of the Observability architecture include the following
items:

- The multicluster hub operator, also known as the
  `multiclusterhub-operator` pod, deploys the
  `multicluster-observability-operator` pod. It is the root component
  that deploys resources for the Red Hat Advanced Cluster Management
  Observability service, such as the metrics store on the hub cluster
  and collectors on managed clusters through the generation of
  `ManifestWorks` resources.

- The *Observability add-on controller* is the API server that
  automatically updates the log of the managed cluster.

- The Thanos infrastructure includes the Thanos Compactor, which is
  deployed by the `multicluster-observability-operator` pod. The Thanos
  Compactor ensures that queries are performing well by using the
  retention configuration, and compaction of the data in storage.

  To help identify when the Thanos Compactor is experiencing issues, use
  the four default alerts that are monitoring its health. Read the
  following table of default alerts:

  - Alert: ACMThanosCompactHalted - Severity: critical - Description: An
    alert is sent when the compactor stops.

  - Alert: ACMThanosCompactHighCompactionFailures - Severity: warning -
    Description: An alert is sent when the compaction failure rate is
    greater than 5 percent.

  - Alert: ACMThanosCompactBucketHighOperationFailures - Severity:
    warning - Description: An alert is sent when the bucket operation
    failure rate is greater than 5 percent.

  - Alert: ACMThanosCompactHasNotRun - Severity: warning - Description:
    An alert is sent when the compactor has not uploaded anything in
    last 24 hours.

- The observability component deploys an instance of *Grafana* to enable
  data visualization with dashboards (static) or data exploration. You
  can also design your Grafana dashboard. For more information, see
  *Using Grafana dashboards* in the additional resources section.

- The *Prometheus Alertmanager* enables alerts to be forwarded with
  third-party applications. You can customize the observability service
  by creating custom recording rules or alerting rules.

### Persistent stores used in the observability service

**Important:** Do not use the local storage operator or a storage class
that uses local volumes for persistent storage. You can lose data if the
pod relaunched on a different node after a restart. When this happens,
the pod can no longer access the local storage on the node. Be sure that
you can access the persistent volumes of the `receive` and `rules` pods
to avoid data loss.

When you install Red Hat Advanced Cluster Management the following
persistent volumes (PV) must be created so that Persistent Volume Claims
(PVC) can attach to it automatically. As a reminder, you must define a
storage class in the `MultiClusterObservability` custom resource when
there is no default storage class specified or you want to use a
non-default storage class to host the PVs. It is recommended to use
Block Storage, similar to what Prometheus uses. Also each replica of
`alertmanager`, `thanos-compactor`, `thanos-ruler`,
`thanos-receive-default` and `thanos-store-shard` must have its own PV.
View the following table:

- Component name - Purpose

- alertmanager - Alertmanager stores the nflog data and silenced alerts
  in its storage. nflog is an append-only log of active and resolved
  notifications along with the notified receiver, and a hash digest of
  contents that the notification identified.

- observability-thanos-compactor - The compactor needs local disk space
  to store intermediate data for its processing, as well as bucket state
  cache. The required space depends on the size of the underlying
  blocks. The compactor must have enough space to download all of the
  source blocks, then build the compacted blocks on the disk. On-disk
  data is safe to delete between restarts and should be the first
  attempt to get crash-looping compactors unstuck. However, it is
  recommended to give the compactor persistent disks in order to
  effectively use bucket state cache in between restarts.

- observability-thanos-rule - The thanos ruler evaluates Prometheus
  recording and alerting rules against a chosen query API by issuing
  queries at a fixed interval. Rule results are written back to the disk
  in the Prometheus 2.0 storage format. The amount of hours or days of
  data retained in this stateful set was fixed in the API version
  observability.open-cluster-management.io/v1beta1. It has been exposed
  as an API parameter in
  observability.open-cluster-management.io/v1beta2: RetentionInLocal

- observability-thanos-receive-default - Thanos receiver accepts
  incoming data (Prometheus remote-write requests) and writes these into
  a local instance of the Prometheus TSDB. Periodically (every 2 hours),
  TSDB blocks are uploaded to the object storage for long term storage
  and compaction. The amount of hours or days of data retained in this
  stateful set, which acts a local cache was fixed in API Version
  observability.open-cluster-management.io/v1beta. It has been exposed
  as an API parameter in
  observability.open-cluster-management.io/v1beta2: RetentionInLocal

- observability-thanos-store-shard - It acts primarily as an API gateway
  and therefore does not need a significant amount of local disk space.
  It joins a Thanos cluster on startup and advertises the data it can
  access. It keeps a small amount of information about all remote blocks
  on local disk and keeps it in sync with the bucket. This data is
  generally safe to delete across restarts at the cost of increased
  startup times.

**Note:** The time series historical data is stored in object stores.
Thanos uses object storage as the primary storage for metrics and
metadata related to them. For more details about the object storage and
downsampling, see *Enabling observability service*.

## Observability configuration

When the observability service is enabled, the hub cluster is always
configured to collect and send metrics to the configured Thanos
instance, regardless of whether `disableHubSelfManagement` is set to
`true` (enabled) or set to `false` (disabled). When the hub cluster is
self-managed as a `local-cluster`, the `disableHubSelfManagement`
parameter is set to `false`, which is the default setting. The
`multiclusterhub-operator` enables the
`multicluster-observability-operator` pod by default. You must configure
the `multicluster-observability-operator` pod.

Metrics and alerts for the hub cluster appear in the
`<your-local-cluster-name>` namespace. The local cluster is only
available if `disableHubSelfManagement` is enabled. You can query the
`<your-local-cluster-name>` metrics in the Grafana explorer. Continue
reading to understand what metrics that you can collect with the
observability component, and for information about the observability pod
capacity.

### Metric types

By default, OpenShift Container Platform sends metrics to Red Hat using
the Telemetry service. The `acm_managed_cluster_info` is available with
Red Hat Advanced Cluster Management and is included with telemetry, but
is *not* displayed on the Red Hat Advanced Cluster Management *Observe
environments overview* dashboard.

View the following table of metric types that are supported by the
framework:

- Metric name: acm\_managed\_cluster\_info - Metric type: Gauge -
  Labels/tags: hub\_cluster\_id, managed\_cluster\_id, vendor, cloud,
  version, available, created\_via, core\_worker, socket\_worker -
  Status: Stable

- Metric name: config\_policies\_evaluation\_duration\_seconds\_bucket -
  Metric type: Histogram - Labels/tags: None - Status: Stable. Read
  Governance metric for more details.

- Metric name: config\_policies\_evaluation\_duration\_seconds\_count -
  Metric type: Histogram - Labels/tags: None - Status: Stable. Refer to
  Governance metric for more details.

- Metric name: config\_policies\_evaluation\_duration\_seconds\_sum -
  Metric type: Histogram - Labels/tags: None - Status: Stable. Read
  Governance metric for more details.

- Metric name: policy\_governance\_info - Metric type: Gauge -
  Labels/tags: type, policy, policy\_namespace, cluster\_namespace -
  Status: Stable. Review Governance metric for more details.

- Metric name: cluster\_policy\_governance\_info - Metric type: Gauge -
  Labels/tags: kind, policy, policy\_namespace, severity - Status:
  Stable. Review Governance metric for more details.

- Metric name: policyreport\_info - Metric type: Gauge - Labels/tags:
  managed\_cluster\_id, category, policy, result, severity - Status:
  Stable. Read Managing insight \_PolicyReports\_ for more details.

- Metric name: search\_api\_db\_connection\_failed\_total - Metric type:
  Counter - Labels/tags: None - Status: Stable. See the Search
  components section in the Searching in the console documentation.

- Metric name: search\_api\_dbquery\_duration\_seconds - Metric type:
  Histogram - Labels/tags: None - Status: Stable. See the Search
  components section in the Searching in the console documentation.

- Metric name: search\_api\_requests - Metric type: Histogram -
  Labels/tags: None - Status: Stable. See the Search components section
  in the Searching in the console documentation.

- Metric name: search\_indexer\_request\_count - Metric type: Counter -
  Labels/tags: None - Status: Stable. See the Search components section
  in the Searching in the console documentation.

- Metric name: search\_indexer\_request\_duration - Metric type:
  Histogram - Labels/tags: None - Status: Stable. See the Search
  components section in the Searching in the console documentation.

- Metric name: search\_indexer\_requests\_in\_flight - Metric type:
  Gauge - Labels/tags: None - Status: Stable. See the Search components
  section in the Searching in the console documentation.

- Metric name: search\_indexer\_request\_size - Metric type: Histogram -
  Labels/tags: None - Status: Stable. See the Search components section
  in the Searching in the console documentation.

### Default metrics

To view the default metrics, see the `observability-metrics-allowlist`
by running the following command:

    oc -n open-cluster-management-observability get cm observability-metrics-allowlist -o yaml

**Note:** You cannot change the default metrics in the allowlist.

### Observability pod capacity requests

Observability components require 2701mCPU and 11972Mi memory to install
the observability service. The following table is a list of the pod
capacity requests for five managed clusters with `observability-addons`
enabled:

- Deployment or StatefulSet: observability-alertmanager - Container
  name: alertmanager - CPU (mCPU): 4 - Memory (Mi): 200 - Replicas: 3 -
  Pod total CPU: 12 - Pod total memory: 600

- Deployment or StatefulSet: config-reloader - Container name: 4 - CPU
  (mCPU): 25 - Memory (Mi): 3 - Replicas: 12 - Pod total CPU: 75

- Deployment or StatefulSet: alertmanager-proxy - Container name: 1 -
  CPU (mCPU): 20 - Memory (Mi): 3 - Replicas: 3 - Pod total CPU: 60

- Deployment or StatefulSet: observability-grafana - Container name:
  grafana - CPU (mCPU): 4 - Memory (Mi): 100 - Replicas: 2 - Pod total
  CPU: 8 - Pod total memory: 200

- Deployment or StatefulSet: grafana-dashboard-loader - Container name:
  4 - CPU (mCPU): 50 - Memory (Mi): 2 - Replicas: 8 - Pod total CPU: 100

- Deployment or StatefulSet: observability-observatorium-api - Container
  name: observatorium-api - CPU (mCPU): 20 - Memory (Mi): 128 -
  Replicas: 2 - Pod total CPU: 40 - Pod total memory: 256

- Deployment or StatefulSet: observability-observatorium-operator -
  Container name: observatorium-operator - CPU (mCPU): 100 - Memory
  (Mi): 100 - Replicas: 1 - Pod total CPU: 10 - Pod total memory: 50

- Deployment or StatefulSet: observability-rbac-query-proxy - Container
  name: rbac-query-proxy - CPU (mCPU): 20 - Memory (Mi): 100 - Replicas:
  2 - Pod total CPU: 40 - Pod total memory: 200

- Deployment or StatefulSet: oauth-proxy - Container name: 1 - CPU
  (mCPU): 20 - Memory (Mi): 2 - Replicas: 2 - Pod total CPU: 40

- Deployment or StatefulSet: observability-thanos-compact - Container
  name: thanos-compact - CPU (mCPU): 500 - Memory (Mi): 1024 - Replicas:
  1 - Pod total CPU: 100 - Pod total memory: 512

- Deployment or StatefulSet: observability-thanos-query - Container
  name: thanos-query - CPU (mCPU): 300 - Memory (Mi): 1024 - Replicas:
  2 - Pod total CPU: 600 - Pod total memory: 2048

- Deployment or StatefulSet: observability-thanos-query-frontend -
  Container name: thanos-query-frontend - CPU (mCPU): 100 - Memory (Mi):
  256 - Replicas: 2 - Pod total CPU: 200 - Pod total memory: 512

- Deployment or StatefulSet:
  observability-thanos-query-frontend-memcached - Container name:
  memcached - CPU (mCPU): 45 - Memory (Mi): 128 - Replicas: 3 - Pod
  total CPU: 135 - Pod total memory: 384

- Deployment or StatefulSet: exporter - Container name: 5 - CPU (mCPU):
  50 - Memory (Mi): 3 - Replicas: 15 - Pod total CPU: 150

- Deployment or StatefulSet: observability-thanos-receive-controller -
  Container name: thanos-receive-controller - CPU (mCPU): 4 - Memory
  (Mi): 32 - Replicas: 1 - Pod total CPU: 4 - Pod total memory: 32

- Deployment or StatefulSet: observability-thanos-receive-default -
  Container name: thanos-receive - CPU (mCPU): 300 - Memory (Mi): 512 -
  Replicas: 3 - Pod total CPU: 900 - Pod total memory: 1536

- Deployment or StatefulSet: observability-thanos-rule - Container name:
  thanos-rule - CPU (mCPU): 50 - Memory (Mi): 512 - Replicas: 3 - Pod
  total CPU: 150 - Pod total memory: 1536

- Deployment or StatefulSet: configmap-reloader - Container name: 4 -
  CPU (mCPU): 25 - Memory (Mi): 3 - Replicas: 12 - Pod total CPU: 75

- Deployment or StatefulSet: observability-thanos-store-memcached -
  Container name: memcached - CPU (mCPU): 45 - Memory (Mi): 128 -
  Replicas: 3 - Pod total CPU: 135 - Pod total memory: 384

- Deployment or StatefulSet: exporter - Container name: 5 - CPU (mCPU):
  50 - Memory (Mi): 3 - Replicas: 15 - Pod total CPU: 150

- Deployment or StatefulSet: observability-thanos-store-shard -
  Container name: thanos-store - CPU (mCPU): 100 - Memory (Mi): 1024 -
  Replicas: 3 - Pod total CPU: 300 - Pod total memory: 3072

## Observability advanced configuration

After you enable Observability, you can further customize the
Observability configuration to the specific needs of your environment.
Manage and view cluster fleet data that the Observability service
collects.

**Required access:** Cluster administrator

### Adding custom metrics

To monitor metrics from a remote cluster by using Red Hat Advanced
Cluster Management for Kubernetes, check if the metric is exported as a
Platform or a User workload metric. Use one of the following three
methods to find the metric type:

- Find the metric type in the documentation of the solution you want to
  monitor.

- Find the metric type by contacting the support for your product.

- Find the metric type by checking the annotation that the
  `ServiceMonitor` for the observed resource uses.

  - Platform metrics use
    `operator.prometheus.io/controller-id: openshift-platform-monitoring/prometheus-operator`.

  - User workload metrics use
    `operator.prometheus.io/controller-id: openshift-user-workload-monitoring/prometheus-operator`.

You can also find `ServiceMonitors` in the console by going to
**Observe** &gt; **Targets** and choosing Platform or User from the
**Source** filter in the top right.

**Note:** The **Source** filter provides service monitor or target
information, not a list of metrics.

If the metric is a Platform, continue at Adding Platform metrics. If the
metric is a User workload, continue at Adding user workload metrics.

**Required access:** Cluster administrator

#### Adding Platform metrics

You can monitor Platform metrics by creating a `ConfigMap` on the hub
cluster in the `open-cluster-management-observability` namespace. Use
`observability-metrics-custom-allowlist` as the name. See the following
`ConfigMap` example that you can use to monitor Platform metrics:

    kind: ConfigMap
    apiVersion: v1
    metadata:
      name: observability-metrics-custom-allowlist
      namespace: open-cluster-management-observability
      data:
      metrics_list.yaml: |
        names: 
          - node_memory_MemTotal_bytes
        recording_rules: 
          - record: apiserver_request_duration_seconds:histogram_quantile_90
            expr: histogram_quantile(0.90,sum(rate(apiserver_request_duration_seconds_bucket {job=\"apiserver\", verb!=\"WATCH\"}[5m])) by (verb,le))

- **Optional:** Add the names of the custom metrics you want to collect
  from your managed cluster.

- **Optional:** Add one value for the `expr` and `record` parameter pair
  to define the query expression.

  **Note:** The name for the metrics you collect is the same name that
  you define in your managed cluster `record` parameter. After you run
  the query expression, you get the metric value results. You can use
  one section or both sections, which applies to every cluster with
  monitoring enabled.

If you only want to collect custom metrics from a single managed
cluster, use the following example and apply the config map on your
managed cluster in the `open-cluster-management-addon-observability`
namespace:

    kind: ConfigMap
    apiVersion: v1
    metadata:
      name: observability-metrics-custom-allowlist
      namespace: open-cluster-management-addon-observability
      data:
      metrics_list.yaml: |
        names: 
          - node_memory_MemTotal_bytes
            recording_rules: 
          - record: apiserver_request_duration_seconds:histogram_quantile_90
            expr: histogram_quantile(0.90,sum(rate(apiserver_request_duration_seconds_bucket{job="apiserver", verb!="WATCH"}[5m])) by (verb,le))

- **Optional:** Add the names of the custom metrics you want to collect
  from your managed cluster.

- **Optional:** Enter only one value for the `expr` and `record`
  parameter pair to define the query expression.

  **Note:** The name for the metrics you collect is the same name that
  you define in your managed cluster `record` parameter. After you run
  the query expression, you get the metric value results. You can use
  one section or both sections.

#### Adding User workload metrics

You can monitor User workload metrics by setting the configuration on
the managed cluster in namespace where you want to capture the metric.
The name must be `observability-metrics-custom-allowlist`.

The following example monitors the User workload metric `sample_metrics`
from the namespace `monitored_namespace`. If you create the
configuration in the `open-cluster-management-addon-observability`
namespace instead, the metrics are collected from all the namespaces of
the managed cluster. See the following example:

    kind: ConfigMap
    apiVersion: v1
    metadata:
      name: observability-metrics-custom-allowlist
      namespace: <monitored_namespace> 
    data:
      uwl_metrics_list.yaml:
        names:
          - <sample_metrics> 

- Add the namespace where you want to capture the metric.

- Add the value of the config map data in YAML format. Add list of
  metric names that you want to collect from the `test` namespace to the
  `names` section. After you create the config map, the observability
  collector collects and pushes the metrics from the target namespace to
  the hub cluster.

#### Removing default metrics

If you do not want to collect data for a specific metric from your
managed cluster, remove the metric from the
`observability-metrics-custom-allowlist.yaml` file. When you remove a
metric, the metric data is not collected from your managed clusters.
Complete the following steps to remove a default metric:

1.  Verify that `mco observability` is enabled by using the following
    command:

        oc get mco observability -o yaml

2.  Add the name of the default metric to the `metrics_list.yaml`
    parameter with a hyphen `-` at the start of the metric name. View
    the following metric example:

        -cluster_infrastructure_provider

3.  Create the `observability-metrics-custom-allowlist` config map in
    the `open-cluster-management-observability` namespace with the
    following command:

        oc apply -n open-cluster-management-observability -f observability-metrics-custom-allowlist.yaml

4.  Verify that the observability service is not collecting the specific
    metric from your managed clusters. When you query the metric from
    the Grafana dashboard, the metric is not displayed.

#### Dynamic metrics for single-node OpenShift clusters

Dynamic metrics collection supports automatic metric collection based on
certain conditions. By default, a single-node OpenShift cluster does not
collect pod and container resource metrics. Once a single-node OpenShift
cluster reaches a specific level of resource consumption, the defined
granular metrics are collected dynamically. When the cluster resource
consumption is consistently less than the threshold for a period of
time, granular metric collection stops.

The metrics are collected dynamically based on the conditions on the
managed cluster specified by a collection rule. Because these metrics
are collected dynamically, the following Red Hat Advanced Cluster
Management Grafana dashboards do not display any data. When a collection
rule is activated and the corresponding metrics are collected, the
following panels display data for the duration of the time that the
collection rule is initiated:

- Kubernetes/Compute Resources/Namespace (Pods)

- Kubernetes/Compute Resources/Namespace (Workloads)

- Kubernetes/Compute Resources/Nodes (Pods)

- Kubernetes/Compute Resources/Pod

- Kubernetes/Compute Resources/Workload

A collection rule includes the following conditions:

- A set of metrics to collect dynamically.

- Conditions written as a PromQL expression.

- A time interval for the collection, which must be set to `true`.

- A match expression to select clusters where the collect rule must be
  evaluated.

By default, collection rules are evaluated continuously on managed
clusters every 30 seconds, or at a specific time interval. The lowest
value between the collection interval and time interval takes
precedence.

Once the collection rule condition persists for the duration specified
by the `for` attribute, the collection rule starts and the metrics
specified by the rule are automatically collected on the managed
cluster. Metrics collection stops automatically after the collection
rule condition no longer exists on the managed cluster, at least 15
minutes after it starts.

The collection rules are grouped together as a parameter section named
`collect_rules`, where it can be enabled or disabled as a group. Red Hat
Advanced Cluster Management installation includes the collection rule
group, `SNOResourceUsage` with two default collection rules:
`HighCPUUsage` and `HighMemoryUsage`. The `HighCPUUsage` collection rule
begins when the node CPU usage exceeds 70%.

The `HighMemoryUsage` collection rule begins if the overall memory
utilization of the single-node OpenShift cluster exceeds 70% of the
available node memory. Currently, the previously mentioned thresholds
are fixed and cannot be changed. When a collection rule begins for more
than the interval specified by the `for` attribute, the system
automatically starts collecting the metrics that are specified in the
`dynamic_metrics` section.

View the list of dynamic metrics that from the `collect_rules` section,
in the following YAML file:

    collect_rules:
      - group: SNOResourceUsage
        annotations:
          description: >
            By default, a {sno} cluster does not collect pod and container resource metrics. Once a {sno} cluster
            reaches a level of resource consumption, these granular metrics are collected dynamically.
            When the cluster resource consumption is consistently less than the threshold for a period of time,
            collection of the granular metrics stops.
        selector:
          matchExpressions:
            - key: clusterType
              operator: In
              values: ["{sno}"]
        rules:
        - collect: SNOHighCPUUsage
          annotations:
            description: >
              Collects the dynamic metrics specified if the cluster cpu usage is constantly more than 70% for 2 minutes
          expr: (1 - avg(rate(node_cpu_seconds_total{mode=\"idle\"}[5m]))) * 100 > 70
          for: 2m
          dynamic_metrics:
            names:
              - container_cpu_cfs_periods_total
              - container_cpu_cfs_throttled_periods_total
              - kube_pod_container_resource_limits
              - kube_pod_container_resource_requests
              - namespace_workload_pod:kube_pod_owner:relabel
              - node_namespace_pod_container:container_cpu_usage_seconds_total:sum_irate
              - node_namespace_pod_container:container_cpu_usage_seconds_total:sum_rate
        - collect: SNOHighMemoryUsage
          annotations:
            description: >
              Collects the dynamic metrics specified if the cluster memory usage is constantly more than 70% for 2 minutes
          expr: (1 - sum(:node_memory_MemAvailable_bytes:sum) / sum(kube_node_status_allocatable{resource=\"memory\"})) * 100 > 70
          for: 2m
          dynamic_metrics:
            names:
              - kube_pod_container_resource_limits
              - kube_pod_container_resource_requests
              - namespace_workload_pod:kube_pod_owner:relabel
            matches:
              - __name__="container_memory_cache",container!=""
              - __name__="container_memory_rss",container!=""
              - __name__="container_memory_swap",container!=""
              - __name__="container_memory_working_set_bytes",container!=""

A `collect_rules.group` can be disabled in the `custom-allowlist` as
shown in the following example. When a `collect_rules.group` is
disabled, metrics collection reverts to the previous behavior. These
metrics are collected at regularly, specified intervals:

    collect_rules:
      - group: -SNOResourceUsage

The data is only displayed in Grafana when the rule is initiated.

### Scaling metrics collection (Technology Preview)

To enhance performance in high-scale deployments, you can configure the
`metrics-collector` to collect metrics in parallel with multiple
workers. The default configuration uses a single worker to federate
metrics. By increasing the number of workers in the metric collection
process, you enable internal workers to shard `/federate` endpoint
requests that are made to Prometheus on your managed cluster.

**Required access:** Cluster administrator

#### Increasing and decreasing metrics collection

To increase and decrease metrics collection on your clusters, edit the
`workers` parameter in the `multicluster-observability-operator`
resource. Complete the following steps:

1.  If you want to use the same `workers` value for each of your managed
    clusters, set the value in your `MultiClusterObservability` custom
    resource definition. By default, the value is set to `1`. For
    example, change the `workers` parameter value to `4`. Your YAML file
    might resemble the following resource:

        apiVersion: observability.open-cluster-management.io/v1beta2
        kind: MultiClusterObservability
        metadata:
          name: observability
        spec:
          observabilityAddonSpec:
            enableMetrics: true
            workers: 4

2.  **Optional:** If you want to override the `workers` parameter for
    specific clusters, add the
    `observability.open-cluster-management.io/addon-source: "override"`
    annotation to the `ObservabilityAddOn` specification of your managed
    cluster.

    1.  To revert the override, use the
        `observability.open-cluster-management.io/addon-source: "mco"`
        annotation.

3.  To verify the value of the `workers` parameter, check the values in
    the `MultiClusterObservability` custom resource.

### Configuring proxy settings for observability add-ons

Configure the proxy settings to allow the communications from the
managed cluster to access the hub cluster through a HTTP and HTTPS proxy
server. Typically, add-ons do not need any special configuration to
support HTTP and HTTPS proxy servers between a hub cluster and a managed
cluster. But if you enabled the observability add-on, you must complete
the proxy configuration.

#### Prerequisites

- You have a hub cluster.

- You have enabled the proxy settings between the hub cluster and
  managed cluster.

#### Configuring proxy settings

Complete the following steps to configure the proxy settings for the
observability add-on:

1.  Go to the cluster namespace on your hub cluster.

2.  Create an `AddOnDeploymentConfig` resource with the proxy settings
    by adding a `spec.proxyConfig` parameter. View the following YAML
    example:

        apiVersion: addon.open-cluster-management.io/v1alpha1
        kind: AddOnDeploymentConfig
        metadata:
          name: <addon-deploy-config-name>
          namespace: <managed-cluster-name>
        spec:
          agentInstallNamespace: open-cluster-management-addon-observability
          proxyConfig:
            httpsProxy: "http://<username>:<password>@<ip>:<port>" 
            noProxy: ".cluster.local,.svc,172.30.0.1" 

    - For this field, you can specify either a HTTP proxy or a HTTPS
      proxy.

    - Include the IP address of the `kube-apiserver`.

3.  To get the IP address, run following command on your managed
    cluster:

        oc -n default describe svc kubernetes | grep IP:

4.  Go to the `ManagedClusterAddOn` resource and update it by
    referencing the `AddOnDeploymentConfig` resource that you made. View
    the following YAML example:

        apiVersion: addon.open-cluster-management.io/v1alpha1
        kind: ManagedClusterAddOn
        metadata:
          name: observability-controller
          namespace: <managed-cluster-name>
        spec:
          installNamespace: open-cluster-management-addon-observability
          configs:
          - group: addon.open-cluster-management.io
            resource: addondeploymentconfigs
            name: <addon-deploy-config-name>
            namespace: <managed-cluster-name>

5.  Verify the proxy settings. If you successfully configured the proxy
    settings, the metric collector deployed by the observability add-on
    agent on the managed cluster sends the data to the hub cluster.
    Complete the following steps:

    1.  Go to the hub cluster then the managed cluster on the Grafana
        dashboard.

    2.  View the metrics for the proxy settings.

#### Disabling proxy settings for observability add-ons

If your development needs change, you might need to disable the proxy
setting for the observability add-ons you configured for the hub cluster
and managed cluster. You can disable the proxy settings for the
observability add-on at any time. Complete the following steps:

1.  Go to the `ManagedClusterAddOn` resource.

2.  Remove the referenced `AddOnDeploymentConfig` resource.

### Customizing route certificate

If you want to customize the OpenShift Container Platform route
certification, you must add the routes in the `alt_names` section. To
ensure your OpenShift Container Platform routes are accessible, add the
following information: `alertmanager.apps.<domainname>`,
`observatorium-api.apps.<domainname>`,
`rbac-query-proxy.apps.<domainname>`.

**Note:** Users are responsible for certificate rotations and updates.

#### Customizing certificates for accessing the object store

You can configure secure connections with the observability object store
by creating a `Secret` resource that contains the certificate authority
and configuring the `MultiClusterObservability` custom resource.
Complete the following steps:

1.  To validate the object store connection, create the `Secret` object
    in the file that contains the certificate authority by using the
    following command:

        oc create secret generic <tls_secret_name> --from-file=ca.crt=<path_to_file> -n open-cluster-management-observability

    1.  Alternatively, you can apply the following YAML to create the
        secret:

    <!-- -->

        apiVersion: v1
        kind: Secret
        metadata:
          name: <tls_secret_name>
          namespace: open-cluster-management-observability
        type: Opaque
        data:
          ca.crt: <base64_encoded_ca_certificate>

    **Optional:** If you want to enable mutual TLS, you need to add the
    `public.crt` and `private.key` keys in the previous secret.

2.  Add the TLS secret details to the `metricObjectStorage` section by
    using the following command:

        oc edit mco observability -o yaml

    Your file might resemble the following YAML:

        metricObjectStorage:
          key: thanos.yaml
          name: thanos-object-storage
          tlsSecretName: tls-certs-secret 
          tlsSecretMountPath: /etc/<s3-directory>/certs 

    - The value for `tlsSecretName` is the name of the `Secret` object
      that you previously created.

    - The `/etc/<s3-directory>/certs/` path defined for the
      `tlsSecretMountPath` parameter specifies where the certificates
      are mounted in the Observability components. This path is required
      for the next step.

3.  Update the `thanos.yaml` definition in the `thanos-object-storage`
    secret by adding the `http_config.tls_config` section with the
    certificate details. View the following example. Replace values
    where needed:

        thanos.yaml: |
           type: s3
           config:
             bucket: <bucket-name>
             endpoint: <s3.port>
             insecure: false 
             access_key: <s3-access>
             secret_key: <s3-secret>
             http_config:
               tls_config:
                 ca_file: /etc/<s3-directory>/certs/ca.crt 
                 insecure_skip_verify: false

    - Set the `insecure` parameter to `false` to enable HTTPS.

    - The path for the `ca_file` parameter must match the
      `tlsSecretMountPath` from the `MultiClusterObservability` custom
      resource. The `ca.crt` must match the key in the
      `<tls_secret_name>` `Secret` resource.

      **Optional:** If you want to enable mutual TLS, you need to add
      the `cert_file` and `key_file` keys to the `tls_config` section.
      See the following example. Replace values where needed:

    <!-- -->

         thanos.yaml: |
            type: s3
            config:
              bucket: <bucket-name>
              endpoint: <s3.port>
              insecure: false
              access_key: <s3-access>
              secret_key: <s3-secret>
              http_config:
                tls_config:
                  ca_file: /etc/<s3-directory>/certs/ca.crt 
                  cert_file: /etc/<s3-directory>/certs/public.crt
                  key_file: /etc/<s3-directory>/certs/private.key
                  insecure_skip_verify: false

    - The path for `ca_file`, `cert_file`, and `key_file` must match the
      `tlsSecretMountPath` from the `MultiClusterObservability` custom
      resource. The `ca.crt`, `public.crt`, and `private.crt` must match
      the respective key in the `tls_secret_name>` `Secret` resource.

4.  To verify that you can access the object store, check that the pods
    are deployed. Run the following command:

        oc -n open-cluster-management-observability get pods -l app.kubernetes.io/name=thanos-store

### Creating custom rules

Create custom rules for the observability installation by adding
Prometheus recording rules and alerting rules to the observability
resource.

To precalculate expensive expressions, use the recording rules abilities
with Prometheus to create alert conditions and send notifications based
on how you want to send an alert to an external service. The results are
saved as a new set of time series.

Complete the following steps to create a custom alert rule within the
`thanos-ruler-custom-rules` config map:

1.  Create the following custom alert rule to get a notification for
    when your CPU usage passes your defined value:

        data:
          custom_rules.yaml: |
            groups:
              - name: cluster-health
                rules:
                - alert: ClusterCPUHealth-jb
                  annotations:
                    summary: Notify when CPU utilization on a cluster is greater than the defined utilization limit
                    description: "The cluster has a high CPU usage: {{ $value }} core for {{ $labels.cluster }} {{ $labels.clusterID }}."
                  expr: |
                    max(cluster:cpu_usage_cores:sum) by (clusterID, cluster, prometheus) > 0
                  for: 5s
                  labels:
                    cluster: "{{ $labels.cluster }}"
                    prometheus: "{{ $labels.prometheus }}"
                    severity: critical

    **Notes:**

    - When you update your custom rules, `observability-thanos-rule`
      pods restart automatically.

    - You can create multiple rules in the configuration.

    - The default alert rules are in the
      `observability-thanos-rule-default-rules` config map of the
      `open-cluster-management-observability` namespace.

2.  Create a custom recording rule to get the sum of the container
    memory cache of a pod. See the following example:

        data:
          custom_rules.yaml: |
            groups:
              - name: container-memory
                rules:
                - record: pod:container_memory_cache:sum
                  expr: sum(container_memory_cache{pod!=""}) BY (pod, container)

    **Note:** After you make changes to the config map, the
    configuration automatically reloads. The configuration reloads
    because of the `config-reload` within the
    `observability-thanos-rule` sidecar.

To verify that the alert rules are functioning correctly, go to the
Grafana dashboard, select the **Explore** page, and query `ALERTS`. The
alert is only available in Grafana if you created the alert.

### Updating the *MultiClusterObservability* custom resource replicas from the console

If your workload increases, increase the number of replicas of your
observability pods. Navigate to the console from your hub cluster.
Locate the `MultiClusterObservability` custom resource, and update the
`replicas` parameter value for the component where you want to change
the replicas. Your updated YAML might resemble the following content:

    spec:
       advanced:
          receive:
             replicas: 6

For more information about the parameters within the `mco observability`
custom resource, see the Observability API documentation.

### Increasing and decreasing persistent volumes and persistent volume claims

Increase and decrease the persistent volume and persistent volume claims
to change the amount of storage in your storage class. Complete the
following steps:

1.  To increase the size of the persistent volume, update the
    `MultiClusterObservability` custom resource if the storage class
    support expanding volumes.

2.  To decrease the size of the persistent volumes remove the pods using
    the persistent volumes, delete the persistent volume and recreate
    them. You might experience data loss in the persistent volume.
    Complete the following steps:

    1.  Pause the `MultiClusterObservability` operator by adding the
        annotation `mco-pause: "true"` to the
        `MultiClusterObservability` custom resource.

    2.  Look for the stateful sets or deployments of the desired
        component. Change their replica count to `0`. This initiates a
        shutdown, which involves uploading local data when applicable to
        avoid data loss. For example, the Thanos `Receive` stateful set
        is named `observability-thanos-receive-default` and has three
        replicas by default. Therefore, you are looking for the
        following persistent volume claims:

        - `data-observability-thanos-receive-default-0`

        - `data-observability-thanos-receive-default-1`

        - `data-observability-thanos-receive-default-2`

    3.  Delete the persistent volumes and persistent volume claims used
        by the desired component.

    4.  In the `MultiClusterObservability` custom resource, edit the
        storage size in the configuration of the component to the
        desired amount in the storage size field. Prefix with the name
        of the component.

    5.  Unpause the `MultiClusterObservability` operator by removing the
        previously added annotation.

    6.  To initiate a reconcilation after having the operator paused,
        delete the `multicluster-observability-operator` and
        `observatorium-operator` pods. The pods are recreated and
        reconciled immediately.

3.  Verify that persistent volume and volume claims are updated by
    checking the `MultiClusterObservability` custom resource.

### Customizing the managed cluster Observatorium API and Alertmanager URLs (Technology Preview)

You can customize the Observatorium API and Alertmanager URLs that the
managed cluster uses to communicate with the hub cluster to maintain all
Red Hat Advanced Cluster Management functions when you use a load
balancer or reserve proxy. To customize the URLs, complete the following
steps:

1.  Add your URLs to the `advanced` section of the
    `MultiClusterObservability` `spec`. See the following example:

<!-- -->

    spec:
      advanced:
        customObservabilityHubURL: <yourURL>
        customAlertmanagerHubURL: <yourURL>

**Notes:**

- Only HTTPS URLs are supported. If you do not add `https://` to your
  URL, the scheme is added automatically.

- You can include the standard path for the Remote Write API,
  `/api/metrics/v1/default/api/v1/receive` in the
  `customObservabilityHubURL` `spec`. If you do not include the path,
  the Observability service automatically adds the path at runtime.

- Any intermediate component you use for the custom Observability hub
  cluster URL cannot use TLS termination because the component relies on
  MTLS authentication. The custom Alertmanager hub cluster URL supports
  intermediate component TLS termination by using your own existing
  certificate instructions.

  1.  If you are using a `customObservabilityHubURL`, create a route
      object by using the following template. Replace
      `<intermediate_component_url>` with the intermediate component
      URL:

<!-- -->

    apiVersion: route.openshift.io/v1
    kind: Route
    metadata:
      name: proxy-observatorium-api
      namespace: open-cluster-management-observability
    spec:
      host: <intermediate_component_url>
      port:
        targetPort: public
      tls:
        insecureEdgeTerminationPolicy: None
        termination: passthrough
      to:
        kind: Service
        name: observability-observatorium-api
        weight: 100
      wildcardPolicy: None

1.  If you are using a `customAlertmanagerHubURL`, create a route object
    by using the following template. Replace
    `<intermediate_component_url>` with the intermediate component URL:

<!-- -->

    apiVersion: route.openshift.io/v1
    kind: Route
    metadata:
      name: alertmanager-proxy
      namespace: open-cluster-management-observability
    spec:
      host: <intermediate_component_url>
      path: /api/v2
      port:
        targetPort: oauth-proxy
      tls:
        insecureEdgeTerminationPolicy: Redirect
        termination: reencrypt
      to:
        kind: Service
        name: alertmanager
        weight: 100
      wildcardPolicy: None

### Configuring fine-grain RBAC (Technology Preview)

To restrict metric access to specific namespaces within the cluster, use
fine-grain role-based access control (RBAC). Using fine-grain RBAC, you
can allow application teams to only view the metrics for the namespaces
that you give them permission to access.

You must configure metric access control on the hub cluster for the
users of that hub cluster. On this hub cluster, a `ManagedCluster`
custom resource represents every managed cluster. To configure RBAC and
to select the allowed namespaces, use the rules and action verbs
specified in the `ManagedCluster` custom resources.

For example, you have an application named, `my-awesome-app`, and this
application is on two different managed clusters, `devcluster1` and
`devcluster2`. Both clusters are in the `AwesomeAppNS` namespace. You
have an `admin` user group named, `my-awesome-app-admins`, and you want
to restrict this user group to only have access to metrics from only
these two namespaces on the hub cluster.

To use fine-grain RBAC to restrict the user group access, complete the
following steps:

1.  Define a `ClusterRole` resource with permissions to access metrics.
    Your resource might resemble the following YAML:

        apiVersion: rbac.authorization.k8s.io/v1
        kind: ClusterRole
        metadata:
         name: awesome-app-metrics-role
        rules:
         - apiGroups:
             - "cluster.open-cluster-management.io"
           resources:
             - managedclusters: 
           resourceNames: 
             - devcluster1
             - devcluster2
           verbs: 
             - metrics/AwesomeAppNS

    - Represents the parameter values for the managed clusters.

    - Represents the list of managed clusters.

    - Represents the namespace of the managed clusters.

2.  Define a `ClusterRoleBinding` resource that binds the group,
    `my-awesome-app-admins`, with the `ClusterRole` resource for the
    `awesome-app-metrics-role`. Your resource might resemble the
    following YAML:

        kind: ClusterRoleBinding
        apiVersion: rbac.authorization.k8s.io/v1
        metadata:
         name: awesome-app-metrics-role-binding
        subjects:
         - kind: Group
           apiGroup: rbac.authorization.k8s.io
           name: my-awesome-app-admins
        roleRef:
         apiGroup: rbac.authorization.k8s.io
         kind: ClusterRole
         name: awesome-app-metrics-role

After completing these steps, when the users in the
`my-awesome-app-admins` log into the Grafana console, they have the
following restrictions:

- Users see no data for dashboards that summarize fleet level data.

- Users can only select managed clusters and namespaces specified in the
  `ClusterRole` resource.

To set up different types of user access, define separate `ClusterRoles`
and `ClusterRoleBindings` resources to represent the different managed
clusters in the namespaces.

## Enabling the Observability service

When you enable the Observability service on your hub cluster, the
`multicluster-observability-operator` watches for new managed clusters
and automatically deploys metric and alert collection services to the
managed clusters. You can use metrics and configure Grafana dashboards
to make cluster resource information visible, help you save cost, and
prevent service disruptions.

Monitor the status of your managed clusters with the Observability
component, also known as the `multicluster-observability-operator` pod.

**Required access:** Cluster administrator, the
`open-cluster-management:cluster-manager-admin` role, or S3
administrator.

### Prerequisites

- You must install Red Hat Advanced Cluster Management for Kubernetes.
  See Installing while connected online for more information.

- You must specify the `storageConfig.storageClass` field in the
  `MultiClusterObservability` custom resource if you do not want to use
  the platform default `storageClass`.

- Direct network access to the hub cluster is required. Network access
  to load balancers and proxies are not supported. For more information,
  see Networking.

- You must configure an object store to create a storage solution.

  - **Important:** When you configure your object store, ensure that you
    meet the encryption requirements that are necessary when sensitive
    data is persisted. The Observability service uses Thanos supported,
    stable object stores. You might not be able to share an object store
    bucket by multiple Red Hat Advanced Cluster Management Observability
    installations. Therefore, for each installation, provide a separate
    object store bucket.

  - Red Hat Advanced Cluster Management supports the following cloud
    providers with stable object stores:

    - Amazon Web Services S3 (AWS S3)

    - Red Hat Ceph (S3 compatible API)

    - Google Cloud Storage

    - Azure storage

    - Red Hat OpenShift Data Foundation, formerly known as Red Hat
      OpenShift Container Storage

    - Red Hat OpenShift on IBM Cloud

### Enabling Observability from the command line interface

Enable the Observability service by creating a
`MultiClusterObservability` custom resource instance. Before you enable
Observability, see Observability pod capacity requests for more
information.

**Notes:**

- When Observability is enabled or disabled on OpenShift Container
  Platform managed clusters that are managed by Red Hat Advanced Cluster
  Management, the Observability endpoint operator updates the
  `cluster-monitoring-config` config map by adding additional
  `alertmanager` configuration that automatically restarts the local
  Prometheus.

- The Observability endpoint operator updates the
  `cluster-monitoring-config` config map by adding additional
  `alertmanager` configurations that automatically restart the local
  Prometheus. When you insert the `alertmanager` configuration in the
  OpenShift Container Platform managed cluster, the configuration
  removes the settings that relate to the retention field of the
  Prometheus metrics.

Complete the following steps to enable the Observability service:

1.  Log in to your Red Hat Advanced Cluster Management hub cluster.

2.  Create a namespace for the Observability service with the following
    command:

        oc create namespace open-cluster-management-observability

3.  Generate your pull-secret. If Red Hat Advanced Cluster Management is
    installed in the `open-cluster-management` namespace, run the
    following command:

        DOCKER_CONFIG_JSON=`oc extract secret/multiclusterhub-operator-pull-secret -n open-cluster-management --to=-`

    1.  If the `multiclusterhub-operator-pull-secret` is not defined in
        the namespace, copy the `pull-secret` from the
        `openshift-config` namespace into the
        `open-cluster-management-observability` namespace by running the
        following command:

            DOCKER_CONFIG_JSON=`oc extract secret/pull-secret -n openshift-config --to=-`

    2.  Create the pull-secret in the
        `open-cluster-management-observability` namespace by running the
        following command:

            oc create secret generic multiclusterhub-operator-pull-secret \
                -n open-cluster-management-observability \
                --from-literal=.dockerconfigjson="$DOCKER_CONFIG_JSON" \
                --type=kubernetes.io/dockerconfigjson

    **Important:** If you modify the global pull secret for your cluster
    by using the OpenShift Container Platform documentation, be sure to
    also update the global pull secret in the Observability namespace.
    See Updating the global pull secret for more details.

4.  Create a secret for your object storage for your cloud provider.
    Your secret must contain the credentials to your storage solution.
    For example, run the following command:

        oc create -f thanos-object-storage.yaml -n open-cluster-management-observability

    View the following examples of secrets for the supported object
    stores:

    - For Amazon S3 or S3 compatible, your secret might resemble the
      following file:

          apiVersion: v1
          kind: Secret
          metadata:
            name: thanos-object-storage
            namespace: open-cluster-management-observability
          type: Opaque
          stringData:
            thanos.yaml: |
              type: s3
              config:
                bucket: YOUR_S3_BUCKET
                endpoint: YOUR_S3_ENDPOINT 
                insecure: true
                access_key: YOUR_ACCESS_KEY
                secret_key: YOUR_SECRET_KEY

      - Enter the URL without the protocol. Enter the URL for your
        Amazon S3 endpoint that might resemble the following URL:
        `s3.us-east-1.amazonaws.com`.

        For more details, see the Amazon Simple Storage Service user
        guide.

    - For Google Cloud Platform, your secret might resemble the
      following file:

          apiVersion: v1
          kind: Secret
          metadata:
            name: thanos-object-storage
            namespace: open-cluster-management-observability
          type: Opaque
          stringData:
            thanos.yaml: |
              type: GCS
              config:
                bucket: YOUR_GCS_BUCKET
                service_account: YOUR_SERVICE_ACCOUNT

      For more details, see Google Cloud Storage.

    - For Azure your secret might resemble the following file:

          apiVersion: v1
          kind: Secret
          metadata:
            name: thanos-object-storage
            namespace: open-cluster-management-observability
          type: Opaque
          stringData:
            thanos.yaml: |
              type: AZURE
              config:
                storage_account: YOUR_STORAGE_ACCT
                storage_account_key: YOUR_STORAGE_KEY
                container: YOUR_CONTAINER
                endpoint: blob.core.windows.net 
                max_retries: 0

      - If you use the `msi_resource` path, the endpoint authentication
        is complete by using the system-assigned managed identity. Your
        value must resemble the following endpoint:
        `https://<storage-account-name>.blob.core.windows.net`.

        If you use the `user_assigned_id` path, endpoint authentication
        is complete by using the user-assigned managed identity. When
        you use the `user_assigned_id`, the `msi_resource` endpoint
        default value is `https:<storage_account>.<endpoint>`. For more
        details, see Azure Storage documentation.

        **Note:** If you use Azure as an object storage for a Red Hat
        OpenShift Container Platform cluster, the storage account
        associated with the cluster is not supported. You must create a
        new storage account.

    - For Red Hat OpenShift Data Foundation, your secret might resemble
      the following file:

          apiVersion: v1
          kind: Secret
          metadata:
            name: thanos-object-storage
            namespace: open-cluster-management-observability
          type: Opaque
          stringData:
            thanos.yaml: |
              type: s3
              config:
                bucket: YOUR_RH_DATA_FOUNDATION_BUCKET
                endpoint: YOUR_RH_DATA_FOUNDATION_ENDPOINT 
                insecure: false
                access_key: YOUR_RH_DATA_FOUNDATION_ACCESS_KEY
                secret_key: YOUR_RH_DATA_FOUNDATION_SECRET_KEY

      - Enter the URL without the protocol. Enter the URL for your Red
        Hat OpenShift Data Foundation endpoint that might resemble the
        following URL: `example.redhat.com:443`.

        For more details, see Red Hat OpenShift Data Foundation.

    - For Red Hat OpenShift on IBM (ROKS), your secret might resemble
      the following file:

    <!-- -->

        apiVersion: v1
        kind: Secret
        metadata:
          name: thanos-object-storage
          namespace: open-cluster-management-observability
        type: Opaque
        stringData:
          thanos.yaml: |
            type: s3
            config:
              bucket: YOUR_ROKS_S3_BUCKET
              endpoint: YOUR_ROKS_S3_ENDPOINT 
              insecure: true
              access_key: YOUR_ROKS_ACCESS_KEY
              secret_key: YOUR_ROKS_SECRET_KEY

    - Enter the URL without the protocol. Enter the URL for your Red Hat
      OpenShift Data Foundation endpoint that might resemble the
      following URL: `example.redhat.com:443`.

      For more details, follow the IBM Cloud documentation, Cloud Object
      Storage. Be sure to use the service credentials to connect with
      the object storage. For more details, follow the IBM Cloud
      documentation, Cloud Object Store and Service Credentials.

#### Configuring storage for AWS Security Token Service

For Amazon S3 or S3 compatible storage, you can also use short term,
limited-privilege credentials that are generated with AWS Security Token
Service (AWS STS). Refer to AWS Security Token Service documentation for
more details.

Generating access keys using AWS Security Service require the following
additional steps:

1.  Create an IAM policy that limits access to an S3 bucket.

2.  Create an IAM role with a trust policy to generate JWT tokens for
    OpenShift Container Platform service accounts.

3.  Specify annotations for the Observability service accounts that
    requires access to the S3 bucket. You can find an example of how
    Observability on Red Hat Red Hat OpenShift Service on AWS (ROSA)
    cluster can be configured to work with AWS STS tokens in the *Set
    environment* step. See Red Hat OpenShift Service on AWS (ROSA) for
    more details, along with ROSA with STS explained for an in-depth
    description of the requirements and setup to use STS tokens.

#### Generating access keys using the AWS Security Service

Complete the following steps to generate access keys using the AWS
Security Service:

1.  Set up the AWS environment. Run the following commands:

        export POLICY_VERSION=$(date +"%m-%d-%y")
        export TRUST_POLICY_VERSION=$(date +"%m-%d-%y")
        export CLUSTER_NAME=<my-cluster>
        export S3_BUCKET=$CLUSTER_NAME-acm-observability
        export REGION=us-east-2
        export NAMESPACE=open-cluster-management-observability
        export SA=tbd
        export SCRATCH_DIR=/tmp/scratch
        export OIDC_PROVIDER=$(oc get authentication.config.openshift.io cluster -o json | jq -r .spec.serviceAccountIssuer| sed -e "s/^https:\/\///")
        export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
        export AWS_PAGER=""
        rm -rf $SCRATCH_DIR
        mkdir -p $SCRATCH_DIR

2.  Create an S3 bucket with the following command:

        aws s3 mb s3://$S3_BUCKET

3.  Create a `s3-policy` JSON file for access to your S3 bucket. Run the
    following command:

        {
            "Version": "$POLICY_VERSION",
            "Statement": [
                {
                    "Sid": "Statement",
                    "Effect": "Allow",
                    "Action": [
                        "s3:ListBucket",
                        "s3:GetObject",
                        "s3:DeleteObject",
                        "s3:PutObject",
                        "s3:PutObjectAcl",
                        "s3:CreateBucket",
                        "s3:DeleteBucket"
                    ],
                    "Resource": [
                        "arn:aws:s3:::$S3_BUCKET/*",
                        "arn:aws:s3:::$S3_BUCKET"
                    ]
                }
            ]
         }

4.  Apply the policy with the following command:

        S3_POLICY=$(aws iam create-policy --policy-name $CLUSTER_NAME-acm-obs \
        --policy-document file://$SCRATCH_DIR/s3-policy.json \
        --query 'Policy.Arn' --output text)
        echo $S3_POLICY

5.  Create a `TrustPolicy` JSON file. Run the following command:

        {
         "Version": "$TRUST_POLICY_VERSION",
         "Statement": [
           {
             "Effect": "Allow",
             "Principal": {
               "Federated": "arn:aws:iam::${AWS_ACCOUNT_ID}:oidc-provider/${OIDC_PROVIDER}"
             },
             "Action": "sts:AssumeRoleWithWebIdentity",
             "Condition": {
               "StringEquals": {
                 "${OIDC_PROVIDER}:sub": [
                   "system:serviceaccount:${NAMESPACE}:observability-thanos-query",
                   "system:serviceaccount:${NAMESPACE}:observability-thanos-store-shard",
                   "system:serviceaccount:${NAMESPACE}:observability-thanos-compact",
                   "system:serviceaccount:${NAMESPACE}:observability-thanos-rule",
                   "system:serviceaccount:${NAMESPACE}:observability-thanos-receive"
                 ]
               }
             }
           }
         ]
        }

6.  Create a role for AWS Prometheus and CloudWatch with the following
    command:

        S3_ROLE=$(aws iam create-role \
          --role-name "$CLUSTER_NAME-acm-obs-s3" \
          --assume-role-policy-document file://$SCRATCH_DIR/TrustPolicy.json \
          --query "Role.Arn" --output text)
        echo $S3_ROLE

7.  Attach the policies to the role. Run the following command:

        aws iam attach-role-policy \
          --role-name "$CLUSTER_NAME-acm-obs-s3" \
          --policy-arn $S3_POLICY

    Your secret might resemble the following file. The `config` section
    specifies `signature_version2: false` and does not specify
    `access_key` and `secret_key`:

        apiVersion: v1
        kind: Secret
        metadata:
          name: thanos-object-storage
          namespace: open-cluster-management-observability
        type: Opaque
        stringData:
          thanos.yaml: |
            type: s3
            config:
              bucket: $S3_BUCKET
              endpoint: s3.$REGION.amazonaws.com
              signature_version2: false

8.  Specify the service account annotations in the
    `MultiClusterObservability` custom resource as described in
    *Creating the MultiClusterObservability custom resource* section.

9.  Retrieve the S3 access key and secret key for your cloud providers
    with the following commands. You must decode, edit, and encode your
    `base64` string in the secret:

    1.  To edit and decode the S3 access key for your cloud provider,
        run the following command:

            YOUR_CLOUD_PROVIDER_ACCESS_KEY=$(oc -n open-cluster-management-observability get secret <object-storage-secret> -o jsonpath="{.data.thanos\.yaml}" | base64 --decode | grep access_key | awk '{print $2}')

    2.  To view the access key for your cloud provider, run the
        following command:

            echo $YOUR_CLOUD_PROVIDER_ACCESS_KEY

    3.  To edit and decode the secret key for your cloud provider, run
        the following command:

            YOUR_CLOUD_PROVIDER_SECRET_KEY=$(oc -n open-cluster-management-observability get secret <object-storage-secret> -o jsonpath="{.data.thanos\.yaml}" | base64 --decode | grep secret_key | awk '{print $2}')

    4.  Run the following command to view the secret key for your cloud
        provider:

    <!-- -->

        echo $YOUR_CLOUD_PROVIDER_SECRET_KEY

10. Verify that Observability is enabled by checking the pods for the
    following deployments and stateful sets. You might receive the
    following information:

        observability-thanos-query (deployment)
        observability-thanos-compact (statefulset)
        observability-thanos-receive-default  (statefulset)
        observability-thanos-rule   (statefulset)
        observability-thanos-store-shard-x  (statefulsets)

#### Creating the MultiClusterObservability custom resource

Use the `MultiClusterObservability` custom resource to specify the
persistent volume storage size for various components. You must set the
storage size during the initial creation of the
`MultiClusterObservability` custom resource. When you update the storage
size values post-deployment, changes take effect only if the storage
class supports dynamic volume expansion. For more information, see
Expanding persistent volumes from the Red Hat OpenShift Container
Platform documentation.

Complete the following steps to create the `MultiClusterObservability`
custom resource on your hub cluster:

1.  Create the `MultiClusterObservability` custom resource YAML file
    named `multiclusterobservability_cr.yaml`.

    View the following default YAML file for Observability:

        apiVersion: observability.open-cluster-management.io/v1beta2
        kind: MultiClusterObservability
        metadata:
          name: observability
        spec:
          observabilityAddonSpec: {}
          storageConfig:
            metricObjectStorage:
              name: thanos-object-storage
              key: thanos.yaml

    You might want to modify the value for the `retentionConfig`
    parameter in the `advanced` section. For more information, see
    Thanos Downsampling resolution and retention. Depending on the
    number of managed clusters, you might want to update the amount of
    storage for stateful sets. If your S3 bucket is configured to use
    STS tokens, annotate the service accounts to use STS with S3 role.
    View the following configuration:

        spec:
          advanced:
            compact:
               serviceAccountAnnotations:
                   eks.amazonaws.com/role-arn: $S3_ROLE
            store:
               serviceAccountAnnotations:
                  eks.amazonaws.com/role-arn: $S3_ROLE
            rule:
               serviceAccountAnnotations:
                  eks.amazonaws.com/role-arn: $S3_ROLE
            receive:
               serviceAccountAnnotations:
                  eks.amazonaws.com/role-arn: $S3_ROLE
            query:
               serviceAccountAnnotations:
                  eks.amazonaws.com/role-arn: $S3_ROLE

    See Observability API for more information.

2.  To deploy on infrastructure machine sets, you must set a label for
    your set by updating the `nodeSelector` in the
    `MultiClusterObservability` YAML. Your YAML might resemble the
    following content:

          nodeSelector:
            node-role.kubernetes.io/infra: ""

    For more information, see Creating infrastructure machine sets.

3.  Apply the Observability YAML to your cluster by running the
    following command:

        oc apply -f multiclusterobservability_cr.yaml

    **Note:** By default, if you do not define the
    `storageConfig.storageClass` field in the
    `MultiClusterObservability` custom resource, platform default
    `StorageClass` fields are populated in the `storageConfig` section
    of the `MultiClusterObservability` resource. For example, AWS
    default `storageClass` is set to `gp2`.

4.  Verify default `storageClass` by running the following command:

        oc get storageClass

    See the following example output:

        NAME                PROVISIONER       RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
        gp2-csi             ebs.csi.aws.com   Delete          WaitForFirstConsumer   true                   151m
        gp3-csi (default)   ebs.csi.aws.com   Delete          WaitForFirstConsumer   true                   151m

5.  Validate that the Observability service is enabled and the data is
    populated by launching the Grafana dashboards.

6.  Click the **Grafana link** that is near the console header, from
    either the console *Overview* page or the *Clusters* page.

7.  Access the `multicluster-observability-operator` deployment to
    verify that the `multicluster-observability-operator` pod is being
    deployed by the `multiclusterhub-operator` deployment. Run the
    following command:

        oc get deploy multicluster-observability-operator -n open-cluster-management --show-labels

    You might receive the following results:

        NAME                                  READY   UP-TO-DATE   AVAILABLE   AGE   LABELS
        multicluster-observability-operator   1/1     1            1           35m   installer.name=multiclusterhub,installer.namespace=open-cluster-management

8.  View the `labels` section of the
    `multicluster-observability-operator` deployment for labels that are
    associated with the resource. The `labels` section might contain the
    following details:

         labels:
            installer.name: multiclusterhub
            installer.namespace: open-cluster-management

9.  *Optional:* If you want to exclude specific managed clusters from
    collecting the Observability data, add the following cluster label
    to your clusters: `observability: disabled`.

The Observability service is enabled. After you enable the Observability
service, the following functions are initiated:

- All the alert managers from the managed clusters are forwarded to the
  Red Hat Advanced Cluster Management hub cluster.

- All the managed clusters that are connected to the Red Hat Advanced
  Cluster Management hub cluster are enabled to send alerts back to the
  Red Hat Advanced Cluster Management Observability service. You can
  configure the Red Hat Advanced Cluster Management Alertmanager to take
  care of deduplicating, grouping, and routing the alerts to the correct
  receiver integration such as email, PagerDuty, or OpsGenie. You can
  also handle silencing and inhibition of the alerts.

  **Note:** Alert forwarding to the Red Hat Advanced Cluster Management
  hub cluster feature is only supported by managed clusters on a
  supported OpenShift Container Platform version. After you install Red
  Hat Advanced Cluster Management with Observability enabled, alerts are
  automatically forwarded to the hub cluster. See Forwarding alerts to
  learn more.

### Enabling Observability from the Red Hat OpenShift Container Platform console

Optionally, you can enable Observability from the Red Hat OpenShift
Container Platform console, create a project named
`open-cluster-management-observability`. Complete the following steps:

1.  Create an image pull-secret named,
    `multiclusterhub-operator-pull-secret` in the
    `open-cluster-management-observability` project.

2.  Create your object storage secret named, `thanos-object-storage` in
    the `open-cluster-management-observability` project.

3.  Enter the object storage secret details, then click **Create**. See
    step four of the *Enabling Observability* section to view an example
    of a secret.

4.  Create the `MultiClusterObservability` custom resource instance.
    When you receive the following message, the Observability service is
    enabled successfully from OpenShift Container Platform:
    `Observability components are deployed and running`.

#### Verifying the Thanos version

After Thanos is deployed on your cluster, verify the Thanos version from
the command line interface (CLI).

After you log in to your hub cluster, run the following command in the
Observability pods to receive the Thanos version:

    thanos --version

The Thanos version is displayed.

### Disabling Observability

You can disable Observability, which stops data collection on the Red
Hat Advanced Cluster Management hub cluster.

#### Disabling Observability on all clusters

Disable Observability by removing Observability components on all
managed clusters. Update the `multicluster-observability-operator`
resource by setting `enableMetrics` to `false`. Your updated resource
might resemble the following change:

    spec:
      imagePullPolicy: Always
      imagePullSecret: multiclusterhub-operator-pull-secret
      observabilityAddonSpec: 
        enableMetrics: false 
      workers: 1

- Use the `observabilityAddonSpec` parameter to define the global
  settings for all managed clusters that have the Observability add-on
  enabled.

- Use the `enableMetrics` parameter to indicate that the Observability
  add-on is enabled to push metrics to hub cluster server.

#### Disabling Observability on a single cluster

Disable Observability by removing Observability components on specific
managed clusters. Complete the following steps:

1.  Add the `observability: disabled` label to the
    `managedclusters.cluster.open-cluster-management.io` custom
    resource.

2.  From the Red Hat Advanced Cluster Management console *Clusters*
    page, add the `observability=disabled` label to the specified
    cluster.

    **Note:** When a managed cluster with the Observability component is
    detached, the `metrics-collector` deployments are removed.

### Removing Observability

When you remove the `MultiClusterObservability` custom resource, you are
disabling and uninstalling the Observability service. From the OpenShift
Container Platform console navigation, select **Operators** &gt;
**Installed Operators** &gt; **Advanced Cluster Manager for
Kubernetes**. Remove the `MultiClusterObservability` custom resource.

### Additional resources

- 

- See Using Observability.

- To learn more about customizing the observability service, see
  Observability advanced configuration.

- For more related topics, return to the Observability service.

## Using Observability

Use the Observability service to view the utilization of clusters across
your fleet.

**Required access:** Cluster administrator

### Querying metrics using the Observability API

To access your endpoint by using the mutual TLS, which verifies the
identities of both parties in a network connection, query metrics
through the Red Hat OpenShift Container Platform `rbac-query-proxy`
route with the Observability external API. Complete the following steps
to get your queries for the `rbac-query-proxy` route:

1.  Get the details of the route with the following command:

        oc get route rbac-query-proxy -n open-cluster-management-observability

2.  To access the `rbac-query-proxy` route with your OpenShift Container
    Platform OAuth access token, run the following command to get the
    token. The token must be associated with a user or service account,
    which has permission to get namespaces:

        MY_TOKEN=$(oc whoami --show-token)

3.  To access the `openshift-ingress` route, get the default CA
    certificate and store the content of the `tls.crt` key in a local
    file. Run the following command:

        oc -n openshift-ingress get secret router-certs-default -o jsonpath="{.data.tls\.crt}" | base64 -d > ca.crt

    **Note:** The `router-certs-default` secret does not exist if your
    hub cluster is running on OpenShift Service on AWS. Instead, use the
    CA certificate that `spec.defaultCertificate.name` points to in the
    default ingress controller object. Store the content of the
    `tls.crt` key in a local file. Complete the following steps:

    1.  Get the name of the `spec.defaultCertificate.name` by running
        the following command:

            SECRET_NAME=$(oc get ingresscontroller default -n openshift-ingress-operator -o jsonpath=" {.spec.defaultCertificate.name}")

    2.  Extract the certificate from the secret by running the following
        command:

            oc get secret $SECRET_NAME -n openshift-ingress -o jsonpath=" {.data.tls\.crt}" | base64 -d > ca.crt

4.  To query metrics from the API, run the following command:

        curl --cacert ./ca.crt -H "Authorization: Bearer {TOKEN}" https://{PROXY_ROUTE_URL}/api/v1/query?query={QUERY_EXPRESSION}

    **Note:** The `QUERY_EXPRESSION` is the standard Prometheus query
    expression. For example, query the metrics
    `cluster_infrastructure_provider` by replacing the URL in the
    previous command with the following URL:
    `https://{PROXY_ROUTE_URL}/api/v1/query?query=cluster_infrastructure_provider`.
    For more details, see Querying Prometheus.

5.  If you want to configure custom certificates for the
    `rbac-query-proxy` route, see Replacing certificates for
    rbac-query-proxy route.

#### Exporting metrics to external endpoints

To support the Prometheus Remote-Write specification in real time,
export metrics to external endpoints. Complete the following steps to
export metrics to external endpoints:

1.  Create the Kubernetes secret for an external endpoint with the
    access information of the external endpoint in the
    `open-cluster-management-observability` namespace. View the
    following example secret:

        apiVersion: v1
        kind: Secret
        metadata:
          name: victoriametrics
          namespace: open-cluster-management-observability
        type: Opaque
        stringData:
          ep.yaml: | 
            url: http://victoriametrics:8428/api/v1/write 
            http_client_config: 
              basic_auth: 
                username: test 
                password: test 
              tls_config: 
                secret_name: 
                ca_file_key: 
                cert_file_key: 
                key_file_key: 
                insecure_skip_verify: 

    - The `ep.yaml` parameter is the key of the content and is used in
      the `MultiClusterObservability` custom resource in next step.
      Currently, Observability supports exporting metrics to endpoints
      without any security checks, with basic authentication or with
      `tls` enablement. View the following tables for a full list of
      supported parameters:

    - The `url` parameter is required and the URL for the external
      endpoint. Enter the value as a string.

    - The `http_client_config` parameter is optional and is the advanced
      configuration for the HTTP client.

    - The `basic_auth` parameter is optional and is the HTTP client
      configuration for basic authentication.

    - The `username` parameter is optional and is the user name for
      basic authorization. Enter the value as a string.

    - The `password` is optional and is the password for basic
      authorization. Enter the value as a string.

    - The `tls_config` parameter is optional and is the HTTP client
      configuration for TLS.

    - The `secret_name` parameter is required and is the name of the
      secret that contains certificates. Enter the value as a string.

    - The `ca_file_key` parameter is required and the key of the CA
      certificate in the secret. This parameter is only optional if the
      `insecure_skip_verify` parameter is set to `true`. Enter the value
      as a string.

    - The `cert_file_key` parameter is required and is the key of the
      client certificate in the secret. Enter the value as a string.

    - The `key_file_key` parameter is required and is the key of the
      client key in the secret. Enter the value as a string.

    - The `insecure_skip_verify` parameter is optional and used to skip
      the verification for target certificate. Enter the value as a
      boolean value.

2.  To add a list of external endpoints that you want to export, add the
    `writeStorage` parameter to the `MultiClusterObservability` custom
    resource. View the following example:

        spec:
          storageConfig:
            writeStorage: 
            - key: ep.yaml
              name: victoriametrics

    - Each item contains two attributes: *name* and *key*. *Name* is the
      name of the Kubernetes secret that contains endpoint access
      information, and *key* is the key of the content in the secret. If
      you add more than one item to the list, then the metrics are
      exported to multiple external endpoints.

3.  View the status of metric export after the metrics export is enabled
    by checking the `acm_remote_write_requests_total` metric.

    1.  From the OpenShift Container Platform console of your hub
        cluster, navigate to the *Metrics* page by clicking **Metrics**
        in the *Observe* section.

    2.  Then query the `acm_remote_write_requests_total` metric. The
        value of that metric is the total number of requests with a
        specific response for one external endpoint, on one
        observatorium API instance. The `name` label is the name for the
        external endpoint. The `code` label is the return code of the
        HTTP request for the metrics export.

### Viewing and exploring data by using dashboards

View the data from your managed clusters by accessing Grafana from the
hub cluster. You can query specific alerts and add filters for the
query.

For example, to explore the *cluster\_infrastructure\_provider* alert
from a single-node OpenShift cluster, use the following query
expression: `cluster_infrastructure_provider{clusterType="SNO"}`

**Note:** Do not set the `ObservabilitySpec.resources.CPU.limits`
parameter if Observability is enabled on single node managed clusters.
When you set the CPU limits, it causes the Observability pod to be
counted against the capacity for your managed cluster. See the reference
for *Management Workload Partitioning* in the *Additional resources*
section.

#### Viewing historical data

When you query historical data, manually set your query parameter
options to control how much data is displayed from the dashboard.
Complete the following steps:

1.  From your hub cluster, select the **Grafana link** that is in the
    console header.

2.  Edit your cluster dashboard by selecting **Edit Panel**.

3.  From the Query front-end data source in Grafana, click the *Query*
    tab.

4.  Select `$datasource`.

5.  If you want to see more data, increase the value of the *Step*
    parameter section. If the *Step* parameter section is empty, it is
    automatically calculated.

6.  Find the *Custom query parameters* field and select
    **`max_source_resolution=auto`**.

7.  To verify that the data is displayed, refresh your Grafana page.

Your query data appears from the Grafana dashboard.

#### Viewing Red Hat Advanced Cluster Management dashboards

When you enable the Red Hat Advanced Cluster Management Observability
service, three dashboards become available. View the following dashboard
descriptions:

- *Alert Analysis*: Overview dashboard of the alerts being generated
  within the managed cluster fleet.

- *Clusters by Alert*: Alert dashboard where you can filter by the alert
  name.

- *Alerts by Cluster*: Alert dashboard where you can filter by cluster,
  and view real-time data for alerts that are initiated or pending
  within the cluster environment.

#### Viewing the etcd table

You can also view the etcd table from the hub cluster dashboard in
Grafana to learn the stability of the etcd as a data store. Select the
Grafana link from your hub cluster to view the *etcd* table data, which
is collected from your hub cluster. The *Leader election changes* across
managed clusters are displayed.

#### Viewing the Kubernetes API server dashboard

To see the total number of clusters that are exceeding or meeting the
targeted *service-level objective* (SLO) value for the past seven or
30-day period, offending and non-offending clusters, and API Server
Request Duration, use the following options to view the Kubernetes API
server dashboards:

- View the cluster fleet Kubernetes API service-level overview from the
  hub cluster dashboard in Grafana.

  1.  Navigate to the Grafana dashboard.

  2.  Access the managed dashboard menu by selecting **Kubernetes** &gt;
      **Service-Level Overview** &gt; **API Server**. The *Fleet
      Overview* and *Top Cluster* details are displayed.

- View the Kubernetes API service-level overview table from the hub
  cluster dashboard in Grafana to see the error budget for the past
  seven or 30-day period, the remaining downtime, and trend.

  1.  Navigate to the Grafana dashboard from your hub cluster.

  2.  Access the managed dashboard menu by selecting **Kubernetes** &gt;
      **Service-Level Overview** &gt; **API Server**. The *Fleet
      Overview* and *Top Cluster* details are displayed.

#### Viewing the OpenShift Virtualization dashboard

You can view the Red Hat OpenShift Virtualization dashboard to see
comprehensive insights for each cluster with the OpenShift
Virtualization operator installed. The state of the operator is
displayed, which is determined by active OpenShift Virtualization alerts
and the conditions of the Hyperconverged Cluster Operator. Additionally,
you view the number of running virtual machines and the operator version
for each cluster.

The dashboard also lists alerts affecting the health of the operator and
separately includes all OpenShift Virtualization alerts, even those not
impacting the health of the operator. You can filter the dashboard by
cluster name, operator health alerts, health impact of alerts, and alert
severity.

### Using Grafana dashboards

Use Grafana dashboards to view hub cluster and managed cluster metrics.
The data displayed in the Grafana alerts dashboard relies on `alerts`
metrics, originating from managed clusters. The `alerts` metric does not
affect managed clusters forwarding alerts to Red Hat Advanced Cluster
Management alert manager on the hub cluster. Therefore, the metrics and
alerts have distinct propagation mechanisms and follow separate code
paths.

Even if you see data in the Grafana alerts dashboard, that does not
guarantee that the managed cluster alerts are successfully forwarding to
the Red Hat Advanced Cluster Management hub cluster alert manager. If
the metrics are propagated from the managed clusters, you can view the
data displayed in the Grafana alerts dashboard.

#### Setting up the Grafana developer instance

You can design your Grafana dashboard by creating a `grafana-dev`
instance. Be sure to use the most current `grafana-dev` instance.

Complete the following steps to set up the Grafana developer instance:

1.  Clone the
    open-cluster-management/multicluster-observability-operator/
    repository, so that you are able to run the scripts that are in the
    `tools` folder.

2.  Run the `setup-grafana-dev.sh` to setup your Grafana instance. When
    you run the script the following resources are created:
    `secret/grafana-dev-config`, `deployment.apps/grafana-dev`,
    `service/grafana-dev`, `ingress.extensions/grafana-dev`,
    `persistentvolumeclaim/grafana-dev`:

        ./setup-grafana-dev.sh --deploy
        secret/grafana-dev-config created
        deployment.apps/grafana-dev created
        service/grafana-dev created
        serviceaccount/grafana-dev created
        clusterrolebinding.rbac.authorization.k8s.io/open-cluster-management:grafana-crb-dev created
        route.route.openshift.io/grafana-dev created
        persistentvolumeclaim/grafana-dev created
        oauthclient.oauth.openshift.io/grafana-proxy-client-dev created
        deployment.apps/grafana-dev patched
        service/grafana-dev patched
        route.route.openshift.io/grafana-dev patched
        oauthclient.oauth.openshift.io/grafana-proxy-client-dev patched
        clusterrolebinding.rbac.authorization.k8s.io/open-cluster-management:grafana-crb-dev patched

3.  Switch the user role to Grafana administrator with the
    `switch-to-grafana-admin.sh` script.

    1.  Select the Grafana URL,
        `https:grafana-dev-open-cluster-management-observability.{OPENSHIFT_INGRESS_DOMAIN}`,
        and log in.

    2.  Then run the following command to add the switched user as
        Grafana administrator. For example, after you log in using
        `kubeadmin`, run following command:

            ./switch-to-grafana-admin.sh kube:admin
            User <kube:admin> switched to be grafana admin

The Grafana developer instance is set up.

##### Verifying Grafana version

Verify the Grafana version from the command line interface (CLI) or from
the Grafana user interface.

After you log in to your hub cluster, access the `observabilty-grafana`
pod terminal. Run the following command:

    grafana-cli

The Grafana version that is currently deployed within the cluster
environment is displayed.

Alternatively, you can navigate to the *Manage* tab in the Grafana
dashboard. Scroll to the end of the page, where the version is listed.

#### Designing your Grafana dashboard

After you set up the Grafana instance, you can design the dashboard.
Complete the following steps to refresh the Grafana console and design
your dashboard:

1.  From the Grafana console, create a dashboard by selecting the
    **Create** icon from the navigation panel. Select **Dashboard**, and
    then click **Add new panel**.

2.  From the *New Dashboard/Edit Panel* view, navigate to the *Query*
    tab.

3.  Configure your query by selecting `Observatorium` from the data
    source selector and enter a PromQL query.

4.  From the Grafana dashboard header, click the **Save** icon that is
    in the dashboard header.

5.  Add a descriptive name and click **Save**.

##### Designing your Grafana dashboard with a ConfigMap

Design your Grafana dashboard with a ConfigMap. You can use the
`generate-dashboard-configmap-yaml.sh` script to generate the dashboard
ConfigMap, and to save the ConfigMap locally:

    ./generate-dashboard-configmap-yaml.sh "Your Dashboard Name"
    Save dashboard <your-dashboard-name> to ./your-dashboard-name.yaml

If you do not have permissions to run the previously mentioned script,
complete the following steps:

1.  Select a dashboard and click the **Dashboard settings** icon.

2.  Click the **JSON Model** icon from the navigation panel.

3.  Copy the dashboard JSON data and paste it in the `data` section.

4.  Modify the `name` and replace `$your-dashboard-name`. Enter a
    universally unique identifier (UUID) in the `uid` field in
    `data.$your-dashboard-name.json.$$your_dashboard_json`. You can use
    a program such as *uuidegen* to create a UUID. Your ConfigMap might
    resemble the following file:

        kind: ConfigMap
        apiVersion: v1
        metadata:
          name: $your-dashboard-name
          namespace: open-cluster-management-observability
          labels:
            grafana-custom-dashboard: "true"
        data:
          $your-dashboard-name.json: |-
            $your_dashboard_json

    **Notes:**

    - If your dashboard is created within the `grafana-dev` instance,
      you can take the name of the dashboard and pass it as an argument
      in the script. For example, a dashboard named *Demo Dashboard* is
      created in the `grafana-dev` instance. From the CLI, you can run
      the following script:

          ./generate-dashboard-configmap-yaml.sh "Demo Dashboard"

      After running the script, you might receive the following message:

          Save dashboard <demo-dashboard> to ./demo-dashboard.yaml

    - If your dashboard is not in the *General* folder, you can specify
      the folder name in the `annotations` section of this ConfigMap:

          annotations:
            observability.open-cluster-management.io/dashboard-folder: Custom

      After you complete your updates for the ConfigMap, you can install
      it to import the dashboard to the Grafana instance.

Verify that the YAML file is created by applying the YAML from the CLI
or OpenShift Container Platform console. A ConfigMap within the
`open-cluster-management-observability` namespace is created. Run the
following command from the CLI:

    oc apply -f demo-dashboard.yaml

From the OpenShift Container Platform console, create the ConfigMap
using the `demo-dashboard.yaml` file. The dashboard is located in the
*Custom* folder.

#### Uninstalling the Grafana developer instance

When you uninstall the instance, the related resources are also deleted.
Run the following command:

    ./setup-grafana-dev.sh --clean
    secret "grafana-dev-config" deleted
    deployment.apps "grafana-dev" deleted
    serviceaccount "grafana-dev" deleted
    route.route.openshift.io "grafana-dev" deleted
    persistentvolumeclaim "grafana-dev" deleted
    oauthclient.oauth.openshift.io "grafana-proxy-client-dev" deleted
    clusterrolebinding.rbac.authorization.k8s.io "open-cluster-management:grafana-crb-dev" deleted

### Using managed cluster labels in Grafana

Enable managed cluster labels to use them with Grafana dashboards. When
observability is enabled in the hub cluster, the
`observability-managed-cluster-label-allowlist` ConfigMap is created in
the `open-cluster-management-observability` namespace. The ConfigMap
contains a list of managed cluster labels maintained by the
`observabilty-rbac-query-proxy` pod, to populate a list of label names
to filter from within the *ACM - Cluster Overview* Grafana dashboard. By
default, observability ignores a subset of labels in the
`observability-managed-cluster-label-allowlist` ConfigMap.

When a cluster is imported into the managed cluster fleet or modified,
the `observability-rbac-query-proxy` pod watches for any changes in
reference to the managed cluster labels and automatically updates the
`observability-managed-cluster-label-allowlist` ConfigMap to reflect the
changes. The ConfigMap contains only unique label names, which are
either included in the `ignore_labels` or `labels` list. Your
`observability-managed-cluster-label-allowlist` ConfigMap might resemble
the following YAML file:

    data:
      managed_cluster.yaml: |
        ignore_labels: 
          - clusterID
          - cluster.open-cluster-management.io/clusterset
          - feature.open-cluster-management.io/addon-application-manager
          - feature.open-cluster-management.io/addon-cert-policy-controller
          - feature.open-cluster-management.io/addon-cluster-proxy
          - feature.open-cluster-management.io/addon-config-policy-controller
          - feature.open-cluster-management.io/addon-governance-policy-framework
          - feature.open-cluster-management.io/addon-observability-controller
          - feature.open-cluster-management.io/addon-search-collector
          - feature.open-cluster-management.io/addon-work-manager
          - installer.name
          - installer.namespace
          - local-cluster
          - name
        labels: 
          - cloud
          - vendor

\+ &lt;1&gt; Any label that is listed in the `ignore_labels` keylist of
the ConfigMap is removed from the drop-down filter on the *ACM -
Clusters Overview* Grafana dashboard. &lt;2&gt; The labels that are
enabled are displayed in the drop-down filter on the *ACM - Clusters
Overview* Grafana dashboard. The values are from the
`acm_managed_cluster_labels` metric, depending on the `label` key value
that is selected.

#### Adding managed cluster labels

When you add a managed cluster label to the
`observability-managed-cluster-label-allowlist` ConfigMap, the label
becomes available as a filter option in Grafana. Add a unique label to
the hub cluster, or managed cluster object that is associated with the
managed cluster fleet. For example, if you add the label,
`department=finance` to a managed cluster, the ConfigMap is updated and
might resemble the following changes:

    data:
      managed_cluster.yaml: |
        ignore_labels:
          - clusterID
          - cluster.open-cluster-management.io/clusterset
          - feature.open-cluster-management.io/addon-application-manager
          - feature.open-cluster-management.io/addon-cert-policy-controller
          - feature.open-cluster-management.io/addon-cluster-proxy
          - feature.open-cluster-management.io/addon-config-policy-controller
          - feature.open-cluster-management.io/addon-governance-policy-framework
          - feature.open-cluster-management.io/addon-observability-controller
          - feature.open-cluster-management.io/addon-search-collector
          - feature.open-cluster-management.io/addon-work-manager
          - installer.name
          - installer.namespace
          - local-cluster
          - name
        labels:
          - cloud
          - department
          - vendor

#### Enabling managed cluster labels

Enable a managed cluster label that is already disabled by removing the
label from the `ignore_labels` list in the
`observability-managed-cluster-label-allowlist` ConfigMap.

For example, enable the `local-cluster` and `name` labels. Your
`observability-managed-cluster-label-allowlist` ConfigMap might resemble
the following content:

    data:
      managed_cluster.yaml: |
        ignore_labels:
          - clusterID
          - installer.name
          - installer.namespace
        labels:
          - cloud
          - vendor
          - local-cluster
          - name

The ConfigMap resyncs after 30 seconds to ensure that the cluster labels
are updated. After you update the ConfigMap, check the
`observability-rbac-query-proxy` pod logs in the
`open-cluster-management-observability` namespace to verify where the
label is listed. The following information might be displayed in the pod
log:

    enabled managedcluster labels: <label>

From the Grafana dashboard, verify that the label is listed as a value
in the *Label* drop-down menu.

#### Disabling managed cluster labels

Exclude a managed cluster label from being listed in the *Label*
drop-down filter. Add the label name to the `ignore_labels` list. For
example, your YAML might resemble the following file if you add
`local-cluster` and `name` back into the `ignore_labels` list:

    data:
      managed_cluster.yaml: |
        ignore_labels:
          - clusterID
          - installer.name
          - installer.namespace
          - local-cluster
          - name
        labels:
          - cloud
          - vendor

Check the `observability-rbac-query-proxy` pod logs in the
`open-cluster-management-observability` namespace to verify where the
label is listed. The following information might be displayed in the pod
log:

    disabled managedcluster label: <label>

## Managing alerts

Configure Observability alerts to monitor both your hub cluster and
managed cluster activity, forward platform and user workload alerts to
the Alertmanager on your hub cluster, and route notifications to
external systems such as Slack, email, or PagerDuty.

### Prerequisites

You must have the following credentials and complete the following
actions to manage alerts:

- Enable Observability on your hub cluster.

- Have the create permission for `Secret` resources in the
  `open-cluster-management-observability` namespace.

- Have edit permission on the `MultiClusterObservability` resource.

- Configure the Prometheus instances on your managed cluster to help
  prevent metric loss during restart. For help, see Configuring
  persistent storage in the OpenShift Container Platform documentation.

- Enable user workload monitoring and alerts on your managed clusters.
  For help, see Configuring user workload monitoring and Managing alerts
  in the OpenShift Container Platform documentation.

- For the user workload for Prometheus, add a label to alerting rules in
  order to force only user workload Prometheus that are deployed in the
  `openshift-user-workload-monitoring` namespace to evaluate the
  alerting rule and prevents the Thanos Ruler instance from processing
  them. For help, see Creating alerting rules for user-defined projects
  in the OpenShift Container Platform documentation.

### Configuring Alertmanager

Integrate external messaging tools such as email, Slack, and PagerDuty
to receive notifications from Alertmanager. You must override the
`alertmanager-config` secret in the
`open-cluster-management-observability` namespace to add integrations,
and configure routes for Alertmanager. Complete the following steps to
update the custom receiver rules:

1.  Extract the data from the `alertmanager-config` secret. Run the
    following command:

        oc -n open-cluster-management-observability get secret alertmanager-config --template='{{ index .data "alertmanager.yaml" }}' |base64 -d > alertmanager.yaml

2.  Edit and save the `alertmanager.yaml` file configuration by running
    the following command:

        oc -n open-cluster-management-observability create secret generic alertmanager-config --from-file=alertmanager.yaml --dry-run -o=yaml |  oc -n open-cluster-management-observability replace secret --filename=-

    Your updated secret might resemble the following content:

        global
          smtp_smarthost: 'localhost:25'
          smtp_from: 'alertmanager@example.org'
          smtp_auth_username: 'alertmanager'
          smtp_auth_password: 'password'
        templates:
        - '/etc/alertmanager/template/*.tmpl'
        route:
          group_by: ['alertname', 'cluster', 'service']
          group_wait: 30s
          group_interval: 5m
          repeat_interval: 3h
          receiver: team-X-mails
          routes:
          - match_re:
              service: ^(foo1|foo2|baz)$
            receiver: team-X-mails

After you modify the secret, your changes are applied immediately. For
an example of Alertmanager, see prometheus/alertmanager.

### Securing communication from Alertmanager to third-party endpoints

Enable secure external communication from Alertmanager to third-party
endpoints such as Slack, email, and PagerDuty by keeping your
credentials secure and manageable through Kubernetes `Secret` resources.
You can create `Secret` resources with arbitrary content that you can
mount within your `alertmanager` pods for access to authorization
credentials.

To reference secrets within your Alertmanager configuration, add the
`Secret` resource content within the
`open-cluster-management-observability` namespace and mount the content
within the `alertmanager` pods. For example, to create and mount a `tls`
secret, complete the following steps:

1.  To create a `tls` secret with TLS certificates, run the following
    command:

        oc create secret tls tls --cert=</path/to/cert.crt> --key=</path/to/cert.key> -n open-cluster-management-observability

2.  To mount the `tls` secret to your `MultiClusterObservability`
    resource, add it to the `advanced` section. Your resource might
    resemble the following content:

        ...
        advanced:
         alertmanager:
           secrets: ['tls']

3.  To add a reference of your `tls` secret within your Alertmanager
    configuration, add the path of your secret to the configuration.
    Your resource might resemble the following configuration:

        tls_config:
         cert_file: '/etc/alertmanager/secrets/tls/tls.crt'
         key_file: '/etc/alertmanager/secrets/tls/tls.key'

4.  To verify that the secrets are within your `alertmanager` pods, run
    the following command:

        oc -n open-cluster-management-observability get secret alertmanager-config --template='{{ index .data "alertmanager.yaml" }}' |base64 -d > alertmanager.yaml

    Your YAML might resemble the following contents:

        "global":
          "http_config":
            "tls_config":
              "cert_file": "/etc/alertmanager/secrets/storyverify/tls.crt"
              "key_file": "/etc/alertmanager/secrets/storyverify/tls.key"

5.  To save the `alertmanager.yaml` configuration in the
    `alertmanager-config` secret, run the following command:

        oc -n open-cluster-management-observability create secret generic alertmanager-config --from-file=alertmanager.yaml --dry-run -o=yaml

6.  To replace the previous secret with your new secret, run the
    following command:

        oc -n open-cluster-management-observability replace secret --filename=-

### Forwarding alerts

After you enable Observability, alerts from your OpenShift Container
Platform managed clusters are automatically sent to Alertmanager on your
hub cluster. By default, all platform alerts are sent to Alertmanager on
your hub cluster. When you enable user workload alerts on your OpenShift
Container Platform managed clusters, user workload alerts are also sent
to your hub cluster. You can use the `alertmanager-config` YAML file to
configure alerts with an external notification system.

View the following example of the `alertmanager-config` YAML file:

    global:
      slack_api_url: '<slack_webhook_url>'

    route:
      receiver: 'slack-notifications'
      group_by: [alertname, datacenter, app]

    receivers:
    - name: 'slack-notifications'
      slack_configs:
      - channel: '#alerts'
        text: 'https://internal.myorg.net/wiki/alerts/{{ .GroupLabels.app }}/{{ .GroupLabels.alertname }}'

If you want to configure a proxy for alert forwarding, add the following
`global` entry to the `alertmanager-config` YAML file:

    global:
      slack_api_url: '<slack_webhook_url>'
      http_config:
        proxy_url: http://****

To forward user workload alerts, the alerts must be processed by the
user workload Prometheus instance and not by Thanos ruler. See the
following example of the `PrometheusRule` resource:

    apiVersion: monitoring.coreos.com/v1
    kind: PrometheusRule
    metadata:
      labels:
        openshift.io/prometheus-rule-evaluation-scope: leaf-prometheus

### Disabling alert forwarding for managed clusters

To disable alert forwarding for managed clusters, add the
`mco-disable-alerting: "true"` annotation to the
`MultiClusterObservability` custom resource. When you set the
`mco-disable-alerting: "true"` annotation, both the platform and user
workload alerts are not forwarded to the Alertmanager on your hub
cluster. The forwarding configuration on your managed clusters is
reverted.

Configuration updates to the `cluster-monitoring-config` config map in
the `openshift-monitoring` namespace are reverted. Setting the
annotation ensures that the `cluster-monitoring-config` config map is
not managed or updated by the Observability operator endpoint. After you
update the configuration, both platform and user workload Prometheus
instances on your managed cluster restarts. Complete the following
steps:

When the changes are reverted, a config map named
`cluster-monitoring-reverted` is created in the
`open-cluster-management-addon-observability` namespace. Any new, alert
forward configurations that are manually added are not reverted from the
config map.

1.  Run the following command to set the `mco-disable-alerting`
    annotation to `"true"`:

        oc annotate MultiClusterObservability observability mco-disable-alerting=true

    **Important:** You lose metrics when Prometheus on your managed
    cluster is not configured with a persistent volume.

2.  Verify that the hub cluster alert manager is no longer propagating
    managed cluster alerts to third-party messaging tools.

### Disabling user workload alert forwarding for managed clusters

To disable user workload alert forwarding for managed clusters, add the
`mco-disable-uwl-alerting: "true"` annotation to the
`MultiClusterObservability` custom resource. When you set the
annotation, forwarding user workload alerts to Alertmanager on your hub
cluster stops and platform alerts continue to forward to Alertmanager.

Setting the annotation ensures that the
`user-workload-monitoring-config` config map is not managed or updated
by the Observability operator endpoint. After you update the
configuraion, the user workload Prometheus instance on your managed
cluster restarts.

Run the following command to set the `mco-disable-uwl-alerting`
annotation to `"true"`:

    oc annotate MultiClusterObservability observability mco-disable-uwl-alerting=true

### Silencing alerts

Add alerts that you do not want to receive. You can silence alerts by
the alert name, match label, or time duration. After you add the alert
that you want to silence, an ID is created. Your ID for your silenced
alert might resemble the following string,
`d839aca9-ed46-40be-84c4-dca8773671da`.

Continue reading for ways to silence alerts:

- To silence a Red Hat Advanced Cluster Management alert, you must have
  access to the `alertmanager` pods in the
  `open-cluster-management-observability` namespace. For example, enter
  the following command in the `observability-alertmanager-0` pod
  terminal to silence `SampleAlert`:

      amtool silence add --alertmanager.url="http://localhost:9093" --author="user" --comment="Silencing sample alert" alertname="SampleAlert"

- Silence an alert by using multiple match labels. The following command
  uses `match-label-1` and `match-label-2`:

      amtool silence add --alertmanager.url="http://localhost:9093" --author="user" --comment="Silencing sample alert" <match-label-1>=<match-value-1> <match-label-2>=<match-value-2>

- If you want to silence an alert for a specific period of time, use the
  `--duration` flag. Run the following command to silence the
  `SampleAlert` for an hour:

      amtool silence add --alertmanager.url="http://localhost:9093" --author="user" --comment="Silencing sample alert" --duration="1h" alertname="SampleAlert"

  You can also specify a start or end time for the silenced alert. Enter
  the following command to silence the `SampleAlert` at a specific start
  time:

      amtool silence add --alertmanager.url="http://localhost:9093" --author="user" --comment="Silencing sample alert" --start="2023-04-14T15:04:05-07:00" alertname="SampleAlert"

- To view all silenced alerts that are created, run the following
  command:

      amtool silence --alertmanager.url="http://localhost:9093"

- If you no longer want an alert to be silenced, end the silencing of
  the alert by running the following command:

      amtool silence expire --alertmanager.url="http://localhost:9093" "d839aca9-ed46-40be-84c4-dca8773671da"

- To end the silencing of all alerts, run the following command:

      amtool silence expire --alertmanager.url="http://localhost:9093" $(amtool silence query --alertmanager.url="http://localhost:9093" -q)

### Migrating observability storage

If you use alert silencers, you can migrate observability storage while
retaining the silencers from its earlier state. To do this, migrate your
Red Hat Advanced Cluster Management observability storage by creating
new `StatefulSets` and `PersistentVolumes` (PV) resources that use your
chosen `StorageClass` resource.

**Note:** The storage for PVs is different from the object storage used
to store the metrics collected from your clusters.

When you use `StatefulSets` and PVs to migrate your observability data
to new storage, it stores the following data components:

- **Observatorium or Thanos:** Receives data then uploads it to object
  storage. Some of its components store data in PVs. For this data, the
  Observatorium or Thanos automatically regenerates the object storage
  on a startup, so there is no consequence if you lose this data.

- **Alertmanager:** Only stores silenced alerts. If you want to keep
  these silenced alerts, you must migrate that data to the new PV.

To migrate your observability storage, complete the following steps:

1.  In the `MultiClusterObservability`, set the
    `.spec.storageConfig.storageClass` field to the new storage class.

2.  To ensure the data of the earlier `PersistentVolumes` is retained
    even when you delete the `PersistentVolumeClaim`, go to all your
    existing `PersistentVolumes`.

3.  Change the `reclaimPolicy` to
    `` "Retain": `oc patch pv <your-pv-name> -p '{"spec":{"persistentVolumeReclaimPolicy":"Retain"}}' ``.

4.  **Optional:** To avoid losing data, see Migrate persistent data to
    another Storage Class in DG 8 Operator in OCP 4.

5.  Delete both the `StatefulSet` and the `PersistentVolumeClaim` in the
    following `StatefulSet` cases:

    1.  `alertmanager-db-observability-alertmanager-<REPLICA_NUMBER>`

    2.  `data-observability-thanos-<COMPONENT_NAME>`

    3.  `data-observability-thanos-receive-default`

    4.  `data-observability-thanos-store-shard`

    5.  **Important:** You might need to delete, then re-create, the
        `MultiClusterObservability` operator pod so that you can create
        the new `StatefulSet`.

6.  Re-create a new `PersistentVolumeClaim` with the same name but the
    correct `StorageClass`.

7.  Create a new `PersistentVolumeClaim` referring to the old
    `PersistentVolume`.

8.  Verify that the new `StatefulSet` and `PersistentVolumes` use the
    new `StorageClass` that you chose.

### Suppressing alerts

Suppress Red Hat Advanced Cluster Management alerts across your clusters
globally that are less severe. Suppress alerts by defining an inhibition
rule in the `alertmanager-config` in the
`open-cluster-management-observability` namespace.

An inhibition rule mutes an alert when there is a set of parameter
matches that match another set of existing matchers. In order for the
rule to take effect, both the target and source alerts must have the
same label values for the label names in the `equal` list. Your
`inhibit_rules` might resemble the following:

    global:
      resolve_timeout: 1h
    inhibit_rules:
      - equal:
          - namespace
        source_match:
          severity: critical
        target_match_re:
          severity: warning|info

- The `inhibit_rules` parameter section is defined to look for alerts in
  the same namespace. When a `critical` alert is initiated within a
  namespace and if there are any other alerts that contain the severity
  level `warning` or `info` in that namespace, only the `critical`
  alerts are routed to the Alertmanager receiver. The following alerts
  might be displayed when there are matches:

      ALERTS{alertname="foo", namespace="ns-1", severity="critical"}
      ALERTS{alertname="foo", namespace="ns-1", severity="warning"}

- If the value of the `source_match` and `target_match_re` parameters do
  not match, the alert is routed to the receiver:

      ALERTS{alertname="foo", namespace="ns-1", severity="critical"}
      ALERTS{alertname="foo", namespace="ns-2", severity="warning"}

  - To view suppressed alerts in Red Hat Advanced Cluster Management,
    enter the following command:

  <!-- -->

      amtool alert --alertmanager.url="http://localhost:9093" --inhibited

## *RightSizingRecommendation* guides (Technology Preview)

The `RightSizingRecommendation` feature compares real-time CPU and
memory usage with the resource configuration that you set, and offers
guides to optimize workloads on a namespace and cluster level.

With `RightSizingRecommendation`, you can use infrastructure more
efficiently, reduce costs, and ensure better performance across
workloads by identifying over-provisioned or under-utilized resources
across managed clusters.

You can enable `RightSizingRecommendation` for namespaces and virtual
machines. View the following descriptions of your
`RightSizingRecommendation` options:

Namespace right-sizing  
Optimize workloads at the namespace and cluster level based on your pod
CPU or memory usage.

Virtualization right-sizing  
Optimize workloads at the virtual machine level and cluster level based
on your virtual machine CPU or memory usage.

**Notes:**

- Prometheus rules are based on the cluster name, not on the cluster ID.

- The CPU and memory request, utilization, and guide metrics show
  maximum values based on the last number of aggregated days you select.

- Historical data points are not backfilled. After you install the
  `RightSizingRecommendation` feature, you need to wait to investigate
  longer aggregation periods.

### Optimizing workloads by using *RightSizingRecommendation* for namespaces (Technology Preview)

Implement `RightSizingRecommendation` to view a comparison of real-time
CPU and memory usage with the resource configuration that you set.
Enable `RightSizingRecommendation` for your namespaces in the
`MultiClusterObservability` custom resource on the hub cluster.

After enabling `RightSizingRecommendation`, the following resources are
created automatically:

The `rs-namespace-config` `ConfigMap`  
Stores configurations for placement and `PrometheusRule`.

The `rs-prom-rules-policy` `Policy`  
Contains the Prometheus rules to evaluate resource usage.

The `rs-placement` `Placement`  
Determines target clusters based on label selectors.

The `rs-policyset-binding` `PlacementBinding`  
Binds the policy and placement together.

**Required access:** Editor

#### Enabling *RightSizingRecommendation* for namespaces (Technology Preview)

Complete the following steps to enable `RightSizingRecommendation` for
namespaces:

1.  Open the `observability` instance configuration. Run the following
    command:

        oc edit multiclusterobservability observability

2.  Add the following lines to the `spec` section of your
    `MultiClusterObservability` custom resource:

        apiVersion: observability.open-cluster-management.io/v1beta2
        kind: MultiClusterObservability
        metadata:
          name: observability
        spec:
          capabilities:
            platform:
              analytics:
                namespaceRightSizingRecommendation:
                  enabled: true
        . . .

3.  To disable `RightSizingRecommendation` for namespaces, set the
    `namespaceRightSizingRecommendation.enabled:` to `false` .

4.  View `RightSizingRecommendation` guides from your Grafana board by
    selecting **RightSizing Recommendation** &gt; **ACM Right-Sizing
    Namespace**.

5.  To view the aggregated data on Grafana, expand or collapse the
    dashboard by clicking the drop-down arrow. For example, expand the
    memory data by clicking the name of the dashboard.

### Configuring *RightSizingRecommendation* for namespaces (Technology Preview)

Customize `RightSizingRecommendation` to optimize CPU and memory
resources for your namespaces. Edit the `rs-namespace-config`
`ConfigMap` resource.

**Required access:** Editor

Complete the following steps:

1.  Configure your placement for the `rs-namespace-config` `ConfigMap`
    resource placement. See the following example where the policy only
    applies to clusters with the `environment=prod` label:

        placementConfiguration: |
         spec:
           . . .
           predicates:
           - requiredClusterSelector:
               labelSelector:
                 matchLabels:
                   environment: prod
           . . .

2.  Configure your `PrometheusRule` resource by completing changes to
    one of the following steps:

    1.  Define the namespaces that you want to include or exclude in the
        `namespaceFilterCriteria` specification.

    2.  Add a list of namespaces that you want to include in the
        `inclusionCriteria` specification.

    3.  Add a list of namespaces that you want to exclude in the
        `exclusionCriteria` specification.

        **Note:** You cannot use both `inclusionCriteria` and
        `exclusionCriteria` at the same time.

    4.  To adjust the CPU and memory percentages, define the percentage
        usage.

        See the following example where the `inclusionCriteria`
        specification includes `prod` and the `exclusionCriteria`
        excludes `openshift`:

    <!-- -->

        . . .
          prometheusRuleConfig: |
           namespaceFilterCriteria:
            inclusionCriteria:
            - prod.*
            exclusionCriteria:
            - openshift.*
          labelFilterCriteria:
          - labelName: label_kubernetes_io_metadata_name
            inclusionCriteria:
            - prod
            - staging
            exclusionCriteria:
            - kube.*
          recommendationPercentage: 120
          . . .

3.  Configure your namespace binding. By default, the
    `RightSizingRecommendation` feature uses the
    `open-cluster-management-global-set` namespace for binding policies
    to clusters.

    1.  To bind generated policies to a different namespace and cluster
        set, add your namespace to the `namespaceBinding` specification.
        **Important:** Ensure that the target namespace is part of a
        valid `ClusterSet` before you apply the change. The policies
        that you generate might not apply to any clusters if there is no
        valid binding.

        See the following example where the `<your-namespace-binding>`
        namespace is the value for `namespaceBinding`:

    <!-- -->

        apiVersion: observability.open-cluster-management.io/v1beta2
        kind: MultiClusterObservability
        metadata:
          name: observability
        spec:
          . . .
          capabilities:
            platform:
              analytics:
                namespaceRightSizingRecommendation:
                  enabled: true
                  namespaceBinding: <your-namespace-binding>
          . . .

### Enabling *RightSizingRecommendation* for Virtualization workloads (Technology Preview)

Enable `RightSizingRecommendation` for Virtualization to help you
identify over-provisioned or under-utilized virtual machine resources
across managed clusters.

Implement `RightSizingRecommendation` by enabling the feature in the
`MultiClusterObservability` custom resource on the hub cluster.

After enabling `RightSizingRecommendation`, the following resources are
created automatically:

The `rs-virt-config` `ConfigMap`  
Stores virtual machine configurations for placement and
`PrometheusRule`.

The `rs-virt-prom-rules-policy` `Policy`  
Contains the Prometheus rules to evaluate resource usage.

The `rs-virt-placement` `Placement`  
Determines target clusters based on label selectors.

The `rs-virt-policyset-binding` `PlacementBinding`  
Binds the policy and placement together.

**Required access:** Editor

Complete the following steps to enable right-sizing for your virtual
machines:

1.  Open the `observability` instance configuration. Run the following
    command:

        oc edit multiclusterobservability observability

2.  Add the following lines to the `spec` section of your
    `MultiClusterObservability` custom resource:

        apiVersion: observability.open-cluster-management.io/v1beta2
        kind: MultiClusterObservability
        metadata:
          name: observability
        spec:
          capabilities:
            platform:
              analytics:
                virtualizationRightSizingRecommendation:
                  enabled: true
        . . .

3.  To disable `RightSizingRecommendation` for your virtual machines,
    set the `virtualizationRightSizingRecommendation.enabled:` parameter
    to `false`.

4.  View `RightSizingRecommendation` guides from your Grafana dashboard
    by selecting **RightSizing Recommendation** &gt; **ACM Right-Sizing
    OpenShift Virtualization**.

    **Note:** The CPU and memory information at the cluster level is
    displayed.

5.  To view CPU and memory details, and past resource usage for your
    virtual machines, select the name of your virtual machine.

### Configuring *RightSizingRecommendation* for Virtualization (Technology Preview)

You can customize the `RightSizingRecommendation` specification to
optimize CPU and memory resources for your virtual machines. Edit the
`MultiClusterObservability` resource.

Complete the following steps:

1.  Configure placement for your virtual machines by editing the
    `rs-virt-config` `ConfigMap` resource and defining the
    `placementConfiguration` parameter. Customize your placement to
    where the policy only applies to clusters with the
    `environment=prod` label, as displayed in the following example:

        placementConfiguration: |
         spec:
           . . .
           predicates:
           - requiredClusterSelector:
               labelSelector:
                 matchLabels:
                   environment: prod
           . . .

2.  Configure `PrometheusRule` for your virtual machines by completing
    one of the following steps:

    1.  Define the namespaces that you want to include or exclude in the
        `namespaceFilterCriteria` specification.

        1.  Add a list of namespaces that you want to include in the
            `inclusionCriteria` specification.

        2.  Add a list of namespaces that you want to exclude in the
            `exclusionCriteria` specification.

            **Note:** You cannot use both `inclusionCriteria` and
            `exclusionCriteria` at the same time.

        3.  To adjust the CPU and memory percentages, define the
            percentage usage.

        See the following example where the `inclusionCriteria`
        specification includes `prod` and the `exclusionCriteria`
        excludes `openshift`:

    <!-- -->

        . . .
          prometheusRuleConfig: |
           namespaceFilterCriteria:
            inclusionCriteria:
            - prod.*
            exclusionCriteria:
            - openshift.*
          labelFilterCriteria:
          - labelName: label_kubernetes_io_metadata_name
            inclusionCriteria:
            - prod
            - staging
            exclusionCriteria:
            - kube.*
          recommendationPercentage: 120
          . . .

3.  Configure your namespace binding. By default, the
    `RightSizingRecommendation` feature uses the
    `open-cluster-management-global-set` namespace for binding policies
    to clusters.

    1.  To bind generated policies to a different namespace and cluster
        set, use the `namespaceBinding` property. **Important:** Ensure
        that the target namespace is part of a valid `ClusterSet` before
        you apply the change. The policies that you generate might not
        apply to any clusters if there is no valid binding.

        See the following example where the `<your-namespace-binding>`
        namespace is the value for `namespaceBinding`:

    <!-- -->

        apiVersion: observability.open-cluster-management.io/v1beta2
        kind: MultiClusterObservability
        metadata:
          name: observability
        spec:
          . . .
          capabilities:
            platform:
              analytics:
                virtualizationRightSizingRecommendation:
                  enabled: true
                  namespaceBinding: <your-namespace-binding>
          . . .

    **Important:** Ensure that the target namespace is part of a valid
    `ClusterSet` before you apply the change. The policies that you
    generate might not apply to any clusters if there is no valid
    binding.

## Multicluster observability add-on

Use the multicluster observability add-on as an alternative way to
collect metrics from your managed clusters. Configure metrics collection
by using names, matchers, and recording rules for both platform and user
workloads. The multicluster observability add-on use the Prometheus
Operator and Prometheus Agent from the Red Hat OpenShift Cluster
Observabililty Operator to federate, downsample, and remote-write
metrics to your hub cluster. Reduce data loss during network partitions
between your managed and hub clusters when you enable the multicluster
observability add-on. By default, the multicluster observability add-on
is disabled.

### Managed cluster workloads

Managed cluster monitoring workloads use the Prometheus Operator and
Prometheus Agent from the Cluster Observability Operator. The
multicluster observability add-on uses the existing
`obo-prometheus-operator` from Red Hat OpenShift Cluster Observabililty
Operator on a managed cluster to reconcile Prometheus custom resources.
If `obo-prometheus-operator` is not present, the multicluster
observability add-on deploys `obo-prometheus-operator` within the
configured `agentInstallNamespace`.

Both of the multicluster observability add-on and Cluster Observabililty
Operator share the `monitoring.rhobs` API Group for the `ScrapeConfig`
and `PrometheusAgent` resources.

For other managed clusters that are not OpenShift Container Platform
clusters, the following resources are deployed:

- Node exporter

- Kube state metrics

- Prometheus server

**Note:** For clusters other than OpenShift Container Platform, the
cluster ID of other managed clusters use the `id.k8s.io` claim of the
managed cluster, while the current endpoint operator uses the cluster
name.

### Configurable APIs

Control monitoring behavior on your managed clusters by configuring
default resource configurations. The following default resources are
automatically created for platform monitoring and to have functional
dashboards, `PrometheusAgent`, `ScrapeConfig`, and `PrometheusRule`.
View the following descriptions of each API:

`PrometheusAgent`  
Defines a `PrometheusAgent` deployment, a resource-optimized Prometheus
instance for remote-write workflows. Configures remote-write targets,
scrape intervals, and resource limits. Use the `PrometheusAgent`
resource as your metrics collector.

`ScrapeConfig`  
A list of metrics to be federated from a given `target`. Configure the
following specifications, `job_name`, `metrics_path`, `params`, and
`relabel_configs`. You can override the `target` configuration for user
workloads.

`PrometheusRule`  
Supports alerting and recording rule definitions that you can apply for
each cluster. Supports groups of rules with evaluation intervals and
alert annotations or labels.

`ClusterManagementAddOn`  
Placements and configurations for deploying your managed clusters.
Configurations include an `AddonDeploymentConfig` resource to customize
the deployment of the multicluster observability add-on on managed
clusters. You can use this configuration to customize the node placement
and select the installation namespace on your managed clusters, where
the Prometheus Agent pods are deployed.

**Note:** A single `AddonDeploymentConfig` resource is used for all
placements.

### Default platform metrics

By default, the multicluster observability add-on collects platform
metrics from your managed clusters. There are a set of `ScrapeConfig`
resources that are automatically generated and deployed to all of your
managed clusters. All placements that you reference within the
`ClusterManagementAddOn` resource automatically receive the
`ScrapeConfig` configurations. Use the default `ScrapeConfig` resources
for platform workload dashboards.

The following default platform metrics are collected:

- `platform-metrics-hcp`, which is specific for the hosted control plane
  platform

- `platform-metrics-virtualization`, which is specific for the Red Hat
  OpenShift Virtualization platform

- `platform-metrics-alerts`, which is specific for custom alert rule
  metrics across all platforms

- `platform-metrics-default`, which is specific for default metrics
  across all platfroms

### Health status of the multicluster observability add-on

The multicluster observability add-on health status is reported through
the `ManagedClusterAddOn` resource. From the OpenShift Container
Platform console for each managed cluster, the `ManagedClusterResource`
is displayed in the **Fleet Management** view. The status is degraded if
some resources are not deployed or the platform `PrometheusAgent`
resource is not running.

**Note:** For OpenShift Container Platform versions earlier than version
4.20, select **All Clusters** from the **Cluster** switcher.

The following alerting rules are pushed to all managed clusters:

`MetricsCollectorNotIngestingSamples`  
Alerts you when the `PrometheusAgent` resource is not federating any
metrics.

`MetricsCollectorRemoteWriteFailures`  
Alerts you when there is a high failure rate for remote-write requests
in the `PrometheusAgent` resource of your managed cluster.

`MetricsCollectorRemoteWriteBehind`  
Alerts you when the `PrometheusAgent` resource remote-write is too slow.

### Enabling the multicluster observability add-on

Enable the multicluster observability add-on on your hub cluster to
configure your metrics for your platform and user workloads. You are
required to enable platform workloads and it is optional to enable user
workloads.

When you enable `platform` and `userWorkloads` specifications, the
`MultiClusterObservability` operator stops deploying the metrics
collectors to your managed clusters and deploys the
`multicluster-observability-addon-manager` in the
`open-cluster-management-observability` namespace. The
`multicluster-observability-addon-manager` deploys the new metrics
collectors based on the `PrometheusAgent` resource defined on your hub
cluster.

**Required access:** Cluster administrator

Procedure

Complete the following steps to enable the multicluster observability
add-on on your hub cluster:

1.  To enable platform monitoring and user workload monitoring, add the
    `platform` and `userWorkloads` specification to your
    `MultiClusterObservability` resource. Run the following command:

        oc patch mco observability -n open-cluster-management-observability --type=merge -p '{"spec":{"capabilities":{"platform":{"metrics":{"default":{"enabled": true}}},"userWorkloads":{"metrics":{"default":{"enabled": true}}}}}}'

    Your `MultiClusterObservability` resource might resemble the
    following file example:

        apiVersion: observability.open-cluster-management.io/v1beta2
        kind: MultiClusterObservability
        metadata:
          name: observability
        spec:
          capabilities:
            platform:
              metrics:
                default:
                  enabled: true
            userWorkloads:
              metrics:
                default:
                  enabled: true

2.  To verify that the default configuration resources for the
    multicluster observability add-on are created, open your
    `multicluster-observability-addon` `ClusterManagementAddon`
    resource. Run the following command:

        oc get prometheusagents -n open-cluster-management-observability

3.  Verify that the default configurations are added to your placements.
    Run the following command:

        oc get cma multicluster-observability-addon -o yaml | yq '.spec.installStrategy.placements'

### Configuring APIs for the multicluster observability add-on

Configure the default metrics-specific APIs of the multicluster
observability add-on. When you reference a new placement in your
`ClusterManagementAddon` resource, the
`multicluster-observability-addon-manager` automatically creates
specific default `PrometheusAgent` resources. The
`multicluster-observability-addon-manager` adds the `PrometheusAgent`
resources reference in the related `Placement` configurations.

While there is one `PrometheusAgent` resource created by the placement,
the default `ScrapeConfigs` and `PrometheusRules` are common to all
placements. The following resources are the default configuration
resources for the multicluster observability add-on: `PrometheusAgent`,
`ScrapeConfigs`, and `PrometheusRules`.

**Required access:** Cluster administrator

Procedure

Complete the following to configure the APIs for the multicluster
observability add-on:

1.  **Optional** Override the default scrape interval for your
    `PrometheusAgent` resource by changing the `scrapeInterval`
    parameter. The default value is `300s`. You can also override the
    `scrapeInterval` of the `scrapeConfig` resource.

2.  Configure the `ScrapeConfig` resource to define a set of metrics for
    independent federation from Prometheus of your managed clusters.
    Complete the following steps:

    1.  Add the name of the job that you want to reference for the
        `jobName` parameter.

    2.  To ensure that Prometheus federates metrics, add the `/federate`
        URL path for the `metricsPath` parameter.

    3.  Add the metric name and labels that you want to collect. See the
        following YAML file example where the `ScrapeConfig` resource
        collects the `up` metric:

    <!-- -->

        apiVersion: monitoring.rhobs/v1alpha1
        kind: ScrapeConfig
        metadata:
          name: some-metrics-to-collect
          namespace: open-cluster-management-observability
          labels:
            - app.kubernetes.io/component: <platform-metrics-collector> or <user-workload-metrics-collector>
        spec:
          jobName: some-job-name
          metricsPath: /federate
          params:
            match[]:
            - '{__name__="up"}'

3.  Configure the `PrometheusRule` resource to limit the cardinality of
    your collected metrics on your hub cluster. Complete the following
    steps:

    1.  Define alerting and recording rules for platform and user
        workload monitoring on your managed clusters.

    2.  To target user workloads in your `PrometheusRule` resource, add
        the following annotation to define the namespace where you want
        to deploy the resource:
        `observability.open-cluster-management.io/target-namespace`.

    **Notes:**

    - When the
      `observability.open-cluster-management.io/target-namespace` is not
      set in your `PrometheusRule` resource, the `PrometheusRule`
      resource are deployed to the default installation namespace. If
      `openshift.io/cluster-monitoring` is set to `true`, the
      `PrometheusRule` resouces are not monitored by OpenShift Container
      Platform user workload monitoring stack.

    - Be sure to use the `monitoring.coreos.com` group for the
      `PrometheusRule` resource.

4.  Configure the `AddonDeploymentConfig` resource to customize the
    deployment of the multicluster observability add-on on managed
    clusters. **Note:** The values in the `AddonDeploymentConfig`
    resource are override direct modifications of other resources.
    Complete the following steps:

    1.  Define the namespace where you install the `PrometheusAgent`
        resource for the `agentInstallNamespace` parameter. The default
        namespace is `open-cluster-management-agent-addon`.

    2.  Add the `nodePlacement` specification with the associated
        `nodeSelector` and `tolerations` parameters.

    3.  Edit the `proxyConfig` specification by updating the `httpProxy`
        and `noProxy` configurations.

### Adding custom metrics for the multicluster observability add-on

Add your own custom metrics to be collected from your managed clusters
by configuring the `ScrapeConfig` resource. The `ScrapeConfig` must be
added to the `Placement` configurations of the `ClusterManagementAddOn`
resource for deploying on the corresponding managed clusters. The
Prometheus operator on each managed cluster adds the new `ScrapeConfig`
resource to the `PrometheusAgent` resource.

**Requierd access:** Cluster administrator

Complete the following steps to add custom metrics for the multicluster
observability add-on:

1.  Create a new `ScrapeConfig` resource in the
    `open-cluster-management-observability` namespace that includes
    values for the required parameters, `jobName`, `metricsPath`, and
    `params`.

2.  Add the appropriate label for the `app.kubernetes.io/component`
    parameter to specify whether the metrics are for platform monitoring
    or user workload monitoring. Use one of the following label values,
    `platform-metrics-collector` or `user-workload-metrics-collector`.

    **Note:** When you use the `platform-metrics-collector` label, the
    multicluster observability add-on automatically sets the
    `scrapeClass` and `targets` parameters to enable federation from the
    platform Prometheus of your OpenShift Container Platform managed
    cluster. You can override the `scrapeClass` and `targets` parameters
    by adding the value that you need.

3.  **Optional:** Manually set the `scrapeClass` and `staticConfigs`
    specifications for your `user-workload-metrics-collector`
    `ScrapeConfig` resource.

4.  Add the `ScrapeConfig` resource reference to the placements of the
    `ClusterManagementAddOn` resource where you want the resource to be
    deployed.

    **Note:** Ensure that you reference the `ScrapeConfig` resource only
    after you create it. Otherwise, the add-on status updates to a
    `Deploying` status because the resource does not exist.

    Your `ScrapeConfig` resource might resemble the following YAML file:

        apiVersion: monitoring.rhobs/v1alpha1
        kind: ScrapeConfig
        metadata:
          name: add-custom-metrics
          namespace: open-cluster-management-observability
          labels:
            - app.kubernetes.io/component: platform-metrics-collector
        spec:
          jobName: some-job-name
          metricsPath: /federate
          params:
            match[]:
            - '{__name__="up"}'

### Federating user workloads from Cluster Observability Operator

Federate your user workloads from the Red Hat OpenShift Cluster
Observability Operator on your managed clusters. By default, user
workload metrics are federated from the Prometheus user-workload on your
OpenShift Container Platform cluster.

**Required access:** Cluster administrator

Prerequisites

- User workload monitoring is enabled on your managed cluster.

- User workload monitoring is enabled in the `MultiClusterObservability`
  custom resource.

- You have created `ScrapeConfig` resources with the
  `app.kubernetes.io/component: <user-workload-metrics-collector>`
  label.

- The `ScrapeConfig` resources are referenced in the configurations list
  of the `ClusterManagementAddOn` for the target placements.

Procedure

Complete the following steps to federate user workloads from the Cluster
Observability Operator on your managed clusters:

1.  Update your `ScrapeConfig` resource by adding the endpoint of the
    Cluster Observability Operator `MonitoringStack` resource. Your
    resource might resemble the following YAML file:

        apiVersion: monitoring.coreos.com/v1alpha1
        kind: ScrapeConfig
        spec:
          scrapeClass: “”
          scheme: HTTP
          staticConfigs:
          - targets:
            - my-monitoring-stack.my-monitoring-ns.svc:9090

2.  If you use a proxy with the Prometheus server, modify the
    `ScrapeConfig` resource to include your TLS configuration. Create a
    corresponding `scrapeClass` specification on the user workload
    `PrometheusAgent` resource. Then reference the `PrometheusAgent`
    resource within the `ScrapeConfig` resource.

### Relabeling default metrics for the multicluster observability add-on

Relabel configurations to modify or remove the default metrics that you
are collecting. Relabel configurations in each `ScrapeConfig` resource
or globally in the `remoteWrite` configuration of the `PrometheusAgent`
resource.

**Required access:** Cluster administrator

Procedure

Complete the following step to remove a default metric by relabeling the
metric for the multicluster observability add-on:

1.  To remove the `Watchdog` alert metric, add the `writeRelabelConfigs`
    specification to the `remoteWrite` configuration of the
    `PrometheusAgent` resource. The metric removal is complete after it
    is federated. Your `PrometheusAgent` resource might resemble the
    following YAML file:

        apiVersion: monitoring.rhobs/v1alpha1
        kind: ScrapeConfig
        metadata:
          name: platform-metrics-alerts
          namespace: open-cluster-management-observability
        spec:
          jobName: alerts
          metricRelabelings:
            - action: labeldrop
              regex: managed_cluster|id
            - action: drop
              regex: ^Watchdog$
              sourceLabels:
                - alertname
          metricsPath: /federate
          params:
            'match[]':
              - '{__name__="ALERTS"}'
          scheme: HTTPS
          scrapeClass: not-configurable
          staticConfigs:
            - targets:
                - not-configurable

### Exporting metrics to external endpoints for the multicluster observability add-on

To configure an external metrics endpoint, add your custom `remoteWrite`
specification to your `PrometheusAgents` resources. When you configure
your `remoteWrite` specification, the managed cluster sends metrics are
directly to the external endpoint.

Update related multicluster observability add-on configurations by
relabeling default metrics. Exporting metrics from your managed cluster
helps you improve resiliency during network partitions between your
managed and hub clusters for up to two hours.

**Required access:** Cluster administrator

Procedure

Complete the following steps to export metrics to external endpoints for
the `PrometheusAgent` resource:

1.  Create the TLS `Secret` config maps within the
    `open-cluster-management-observability` namespace.

2.  Add the secret names to the `secrets` specification of the
    `PrometheusAgent` resource.

3.  Add the `remoteWrite` specification to the `PrometheusAgent`
    resource. Your `PrometheusAgent` resource might resemble the
    following YAML file, where the `up` metric is exported to a custom
    endpoint:

        apiVersion: monitoring.rhobs/v1alpha1
        kind: PrometheusAgent
        metadata:
          name: mcoa-default-platform-metrics-collector-global
          namespace: open-cluster-management-observability
        spec:
          secrets:
            - custom-endpoint-ca
            - custom-endpoint-cert
          remoteWrite:
            - name: custom-endpoint
              tlsConfig:
                caFile: /etc/prometheus/secrets/custom-endpoint-ca/ca.crt
                certFile: /etc/prometheus/secrets/custom-endpoint-cert/tls.crt
                keyFile: /etc/prometheus/secrets/custom-endpoint-cert/tls.key
              url: 'https://my-custom-remote-write-endpoint.io/api/v1/receive'
              writeRelabelConfigs:
                - action: keep
                  regex: ^up$
                  sourceLabels:
                    - __name__
            - name: acm-observability
              ...

### Forwarding alerts for multicluster observability add-on

Configure alert forwarding for the multicluster observability add-on to
send alerts to the Alertmanager of the Observability stack from your
managed clusters. By default, multicluster observability add-on is not
configured to send alerts from Prometheus on your managed clusters to
the hub cluster Alertmanager.

Create a policy to configure alert forwarding when you use the
multicluster observability add-on.

**Required access:** Cluster administrator

Procedure

Complete the following steps to create a policy to configure alert
forwarding for the multicluster observability add-on:

1.  To configure alert forwarding for platform metrics, create a YAML
    file named `mcoa-alert-forward-platform.yaml`.

    1.  Add the base domain of your hub cluster for the `$hubBaseDomain`
        parameter. If you make custom changes to the
        `additionalAlertmanagerConfigs` specification of the config map,
        be sure to add the changes directly into the policy, before
        applying the policy.

        See the following example:

            apiVersion: policy.open-cluster-management.io/v1
            kind: Policy
            metadata:
              name: mcoa-alert-forward-platform
              namespace: open-cluster-management-global-set
            spec:
              disabled: false
              policy-templates:
              - objectDefinition:
                  apiVersion: policy.open-cluster-management.io/v1
                  kind: ConfigurationPolicy
                  metadata:
                    name: mcoa-alert-forward-platform
                  spec:
                    namespaceSelector:
                      exclude:
                      - kube-*
                      include:
                      - default
                    object-templates-raw: |
                      {{ $hubBaseDomain:= "INPUT_BASE_DOMAIN" }}
                      {{ $hubName := (split "." $hubBaseDomain)._0 }}
                      {{- $cmo := (lookup "v1" "ConfigMap" "openshift-monitoring" "cluster-monitoring-config") }}
                      {{- $cy := dict }}
                      {{- if and $cmo $cmo.data }}
                        {{- $cy = (index $cmo "data" "config.yaml") | fromYaml }}
                      {{- end }}

                      {{- $mangedConfig := dict }}

                      {{- $pm := `
                        prometheusK8s:
                          additionalAlertmanagerConfigs:
                          - apiVersion: v2
                            bearerToken:
                              key: token
                              name: observability-alertmanager-accessor-%[1]s
                            scheme: https
                            staticConfigs:
                            - alertmanager-open-cluster-management-observability.apps.%[2]s
                            tlsConfig:
                              ca:
                                key: service-ca.crt
                                name: hub-alertmanager-router-ca-%[1]s
                              insecureSkipVerify: false
                          externalLabels:
                            managed_cluster: %[3]s
                      ` }}

                        {{- $mangedConfig = merge $mangedConfig
                                          ((printf $pm $hubName $hubBaseDomain (fromClusterClaim "id.openshift.io"))| fromYaml)
                      }}
                      - complianceType: mustonlyhave
                        objectDefinition:
                          apiVersion: v1
                          data:
                            config.yaml: |
                              {{ (merge $cy $mangedConfig)| toYaml |autoindent }}
                          kind: ConfigMap
                          metadata:
                            name: cluster-monitoring-config
                            namespace: openshift-monitoring
                        recordDiff: InStatus
              remediationAction: inform

    2.  Create a `PlacementBinding` resource to bind the policy to the
        `global` placement.See the following sample:

            apiVersion: policy.open-cluster-management.io/v1
            kind: PlacementBinding
            metadata:
              name: mcoa-alert-forward-platform-placement
              namespace: open-cluster-management-global-set
            placementRef:
              apiGroup: cluster.open-cluster-management.io
              kind: Placement
              name: global
            subjects:
            - apiGroup: policy.open-cluster-management.io
              kind: Policy
              name: mcoa-alert-forward-platform

    3.  To apply the policy changes across all managed clusters and
        enable alert forwarding from your managed clusters to the hub
        cluster, change the `remediationAction` parameter value to
        `enforce`.

        **Note:** The `remediationAction` of the previous policy is set
        to `inform` mode. From the console, validate your changes by
        viewing the policy from the **Governance** page. Your policy
        appears as non-compliant.

    4.  Apply your YAML file. Run the following command:

            oc apply -f ./forward-platform-alerts.yaml

    **Note:** If you have managed clusters other than a Red Hat
    OpenShift Container Platform cluster, you must create the
    appropriate `PlacementBinding` resource targeting the managed
    clusters.

2.  To configure alert forwarding for user workload metrics, create a
    YAML file named `mcoa-alert-forward-uwl`.

    1.  Add the base domain for your hub cluster in the `$hubBaseDomain`
        parameter. Your YAML file might resemble the following example:

            apiVersion: policy.open-cluster-management.io/v1
            kind: Policy
            metadata:
              name: mcoa-alert-forward-uwl
              namespace: open-cluster-management-global-set
            spec:
              disabled: false
              policy-templates:
              - objectDefinition:
                  apiVersion: policy.open-cluster-management.io/v1
                  kind: ConfigurationPolicy
                  metadata:
                    name: mcoa-alert-forward-uwl
                  spec:
                    namespaceSelector:
                      exclude:
                      - kube-*
                      include:
                      - default
                    object-templates-raw: |
                      {{ $hubBaseDomain:= "INPUT_BASE_DOMAIN" }}
                      {{ $hubName := (split "." $hubBaseDomain)._0 }}

                      {{- $cmo := (lookup "v1" "ConfigMap" "openshift-user-workload-monitoring" "user-workload-monitoring-config") }}
                      {{- $cy := dict }}
                      {{- if and $cmo $cmo.data }}
                        {{- $cy = (index $cmo "data" "config.yaml") | fromYaml }}
                      {{- end }}

                      {{- $mangedConfig := dict }}

                      {{- $pm := `
                        prometheus:
                          additionalAlertmanagerConfigs:
                          - apiVersion: v2
                            bearerToken:
                              key: token
                              name: observability-alertmanager-accessor-%[1]s
                            scheme: https
                            staticConfigs:
                            - alertmanager-open-cluster-management-observability.apps.%[2]s
                            tlsConfig:
                              ca:
                                key: service-ca.crt
                                name: hub-alertmanager-router-ca-%[1]s
                              insecureSkipVerify: false
                          externalLabels:
                            managed_cluster: %[3]s
                      ` }}

                        {{- $mangedConfig = merge $mangedConfig
                                          ((printf $pm $hubName $hubBaseDomain (fromClusterClaim "id.openshift.io"))| fromYaml)
                      }}
                      - complianceType: mustonlyhave
                        objectDefinition:
                          apiVersion: v1
                          data:
                            config.yaml: |
                              {{ (merge $cy $mangedConfig )| toYaml |autoindent }}
                          kind: ConfigMap
                          metadata:
                            name: user-workload-monitoring-config
                            namespace: openshift-user-workload-monitoring
                        recordDiff: InStatus
              remediationAction: inform

    2.  Create a `PlacementBinding` resource to bind the policy to the
        `global` placement. Your YAML file might resemble the following
        sample:

            apiVersion: policy.open-cluster-management.io/v1
            kind: PlacementBinding
            metadata:
              name: mcoa-alert-forward-uwl-placement
              namespace: open-cluster-management-global-set
            placementRef:
              apiGroup: cluster.open-cluster-management.io
              kind: Placement
              name: global
            subjects:
            - apiGroup: policy.open-cluster-management.io
              kind: Policy
              name: mcoa-alert-forward-uwl

    3.  Apply your YAML file. Run the following command:

    <!-- -->

        oc apply -f ./forward-uwl-alerts.yaml

# Using observability with Red Hat Insights

Red Hat Insights is integrated with Red Hat Advanced Cluster Management
observability, and is enabled to help identify existing or potential
problems in your clusters. Red Hat Insights helps you to identify,
prioritize, and resolve stability, performance, network, and security
risks. Red Hat OpenShift Container Platform offers cluster health
monitoring through Red Hat OpenShift Cluster Manager. Red Hat OpenShift
Cluster Manager collects anonymized, aggregated information about the
health, usage, and size of the clusters. For more information, see Red
Hat Insights product documentation.

When you create or import an OpenShift cluster, anonymized data from
your managed cluster is automatically sent to Red Hat. This information
is used to create insights, which provide cluster health information.
Red Hat Advanced Cluster Management administrator can use this health
information to create alerts based on severity.

**Required access**: Cluster administrator

## Prerequisites

- Ensure that Red Hat Insights is enabled. For more information, see
  Modifying the global cluster pull secret to disable remote health
  reporting.

- Install a supported version of OpenShift Container Platform.

- Hub cluster user, who is registered to Red Hat OpenShift Cluster
  Manager, must be able to manage all the Red Hat Advanced Cluster
  Management managed clusters in Red Hat OpenShift Cluster Manager.

## Managing insight *PolicyReports*

Red Hat Advanced Cluster Management for Kubernetes `PolicyReports` are
violations that are generated by the `insights-client`. The
`PolicyReports` are used to define and configure alerts that are sent to
incident management systems. When there is a violation, alerts from a
`PolicyReport` are sent to incident management system.

### Searching for insight policy reports

You can search for a specific insight `PolicyReport` that has a
violation, across your managed clusters. Complete the following steps:

1.  Log in to your Red Hat Advanced Cluster Management hub cluster.

2.  Select **Search** from the navigation menu.

3.  Enter the following query: `kind:PolicyReport`.

    **Note:** The `PolicyReport` name matches the name of the cluster.

4.  You can specify your query with the insight policy violation and
    categories. When you select a `PolicyReport` name, you are
    redirected to the *Details* page of the associated cluster. The
    *Insights* sidebar is automatically displayed.

5.  If the search service is disabled and you want to search for an
    insight, run the following command from your hub cluster:

        oc get policyreport --all-namespaces

### Viewing identified issues from the console

You can view the identified issues on a specific cluster. Complete the
following steps:

1.  Log in to your Red Hat Advanced Cluster Management cluster.

2.  Select **Overview** from the navigation menu.

3.  Check the *Cluster issues* summary card. Select a severity link to
    view the `PolicyReports` that are associated with that severity.
    Details of the cluster issues and the severities are displayed from
    the *Search* page. Policy reports that are associated with the
    severity and have one or more issues appear.

4.  Select a policy report to view cluster details from the *Clusters*
    page. The *Status* card displays information about *Nodes*,
    *Applications*, *Policy violations*, and *Identified issues*.

5.  Select the **Number of identified issues** to view details. The
    *Identified issues* card represents the information from Red Hat
    insights. The *Identified issues* status displays the number of
    issues by severity. The triage levels used for the issues are the
    following severity categories: *Critical*, *Major*, *Low*, and
    *Warning*.

    1.  Alternatively, you can select **Clusters** from the navigation
        menu.

    2.  Select a managed cluster from the table to view more details.

    3.  From the *Status* card, view the number of identified issues.

6.  Select the number of potential issues to view the severity chart and
    recommended remediations for the issues from the *Potential issue*
    side panel. You can also use the search feature to search for
    recommended remediations. The remediation option displays the
    *Description* of the vulnerability, *Category* that vulnerability is
    associated with, and the *Total risk*.

7.  Click the link to the vulnerability to view steps on *How to
    remediate* and the *Reason* for the vulnerability.

    **Note:** When you resolve the issue, you receive the Red Hat
    Insights every 30 minutes, and Red Hat Insights is updated every two
    hours.

8.  Be sure to verify which component sent the alert message from the
    `PolicyReport`.

    1.  Navigate to the *Governance* page and select a specific
        `PolicyReport`.

    2.  Select the *Status* tab and click the **View details** link to
        view the `PolicyReport` YAML file.

    3.  Locate the `source` parameter, which informs you of the
        component that sent the violation. The value options are `grc`
        and `insights`.

### Viewing update risk predictions

View the potential risks for updating your managed clusters. Complete
the following steps:

1.  Log in to your managed cluster.

2.  Go to the *Overview* page.

3.  From the *Powered by Insights* section, you can view the percentage
    of clusters with predicted risks, which are listed by severity.

4.  Select the number for the severity to view the list of clusters from
    the *Clusters* page.

5.  Select the cluster that you want, then click the **Actions**
    drop-down button.

6.  Click **Upgrade clusters** to view the risk for the upgdate.

7.  From the *Upgrade clusters* modal, find the *Upgrade risks* column
    and click the link for the number of risks to view information in
    the Hybrid Cloud console.
