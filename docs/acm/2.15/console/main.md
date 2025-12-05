# Web console

## Console overview

Learn more about console components that you can use to view, manage, or
customize your console.

### Home

From the Red Hat Advanced Cluster Management for Kubernetes *Home* page
in the *Fleet Management* perspective, you can access more information
and you can search across the product. Click **Welcome** for more
introductory information about each product function.

#### Overview

Click **Overview** to see summary information, or to access clickable
*Cluster* percentage values for policy violations, and more.

From the *Overview* page, you can view the following information:

- Cluster and node counts across all clusters and for each provider

- Cluster status

- Cluster compliance

- Pod status

- Cluster add-ons

You can also access all APIs from the integrated console. Select the
**Administrator** perspective, then navigate to **Home** \> **API
Explorer** to explore API groups.

**Note:** For Red Hat OpenShift Container Platform versions earlier than
version 4.20, select **local-cluster** from the cluster switcher. Then
select **Home** \> **API Explorer** to explore API groups.

From the *Fleet Management* perspective, select **Overview** to access
cluster resource metrics.

The following information is displayed from the Overview page:

- Number of clusters

- Application types

- Number of enabled policies on your cluster

- Cluster version

- Total number of nodes on your cluster

- Number of worker cores

The following information from Red Hat Insights is displayed:

- Cluster recommendations

- Number of risk predictions

- Cluster health which includes the status and violations

- A view of your resources based on your custom query.

If observability is enabled, alert and failing operator metrics from
across your fleet are also displayed.

To learn about Search, see Search.

#### Command line tools

From the *Home* page, you can access Command Line Interface (CLI)
downloads by using the following steps:

1.  Click the `?` icon in the toolbar of the console.

2.  Click **Command Line Tools** from the drop-down menu.

3.  Find the **Advanced Cluster Management** header to find a list of
    tools that are available for Red Hat Advanced Cluster Management,
    which is specified with the operating system and architecture.

4.  Select the appropriate binary file to download and use on your local
    system.

### Infrastructure

From *Clusters*, you can create new clusters or import existing
clusters. From *Automation*, you can create an Ansible template.

For more information about managing clusters, see The multicluster
engine operator cluster lifecycle overview.

Additionally, see specific information on these cluster types at
Configuring Ansible Automation Platform tasks to run on managed
clusters.

### Applications

Create an application and edit a `.yaml` file. Access an overview or
more advanced information about each application. For more information
about application resources, see Managing applications.

### Governance

Create and edit a `.yaml` file to create a policy. Use the *Governance*
dashboard to manage policies and policy controllers.

For more information, see Governance.

### Credentials

The credential stores the access information for a cloud provider. Each
provider account requires its own credential, as does each domain on a
single provider.

Review your credentials or add a credential.

See Managing credentials overview for more specific information about
providers and credentials.

## Accessing your console

The Red Hat Advanced Cluster Management for Kubernetes web console is
integrated with the Red Hat OpenShift Container Platform web console as
a console plug-in. You can access Red Hat Advanced Cluster Management
within the OpenShift Container Platform console by selecting **Fleet
Management** from the perspective selector.

Select the **Administrator** perspective when you want to use OpenShift
Container Platform console features on the cluster where you installed
Red Hat Advanced Cluster Management. Select **Fleet Management** from
the perspective selector when you want to use Red Hat Advanced Cluster
Management features to manage your fleet of clusters.

**Important:** For Red Hat OpenShift Container Platform versions earlier
than version 4.20, select **All Clusters** from the cluster switcher. If
the cluster switcher is not present, the required console plug-ins might
not be enabled. Also select **`local-cluster`** from the cluster
switcher to use OpenShift Container Platform console features.

For new installations, the console plug-ins are enabled by default. If
you upgraded from a previous version of Red Hat Advanced Cluster
Management and want to enable the plug-ins, or if you want to disable
the plug-ins, complete the following steps:

1.  To disable the plug-in, be sure you are in the *Administrator*
    perspective in the OpenShift Container Platform console.

2.  Find **Administration** in the navigation and click **Cluster
    Settings**, then click the *Configuration* tab.

3.  From the list of *Configuration resources*, click the **Console**
    resource with the `operator.openshift.io` API group, which contains
    cluster-wide configuration for the web console.

4.  Select the *Console plug-ins* tab. Both the `acm` and `mce` plug-ins
    are listed.

5.  Modify plug-in status from the table. In a few moments, you are
    prompted to refresh the console.

**Note:** To enable and disable the console, see MultiClusterHub
advanced for information.

To learn more about the Red Hat Advanced Cluster Management for
Kubernetes console, see Console overview.
