# multicluster global hub

The multicluster global hub is a set of components that enable you to
import one or more hub clusters and manage them from a single hub
cluster.

After importing the hub clusters as managed hub clusters, you can use
multicluster global hub to complete the following tasks across all of
the managed hub clusters:

- Report the policy compliance status and trend

- Inventory all managed hubs and managed clusters on the overview page

- Detect and alert in cases of irregular policy behavior

The multicluster global hub is useful when a single hub cluster cannot
manage the large number of clusters in a high-scale environment. When
this happens, you divide the clusters into smaller groups of clusters
and configure a hub cluster for each group.

It is often inconvenient to view the data on multiple hub clusters for
the managed clusters that are managed by that hub cluster. The
multicluster global hub provides an easier way to view information from
multiple hubs by designating multiple hub clusters as managed hub
clusters. The multicluster global hub cluster manages the other hub
clusters and gathers summarized information from the managed hub
clusters.

Enable the Observability service on your multicluster global hub to view
the health and utilization of your managed hub clusters in Grafana
dashboards. View metrics from your multicluster global hub and hub
cluster. For more information about Observability, see Observability
service documentation.

## multicluster global hub architecture

The multicluster global hub consists of the following components that
are used to access and manage your hub clusters:

- A server component called the *global hub cluster* where the
  management tools and the console run

- A client component that is installed on Red Hat Advanced Cluster
  Management, named the *managed hub*, which can be managed by the
  global hub cluster. The managed hub also manages other clusters. You
  do not have to use a dedicated cluster for your multicluster global
  hub cluster.

Learn more about the architecture in the following sections:

### The multicluster global hub operator

The multicluster global hub operator contains the components of
multicluster global hub. The operator deploys all of the required
components for global multicluster management. The components include
`multicluster-global-hub-manager`, `multicluster-global-hub-grafana`,
and provided versions of `Kafka` and `PostgreSQL` in the multicluster
global hub cluster and `multicluster-global-hub-agent` in the managed
hub clusters.

### The multicluster global hub manager

The multicluster global hub manager is used to persist the data into the
`postgreSQL` database. The data is from Kafka transport. The manager
also posts the data to the Kafka transport, so it can be synchronized
with the data on the managed hub clusters.

### The multicluster global hub agent

The multicluster global hub agent runs on the managed hub clusters. It
synchronizes the data between the multicluster global hub cluster and
the managed hub clusters. For example, the agent synchronizes the
information of the managed clusters from the managed hub clusters to the
multicluster global hub cluster and synchronizes the policy or
application from the multicluster global hub cluster to the managed hub
clusters.

### The multicluster global hub visualizations

Grafana runs on the multicluster global hub cluster as the main service
for multicluster global hub visualizations. The PostgreSQL data
collected by the Global Hub Manager is its default DataSource. By
exposing the service using the route called
`multicluster-global-hub-grafana`, you can access the multicluster
global hub Grafana dashboards by accessing the console.

## multicluster global hub requirements

Learn about the multicluster global hub requirements and review the
components and environments that are supported by multicluster global
hub.

**Required access:** Cluster administrator

**OpenShift Container Platform Dedicated environment required access:**
You must have `cluster-admin` permissions. By default `dedicated-admin`
role does not have the required permissions to create namespaces in the
OpenShift Container Platform Dedicated environment.

### Networking requirements

See the following networking requirements:

- The managed hub cluster is also a multicluster global hub managed
  cluster in Red Hat Advanced Cluster Management. You must configure the
  network component in Red Hat Advanced Cluster Management. For Red Hat
  Advanced Cluster Management networking details, see Networking.

- To review the multicluster global hub network information, see the
  following table:

  - Direction: Inbound from the browser - Protocol: HTTPS - Connection:
    Access the Grafana dashboard - Port that is specified: 443 - Source
    address: Browser - Destination address: Grafana route IP address

  - Direction: Outbound to Kafka Cluster - Protocol: HTTPS - Connection:
    The multicluster global hub manager needs to receive data from Kafka
    cluster - Port that is specified: 443 - Source address:
    multicluster-global-hub-manager-xxx pod - Destination address: Kafka
    route host

  - Direction: Outbound to PostgreSQL database - Protocol: HTTPS -
    Connection: The multicluster global hub needs to contribute data to
    the PostgreSQL database - Port that is specified: 443 - Source
    address: multicluster-global-hub-manager-xxx pod - Destination
    address: PostgreSQL database IP address

- To review the managed hub network information, see the following
  table:

  - Direction: Outbound to Kafka Cluster - Protocol: HTTPS - Connection:
    The multicluster global hub agent needs to sync cluster and policy
    information to Kafka cluster - Port that is specified: 443 - Source
    address: multicluster-global-hub-agent pod - Destination address:
    Kafka route host

- For sizing guidelines, see Sizing your Red Hat Advanced Cluster
  Management cluster.

### Supported components

See the following supported components:

- The multicluster global hub and OpenShift Container Platform console
  share an integrated console, so they support the same browser. For
  information about supported browsers and versions, see Accessing the
  web console in the Red Hat OpenShift Container Platform documentation

- See the following table of supported platforms for the multicluster
  global hub cluster:

  - Platform: Red Hat Advanced Cluster Management 2.14, and later 2.14.x
    releases - Supported for global hub cluster: Yes - Supported for
    managed hub cluster: Yes

  - Platform: Red Hat Advanced Cluster Management 2.13, and later 2.13.x
    releases - Supported for global hub cluster: Yes - Supported for
    managed hub cluster: Yes

  - Platform: Red Hat Advanced Cluster Management 2.12, and later 2.12.x
    releases - Supported for global hub cluster: Yes - Supported for
    managed hub cluster: Yes

  - Platform: Red Hat Advanced Cluster Management on Arm - Supported for
    global hub cluster: Yes - Supported for managed hub cluster: Yes

  - Platform: Red Hat Advanced Cluster Management on IBM Z - Supported
    for global hub cluster: Yes - Supported for managed hub cluster: Yes

  - Platform: Red Hat Advanced Cluster Management on IBM Power Systems -
    Supported for global hub cluster: Yes - Supported for managed hub
    cluster: Yes

- multicluster global hub supports middleware, such as Kafka,
  PostgreSQL, and Grafana. See the following table for a list of
  supported middleware and built-in versions:

  - Middleware: amq-streams - Built-in version: 2.9.x

  - Middleware: Kafka - Built-in version: 3.9.0

  - Middleware: PostgreSQL - Built-in version: 16

  - Middleware: Grafana - Built-in version: 11.1.0

## Installing multicluster global hub in a connected environment

The multicluster global hub is installed through Operator Lifecycle
Manager, which manages the installation, upgrade, and removal of the
components that comprise the operator.

**Required access:** Cluster administrator

### Prerequisites

- For the OpenShift Container Platform Dedicated environment, you must
  have `cluster-admin` permissions to access the environment. By default
  `dedicated-admin` role does not have the required permissions to
  create namespaces in the OpenShift Container Platform Dedicated
  environment.

- You must install and configure Red Hat Advanced Cluster Management for
  Kubernetes. For more details, see Installing and upgrading.

- You must configure the Red Hat Advanced Cluster Management network.
  The managed hub cluster is also a managed cluster of multicluster
  global hub in Red Hat Advanced Cluster Management. For more details,
  see Hub cluster network configuration.

#### Installing multicluster global hub by using the console

To install the multicluster global hub operator in a connected
environment by using the OpenShift Container Platform console, complete
the following steps:

1.  Log in to the OpenShift Container Platform console as a user with
    the `cluster-admin` role.

2.  From the navigation menu, select **Operators** \> the
    **OperatorHub** icon.

3.  Locate and select the **Multicluster global hub operator**.

4.  Click **Install** to start the installation.

5.  After the installation completes, check the status on the *Installed
    Operators* page.

6.  Click **Multicluster global hub operator** to go to the *Operator*
    page.

7.  Click the **Multicluster global hub** tab to see the
    `Multicluster Global Hub` instance.

8.  Click **Create Multicluster Global Hub** to create the
    `Multicluster Global Hub` instance.

9.  Enter the required information and click **Create** to create the
    `Multicluster Global Hub` instance.

## Installing multicluster global hub in a disconnected environment

If your cluster is in a restricted network, you can deploy the
multicluster global hub operator in the disconnected environment.

**Required access:** Cluster administrator

### Prerequisites

You must meet the following requirements before you install multicluster
global hub in a disconnected environment:

- An image registry and a bastion host must have access to both the
  internet and to your mirror registry.

- Install the Operator Lifecycle Manager on your cluster. See Operator
  Lifecycle Manager (OLM).

- Install Red Hat Advanced Cluster Management for Kubernetes.

- 

### Configuring a mirror registry

Installing multicluster global hub in a disconnected environment
involves the use of a local mirror image registry. At this point, it is
assumed that you have set up a mirror registry during the OpenShift
Container Platform cluster installation.

Complete the following procedures to provision the mirror registry for
multicluster global hub:

#### Creating operator packages in mirror catalog with oc-mirror plug-in

Red Hat provides the multicluster global hub and AMQ Streams operators
in the Red Hat operators catalog, which are delivered by the
`registry.redhat.io/redhat/redhat-operator-index` index image. When you
prepare your mirror of this catalog index image, you can choose to
either mirror the entire catalog as provided by Red Hat, or you can
mirror a subset that contains only the operator packages that you intend
to use.

If you are creating a full mirror catalog, no special considerations are
needed as all of the packages required to install multicluster global
hub and AMQ Streams are included. However, if you are creating a partial
or filtered mirrored catalog, for which you identify particular packages
to be included, you must to include the
`multicluster-global-hub-operator-rh` and `amq-streams` package names in
your list.

Complete the following steps to create a local mirror registry of the
`multicluster-global-hub-operator-rh` and `amq-streams` packages:

1.  Create a `ImageSetConfiguration` YAML file to configure and add the
    operator image. Your YAML file might resemble the following content,
    with the current version replacing `4.x`:

    ``` yaml
    kind: ImageSetConfiguration
    apiVersion: mirror.openshift.io/v1alpha2
    storageConfig:
      registry:
          imageURL: myregistry.example.com:5000/mirror/oc-mirror-metadata
    mirror:
      platform:
        channels:
        - name: stable-4.x
          type: ocp
      operators:
      - catalog: registry.redhat.io/redhat/redhat-operator-index:v4.x
        packages:
        - name: multicluster-global-hub-operator-rh
        - name: amq-streams
      additionalImages: []
      helm: {}
    ```

2.  Mirror the image set directly to the target mirror registry by using
    the following command:

    ``` bash
    oc mirror --config=./imageset-config.yaml docker://myregistry.example.com:5000
    ```

3.  Mirror the image set in a fully disconnected environment. For more
    details, see Mirroring images for a disconnected installation.

#### Adding the registry and catalog to your disconnected cluster

To make your mirror registry and catalog available on your disconnected
cluster. Complete the following steps:

1.  Disable the default catalog sources of Operator Hub. Run the
    following command to update the `OperatorHub` resource:

    ``` bash
    oc patch OperatorHub cluster --type json \
    -p '[{"op": "add", "path": "/spec/disableAllDefaultSources", "value": true}]'
    ```

2.  Mirror the Operator catalog by completing the procedure, Mirroring
    the Operator catalog.

3.  Add the `CatalogSource` resource for your mirrored catalog into the
    `openshift-marketplace` namespace. Your `CatalogSource` YAML file
    might be similar to the following example, with `4.x` set as the
    supported version:

    ``` yaml
    apiVersion: operators.coreos.com/v1alpha1
    kind: CatalogSource
    metadata:
      name: my-mirror-catalog-source
      namespace: openshift-marketplace
    spec:
      image: myregistry.example.com:5000/mirror/my-operator-index:v4.x
      sourceType: grpc
      secrets:
      - <global-hub-secret>
    ```

    - **Note:** Take note of the value of the `metadata.name` field.

4.  Save the updated file.

5.  Query the available `PackageManifest` resource to verify that the
    required packages are available from your disconnected cluster. Run
    the following command:

    ``` bash
    oc -n openshift-marketplace get packagemanifests
    ```

6.  Verify that the displayed list includes entries showing the
    `multicluster-global-hub-operator-rh` and `amq-streams` packages.
    Verify that the catalog source for your mirror catalog supplies
    these packages.

7.  To change the build in the `amq-strimzi` catalog source, create a
    multicluster global hub annotation. Apply the following YAML:

    ``` yaml
    apiVersion: operator.open-cluster-management.io/v1alpha4
    kind: MulticlusterGlobalHub
    metadata:
      annotations:
        global-hub.open-cluster-management.io/strimzi-catalog-source-name: redhat-operators
        global-hub.open-cluster-management.io/strimzi-catalog-source-namespace: openshift-marketplace
        global-hub.open-cluster-management.io/strimzi-subscription-package-name: amq-streams
        global-hub.open-cluster-management.io/strimzi-subscription-channel: amq-streams-2.9.x
      name: multiclusterglobalhub
    spec:
      ......
    ```

### Configuring the image registry

In order to have your cluster obtain container images for the
multicluster global hub operator from your local mirror registry, rather
than from the internet-hosted registries, you must configure an
`ImageContentSourcePolicy` resource on your disconnected cluster to
redirect image references to your mirror registry. The
`ImageContentSourcePolicy` only support the image mirror with image
**digest**.

If you mirrored your catalog using the `oc adm catalog mirror` command,
the needed image content source policy configuration is in the
`imageContentSourcePolicy.yaml` file inside the `manifests-` directory
that is created by that command.

If you used the `oc-mirror` plug-in to mirror your catalog instead, the
`imageContentSourcePolicy.yaml` file is within the
`oc-mirror-workspace/results-` directory created by the `oc-mirror`
plug-in.

In either case, you can apply the policies to your disconnected command
using an `oc apply` or `oc replace` command such as
`oc replace -f ./<path>/imageContentSourcePolicy.yaml`

The required image content source policy statements can vary based on
how you created your mirror registry, but are similar to this example:

``` yaml
apiVersion: operator.openshift.io/v1alpha1
kind: ImageContentSourcePolicy
metadata:
  labels:
    operators.openshift.org/catalog: "true"
  name: global-hub-operator-icsp
spec:
  repositoryDigestMirrors:
  - mirrors:
    - myregistry.example.com:5000/multicluster-globalhub
    source: registry.redhat.io/multicluster-globalhub
  - mirrors:
    - myregistry.example.com:5000/openshift4
    source: registry.redhat.io/openshift4
  - mirrors:
    - myregistry.example.com:5000/redhat
    source: registry.redhat.io/redhat
  - mirrors:
    - myregistry.example.com:5000/rhel9
    source: registry.redhat.io/rhel9
  - mirrors:
    - myregistry.example.com:5000/amq-streams
    source: registry.redhat.io/amq-streams
```

You can configure different image registries for different managed hubs
with the `ManagedClusterImageRegistry`. See Importing a cluster that has
a ManagedClusterImageRegistry to use the `ManagedClusterImageRegistry`
API to replace the agent image.

By completing the previous step, a label and an annotation are added to
the selected `ManagedCluster`. This means that the agent image in the
cluster are replaced with the mirror image.

- Label:
  `multicluster-global-hub.io/image-registry=<namespace.managedclusterimageregistry-name>`

- Annotation:
  `multicluster-global-hub.io/image-registries: <image-registry-info>`

#### Configure the image pull secret

If the Operator or Operand images that are referenced by a subscribed
Operator require access to a private registry, you can either provide
access to all namespaces in the cluster, or to individual target tenant
namespaces.

##### Configure the multicluster global hub image pull secret in an OpenShift Container Platform cluster

You can configure the image pull secret in an existing OpenShift
Container Platform cluster.

**Note:** Applying the image pull secret on a pre-existing cluster
causes a rolling restart of all of the nodes.

Complete the following steps to configure the pull secret:

1.  Export the user name from the pull secret:

        export USER=<the-registry-user>

2.  Export the password from the pull secret:

        export PASSWORD=<the-registry-password>

3.  Copy the pull secret:

        oc get secret/pull-secret -n openshift-config --template='{{index .data ".dockerconfigjson" | base64decode}}' > pull_secret.yaml

4.  Log in using the pull secret:

        oc registry login --registry=${REGISTRY} --auth-basic="$USER:$PASSWORD" --to=pull_secret.yaml

5.  Specify the multicluster global hub image pull secret:

        oc set data secret/pull-secret -n openshift-config --from-file=.dockerconfigjson=pull_secret.yaml

6.  Remove the old pull secret:

        rm pull_secret.yaml

##### Configure the multicluster global hub image pull secret to an individual namespace

You can configure the image pull secret to an individual namespace by
completing the following steps:

1.  Create the secret in the tenant namespace by running the following
    command:

    ``` shell
    oc create secret generic <secret_name> -n <tenant_namespace> \
    --from-file=.dockerconfigjson=<path/to/registry/credentials> \
    --type=kubernetes.io/dockerconfigjson
    ```

2.  Link the secret to the service account for your operator or operand:

    ``` shell
    oc secrets link <operator_sa> -n <tenant_namespace> <secret_name> --for=pull
    ```

#### Installing the Global Hub Operator

You can install and subscribe an Operator from the Red Hat OpenShift
Software Catalog. See Adding Operators to a cluster for the procedure.
After adding the Operator, you can check the status of the multicluster
global hub Operator by running the following command:

``` bash
oc get pods -n multicluster-global-hub
NAME                                                READY   STATUS    RESTARTS   AGE
multicluster-global-hub-operator-687584cb7c-fnftj   1/1     Running   0          2m12s
```

## Installing multicluster global hub on an existing Red Hat Advanced Cluster Management hub cluster

You can install multicluster global hub in an existing Red Hat Advanced
Cluster Management hub cluster and enable the multicluster global hub
agent in Red Hat Advanced Cluster Management. Learn about the following
capabilities:

- When you install multicluster global hub in an Red Hat Advanced
  Cluster Management hub cluster, Kafka receives the information from
  the multicluster global hub operator and stores it in the multicluster
  global hub database, giving you access to the clusters, policies, and
  events.

- Kafka stores the multicluster global hub operator information, so as a
  Kafka consumer, you can access other components. For example, you can
  integrate with Red Hat Advanced Cluster Security and Red Hat
  Event-Driven Ansible.

- Your data is stored in the multicluster global hub database so you can
  view the cluster and policy information in the Grafana dashboards.

To install multicluster global hub on an existing Red Hat Advanced
Cluster Management hub cluster, you must set the `installAgentOnLocal`
field to `true` by applying the following YAML sample:

``` yaml
apiVersion: operator.open-cluster-management.io/v1alpha4
kind: MulticlusterGlobalHub
metadata:
  name: multiclusterglobalhub
  namespace: multicluster-global-hub
spec:
  enableMetrics: true
  installAgentOnLocal: true  
  dataLayer:
    kafka:
      topics:
        specTopic: gh-spec 
        statusTopic: gh-status 
      consumerGroupPrefix: org1_  
    postgres:
      retention: 18m
  availabilityConfig: High 
```

- `installAgentOnLocal`: Deploys multicluster global hub on the
  multicluster global hub cluster. If you set the value to `true`, the
  multicluster global hub operator installs the agent on the
  multicluster global hub cluster.

- `specTopic`: Distributes workloads from multicluster global hub to
  managed hub clusters. The default value is `gh-spec`.

- `statusTopic`: Reports events and status updates to the multicluster
  global hub manager. When a topic ends with an asterisk, the topic is
  intended for the individual managed hub clusters. The default value
  for all managed hub clusters is `gh-status`.

- `consumerGroupPrefix`: Specifies the prefix for Kafka consumer groups.
  The final consumer group identification for multicluster global hub is
  `<prefix> + "global_hub"`, and for managed hub clusters it is
  `<prefix> + <managed-hub-name>`. In the final group identification,
  all hyphens, get changed to underscores. If you do not specify a
  value, the default consumer group is the name of the hubs without any
  prefix.

- `availabilityConfig`: Specifies the replication of deployments to
  improve their availability. For the values of the replications, you
  have the options of `Basic` and `High`. For the `High` value, the
  `availabilityConfig` creates one replica for the multicluster global
  hub manager and Grafana. It creates two replicas for the Kafka broker,
  which is a separate component in multicluster global hub. The default
  value is `High`.

**Note:** If you enabled the `MultiClusterObservability` custom resource
in the Red Hat Advanced Cluster Management after you installed
multicluster global hub, then any new update for the
`MultiClusterObservability` custom resource does not take effect.

## Integrating existing components

The multicluster global hub requires middleware components, Kafka and
PostgreSQL, along with Grafana as the Observability platform to provide
the policy compliance view. The multicluster global hub provides
versions of Kafka, PostgreSQL, and Grafana. You can also integrate your
own existing Kafka, PostgreSQL, and Grafana.

### Integrating an existing version of Kafka

If you have your own instance of Kafka, you can use it as the transport
for multicluster global hub. Complete the following steps to integrate
an instance of Kafka:

1.  If you do not have a persistent volume for your Kafka instance, you
    need to create one.

2.  Create a secret named `multicluster-global-hub-transport` in the
    `multicluster-global-hub` namespace.

    1.  Extract the information in the following required fields:

        - `bootstrap.servers`: Specifies the Kafka bootstrap servers.

        - `ca.crt`: Required if you use the `KafkaUser` custom resource
          to configure authentication credentials. See the *User
          authentication* topic in the STRIMZI documentation for the
          required steps to extract the `ca.crt` certificate from the
          secret.

        - `client.crt`: Required, see the *User authentication* topic in
          the STRIMZI documentation for the steps to extract the
          `user.crt` certificate from the secret.

        - `client.key`: Required, see the *User authentication* topic in
          the STRIMZI documentation for the steps to extract the
          `user.key` from the secret.

3.  Create the secret by running the following command, replacing the
    values with your extracted values where necessary:

    ``` bash
    oc create secret generic multicluster-global-hub-transport -n multicluster-global-hub \
        --from-literal=bootstrap_server=<kafka-bootstrap-server-address> \
        --from-file=ca.crt=<CA-cert-for-kafka-server> \
        --from-file=client.crt=<Client-cert-for-kafka-server> \
        --from-file=client.key=<Client-key-for-kafka-server>
    ```

4.  If automatic topic creation is configured on your Kafka instance,
    then skip this step. If it is not configured, create the `spec` and
    `status` topics manually.

5.  Ensure that the global hub user that accesses Kafka has the
    permission to read data from the topics and write data to the
    topics.

### Integrating an existing version of PostgreSQL

If you have your own PostgreSQL relational database, you can use it as
the storage for multicluster global hub.

The minimum required storage size is 20GB. This amount can store 3
managed hubs with 250 managed clusters and 50 policies per managed hub
for 18 months. You need to create a secret named
`multicluster-global-hub-storage` in the `multicluster-global-hub`
namespace. The secret must contain the following fields:

- `database_uri`: It is used to create the database and insert data.
  Your value must resemble the following format:
  `postgres://<user>:<password>@<host>:<port>/<database>?sslmode=<mode>`.

- `database_uri_with_readonlyuser`: It is used to query data by the
  instance of Grafana that is used by multicluster global hub. It is an
  optional value. Your value must resemble the following format:
  `postgres://<user>:<password>@<host>:<port>/<database>?sslmode=<mode>`.

- The `ca.crt`, which is based on the `sslmode`, is an optional value.

  1.  Verify that your cluster has the minimum required storage size of
      20GB. This amount can store three managed hubs with 250 managed
      clusters and 50 policies per managed hub for 18 months.

  2.  Create the secret by running the following command:

  ``` bash
  oc create secret generic multicluster-global-hub-storage -n multicluster-global-hub \
      --from-literal=database_uri=<postgresql-uri> \
      --from-literal=database_uri_with_readonlyuser=<postgresql-uri-with-readonlyuser> \
      --from-file=ca.crt=<CA-for-postgres-server>
  ```

The host must be accessible from the multicluster global hub cluster. If
your PostgreSQL database is in a Kubernetes cluster, you can consider
using the service type with `nodePort` or `LoadBalancer` to expose the
database. For more information, see Accessing the provisioned postgres
database for troubleshooting.

### Integrating an existing version of Grafana

Using an existing Grafana instance might work with multicluster global
hub if you are relying on your own Grafana to get metrics from multiple
sources, such as Prometheus, from different clusters and if you
aggregate the metrics yourself. To get multicluster global hub data into
your own Grafana, you need to configure the data source and import the
dashboards.

1.  Collect the PostgreSQL connection information from the multicluster
    global hub Grafana `datasource` secret by running the following
    command:

    ``` bash
    oc get secret multicluster-global-hub-grafana-datasources -n multicluster-global-hub -ojsonpath='{.data.datasources\.yaml}' | base64 -d
    ```

    The output resembles the following example:

    ``` yaml
    apiVersion: 1
    datasources:
    - access: proxy
      isDefault: true
      name: Global-Hub-DataSource
      type: postgres
      url: postgres-primary.multicluster-global-hub.svc:5432
      database: hoh
      user: guest
      jsonData:
        sslmode: verify-ca
        tlsAuth: true
        tlsAuthWithCACert: true
        tlsConfigurationMethod: file-content
        tlsSkipVerify: true
        queryTimeout: 300s
        timeInterval: 30s
      secureJsonData:
        password: xxxxx
        tlsCACert: xxxxx
    ```

2.  Configure the `datasource` in your own Grafana instance by adding a
    source, such as PostgreSQL, and complete the required fields with
    the information you previously extracted.

    See the following required fields:

    - Name

    - Host

    - Database

    - User

    - Password

    - TLS/SSL Mode

    - TLS/SSL Method

    - CA Cert

3.  If your Grafana is not in the multicluster global hub cluster, you
    need to expose the PostgreSQL by using the `LoadBalancer` so the
    PostgreSQL can be accessed from outside. You can add the following
    value into the `PostgresCluster` operand:

    ``` yaml
    service:
      type: LoadBalancer
    ```

    After you add that content, then you can get the `EXTERNAL-IP` from
    the `postgres-ha` service. See the following example:

    ``` bash
    oc get svc postgres-ha -n multicluster-global-hub
    NAME          TYPE           CLUSTER-IP      EXTERNAL-IP                        PORT(S)          AGE
    postgres-ha   LoadBalancer   172.30.227.58   xxxx.us-east-1.elb.amazonaws.com   5432:31442/TCP   128m
    ```

    After running that command, you can use
    `xxxx.us-east-1.elb.amazonaws.com:5432` as the PostgreSQL Connection
    Host.

4.  Import the existing dashboards.

    1.  Follow the steps in Export and import dashboards in the official
        Grafana documentation to export the dashboard from the existing
        Grafana instance.

    2.  Follow the steps in Export and import dashboards in the official
        Grafana documentation to import a dashboard into the
        multicluster global hub Grafana instance.

### Additional resources

See User authentication in the STRIMZI documentation for more
information about how to extract the `ca.crt` certificate from the
secret.

See User authentication in the STRIMZI documentation for the steps to
extract the `user.crt` certificate from the secret.

## Importing a managed hub cluster in the default mode

Import an existing hub cluster as a managed hub cluster to help you
control your different environments when you develop and deploy your
applications.

### Prerequisites

1.  Disable the cluster self-management setting in the existing hub
    cluster by setting the `disableHubSelfManagement` setting to `true`
    in the `multiclusterhub` custom resource. This setting disables the
    automatic import of the hub cluster as a managed cluster.

2.  Import the managed hub cluster by completing the steps in Cluster
    import introduction.

### Importing a managed hub cluster

To import an existing hub cluster as a managed hub cluster, complete the
following steps:

1.  Set the label
    `global-hub.open-cluster-management.io/deploy-mode=default` to the
    `managedcluster` when you import the managed hub cluster.

2.  Check the multicluster global hub agent status to ensure that the
    agent is running in the managed hub cluster. Run the following
    command:

        oc get managedclusteraddon multicluster-global-hub-controller -n <managed_hub_cluster_name>

**Note:** If you upgrade multicluster global hub, you must manually add
the label `global-hub.open-cluster-management.io/deploy-mode=default` to
all the managed hub clusters.

## Importing a managed hub cluster in the hosted mode

To enable `local-cluster` on your managed hub cluster, you must import
it in the hosted mode.

### Prerequisites

- Enable the `local-cluster` in the multicluster global hub cluster.

- Install the latest Red Hat Advanced Cluster Management version.

- Make sure this `kubeconfig` file is always usable. If it expires,
  regenerate the `auto-import-secret` in the managed hub cluster
  namespace with the following command:

      oc create secret generic auto-import-secret --from-file=kubeconfig=./managedClusterKubeconfig -n <Managedhub Namespace>

### Importing a managed hub cluster in the hosted mode

When you import an existing managed hub cluster in the hosted mode, you
only get support for imported managed hub clusters that use a
`kubeconfig` file. Red Hat Advanced Cluster Management for Kubernetes
uses this `kubeconfig` file to generate the `auto-import-secret` which
connects to your managed hub cluster. In the hosted mode, multicluster
global hub does not support backup and restore.

Import your managed hub cluster by setting the label
`global-hub.open-cluster-management.io/deploy-mode=hosted` to
`managedcluster`.

With this label, multicluster global hub does the following actions:

- Imports the new managed hub cluster in the hosted mode.

- Installs the multicluster global hub agent in the new managed hub
  cluster that uses the hosted mode.

- Disables the following `addons` in the new managed hub cluster
  namespaces: `applicationManager`, `certPolicyController`, and
  `policyController`.

- Changes the following managed hub clusters `addons` that are related
  to the new namespace: `work-manager`,`cluster-proxy`, and
  `managed-serviceaccount`.

- Changes these namespaces to
  `open-cluster-management-global-hub-agent-addon`.

## Accessing the Grafana data

The Grafana data is exposed through the route. Run the following command
to display the login URL:

    oc get route multicluster-global-hub-grafana -n <the-namespace-of-multicluster-global-hub-instance>

The authentication method of this URL is same as authenticating to the
Red Hat OpenShift Container Platform console.

### Viewing policy status with Grafana dashboards

After accessing the global hub Grafana data, you can monitor the
policies that were configured through the hub cluster environments that
are managed.

From the multicluster global hub dashboard, you can identify the
compliance status of the policies of the system over a selected time
range. The policy compliance status is updated daily, so the dashboard
does not display the status of the current day until the following day.

To navigate the multicluster global hub dashboards, you can observe and
filter the policy data by grouping them by `policy` or by `cluster`.

If you prefer to examine the policy data by using the `policy` grouping,
start from the and the dashboard called
`Global Hub - Policy Group Compliancy Overview`.

This dashboard allows you to filter the policy data based on `standard`,
`category`, and `control`. After selecting a specific point in time on
the graph, you are directed to the `Global Hub - Offending Policies`
dashboard. The `Global Hub - Offending Policies` dashboard lists the
non-compliant or unknown policies at that time. After selecting a target
policy, you can view related events and see what has changed by
accessing the `Global Hub - What’s Changed / Policies` dashboard.

Similarly, if you want to examine the policy data by `cluster` grouping,
begin by using the `Global Hub - Cluster Group Compliancy Overview`
dashboard. The navigation flow is identical to the `policy` grouping
flow, but you select filters that are related to the cluster, such as
managed cluster `labels` and `values`. Instead of viewing policy events
for all clusters, after reaching the
`Global Hub - What’s Changed / Clusters` dashboard, you can view policy
events related to an individual cluster.

### Viewing Strimzi information with Grafana dashboards

To understand the health and performance of your Kafka deployment and
Postgres database, collect their metrics. When you check the metrics,
you can identify issues before they become critical and make informed
decisions about resource allocation and capacity planning. If you do not
collect and check the metrics, you might have limited visibility into
the behavior of your Kafka deployment, making troubleshooting more
difficult.

You can check the dashboards and their metrics in the multicluster
global hub Grafana. In the Strimzi folder, you can view the following
dashboards:

- multicluster global hub - Strimzi Operator

- multicluster global hub - Strimzi Kafka

- multicluster global hub - Strimzi Kraft

### Viewing Postgres information with Grafana dashboards (Technology Preview)

To understand the health and performance of your Postgres config,
collect and check the Postgres metrics in the Grafana dashboard. In the
Postgres folder, you can view the following dashboard:

- multicluster global hub - PostgresSQL Database

### Viewing cluster information with Grafana dashboards

To filter your managed clusters and to view their details and events,
use the Grafana dashboards. With the Grafana dashboard, you can filter
your managed clusters based on: `hub`, `labels` and `name`.
Additionally, you can view the distribution of your managed clusters
based on: `hub`, `status`, `cloud`, and `version`.

In the Cluster folder, you can view the following dashboard:

- multicluster global hub - Cluster Overview

## Grafana alerts (Technology Preview)

You can configure three Grafana alerts, which are stored in the
`multicluster-global-hub-default-alerting` config map. These alerts
notify you of suspicious policies, suspicious clusters compliance status
change, and failed cron jobs.

See the following descriptions of the alerts:

- Suspicious policy change: This alert rule watches the suspicious
  policies change. If the following events occur more than five times in
  one hour, it creates notifications.

  - A policy was enabled or disabled.

  - A policy was updated.

- Suspicious cluster compliance status change: This alert rule watches
  the cluster compliance status and policy events for a cluster. There
  are two rules in this alert:

  - Cluster compliance status changes frequently: If a cluster
    compliance status changes from `compliance` to `non-compliance` more
    than three times in one hour, it creates notifications.

  - Too many policy events in a cluster: For a policy in a cluster, if
    there are more than 20 events in five minutes, it creates
    notifications. If this alert is always firing, the data in the
    `event.local_policies` table increases too fast.

- Cron Job failed: This alert watches the cron jobs that are described
  in Configuring the cron jobs for failed events. There are two rules in
  this alert:

  - Local compliance job failed: If this alert rule creates
    notifications, it means the local compliance status synchronization
    job failed. It might cause the data in the
    `history.local_compliance` table to be lost. Run the job manually,
    if necessary.

  - Data retention job failed: If this alert rule starts creating
    notifications, it means the data retention job failed. You can run
    it manually.

### Deleting a default Grafana alert rule

If the default Grafana alert rules do not provide useful information,
you can delete the Grafana alert rule by including a `deleteRules`
section in the `multicluster-global-hub-custom-alerting` config map. See
Customize Grafana alerting resources for more information about the
`multicluster-global-hub-custom-alerting` config map.

To delete all of the default alerts, the `deleteRules` configuration
section should resemble the following example:

        deleteRules:
          - orgId: 1
            uid: globalhub_suspicious_policy_change
          - orgId: 1
            uid: globalhub_cluster_compliance_status_change_frequently
          - orgId: 1
            uid: globalhub_high_number_of_policy_events
          - orgId: 1
            uid: globalhub_data_retention_job
          - orgId: 1
            uid: globalhub_local_compliance_job

### Customizing Grafana alerts

The multicluster global hub supports creating custom Grafana alerts.
Complete the following steps to customize your Grafana alerts:

#### Customizing your grafana.ini file

To customize your `grafana.ini` file, create a secret named
`multicluster-global-hub-custom-grafana-config` in the namespace where
you installed your multicluster global hub operator. The secret data key
is `grafana.ini`, as seen in the following example. Replace the required
information with your own credentials:

``` yaml
apiVersion: v1
kind: Secret
metadata:
  name: multicluster-global-hub-custom-grafana-config
  namespace: multicluster-global-hub
type: Opaque
stringData:
  grafana.ini: |
    [smtp]
    enabled = true
    host = smtp.google.com:465
    user = <example@google.com>
    password = <password>
    ;cert_file =
    ;key_file =
    skip_verify = true
    from_address = <example@google.com>
    from_name = Grafana
    ;ehlo_identity = dashboard.example.com 
```

\<1\>The `EHLO` identity in the `SMTP` dialog, which defaults to
`instance_name`.

**Note:** You cannot configure the section that already contains the
`multicluster-global-hub-default-grafana-config` secret.

#### Customizing Grafana alerting resources

The multicluster global hub supports customizing the alerting resources,
which is explained in Create and manage alerting resources using file
provisioning in the Grafana documentation.

To customize the alerting resources, create a config map named
`multicluster-global-hub-custom-alerting` in the
`multicluster-global-hub` namespace.

The config map data key is `alerting.yaml`, as in the following example:

``` yaml
apiVersion: v1
data:
  alerting.yaml: |
    contactPoints:
      - orgId: 1
        name: globalhub_policy
        receivers:
          - uid: globalhub_policy_alert_email
            type: email
            settings:
              addresses: <example@redhat.com>
              singleEmail: false
          - uid: globalhub_policy_alert_slack
            type: slack
            settings:
              url: <Slack-webhook-URL>
              title: |
                {{ template "globalhub.policy.title" . }}
              text: |
                {{ template "globalhub.policy.message" . }}
    policies:
      - orgId: 1
        receiver: globalhub_policy
        group_by: ['grafana_folder', 'alertname']
        matchers:
          - grafana_folder = Policy
        repeat_interval: 1d
    deleteRules:
      - orgId: 1
        uid: [Alert Rule Uid]
    muteTimes:
      - orgId: 1
        name: mti_1
        time_intervals:
          - times:
              - start_time: '06:00'
                end_time: '23:59'
                location: 'UTC'
            weekdays: ['monday:wednesday', 'saturday', 'sunday']
            months: ['1:3', 'may:august', 'december']
            years: ['2020:2022', '2030']
            days_of_month: ['1:5', '-3:-1']
kind: ConfigMap
metadata:
  name: multicluster-global-hub-custom-alerting
  namespace: multicluster-global-hub
```

## Configuring the cron jobs

You can configure the cron job settings of the multicluster global hub.

After you install the multicluster global hub operand, the multicluster
global hub manager runs and displays a job scheduler for you to schedule
the following cron jobs:

- **Local compliance status sync job:** This cron job runs at midnight
  every day based on the policy status and events collected by the
  manager on the previous day. Run this job to summarize the compliance
  status and the change frequency of the policy on the cluster, and
  store them to the `history.local_compliance` table as the data source
  of the Grafana dashboards.

- **Data retention job:** Some data tables in multicluster global hub
  continue to grow over time, which normally can cause problems when the
  tables get too large. The following two actions help to minimize the
  issues that result from tables that are too large:

  1.  Delete older data that is no longer needed.

  2.  Enable partitioning on the large table to run queries and
      deletions on faster.

      For event tables, such as the `event.local_policies` and the
      `history.local_compliance` that increase in size daily, range
      partitioning divides the large tables into smaller partitions.
      This process also creates the partition tables for the next month
      each time it is run.

      For the policy and cluster tables, such as `local_spec.policies`
      and `status.managed_clusters`, the `deleted_at` indexes on the
      tables to improve performance when you delete.

  You can change the duration of time that the data is retained by
  changing the `retention` setting on the multicluster global hub
  operand. The recommended minimum value is `1 month`, and the default
  value is `18 months`. The run interval of this job should be less than
  one month.

The listed cron jobs run every time the multicluster global hub manager
starts. The local compliance status sync job is run once a day and can
be run multiple times within the day without changing the result.

The data retention job is run once a week and also can be run many times
per month without a change in the results.

The status of these jobs are are saved in the
`multicluster_global_hub_jobs_status` metrics, which can be viewed from
the console of the Red Hat OpenShift Container Platform cluster. A value
of `0` indicates that the job ran successfully, while a value of `1`
indicates failure.

## Running the summarization process manually

You can manually run the summarization process to restore the initial
compliance state of the day when the job is not triggered or has not
failed running. To manually run the summarization process, complete the
following steps:

1.  Use the earlier day’s compliance history as the initial state for
    the recovery day’s history.

2.  Connect to the database.

    You can use clients such as `pgAdmin` and `tablePlush` to connect to
    the multicluster global hub database. Or, you can directly connect
    to the database on the cluster by running the following command:

        oc exec -it multicluster-global-hub-postgresql-0 -n multicluster-global-hub -- psql -d hoh

3.  Decide the date when you want the summarization process to run, for
    example: `2023-07-06`

    Find the local compliance job failure information from the dashboard
    metrics or the `history.local_compliance_job_log` table. In this
    example, the date is, `2023-07-06`, so you know that `2023-07-06` is
    the date when you need to manually run the summary processes.

4.  Recover the initial compliance of `2023-07-06` by running the
    following SQL:

        -- call the func to generate the initial data of '2023-07-06' by inheriting '2023-07-05'
        CALL history.generate_local_compliance('2024-07-06');

## Backup for multicluster global hub (Technology Preview)

Use multicluster global hub with Red Hat Advanced Cluster Management
backup and restore features for recovery solutions and to access basic
resources. To learn more about how these features help you, see backup
and restore.

multicluster global hub also supports backup `postgres pvc` by using the
`acm-hub-pvc-backup`. To ensure your multicluster global hub can support
the backup `postgres pvc`, you must have the current version of VolySync
and Red Hat Advanced Cluster Management. For detailed steps on backing
up your data, see acm-hub-pvc-backup.

### Restoring multicluster global hub backup and restore

If you need to restore your multicluster global hub cluster, see prepare
the new hub cluster. Install the multicluster global hub operator but do
not create the multicluster global hub custom resource (CR) because the
CR is automatically restored.

## multicluster global hub search (Technology Preview)

Global search expands the search capabilities when you use multicluster
global hub to manage your environment.

### Prerequisites

You need to enable multicluster global hub.

### Enabling global search

To enable global search, add the `global-search-preview=true` annotation
to the `search-v2-operator` resource by running the following command:

``` bash
oc annotate search search-v2-operator -n open-cluster-management global-search-preview=true
```

The search operator is updated with the following status condition:

``` yaml
status:
  conditions:
    - lastTransitionTime: '2024-05-31T19:49:37Z'
      message: None
      reason: None
      status: 'True'
      type: GlobalSearchReady
```

## Migrating managed clusters

**Technology Preview:** You can access the Managed Cluster Migration
feature in multicluster global hub 1.5. You can migrate managed clusters
from one Red Hat Advanced Cluster Management hub cluster to another and
across versions, for example, from Red Hat Advanced Cluster Management
2.13 to Red Hat Advanced Cluster Management 2.14.

By using multicluster global hub to migrate your managed cluster, you
have a unified process that helps you perform the following actions:

- Reorganize workloads among Red Hat Advanced Cluster Management hub
  clusters

- Move clusters and their resources together

- Automate cluster registration and cleanup

- Tracks individual steps with detailed status updates

To fully migrate your managed clusters, complete the following sections:

1.  Prerequisites

2.  Managed cluster migration process

3.  Preparing the migration environment

4.  Migrating managed clusters

5.  Tracking the migration status

### Prerequisites

To migrate your managed clusters, you need the following components:

- The multicluster global hub operator to organize the migration
  workflow.

- The `source` Red Hat Advanced Cluster Management hub cluster to manage
  the clusters and the associated resources.

- The `target` Red Hat Advanced Cluster Management hub cluster to
  receive the migrated clusters and the associated resources.

### Managed cluster migration process

With multicluster global hub, you can manage large fleets of clusters by
implementing the event-driven architecture of multicluster global hub.
multicluster global hub connects itself to your managed hub clusters.
With the multicluster global hub event-based design, you can enable
multicluster global hub to communicate, organize, synchronize, and
transfer resources and cluster states among all you hub clusters.

The manage cluster migration process requires coordination between a
`source` and `target` Red Hat Advanced Cluster Management hub cluster.
The `multicluster-global-hub-agent` performs the migrations tasks on the
`source` and `target` hub clusters. The
`multicluster-global-hub-manager` controls the flow of the migration
between the `source` and `target` hub clusters and manages the
`ManagedClusterMigration` resources.

During the managed cluster migration, the `source` and `target` hub
clusters go through different phases. These phases and their conditions
help track the status changes of the hub clusters throughout the
migration process. See the following table for an outline of each phase
and its condition:

- Phase: Pending - Condition: Performs one migration at a time. Other
  migrations remain Pending.

- Phase: Validating - Condition: Verifies that the clusters and hub
  clusters are valid.

- Phase: Initializing - Condition: Prepares the target and source hub
  cluster.

- Phase: Deploying - Condition: Migrates selected clusters and their
  resources.

- Phase: Registering - Condition: Restarts the registration of the
  cluster to the target hub cluster.

- Phase: Cleaning - Condition: Cleans the resources from both target and
  source hub cluster and manages the rollback if needed.

- Phase: Completed - Condition: Confirms the migrations are successfully
  completed.

- Phase: Failed - Condition: Confirms that the migration has failed and
  includes this failure message in the status.

See the following table for the supported versions and the corresponding
multicluster global hub `source`, and `target` hub versions:

- multicluster global hub version for migration: multicluster global hub
  1.5 - source hub version: Red Hat Advanced Cluster Management 2.14 -
  target hub version: Red Hat Advanced Cluster Management 2.14

- multicluster global hub version for migration: multicluster global hub
  1.5 - source hub version: Red Hat Advanced Cluster Management 2.13 -
  target hub version: Red Hat Advanced Cluster Management 2.14

### Preparing the migration environment

To prepare your multicluster global hub environment for migration, you
can create a Brownfield environment by deploying the multicluster global
hub control plane directly into the `source` hub cluster. Then, you can
import the `target` hub cluster into the multicluster global hub
environment that is in the `Hosted` mode.

Complete the following steps:

1.  Install the multicluster global hub operator in the `source` Red Hat
    Advanced Cluster Management hub cluster.

2.  Enable the `local-cluster` in the multicluster global hub custom
    operator that is running in the `source` hub cluster.

3.  Apply the following YAML to create the multicluster global hub
    operand and enable the multicluster global hub agent to run locally:

    ``` yaml
    apiVersion: operator.open-cluster-management.io/v1alpha4
    kind: MulticlusterGlobalHub
    metadata:
      name: multiclusterglobalhub
      namespace: multicluster-global-hub
    spec:
      availabilityConfig: High
      installAgentOnLocal: true
    ```

4.  Import the target hub cluster into multicluster global hub that is
    in the `Hosted` mode. Add the following label to the managed hub
    cluster:

    ``` bash
    global-hub.open-cluster-management.io/deploy-mode=hosted
    ```

### Migrating managed clusters

After you configure your multicluster global hub migration environment,
migrate your managed clusters. Complete the following steps to migrate
the `cluster1` sample and the associated resources from `hub1` to `hub2`
hub clusters:

You can create a `ManagedClusterMigration` resource in the multicluster
global hub migration environment by directly selecting your managed
clusters by name or by using a `Placement` resource.

To migrate your specific managed clusters by name, complete the
following steps:

1.  Go to your multicluster global hub namespace.

2.  Apply the following YAML file:

    ``` yaml
    apiVersion: global-hub.open-cluster-management.io/v1alpha1
    kind: ManagedClusterMigration
    metadata:
      name: migration-sample
    spec:
      from: local-cluster 
      includedManagedClusters:
        - cluster1 
        - cluster2
      to: hub2 
    ```

    - The `source` hub cluster is a `local-cluster` that multicluster
      global hub installed in `hub1` hub cluster.

    - The managed clusters that are being migrated to `hub2` hub
      cluster. The managed cluster in `hub1` and `hub2` hub clusters
      must be different from one another.

    - The `target` hub cluster is `hub2`.

To migrate your managed clusters with the `Placement` resource, complete
the following steps:

1.  Go to your multicluster global hub namespace.

2.  Select clusters based on labels, cluster properties, or other
    criteria defined in your `Placement` resource.

3.  Apply the following YAML file:

    ``` yaml
    apiVersion: global-hub.open-cluster-management.io/v1alpha1
    kind: ManagedClusterMigration
    metadata:
      name: migration-placement-sample
    spec:
      from: local-cluster 
      includedManagedClustersPlacementRef: production-clusters 
      to: hub2 
    ```

    - The `source` hub cluster is a `local-cluster` that multicluster
      global hub installed in `hub1` hub cluster.

    - The `Placement` resource that has the name `production-clusters`
      and that defines which clusters get migrated. You must define the
      `Placement` resource in the multicluster global hub agent
      namespace of the source hub cluster. For example, you can name the
      `Placement` resource `multicluster-global-hub` or
      `multicluster-global-hub-agent`.

    - The `target` hub cluster is `hub2`.

4.  Specify the `includedManagedClusters` or
    `includedManagedClustersPlacementRef` cluster type to include in
    your migration. Include only one of these cluster types in your
    migration because they cannot exist together.

### Tracking the migration status

During the migration process, you can track the statuses of your managed
clusters by using the multicluster global hub `ConfigMap` or the
migration customer resource.

multicluster global hub automatically creates a `ConfigMap` which gives
you a detailed cluster list, telling you if the cluster migration fails
or succeeds. The migration customer resources gives you the status of
the entire migration process.

Track the migration status of your managed clusters by completing the
following steps:

1.  View the migration status from the `ConfigMap` by running the
    following command:

    ``` bash
    kubectl get configmap <migration-name> -n <global-hub-namespace> -o yaml
    ```

2.  Ensure that the `ConfigMap` that you see resembles the following
    sample:

    ``` yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: migration-sample
      namespace: multicluster-global-hub
    data:
      success: '["cluster1","cluster3"]'
      failure: '["cluster2"]'
    ```

3.  To view the tracking status from the migration customer resource,
    verify that its migration status is `True`, and that it resembles
    the following sample:

``` yaml
status:
  conditions:
    - type: ResourceValidated
      status: "True"
      message: Migration resources have been validated
    - type: ResourceInitialized
      status: "True"
      message: All source and target hubs have been initialized
    - type: ResourceDeployed
      status: "True"
      message: Resources have been successfully deployed to the target hub cluster
    - type: ClusterRegistered
      status: "True"
      message: All migrated clusters have been successfully registered
    - type: ResourceCleaned
      status: "True"
      message: Resources have been successfully cleaned up from the hub clusters
  phase: Completed
```

## Recovering data from the upgraded built-in PostgreSQL (Deprecated)

Starting with multicluster global hub version 1.4.0, the built-in
PostgreSQL database is upgraded to version 16. This upgrade replaces the
earlier `multicluster-global-hub-postgres` instance with the new
`multicluster-global-hub-postgressql` instance.

By default, this upgrade automatically re-syncs real-time data, such as
`policies` and `clusters`, to the new Postgres instance. Historical
data, such as `event` and `history` tables, are not automatically
recovered.

### Restoring historical data

When the multicluster global hub upgrade to version 1.4.0 removes your
historical data, recover your data by completing the following steps:

1.  Clone the Red Hat Advanced Cluster Management for Kubernetes Git
    repository to access the shell script that you need to recover your
    data by running the following command:

    ``` bash
    git clone -b release-2.13 https://github.com/stolostron/multicluster-global-hub.git
    ```

2.  Restore your history tables by completing the following steps:

    1.  If the default namespace is `multicluster-global-hub`, run the
        following shell script:

        ``` bash
        ./doc/upgrade/restore_history_tables.sh
        ```

    2.  If the namespace is not specified as `multicluster-global-hub`,
        set the multicluster global hub namespace when you run the
        following shell script:

    ``` bash
    ./doc/upgrade/restore_history_tables.sh 
    ```

    - The multicluster global hub that you installed.

3.  Restore your event tables by completing the following steps:

    1.  If the default namespace is `multicluster-global-hub`, run the
        following shell script:

        ``` bash
        ./doc/upgrade/restore_event_tables.sh
        ```

    2.  If the namespace is not specified as `multicluster-global-hub`,
        set the multicluster global hub namespace when you run the
        following shell script:

    ``` bash
    ./doc/upgrade/restore_event_tables.sh 
    ```

    - The multicluster global hub that you installed.

### Deleting legacy built-in Postgres data

After multicluster global hub upgrades to version 1.4.0, it switches to
the new built-in Postgres instance. The global hub operator does not
automatically delete resources associated with the legacy Postgres
instance. To delete the legacy Postgres resources, complete the
following steps:

1.  If the default namespace is `multicluster-global-hub`, run the
    following shell script:

    ``` bash
    ./doc/upgrade/cleanup_legacy_postgres.sh
    ```

2.  If the namespace is not specified as `multicluster-global-hub`, set
    the multicluster global hub namespace when you run the following
    shell script:

    ``` bash
    ./doc/upgrade/cleanup_legacy_postgres.sh 
    ```

    - The multicluster global hub that you installed.
