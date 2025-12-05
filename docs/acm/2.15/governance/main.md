# Governance

Enterprises must meet internal standards for software engineering,
secure engineering, resiliency, security, and regulatory compliance for
workloads hosted on private, multi and hybrid clouds. Red Hat Advanced
Cluster Management for Kubernetes governance provides an extensible
policy framework for enterprises to introduce their own security
policies.

## Policy controllers

Policy controllers monitor and report whether your cluster is compliant
with a policy. Use the Red Hat Advanced Cluster Management for
Kubernetes policy framework by using the supported policy templates to
apply policies managed by these controllers. The policy controllers
manage Kubernetes custom resource definition instances.

**Important:** Only the configuration policy controller policies support
the `enforce` feature. You must manually remediate policies, where the
policy controller does not support the `enforce` feature.

### Kubernetes configuration policy controller

Use the configuration policy controller to configure any Kubernetes
resource and apply security policies across your clusters. The
configuration policy controller communicates with the local Kubernetes
API server so that you can get a list of your configurations that are in
your cluster.

During installation, the configuration policy controller is created on
the managed cluster. The configuration policy is provided in the
`policy-templates` field of the policy on the hub cluster, and is
propagated to the selected managed clusters by the governance framework.

When the `remediationAction` for the configuration policy controller is
set to `InformOnly`, the parent policy does not enforce the
configuration policy, even if the `remediationAction` in the parent
policy is set to `enforce`.

If you have existing Kubernetes manifests that you want to put in a
policy, the Policy Generator is a useful tool to accomplish this.

#### Configuration policy YAML structure

You can find the description of a field on your managed cluster by
running the
`oc explain --api-version=policy.open-cluster-management.io/v1 ConfigurationPolicy.<field-path>`
command. Replace `<field-path>` with the path to the field that you
need.

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: policy-config
spec:
  namespaceSelector:
    include: ["default"]
    exclude: []
    matchExpressions: []
    matchLabels: {}
  remediationAction: inform 
  customMessage:
    compliant: {}
    noncompliant: {}
  severity: low
  evaluationInterval:
    compliant: ""
    noncompliant: ""
  object-templates-raw: ""
  object-templates: 
   - complianceType: musthave
     metadataComplianceType:
     recordDiff: ""
     recreateOption: ""
     objectSelector:
       matchLabels: {}
       matchExpressions: []
     objectDefinition:
       apiVersion: v1
       kind: Pod
       metadata:
         name: pod
       spec:
         containers:
          - image: pod-image
            name: pod-name
            ports:
             - containerPort: 80
   - complianceType: mustonlyhave
     objectDefinition:
       apiVersion: v1
       kind: ConfigMap
       metadata:
         name: myconfig
         namespace: default
         data:
           testData: hello
```

- When the `remediationAction` for the configuration policy is set to
  `enforce`, the controller applies the specified configuration to the
  target managed cluster. However, configuration policies that specify
  an object without a name can only be set to `inform`, unless the
  `objectSelector` is also configured.

- A Kubernetes object is defined in the `object-templates` array in the
  configuration policy, where fields of the configuration policy
  controller is compared with objects on the managed cluster. You can
  also use templated values within configuration policies. For more
  advanced use cases, specify a string in `object-templates-raw` to
  create the `object-templates` that you want. For more information, see
  *Template processing*.

#### Configuration policy YAML table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to ConfigurationPolicy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name of the policy.

- Field: spec.namespaceSelector - Optional or required: Required for
  namespaced objects that do not have a namespace specified -
  Description: Determines namespaces in the managed cluster that the
  object is applied to. The include and exclude parameters accept file
  path expressions to include and exclude namespaces by name. The
  matchExpressions and matchLabels parameters specify namespaces to
  include by label. See the Kubernetes labels and selectors
  documentation. The resulting list is compiled by using the
  intersection of results from all parameters.

- Field: spec.remediationAction - Optional or required: Required -
  Description: Specifies the action to take when the policy is
  non-compliant. Use the following parameter values: inform, InformOnly,
  or enforce.

- Field: spec.customMessage - Optional or required: Optional -
  Description: Configure the compliance message sent by the
  configuration policy based on the current compliance. Each message
  configuration is a string that can contain Go templates. The
  .DefaultMessage and .Policy context variables are available for use in
  the templates. You can access the default message by using the
  .DefaultMessage parameter. The .Policy context variable contains the
  current policy object, including its status. For example, you can
  access the state of each related object by specifying the
  .Policy.status.relatedObjects\[\*\].object field. If you set a value
  for the evaluationInterval field other than watch, only the kind,
  name, and namespace of the related objects are available.

- Field: spec.customMessage.compliant - Optional or required: Optional -
  Description: Configure custom messages for configuration policies that
  are compliant. Go templates and UTF-8 encoded characters, including
  emoji and foreign characters, are supported values.

- Field: spec.customMessage.noncompliant - Optional or required:
  Optional - Description: Configure custom messages for configuration
  policies that are non-compliant. Go templates and UTF-8 encoded
  characters, including emoji and foreign characters, are supported
  values.

- Field: spec.severity - Optional or required: Required - Description:
  Specifies the severity when the policy is non-compliant. Use the
  following parameter values: low, medium, high, or critical.

- Field: spec.evaluationInterval - Optional or required: Optional -
  Description: Specifies the frequency for a policy to be evaluated when
  it is in a particular compliance state. Use the parameters compliant
  and noncompliant. The default value for the compliant and noncompliant
  parameters is watch to leverage Kubernetes API watches instead of
  polling the Kubernetes API server.When managed clusters have low
  resources, the evaluation interval can be set to long polling
  intervals to reduce CPU and memory usage on the Kubernetes API and
  policy controller. These are in the format of durations. For example,
  1h25m3s represents 1 hour, 25 minutes, and 3 seconds. These can also
  be set to never to avoid evaluating the policy after it is in a
  particular compliance state.

- Field: spec.evaluationInterval.compliant - Optional or required:
  Optional - Description: Specifies the evaluation frequency for a
  compliant policy. To enable the previous polling behavior, set this
  parameter to 10s.

- Field: spec.evaluationInterval.noncompliant - Optional or required:
  Optional - Description: Specifies the evaluation frequency for a
  non-compliant policy. To enable the previous polling behavior, set
  this parameter to 10s.

- Field: spec.object-templates - Optional or required: Optional -
  Description: The array of Kubernetes objects (either fully defined or
  containing a subset of fields) for the controller to compare with
  objects on the managed cluster. Note: While spec.object-templates and
  spec.object-templates-raw are listed as optional, exactly one of the
  two parameter fields must be set.

- Field: spec.object-templates-raw - Optional or required: Optional -
  Description: Used to set object templates with a raw YAML string.
  Specify conditions for the object templates, where advanced functions
  like if-else statements and the range function are supported values.
  For example, add the following value to avoid duplication in your
  object-templates definition: {{- if eq .metadata.name
  "policy-grc-your-meta-data-name" }} replicas: 2 {{- else }} replicas:
  1 {{- end }} Note: While spec.object-templates and
  spec.object-templates-raw are listed as optional, exactly one of the
  two parameter fields must be set.

- Field: spec.object-templates\[\].complianceType - Optional or
  required: Required - Description: Use this parameter to define the
  desired state of the Kubernetes object on your managed clusters. Use
  one of the following verbs as the parameter value: mustonlyhave:
  Indicates that an object must exist with the exact fields and values
  as defined in the objectDefinition. musthave: Indicates an object must
  exist with the same fields as specified in the objectDefinition. Any
  existing fields on the object that are not specified in the
  object-template are ignored. In general, array values are appended.
  The exception for the array to be patched is when the item contains a
  name key with a value that matches an existing item. Use a fully
  defined objectDefinition using the mustonlyhave compliance type, if
  you want to replace the array. mustnothave: Indicates that an object
  with the same fields as specified in the objectDefinition cannot
  exist.

- Field: spec.object-templates\[\].metadataComplianceType - Optional or
  required: Optional - Description: Overrides
  spec.object-templates\[\].complianceType when comparing the manifest’s
  metadata section to objects on the cluster ("musthave",
  "mustonlyhave"). Default is unset to not override complianceType for
  metadata.

- Field: spec.object-templates\[\].recordDiff - Optional or required:
  Optional - Description: Use this parameter to specify if and where to
  display the difference between the object on the cluster and the
  objectDefinition in the policy. The following options are supported:
  Set to InStatus to store the difference in the ConfigurationPolicy
  status. Set to Log to log the difference in the controller logs. Set
  to None to not log the difference. By default, this parameter is set
  to InStatus if the controller does not detect sensitive data in the
  difference. Otherwise, the default is None. If sensitive data is
  detected, the ConfigurationPolicy status displays a message to set
  recordDiff to view the difference.

- Field: spec.object-templates\[\].recreateOption - Optional or
  required: Optional - Description: Describes when to delete and
  recreate an object when an update is required. When you set the object
  to IfRequired, the policy recreates the object when updating an
  immutable field. When you set the parameter to Always, the policy
  recreates the object on any update. When you set the remediationAction
  to inform, the parameter value, recreateOption, has no effect on the
  object. The IfRequired value has no effect on clusters without dry-run
  update support. The default value is None.

- Field: spec.object-templates\[\].objectSelector - Optional or
  required: Optional - Description: ObjectSelector defines a label
  selector to select names of objects that are defined in an unnamed
  objectDefinition. The matchExpressions and matchLabels parameters
  specify objects to include by label. If there is an object name that
  is defined in the objectDefinition, the objectSelector is ignored. For
  more information, see Kubernetes labels and selectors.

- Field: spec.object-templates\[\].objectDefinition - Optional or
  required: Required - Description: A Kubernetes object (either fully
  defined or containing a subset of fields) for the controller to
  compare with objects on the managed cluster.

- Field: spec.pruneObjectBehavior - Optional or required: Optional -
  Description: Determines whether to clean up resources related to the
  policy when the policy is removed from a managed cluster.

### Certificate policy controller

You can use the certificate policy controller to detect certificates
that are close to expiring, time durations (hours) that are too long, or
contain DNS names that fail to match specified patterns. You can add the
certificate policy to the `policy-templates` field of the policy on the
hub cluster, which propagates to the selected managed clusters by using
the governance framework. See the Hub cluster policy framework
documentation for more details on the hub cluster policy.

Configure and customize the certificate policy controller by updating
the following parameters in your controller policy:

- `minimumDuration`

- `minimumCADuration`

- `maximumDuration`

- `maximumCADuration`

- `allowedSANPattern`

- `disallowedSANPattern`

Your policy might become non-compliant due to either of the following
scenarios:

- When a certificate expires in less than the minimum duration of time
  or exceeds the maximum time.

- When DNS names fail to match the specified pattern.

The certificate policy controller is created on your managed cluster.
The controller communicates with the local Kubernetes API server to get
the list of secrets that contain certificates and determine all
non-compliant certificates.

Certificate policy controller does not support the `enforce` feature.

**Note:** The certificate policy controller automatically looks for a
certificate in a secret in only the `tls.crt` key. If a secret is stored
under a different key, add a label named `certificate_key_name` with a
value set to the key to let the certificate policy controller know to
look in a different key. For example, if a secret contains a certificate
stored in the key named `sensor-cert.pem`, add the following label to
the secret: `certificate_key_name: sensor-cert.pem`.

#### Certificate policy controller YAML structure

View the following example of a certificate policy and review the
element in the YAML table:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: CertificatePolicy
metadata:
  name: certificate-policy-example
spec:
  namespaceSelector:
    include: ["default"]
    exclude: []
    matchExpressions: []
    matchLabels: {}
  labelSelector:
    myLabelKey: myLabelValue
  remediationAction:
  severity:
  minimumDuration:
  minimumCADuration:
  maximumDuration:
  maximumCADuration:
  allowedSANPattern:
  disallowedSANPattern:
```

##### Certificate policy controller YAML table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to CertificatePolicy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name to identify the policy.

- Field: metadata.labels - Optional or required: Optional - Description:
  In a certificate policy, the category=system-and-information-integrity
  label categorizes the policy and facilitates querying the certificate
  policies. If there is a different value for the category key in your
  certificate policy, the value is overridden by the certificate
  controller.

- Field: spec.namespaceSelector - Optional or required: Required -
  Description: Determines namespaces in the managed cluster where
  secrets are monitored. The include and exclude parameters accept file
  path expressions to include and exclude namespaces by name. The
  matchExpressions and matchLabels parameters specify namespaces to be
  included by label. See the Kubernetes labels and selectors
  documentation. The resulting list is compiled by using the
  intersection of results from all parameters.Note: If the
  namespaceSelector for the certificate policy controller does not match
  any namespace, the policy is considered compliant.

- Field: spec.labelSelector - Optional or required: Optional -
  Description: Specifies identifying attributes of objects. See the
  Kubernetes labels and selectors documentation.

- Field: spec.remediationAction - Optional or required: Required -
  Description: Specifies the remediation of your policy. Set the
  parameter value to inform. Certificate policy controller only supports
  inform feature.

- Field: spec.severity - Optional or required: Optional - Description:
  Informs the user of the severity when the policy is non-compliant. Use
  the following parameter values: low, medium, high, or critical.

- Field: spec.minimumDuration - Optional or required: Required -
  Description: When a value is not specified, the default value is 100h.
  This parameter specifies the smallest duration (in hours) before a
  certificate is considered non-compliant. The parameter value uses the
  time duration format from Golang. See Golang Parse Duration for more
  information.

- Field: spec.minimumCADuration - Optional or required: Optional -
  Description: Set a value to identify signing certificates that might
  expire soon with a different value from other certificates. If the
  parameter value is not specified, the CA certificate expiration is the
  value used for the minimumDuration. See Golang Parse Duration for more
  information.

- Field: spec.maximumDuration - Optional or required: Optional -
  Description: Set a value to identify certificates that have been
  created with a duration that exceeds your desired limit. The parameter
  uses the time duration format from Golang. See Golang Parse Duration
  for more information.

- Field: spec.maximumCADuration - Optional or required: Optional -
  Description: Set a value to identify signing certificates that have
  been created with a duration that exceeds your defined limit. The
  parameter uses the time duration format from Golang. See Golang Parse
  Duration for more information.

- Field: spec.allowedSANPattern - Optional or required: Optional -
  Description: A regular expression that must match every SAN entry that
  you have defined in your certificates. This parameter checks DNS names
  against patterns. See the Golang Regular Expression syntax for more
  information.

- Field: spec.disallowedSANPattern - Optional or required: Optional -
  Description: A regular expression that must not match any SAN entries
  you have defined in your certificates. This parameter checks DNS names
  against patterns.Note: To detect wild-card certificate, use the
  following SAN pattern: disallowedSANPattern: "\[\\\*\]"See the Golang
  Regular Expression syntax for more information.

#### Certificate policy sample

When your certificate policy controller is created on your hub cluster,
a replicated policy is created on your managed cluster.

### Policy set controller

The policy set controller aggregates the policy status scoped to
policies that are defined in the same namespace. Create a policy set
(`PolicySet`) to group policies that are in the same namespace. All
policies in the `PolicySet` are placed together in a selected cluster by
creating a `PlacementBinding` to bind the `PolicySet` and `Placement`.
The policy set is deployed to the hub cluster.

Additionally, when a policy is a part of multiple policy sets, existing
and new `Placement` resources remain in the policy. When a user removes
a policy from the policy set, the policy is not applied to the cluster
that is selected in the policy set, but the placements remain. The
policy set controller only checks for violations in clusters that
include the policy set placement.

#### Policy set YAML structure

Your policy set might resemble the following YAML file:

``` yaml
apiVersion: policy.open-cluster-management.io/v1beta1
kind: PolicySet
metadata:
  name: demo-policyset
spec:
  policies:
  - policy-demo

---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
  name: demo-policyset-pb
placementRef:
  apiGroup: cluster.open-cluster-management.io
  kind: Placement
  name: demo-policyset-pr
subjects:
- apiGroup: policy.open-cluster-management.io
  kind: PolicySet
  name: demo-policyset
---
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name: demo-policyset-pr
spec:
  predicates:
  - requiredClusterSelector:
      labelSelector:
        matchExpressions:
          - key: name
            operator: In
            values:
              - local-cluster
    tolerations:
        - key: cluster.open-cluster-management.io/unavailable
          operator: Exists
        - key: cluster.open-cluster-management.io/unreachable
          operator: Exists
```

#### Policy set table

View the following parameter table for descriptions:

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1beta1.

- Field: kind - Optional or required: Required - Description: Set the
  value to PolicySet to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: spec - Optional or required: Required - Description: Add
  configuration details for your policy.

- Field: spec.policies - Optional or required: Optional - Description:
  The list of policies that you want to group together in the policy
  set.

#### Policy set sample

``` yaml
apiVersion: policy.open-cluster-management.io/v1beta1
kind: PolicySet
metadata:
  name: pci
  namespace: default
spec:
  description: Policies for PCI compliance
  policies:
  - policy-pod
  - policy-namespace
status:
  compliant: NonCompliant
  placement:
  - placementBinding: binding1
    placement: placement1
    policySet: policyset-ps
```

### Operator policy controller

The operator policy controller allows you to monitor and install
Operator Lifecycle Manager operators across your clusters. Use the
operator policy controller to monitor the health of various pieces of
the operator and to specify how you want to automatically handle updates
to the operator.

You can also distribute an operator policy to managed clusters by using
the governance framework and adding the policy to the `policy-templates`
field of a policy on the hub cluster.

You can also use template values within the `operatorGroup` and
`subscription` fields of an operator policy. For more information, see
*Template processing*.

#### Prerequisites

- Operator Lifecycle Manager must be available on your managed cluster.
  This is enabled by default on Red Hat OpenShift Container Platform.

- **Required access:** Cluster administrator

#### Operator policy YAML table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1beta1.

- Field: kind - Optional or required: Required - Description: Set the
  value to OperatorPolicy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: spec.remediationAction - Optional or required: Required -
  Description: If the remediationAction for the operator policy is set
  to enforce, the controller creates resources on the target managed
  cluster to communicate to OLM to install the operator and approve
  updates based on the versions specified in the policy. + If the
  remediationAction set to inform, the controller only reports the
  status of the operator, including if any upgrades are available.

- Field: spec.operatorGroup - Optional or required: Optional -
  Description: By default, if the operatorGroup field is not specified,
  the controller generates an AllNamespaces type OperatorGroup resource
  in the same namespace as the subscription, if supported. The operator
  policy controller produces this resource. View the following parameter
  descriptions: name: The name of the OperatorGroup resource. namespace:
  The namespace of the OperatorGroup resource. This parameter must match
  the namespace where you install the operator. targetNamespaces: A list
  of namespaces that the operator is configured to watch and operate.

- Field: spec.complianceType - Optional or required: Required -
  Description: Specifies the desired state of the operator on the
  cluster. If set to musthave, the policy is compliant when the operator
  is found. If set to mustnothave, the policy is compliant when the
  operator is not found.

- Field: spec.removalBehavior - Optional or required: Optional -
  Description: Determines which resource types need to be kept or
  removed when you enforce an OperatorPolicy resource with
  complianceType: mustnothave defined. There is no effect when
  complianceType is set to musthave. View the following parameter
  descriptions: operatorGroups can be set to Keep or DeleteIfUnused. The
  default value is DeleteIfUnusued which only removes the OperatorGroup
  resource if it is not used by any other operators. subscriptions can
  be set to Keep or Delete. The default value is Delete.
  clusterServiceVersions can be set to Keep or Delete. The default value
  is Delete. customResourceDefinitions can be set to Keep or Delete. The
  default value is Keep. If you set this to Delete, the
  CustomResourceDefintion resources on the managed cluster are removed
  and can cause data loss.

- Field: spec.subscription - Optional or required: Required -
  Description: Define the configurations to create an operator
  subscription. Add information in the following fields to create an
  operator subscription. View the following parameter descriptions:
  channel: If not specified, the default channel is selected from the
  operator catalog. The default can be different on different OpenShift
  Container Platform versions. name: Specify the package name of the
  operator. namespace: If not specified, the default namespaced that is
  used for OpenShift Container Platform managed clusters is
  openshift-operators. source: If not specified, the catalog that
  contains the operator is chosen. sourceNamespace: If not specified,
  the namespace of the catalog that contains the operator is chosen.
  config: Optional. Specify extra configuration details for the operator
  subscription. The name field is the only required field. The other
  fields are populated based on the catalog information within the
  managed cluster. Note: If you define a value for the
  installPlanApproval field in this parameter section, the policy
  becomes non-compliant. Use spec.upgradeApproval in the OperatorPolicy
  resource.

- Field: spec.complianceConfig - Optional or required: Optional -
  Description: Use this parameter to define the compliance behavior for
  specific scenarios that are associated with operators. You can set
  each of the following options individually, where the supported values
  are Compliant and NonCompliant: catalogSourceUnhealthy: Define the
  compliance when the catalog source for the operator is unhealthy. The
  default value is Compliant because this only affects possible
  upgrades. deploymentsUnavailable: Define the compliance when at least
  one deployment of the operator is not fully available. The default
  value is NonCompliant because this reflects the availability of the
  service that the operator provides. upgradesAvailable: Define the
  compliance when there is an upgrade available for the operator. The
  default value is Compliant because the existing operator installation
  might be running correctly. deprecationsPresent: Specifies that the
  compliance of the policy is affected by the deprecations. For example,
  the default value is Compliant, but if the
  deprecationsPresent=NonCompliant configuration detects the
  deprecations, then the policy compliance status is set to
  NonCompliant.

- Field: spec.upgradeApproval - Optional or required: Required -
  Description: If the upgradeApproval field is set to Automatic, version
  upgrades on the cluster are approved by the policy when the policy is
  set to enforce. If you set the field to None, version upgrades to the
  specific operator are not approved when the policy is set to enforce.

- Field: spec.versions - Optional or required: Optional - Description:
  Declare which versions of the operator are compliant. The versions
  parameter is a list of templatable strings that specifies which
  installed ClusterServiceVersion names are compliant when in inform
  mode, and which InstallPlans are approved when in enforce mode. To
  give different versions in one entry, separate the versions with
  commas. If the field is empty, the strings are ignored and all
  ClusterServiceVersion names are approved. The default value is empty.

## Template processing

Configuration policies and operator policies support the inclusion of
Golang text templates. These templates are resolved at runtime either on
the hub cluster or the target managed cluster using configurations
related to that cluster. This gives you the ability to define policies
with dynamic content, and inform or enforce Kubernetes resources that
are customized to the target cluster.

A policy definition can contain both hub cluster and managed cluster
templates. Hub cluster templates are processed first on the hub cluster,
then the policy definition with resolved hub cluster templates is
propagated to the target clusters. A controller on the managed cluster
processes any managed cluster templates in the policy definition and
then enforces or verifies the fully resolved object definition.

The template must conform to the Golang template language specification,
and the resource definition generated from the resolved template must be
a valid YAML. See the Golang documentation about *Package templates* for
more information. Any errors in template validation are recognized as
policy violations. When you use a custom template function, the values
are replaced at runtime.

**Important:**

- If you use hub cluster templates to propagate secrets or other
  sensitive data, the sensitive data exists in the managed cluster
  namespace on the hub cluster and on the managed clusters where that
  policy is distributed. The template content is expanded in the policy,
  and policies are not encrypted by the OpenShift Container Platform
  ETCD encryption support. To address this, use `fromSecret` or
  `copySecretData`, which automatically encrypts the values from the
  secret, or `protect` to encrypt other values.

- When you add multiline string values such as, certificates, always add
  `| toRawJson | toLiteral` syntax at the end of the template pipeline
  to handle line breaks. For example, if you are copying a certificate
  from a `Secret` resource and including it in a `ConfigMap` resource,
  your template pipeline might be similar to the following syntax:

      ca.crt: '{{ fromSecret "openshift-config" "ca-config-map-secret" "ca.crt"  | base64dec | toRawJson | toLiteral }}'

  The `toRawJson` template function converts the input value to a JSON
  string with new lines escaped to not affect the YAML structure. The
  `toLiteral` template function removes the outer single quotes from the
  output. For example, when templates are processed for the
  `key: '{{ 'hello\nworld' | toRawJson }}'` template pipeline, the
  output is `key: '"hello\nworld"'`. The output of the
  `key: '{{ 'hello\nworld' | toRawJson | toLiteral }}'` template
  pipeline is `key: "hello\nworld"`.

See the following table for a comparison of hub cluster and managed
cluster templates:

### Comparison of hub cluster and managed cluster templates

- Templates: Syntax - Hub cluster: Golang text template specification -
  Managed cluster: Golang text template specification

- Templates: Delimiter - Hub cluster: {{hub … hub}} - Managed cluster:
  {{ … }}

- Templates: Context - Hub cluster: Context variables
  .ManagedClusterName, .ManagedClusterLabels, and .PolicyMetadata are
  available. .ManagedClusterName resolves to the name of the target
  cluster where the policy is propagated. .ManagedClusterLabels resolves
  to a map of keys and values of the labels on the managed cluster where
  the policy is propagated. .PolicyMetadata resolves to a map with the
  name, namespace, labels, and annotations keys with values from the
  root policy. - Managed cluster: For ConfigurationPolicy resources,
  context variables .ObjectName, .ObjectNamespace, and .Object are
  available inside objectDefinition. If the object is not
  cluster-scoped, ObjectNamespace resolves to the name of the selected
  namespace from the spec.namespaceSelector or metadata.namespace that
  you specified. The .ObjectName resolves to the name of the object from
  the objectSelector or metadata.name that you specified. The .Object is
  the full target object that is currently on the cluster.

- Templates: Access control - Hub cluster: By default, you can only
  reference namespaced Kubernetes resources that are in the same
  namespace as the Policy object and the ManagedCluster object of the
  cluster that the policy propagates to.Alternatively, you can specify
  the spec.hubTemplateOptions.serviceAccountName field in the Policy
  object to a service account in the same namespace as the Policy
  resource. When you specify the field, the service account is used for
  all hub cluster template lookups.Note: The service account must have
  list and watch permissions on any resource that is looked up in a hub
  cluster template. - Managed cluster: You can reference any resource on
  the cluster.

- Templates: Functions - Hub cluster: A set of template functions that
  support dynamic access to Kubernetes resources and string
  manipulation. See Template functions for more information. See the
  Access control row for lookup restrictions.The fromSecret template
  function on the hub cluster stores the resulting value as an encrypted
  string on the replicated policy, in the managed cluster namespace.The
  equivalent call might use the following syntax: {{hub "(lookup "v1"
  "Secret" "default" "my-hub-secret").data.message \| protect hub}} -
  Managed cluster: A set of template functions support dynamic access to
  Kubernetes resources and string manipulation. See Template functions
  for more information.

- Templates: Function output storage - Hub cluster: The output of
  template functions are stored in Policy resource objects in each
  applicable managed cluster namespace on the hub cluster, before it is
  synced to the managed cluster. This means that any sensitive results
  from template functions are readable by anyone with read access to the
  Policy resource objects on the hub cluster, and anyone with read
  access to the ConfigurationPolicy or OperatorPolicy resource objects
  on the managed clusters. Additionally, if etcd encryption is enabled,
  the policy resource objects are not encrypted. It is best to carefully
  consider this when using template functions that return sensitive
  output (e.g. from a secret). - Managed cluster: The output of template
  functions are not stored in policy related resource objects.

- Templates: Processing - Hub cluster: Processing occurs at runtime on
  the hub cluster during propagation of replicated policies to clusters.
  Policies and the hub cluster templates within the policies are
  processed on the hub cluster only when templates are created or
  updated. - Managed cluster: Processing occurs on the managed cluster.
  Configuration policies are processed periodically, which automatically
  updates the resolved object definition with data in the referenced
  resources. Operator policies automatically update whenever a
  referenced resource changes.

- Templates: Processing errors - Hub cluster: Errors from the hub
  cluster templates are displayed as violations on the managed clusters
  the policy applies to. - Managed cluster: Errors from the managed
  cluster templates are displayed as violations on the specific target
  cluster where the violation occurred.

### Template functions

Reference Kubernetes resources such as resource-specific and generic
template functions on your hub cluster by using the `{{hub …​ hub}}`
delimiters, or on your managed cluster by using the `{{ …​ }}`
delimiters. You can use resource-specific functions for convenience and
to make the content of your resources more accessible.

#### Template function descriptions

If you use the generic function, `lookup`, which is more advanced,
familiarize yourself with the YAML structure of the resource that is
being looked up. In addition to these functions, utility functions such
as `base64enc`, `base64dec`, `indent`, `autoindent`, `toInt`, `toBool`,
and more are available.

To conform templates with YAML syntax, you must define templates in the
policy resource as strings using quotes or a block character (`|` or
`>`). This causes the resolved template value to also be a string. To
override this, use `toInt` or `toBool` as the final function in the
template to initiate further processing that forces the value to be
interpreted as an integer or boolean respectively.

##### *fromSecret*

The `fromSecret` function returns the value of the given data key in the
secret. View the following syntax for the function:

    func fromSecret (ns string, secretName string, datakey string) (dataValue string, err error)

When you use this function, enter the namespace, name, and data key of a
Kubernetes `Secret` resource. You must use the same namespace that is
used for the policy when using the function in a hub cluster template.
See *Template processing* for more details.

View the following configuration policy that enforces a `Secret`
resource on the target cluster:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-fromsecret
spec:
  object-templates:
  - objectDefinition:
      apiVersion: v1
      kind: Secret 
      metadata:
        name: demosecret
        namespace: test
      type: Opaque
      data: 
        USER_NAME: YWRtaW4=
        PASSWORD: '{{ fromSecret "default" "localsecret" "PASSWORD" }}' 
```

- You receive a policy violation if the Kubernetes `Secret` resource
  does not exist on the target cluster. If the data key does not exist
  on the target cluster, the value becomes an empty string.

- When you use the `fromSecret` function with hub cluster templates, the
  output is automatically encrypted using the protect function to
  protect the value in flight to the managed cluster.

- The value for the `PASSWORD` data key is a template that references
  the secret on the target cluster.

**Important:** When you add multiline string values such as,
certificates, always add `| toRawJson | toLiteral` syntax at the end of
the template pipeline to handle line breaks. For example, if you are
copying a certificate from a `Secret` resource and including it in a
`ConfigMap` resource, your template pipeline might be similar to the
following syntax:

    ca.crt: '{{ fromSecret "openshift-config" "ca-config-map-secret" "ca.crt"  | base64dec | toRawJson | toLiteral }}'

- The `toRawJson` template function converts the input value to a JSON
  string with new lines escaped to not affect the YAML structure.

- The `toLiteral` template function removes the outer single quotes from
  the output. For example, when templates are processed for the
  `key: '{{ 'hello\nworld' | toRawJson }}'` template pipeline, the
  output is `key: '"hello\nworld"'`. The output of the
  `key: '{{ 'hello\nworld' | toRawJson | toLiteral }}'` template
  pipeline is `key: "hello\nworld"`.

##### *fromConfigmap*

The `fromConfigMap` function returns the value of the given data key in
the config map. When you use this function, enter the namespace, name,
and data key of a Kubernetes `ConfigMap` resource. You must use the same
namespace that is used for the policy using the function in a hub
cluster template. See *Template processing* for more details.

View the following syntax for the function:

    func fromConfigMap (ns string, configmapName string, datakey string) (dataValue string, err Error)

View the following configuration policy that enforces a Kubernetes
resource on the target managed cluster:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-fromcm-lookup
spec:
  object-templates:
  - objectDefinition:
      ...
      data: 
        app-name: sampleApp
        app-description: "this is a sample app"
        log-file: '{{ fromConfigMap "default" "logs-config" "log-file" }}' 
        log-level: '{{ fromConfigMap "default" "logs-config" "log-level" }}' 
```

- If the `data` key does not exist on the target cluster, the value
  becomes an empty string.

- The `log-file` template value retrieves the value of the `log-file`
  data key from the `logs-config` `ConfigMap` in the `default`
  namespace.

- The `log-level` template value retrieves the value of the `log-level`
  data key from the `logs-config` `ConfigMap` in the `default`
  namespace.

##### *fromClusterClaim*

The `fromClusterClaim` function returns the value of the `Spec.Value` in
the `ClusterClaim` resource. View the following syntax for the function:

    func fromClusterClaim (clusterclaimName string) (dataValue string, err Error)

View the following example of the configuration policy that enforces a
Kubernetes resource on the target managed cluster:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-clusterclaims 
spec:
  object-templates:
  - objectDefinition:
      ...
      data: 
        platform: '{{ fromClusterClaim "platform.open-cluster-management.io" }}' 
        product: '{{ fromClusterClaim "product.open-cluster-management.io" }}'
        version: '{{ fromClusterClaim "version.openshift.io" }}'
```

- When you use this function, enter the name of a Kubernetes
  `ClusterClaim` resource. You receive a policy violation if the
  `ClusterClaim` resource does not exist.

- Configuration values can be set as key-value properties.

- The value for the `platform` data key is a template that retrieves the
  value of the `platform.open-cluster-management.io` cluster claim.
  Similarly, it retrieves values for `product` and `version` from the
  `ClusterClaim` resource.

##### *lookupClusterClaim*

The `lookupClusterClaim` function is similar to the `fromClusterClaim`
function. The only difference is that when the `lookupClusterClaim`
function cannot find the `ClusterClaim` resource, `lookupClusterClaim`
gives you an empty string. You can use your preferred templating
function to detect when the response is an empty string, and then adjust
the output. For example, when the `ClusterClaim` does not exist, you can
define a default value or skip the object.

View the following example of the configuration policy that enforces a
Kubernetes resource on the target managed cluster:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-clusterclaims 
spec:
  object-templates:
  - objectDefinition:
      ...
      kind: ConfigMap
      data:
        something: '{{ default "empty" (lookupClusterClaim "possibly.nonexistent") }}'
```

- When the `possibly.nonexistent` `ClusterClaim` is found, its value
  gets used in the ConfigMap. If the `ClusterClaim` does not exist,
  `empty` gets used instead through the `default` function that is
  provided by Sprig.

##### *lookup*

The `lookup` function returns the Kubernetes resource as a JSON
compatible map. When you use this function, enter the API version, kind,
namespace, name, and optional label selectors of the Kubernetes
resource. You must use the same namespace that is used for the policy
within the hub cluster template. See *Template processing* for more
details.

If the requested resource does not exist, an empty map is returned. If
the resource does not exist and the value is provided to another
template function, you might get the following error:
`invalid value; expected string`.

**Note:** Use the `default` template function, so the correct type is
provided to later template functions. See the *Sprig open source*
section.

View the following syntax for the function:

    func lookup (apiversion string, kind string, namespace string, name string, labelselector ...string) (value string, err Error)

For label selector examples, see the reference to the *Kubernetes labels
and selectors* documentation, in the *Additional resources* section.
View the following example of the configuration policy that enforces a
Kubernetes resource on the target managed cluster:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-lookup
spec:
  object-templates:
  - objectDefinition:
      ...
      data: 
        app-name: sampleApp
        app-description: "this is a sample app"
        metrics-url: >- 
          http://{{ (lookup "v1" "Service" "default" "metrics").spec.clusterIP }}:8080
```

- Configuration values can be set as key-value properties.

- The value for the `metrics-url` data key is a template that retrieves
  the `v1/Service` Kubernetes resource `metrics` from the `default`
  namespace, and is set to the value of the `spec.clusterIP` in the
  queried resource.

##### *base64enc*

The `base64enc` function returns a `base64` encoded value of the input
`data string`. When you use this function, enter a string value. View
the following syntax for the function:

    func base64enc (data string) (enc-data string)

View the following example of the configuration policy that uses the
`base64enc` function:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-fromsecret
spec:
  object-templates:
  - objectDefinition:
      ...
      data:
        USER_NAME: >-
          {{ fromConfigMap "default" "myconfigmap" "admin-user" | base64enc }}
```

##### *base64dec*

The `base64dec` function returns a `base64` decoded value of the input
`enc-data string`. When you use this function, enter a string value.
View the following syntax for the function:

    func base64dec (enc-data string) (data string)

View the following example of the configuration policy that uses the
`base64dec` function:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-fromsecret
spec:
  object-templates:
  - objectDefinition:
      ...
      data:
        app-name: >-
          {{ ( lookup "v1"  "Secret" "testns" "mytestsecret") .data.appname ) | base64dec }}
```

##### *indent*

The `indent` function returns the padded `data string`. When you use
this function, enter a data string with the specific number of spaces.
View the following syntax for the function:

    func indent (spaces  int,  data string) (padded-data string)

View the following example of the configuration policy that uses the
`indent` function:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
spec:
  object-templates:
  - objectDefinition:
      ...
      data:
        Ca-cert: >-
          {{ ( index ( lookup "v1" "Secret" "default" "mycert-tls"  ).data  "ca.pem"  ) |  base64dec | indent 4  }}
```

##### *autoindent*

The `autoindent` function acts like the `indent` function that
automatically determines the number of leading spaces based on the
number of spaces before the template.

View the following example of the configuration policy that uses the
`autoindent` function:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-fromsecret
spec:
  object-templates:
  - objectDefinition:
      ...
      data:
        Ca-cert: >-
          {{ ( index ( lookup "v1" "Secret" "default" "mycert-tls"  ).data  "ca.pem"  ) |  base64dec | autoindent }}
```

##### *toInt*

The `toInt` function casts and returns the integer value of the input
value. When this is the last function in the template, there is further
processing of the source content. This is to ensure that the value is
interpreted as an integer by the YAML. When you use this function, enter
the data that needs to be casted as an integer. View the following
syntax for the function:

    func toInt (input interface{}) (output int)

View the following example of the configuration policy that uses the
`toInt` function:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-template-function
spec:
  object-templates:
  - objectDefinition:
      ...
      spec:
        vlanid: >-
          {{ (fromConfigMap "site-config" "site1" "vlan")  | toInt }}
```

##### *toBool*

The `toBool` function converts the input string into a boolean, and
returns the boolean. When this is the last function in the template,
there is further processing of the source content. This is to ensure
that the value is interpreted as a boolean by the YAML. When you use
this function, enter the string data that needs to be converted to a
boolean. View the following syntax for the function:

    func toBool (input string) (output bool)

View the following example of the configuration policy that uses the
`toBool` function:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-template-function
spec:
  object-templates:
  - objectDefinition:
      ...
      spec:
        enabled: >-
          {{ (fromConfigMap "site-config" "site1" "enabled")  | toBool }}
```

##### *fromYaml*

The `fromYaml`, or `fromYAML`, function parses a YAML string into a
Golang object. You can use this function with a `ConfigMap` resource
that has a YAML string value.

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-template-function
spec:
  object-templates:
  - objectDefinition:
      ...
      spec:
        replicas: >-
          {{ (fromConfigMap "default" "app-config" "config.yaml") | fromYaml | index "replicas" }}
```

##### *toYaml*

The `toYaml`, or `toYAML`, function parses a Golang object into a YAML
string. For a multiline result to be properly indented, you must pass
the output to either the `autoindent` or `indent` function.

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-template-function
spec:
  object-templates:
  - objectDefinition:
      ...
      data:
        config.yaml: |
          {{ dict "key1" "value1" "key2" "value2" | toYaml | autoindent }}
```

##### *protect*

The `protect` function enables you to encrypt a string in a hub cluster
policy template. It is automatically decrypted on the managed cluster
when the policy is evaluated. View the following example of the
configuration policy that uses the `protect` function:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: demo-template-function
spec:
  object-templates:
  - objectDefinition:
    ...
    spec:
      enabled: >-
        {{hub (lookup "v1" "Secret" "default" "my-hub-secret").data.message | protect hub}}
```

In the previous YAML example, there is an existing hub cluster policy
template that is defined to use the `lookup` function. On the replicated
policy in the managed cluster namespace, the value might resemble the
following syntax:
`$ocm_encrypted:okrrBqt72oI+3WT/0vxeI3vGa+wpLD7Z0ZxFMLvL204=`

Each encryption algorithm used is AES-CBC using 256-bit keys. Each
encryption key is unique per managed cluster and is automatically
rotated every 30 days.

This ensures that your decrypted value is to never be stored in the
policy on the managed cluster.

To force an immediate rotation, delete the
`policy.open-cluster-management.io/last-rotated` annotation on the
`policy-encryption-key` Secret in the managed cluster namespace on the
hub cluster. Policies are then reprocessed to use the new encryption
key.

##### *toLiteral*

The `toLiteral` function removes any quotation marks around the template
string after it is processed. You can use this function to convert a
JSON string from a config map field to a JSON value in the manifest. Run
the following function to remove quotation marks from the `key`
parameter value:

    key: '{{ "[\"10.10.10.10\", \"1.1.1.1\"]" | toLiteral }}'

After using the `toLiteral` function, the following update is displayed:

    key: ["10.10.10.10", "1.1.1.1"]

##### *copySecretData*

The `copySecretData` function copies all of the `data` contents of the
specified secret. View the following sample of the function:

``` yaml
...
objectDefinition:
  apiVersion: v1
  kind: Secret
  metadata:
    name: my-secret-copy
  data: '{{ copySecretData "default" "my-secret" }}' 
```

- When you use this function with hub cluster templates, the output is
  automatically encrypted using the protect function.

##### *copyConfigMapData*

The `copyConfigMapData` function copies all of the `data` content of the
specified config map. View the following sample of the function:

``` yaml
...
objectDefinition:
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: my-secret-copy
  data: '{{ copyConfigMapData "default" "my-configmap" }}'
```

##### *getNodesWithExactRoles*

The `getNodesWithExactRoles` function returns a list of nodes with only
the roles that you specify, and ignores nodes that have any additional
roles except the `node-role.kubernetes.io/worker` role. View the
following sample function where you are selecting `"infra"` nodes and
ignoring the storage nodes:

``` yaml
...
objectDefinition:
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: my-configmap
    data:
      infraNode: |
        {{- range $i,$nd := (getNodesWithExactRoles "infra").items }}
        node{{ $i }}: {{ $nd.metadata.name }}
        {{- end }}
      replicas: {{ len ((getNodesWithExactRoles "infra").items) | toInt }}
```

##### *hasNodesWithExactRoles*

The `hasNodesWithExactRoles` function returns the `true` value if the
cluster contains nodes with only the roles that you specify, and ignores
nodes that have any additional roles except the
`node-role.kubernetes.io/worker` role. View the following sample of the
function:

``` yaml
...
objectDefinition:
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: my-configmap
  data:
    key: '{{ hasNodesWithExactRoles "infra" }}'
```

##### *skipObject*

The `skipObject` function is only available in managed cluster templates
in a `ConfigurationPolicy` resource. Calling `{{ skipObject }}` at any
time inside a Go template signals to skip that particular object for the
policy. When you use the `skipObject` with the `objectSelector`, you can
further filter objects selected by name. You can call `skipObject` by
itself inside a conditional or with an optional boolean argument.

View the following example that selects objects that have the label
`foo: bar`, but skips objects that have a name with the suffix `-prod`:

``` yaml
...
objectSelector:
  matchExpressions:
  - key: foo
    operator: In
    values:
    - bar
objectDefinition:
  apiVersion: v1
  kind: ConfigMap
  data:
    key: '{{ skipObject (hasSuffix "-prod" .ObjectName) }}{{ hasNodesWithExactRoles "infra" }}'
```

##### Sprig open source

Red Hat Advanced Cluster Management supports the following template
functions that are included from the `sprig` open source project:

- Sprig library: Cryptographic and security - Functions: htpasswd

- Sprig library: Date - Functions: date, mustToDate, now, toDate

- Sprig library: Default - Functions: default, empty, fromJson,
  mustFromJson, ternary, toJson, toRawJson, mustToRawJsonThe Json
  functions listed are also aliased to an equivalent uppercase JSON
  function.

- Sprig library: Dictionaries and dict - Functions: dict, dig, get,
  hasKey, keys, merge, mustMerge, set, unset, values

- Sprig library: Encoding - Functions: b64dec, b64enc

- Sprig library: Flow control - Functions: fail

- Sprig library: Integer math - Functions: add, mul, div, round, sub

- Sprig library: Integer slice - Functions: until, untilStep,

- Sprig library: Lists - Functions: append, has, list, mustAppend,
  mustHas, mustPrepend, mustSlice, prepend, slice

- Sprig library: String lists - Functions: concat, join, sortAlpha,
  split, splitn, splitList

- Sprig library: Strings - Functions: cat, contains, hasPrefix,
  hasSuffix, lower, mustRegexFind, mustRegexFindAll, mustRegexMatch,
  quote, regexFind, regexFindAll, regexMatch, regexQuoteMeta, replace,
  substr, trim, trimAll, trunc, upper

- Sprig library: Version comparison - Functions: semver, semverCompare

### Using advanced template processing in policies

Use both managed cluster and hub cluster templates to reduce the need to
create separate policies for each target cluster or hardcode
configuration values in the policy definitions. For security, both
resource-specific and the generic lookup functions in hub cluster
templates are restricted to the namespace of the policy on the hub
cluster.

**Important:** If you use hub cluster templates to propagate secrets or
other sensitive data, that causes sensitive data exposure in the managed
cluster namespace on the hub cluster and on the managed clusters where
that policy is distributed. The template content is expanded in the
policy, and policies are not encrypted by the OpenShift Container
Platform ETCD encryption support. To address this, use `fromSecret` or
`copySecretData`, which automatically encrypts the values from the
secret, or `protect` to encrypt other values.

#### Special annotation for reprocessing

Hub cluster templates are resolved to the data in the referenced
resources during policy creation, or when the referenced resources are
updated.

If you need to manually initiate an update, use the special annotation,
`policy.open-cluster-management.io/trigger-update`, to indicate changes
for the data referenced by the templates. Any change to the special
annotation value automatically initiates template processing.
Additionally, the latest contents of the referenced resource are read
and updated in the policy definition that is propagated for processing
on managed clusters. A way to use this annotation is to increment the
value by one each time.

#### Bypassing template processing

By default, Red Hat Advanced Cluster Management processes all Go
templates. You might create a policy that contains a template in
`policy-templates` that is not intended to be processed by Red Hat
Advanced Cluster Management. To bypass template processing for a
particular template, change `{{ template content }}` to
`` {{ `{{ template content }}` }} ``. Then, the template returns a raw
string to be processed by a subsequent templating engine.

If you want to completely bypass the template resolution for a
configuration policy, add the
`policy.open-cluster-management.io/disable-templates: "true"` annotation
in the relevant `ConfigurationPolicy` that is contained in your `Policy`
resource.

#### Configuration policy `objectSelector`

To iterate over many objects that are filtered by a label with
`ConfigurationPolicy`, use the `objectSelector` and specify the `kind`
in the `objectDefinition`. The `objectSelector` is similar to the
`namespaceSelector`, except that it does not have name filtering
capabilities. To filter by name, use the `skipObject` Go template
function. If you reference `{{ skipObject }}` at any time, it signals to
skip that particular object from those that are selected by the
`objectSelector` for the policy.

See the following YAML sample that selects objects that have the label
`foo: bar`, but skips objects that have a name with the suffix `-prod`:

``` yaml
...
objectSelector:
  matchExpressions:
  - key: foo
    operator: In
    values:
    - bar
objectDefinition:
  apiVersion: v1
  kind: ConfigMap
  data:
    key: '{{ if (hasSuffix "-prod" .ObjectName) }}{{ skipObject }}{{ end }}{{ hasNodesWithExactRoles "infra" }}'
```

#### Processing raw templates in configuration policies

The `object-template-raw` parameter is an optional parameter that
supports advanced templating use-cases, such as the `if` conditional
function and the `range` loop function. The `object-templates-raw`
parameter accepts a string containing Go templates, and when you use
these templates, they must result in an `object-templates` array.

For example, see the following YAML sample that adds the
`species-category: mammal` label to any `ConfigMap` in the `default`
namespace that has a `name` key equal to `Sea Otter`:

``` yaml
object-templates-raw: |
  {{- range (lookup "v1" "ConfigMap" "default" "").items }}
  {{- if eq .data.name "Sea Otter" }}
  - complianceType: musthave
    objectDefinition:
      kind: ConfigMap
      apiVersion: v1
      metadata:
        name: {{ .metadata.name }}
        namespace: {{ .metadata.namespace }}
        labels:
          species-category: mammal
  {{- end }}
  {{- end }}
```

**Note:** While `spec.object-templates` and `spec.object-templates-raw`
are optional, exactly one of the two parameter fields must be set.

View the following policy example that uses advanced templates to create
and configure infrastructure `MachineSet` objects for your managed
clusters.

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: create-infra-machineset
spec:
  remediationAction: enforce
  severity: low
  object-templates-raw: |
    {{- /* Specify the parameters needed to create the MachineSet  */ -}}
    {{- $machineset_role := "infra" }}
    {{- $region := "ap-southeast-1" }}
    {{- $zones := list "ap-southeast-1a" "ap-southeast-1b" "ap-southeast-1c" }}
    {{- $infrastructure_id := (lookup "config.openshift.io/v1" "Infrastructure" "" "cluster").status.infrastructureName }}
    {{- $worker_ms := (index (lookup "machine.openshift.io/v1beta1" "MachineSet" "openshift-machine-api" "").items 0) }}
    {{- /* Generate the MachineSet for each zone as specified  */ -}}
    {{- range $zone := $zones }}
    - complianceType: musthave
      objectDefinition:
        apiVersion: machine.openshift.io/v1beta1
        kind: MachineSet
        metadata:
          labels:
            machine.openshift.io/cluster-api-cluster: {{ $infrastructure_id }}
          name: {{ $infrastructure_id }}-{{ $machineset_role }}-{{ $zone }}
          namespace: openshift-machine-api
        spec:
          replicas: 1
          selector:
            matchLabels:
              machine.openshift.io/cluster-api-cluster: {{ $infrastructure_id }}
              machine.openshift.io/cluster-api-machineset: {{ $infrastructure_id }}-{{ $machineset_role }}-{{ $zone }}
          template:
            metadata:
              labels:
                machine.openshift.io/cluster-api-cluster: {{ $infrastructure_id }}
                machine.openshift.io/cluster-api-machine-role: {{ $machineset_role }}
                machine.openshift.io/cluster-api-machine-type: {{ $machineset_role }}
                machine.openshift.io/cluster-api-machineset: {{ $infrastructure_id }}-{{ $machineset_role }}-{{ $zone }}
            spec:
              metadata:
                labels:
                  node-role.kubernetes.io/{{ $machineset_role }}: ""
              taints:
                - key: node-role.kubernetes.io/{{ $machineset_role }}
                  effect: NoSchedule
              providerSpec:
                value:
                  ami:
                    id: {{ $worker_ms.spec.template.spec.providerSpec.value.ami.id }}
                  apiVersion: awsproviderconfig.openshift.io/v1beta1
                  blockDevices:
                    - ebs:
                        encrypted: true
                        iops: 2000
                        kmsKey:
                          arn: ''
                        volumeSize: 500
                        volumeType: io1
                  credentialsSecret:
                    name: aws-cloud-credentials
                  deviceIndex: 0
                  instanceType: {{ $worker_ms.spec.template.spec.providerSpec.value.instanceType }}
                  iamInstanceProfile:
                    id: {{ $infrastructure_id }}-worker-profile
                  kind: AWSMachineProviderConfig
                  placement:
                    availabilityZone: {{ $zone }}
                    region: {{ $region }}
                  securityGroups:
                    - filters:
                        - name: tag:Name
                          values:
                            - {{ $infrastructure_id }}-worker-sg
                  subnet:
                    filters:
                      - name: tag:Name
                        values:
                          - {{ $infrastructure_id }}-private-{{ $zone }}
                  tags:
                    - name: kubernetes.io/cluster/{{ $infrastructure_id }}
                      value: owned
                  userDataSecret:
                    name: worker-user-data
    {{- end }}
```

#### Resolving hub templates after defining configuration policies

By default, if you use the hub templates in the `ConfigurationPolicy`
and `OperatorPolicy` resources, you must correspond the `Policy`
resources that are defined on the hub cluster with these resources.

You can define configuration policies directly on the managed clusters.
For example, OpenShift GitOps is one that you can define configuration
policies directly on the managed cluster. To resolve hub templates on
the managed cluster in that situation, you can enable the
`governance-standalone-hub-templating` add-on.

To enable the `governance-standalone-hub-templating` add-on, complete
the following steps:

1.  On your hub cluster, go to the managed cluster namespace.

2.  Create a `ManagedClusterAddOn` resource with the
    `governance-standalone-hub-templating` name by using the following
    YAML sample:

    ``` yaml
    apiVersion: addon.open-cluster-management.io/v1alpha1
    kind: ManagedClusterAddOn
    metadata:
      name: governance-standalone-hub-templating
      namespace: <cluster name>
      labels:
        cluster.open-cluster-management.io/backup: ''
    spec:
      installNamespace: open-cluster-management-agent-addon
    ```

By default, the agent on the managed cluster only has access to the
`ManagedCluster` resources on the hub cluster. You can use the
`.ManagedClusterLabels` template variable in the hub cluster templates
inside the `ConfigurationPolicies` that are deployed directly to the
managed cluster.

If you want the hub template to access other resources, such as the
`lookup` or `fromConfigMap` function calls, you must add those specific
permissions to the add-on group. You can add these permissions through
resources, such as `Roles`, `ClusterRoles`, `RoleBindings`, and
`ClusterRoleBindings`.

The name of the add-on group depends on the name of your managed
cluster, but it has the following standard form:
`system:open-cluster-management:cluster:<cluster name>:addon:governance-standalone-hub-templating`.

To allow access to `Configmaps` in your managed cluster namespace on
your hub cluster, complete the following steps:

1.  Add the `Role` resource by running the following command:

    ``` bash
    oc create role -n <cluster name> cm-reader --verb=get,list,watch --resource=configmaps
    ```

2.  Add the `Rolebinding` by running the following command:

    ``` bash
    oc create rolebinding -n <cluster name> cm-reader-binding --role=cm-reader --group=system:open-cluster-management:cluster:<cluster name>:addon:governance-standalone-hub-templating
    ```

3.  To ensure these resources on the hub cluster get backed up and
    restored, add the following label to each resource that you create:
    `cluster.open-cluster-management.io/backup`.

After you add these resources, the add-on can resolve the hub templates,
and the state of the policy gets saved on a secret on the managed
clusters. This secret prevents interruptions if the hub cluster becomes
temporarily unavailable to the managed cluster.

# Policy deployment

The Kubernetes API is used to define and interact with policies. You are
responsible for ensuring that the environment meets internal enterprise
security standards for software engineering, secure engineering,
resiliency, security, and regulatory compliance for workloads hosted on
Kubernetes clusters.

## Deployment options

The `CertificatePolicy`, `ConfigurationPolicy`, and `OperatorPolicy`
policies and Gatekeeper constraints can be deployed to your managed
clusters in two ways. You can deploy policies to your managed clusters
by using the *Hub cluster policy framework* or *Deploying policies with
external tools*. View the following descriptions of each option:

Hub cluster policy framework  
The first approach is to leverage the policy framework on the hub
cluster. This involves defining the policies and Gatekeeper constraints
within a `Policy` object on the hub cluster and leveraging a `Placement`
and `PlacementBinding` to select which clusters the policies get
deployed to. The policy framework handles the delivery to the managed
cluster and the status aggregation back to the hub cluster. The `Policy`
objects are represented in the *Policies* table in the Red Hat Advanced
Cluster Management for Kubernetes console.

Deploying policies with external tools  
Alternatively, you can use an external tool, such as Red Hat OpenShift
GitOps, to deliver the policies and Gatekeeper constraints directly to
the managed cluster. Your policies are shown in the *Discovered
policies* table in the Red Hat Advanced Cluster Management console and
can be a helpful option if a configuration management strategy is
already in place, but there is a desire to supplement the strategy with
Red Hat Advanced Cluster Management policies.

See the following comparison table to learn which option supports
specific features, which helps you make a decision on which deployment
strategy is more suitable for your use case:

- Feature: Hub cluster templating - Policy framework: Yes - Deployed
  with external tools: Yes, but requires additional setup.

- Feature: Managed cluster templating - Policy framework: Yes - Deployed
  with external tools: Yes

- Feature: Red Hat Advanced Cluster Management console support - Policy
  framework: Yes - Deployed with external tools: Yes, you can view
  policies that are deployed by external tools from the Discover
  policies table. Policies that are deployed with external tools are not
  displayed from the Governance Overview dashboard. You must enable
  Search on your managed cluster.

- Feature: Policy grouping - Policy framework: Yes, you can have a
  combination of statuses and deployments through Policy and PolicySet
  resources. - Deployed with external tools: You can use Kubernetes
  labels on the policy resources to logically group related policies and
  view the in the Discovered policies table. You can also use Argo CD
  Application objects for grouping and to get a high-level status.

- Feature: Policy event history - Policy framework: You can view the
  last 10 events per cluster per policy stored on the hub cluster. -
  Deployed with external tools: No, but you can scrape the policy event
  history from the controller logs on each managed cluster.

- Feature: Policy dependencies - Policy framework: Yes - Deployed with
  external tools: No. Alternatively, you can use the Argo CD sync waves
  feature to define dependencies.

- Feature: Policy Generator - Policy framework: Yes - Deployed with
  external tools: No

- Feature: OpenShift GitOps health checksYou must complete extra
  configuration for Argo CD versions earlier than 2.13. - Policy
  framework: Yes - Deployed with external tools: Yes

- Feature: OpenShift GitOps applying native Kubernetes manifests and Red
  Hat Advanced Cluster Management policy on the managed cluster - Policy
  framework: No, you must deploy a policy on your Red Hat Advanced
  Cluster Management hub cluster. - Deployed with external tools: Yes

- Feature: Policy status metric on the hub cluster for alerts - Policy
  framework: Yes - Deployed with external tools: Yes,
  cluster_policy_governance_info.

- Feature: Running Ansible jobs on violated policies - Policy framework:
  Yes, use the PolicyAutomation resource. - Deployed with external
  tools: No

## Hub cluster policy framework

To create and manage policies, gain visibility and remediate
configurations to meet standards, use the Red Hat Advanced Cluster
Management for Kubernetes Governance security policy framework. Red Hat
Advanced Cluster Management for Kubernetes governance provides an
extensible policy framework for enterprises to introduce their own
security policies.

You can create a `Policy` resource in any namespace on the hub cluster
except the managed cluster namespaces. If you create a policy in a
managed cluster namespace, it is deleted by Red Hat Advanced Cluster
Management. Each Red Hat Advanced Cluster Management policy can be
organized into one or more policy template definitions. For more details
about the policy elements, view the *Policy YAML table* section on this
page.

### Requirements

- Each policy requires a `Placement` resource that defines the clusters
  that the policy document is applied to, and a `PlacementBinding`
  resource that binds the Red Hat Advanced Cluster Management for
  Kubernetes policy.

  Policy resources are applied to cluster based on an associated
  `Placement` definition, where you can view a list of managed clusters
  that match a certain criteria. A sample `Placement` resource that
  matches all clusters that have the `environment=dev` label resembles
  the following YAML:

  ``` yaml
  apiVersion: cluster.open-cluster-management.io/v1beta1
  kind: Placement
  metadata:
    name: placement-policy-role
  spec:
    predicates:
    - requiredClusterSelector:
      labelSelector:
      matchExpressions:
        - {key: environment, operator: In, values: ["dev"]}
      tolerations:
          - key: cluster.open-cluster-management.io/unavailable
            operator: Exists
          - key: cluster.open-cluster-management.io/unreachable
            operator: Exists
  ```

  To learn more about placement and the supported criteria, see
  Placement overview in the Cluster lifecycle documentation.

- In addition to the `Placement` resource, you must create a
  `PlacementBinding` to bind your `Placement` resource to a policy. A
  sample `Placement` resource that matches all clusters that have the
  `environment=dev` label resembles the following YAML:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: PlacementBinding
  metadata:
    name: binding-policy-role
  placementRef:
    name: placement-policy-role 
    kind: Placement
    apiGroup: cluster.open-cluster-management.io
  subjects: 
  - name: policy-role
    kind: Policy
    apiGroup: policy.open-cluster-management.io
  ```

  - If you use the previous sample, make sure you update the name of the
    `Placement` resource in the `placementRef` section to match your
    placement name.

  - You must update the name of the policy in the `subjects` section to
    match your policy name. Use the
    `oc apply -f resource.yaml -n namespace` command to apply both the
    `Placement` and the `Placementbinding` resources. Make sure the
    policy, placement and placement binding are all created in the same
    namespace.

- To use a `Placement` resource, you must bind a `ManagedClusterSet`
  resource to the namespace of the `Placement` resource with a
  `ManagedClusterSetBinding` resource. Refer to Creating a
  ManagedClusterSetBinding resource for additional details.

- When you create a `Placement` resource for your policy from the
  console, the status of the placement toleration is automatically added
  to the `Placement` resource. See Adding a toleration to a placement
  for more details.

**Best practice:** Use the command line interface (CLI) to make updates
to the policies when you use the `Placement` resource.

### Hub cluster policy components

#### Policy YAML structure

When you create a policy, you must include required parameter fields and
values. Depending on your policy controller, you might need to include
other optional fields and values. View the following YAML structure for
policies:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  disabled:
  remediationAction:
  dependencies:
  - apiVersion: policy.open-cluster-management.io/v1
    compliance:
    kind: Policy
    name:
    namespace:
  policy-templates:
    - objectDefinition:
        apiVersion:
        kind:
        metadata:
          name:
        spec:
---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
bindingOverrides:
  remediationAction:
subFilter:
  name:
placementRef:
  name:
  kind: Placement
  apiGroup: cluster.open-cluster-management.io
subjects:
- name:
  kind:
  apiGroup:
---
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name:
spec:
```

#### Policy YAML table

View the following table for policy parameter descriptions:

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.annotations - Optional or required: Optional -
  Description: Used to specify a set of security details that describes
  the set of standards the policy is trying to validate. All annotations
  documented here are represented as a string that contains a
  comma-separated list.Note: You can view policy violations based on the
  standards and categories that you define for your policy on the
  Policies page, from the console.

- Field: bindingOverrides.remediationAction - Optional or required:
  Optional - Description: When this parameter is set to enforce, it
  provides a way for you to override the remediation action of the
  related PlacementBinding resources for configuration policies. The
  default value is null.

- Field: subFilter - Optional or required: Optional - Description: Set
  this parameter to restriction to select a subset of bound policies.
  The default value is null.

- Field: annotations.policy.open-cluster-management.io/standards -
  Optional or required: Optional - Description: The name or names of
  security standards the policy is related to. For example, National
  Institute of Standards and Technology (NIST) and Payment Card Industry
  (PCI).

- Field: annotations.policy.open-cluster-management.io/categories -
  Optional or required: Optional - Description: A security control
  category represent specific requirements for one or more standards.
  For example, a System and Information Integrity category might
  indicate that your policy contains a data transfer protocol to protect
  personal information, as required by the HIPAA and PCI standards.

- Field: annotations.policy.open-cluster-management.io/controls -
  Optional or required: Optional - Description: The name of the security
  control that is being checked. For example, Access Control or System
  and Information Integrity.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. If specified, the
  spec.remediationAction value that is defined overrides any
  remediationAction parameter defined in the child policies in the
  policy-templates section. For example, if the spec.remediationAction
  value is set to enforce, then the remediationAction in the
  policy-templates section is set to enforce during runtime.

- Field: spec.copyPolicyMetadata - Optional or required: Optional -
  Description: Specifies whether the labels and annotations of a policy
  should be copied when replicating the policy to a managed cluster. If
  you set to true, all of the labels and annotations of the policy are
  copied to the replicated policy. If you set to false, only the policy
  framework specific policy labels and annotations are copied to the
  replicated policy.

- Field: spec.dependencies - Optional or required: Optional -
  Description: Used to create a list of dependency objects detailed with
  extra considerations for compliance.

- Field: spec.policy-templates - Optional or required: Required -
  Description: Used to create one or more policies to apply to a managed
  cluster.

- Field: spec.policy-templates.extraDependencies - Optional or required:
  Optional - Description: For policy templates, this is used to create a
  list of dependency objects detailed with extra considerations for
  compliance.

- Field: spec.policy-templates.ignorePending - Optional or required:
  Optional - Description: Used to mark a policy template as compliant
  until the dependency criteria is verified.Important: Some policy kinds
  might not support the enforce feature.

#### Policy sample file

View the following YAML file which is a configuration policy for roles:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name: policy-role
  annotations:
    policy.open-cluster-management.io/standards: NIST SP 800-53
    policy.open-cluster-management.io/categories: AC Access Control
    policy.open-cluster-management.io/controls: AC-3 Access Enforcement
    policy.open-cluster-management.io/description:
spec:
  remediationAction: inform
  disabled: false
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name: policy-role-example
        spec:
          remediationAction: inform # the policy-template spec.remediationAction is overridden by the preceding parameter value for spec.remediationAction.
          severity: high
          namespaceSelector:
            include: ["default"]
          object-templates:
            - complianceType: mustonlyhave # role definition should exact match
              objectDefinition:
                apiVersion: rbac.authorization.k8s.io/v1
                kind: Role
                metadata:
                  name: sample-role
                rules:
                  - apiGroups: ["extensions", "apps"]
                    resources: ["deployments"]
                    verbs: ["get", "list", "watch", "delete","patch"]
---
apiVersion: policy.open-cluster-management.io/v1
kind: PlacementBinding
metadata:
  name: binding-policy-role
placementRef:
  name: placement-policy-role
  kind: Placement
  apiGroup: cluster.open-cluster-management.io
subjects:
- name: policy-role
  kind: Policy
  apiGroup: policy.open-cluster-management.io
---
apiVersion: cluster.open-cluster-management.io/v1beta1
kind: Placement
metadata:
  name: placement-policy-role
spec:
  predicates:
  - requiredClusterSelector:
      labelSelector:
        matchExpressions:
        - {key: environment, operator: In, values: ["dev"]}
    tolerations:
        - key: cluster.open-cluster-management.io/unavailable
          operator: Exists
        - key: cluster.open-cluster-management.io/unreachable
          operator: Exists
```

### Policy dependencies

Dependencies can be used to activate a policy only when other policies
on your cluster are in a certain state. When the dependency criteria is
not met, the policy is labeled as `Pending` and resources are not
created on your managed cluster. There are more details about the the
criteria status in the policy status.

You can use policy dependencies to control the ordering of how objects
are applied. For example, if you have a policy for an operator and
another policy for a resource that the operator manages, you can set a
dependency on the second policy so that it does not attempt to create
the resource until the operator is installed. This can help with the
performance on the managed cluster.

**Required access:** Policy administrator

**Important:**

- You cannot use a dependency to apply a policy on one cluster based on
  the status of a policy in another cluster.

- If you create a policy dependency with a period, `.`, in the name, you
  must also add the namespace to the start of the name in the dependency
  section and follow with a period. For example, a policy in the
  `default` namespace that is named, `my-4.17-policy` must be written as
  it is in the following example: `default.my-4.17-policy`.

View the following policy dependency example, where the
`ScanSettingBinding` is only created if the
`upstream-compliance-operator` policy is already compliant on the
managed cluster:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  annotations:
    policy.open-cluster-management.io/categories: CM Configuration Management
    policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
    policy.open-cluster-management.io/standards: NIST SP 800-53
    policy.open-cluster-management.io/description:
  name: moderate-compliance-scan
  namespace: default
spec:
  dependencies: 
  - apiVersion: policy.open-cluster-management.io/v1
    compliance: Compliant
    kind: Policy
    name: upstream-compliance-operator
    namespace: default
  disabled: false
  policy-templates:
  - extraDependencies: 
    - apiVersion: policy.open-cluster-management.io/v1
      kind: ConfigurationPolicy
      name: scan-setting-prerequisite
      compliance: Compliant
    ignorePending: false 
    objectDefinition:
      apiVersion: policy.open-cluster-management.io/v1
      kind: ConfigurationPolicy
      metadata:
        name: moderate-compliance-scan
      spec:
        object-templates:
        - complianceType: musthave
          objectDefinition:
            apiVersion: compliance.openshift.io/v1alpha1
            kind: ScanSettingBinding
            metadata:
              name: moderate
              namespace: openshift-compliance
            profiles:
            - apiGroup: compliance.openshift.io/v1alpha1
              kind: Profile
              name: ocp4-moderate
            - apiGroup: compliance.openshift.io/v1alpha1
              kind: Profile
              name: ocp4-moderate-node
            settingsRef:
              apiGroup: compliance.openshift.io/v1alpha1
              kind: ScanSetting
              name: default
        remediationAction: enforce
        severity: low
```

- The `dependencies` field is set on a `Policy` object, and the
  requirements apply to all policy templates in the policy.

- The `extraDependencies` field can be set on individual policy
  template. For example the parameter can be set for a configuration
  policy, and defines criteria that must be satisfied in addition to any
  `dependencies` set in the policy.

- The `ignorePending` field can be set on each individual policy
  template, and configures whether the `Pending` status on that template
  is considered as `Compliant` or `NonCompliant` when the overall policy
  compliance is calculated. By default, this is set to `false` and a
  `Pending` template causes the policy to be `NonCompliant`. When you
  set this to `true` the policy can still be `Compliant` when this
  template is `Pending`, which is useful when that is expected status of
  the template.

### Integrating Policy Generator

By integrating the Policy Generator, you can use it to automatically
build Red Hat Advanced Cluster Management for Kubernetes policies. To
integrate the Policy Generator, see Policy Generator.

For an example of what you can do with the Policy Generator, see
Generating a policy that installs the Compliance Operator.

### Policy Generator

The Policy Generator is a part of the Red Hat Advanced Cluster
Management for Kubernetes application lifecycle subscription Red Hat
OpenShift GitOps workflow that generates Red Hat Advanced Cluster
Management policies using Kustomize. The Policy Generator builds Red Hat
Advanced Cluster Management policies from Kubernetes manifest YAML
files, which are provided through a `PolicyGenerator` manifest YAML file
that is used to configure it. The Policy Generator is implemented as a
Kustomize generator plug-in. For more information on Kustomize, read the
*Kustomize documentation*.

#### Policy Generator capabilities

The integration of the Policy Generator with the Red Hat Advanced
Cluster Management application lifecycle subscription OpenShift GitOps
workflow simplifies the distribution of Kubernetes resource objects to
managed OpenShift Container Platform clusters, and Kubernetes clusters
through Red Hat Advanced Cluster Management policies.

Use the Policy Generator to complete the following actions:

- Convert any Kubernetes manifest files to Red Hat Advanced Cluster
  Management configuration policies, including manifests that are
  created from a Kustomize directory.

- Patch the input Kubernetes manifests before they are inserted into a
  generated Red Hat Advanced Cluster Management policy.

- Generate additional configuration policies so you can report on
  Gatekeeper policy violations through Red Hat Advanced Cluster
  Management for Kubernetes.

- Generate policy sets on the hub cluster.

#### Policy Generator configuration structure

The Policy Generator is a Kustomize generator plug-in that is configured
with a manifest of the `PolicyGenerator` kind and
`policy.open-cluster-management.io/v1` API version. Continue reading to
learn about the configuration structure:

- To use the plug-in, add a `generators` section in a
  `kustomization.yaml` file. View the following example:

  ``` yaml
  generators:
    - policy-generator-config.yaml 
  ```

  - The `policy-generator-config.yaml` file that is referenced in the
    previous example is a YAML file with the instructions of the
    policies to generate.

- A simple `PolicyGenerator` configuration file might resemble the
  following example, with `policyDefaults` and `policies`:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: PolicyGenerator
  metadata:
    name: config-data-policies
  policyDefaults:
    namespace: policies
    policySets: []
  policies:
    - name: config-data
      manifests:
        - path: configmap.yaml 
  ```

  - The `configmap.yaml` file represents a Kubernetes manifest YAML file
    to be included in the policy. Alternatively, you can set the path to
    a Kustomize directory, or a directory with multiple Kubernetes
    manifest YAML files. View the following `ConfigMap` example:

  ``` yaml
  apiVersion: v1
  kind: ConfigMap
  metadata:
    name: my-config
    namespace: default
  data:
    key1: value1
    key2: value2
  ```

- You can use the `object-templates-raw` manifest to automatically
  generate a `ConfigurationPolicy` resource with the content you add.
  For example, you can create a manifest file with the following syntax:

  ``` yaml
  object-templates-raw: |
    {{- range (lookup "v1" "ConfigMap" "my-namespace" "").items }}
    - complianceType: musthave
      objectDefinition:
        kind: ConfigMap
        apiVersion: v1
        metadata:
          name: {{ .metadata.name }}
          namespace: {{ .metadata.namespace }}
          labels:
            i-am-from: template
    {{- end }}
  ```

- After you create a manifest file, you can create a `PolicyGenerator`
  configuration file. See the following YAML example and for `path`,
  enter the path to your `manifest.yaml` file:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: PolicyGenerator
  metadata:
    name: config-data-policies
  policyDefaults:
    namespace: policies
    policySets: []
  policies:
    - name: config-data
      manifests:
        - path: manifest.yaml
  ```

- The generated `Policy` resource, along with the generated `Placement`
  resource, and `PlacementBinding` resource, might resemble the
  following examples. **Note:** Specifications for resources are
  described in the *Policy Generator configuration reference table*.

  ``` yaml
  apiVersion: cluster.open-cluster-management.io/v1beta1
  kind: Placement
  metadata:
    name: placement-config-data
    namespace: policies
  spec:
    predicates:
    - requiredClusterSelector:
        labelSelector:
          matchExpressions: []
      tolerations:
          - key: cluster.open-cluster-management.io/unavailable
            operator: Exists
          - key: cluster.open-cluster-management.io/unreachable
            operator: Exists
  ---
  apiVersion: policy.open-cluster-management.io/v1
  kind: PlacementBinding
  metadata:
    name: binding-config-data
    namespace: policies
  placementRef:
    apiGroup: cluster.open-cluster-management.io
    kind: Placement
    name: placement-config-data
  subjects:
  - apiGroup: policy.open-cluster-management.io
    kind: Policy
    name: config-data
  ---
  apiVersion: policy.open-cluster-management.io/v1
  kind: Policy
  metadata:
    annotations:
      policy.open-cluster-management.io/categories: CM Configuration Management
      policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
      policy.open-cluster-management.io/standards: NIST SP 800-53
      policy.open-cluster-management.io/description:
    name: config-data
    namespace: policies
  spec:
    disabled: false
    policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name: config-data
        spec:
          object-templates:
          - complianceType: musthave
            objectDefinition:
              apiVersion: v1
              data:
                key1: value1
                key2: value2
              kind: ConfigMap
              metadata:
                name: my-config
                namespace: default
          remediationAction: inform
          severity: low
  ```

#### Policy Generator configuration reference table

All the fields in the `policyDefaults` section, except for `namespace`,
can be overridden for each policy, and all the fields in the
`policySetDefaults` section can be overridden for each policy set.

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to PolicyGenerator to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: placementBindingDefaults.name - Optional or required:
  Optional - Description: If multiple policies use the same placement,
  this name is used to generate a unique name for the resulting
  PlacementBinding, binding the placement with the array of policies
  that reference it.

- Field: policyDefaults - Optional or required: Required - Description:
  Any default value listed here is overridden by an entry in the
  policies array except for namespace.

- Field: policyDefaults.namespace - Optional or required: Required -
  Description: The namespace of all the policies.

- Field: policyDefaults.complianceType - Optional or required:
  Optional - Description: Determines the policy controller behavior when
  comparing the manifest to objects on the cluster. The values that you
  can use are musthave, mustonlyhave, or mustnothave. The default value
  is musthave.

- Field: policyDefaults.metadataComplianceType - Optional or required:
  Optional - Description: Overrides complianceType when comparing the
  manifest metadata section to objects on the cluster. The values that
  you can use are musthave, and mustonlyhave. The default value is empty
  ({}) to avoid overriding the complianceType for metadata.

- Field: policyDefaults.categories - Optional or required: Optional -
  Description: Array of categories to be used in the
  policy.open-cluster-management.io/categories annotation. The default
  value is CM Configuration Management.

- Field: policyDefaults.controls - Optional or required: Optional -
  Description: Array of controls to be used in the
  policy.open-cluster-management.io/controls annotation. The default
  value is CM-2 Baseline Configuration.

- Field: policyDefaults.standards - Optional or required: Optional -
  Description: An array of standards to be used in the
  policy.open-cluster-management.io/standards annotation. The default
  value is NIST SP 800-53.

- Field: policyDefaults.policyAnnotations - Optional or required:
  Optional - Description: Annotations that the policy includes in the
  metadata.annotations section. It is applied for all policies unless
  specified in the policy. The default value is empty ({}).

- Field: policyDefaults.configurationPolicyAnnotations - Optional or
  required: Optional - Description: Key-value pairs of annotations to
  set on generated configuration policies. For example, you can disable
  policy templates by defining the following parameter:
  {"policy.open-cluster-management.io/disable-templates": "true"}. The
  default value is empty ({}).

- Field: policyDefaults.copyPolicyMetadata - Optional or required:
  Optional - Description: Copies the labels and annotations for all
  policies and adds them to a replica policy. Set to true by default. If
  set to false, only the policy framework specific policy labels and
  annotations are copied to the replicated policy.

- Field: policyDefaults.customMessage - Optional or required: Optional -
  Description: Configures the compliance messages emitted by the
  configuration policy to use one of the specified Go templates based on
  the current compliance.

- Field: policyDefaults.severity - Optional or required: Optional -
  Description: The severity of the policy violation. The default value
  is low.

- Field: policyDefaults.disabled - Optional or required: Optional -
  Description: Whether the policy is disabled, meaning it is not
  propagated and no status as a result. The default value is false to
  enable the policy.

- Field: policyDefaults.remediationAction - Optional or required:
  Optional - Description: The remediation mechanism of your policy. The
  parameter values are enforce and inform. The default value is inform.

- Field: policyDefaults.namespaceSelector - Optional or required:
  Required for namespaced objects that do not have a namespace
  specified - Description: Determines namespaces in the managed cluster
  that the object is applied to. The include and exclude parameters
  accept file path expressions to include and exclude namespaces by
  name. The matchExpressions and matchLabels parameters specify
  namespaces to include by label. Read the Kubernetes labels and
  selectors documentation. The resulting list is compiled by using the
  intersection of results from all parameters.

- Field: policyDefaults.objectSelector - Optional or required:
  Optional - Description: Defines the label selector for objects that
  are defined in the objectDefinition. If there is an object name that
  is defined in the objectDefinition, the objectSelector is ignored.

- Field: policyDefaults.evaluationInterval - Optional or required:
  Optional - Description: Specifies the frequency for a policy to be
  evaluated when it is in a particular compliance state. Use the
  parameters compliant and noncompliant. The default value for the
  compliant and noncompliant parameters is watch to leverage Kubernetes
  API watches instead of polling the Kubernetes API server.When managed
  clusters have low resources, the evaluation interval can be set to
  long polling intervals to reduce CPU and memory usage on the
  Kubernetes API and policy controller. These are in the format of
  durations. For example, 1h25m3s represents 1 hour, 25 minutes, and 3
  seconds. These can also be set to never to avoid evaluating the policy
  after it is in a particular compliance state.

- Field: policyDefaults.evaluationInterval.compliant - Optional or
  required: Optional - Description: Specifies the evaluation frequency
  for a compliant policy. If you want to enable the previous polling
  behavior, set this parameter to 10s.

- Field: policyDefaults.evaluationInterval.noncompliant - Optional or
  required: Optional - Description: Specifies the evaluation frequency
  for a non-compliant policy. If you want to enable the previous polling
  behavior, set this parameter to 10s.

- Field: policyDefaults.pruneObjectBehavior - Optional or required:
  Optional - Description: Determines whether objects created or
  monitored by the policy should be deleted when the policy is deleted.
  Pruning only takes place if the remediation action of the policy has
  been set to enforce. Example values are DeleteIfCreated, DeleteAll, or
  None. The default value is None.

- Field: policyDefaults.recreateOption - Optional or required:
  Optional - Description: Describes whether to delete and recreate an
  object when an update is required. The IfRequired value recreates the
  object when you update an immutable field. Without dry run update
  support, the IfRequired has no effect on clusters. The Always value
  always recreate the object if a mismatch is detected.When the
  remediationAction parameter is set to inform the RecreateOption value
  has no effect. The default value is None.

- Field: policyDefaults.recordDiff - Optional or required: Optional -
  Description: Specifies if and where to log the difference between the
  object on the cluster and the objectDefinition in the policy. Set to
  Log to log the difference in the controller logs or None to not log
  the difference. By default, this parameter is empty to not log the
  difference.

- Field: policyDefaults.dependencies - Optional or required: Optional -
  Description: A list of objects that must be in specific compliance
  states before this policy is applied. Cannot be specified when
  policyDefaults.orderPolicies is set to true.

- Field: policyDefaults.dependencies\[\].name - Optional or required:
  Required - Description: The name of the object being depended on.

- Field: policyDefaults.dependencies\[\].namespace - Optional or
  required: Optional - Description: The namespace of the object being
  depended on. The default is the namespace of policies set for the
  Policy Generator.

- Field: policyDefaults.dependencies\[\].compliance - Optional or
  required: Optional - Description: The compliance state the object
  needs to be in. The default value is Compliant.

- Field: policyDefaults.dependencies\[\].kind - Optional or required:
  Optional - Description: The kind of the object. By default, the kind
  is set to Policy, but can also be other kinds that have compliance
  state, such as ConfigurationPolicy.

- Field: policyDefaults.dependencies\[\].apiVersion - Optional or
  required: Optional - Description: The API version of the object. The
  default value is policy.open-cluster-management.io/v1.

- Field: policyDefaults.description - Optional or required: Optional -
  Description: The description of the policy you want to create.

- Field: policyDefaults.extraDependencies - Optional or required:
  Optional - Description: A list of objects that must be in specific
  compliance states before this policy is applied. The dependencies that
  you define are added to each policy template (for example,
  ConfigurationPolicy) separately from the dependencies list. Cannot be
  specified when policyDefaults.orderManifests is set to true.

- Field: policyDefaults.extraDependencies\[\].name - Optional or
  required: Required - Description: The name of the object being
  depended on.

- Field: policyDefaults.extraDependencies\[\].namespace - Optional or
  required: Optional - Description: The namespace of the object being
  depended on. By default, the value is set to the namespace of policies
  set for the Policy Generator.

- Field: policyDefaults.extraDependencies\[\].compliance - Optional or
  required: Optional - Description: The compliance state the object
  needs to be in. The default value is Compliant.

- Field: policyDefaults.extraDependencies\[\].kind - Optional or
  required: Optional - Description: The kind of the object. The default
  value is to Policy, but can also be other kinds that have a compliance
  state, such as ConfigurationPolicy.

- Field: policyDefaults.extraDependencies\[\].apiVersion - Optional or
  required: Optional - Description: The API version of the object. The
  default value is policy.open-cluster-management.io/v1.

- Field: policyDefaults.ignorePending - Optional or required: Optional -
  Description: Bypass compliance status checks when the Policy Generator
  is waiting for its dependencies to reach their desired states. The
  default value is false.

- Field: policyDefaults.orderPolicies - Optional or required: Optional -
  Description: Automatically generate dependencies on the policies so
  they are applied in the order you defined in the policies list. By
  default, the value is set to false. Cannot be specified at the same
  time as policyDefaults.dependencies.

- Field: policyDefaults.orderManifests - Optional or required:
  Optional - Description: Automatically generate extraDependencies on
  policy templates so that they are applied in the order you defined in
  the manifests list for that policy. Cannot be specified when
  policyDefaults.consolidateManifests is set to true. Cannot be
  specified at the same time as policyDefaults.extraDependencies.

- Field: policyDefaults.consolidateManifests - Optional or required:
  Optional - Description: This determines if a single configuration
  policy is generated for all the manifests being wrapped in the policy.
  If set to false, a configuration policy per manifest is generated. The
  default value is true.

- Field: policyDefaults.informGatekeeperPolicies (Deprecated) - Optional
  or required: Optional - Description: Set informGatekeeperPolicies to
  false to use Gatekeeper manifests directly without defining it in a
  configuration policy. When the policy references a violated Gatekeeper
  policy manifest, an additional configuration policy is generated in
  order to receive policy violations in Red Hat Advanced Cluster
  Management. The default value is true.

- Field: policyDefaults.informKyvernoPolicies - Optional or required:
  Optional - Description: When the policy references a Kyverno policy
  manifest, this determines if an additional configuration policy is
  generated to receive policy violations in Red Hat Advanced Cluster
  Management, when the Kyverno policy is violated. The default value is
  true.

- Field: policyDefaults.policyLabels - Optional or required: Optional -
  Description: Labels that the policy includes in its metadata.labels
  section. The policyLabels parameter is applied for all policies unless
  specified in the policy.

- Field: policyDefaults.gatekeeperEnforcementAction - Optional or
  required: Optional - Description: Overrides the spec.enforcementAction
  field of a Gatekeeper constraint. This only applies to Gatekeeper
  constraints and is ignored by other manifests. If not set, the
  spec.enforcementAction field does not change.

- Field: policyDefaults.policySets - Optional or required: Optional -
  Description: Array of policy sets that the policy joins. Policy set
  details can be defined in the policySets section. When a policy is
  part of a policy set, a placement binding is not generated for the
  policy since one is generated for the set. Set
  policies\[\].generatePlacementWhenInSet or
  policyDefaults.generatePlacementWhenInSet to override
  policyDefaults.policySets.

- Field: policyDefaults.generatePolicyPlacement - Optional or required:
  Optional - Description: Generate placement manifests for policies. Set
  to true by default. When set to false, the placement manifest
  generation is skipped, even if a placement is specified.

- Field: policyDefaults.generatePlacementWhenInSet - Optional or
  required: Optional - Description: When a policy is part of a policy
  set, by default, the generator does not generate the placement for
  this policy since a placement is generated for the policy set. Set
  generatePlacementWhenInSet to true to deploy the policy with both
  policy placement and policy set placement. The default value is false.

- Field: policyDefaults.placement - Optional or required: Optional -
  Description: The placement configuration for the policies. This
  defaults to a placement configuration that matches all clusters.

- Field: policyDefaults.placement.name - Optional or required:
  Optional - Description: Specifying a name to consolidate placements
  that contain the same cluster label selectors.

- Field: policyDefaults.placement.labelSelector - Optional or required:
  Optional - Description: Specify a placement by defining a cluster
  label selector using either key:value, or providing a
  matchExpressions, matchLabels, or both, with appropriate values. See
  placementPath to specify an existing file.

- Field: policyDefaults.placement.placementName - Optional or required:
  Optional - Description: Define this parameter to use a placement that
  already exists on the cluster. A Placement is not created, but a
  PlacementBinding binds the policy to this Placement.

- Field: policyDefaults.placement.placementPath - Optional or required:
  Optional - Description: To reuse an existing placement, specify the
  path relative to the location of the kustomization.yaml file. If
  provided, this placement is used by all policies by default. See
  labelSelector to generate a new Placement.

- Field: policyDefaults.placement.clusterSelector (Deprecated) -
  Optional or required: Optional - Description: PlacementRule is
  deprecated. Use labelSelector instead to generate a placement. Specify
  a placement rule by defining a cluster selector using either key:value
  or by providing matchExpressions, matchLabels, or both, with
  appropriate values. See placementRulePath to specify an existing file.

- Field: policyDefaults.placement.placementRuleName (Deprecated) -
  Optional or required: Optional - Description: PlacementRule is
  deprecated. Alternatively, use placementName to specify a placement.
  To use an existing placement rule on the cluster, specify the name for
  this parameter. A PlacementRule is not created, but a PlacementBinding
  binds the policy to the existing PlacementRule.

- Field: policyDefaults.placement.placementRulePath (Deprecated) -
  Optional or required: Optional - Description: PlacementRule is
  deprecated. Alternatively, use placementPath to specify a placement.
  To reuse an existing placement rule, specify the path relative to the
  location of the kustomization.yaml file. If provided, this placement
  rule is used by all policies by default. See clusterSelector to
  generate a new PlacementRule.

- Field: policySetDefaults - Optional or required: Optional -
  Description: Default values for policy sets. Any default value listed
  for this parameter is overridden by an entry in the policySets array.

- Field: policySetDefaults.placement - Optional or required: Optional -
  Description: The placement configuration for the policies. This
  defaults to a placement configuration that matches all clusters. See
  policyDefaults.placement for description of this field.

- Field: policySetDefaults.generatePolicySetPlacement - Optional or
  required: Optional - Description: Generate placement manifests for
  policy sets. Set to true by default. When set to false the placement
  manifest generation is skipped, even if a placement is specified.

- Field: policies - Optional or required: Required - Description: The
  list of policies to create along with overrides to either the default
  values, or the values that are set in policyDefaults. See
  policyDefaults for additional fields and descriptions.

- Field: policies.description - Optional or required: Optional -
  Description: The description of the policy you want to create.

- Field: policies\[\].name - Optional or required: Required -
  Description: The name of the policy to create.

- Field: policies\[\].manifests - Optional or required: Required -
  Description: The list of Kubernetes object manifests to include in the
  policy, along with overrides to either the default values, the values
  set in this policies item, or the values set in policyDefaults. See
  policyDefaults for additional fields and descriptions. When
  consolidateManifests is set to true, only complianceType,
  metadataComplianceType, and recordDiff can be overridden at the
  policies\[\].manifests level.

- Field: policies\[\].manifests\[\].path - Optional or required:
  Required - Description: Path to a single file, a flat directory of
  files, or a Kustomize directory relative to the kustomization.yaml
  file. If the directory is a Kustomize directory, the generator runs
  Kustomize against the directory before generating the policies. If
  there is a requirement to process Helm charts for the Kustomize
  directory, set POLICY_GEN_ENABLE_HELM to true in the environment where
  the policy generator is running to enable Helm for the Policy
  Generator. The following manifests are supported: Non-root policy type
  manifests such as CertificatePolicy, ConfigurationPolicy,
  OperatorPolicy that have a Policy suffix. The previous manifests are
  not modified except for patches and are directly added as a
  policy-templates entry of the Policy resource. Gatekeeper constraints
  are also directly included if informGatekeeperPolicies is set to
  false. Manifests containing only an object-templates-raw key. The
  corresponding value is used directly in a generated
  ConfigurationPolicy resource without modification, which is added as a
  policy-templates entry of the Policy entry. For everything else,
  ConfigurationPolicy objects are generated to wrap the previously
  mentioned manifests. The resulting ConfigurationPolicy manifest is
  added as a policy-templates entry of the Policy resource.

- Field: policies\[\].manifests\[\].name - Optional or required:
  Optional - Description: Serves as the ConfigurationPolicy resource
  name when ConsolidateManifests is set to false. If multiple manifests
  are present in the path, an index number is appended. If multiple
  manifests are present and their names are provided, with
  consolidateManifests set to true, the name of the first manifest is
  used for all manifest paths.

- Field: policies\[\].manifests\[\].patches - Optional or required:
  Optional - Description: A list of Kustomize patches to apply to the
  manifest at the path. If there are multiple manifests, the patch
  requires the following fields: apiVersion, kind, metadata.name, and
  metadata.namespace. To ensure a Kustomize patch is applied to the
  correct manifest, set values for the fields specified earlier. If
  there is a single manifest, you can patch the metadata.name and
  metadata.namespace parameters. For more details, see the Kustomize
  documentation on strategic merge patches.

- Field: policies\[\].manifests\[\].openapi.path - Optional or required:
  Optional - Description: Use the openapi.path field to specify the path
  to an OpenAPI schema file to be used when patching the manifest. This
  is useful when patching the arrays of a custom resource. See the
  Kustomize documentation on openapi for details.

- Field: policies.policyLabels - Optional or required: Optional -
  Description: Labels that the policy includes in its metadata.labels
  section. The policyLabels parameter is applied for all policies unless
  specified in the policy.

- Field: policySets - Optional or required: Optional - Description: The
  list of policy sets to create, along with overrides to either the
  default values or the values that are set in policySetDefaults. To
  include a policy in a policy set, use policyDefaults.policySets,
  policies\[\].policySets, or policySets.policies. See policySetDefaults
  for additional fields and descriptions.

- Field: policySets\[\].name - Optional or required: Required -
  Description: The name of the policy set to create.

- Field: policySets\[\].description - Optional or required: Optional -
  Description: The description of the policy set to create.

- Field: policySets\[\].policies - Optional or required: Optional -
  Description: The list of policies to be included in the policy set. If
  policyDefaults.policySets or policies\[\].policySets is also
  specified, the lists are merged.

### Generating a policy that installs the Compliance Operator

Generate a policy that installs the Compliance Operator onto your
clusters. For an operator that uses the *namespaced* installation mode,
such as the Compliance Operator, an `OperatorGroup` manifest is also
required.

Complete the following steps:

1.  Create a YAML file with a `Namespace`, a `Subscription`, and an
    `OperatorGroup` manifest called `compliance-operator.yaml`. The
    following example installs these manifests in the
    `compliance-operator` namespace. Replace `<release-0.x>` with the
    correct channel:

    ``` yaml
    apiVersion: v1
    kind: Namespace
    metadata:
      name: openshift-compliance
    ---
    apiVersion: operators.coreos.com/v1
    kind: OperatorGroup
    metadata:
      name: compliance-operator
      namespace: openshift-compliance
    spec:
      targetNamespaces:
        - openshift-compliance
    ---
    apiVersion: operators.coreos.com/v1alpha1
    kind: Subscription
    metadata:
      name: compliance-operator
      namespace: openshift-compliance
    spec:
      channel: <release-0.x>
      name: compliance-operator
      source: redhat-operators
      sourceNamespace: openshift-marketplace
    ```

2.  Create a `PolicyGenerator` configuration file. View the following
    `PolicyGenerator` policy example that installs the Compliance
    Operator on all OpenShift Container Platform managed clusters:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: PolicyGenerator
    metadata:
      name: install-compliance-operator
    policyDefaults:
      namespace: policies
      placement:
        labelSelector:
          matchExpressions:
            - key: vendor
              operator: In
              values:
                - "OpenShift"
    policies:
      - name: install-compliance-operator
        manifests:
          - path: compliance-operator.yaml
    ```

3.  Add the policy generator to your `kustomization.yaml` file. The
    `generators` section might resemble the following configuration:

    ``` yaml
    generators:
      - policy-generator-config.yaml
    ```

    As a result, the generated policy resembles the following file:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: Placement
    metadata:
      name: placement-install-compliance-operator
      namespace: policies
    spec:
      predicates:
      - requiredClusterSelector:
          labelSelector:
            matchExpressions:
            - key: vendor
              operator: In
              values:
              - OpenShift
        tolerations:
            - key: cluster.open-cluster-management.io/unavailable
              operator: Exists
            - key: cluster.open-cluster-management.io/unreachable
              operator: Exists
    ---
    apiVersion: policy.open-cluster-management.io/v1
    kind: PlacementBinding
    metadata:
      name: binding-install-compliance-operator
      namespace: policies
    placementRef:
      apiGroup: cluster.open-cluster-management.io
      kind: Placement
      name: placement-install-compliance-operator
    subjects:
      - apiGroup: policy.open-cluster-management.io
        kind: Policy
        name: install-compliance-operator
    ---
    apiVersion: policy.open-cluster-management.io/v1
    kind: Policy
    metadata:
      annotations:
        policy.open-cluster-management.io/categories: CM Configuration Management
        policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
        policy.open-cluster-management.io/standards: NIST SP 800-53
        policy.open-cluster-management.io/description:
      name: install-compliance-operator
      namespace: policies
    spec:
      disabled: false
      policy-templates:
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: install-compliance-operator
            spec:
              object-templates:
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: v1
                    kind: Namespace
                    metadata:
                      name: openshift-compliance
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: operators.coreos.com/v1alpha1
                    kind: Subscription
                    metadata:
                      name: compliance-operator
                      namespace: openshift-compliance
                    spec:
                      channel: <release-0.x>
                      name: compliance-operator
                      source: redhat-operators
                      sourceNamespace: openshift-marketplace
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: operators.coreos.com/v1
                    kind: OperatorGroup
                    metadata:
                      name: compliance-operator
                      namespace: openshift-compliance
                    spec:
                      targetNamespaces:
                        - compliance-operator
              remediationAction: enforce
              severity: low
    ```

### Governance policy framework architecture

Enhance the security for your cluster with the Red Hat Advanced Cluster
Management for Kubernetes governance lifecycle. The product governance
lifecycle is based on using supported policies, processes, and
procedures to manage security and compliance from a central interface
page. View the following diagram of the governance architecture:

View the following component descriptions for the governance
architecture diagram:

- **Governance policy framework:** The previous image represents the
  framework that runs as the `governance-policy-framework` pod on
  managed clusters and contains the following controllers:

  - **Spec sync controller:** Synchronizes the replicated policy in the
    managed cluster namespace on the hub cluster to the managed cluster
    namespace on the managed cluster.

  - **Status sync controller:** Records compliance events from policy
    controllers in the replicated policies on the hub and managed
    cluster. The status only contains updates that are relevant to the
    current policy and does not consider past statuses if the policy is
    deleted and recreated.

  - **Template sync controller:** Creates, updates, and deletes objects
    in the managed cluster namespace on the managed cluster based on the
    definitions from the replicated policy `spec.policy-templates`
    entries.

  - **Gatekeeper sync controller:** Records Gatekeeper constraint audit
    results as compliance events in corresponding Red Hat Advanced
    Cluster Management policies.

- **Policy propagator controller:** Runs on the Red Hat Advanced Cluster
  Management hub cluster and generates the replicated policies in the
  managed cluster namespaces on the hub based on the placements bound to
  the root policy. It also aggregates compliance status from replicated
  policies to the root policy status and initiates automations based on
  policy automations bound to the root policy.

- **Governance policy add-on controller:** Runs on the Red Hat Advanced
  Cluster Management hub cluster and manages the installation of policy
  controllers on managed clusters.

#### Governance architecture components

The governance architecture also include following components:

- **Governance dashboard:** Provides a summary of your cloud governance
  and risk details, which include policy and cluster violations. Refer
  to the *Manage Governance dashboard* section to learn about the
  structure of an Red Hat Advanced Cluster Management for Kubernetes
  policy framework, and how to use the Red Hat Advanced Cluster
  Management for Kubernetes *Governance* dashboard.

  **Notes:**

  - When a policy is propagated to a managed cluster, it is first
    replicated to the cluster namespace on the hub cluster, and is named
    and labeled using `namespaceName.policyName`. When you create a
    policy, make sure that the length of the `namespaceName.policyName`
    does not exceed 63 characters due to the Kubernetes length limit for
    label values.

  - When you search for a policy in the hub cluster, you might also
    receive the name of the replicated policy in the managed cluster
    namespace. For example, if you search for `policy-dhaz-cert` in the
    `default` namespace, the following policy name from the hub cluster
    might also appear in the managed cluster namespace:
    `default.policy-dhaz-cert`.

- **Policy-based governance framework:** Supports policy creation and
  deployment to various managed clusters based on attributes associated
  with clusters, such as a geographical region. There are examples of
  the predefined policies and instructions on deploying policies to your
  cluster in the *open source community*. Additionally, when policies
  are violated, automations can be configured to run and take any action
  that the user chooses.

- **Open source community:** Supports community contributions with a
  foundation of the Red Hat Advanced Cluster Management policy
  framework. Policy controllers and third-party policies are also a part
  of the `open-cluster-management-io` project. You can contribute and
  deploy policies using GitOps.

### Governance dashboard

Manage your security policies and policy violations by using the
*Governance* dashboard to create, view, and edit your resources. You can
create YAML files for your policies from the command line and console.
Continue reading for details about the *Governance* dashboard from the
console.

#### Governance page

The following tabs are displayed on the *Governance* page *Overview*,
*Policy sets*, and *Policies*. Read the following descriptions to know
which information is displayed:

- **Overview**

  The following summary cards are displayed from the *Overview* tab:
  *Policy set violations*, *Policy violations*, *Clusters*,
  *Categories*, *Controls*, and *Standards*.

- **Policy sets**

  Create and manage hub cluster policy sets.

- **Policies**

  - Create and manage security policies. The table of policies list the
    following details of a policy: *Name*, *Namespace*, and *Cluster
    violations* are displayed.

  - You can edit, enable or disable, set remediation to inform or
    enforce, or remove a policy by selecting the **Actions** icon. You
    can view the categories and standards of a specific policy by
    selecting the drop-down arrow to expand the row.

  - Reorder your table columns in the *Manage column* dialog box. Select
    the *Manage column* icon for the dialog box to be displayed. To
    reorder your columns, select the *Reorder* icon and move the column
    name. For columns that you want to appear in the table, click the
    checkbox for specific column names and select the **Save** button.

  - Complete bulk actions by selecting multiple policies and clicking
    the **Actions** button. You can also customize your policy table by
    clicking the **Filter** button.

    When you select a policy in the table list, the following tabs of
    information are displayed from the console:

    - *Details*: Select the *Details* tab to view policy details and
      placement details. In the *Placement* table, the *Compliance*
      column provides links to view the compliance of the clusters that
      are displayed.

    - *Results*: Select the *Results* tab to view a table list of all
      clusters that are associated to the policy.

- From the *Message* column, click the **View details** link to view the
  template details, template YAML, and related resources. You can also
  view related resources. Click the **View history** link to view the
  violation message and a time of the last report.

#### Governance automation configuration

If there is a configured automation for a specific policy, you can
select the automation to view more details. View the following
descriptions of the schedule frequency options for your automation:

- *Manual run*: Manually set this automation to run once. After the
  automation runs, it is set to `disabled`. **Note:** You can only
  select *Manual run* mode when the schedule frequency is disabled.

- *Run once mode*: When a policy is violated, the automation runs one
  time. After the automation runs, it is set to `disabled`. After the
  automation is set to `disabled`, you must continue to run the
  automation manually. When you run *once mode*, the extra variable of
  `target_clusters` is automatically supplied with the list of clusters
  that violated the policy. The Ansible Automation Platform Job template
  must have `PROMPT ON LAUNCH` enabled for the `EXTRA VARIABLES` section
  (also known as `extra_vars`).

- *Run everyEvent mode*: When a policy is violated, the automation runs
  every time for each unique policy violation per managed cluster. Use
  the `DelayAfterRunSeconds` parameter to set the minimum seconds before
  an automation can be restarted on the same cluster. If the policy is
  violated multiple times during the delay period and kept in the
  violated state, the automation runs one time after the delay period.
  The default is 0 seconds and is only applicable for the `everyEvent`
  mode. When you run `everyEvent` mode, the extra variable of
  `target_clusters` and Ansible Automation Platform Job template is the
  same as *once mode*.

- *Disable automation*: When the scheduled automation is set to
  `disabled`, the automation does not run until the setting is updated.

The following variables are automatically provided in the `extra_vars`
of the Ansible Automation Platform Job:

- `policy_name`: The name of the non-compliant root policy that
  initiates the Ansible Automation Platform job on the hub cluster.

- `policy_namespace`: The namespace of the root policy.

- `hub_cluster`: The name of the hub cluster, which is determined by the
  value in the `clusters` `DNS` object.

- `policy_sets`: This parameter contains all associated policy set names
  of the root policy. If the policy is not within a policy set, the
  `policy_set` parameter is empty.

- `policy_violations`: This parameter contains a list of non-compliant
  cluster names, and the value is the policy `status` field for each
  non-compliant cluster.

### Creating configuration policies

You can create a YAML file for your configuration policy from the
command line interface (CLI) or from the console. As you create a
configuration policy from the console, a YAML file is displayed in the
YAML editor.

#### Prerequisites

- **Required access**: Administrator or cluster administrator

- If you have an existing Kubernetes manifest, consider using the Policy
  Generator to automatically include the manifests in a policy. See the
  Policy Generator documentation.

#### Creating a configuration policy from the CLI

Complete the following steps to create a configuration policy from the
(CLI):

1.  Create a YAML file for your configuration policy. Run the following
    command:

    ``` bash
    oc create -f configpolicy-1.yaml
    ```

    Your configuration policy might resemble the following policy:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: Policy
    metadata:
      name: policy-1
      namespace: my-policies
    policy-templates:
    - apiVersion: policy.open-cluster-management.io/v1
      kind: ConfigurationPolicy
      metadata:
        name: mustonlyhave-configuration
      spec:
        namespaceSelector:
          include: ["default"]
          exclude: ["kube-system"]
        remediationAction: inform
        disabled: false
        complianceType: mustonlyhave
        object-templates:
    ```

2.  Apply the policy by running the following command:

    ``` bash
    oc apply -f <policy-file-name>  --namespace=<namespace>
    ```

3.  Verify and list the policies by running the following command:

    ``` bash
    oc get policies.policy.open-cluster-management.io --namespace=<namespace>
    ```

Your configuration policy is created.

##### Viewing your configuration policy from the CLI

Complete the following steps to view your configuration policy from the
CLI:

1.  View details for a specific configuration policy by running the
    following command:

    ``` bash
    oc get policies.policy.open-cluster-management.io <policy-name> -n <namespace> -o yaml
    ```

2.  View a description of your configuration policy by running the
    following command:

    ``` bash
    oc describe policies.policy.open-cluster-management.io <name> -n <namespace>
    ```

##### Viewing your configuration policy from the console

View any configuration policy and its status from the console.

After you log in to your cluster from the console, select **Governance**
to view a table list of your policies. **Note:** You can filter the
table list of your policies by selecting the *All policies* tab or
*Cluster violations* tab.

Select one of your policies to view more details. The *Details*,
*Clusters*, and *Templates* tabs are displayed.

#### Disabling configuration policies

To disable your configuration policy, select **Disable policy** from the
*Actions* menu of the policy. The policy is disabled, but not deleted.

#### Deleting a configuration policy

Delete a configuration policy from the CLI or the console. Complete the
following steps:

1.  To delete the policy from your target cluster or clusters, run the
    following command:

    ``` bash
    oc delete policies.policy.open-cluster-management.io <policy-name> -n <namespace>
    ```

2.  Verify that your policy is removed by running the following command:

    ``` bash
    oc get policies.policy.open-cluster-management.io <policy-name> -n <namespace>
    ```

3.  To delete a configuration policy from the console, click the
    **Actions** icon for the policy you want to delete in the policy
    violation table and then click **Delete**.

Your policy is deleted.

### Configuring Ansible Automation Platform for Governance

Red Hat Advanced Cluster Management for Kubernetes Governance can be
integrated with Red Hat Ansible Automation Platform to create policy
violation automations. You can configure the automation from the Red Hat
Advanced Cluster Management console.

#### Prerequisites

- A supported OpenShift Container Platform version

- You must have Ansible Automation Platform version 3.7.3 or a later
  version installed. It is best practice to install the latest supported
  version of Ansible Automation Platform. See Red Hat Ansible Automation
  Platform documentation for more details.

- Install the Ansible Automation Platform Resource Operator from the
  Operator Lifecycle Manager. In the *Update Channel* section, select
  `stable-2.x-cluster-scoped`. Select the **All namespaces on the
  cluster (default)** installation mode.

  **Note:** Ensure that the Ansible Automation Platform job template is
  idempotent when you run it. If you do not have Ansible Automation
  Platform Resource Operator, you can find it from the Red Hat OpenShift
  Software Catalog.

For more information about installing and configuring Red Hat Ansible
Automation Platform, see Setting up Ansible tasks.

#### Creating a policy violation automation from the console

After you log in to your Red Hat Advanced Cluster Management hub
cluster, select **Governance** from the navigation menu, and then click
on the *Policies* tab to view the policy tables.

Configure an automation for a specific policy by clicking **Configure**
in the *Automation* column. You can create automation when the policy
automation panel appears. From the *Ansible credential* section, click
the drop-down menu to select an Ansible credential. If you need to add a
credential, see Managing credentials overview.

**Note:** This credential is copied to the same namespace as the policy.
The credential is used by the `AnsibleJob` resource that is created to
initiate the automation. Changes to the Ansible credential in the
*Credentials* section of the console is automatically updated.

After a credential is selected, click the Ansible job drop-down list to
select a job template. In the *Extra variables* section, add the
parameter values from the `extra_vars` section of the
`PolicyAutomation`. Select the frequency of the automation. You can
select *Run once mode*, *Run everyEvent mode*, or *Disable automation*.

Save your policy violation automation by selecting **Submit**. When you
select the *View Job* link from the Ansible job details side panel, the
link directs you to the job template on the *Search* page. After you
successfully create the automation, it is displayed in the *Automation*
column.

**Note:** When you delete a policy that has an associated policy
automation, the policy automation is automatically deleted as part of
clean up.

Your policy violation automation is created from the console.

#### Creating a policy violation automation from the CLI

Complete the following steps to configure a policy violation automation
from the CLI:

1.  From your terminal, log in to your Red Hat Advanced Cluster
    Management hub cluster using the `oc login` command.

2.  Find or create a policy that you want to add an automation to. Note
    the policy name and namespace.

3.  Create a `PolicyAutomation` resource using the following sample as a
    guide:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1beta1
    kind: PolicyAutomation
    metadata:
      name: policyname-policy-automation
    spec:
      automationDef:
        extra_vars:
          your_var: your_value
        name: Policy Compliance Template
        secret: ansible-tower
        type: AnsibleJob
      mode: disabled
      policyRef: policyname
    ```

4.  The Automation template name in the previous sample is
    `Policy Compliance Template`. Change that value to match your job
    template name.

5.  In the `extra_vars` section, add any parameters you need to pass to
    the Automation template.

6.  Set the mode to either `once`, `everyEvent`, or `disabled`.

7.  Set the `policyRef` to the name of your policy.

8.  Create a secret in the same namespace as this `PolicyAutomation`
    resource that contains the Ansible Automation Platform credential.
    In the previous example, the secret name is `ansible-tower`. Use the
    sample from application lifecycle to see how to create the secret.

9.  Create the `PolicyAutomation` resource.

    **Notes:**

    - An immediate run of the policy automation can be initiated by
      adding the following annotation to the `PolicyAutomation`
      resource:

      ``` yaml
      metadata:
        annotations:
          policy.open-cluster-management.io/rerun: "true"
      ```

    - When the policy is in `once` mode, the automation runs when the
      policy is non-compliant. The `extra_vars` variable, named
      `target_clusters` is added and the value is an array of each
      managed cluster name where the policy is non-compliant.

    - When the policy is in `everyEvent` mode and the
      `DelayAfterRunSeconds` exceeds the defined time value, the policy
      is non-compliant and the automation runs for every policy
      violation.

## Policy deployment with external tools

To deploy `CertificatePolicy`, `ConfigurationPolicy`, `OperatorPolicy`
resources, and Gatekeeper constraints directly to your managed cluster,
you can use an external tool such as Red Hat OpenShift GitOps.

### Deployment workflow

Your `CertificatePolicy`, `ConfigurationPolicy`, `OperatorPolicy`
policies must be in the `open-cluster-management-policies` namespace or
the managed cluster namespace. Policies in other namespaces are ignored
and do not receive a status. If you are using a Red Hat OpenShift GitOps
version with an Argo CD version earlier than 2.13, you must configure
Red Hat Advanced Cluster Management for Kubernetes policy health checks

The OpenShift GitOps service account must have permission to manage Red
Hat Advanced Cluster Management for Kubernetes policies. Deploy policies
with OpenShift GitOps and view the policies from the *Discovered
policies* table of the Governance dashboard. The policies are grouped by
the policy `name` and `kind` fields.

# Policy controller advanced configuration

## Configure the concurrency of the governance framework

Configure the concurrency of the governance framework for each managed
cluster. To change the default value of `2`, set the
`policy-evaluation-concurrency` annotation with a nonzero integer within
quotation marks. Then set the value on the `ManagedClusterAddOn` object
name to `governance-policy-framework` in the managed cluster namespace
of the hub cluster.

See the following YAML example where the concurrency is set to `2` on
the managed cluster named `cluster1`:

``` yaml
apiVersion: addon.open-cluster-management.io/v1alpha1
kind: ManagedClusterAddOn
metadata:
  name: governance-policy-framework
  namespace: cluster1
  annotations:
    policy-evaluation-concurrency: "2"
spec:
  installNamespace: open-cluster-management-agent-addon
```

To set the `client-qps` and `client-burst` annotations, update the
`ManagedClusterAddOn` resource and define the parameters.

See the following YAML example where the queries for each second is set
to `30` and the burst is set to `45` on the managed cluster called
`cluster1`:

``` yaml
apiVersion: addon.open-cluster-management.io/v1alpha1
kind: ManagedClusterAddOn
metadata:
  name: governance-policy-framework
  namespace: cluster1
  annotations:
    client-qps: "30"
    client-burst: "45"
spec:
  installNamespace: open-cluster-management-agent-addon
```

## Configure the concurrency of the configuration policy controller

You can configure the concurrency of the configuration policy controller
for each managed cluster to change how many configuration policies it
can evaluate at the same time. To change the default value of `2`, set
the `policy-evaluation-concurrency` annotation with a nonzero integer
within quotation marks. Then set the value on the `ManagedClusterAddOn`
object name to `config-policy-controller` in the managed cluster
namespace of the hub cluster.

**Note:** Increased concurrency values increase CPU and memory
utilization on the `config-policy-controller` pod, Kubernetes API
server, and OpenShift API server.

See the following YAML example where the concurrency is set to `5` on
the managed cluster named `cluster1`:

``` yaml
apiVersion: addon.open-cluster-management.io/v1alpha1
kind: ManagedClusterAddOn
metadata:
  name: config-policy-controller
  namespace: cluster1
  annotations:
    policy-evaluation-concurrency: "5"
spec:
  installNamespace: open-cluster-management-agent-addon
```

## Configure the rate of requests to the API server

Configure the rate of requests to the API server that the configuration
policy controller makes on each managed cluster. An increased rate
improves the responsiveness of the configuration policy controller,
which also increases the CPU and memory utilization of the Kubernetes
API server and OpenShift API server. By default, the rate of requests
scales with the `policy-evaluation-concurrency` setting and is set to
`30` queries for each second (QPS), with a `45` burst value,
representing a higher number of requests over short periods of time.

You can configure the rate and burst by setting the `client-qps` and
`client-burst` annotations with nonzero integers within quotation marks.
You can set the value on the `ManagedClusterAddOn` object name to
`config-policy-controller` in the managed cluster namespace of the hub
cluster.

See the following YAML example where the queries for each second is set
to `20` and the burst is set to `100` on the managed cluster called
`cluster1`:

``` yaml
apiVersion: addon.open-cluster-management.io/v1alpha1
kind: ManagedClusterAddOn
metadata:
  name: config-policy-controller
  namespace: cluster1
  annotations:
    client-qps: "20"
    client-burst: "100"
spec:
  installNamespace: open-cluster-management-agent-addon
```

## Configure debug log

When you configure and collect debug logs for each policy controller,
you can adjust the log level.

**Note:** Reducing the volume of debug logs means there is less
information displayed from the logs.

You can reduce the debug logs emitted by the policy controllers to be
display error-only bugs in the logs. To reduce the debug logs, set the
debug log value to `-1` in the annotation. See what each value
represents:

- `-1`: error logs only

- `0`: informative logs

- `1`: debug logs

- `2`: verbose debugging logs

To receive the second level of debugging information for the Kubernetes
configuration controller, add the `log-level` annotation with the value
of `2` to the `ManagedClusterAddOn` custom resource. By default, the
`log-level` is set to `0`, which means you receive informative messages.
View the following example:

``` yaml
apiVersion: addon.open-cluster-management.io/v1alpha1
kind: ManagedClusterAddOn
metadata:
  name: config-policy-controller
  namespace: cluster1
  annotations:
    log-level: "2"
spec:
  installNamespace: open-cluster-management-agent-addon
```

Additionally, for each `spec.object-template[]` in a
`ConfigurationPolicy` resource, you can set the parameter `recordDiff`
to `Log`. The difference between the `objectDefinition` and the object
on the managed cluster is logged in the `config-policy-controller` pod
on the managed cluster. View the following example:

This `ConfigurationPolicy` resource with `recordDiff: Log`:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: my-config-policy
spec:
  object-templates:
  - complianceType: musthave
    recordDiff: Log
    objectDefinition:
      apiVersion: v1
      kind: ConfigMap
      metadata:
        name: my-configmap
      data:
        fieldToUpdate: "2"
```

If the `ConfigMap` resource on the cluster lists `fieldToUpdate: "1"`,
then the diff appears in the `config-policy-controller` pod logs with
the following information:

    Logging the diff:
    --- default/my-configmap : existing
    +++ default/my-configmap : updated
    @@ -2,3 +2,3 @@
     data:
    -  fieldToUpdate: "1"
    +  fieldToUpdate: "2"
     kind: ConfigMap

**Important:** Avoid logging the difference for a secure object. The
difference is logged in plain text.

## Governance metric

The policy framework exposes metrics that show policy distribution and
status. Use the `policy_governance_info` metric on the hub cluster to
view trends and analyze any policy failures. See the following topics
for an overview of metrics:

### Metric: policy_governance_info

The OpenShift Container Platform monitoring component collects the
`policy_governance_info` metric. If you enable observability, the
component collects some aggregate data.

**Note:** If you enable observability, enter a query for the metric from
the Grafana *Explore* page. When you create a policy, you are creating a
*root* policy. The framework watches for root policies, `Placement`
resources, and `PlacementBindings` resources to for information about
where to create *propagated* policies, to distribute the policy to
managed clusters.

For both root and propagated policies, a metric of `0` is recorded if
the policy is compliant, `1` if it is non-compliant, and `-1` if it is
in an unknown or pending state.

The `policy_governance_info` metric uses the following labels:

- `type`: The label values are `root` or `propagated`.

- `policy`: The name of the associated root policy.

- `policy_namespace`: The namespace on the hub cluster where the root
  policy is defined.

- `cluster_namespace`: The namespace for the cluster where the policy is
  distributed.

These labels and values enable queries that can show us many things
happening in the cluster that might be difficult to track.

**Note:** If you do not need the metrics, and you have any concerns
about performance or security, you can disable the metric collection.
Set the `DISABLE_REPORT_METRICS` environment variable to `true` in the
propagator deployment. You can also add `policy_governance_info` metric
to the observability allowlist as a custom metric. See Adding custom
metrics for more details.

### Metric: cluster_policy_governance_info

The OpenShift Container Platform monitoring component collects the
`cluster_policy_governance_info` metric. If you enable observability,
the component collects the data.

**Note:** If you enable observability, enter a query for the metric from
the Grafana *Explore* page.

For managed cluster policies, a metric of `0` is recorded if the policy
is compliant, `1` if it is not compliant, and `-1` if it is in an
unknown or pending state.

The `cluster_policy_governance_info` metric uses the following labels:

- `kind`: The kind of the policy.

- `policy`: The name of the policy.

- `policy_namespace`: The namespace on the managed cluster where the
  policy is defined.

- `severity`: The severity specified on the policy.

Use these labels and values to enable detailed queries on changes in the
cluster that might be difficult to track.

**Note:** You can also add `cluster_policy_governance_info` metric to
the observability `allowlist` as a custom metric. For more details, see
Adding custom metrics.

### Metric: *config_policies_evaluation_duration_seconds*

The `config_policies_evaluation_duration_seconds` histogram tracks the
number of seconds it takes to process all configuration policies that
are ready to be evaluated on the cluster. Use the following metrics to
query the histogram:

- `config_policies_evaluation_duration_seconds_bucket`: The buckets are
  cumulative and represent seconds with the following possible entries:
  1, 3, 9, 10.5, 15, 30, 60, 90, 120, 180, 300, 450, 600, and greater.

- `config_policies_evaluation_duration_seconds_count`: The count of all
  events.

- `config_policies_evaluation_duration_seconds_sum`: The sum of all
  values.

Use the `config_policies_evaluation_duration_seconds` metric to
determine if the `ConfigurationPolicy` `evaluationInterval` setting
needs to be changed for resource intensive policies that do not need
frequent evaluation. You can also increase the concurrency at the cost
of higher resource utilization on the Kubernetes API server. See
*Configure the concurrency* section for more details.

To receive information about the time used to evaluate configuration
policies, perform a Prometheus query that resembles the following
expression:

`rate(config_policies_evaluation_duration_seconds_sum[10m])/rate (config_policies_evaluation_duration_seconds_count[10m]`

The `config-policy-controller` pod running on managed clusters in the
`open-cluster-management-agent-addon` namespace calculates the metric.
The `config-policy-controller` does not send the metric to observability
by default.

## Verify configuration changes

When you apply the new configuration with the controller, the
`ManifestApplied` parameter is updated in the `ManagedClusterAddOn`.
That condition timestamp helps verify the configuration correctly. For
example, this command can verify when the `cert-policy-controller` on
the `local-cluster` was updated:

    oc get -n <your-local-cluster-name> managedclusteraddon cert-policy-controller | grep -B4 'type: ManifestApplied'

You might receive the following output:

     - lastTransitionTime: "2023-01-26T15:42:22Z"
        message: manifests of addon are applied successfully
        reason: AddonManifestApplied
        status: "True"
        type: ManifestApplied

# Supported Red Hat Advanced Cluster Management for Kubernetes policies

View the supported policies to learn how to define rules, processes, and
controls on the hub cluster when you create and manage policies in Red
Hat Advanced Cluster Management for Kubernetes.

## Table of sample configuration policies

View the following sample configuration policies:

- Policy sample: Namespace policy - Description: Ensure consistent
  environment isolation and naming with namespaces.

- Policy sample: Pod policy - Description: Ensure cluster workload
  configuration.

- Policy sample: Memory usage policy - Description: Limit workload
  resource usage using limit ranges.

- Policy sample: Pod security policy (Deprecated) - Description: Ensure
  consistent workload security.

- Policy sample: Role policy and Role binding policy - Description:
  Manage role permissions and bindings using roles and role bindings.

- Policy sample: Security content constraints (SCC) policy -
  Description: Manage workload permissions with Security Context
  Constraints.

- Policy sample: ETCD encryption policy - Description: Ensure data
  security with etcd encryption.

- Policy sample: Compliance operator policy - Description: Deploy the
  Compliance Operator to scan and enforce the compliance state of
  clusters leveraging OpenSCAP.

- Policy sample: Compliance operator E8 scan - Description: After
  applying the Compliance operator policy, deploy an Essential 8 (E8)
  scan to check for compliance with E8 security profiles.

- Policy sample: Compliance operator CIS scan - Description: After
  applying the Compliance operator policy, deploy a Center for Internet
  Security (CIS) scan to check for compliance with CIS security
  profiles.

- Policy sample: Image vulnerability policy - Description: Deploy the
  Container Security Operator and detect known image vulnerabilities in
  pods running on the cluster.

- Policy sample: Gatekeeper operator deployment - Description:
  Gatekeeper is an admission webhook that enforces custom resource
  definition-based policies that are run by the Open Policy Agent (OPA)
  policy engine. The Gatekeeper operator is available for installing
  Gatekeeper.

- Policy sample: Gatekeeper compliance policy - Description: After
  deploying Gatekeeper to the clusters, deploy this sample Gatekeeper
  policy that ensures namespaces that are created on the cluster are
  labeled as specified.

- Policy sample: Red Hat OpenShift Platform Plus policy set -
  Description: Red Hat OpenShift Platform Plus is a hybrid-cloud suite
  of products to securely build, deploy, run, and manage applications
  for multiple infrastructures. You can deploy Red Hat OpenShift
  Platform Plus to managed clusters using PolicySets delivered through a
  Red Hat Advanced Cluster Management application.

Red Hat OpenShift Container Platform 4.x also supports the Red Hat
Advanced Cluster Management configuration policies.

## Namespace policy

The Kubernetes configuration policy controller monitors the status of
your namespace policy. Apply the namespace policy to define specific
rules for your namespace.

### Namespace policy YAML structure

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          object-templates:
            - complianceType:
              objectDefinition:
                kind: Namespace
                apiVersion: v1
                metadata:
                  name:
                ...
```

### Namespace policy YAML table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional because it
  overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

### Namespace policy sample

- To view the policy sample, see the `policy-namespace.yaml`.

- For more details, see Managing security policies.

- Refer to Hub cluster policy framework documentation, and to the
  Kubernetes configuration policy controller to learn about other
  configuration policies.

## Pod policy

The Kubernetes configuration policy controller monitors the status of
your pod policies. Apply the pod policy to define the container rules
for your pods. A pod must exist in your cluster to use this information.

### Pod policy YAML structure

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          namespaceSelector:
            exclude:
            include:
            matchLabels:
            matchExpressions:
          object-templates:
            - complianceType:
              objectDefinition:
                apiVersion: v1
                kind: Pod
                metadata:
                  name:
                spec:
                  containers:
                  - image:
                    name:
                ...
```

### Pod policy table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional because the
  value overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

### Pod policy sample

Refer to Kubernetes configuration policy controller to view other
configuration policies that are monitored by the configuration
controller, and see the Hub cluster policy framework to see a full
description of the policy YAML structure and additional fields. Return
to Creating configuration policies documentation to manage other
policies.

## Memory usage policy

The Kubernetes configuration policy controller monitors the status of
the memory usage policy. Use the memory usage policy to limit or
restrict your memory and compute usage. For more information, see *Limit
Ranges* in the Kubernetes documentation.

### Memory usage policy YAML structure

Your memory usage policy might resemble the following YAML file:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          namespaceSelector:
            exclude:
            include:
            matchLabels:
            matchExpressions:
          object-templates:
            - complianceType: mustonlyhave
              objectDefinition:
                apiVersion: v1
                kind: LimitRange
                metadata:
                  name:
                spec:
                  limits:
                  - default:
                      memory:
                    defaultRequest:
                      memory:
                    type:
        ...
```

### Memory usage policy table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional because the
  value overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

### Memory usage policy sample

- To view a sample of the policy, review the `policy-limitmemory.yaml`.

- For more details, see Managing security policies.

- Refer to the Hub cluster policy framework documentation, and to
  Kubernetes configuration policy controller to view other configuration
  policies that are monitored by the controller.

## Pod security policy (Deprecated)

The Kubernetes configuration policy controller monitors the status of
the pod security policy. Apply a pod security policy to secure pods and
containers.

### Pod security policy YAML structure

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          namespaceSelector:
            exclude:
            include:
            matchLabels:
            matchExpressions:
          object-templates:
            - complianceType:
              objectDefinition:
                apiVersion: policy/v1beta1
                kind: PodSecurityPolicy
                metadata:
                  name:
                  annotations:
                    seccomp.security.alpha.kubernetes.io/allowedProfileNames:
                spec:
                  privileged:
                  allowPrivilegeEscalation:
                  allowedCapabilities:
                  volumes:
                  hostNetwork:
                  hostPorts:
                  hostIPC:
                  hostPID:
                  runAsUser:
                  seLinux:
                  supplementalGroups:
                  fsGroup:
                ...
```

### Pod security policy table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional because the
  value overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

### Pod security policy sample

The support of pod security policies is removed from OpenShift Container
Platform and from Kubernetes v1.25 and later. If you apply a
`PodSecurityPolicy` resource, you might receive the following
non-compliant message:

    violation - couldn't find mapping resource with kind PodSecurityPolicy, please check if you have CRD deployed

## Role policy

The Kubernetes configuration policy controller monitors the status of
role policies. Define roles in the `object-template` to set rules and
permissions for specific roles in your cluster.

### Role policy YAML structure

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          namespaceSelector:
            exclude:
            include:
            matchLabels:
            matchExpressions:
          object-templates:
            - complianceType:
              objectDefinition:
                apiVersion: rbac.authorization.k8s.io/v1
                kind: Role
                metadata:
                  name:
                rules:
                  - apiGroups:
                    resources:
                    verbs:
                ...
```

### Role policy table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional because the
  value overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

### Role policy sample

Apply a role policy to set rules and permissions for specific roles in
your cluster. For more information on roles, see Role-based access
control.

To learn how to manage role policies, refer to Creating configuration
policies for more information. See the Kubernetes configuration policy
controller to view other configuration policies that are monitored the
controller.

## Role binding policy

The Kubernetes configuration policy controller monitors the status of
your role binding policy. Apply a role binding policy to bind a policy
to a namespace in your managed cluster.

### Role binding policy YAML structure

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          namespaceSelector:
            exclude:
            include:
            matchLabels:
            matchExpressions:
          object-templates:
            - complianceType:
              objectDefinition:
                kind: RoleBinding # role binding must exist
                apiVersion: rbac.authorization.k8s.io/v1
                metadata:
                  name:
                subjects:
                - kind:
                  name:
                  apiGroup:
                roleRef:
                  kind:
                  name:
                  apiGroup:
                ...
```

### Role binding policy table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional since it
  overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

### Role binding policy sample

For a full description of the policy YAML structure and additional
fields, see the Hub cluster policy framework. Refer to Kubernetes
configuration policy controller documentation to learn about other
configuration policies.

## Security Context Constraints policy

The Kubernetes configuration policy controller monitors the status of
your Security Context Constraints (SCC) policy. Apply an Security
Context Constraints (SCC) policy to control permissions for pods by
defining conditions in the policy.

### SCC policy YAML structure

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          namespaceSelector:
            exclude:
            include:
            matchLabels:
            matchExpressions:
          object-templates:
            - complianceType:
              objectDefinition:
                apiVersion: security.openshift.io/v1
                kind: SecurityContextConstraints
                metadata:
                  name:
                allowHostDirVolumePlugin:
                allowHostIPC:
                allowHostNetwork:
                allowHostPID:
                allowHostPorts:
                allowPrivilegeEscalation:
                allowPrivilegedContainer:
                fsGroup:
                readOnlyRootFilesystem:
                requiredDropCapabilities:
                runAsUser:
                seLinuxContext:
                supplementalGroups:
                users:
                volumes:
                ...
```

### SCC policy table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional since it
  overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

For explanations on the contents of a SCC policy, see Managing Security
Context Constraints from the OpenShift Container Platform documentation.

### SCC policy sample

Apply a Security context constraints (SCC) policy to control permissions
for pods by defining conditions in the policy. For more information, see
Managing Security Context Constraints.

To view the policy sample, see `policy-scc.yaml`. For a full description
of the policy YAML structure and additional fields, see the Hub cluster
policy framework documentation. Refer to Kubernetes configuration policy
controller documentation to learn about other configuration policies.

## ETCD encryption policy

Apply the `etcd-encryption` policy to detect, or enable encryption of
sensitive data in the ETCD data-store. The Kubernetes configuration
policy controller monitors the status of the `etcd-encryption` policy.
For more information, see Encrypting etcd data in the OpenShift
Container Platform documentation. **Note:** The ETCD encryption policy
only supports Red Hat OpenShift Container Platform 4 and later.

### ETCD encryption policy YAML structure

Your `etcd-encryption` policy might resemble the following YAML file:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name:
  namespace:
  annotations:
    policy.open-cluster-management.io/standards:
    policy.open-cluster-management.io/categories:
    policy.open-cluster-management.io/controls:
    policy.open-cluster-management.io/description:
spec:
  remediationAction:
  disabled:
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1
        kind: ConfigurationPolicy
        metadata:
          name:
        spec:
          remediationAction:
          severity:
          object-templates:
            - complianceType:
              objectDefinition:
                apiVersion: config.openshift.io/v1
                kind: APIServer
                metadata:
                  name:
                spec:
                  encryption:
                ...
```

### ETCD encryption policy table

- Field: apiVersion - Optional or required: Required - Description: Set
  the value to policy.open-cluster-management.io/v1.

- Field: kind - Optional or required: Required - Description: Set the
  value to Policy to indicate the type of policy.

- Field: metadata.name - Optional or required: Required - Description:
  The name for identifying the policy resource.

- Field: metadata.namespace - Optional or required: Required -
  Description: The namespace of the policy.

- Field: spec.remediationAction - Optional or required: Optional -
  Description: Specifies the remediation of your policy. The parameter
  values are enforce and inform. This value is optional because it
  overrides any values provided in spec.policy-templates.

- Field: spec.disabled - Optional or required: Required - Description:
  Set the value to true or false. The disabled parameter provides the
  ability to enable and disable your policies.

- Field: spec.policy-templates\[\].objectDefinition - Optional or
  required: Required - Description: Used to list configuration policies
  containing Kubernetes objects that must be evaluated or applied to the
  managed clusters.

### ETCD encryption policy sample

See the Hub cluster policy framework documentation and the Kubernetes
configuration policy controller to view additional details on policy and
configuration policy fields.

## Compliance Operator policy

You can use the Compliance Operator to automate the inspection of
numerous technical implementations and compare those against certain
aspects of industry standards, benchmarks, and baselines. The Compliance
Operator is not an auditor. To be compliant or certified with these
various standards, you need to engage an authorized auditor such as a
Qualified Security Assessor (QSA), Joint Authorization Board (JAB), or
other industry recognized regulatory authority to assess your
environment.

Recommendations that are generated from the Compliance Operator are
based on generally available information and practices regarding such
standards, and might assist you with remediations, but actual compliance
is your responsibility. Work with an authorized auditor to achieve
compliance with a standard.

For the latest updates, see the Compliance Operator release notes.

### Compliance Operator policy overview

You can install the Compliance Operator on your managed cluster by using
the Compliance Operator policy. The Compliance operator policy is
created as a Kubernetes configuration policy in Red Hat Advanced Cluster
Management. OpenShift Container Platform supports the compliance
operator policy.

**Note:** The Compliance operator policy relies on the OpenShift
Container Platform Compliance Operator, which is not supported on the
IBM Power or IBM Z architectures. See Understanding the Compliance
Operator in the OpenShift Container Platform documentation for more
information about the Compliance Operator.

### Compliance operator resources

When you create a compliance operator policy, the following resources
are created:

- A compliance operator namespace (`openshift-compliance`) for the
  operator installation:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: comp-operator-ns
spec:
  remediationAction: inform # will be overridden by remediationAction in parent policy
  severity: high
  object-templates:
    - complianceType: musthave
      objectDefinition:
        apiVersion: v1
        kind: Namespace
        metadata:
          name: openshift-compliance
```

- An operator group (`compliance-operator`) to specify the target
  namespace:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: comp-operator-operator-group
spec:
  remediationAction: inform # will be overridden by remediationAction in parent policy
  severity: high
  object-templates:
    - complianceType: musthave
      objectDefinition:
        apiVersion: operators.coreos.com/v1
        kind: OperatorGroup
        metadata:
          name: compliance-operator
          namespace: openshift-compliance
        spec:
          targetNamespaces:
            - openshift-compliance
```

- A subscription (`comp-operator-subscription`) to reference the name
  and channel. The subscription pulls the profile, as a container, that
  it supports. See the following sample, with the current version
  replacing `4.x`:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: ConfigurationPolicy
metadata:
  name: comp-operator-subscription
spec:
  remediationAction: inform  # will be overridden by remediationAction in parent policy
  severity: high
  object-templates:
    - complianceType: musthave
      objectDefinition:
        apiVersion: operators.coreos.com/v1alpha1
        kind: Subscription
        metadata:
          name: compliance-operator
          namespace: openshift-compliance
        spec:
          channel: "4.x"
          installPlanApproval: Automatic
          name: compliance-operator
          source: redhat-operators
          sourceNamespace: openshift-marketplace
```

After you install the compliance operator policy, the following pods are
created: `compliance-operator`, `ocp4`, and `rhcos4`.

## E8 scan policy

An Essential 8 (E8) scan policy deploys a scan that checks the master
and worker nodes for compliance with the E8 security profiles. You must
install the compliance operator to apply the E8 scan policy.

The E8 scan policy is created as a Kubernetes configuration policy in
Red Hat Advanced Cluster Management. OpenShift Container Platform
supports the E8 scan policy. For more information, see Managing the
Compliance Operator in the OpenShift Container Platform documentation
for more details.

### E8 scan policy resources

When you create an E8 scan policy the following resources are created:

- A `ScanSettingBinding` resource (`e8`) to identify which profiles to
  scan:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: compliance-suite-e8
  spec:
    remediationAction: inform
    severity: high
    object-templates:
      - complianceType: musthave # this template checks if scan has completed by checking the status field
        objectDefinition:
          apiVersion: compliance.openshift.io/v1alpha1
          kind: ScanSettingBinding
          metadata:
            name: e8
            namespace: openshift-compliance
          profiles:
          - apiGroup: compliance.openshift.io/v1alpha1
            kind: Profile
            name: ocp4-e8
          - apiGroup: compliance.openshift.io/v1alpha1
            kind: Profile
            name: rhcos4-e8
          settingsRef:
            apiGroup: compliance.openshift.io/v1alpha1
            kind: ScanSetting
            name: default
  ```

- A `ComplianceSuite` resource (`compliance-suite-e8`) to verify if the
  scan is complete by checking the `status` field:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: compliance-suite-e8
  spec:
    remediationAction: inform
    severity: high
    object-templates:
      - complianceType: musthave # this template checks if scan has completed by checking the status field
        objectDefinition:
          apiVersion: compliance.openshift.io/v1alpha1
          kind: ComplianceSuite
          metadata:
            name: e8
            namespace: openshift-compliance
          status:
            phase: DONE
  ```

- A `ComplianceCheckResult` resource (`compliance-suite-e8-results`)
  which reports the results of the scan suite by checking the
  `ComplianceCheckResult` custom resources (CR):

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: compliance-suite-e8-results
  spec:
    remediationAction: inform
    severity: high
    object-templates:
      - complianceType: mustnothave # this template reports the results for scan suite: e8 by looking at ComplianceCheckResult CRs
        objectDefinition:
          apiVersion: compliance.openshift.io/v1alpha1
          kind: ComplianceCheckResult
          metadata:
            namespace: openshift-compliance
            labels:
              compliance.openshift.io/check-status: FAIL
              compliance.openshift.io/suite: e8
  ```

**Note:** Automatic remediation is supported. Set the remediation action
to `enforce` to create `ScanSettingBinding` resource.

See Managing security policies for more information. **Note:** After
your E8 policy is deleted, it is removed from your target cluster or
clusters.

## OpenShift CIS scan policy

An OpenShift CIS scan policy deploys a scan that checks the master and
worker nodes for compliance with the OpenShift CIS security benchmark.
You must install the compliance operator to apply the OpenShift CIS
policy.

The OpenShift CIS scan policy is created as a Kubernetes configuration
policy in Red Hat Advanced Cluster Management. OpenShift Container
Platform supports the OpenShift CIS scan policy. For more information,
see Understanding the Compliance Operator in the OpenShift Container
Platform documentation for more details.

### OpenShift CIS resources

When you create an OpenShift CIS scan policy the following resources are
created:

- A `ScanSettingBinding` resource (`cis`) to identify which profiles to
  scan:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: compliance-cis-scan
  spec:
    remediationAction: inform
    severity: high
    object-templates:
      - complianceType: musthave # this template creates ScanSettingBinding:cis
        objectDefinition:
          apiVersion: compliance.openshift.io/v1alpha1
          kind: ScanSettingBinding
          metadata:
            name: cis
            namespace: openshift-compliance
          profiles:
          - apiGroup: compliance.openshift.io/v1alpha1
            kind: Profile
            name: ocp4-cis
          - apiGroup: compliance.openshift.io/v1alpha1
            kind: Profile
            name: ocp4-cis-node
          settingsRef:
            apiGroup: compliance.openshift.io/v1alpha1
            kind: ScanSetting
            name: default
  ```

- A `ComplianceSuite` resource (`compliance-suite-cis`) to verify if the
  scan is complete by checking the `status` field:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: compliance-suite-cis
  spec:
    remediationAction: inform
    severity: high
    object-templates:
      - complianceType: musthave # this template checks if scan has completed by checking the status field
        objectDefinition:
          apiVersion: compliance.openshift.io/v1alpha1
          kind: ComplianceSuite
          metadata:
            name: cis
            namespace: openshift-compliance
          status:
            phase: DONE
  ```

- A `ComplianceCheckResult` resource (`compliance-suite-cis-results`)
  which reports the results of the scan suite by checking the
  `ComplianceCheckResult` custom resources (CR):

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: compliance-suite-cis-results
  spec:
    remediationAction: inform
    severity: high
    object-templates:
      - complianceType: mustnothave # this template reports the results for scan suite: cis by looking at ComplianceCheckResult CRs
        objectDefinition:
          apiVersion: compliance.openshift.io/v1alpha1
          kind: ComplianceCheckResult
          metadata:
            namespace: openshift-compliance
            labels:
              compliance.openshift.io/check-status: FAIL
              compliance.openshift.io/suite: cis
  ```

For more information on creating policies, see Managing security
policies.

## Image vulnerability policy

Apply the image vulnerability policy to detect if container images have
vulnerabilities by leveraging the Container Security Operator. The
policy installs the Container Security Operator on your managed cluster
if it is not installed.

The image vulnerability policy is checked by the Kubernetes
configuration policy controller. For more information about the Security
Operator, see the *Container Security Operator* from the Quay
repository.

**Notes:**

- Image vulnerability policy is not functional during a disconnected
  installation.

- The Image vulnerability policy is not supported on the ARM
  architecture.

### Image vulnerability policy YAML structure

When you create the container security operator policy, it involves the
following policies:

- A policy that creates the subscription (`container-security-operator`)
  to reference the name and channel. This operator policy must have
  `spec.remediationAction` set to `enforce` to create the resources.
  View the following example:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1beta1
  kind: OperatorPolicy
  metadata:
    name: operatorpolicy-imagemanifestvuln
  spec:
    remediationAction: enforce
    severity: high
    complianceType: musthave
    upgradeApproval: Automatic
    subscription:
      name: container-security-operator
      namespace: openshift-operators
      source: redhat-operators
      sourceNamespace: openshift-marketplace
  ```

- An `inform` configuration policy to audit whether any
  `ImageManifestVuln` objects were created by the image vulnerability
  scans. View the following example:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: policy-imagemanifestvuln-example-imv
  spec:
    remediationAction: inform  # will be overridden by remediationAction in parent policy
    severity: high
    namespaceSelector:
      exclude: ["kube-*"]
      include: ["*"]
    object-templates:
      - complianceType: mustnothave # mustnothave any ImageManifestVuln object
        objectDefinition:
          apiVersion: secscan.quay.redhat.com/v1alpha1
          kind: ImageManifestVuln # checking for a Kind
  ```

## Red Hat OpenShift Platform Plus policy set

Configure and apply the OpenShift Platform Plus policy set
(`openshift-plus`) to install Red Hat OpenShift Platform Plus.

The OpenShift Platform Plus policy set contains two `PolicySets` that
are deployed. The OpenShift Plus policy set applies multiple policies
that are set to install OpenShift Platform Plus products. The Red Hat
Advanced Cluster Security secured cluster services and the Compliance
Operator are deployed onto all of your OpenShift Container Platform
managed clusters.

### Prerequisites

- Install Red Hat OpenShift Container Platform on Amazon Web Services
  (AWS) environment.

- Install Red Hat Advanced Cluster Management for Kubernetes.

- Install the Policy Generator Kustomize plugin. See the Policy
  Generator documentation for more information.

### OpenShift Platform Plus policy set components

When you apply the policy set to the hub cluster, the following
OpenShift Platform Plus components are installed:

- Component: Red Hat Advanced Cluster Security - Policy:
  policy-acs-central-ca-bundle - Description: Policy used to install the
  central server onto the Red Hat Advanced Cluster Management for
  Kubernetes hub cluster and the managed clusters.

- Component: policy-acs-central-status - Policy: Deployments to receive
  Red Hat Advanced Cluster Security status.

- Component: policy-acs-operator-central - Policy: Configuration for the
  Red Hat Advanced Cluster Security central operator.

- Component: policy-acs-sync-resources - Policy: Policy used to verify
  that the Red Hat Advanced Cluster Security resources are created.

- Component: OpenShift Container Platform - Policy:
  policy-advanced-managed-cluster-status - Description: The managed hub
  cluster. Manager of the managed cluster.

- Component: Compliance operator - Policy:
  policy-compliance-operator-install - Description: Policy used to
  install the Compliance operator.

- Component: Red Hat Quay - Policy: policy-config-quay - Description:
  Configuration policy for Red Hat Quay.

- Component: policy-install-quay - Policy: Policy used to install Red
  Hat Quay.

- Component: policy-quay-status - Policy: Installed onto the Red Hat
  Advanced Cluster Management hub cluster.

- Component: Red Hat Advanced Cluster Management - Policy:
  policy-ocm-observability - Description: Sets up the Red Hat Advanced
  Cluster Management observability service.

- Component: Red Hat OpenShift Data Platform - Policy: policy-odf -
  Description: Available storage for the hub cluster components that is
  used by Red Hat Advanced Cluster Management observability and Quay.

- Component: policy-odf-status - Policy: Policy used to configure the
  Red Hat OpenShift Data Platform status.

## Managing security policies

Create a security policy to report and validate your cluster compliance
based on your specified security standards, categories, and controls.

### Creating a security policy

You can create a security policy from the command line or from the
console.

**Required access:** Cluster administrator

**Important:** \* You must define a placement and placement binding to
apply your policy to a specific cluster. The `PlacementBinding` resource
binds the placement. Enter a valid value for the cluster *Label
selector* field to define a `Placement` and `PlacementBinding` resource.
\* In order to use a `Placement` resource, a `ManagedClusterSet`
resource must be bound to the namespace of the `Placement` resource with
a `ManagedClusterSetBinding` resource. Refer to Creating a
ManagedClusterSetBinding resource for additional details.

#### Creating a security policy from the command line interface

Complete the following steps to create a policy from the command line:

1.  Create a policy by running the following command:

        oc create -f policy.yaml -n <policy-namespace>

2.  Define the template that the policy uses. Edit your YAML file by
    adding a `policy-templates` field to define a template. Your policy
    might resemble the following YAML file:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: Policy
    metadata:
      name: policy1
    spec:
      remediationAction: "enforce" # or inform
      disabled: false # or true
      namespaceSelector:
        include:
        - "default"
        - "my-namespace"
      policy-templates:
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: operator
              # namespace: # will be supplied by the controller via the namespaceSelector
            spec:
              remediationAction: "inform"
              object-templates:
              - complianceType: "musthave" # at this level, it means the role must exist and must have the following rules
                apiVersion: rbac.authorization.k8s.io/v1
                kind: Role
                metadata:
                  name: example
                objectDefinition:
                  rules:
                    - complianceType: "musthave" # at this level, it means if the role exists the rule is a musthave
                      apiGroups: ["extensions", "apps"]
                      resources: ["deployments"]
                      verbs: ["get", "list", "watch", "create", "delete","patch"]
    ```

3.  Define a `PlacementBinding` resource to bind your policy to your
    `Placement` resource. Your `PlacementBinding` resource might
    resemble the following YAML sample:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: PlacementBinding
    metadata:
      name: binding1
    placementRef:
      name: placement1
      apiGroup: cluster.open-cluster-management.io
      kind: Placement
    subjects:
    - name: policy1
      apiGroup: policy.open-cluster-management.io
      kind: Policy
    ```

##### Viewing your security policy from the command line

Complete the following steps to view your security policy from the
command line:

1.  View details for a specific security policy by running the following
    command:

        oc get policies.policy.open-cluster-management.io <policy-name> -n <policy-namespace> -o yaml

2.  View a description of your security policy by running the following
    command:

        oc describe policies.policy.open-cluster-management.io <policy-name> -n <policy-namespace>

#### Creating a cluster security policy from the console

After you log in to your Red Hat Advanced Cluster Management, navigate
to the *Governance* page and click **Create policy**. As you create your
new policy from the console, a YAML file is also created in the YAML
editor. To view the YAML editor, select the toggle at the beginning of
the *Create policy* form to enable it.

1.  Complete the *Create policy* form, then select the **Submit**
    button. Your YAML file might resemble the following policy:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: Policy
    metadata:
      name: policy-pod
      annotations:
        policy.open-cluster-management.io/categories: 'SystemAndCommunicationsProtections,SystemAndInformationIntegrity'
        policy.open-cluster-management.io/controls: 'control example'
        policy.open-cluster-management.io/standards: 'NIST,HIPAA'
        policy.open-cluster-management.io/description:
    spec:
      complianceType: musthave
      namespaces:
        exclude: ["kube*"]
        include: ["default"]
        pruneObjectBehavior: None
      object-templates:
      - complianceType: musthave
        objectDefinition:
          apiVersion: v1
          kind: Pod
          metadata:
            name: pod1
          spec:
            containers:
            - name: pod-name
              image: 'pod-image'
              ports:
              - containerPort: 80
      remediationAction: enforce
      disabled: false
    ```

    See the following `PlacementBinding` example:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: PlacementBinding
    metadata:
      name: binding-pod
    placementRef:
      name: placement-pod
      kind: Placement
      apiGroup: cluster.open-cluster-management.io
    subjects:
    - name: policy-pod
      kind: Policy
      apiGroup: policy.open-cluster-management.io
    ```

    See the following `Placement` example:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta1
     kind: Placement
     metadata:
       name: placement-pod
    spec:
      predicates:
      - requiredClusterSelector:
          labelSelector:
            matchLabels:
              cloud: "IBM"
        tolerations:
            - key: cluster.open-cluster-management.io/unavailable
              operator: Exists
            - key: cluster.open-cluster-management.io/unreachable
              operator: Exists
    ```

2.  **Optional:** Add a description for your policy.

3.  Click **Create Policy**. A security policy is created from the
    console.

##### Viewing your security policy from the console

View any security policy and the status from the console.

1.  Navigate to the *Governance* page to view a table list of your
    policies. **Note:** You can filter the table list of your policies
    by selecting the *Policies* tab or *Cluster violations* tab.

2.  Select one of your policies to view more details. The *Details*,
    *Clusters*, and *Templates* tabs are displayed. When the cluster or
    policy status cannot be determined, the following message is
    displayed: `No status`.

3.  Alternatively, select the *Policies* tab to view the list of
    policies. Expand a policy row to view the *Description*,
    *Standards*, *Controls*, and *Categories* details.

#### Creating policy sets from the command line

By default, the policy set is created with no policies or placements.
You must create a placement for the policy set and have at least one
policy that exists on your cluster. When you create a policy set, you
can add numerous policies.

Run the following command to create a policy set from the command line:

    oc apply -f <policyset-filename>

#### Creating policy sets from the console

1.  From the navigation menu, select **Governance**.

2.  Select the *Policy sets* tab.

3.  Select the **Create policy set** button and complete the form.

4.  Add the details for your policy set and select the **Submit**
    button.

Your policy is listed from the policy table.

### Updating security policies

Learn to update security policies.

#### Adding a policy to a policy set from the command line

1.  Run the following command to edit your policy set:

        oc edit policysets <your-policyset-name>

2.  Add the policy name to the list in the `policies` section of the
    policy set.

3.  Apply your added policy in the placement section of your policy set
    with the following command:

<!-- -->

    oc apply -f <your-added-policy.yaml>

`PlacementBinding` and `Placement` are both created.

**Note:** If you delete the placement binding, the policy is still
placed by the policy set.

#### Adding a policy to a policy set from the console

1.  Add a policy to the policy set by selecting the *Policy sets* tab.

2.  Select the Actions icon and select **Edit**. The *Edit policy set*
    form appears.

3.  Navigate to the *Policies* section of the form to select a policy to
    add to the policy set.

#### Disabling security policies

Your policy is enabled by default. Disable your policy from the console.

After you log in to your Red Hat Advanced Cluster Management for
Kubernetes console, navigate to the *Governance* page to view a table
list of your policies.

Select the **Actions** icon \> **Disable policy**. The *Disable Policy*
dialog box appears.

Click **Disable policy**. Your policy is disabled.

### Deleting a security policy

Delete a security policy from the command line or the console.

Use the following procedure to delete from the command line:

1.  Delete a security policy by running the following command:

        oc delete policies.policy.open-cluster-management.io <policy-name> -n <policy-namespace>

2.  Verify that your policy is removed by running the following command:
    `oc get policies.policy.open-cluster-management.io <policy-name> -n <policy-namespace>`

Use the following procedure to delete a security policy from the
console.

1.  From the navigation menu, click **Governance** to view a table list
    of your policies.

2.  Click the **Actions** icon for the policy you want to delete in the
    policy violation table.

3.  Click **Remove**.

4.  From the *Remove policy* dialog box, click **Remove policy**.

#### Deleting policy sets from the console

1.  From the *Policy sets* tab, select the **Actions** icon for the
    policy set. When you click **Delete**, the *Permanently delete
    Policyset?* dialogue box appears.

2.  Click the **Delete** button.

### Cleaning up resources that are created by policies

Use the `pruneObjectBehavior` parameter in a configuration policy to
clean up resources that are created by the policy. When
`pruneObjectBehavior` is set, the related objects are only cleaned up
after the configuration policy (or parent policy) associated with them
is deleted.

View the following descriptions of the values that can be used for the
parameter:

- `DeleteIfCreated`: Cleans up any resources created by the policy.

- `DeleteAll`: Cleans up all resources managed by the policy.

- `None`: This is the default value and maintains the same behavior from
  previous releases, where no related resources are deleted.

You can set the value directly in the YAML file as you create a policy
from the command line.

From the console, you can select the value in the *Prune Object
Behavior* section of the *Policy templates* step.

**Notes:**

- If a policy that installs an operator has the `pruneObjectBehavior`
  parameter defined, then additional clean up is needed to complete the
  operator uninstall. You might need to delete the operator
  `ClusterServiceVersion` object as part of this cleanup.

- As you disable the `config-policy-addon` resource on the managed
  cluster, the `pruneObjbectBehavior` is ignored. To automatically clean
  up the related resources on the policies, you must remove the policies
  from the managed cluster before the add-on is disabled.

### Policy command-line tool

With the `policytools` command-line tool, you can interact with policies
locally to help with creating and debugging. The `policytools`
command-line tool is available for download from the hub cluster
console. See Command line tools.

`template-resolver`  
The `template-resolver` is a subcommand for `policytools` that resolves
managed cluster and hub cluster templates that are embedded in policies.
The `template-resolver` reads from either a file, or from standard
input.

To resolve a policy with hub cluster templates, you must provide the
`--cluster-name` argument with the name of a managed cluster that is
imported into Red Hat Advanced Cluster Management, and you must provide
the `--hub-kubeconfig` argument with the path to a `kubeconfig` file
that references the hub cluster.

If the input policy uses the `.ObjectName` or `.ObjectNamespace`
template variables, you need to set the values with the `--object-name`
and `--object-namespace` arguments.

The `template-resolver` subcommand connects to the managed cluster and
hub cluster to retrieve information that is necessary to resolve the
templates. Provide paths by using the `--save-resources` and
`--save-hub-resources` arguments to save the resources that the
`template-resolver` retrieves. Those saved files can be used as inputs
for the `dryrun` subcommand.

**Technology Preview:** The `policytools` command-line interface
introduces a `--lint` argument for the `template-resolver` subcommand to
print any linting issues, along with the resolved Go templates from the
input policy.

`dryrun`  
The `dryrun` is a subcommand for `policytools` that evaluates a
`ConfigurationPolicy` resource locally by using static input resources
for the cluster state.

To run a policy, add the path to the `ConfigurationPolicy` YAML by using
the `--policy` flag. You can provide additional resource YAML files,
which are used as the current cluster state. For example, if your policy
defines a specific configuration for a namespace, provide the current
namespace state to see what the policy does. Multiple resources can be
in the same resource file.

To evaluate a policy against the current state of a live cluster, use
the `--from-cluster` flag or set the `DRYRUN_FROM_CLUSTER` environment
variable to `true`.

The `dryrun` subcommand reads the current state of resources directly
from the cluster that you configured in your `kubeconfig` file or from
the cluster that is specified by the `KUBECONFIG` environment variable.
In both these scenarios, the `dryun` subcommand does not gather
information from the resource files.

When you enable the `--from-cluster` flag, it ignores any YAML resource
files that are provided as input. Enabling the `--from-cluster` flag
allows you to test a policy against your actual cluster state without
manually exporting and supporting resource files.

\+ By default, `dryrun` prints the differences between the desired
states of objects that are defined in the policy and the current state
of those resources, as well as compliance messages that the
`ConfigurationPolicy` creates.

To save the compliance messages to a separate file, use the
`--messages-path` argument. To save the full policy status, including
additional information about the related objects, use the
`--status-path` argument.

\+ If the policy is `NonCompliant` based on the input, the tool returns
a non-zero exit code. To compare the resulting status against a known
status, use the `--desired-status` argument. For example, to verify that
the policy reports a missing resource, provide a YAML file with the
missing resource inside a `.relatedObjects` list. To verify that the
policy is `NonCompliant`, create a YAML file with the
`compliant: NonCompliant` line.

### Managing operator policies in disconnected environments

You might need to deploy Red Hat Advanced Cluster Management for
Kubernetes policies on Red Hat OpenShift Container Platform clusters
that are not connected to the internet (disconnected). If the policies
you deploy are used to deploy policies that install an Operator
Lifecycle Manager operator, you must follow the procedure for Mirroring
an Operator catalog.

Complete the following steps to validate access to the operator images:

1.  See Verify required packages are available to validate that packages
    you require to use with policies are available. You must validate
    availability for each image registry used by any managed cluster
    that the following policies are deployed to:

    - `container-security-operator`

    - **Deprecated:** `gatekeeper-operator-product`

    - `compliance-operator`

2.  See Configure image content source policies to validate that the
    sources are available. The image content source policies must exist
    on each of the disconnected managed clusters and can be deployed
    using a policy to simplify the process. See the following table of
    image source locations:

    - Governance policy type: Container security - Image source
      location: registry.redhat.io/quay

    - Governance policy type: Compliance - Image source location:
      registry.redhat.io/compliance

    - Governance policy type: Gatekeeper - Image source location:
      registry.redhat.io/rhacm2

### Installing Red Hat OpenShift Platform Plus by using a policy set

Continue reading for guidance to apply the Red Hat Openshift Platform
Plus policy set. When you apply the Red Hat OpenShift policy set, the
Red Hat Advanced Cluster Security secured cluster services and the
Compliance Operator are deployed onto all of your OpenShift Container
Platform managed clusters.

#### Prerequisites

Complete the following steps before you apply the policy set:

1.  To allow for subscriptions to be applied to your cluster, you must
    apply the `policy-configure-subscription-admin-hub.yaml` policy and
    set the remediation action to `enforce`. Copy and paste the
    following YAML into the YAML editor of the console:

    ``` yaml
    apiVersion: policy.open-cluster-management.io/v1
    kind: Policy
    metadata:
      name: policy-configure-subscription-admin-hub
      annotations:
        policy.open-cluster-management.io/standards: NIST SP 800-53
        policy.open-cluster-management.io/categories: CM Configuration Management
        policy.open-cluster-management.io/controls: CM-2 Baseline Configuration
    spec:
      remediationAction: inform
      disabled: false
      policy-templates:
        - objectDefinition:
            apiVersion: policy.open-cluster-management.io/v1
            kind: ConfigurationPolicy
            metadata:
              name: policy-configure-subscription-admin-hub
            spec:
              remediationAction: inform
              severity: low
              object-templates:
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: rbac.authorization.k8s.io/v1
                    kind: ClusterRole
                    metadata:
                      name: open-cluster-management:subscription-admin
                    rules:
                    - apiGroups:
                      - app.k8s.io
                      resources:
                      - applications
                      verbs:
                      - '*'
                    - apiGroups:
                      - apps.open-cluster-management.io
                      resources:
                      - '*'
                      verbs:
                      - '*'
                    - apiGroups:
                      - ""
                      resources:
                      - configmaps
                      - secrets
                      - namespaces
                      verbs:
                      - '*'
                - complianceType: musthave
                  objectDefinition:
                    apiVersion: rbac.authorization.k8s.io/v1
                    kind: ClusterRoleBinding
                    metadata:
                      name: open-cluster-management:subscription-admin
                    roleRef:
                      apiGroup: rbac.authorization.k8s.io
                      kind: ClusterRole
                      name: open-cluster-management:subscription-admin
                    subjects:
                    - apiGroup: rbac.authorization.k8s.io
                      kind: User
                      name: kube:admin
                    - apiGroup: rbac.authorization.k8s.io
                      kind: User
                      name: system:admin
    ---
    apiVersion: policy.open-cluster-management.io/v1
    kind: PlacementBinding
    metadata:
      name: binding-policy-configure-subscription-admin-hub
    placementRef:
      name: placement-policy-configure-subscription-admin-hub
      kind: Placement
      apiGroup: cluster.open-cluster-management.io
    subjects:
    - name: policy-configure-subscription-admin-hub
      kind: Policy
      apiGroup: policy.open-cluster-management.io
    ---
    apiVersion: cluster.open-cluster-management.io/v1beta1
    kind: Placement
    metadata:
      name: placement-policy-configure-subscription-admin-hub
    spec:
      predicates:
      - requiredClusterSelector:
          labelSelector:
            matchExpressions:
            - {key: name, operator: In, values: ["local-cluster"]}
        tolerations:
            - key: cluster.open-cluster-management.io/unavailable
              operator: Exists
            - key: cluster.open-cluster-management.io/unreachable
              operator: Exists
    ```

2.  To apply the previous YAML from the command line interface, run the
    following command:

        oc apply -f policy-configure-subscription-admin-hub.yaml

3.  Install the Policy Generator kustomize plugin. Use Kustomize v4.5 or
    newer. See Generating a policy to install an Operator.

4.  Policies are installed to the `policies` namespace. You must bind
    that namespace to a `ClusterSet`. For example, copy and apply the
    following example YAML to bind the namespace to the default
    `ClusterSet`:

    ``` yaml
    apiVersion: cluster.open-cluster-management.io/v1beta2
    kind: ManagedClusterSetBinding
    metadata:
        name: default
        namespace: policies
    spec:
        clusterSet: default
    ```

5.  Run the following command to apply the `ManagedClusterSetBinding`
    resource from the command line interface:

        oc apply -f managed-cluster.yaml

After you meet the prerequisite requirements, you can apply the policy
set.

#### Applying Red Hat OpenShift Platform Plus policy set

1.  Use the `openshift-plus/policyGenerator.yaml` file that includes the
    prerequisite configuration for Red Hat OpenShift Plus.

2.  Apply the policies to your hub cluster by using the `kustomize`
    command:

        kustomize build --enable-alpha-plugins  | oc apply -f -

    **Note:** For any components of OpenShift Platform Plus that you do
    not want to install, edit the `policyGenerator.yaml` file and remove
    or comment out the policies for those components.

### Installing an operator by using the *OperatorPolicy* resource

To install Operator Lifecycle Manager (OLM) managed operators on your
managed clusters, use an `OperatorPolicy` policy template in a `Policy`
definition.

#### Creating an *OperatorPolicy* resource to install Quay

See the following operator policy sample that installs the latest Quay
operator in the stable `channel` using the Red Hat operator catalog:

``` yaml
apiVersion: policy.open-cluster-management.io/v1
kind: Policy
metadata:
  name: install-quay
  namespace: open-cluster-management-global-set
spec:
  disabled: false
  policy-templates:
    - objectDefinition:
        apiVersion: policy.open-cluster-management.io/v1beta1
        kind: OperatorPolicy
        metadata:
          name: install-quay
        spec:
          remediationAction: enforce
          severity: critical
          complianceType: musthave
          upgradeApproval: None
          subscription:
            channel: <stable-version>
            name: quay-operator
            source: redhat-operators
            sourceNamespace: openshift-marketplace
```

After you add the `OperatorPolicy` policy template, the `operatorGroup`
and `subscription` objects are created on the cluster by using the
controller. As a result, the rest of the installation is completed by
OLM. You can view the health of owned resources in the
`.status.Conditions` and `.status.relatedObjects` fields of the
`OperatorPolicy` resource on your managed cluster.

To verify the operator policy status, run the following command on your
managed cluster:

``` bash
oc -n <managed cluster namespace> get operatorpolicy install-quay
```

#### Additional resources

See Operator policy controller

# Gatekeeper operator overview

The Gatekeeper operator installs Gatekeeper, which is a validating
webhook with auditing capabilities. Install the Gatekeeper operator on a
Red Hat OpenShift Container Platform cluster from the Operator Lifecycle
Manager operator catalog. With Red Hat Advanced Cluster Management for
Kubernetes, you can install Gatekeeper on your hub cluster by using the
Gatekeeper operator policy. After you install Gatekeeper, use it for the
following benefits:

- Deploy and check Gatekeeper `ConstraintTemplates` and constraints on
  managed clusters by using the Red Hat Advanced Cluster Management
  policy integration.

- Enforce Kubernetes custom resource definition-based policies that run
  with your Open Policy Agent (OPA).

- Evaluate Kubernetes resource compliance requests for the Kubernetes
  API by using the Gatekeeper constraints.

- Use OPA as the policy engine and use Rego as the policy language.

**Prerequisite:** You need a Red Hat Advanced Cluster Management for
Kubernetes or Red Hat OpenShift Container Platform Plus subscription to
install Gatekeeper and apply Gatekeeper policies to your cluster.

## General support

To understand the support you receive from the Gatekeeper operator, see
the following list:

- Supports current version of the Gatekeeper operator, preceding
  versions, and all z-stream releases of those versions.

- Receive maintenance support and relevant security vulnerability fixes
  for preceding and current versions.

- Support for all Red Hat OpenShift Container Platform versions that
  receive standard support. **Note**: The Gatekeeper operator is not
  supported on end-of-life OpenShift Container Platform versions or
  versions that receive extended support.

To view the release notes for the Gatekeeper operator, see
gatekeeper-operator-bundle.

## Operator channels

With the Gatekeeper operator, you have access to two types of channels
to help you make upgrades. These channels are the `stable` channel and
the `y-stream version` channel.

With the `stable` channel, you can access the latest available version,
whether it is an `x-stream`, `y-stream`, or `z-stream`. The `stable`
channel includes the latest version of the latest `y-stream` channel.

With the `y-stream version` channel, you can access all the `z-stream`
versions for a particular `y-stream`.

## Configuring the Gatekeeper operator

Install the Gatekeeper operator from the Operator Lifecycle Manager
catalog to install Gatekeeper on your cluster. With Red Hat Advanced
Cluster Management you can use a policy to install the Gatekeeper
operator by using the governance framework. After you install the
Gatekeeper operator, configure the Gatekeeper operator custom resource
to install Gatekeeper.

### Prerequisites

- **Required access**: Cluster administrator.

- Understand how to use the Operator Lifecycle Manager and the Red Hat
  OpenShift Software Catalog by completing the *Adding Operators to a
  cluster* and the *Additional resources* section in the OpenShift
  Container Platform documentation.

### Gatekeeper custom resource sample

The Gatekeeper operator custom resource tells the Gatekeeper operator to
start the Gatekeeper installation on the cluster. To install Gatekeeper,
use the following sample YAML, which includes sample and default values:

``` yaml
apiVersion: operator.gatekeeper.sh/v1alpha1
kind: Gatekeeper
metadata:
  name: gatekeeper
spec:
  audit:
    auditChunkSize: 66
    auditEventsInvolvedNamespace: Enabled 
    auditFromCache: Enabled
    auditInterval: 10s
    constraintViolationLimit: 55
    containerArguments: 
    - name: ""
      value: ""
    resources:
      limits:
        cpu: 500m
        memory: 150Mi
      requests:
        cpu: 500m
        memory: 130Mi
    emitAuditEvents: Enabled
    logLevel: DEBUG
    podAnnotations: {} 
    replicas: 1
  validatingWebhook: Enabled
  mutatingWebhook: Enabled
  webhook:
    admissionEventsInvolvedNamespace: Enabled 
    containerArguments: 
    - name: ""
      value: ""
    disabledBuiltins:
     - http.send
    emitAdmissionEvents: Enabled
    failurePolicy: Fail
    operations: 
     - CREATE
     - UPDATE
     - CONNECT
    replicas: 3
    resources:
      limits:
        cpu: 480m
        memory: 140Mi
      requests:
        cpu: 400m
        memory: 120Mi
    rules: 
    - operations: []
      resources: []
    timeoutSeconds: 3 
  mutatingWebhookConfig: 
    failurePolicy: ""
    logMutations: Disabled
    mutationAnnotations: Disabled
    namespaceSelector: {}
    operations: []
    rules: 
    - operations: []
      resources: []
    timeoutSeconds: 1 
  config: 
    matches:
      - excludedNamespaces: ["test-*", "my-namespace"]
        processes: ["*"]
    disableDefaultMatches: false 
  nodeSelector:
    region: "EMEA"
  affinity:
    podAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchLabels:
              auditKey: "auditValue"
          topologyKey: topology.kubernetes.io/zone
  tolerations:
    - key: "Example"
      operator: "Exists"
      effect: "NoSchedule"
  podAnnotations:
    some-annotation: "this is a test"
    other-annotation: "another test"
```

- Enable the `auditEventsInvolvedNamespace` parameter to manage the
  namespace audit event you want to create. When you enable this
  parameter, the Gatekeeper controller deployment runs with the
  following argument: `--audit-events-involved-namespace=true`.

- For version 3.20 and later, specify `audit.podAnnotations` specific to
  the audit pod by providing a list of annotation names and values to
  add to the pod. An omitted value is treated as `true`.

- Enable the `admissionEventsInvolvedNamespace` parameter to manage the
  namespace admission event you want to create. When you enable this
  parameter, the Gatekeeper controller deployment runs with the
  following argument: `--admission-events-involved-namespace=true`.

- Specify `containerArguments` by providing a list of argument names and
  values to pass to the container. Omit leading dashes from the argument
  name. An omitted value is treated as `true`. Arguments that you
  provide are ignored if the argument is set previously by the operator
  or configurations from other fields. See the following list of flags
  that are deny-listed and are not currently supported:

  - `port`

  - `prometheus-port`

  - `health-addr`

  - `validating-webhook-configuration-name`

  - `mutating-webhook-configuration-name`

  - `disable-cert-rotation`

  - `client-cert-name`

  - `tls-min-version`

- Use `operations` to manage the operations for which the webhook is
  invoked. For example, `CREATE`, `UPDATE`, `CONNECT`, and `DELETE`.

- For version 3.20 and later, specify `rules` to overwrite the rules
  configuration in the webhook configuration. When set, this field takes
  precedence over the Operations field.

- For version 3.20 and later, specify the timeout for the webhook
  configuration.

- For version 3.20 and later, use the `mutatingWebhookConfig` section to
  configure the mutating webhook with configurations that override the
  values from `spec.webhook` or are specific to the mutating webhook.

- Use the `config` section to exclude namespaces from certain processes
  for all constraints on your cluster.

- The `disableDefaultMatches` parameter is a boolean parameter that
  disables appending the default exempt namespaces provided by the
  Gatekeeper operator. The default exempt namespaces are OpenShift
  Container Platform or Kubernetes system namespaces. By default, this
  parameter is set to `false` to allow the default namespaces to be
  appended.

### Configuring *auditFromCache* for sync details

The Gatekeeper operator exposes a setting in the Gatekeeper operator
custom resource for the audit configuration with the `auditFromCache`
parameter, which is disabled by default. Configure the `auditFromCache`
parameter to collect resources from constraints.

When you set the `auditFromCache` parameter to `Automatic`, the
Gatekeeper operator collects resources from constraints and inserts
those resources into your Gatekeeper `Config` resource. If the resource
does not exist, the Gatekeeper operator creates the `Config` resource.

If you set the `auditFromCache` parameter to `Enabled`, you need to
manually set the Gatekeeper `Config` resource with the objects to sync
to the cache. For more information, see *Configuring Audit* in the
Gatekeeper documentation.

To configure the `auditFromCache` parameter for resource collection from
constraints, complete the following steps:

1.  Set `auditFromCache` to `Automatic` in the `Gatekeeper` resource.
    See the following example:

    ``` yaml
    apiVersion: operator.gatekeeper.sh/v1alpha1
    kind: Gatekeeper
    metadata:
      name: gatekeeper
    spec:
      audit:
        replicas: 2
        logLevel: DEBUG
        auditFromCache: Automatic
    ```

2.  To verify that the resources are added to your `Config` resource,
    view that the `syncOnly` parameter section is added. Run the
    following command:

    ``` bash
    oc get configs.config.gatekeeper.sh config -n openshift-gatekeeper-system
    ```

    Your `Config` resource might resemble the following example:

    ``` yaml
    apiVersion: config.gatekeeper.sh/v1alpha1
    kind: Config
    metadata:
     name: config
     namespace: "openshift-gatekeeper-system"
    spec:
     sync:
       syncOnly:
       - group: ""
         version: "v1"
         kind: "Namespace"
       - group: ""
         version: "v1"
         kind: "Pod"
    ```

**Optional:** You can view the explanation of the `auditFromCache`
setting from the description of the Gatekeeper operator custom resource
by running the following command:

``` bash
oc explain gatekeeper.spec.audit.auditFromCache
```

## Managing the Gatekeeper operator installation policies

Use the Red Hat Advanced Cluster Management policy to install the
Gatekeeper operator and Gatekeeper on a managed cluster.

**Required access**: Cluster administrator

### Installing Gatekeeper using a Gatekeeper operator policy

To install the Gatekeeper operator policy, use the configuration policy
controller. During the install, the operator group and subscription pull
the Gatekeeper operator to install it on your managed cluster. Then, the
policy creates a Gatekeeper custom resource to configure Gatekeeper.

The Red Hat Advanced Cluster Management configuration policy controller
checks the Gatekeeper operator policy and supports the `enforce`
remediation action. When you set the controller to `enforce` it
automatically creates the Gatekeeper operator objects on the managed
cluster.

### Creating a Gatekeeper policy from the console

When you create a Gatekeeper policy from the console, you must set your
remediation `enforce` to install Gatekeeper.

#### Viewing the Gatekeeper operator policy

To view your Gatekeeper operator policy and its status from the console,
complete the following steps:

1.  Select the `policy-gatekeeper-operator` policy to view more details.

2.  Select the *Clusters* tab to view the policy violations.

### Upgrading Gatekeeper and the Gatekeeper operator

You can upgrade the versions for Gatekeeper and the Gatekeeper operator.
When you install the Gatekeeper operator with the Gatekeeper operator
policy, notice the value for `upgradeApproval`. The operator upgrades
automatically when you set `upgradeApproval` to `Automatic`.

If you set `upgradeApproval` to `Manual`, you must manually approve the
upgrade for each cluster where the Gatekeeper operator is installed.

### Disabling Gatekeeper operator policy

To disable your `policy-gatekeeper-operator` policy, select the
**Disable** option from the *Actions* menu in the console, or set
`spec.disabled: true` from the CLI.

### Deleting Gatekeeper operator policy

To delete your Gatekeeper operator policy from your CLI, complete the
following steps:

1.  Delete Gatekeeper operator policy by running the following command:

    ``` bash
    oc delete policies.policy.open-cluster-management.io <policy-gatekeeper-operator-name> -n <namespace>
    ```

2.  Verify that you deleted your policy by running the following
    command:

    ``` bash
    oc get policies.policy.open-cluster-management.io <policy-gatekeeper-operator-name> -n <namespace>
    ```

To delete your Gatekeeper operator policy from the console, click the
**Actions** icon for the `policy-gatekeeper-operator` policy and select
**Delete**.

### Uninstalling Gatekeeper constraints, Gatekeeper instance, and Gatekeeper operator policy

#### Removing Gatekeeper constraints

To remove the Gatekeeper constraint and `ConstraintTemplate` from your
managed cluster, complete the following steps:

1.  Edit your Gatekeeper constraint or `ConstraintTemplate` policy.

2.  Locate the template that you used to create the Gatekeeper
    `Constraint` and `ConstraintTemplate`.

3.  Delete the entries from the list of templates. (Or delete the policy
    if they’re the only templates.)

4.  Save and apply the policy.

**Note:** The constraint and `ConstraintTemplate` are provided directly
in the `policy-templates` instead of within a `ConfigurationPolicy`.

#### Removing Gatekeeper instance

To remove the Gatekeeper instance from your managed cluster, complete
the following steps:

1.  Edit your Gatekeeper operator policy.

2.  Locate the `ConfigurationPolicy` template that you used to create
    the Gatekeeper operator custom resource.

3.  Change the value for `complianceType` of the `ConfigurationPolicy`
    template to `mustnothave`. Changing the value deletes the Gatekeeper
    operator custom resource, signaling to the Gatekeeper operator to
    clean up the Gatekeeper deployment.

#### Removing Gatekeeper operator

To remove the Gatekeeper operator from your managed cluster, complete
the following steps:

1.  Edit your Gatekeeper operator policy.

2.  Locate the `OperatorPolicy` template that you used to create the
    Subscription CR.

3.  Change the value for `complianceType` of the `OperatorPolicy`
    template to `mustnothave`.

## Integrating Gatekeeper constraints and constraint templates

To create Gatekeeper policies, use `ConstraintTemplates` and
constraints. Add templates and constraints to the `policy-templates` of
a `Policy` resource. View the following YAML examples that use
Gatekeeper constraints in Red Hat Advanced Cluster Management policies:

- `ConstraintTemplates` and constraints: Use the Gatekeeper integration
  feature by using Red Hat Advanced Cluster Management policies for
  multicluster distribution of Gatekeeper constraints and Gatekeeper
  audit results aggregation on the hub cluster. The following example
  defines a Gatekeeper `ConstraintTemplate` and constraint
  (`K8sRequiredLabels`) to ensure the `gatekeeper` label is set on all
  namespaces:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: Policy
  metadata:
    name: require-gatekeeper-labels-on-ns
  spec:
    remediationAction: inform 
    disabled: false
    policy-templates:
      - objectDefinition:
          apiVersion: templates.gatekeeper.sh/v1beta1
          kind: ConstraintTemplate
          metadata:
            name: k8srequiredlabels
            annotations:
              policy.open-cluster-management.io/severity: low 
          spec:
            crd:
              spec:
                names:
                  kind: K8sRequiredLabels
                validation:
                  openAPIV3Schema:
                    properties:
                      labels:
                        type: array
                        items: string
            targets:
              - target: admission.k8s.gatekeeper.sh
                rego: |
                  package k8srequiredlabels
                  violation[{"msg": msg, "details": {"missing_labels": missing}}] {
                    provided := {label | input.review.object.metadata.labels[label]}
                    required := {label | label := input.parameters.labels[_]}
                    missing := required - provided
                    count(missing) > 0
                    msg := sprintf("you must provide labels: %v", [missing])
                  }
      - objectDefinition:
          apiVersion: constraints.gatekeeper.sh/v1beta1
          kind: K8sRequiredLabels
          metadata:
            name: ns-must-have-gk
            annotations:
              policy.open-cluster-management.io/severity: low 
          spec:
            enforcementAction: dryrun
            match:
              kinds:
                - apiGroups: [""]
                  kinds: ["Namespace"]
            parameters:
              labels: ["gatekeeper"]
  ```

  - Since the `remediationAction` is set to `inform`, the
    `enforcementAction` field of the Gatekeeper constraint is overridden
    to `warn`. This means that Gatekeeper detects and warns you about
    creating or updating a namespace that is missing the `gatekeeper`
    label. If the policy `remediationAction` is set to `enforce`, the
    Gatekeeper constraint `enforcementAction` field is overridden to
    `deny`. In this context, this configuration prevents any user from
    creating or updating a namespace that is missing the `gatekeeper`
    label.

  - **Optional:** Set a severity value for the
    `policy.open-cluster-management.io/severity` annotation for each
    Gatekeeper constraint or constraint template. Valid values are the
    same as for other Red Hat Advanced Cluster Management policy types:
    `low`, `medium`, `high`, or `critical`.

    With the previous policy, you might receive the following policy
    status message:
    `warn - you must provide labels: {"gatekeeper"} (on Namespace default); warn - you must provide labels: {"gatekeeper"} (on Namespace gatekeeper-system)`.
    When you delete Gatekeeper constraints or `ConstraintTemplates` from
    a policy, the constraints and `ConstraintTemplates` are also deleted
    from your managed cluster.

    To view the Gatekeeper audit results for a specific managed cluster
    from the console, go to to the policy template *Results* page. If
    search is enabled, view the YAML of the Kubernetes objects that
    failed the audit.

    **Notes:**

    - The *Related resources* section is only available when Gatekeeper
      generates audit results.

    - The Gatekeeper audit runs every minute by default. Audit results
      are sent back to the hub cluster to be viewed in the Red Hat
      Advanced Cluster Management policy status of the managed cluster.

- `policy-gatekeeper-admission`: Use the `policy-gatekeeper-admission`
  configuration policy within a Red Hat Advanced Cluster Management
  policy to check for Kubernetes API requests denied by the Gatekeeper
  admission webhook. View the following example:

  ``` yaml
  apiVersion: policy.open-cluster-management.io/v1
  kind: ConfigurationPolicy
  metadata:
    name: policy-gatekeeper-admission
  spec:
    remediationAction: inform 
    severity: low
    object-templates:
      - complianceType: mustnothave
        objectDefinition:
          apiVersion: v1
          kind: Event
          metadata:
            namespace: openshift-gatekeeper-system 
            annotations:
              constraint_action: deny
              constraint_kind: K8sRequiredLabels
              constraint_name: ns-must-have-gk
              event_type: violation
  ```

  - The `ConfigurationPolicy` `remediationAction` parameter is
    overwritten by `remediationAction` in the parent policy.

  - Set to the actual namespace where Gatekeeper is running if it is
    different.
