# Red Hat Edge Manager (Technology Preview)

**Technology Preview:** The Red Hat Edge Manager provides streamlined
management of edge devices and applications through a declarative
approach.

By defining the required state of your edge devices, which includes your
operating system versions, host configurations, and application
deployments, the Red Hat Edge Manager automatically implements and
maintains these configurations across your entire device fleet.

By using the Red Hat Edge Manager on Red Hat Advanced Cluster Management
for Kubernetes, you can manage non-Kubernetes workloads and your
operating system configuration on a Red Hat Enterprise Linux machine
consistently with how you manage it on Red Hat OpenShift Container
Platform.

## Red Hat Edge Manager architecture

**Technology Preview:** You can manage individual devices or an entire
fleet by using the Red Hat Edge Manager. The Red Hat Edge Manager uses
an agent-based architecture that allows for a scalable and robust device
management, even with limited network conditions.

By deploying a Red Hat Edge Manager agent to a device, the agent
autonomously manages and monitors the device while periodically
communicating with the Red Hat Edge Manager service to check for new
configurations and to report device status.

The Red Hat Edge Manager supports image-based operating systems. You can
include the Red Hat Edge Manager agent and the agent configuration in
the image that is distributed to the devices.

Image-based operating systems allow the agent to initiate a
transactional update of the image and to roll back to the previous
version in case of an update error.

The Red Hat Edge Manager architecture has the following main features:

- Agent

- Service

- Image-based operating system

- API server

- Database

- Device

- Device fleet

### Red Hat Edge Manager agent and service

The Red Hat Edge Manager agent is a process running on each managed
device that periodically communicates the Red Hat Edge Manager service
on the Red Hat Advanced Cluster Management hub cluster. The agent is
responsible for the following tasks:

- Enrolling devices into the service

- Periodically checking with the service for changes in the device
  specification, such as changes to the operating system, configuration,
  and applications

- Applying any updates independently from the service

- Reporting status of the device and the applications

The Red Hat Edge Manager service is responsible for the following tasks:

- Authenticating and authorizing users and agents

- Enrolling devices

- Managing device inventory

- Reporting status from individual devices or fleets

The service also communicates with a database that stores the device
inventory and the target device configuration. When communicating with
the service, the agent polls the service for changes in the
configuration. If the agent detects that the current configuration
deviates from the target configuration, the agent attempts to apply the
changes to the device.

When the agent receives a new target configuration from the service, the
agent does the following tasks:

1.  To avoid depending on network connectivity during the update, the
    agent downloads all required resources, such as the operating system
    image and application container images, over the network to disk.

2.  The agent updates the operating system image by delegating to
    `bootc`.

3.  The agent updates configuration files on the file system of the
    device by overlaying a set of files that the service sends to the
    device.

4.  If necessary, the agent reboots into the new operating system.
    Otherwise, the agent signals system services and applications to
    reload the updated configuration.

5.  The agent updates applications running on Podman or MicroShift.

If the update fails or the system does not return online after
rebooting, the agent automatically rolls back to the previous operating
system image and configuration.

**Note:** You can maintain fleet definitions in Git. The Red Hat Edge
Manager periodically syncs with the fleet definitions in the database.

### Red Hat Edge Manager API server

The API server is a core component of the Red Hat Edge Manager service
that allows users and agents to communicate with the service.

The API server exposes the following endpoints:

User-facing API endpoint  
Users can connect to the user-facing API endpoint from the CLI or the
web console. Users must authenticate with the configured external
authentication service to obtain a JSON Web Token (JWT) to make HTTPS
requests.

Agent-facing API endpoint  
Agents connect to the agent-facing endpoint, which is mTLS-protected.
The service authenticates devices using the X.509 client certificates.

The Red Hat Edge Manager service also communicates with various external
systems to authenticate and authorize users, get mTLS certificates
signed, or query configuration for managed devices.

### Device enrollment

**Technology Preview:** You need to enroll devices to a Red Hat Edge
Manager service before you can start managing them. The Red Hat Edge
Manager agent that runs on a device handles the device enrollment.

When the agent starts on a device, the agent searches for the
configuration in the `/etc/flightctl/config.yaml` file. The file defines
the following configurations:

- The enrollment endpoint, which is the Red Hat Edge Manager service
  that the agent connects to for enrollment.

- The enrollment certificate, which is the X.509 client certificate and
  key that the agent only uses to securely request enrollment from the
  Red Hat Edge Manager service.

- **Optional:** Any additional agent configuration.

The agent starts the enrollment process by searching for the enrollment
endpoint, the Red Hat Edge Manager service, that is defined in the
configuration file.

After establishing a secure, mTLS-protected network connection with the
service, the agent submits an enrollment request to the service.

The request includes a description of hardware and operating system of
the device, a X.509 certificate signing request, and the cryptographic
identity of the device.

The enrollment request must be approved by an authorized user. After the
request is approved, the device becomes trusted and managed by the Red
Hat Edge Manager service.

#### Enrollment methods

You can provision the enrollment endpoint and certificate to the device
in the following ways:

Early binding  
You can build an operating system image that includes the enrollment
endpoint and certificate. Devices using an early binding image can
automatically connect to the defined Red Hat Edge Manager service to
request enrollment, without depending on any provisioning
infrastructure.

The devices share the same long-lived X.509 client certificate. However,
in this case, the devices are bound to a specific service and owner.

Late binding  
You can define the enrollment endpoint and certificate at provisioning
time instead of including them in the operating system image. Devices
using a late binding image are not bound to a single owner or service
and can have device-specific, short-lived X.509 client certificates.

However, late binding requires virtualization or bare metal provisioning
infrastructure that can request device-specific enrollment endpoints and
certificates from the Red Hat Edge Manager service and inject them into
the provisioned system by using mechanisms such as cloud-init, Ignition,
or kickstart.

**Note:** The enrollment certificate is only used to secure the network
connection for submitting an enrollment request. The enrollment
certificate is not involved in the actual verification or approval of
the enrollment request. The enrollment certificate is no longer used
with enrolled devices, as the devices rely on device-specific management
certificates instead.

## Enabling the Red Hat Edge Manager

**Technology Preview:** Enable the Red Hat Edge Manager to manage edge
devices and applications at scale.

**Required access:** Cluster administrator

### Enabling the Red Hat Edge Manager from the `MultiClusterHub` resource

Patch the `MultiClusterHub` resource, then verify that Red Hat Edge
Manager is enabled. Complete the following procedure:

1.  Set the `enabled` field to `true` in the `edge-manager-preview`
    entry of `spec.overrides.components` in the `Multiclusterhub`
    resource by running the following command:

    ``` bash
    oc patch multiclusterhubs.operator.open-cluster-management.io multiclusterhub -n open-cluster-management --type json --patch '[{"op": "add", "path":"/spec/overrides/components/-", "value": {"name":"edge-manager-preview","enabled": true}}]'
    ```

2.  Verify that the Red Hat Edge Manager is enabled by running the
    following command on the hub cluster:

    ``` bash
    oc -n open-cluster-management get pods | grep flightctl-api
    ```

    See the following example output:

    ``` bash
    flightctl-api                    2/2     Running   0             43s
    ```

### Enabling the Red Hat Edge Manager console

Enable Red Hat Edge Manager in the OpenShift Container Platform web
console. Complete the following procedure:

1.  Open the console for editing by running the following command:

    ``` bash
    oc edit console.v1.operator.openshift.io
    ```

2.  Enable the Red Hat Edge Manager console by adding `flightctl-plugin`
    to the `spec.plugins` section.

### Red Hat Edge Manager authorization

**Technology Preview:** The Red Hat Edge Manager Kubernetes
authorization uses role-based access control (RBAC) to control
authorization for Red Hat Edge Manager API endpoints.

You can set up Kubernetes RBAC authorization by using the following
roles in the `open-cluster-management` namespace:

- `Role` and `RoleBinding` for namespace-wide authorization

- `ClusterRole` and `ClusterRoleBinding` for cluster-wide authorization

You can use the `Role` or `ClusterRole` API objects to define the
allowed API resources and verbs for a particular role.

The `RoleBinding` or `ClusterRoleBinding` API objects grant permissions
that are defined in a role to one or more users.

For more information, see Role-based access control.

#### Red Hat Edge Manager RBAC roles

The Red Hat Edge Manager has the following default roles and their
permissions:

- Roles - Permissions - Resources

- flightctl-admin - All - All

- flightctl-viewer - get, list - devices, fleets, resourcesyncs

- flightctl-operator - get, list, create, delete, update, patch -
  devices, fleets, resourcesyncs

- get - devices/console

- get, list - repositories, fleets, templateversions

- flightctl-installer - get, list - enrollmentrequests

- post - enrollmentrequests/approval

- get, list, create - certificatesigningrequests

#### Red Hat Edge Manager authorization resources

The following table contains the routes, names, resource names, and
verbs for the Red Hat Edge Manager API endpoints:

- Route - Name - Resource - Verb

- DELETE /api/v1/certificatesigningrequests -
  DeleteCertificateSigningRequests - certificatesigningrequests -
  deletecollection

- GET /api/v1/certificatesigningrequests -
  ListCertificateSigningRequests - certificatesigningrequests - list

- POST /api/v1/certificatesigningrequests -
  CreateCertificateSigningRequest - certificatesigningrequests - create

- DELETE /api/v1/certificatesigningrequests/{name} -
  DeleteCertificateSigningRequest - certificatesigningrequests - delete

- GET /api/v1/certificatesigningrequests/{name} -
  ReadCertificateSigningRequest - certificatesigningrequests - get

- PATCH /api/v1/certificatesigningrequests/{name} -
  PatchCertificateSigningRequest - certificatesigningrequests - patch

- PUT /api/v1/certificatesigningrequests/{name} -
  ReplaceCertificateSigningRequest - certificatesigningrequests - update

- DELETE /api/v1/certificatesigningrequests/{name}/approval -
  DenyCertificateSigningRequest - certificatesigningrequests/approval -
  delete

- POST /api/v1/devices - CreateDevice - devices - create

- GET /api/v1/devices - ListDevices - devices - list

- DELETE /api/v1/devices - DeleteDevices - devices - deletecollection

- GET /api/v1/devices/{name} - ReadDevice - devices - get

- PUT /api/v1/devices/{name} - ReplaceDevice - devices - update

- DELETE /api/v1/devices/{name} - DeleteDevice - devices - delete

- GET /api/v1/devices/{name}/status - ReadDeviceStatus -
  devices/status - get

- PUT /api/v1/devices/{name}/status - ReplaceDeviceStatus -
  devices/status - update

- GET /api/v1/devices/{name}/rendered - GetRenderedDevice -
  devices/rendered - get

- PUT /api/v1/devices/{name}/decommission - DecommissionDevice -
  devices/decommission - update

- GET /ws/v1/devices/{name}/console - DeviceConsole - devices/console -
  get

- POST /api/v1/enrollmentrequests - CreateEnrollmentRequest -
  enrollmentrequests - create

- GET /api/v1/enrollmentrequests - ListEnrollmentRequests -
  enrollmentrequests - list

- DELETE /api/v1/enrollmentrequests - DeleteEnrollmentRequests -
  enrollmentrequests - deletecollection

- GET /api/v1/enrollmentrequests/{name} - ReadEnrollmentRequest -
  enrollmentrequests - get

- PUT /api/v1/enrollmentrequests/{name} - ReplaceEnrollmentRequest -
  enrollmentrequests - update

- PATCH /api/v1/enrollmentrequests/{name} - PatchEnrollmentRequest -
  enrollmentrequests - patch

- DELETE /api/v1/enrollmentrequests/{name} - DeleteEnrollmentRequest -
  enrollmentrequests - delete

- GET /api/v1/enrollmentrequests/{name}/status -
  ReadEnrollmentRequestStatus - enrollmentrequests/status - get

- POST /api/v1/enrollmentrequests/{name}/approval -
  ApproveEnrollmentRequest - enrollmentrequests/approval - post

- PUT /api/v1/enrollmentrequests/{name}/status -
  ReplaceEnrollmentRequestStatus - enrollmentrequests/status - update

- POST /api/v1/fleets - CreateFleet - fleets - create

- GET /api/v1/fleets - ListFleets - fleets - list

- DELETE /api/v1/fleets - DeleteFleets - fleets - deletecollection

- GET /api/v1/fleets/{name} - ReadFleet - fleets - get

- PUT /api/v1/fleets/{name} - ReplaceFleet - fleets - update

- DELETE /api/v1/fleets/{name} - DeleteFleet - fleets - delete

- GET /api/v1/fleets/{name}/status - ReadFleetStatus - fleets/status -
  get

- PUT /api/v1/fleets/{name}/status - ReplaceFleetStatus -
  fleets/status - update

- POST /api/v1/repositories - CreateRepository - repositories - create

- GET /api/v1/repositories - ListRepositories - repositories - list

- DELETE /api/v1/repositories - DeleteRepositories - repositories -
  deletecollection

- PUT /api/v1/repositories/{name} - ReplaceRepository - repositories -
  update

- DELETE /api/v1/repositories/{name} - DeleteRepository - repositories -
  delete

- POST /api/v1/resourcesyncs - CreateResourceSync - resourcesyncs -
  create

- GET /api/v1/resourcesyncs - ListResourceSync - resourcesyncs - list

- DELETE /api/v1/resourcesyncs - DeleteResourceSyncs - resourcesyncs -
  deletecollection

- GET /api/v1/resourcesyncs/{name} - ReadResourceSync - resourcesyncs -
  get

- PUT /api/v1/resourcesyncs/{name} - ReplaceResourceSync -
  resourcesyncs - update

- DELETE /api/v1/resourcesyncs/{name} - DeleteResourceSync -
  resourcesyncs - delete

- GET /api/v1/fleets/{fleet}/templateVersions - ListTemplateVersions -
  fleets/templateversions - list

- DELETE /api/v1/fleets/{fleet}/templateVersions -
  DeleteTemplateVersions - fleets/templateversions - deletecollection

- GET /api/v1/fleets/{fleet}/templateVersions/{name} -
  ReadTemplateVersion - fleets/templateversions - get

- DELETE /api/v1/fleets/{fleet}/templateVersions/{name} -
  DeleteTemplateVersion - fleets/templateversions - delete

## Operating system images for the Red Hat Edge Manager

Image-based operating systems allow the operating system and the
configuration and applications to be versioned, deployed, and updated as
a single unit. Using an image-based operating system reduces operational
risks with the following capability:

- Minimizing drift between tested and deployed environments.

- Reducing failed updates through transactional updates and rollbacks,
  and reducing maintenance and replacement costs.

The Red Hat Edge Manager focuses on image-based Linux operating systems
that run bootable container image (`bootc`). For more information, see
bootc.

**Important:** The `bootc` tool does not update package-based operating
systems.

See the following description for the operating system images process:

- Choose a base `bootc` operating system image, such as a Fedora,
  CentOS, or RHEL image.

- Create a container file that layers the following items onto the base
  `bootc` image:

  - The Red Hat Edge Manager agent and configuration.

  - Optional: Any drivers specific to your target deployment
    environment.

  - Optional: Host configuration, for example certificate authority
    bundles, and application workloads that are common to all
    deployments.

- Build, publish, and sign a `bootc` operating system image using
  `podman` and `skopeo`.

- Create an operating system disk image by using `bootc-image-builder`.

- Build, publish, and sign an operating system disk image using
  `skopeo`.

**Note:** The operating system disk image contains partitions, volumes,
the file system, and the initial `bootc` image. The operating system
disk image only needs to be created once, during provisioning.

For subsequent device updates, only the `bootc` operating system image
is required, which contains the files in the file system.

### Special considerations for building images

#### Build-time configuration over dynamic runtime configuration

Add configuration to the operating system image at build time. Adding
configuration at build time ensures that the configurations are tested,
distributed, and updated together. In cases when build-time
configuration is not feasible or desirable, you can dynamically
configure devices at runtime instead with the Red Hat Edge Manager.

Dynamic runtime configuration is preferable in the following cases:

- You have a configuration that is deployment or site-specific, such as
  a hostname or a site-specific network credential.

- You have secrets that are not secure to distribute with the image.

- You have application workloads that need to be added, updated, or
  deleted without reboot or they are on a faster cadence than the
  operating system.

#### Configuration in `/usr` directory

Place configuration files in the `/usr` directory if the configuration
is static and the application or service supports that configuration. By
placing the configuration in the `/usr` directory, the configuration
remains read-only and fully defined by the image.

It is not feasible or desirable to place the configuration in the `/usr`
directory in the following cases:

- The configuration is deployment or site-specific.

- The application or service only supports reading configuration from
  the `/etc` directory.

- The configuration might need to be changed at runtime.

#### Drop-in directories

Use drop-in directories to add, replace, or remove configuration files
that the service aggregates. Do not directly edit your configuration
files that might cause deviation from the target configuration.

**Note:** You can identify drop-in directories by the `.d/` at the end
of the directory name. For example, `/etc/containers/certs.d`,
`/etc/cron.d`, and `/etc/NetworkManager/conf.d`.

#### Operating system images with scripts

Avoid executing scripts or commands that change the file system. The
`bootc` or the Red Hat Edge Manager can overwrite the changed files that
might cause a deviation or failed integrity checks.

Instead, run such scripts or commands during image building, so changes
are part of the image. Alternatively, use the configuration management
mechanisms of the Red Hat Edge Manager.

### Building a *bootc* operating system image for the Red Hat Edge Manager

**Technology Preview:** To prepare your device to be managed by the Red
Hat Edge Manager, build a `bootc` operating system image that contains
the Red Hat Edge Manager agent. Then build an operating system disk
image for your devices.

#### Installing the Red Hat Edge Manager CLI

To install the Red Hat Edge Manager CLI, complete the following steps:

1.  Enable the subscription manager for the repository appropriate for
    your system by running the following command. Replace `rhacm-<2.x>`
    and `rhel-<version>` with the version of the products that you are
    using:

    ``` bash
    subscription-manager repos --enable rhacm-<2.x>-for-rhel-<version>-<arch>-rpms
    ```

    For a full list of available repositories for the Red Hat Edge
    Manager, see the *Additional resources* section.

2.  Install the `flightctl` CLI with your package manager. Run the
    following command:

    ``` bash
    sudo dnf install flightctl
    ```

#### Optional: Requesting an enrollment certificate for early binding

If you want to include an agent configuration in the image, complete the
following steps:

1.  Get the Red Hat Edge Manager application interface server. Run the
    following command:

    ``` bash
    export RHEM_API_SERVER_URL=$(oc get route -n open-cluster-management flightctl-api-route -o json | jq -r .spec.host)
    ```

2.  Authenticate with the Red Hat Edge Manager service by using the
    `flightctl` CLI. Run the following command:

    ``` bash
    flightctl login --username=<your_user> --password=<your_password> https://$RHEM_API_SERVER_URL
    ```

    **Note:** The CLI uses the certificate authority pool of the host to
    verify the identity of the Red Hat Edge Manager service. The
    verification can lead to a TLS verification error when using
    self-signed certificates, if you do not add your certificate
    authority certificate to the pool. You can bypass the server
    verification by adding the `--insecure-skip-tls-verify` flag to your
    command.

3.  Obtain the enrollment credentials in the format of an agent
    configuration file by running the following command:

    ``` bash
    flightctl certificate request --signer=enrollment --expiration=365d --output=embedded > config.yaml
    ```

    **Notes:**

    - The `--expiration=365d` option specifies that the credentials are
      valid for a year.

    - The `--output=embedded` option specifies that the output is an
      agent configuration file with the enrollment credentials embedded.

      The returned `config.yaml` contains the URLs of the Red Hat Edge
      Manager service, the certificate authority bundle, and the
      enrollment client certificate and key for the agent. See the
      following example:

    ``` yaml
    enrollment-service:
      authentication:
        client-certificate-data: LS0tLS1CRUdJTiBD...
        client-key-data: LS0tLS1CRUdJTiBF...
      service:
        certificate-authority-data: LS0tLS1CRUdJTiBD...
        server: https://agent-api.flightctl.127.0.0.1.nip.io:7443
      enrollment-ui-endpoint: https://ui.flightctl.127.0.0.1.nip.io:8081
    ```

#### Optional: Using image pull secrets

If your device relies on containers from a private repository, you must
configure a pull secret for the registry. Complete the following steps:

1.  Depending on the kind of container image you use, place the pull
    secret in one or both of the following system paths on the device:

    - Operating system images use the `/etc/ostree/auth.json` path.

    - Application container images use the
      `/root/.config/containers/auth.json` path.

    **Important:** The pull secret must exist on the device before the
    secret can be consumed.

2.  Ensure that the pull secrets have the following format:

    ``` json
    {
      "auths": {
        "registry.example.com": {
          "auth": "base64-encoded-credentials"
        }
      }
    }
    ```

For more information, see the *Additional resources* section.

#### Building the operating system image with *bootc*

Build the operating system image with `bootc` that contains the Red Hat
Edge Manager agent. You can optionally include the following items in
your operating system image:

- The agent configuration for early binding

- Any drivers

- Host configuration

- Application workloads that you need

**Note:** You must build the operating system image on a Red Hat
Enterprise Linux host that has the required entitlement for the
specified `rhacm` repository.

Complete the following steps:

1.  Create a `Containerfile` file with the following content to build a
    Red Hat Enterprise Linux based operating system image that includes
    the Red Hat Edge Manager agent and configuration. Replace
    `rhacm-<2.x>` and `rhel-<version>` with the version of the products
    that you are using:

    ``` bash
    FROM registry.redhat.io/rhel9/rhel-bootc:<required_os_version> 

    RUN dnf config-manager --set-enabled rhacm-<2.x>-for-rhel-<version>-$(uname -m)-rpms && \
        dnf -y install flightctl-agent && \
        dnf -y clean all && \
        systemctl enable flightctl-agent.service && \
        systemctl mask bootc-fetch-apply-updates.timer 
    ```

    - The base image that is referenced in `FROM` is a bootable
      container (`bootc`) image that already contains a Linux kernel,
      which allows you to reuse existing standard container build tools
      and workflows.

    - Disables the default automatic updates. The updates are managed by
      the Red Hat Edge Manager.

    **Important:** If your device relies on containers from a private
    repository, the device pull secret must be placed in the
    `/etc/ostree/auth.json` path. The pull secret must exist on the
    device before the secret can be consumed.

    1.  **Optional:** To enable `podman-compose` application support,
        add the following section to the `Containerfile` file:

        ``` bash
        RUN dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
            dnf -y install podman-compose && \
            dnf -y clean all && \
            systemctl enable podman.service
        ```

    2.  **Optional:** If you created the `config.yaml` for early
        binding, add the following section to the `Containerfile`:

        ``` bash
        ADD config.yaml /etc/flightctl/
        ```

    For more information, see Optional: Requesting an enrollment
    certificate for early binding.

2.  Define the Open Container Initiative (OCI) registry by running the
    following command:

    ``` bash
    OCI_REGISTRY=registry.redhat.io
    ```

3.  Define the image repository that you have permissions to write to by
    running the following command:

    ``` bash
    OCI_IMAGE_REPO=${OCI_REGISTRY}/<your_org>/<your_image>
    ```

4.  Define the image tag by running the following command:

    ``` bash
    OCI_IMAGE_TAG=v1
    ```

5.  Build the operating system image for your target platform:

    ``` bash
    sudo podman build -t ${OCI_IMAGE_REPO}:${OCI_IMAGE_TAG} .
    ```

#### Signing and publishing the *bootc* operating system image by using Sigstore

To sign the `bootc` operating system image by using Sigstore, complete
the following steps:

1.  Generate a Sigstore key pair named `signingkey.pub` and
    `signingkey.private`:

    ``` bash
    skopeo generate-sigstore-key --output-prefix signingkey
    ```

2.  Configure container tools such as Podman and Skopeo to upload
    Sigstore signatures together with your signed image to your OCI
    registry:

    ``` bash
    sudo tee "/etc/containers/registries.d/${OCI_REGISTRY}.yaml" > /dev/null <<EOF
    docker:
        ${OCI_REGISTRY}:
            use-sigstore-attachments: true
    EOF
    ```

3.  Log in to your OCI registry by running the following command:

    ``` bash
    sudo podman login ${OCI_REGISTRY}
    ```

4.  Sign and publish the operating system image by running the following
    command:

    ``` bash
    sudo podman push \
        --sign-by-sigstore-private-key ./signingkey.private \
        ${OCI_IMAGE_REPO}:${OCI_IMAGE_TAG}
    ```

#### Building the operating system disk image

Build the operating system disk image that contains the file system for
your devices. Complete the following steps:

1.  Create a directory called `output` by running the following command:

    ``` bash
    mkdir -p output
    ```

2.  Use `bootc-image-builder` to generate an operating system disk image
    of type `iso` from your operating system image. Run the following
    command:

    ``` bash
    sudo podman run --rm -it --privileged --pull=newer \
        --security-opt label=type:unconfined_t \
        -v "${PWD}/output":/output \
        -v /var/lib/containers/storage:/var/lib/containers/storage \
        registry.redhat.io/rhel9/bootc-image-builder:latest \
        --type iso \
        ${OCI_IMAGE_REPO}:${OCI_IMAGE_TAG}
    ```

When the `bootc-image-builder` completes, you can find the ISO disk
image at the `${PWD}/output/bootiso/install.iso` path.

#### Optional: Signing and publishing the operating system disk image to an Open Container Initiative registry

Sign and publish your disk image to your Open Container Initiative (OCI)
registry. Optionally, you can compress and publish the disk image as an
OCI artifact to the same OCI registry as your `bootc` images, which
facilitates a unified hosting and distribution of `bootc` and disk
images. To publish your ISO disk image to a repository named after your
`bootc` image with `/diskimage-iso` appended, complete the following
steps:

##### Optional: Signing and publishing the operating system disk image to an OCI registry

Sign and publish your disk image to your OCI registry. Complete the
following steps:

1.  Change the owner of the directory where the ISO disk image is
    located from `root` to your current user. Run the following command:

    ``` bash
    sudo chown -R $(whoami):$(whoami) "${PWD}/output"
    ```

2.  Define the `OCI_DISK_IMAGE_REPO` environmental variable to be the
    same repository as your `bootc` image with `/diskimage-iso`
    appended. Run the following command:

    ``` bash
    OCI_DISK_IMAGE_REPO=${OCI_IMAGE_REPO}/diskimage-iso
    ```

3.  Create a manifest list by running the following command:

    ``` bash
    sudo podman manifest create \
        ${OCI_DISK_IMAGE_REPO}:${OCI_IMAGE_TAG}
    ```

4.  Add the ISO disk image to the manifest list as an OCI artifact by
    running the following command:

    ``` bash
    sudo podman manifest add \
        --artifact --artifact-type application/vnd.diskimage.iso \
        --arch=amd64 --os=linux \
        ${OCI_DISK_IMAGE_REPO}:${OCI_IMAGE_TAG} \
        "${PWD}/output/bootiso/install.iso"
    ```

5.  Sign the manifest list with your private Sigstore key and push the
    image to the registry. Run the following command:

    ``` bash
    sudo podman manifest push --all \
         --sign-by-sigstore-private-key ./signingkey.private \
        ${OCI_DISK_IMAGE_REPO}:${OCI_IMAGE_TAG} \
        docker://${OCI_DISK_IMAGE_REPO}:${OCI_IMAGE_TAG}
    ```

### Building for specific target platforms

For optimized provisioning and integration with Red Hat OpenShift
Virtualization and VMware vSphere, enrollment certificates and agent
configurations can be provided with `cloud-init` utility, rather than
embedding them in the image. Additionally, you can include appropriate
guest tools for better platform integration. This process generates
platform-specific image formats, such as `QCOW2` for Red Hat OpenShift
Virtualization and `VMDK` for vSphere.

#### Building images for Red Hat OpenShift Virtualization

When building operating system images and disk images for Red Hat
OpenShift Virtualization, you can follow the Building a bootc operating
system image for the Red Hat Edge Manager process with the following
changes:

- Use late binding by injecting the enrollment certificate or the agent
  configuration through `cloud-init` when provisioning the virtual
  device.

- Add the `open-vm-tools` guest tools to the image.

- Build a disk image of type `qcow2` instead of `iso`.

**Note:** You must build the operating system image on a Red Hat
Enterprise Linux host that has the required entitlement for the
specified `rhacm` repository.

Complete the generic steps with changes to the following steps:

1.  Build an operating system image that is based on RHEL 9 that
    includes the Red Hat Edge Manager agent and virtual machine guest
    tools, but excludes the agent configuration.

2.  Create a file named `Containerfile` with the following content.
    Replace `rhacm-<2.x>` and `rhel-<version>` with the version of the
    products that you are using:

    ``` bash
    FROM registry.redhat.io/rhel9/bootc-image-builder:latest

    RUN dnf config-manager --set-enabled rhacm-<2.x>-for-rhel-<version>-$(uname -m)-rpms && \
        dnf -y install flightctl-agent && \
        dnf -y clean all && \
        systemctl enable flightctl-agent.service

    RUN dnf -y install cloud-init open-vm-tools && \
        dnf -y clean all && \
        ln -s ../cloud-init.target /usr/lib/systemd/system/default.target.wants && \
        systemctl enable vmtoolsd.service
    ```

3.  **Optional:** To enable `podman-compose` application support, add
    the following section to the `Containerfile` file:

    ``` bash
    RUN dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm && \
        dnf -y install podman-compose && \
        dnf -y clean all && \
        systemctl enable podman.service
    ```

Build, sign, and publish the `bootc` operating system image by following
the generic image building process.

1.  Create a directory called `output` by running the following command:

    ``` bash
    mkdir -p output
    ```

2.  Generate an operating system disk image of type `vmdk` from your
    operating system image by running the following command:

    ``` bash
    sudo podman run --rm -it --privileged --pull=newer \
        --security-opt label=type:unconfined_t \
        -v "${PWD}/output":/output \
        -v /var/lib/containers/storage:/var/lib/containers/storage \
        registry.redhat.io/rhel9/bootc-image-builder:latest \
        --type qcow2 \
        ${OCI_IMAGE_REPO}:${OCI_IMAGE_TAG}
    ```

When `bootc-image-builder` completes, you can find the disk image in the
`${PWD}/output/vmdk/disk.vmdk` path.

Red Hat OpenShift Virtualization can download disk images from an Open
Container Initiative (OCI) registry, but it uses a container disk image
instead of an OCI artifact.

Complete the following steps to build, sign, and upload the `QCoW2` disk
image:

1.  Create a file that is named `Containerfile.qcow2` with the following
    content:

    ``` bash
    FROM registry.access.redhat.com/ubi9/ubi:latest AS builder
    ADD --chown=107:107 output/qcow2/disk.qcow2 /disk/ 
    RUN chmod 0440 /disk/* 
    FROM scratch
    COPY --from=builder /disk/* /disk/ 
    ```

    - Adds the QCoW2 disk image to a builder container to set the
      required `107` file ownership, which is the QEMU user.

    - Sets the required `0440` file permissions.

    - Copies the file to a scratch image.

2.  Build, sign, and publish your disk image. Run the following command:

    ``` bash
    sudo chown -R $(whoami):$(whoami) "${PWD}/output"
    OCI_DISK_IMAGE_REPO=${OCI_IMAGE_REPO}/diskimage-qcow2
    sudo podman build -t ${OCI_DISK_IMAGE_REPO}:${OCI_IMAGE_TAG} -f Containerfile.qcow2 .
    sudo podman push --sign-by-sigstore-private-key ./signingkey.private ${OCI_DISK_IMAGE_REPO}:${OCI_IMAGE_TAG}
    ```

#### Building images for VMware vSphere

When building operating system images and disk images for VMware
vSphere, you can follow the Building a bootc operating system image for
the Red Hat Edge Manager process with the following changes:

- Using late binding by injecting the enrollment certificate or the
  agent configuration through `cloud-init` when provisioning the virtual
  device.

- Adding the `open-vm-tools` guest tools to the image.

- Building a disk image of type `vmdk` instead of `iso`.

Build an operating system image that is based on RHEL 9 that includes
the Red Hat Edge Manager agent and VM guest tools, but excludes the
agent configuration.

**Note:** You must build the operating system image on a Red Hat
Enterprise Linux host that has the required entitlement for the
specified `rhacm` repository.

Complete the generic steps with changes to the following steps:

1.  Create a file that is named `Containerfile` with the following
    content. Replace `rhacm-<2.x>` and `rhel-<version>` with the version
    of the products that you are using:

    ``` bash
    FROM registry.redhat.io/rhel9/bootc-image-builder:latest

    RUN dnf config-manager --set-enabled rhacm-<2.x>-for-rhel-<version>-$(uname -m)-rpms && \
        dnf -y install flightctl-agent && \
        dnf -y clean all && \
        systemctl enable flightctl-agent.service && \

    RUN dnf -y install cloud-init open-vm-tools && \
        dnf -y clean all && \
        ln -s ../cloud-init.target /usr/lib/systemd/system/default.target.wants && \
        systemctl enable vmtoolsd.service
    ```

2.  Create a directory named `output` by running the following command:

    ``` bash
    mkdir -p output
    ```

3.  Generate an operating system disk image of type `vmdk` from your
    operating system image by running the following command:

    ``` bash
    sudo podman run --rm -it --privileged --pull=newer \
        --security-opt label=type:unconfined_t \
        -v "${PWD}/output":/output \
        -v /var/lib/containers/storage:/var/lib/containers/storage \
        registry.redhat.io/rhel9/bootc-image-builder:latest \
        --type vmdk \
        ${OCI_IMAGE_REPO}:${OCI_IMAGE_TAG}
    ```

When `bootc-image-builder` completes, you can find the disk image in the
`${PWD}/output/vmdk/disk.vmdk` path.

## Provisioning devices

**Technology Preview:** You can provision devices with the Red Hat Edge
Manager in different environments. Use the operating system image or
disk image that you built for use with the Red Hat Edge Manager and
depending on your target environment, provision a physical or virtual
device.

**Required access:** Cluster administrator

### Provisioning physical devices

**Technology Preview:** When you build an ISO disk image from an
operating system image by using the `bootc-image-builder` tool, the
image is similar to the RHEL ISOs available for download. However, your
operating system image content is embedded in the ISO disk image.

To install the ISO disk image to a bare metal system without having
access to the network, see Deploying a custom ISO container image.

For information about installing the ISO through the network, see
Deploying an ISO bootc image over PXE boot.

### Provisioning devices on OpenShift Virtualization

**Technology Preview:** You can provision a virtual machine on OpenShift
Virtualization by using a QCoW2 container disk image that is hosted on
an OCI container registry.

If your operating system image does not already contain the Red Hat Edge
Manager agent enrollment configuration, you can inject the configuration
through the `cloud-init` user data at provisioning.

For more information, see the *Additional resources* section.

#### Prerequisites

- You installed the `flightctl` CLI and logged in to your Red Hat Edge
  Manager service instance.

- You installed the `oc` CLI, used it to log in to your OpenShift
  cluster instance, and changed to the project in which you want to
  create your virtual machine.

#### Creating the *cloud-init* configuration

To create the `cloud-init` configuration, complete the following steps:

1.  Request a new Red Hat Edge Manager agent enrollment configuration
    and store it in a file called `config.yaml`. Run the following
    command:

    ``` bash
    flightctl certificate request --signer=enrollment --expiration=365d --output=embedded > config.yaml
    ```

2.  Create a cloud configuration user data file called
    `cloud-config.yaml` that places the agent configuration in the
    correct location on the first boot. Run the following command:

    ``` bash
    cat <<EOF > cloud-config.yaml
    #cloud-config
    write_files:
    - path: /etc/flightctl/config.yaml
      content: $(cat config.yaml | base64 -w0)
      encoding: b64
    EOF
    ```

3.  Create a Kubernetes `Secret` that contains the cloud configuration
    user data file:

    ``` bash
    oc create secret generic enrollment-secret --from-file=userdata=cloud-config.yaml
    ```

#### Creating the virtual machine

Create a virtual machine that has its primary disk populated from your
QCoW2 container disk image and a `cloud-init` configuration drive that
is populated from your enrollment secret. Complete the following steps:

1.  Create a file that contains a the `VirtualMachine` resource manifest
    by running the following command:

    ``` bash
    cat <<EOF > my-bootc-vm.yaml
    apiVersion: kubevirt.io/v1
    kind: VirtualMachine
    metadata:
      name: my-bootc-vm
    spec:
      runStrategy: RerunOnFailure
      template:
        spec:
          domain:
            cpu:
              cores: 1
            memory:
              guest: 1024M
            devices:
              disks:
                - name: containerdisk
                  disk:
                    bus: virtio
                - name: cloudinitdisk
                  disk:
                    bus: virtio
          volumes:
            - name: containerdisk
              containerDisk:
                image: ${OCI_DISK_IMAGE_REPO}:${OCI_IMAGE_TAG}
            - name: cloudinitdisk
              cloudInitConfigDrive:
                secretRef:
                  name: enrollment-secret
    EOF
    ```

2.  Apply the resource manifest to your cluster by running the following
    command:

    ``` bash
    oc apply -f my-bootc-vm.yaml
    ```

## Managing devices

**Technology Preview:** The Red Hat Edge Manager manages the device
lifecycle from enrollment to decommissioning of a device. The device
lifecycle also includes device management, such as organizing,
monitoring, and updating your devices with the Red Hat Edge Manager.

You can manage your devices individually or in a fleet. The Red Hat Edge
Manager allows you to manage a whole fleet of devices as a single object
instead of managing many devices individually.

You only need to specify the desired configuration once and then, the
Red Hat Edge Manager applies the configuration to all devices in the
fleet.

Understanding individual device management is the foundation for
managing devices in a fleet. You might want to manage your devices
individually in the following scenarios:

- If a few devices have significantly different configuration.

- If you use external automation for updating the devices.

**Required access:** Cluster administrator

To learn more about managing your devices in a fleet, see Managing
device fleets.

### Enrolling devices

**Technology Preview:** To manage your devices with the Red Hat Edge
Manager, you must enroll the devices to the Red Hat Edge Manager
service.

The first time the Red Hat Edge Manager agents runs on a device, the
agent prepares for the enrollment process by generating a cryptographic
key pair. The cryptographic key pair of the device consists of a public
and a private key. The private key never leaves the device, so that the
device cannot be duplicated or impersonated. The key pair is registered
with the Red Hat Edge Manager service during enrollment and is deleted
during decommissioning of the device.

When the device is not yet enrolled, the agent performs service
discovery to find its Red Hat Edge Manager service instance. Then, the
device establishes a secure, mTLS-protected network connection to the
service. The device uses its X.509 enrollment certificate that the
device acquired during image building or device provisioning. The device
submits an enrollment request to the service that includes the
following:

- a description of the device hardware and operating system

- an X.509 Certificate Signing Request which includes the cryptographic
  identity of the device to obtain the initial management certificate

The device is not considered trusted and remains quarantined in a device
lobby until an authorized user approves or denies the request.

#### Prerequisites

- You must install the Red Hat Edge Manager CLI. See Installing the Red
  Hat Edge Manager CLI.

- You must log in to the Red Hat Edge Manager service.

#### Enrolling devices using the CLI

You must enroll devices into the Red Hat Edge Manager service before you
can manage them. Complete the following steps:

1.  List all devices that are currently waiting for approval by running
    the following command:

    ``` bash
    flightctl get enrollmentrequests --field-selector="status.approval.approved != true"
    ```

    See the following example output:

    ``` bash
    NAME           APPROVAL  APPROVER  APPROVED LABELS
    <device_name>  Pending   <none>    <none>
    ```

    **Note:** The unique device name is generated by the agent and
    cannot be changed. The agent chooses a base32-encoded hash of its
    public key as device name.

2.  Approve an enrollment request by specifying the name of the
    enrollment request. Optionally, you can add labels to the device by
    using the `--label` or `-l` flags. See the following example:

    ``` bash
    flightctl approve -l region=eu-west-1 -l site=factory-berlin enrollmentrequest/54shovu028bvj6stkovjcvovjgo0r48618khdd5huhdjfn6raskg
    ```

    See the following example output:

    ``` bash
    NAME           APPROVAL  APPROVER  APPROVED LABELS
    <device_name>  Approved  user      region=eu-west-1,site=factory-berlin
    ```

After you approve the enrollment request, the service issues the
management certificate and registers the device in the inventory. The
device is now ready to be managed.

### Viewing devices

**Technology Preview:** To obtain more information about the devices in
your inventory, you can use the Red Hat Edge Manager CLI.

#### Prerequisites

- You must install the Red Hat Edge Manager CLI. See Installing the Red
  Hat Edge Manager CLI.

- You must log in to the Red Hat Edge Manager service.

- You must enroll at least one device.

#### View device inventory and device details

View devices in your device inventory. Complete the following steps:

1.  View the devices in the device inventory by running the following
    command:

    ``` bash
    flightctl get devices
    ```

    See the following example output:

    ``` bash
    NAME           ALIAS    OWNER   SYSTEM  UPDATED     APPLICATIONS  LAST SEEN
    <device_name>  <none>   <none>  Online  Up-to-date  <none>        3 seconds ago
    ```

2.  View the details of this device in YAML format by running the
    following command:

    ``` bash
    flightctl get device/<device_name> -o yaml
    ```

    See the following example output:

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Device
    metadata:
      name: <device_name>
      labels: 
        region: eu-west-1
        site: factory-berlin
    spec:
      os:
        image: quay.io/flightctl/rhel:9.5 
      config:
      - name: my-os-configuration 
        configType: GitConfigProviderSpec
        gitRef:
          path: /configuration
          repository: my-configuration-repo
          targetRevision: production
    status:
      os:
        image: quay.io/flightctl/rhel:9.5 
      config:
        renderedVersion: "1" 
      applications:
        data: {} 
        summary:
          status: Unknown 
      resources: 
        cpu: Healthy
        disk: Healthy
        memory: Healthy
      systemInfo: 
        architecture: amd64
        bootID: 037750f7-f293-4c5b-b06e-481eef4e883f
        operatingSystem: linux
      summary:
        info: ""
        status: Online 
      updated:
        status: UpToDate 
      lastSeen: "2024-08-28T11:45:34.812851905Z" 
    [...]
    ```

    - User-defined labels assigned to the device.

    - The target OS image version of the device.

    - The target OS configuration of the device.

    - The current OS image version of the device

    - The current OS configuration version of the device.

    - The current list of deployed applications of the device.

    - The health status of applications on the device.

    - The availability of CPU, disk, and memory resources.

    - Basic system information.

    - The health status of the device.

    - The update status of the device.

    - The last check-in time and date of the device.

### Labels and label selectors

**Technology Preview:** You can organize your resources, including
individual devices, fleets and any other resources, by assigning them
labels. For example, you can use labels to record location, hardware
type, or purpose. The Red Hat Edge Manager labels follow the same
syntax, principles, and operators as Kubernetes labels and label
selectors.

You can select devices with labels when viewing the device inventory or
applying operations to the devices.

Labels follow the `key=value` format, where you want to use the key to
group devices. For example, if your labels follow the `site=<location>`
naming convention, you can group your devices by site.

You can also use labels that only consist of keys.

Labels must adhere to the following rules to be valid:

- Keys and value must each be 63 characters or less.

- Keys and values can consist of alphanumeric characters (`a-z`, `A-Z`,
  `0-9`).

- Keys and values can also contain dashes (`-`), underscores (`_`), dots
  (`.`) but not as the first or last character.

- Value can be omitted.

You can apply labels to resources in the following ways:

- Define a set of default labels during image building that are
  automatically applied to all devices during deployment.

- Assign initial labels during enrollment.

- Assign labels post-enrollment.

When resources are labeled, you can select a subset of resources by
writing a label selector. A label selector is a comma-separated list of
labels for selecting resources that have the same set of labels.

See the following examples:

- Example label selector: site=factory-berlin - Selected devices: All
  devices with a site label key and a factory-berlin label value.

- Example label selector: site!=factory-berlin - Selected devices: All
  devices with a site label key but where the label value is not
  factory-berlin.

- Example label selector: site in (factory-berlin,factory-madrid) -
  Selected devices: All devices with a site label key and where the
  label value is either factory-berlin or factory-madrid.

For more information, see Labels and Selectors.

### Using labels

**Technology Preview:** You can organize your devices by using labels.

#### Viewing devices and their labels using the CLI

View devices and their associated labels. You can use labels to organize
your devices and device fleets.

Complete the following steps:

1.  View devices in your inventory by using the `-o wide` option:

    ``` bash
    flightctl get devices -o wide
    ```

    See the following example output:

    ``` bash
    NAME            ALIAS    OWNER   SYSTEM  UPDATED     APPLICATIONS  LAST SEEN      LABELS
    <device1_name>  <none>   <none>  Online  Up-to-date  <none>        3 seconds ago  region=eu-west-1,site=factory-berlin
    <device2_name>  <none>   <none>  Online  Up-to-date  <none>        1 minute ago   region=eu-west-1,site=factory-madrid
    ```

2.  View devices in your inventory with a specific label or set of
    labels by using the `-l <key=value>` option:

    ``` bash
    flightctl get devices -l site=factory-berlin -o wide
    ```

    See the following example output:

    ``` bash
    NAME            ALIAS    OWNER   SYSTEM  UPDATED     APPLICATIONS  LAST SEEN      LABELS
    <device1_name>  <none>   <none>  Online  Up-to-date  <none>        3 seconds ago  region=eu-west-1,site=factory-berlin
    ```

#### Updating labels using the CLI

Update labels on your devices using the CLI. Complete the following
steps:

1.  Export the current definition of the device into a file by running
    the following command:

    ``` bash
    flightctl get device/<device1_name> -o yaml > my_device.yaml
    ```

2.  Use your preferred editor to edit the `my_device.yaml` file. See the
    following example:

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Device
    metadata:
      labels:
        some_key: some_value
        some_other_key: some_other_value
      name: <device1_name>
    spec:
    [...]
    ```

3.  Save the file and apply the updated device definition by running the
    following command:

    ``` bash
    flightctl apply -f my_device.yaml
    ```

4.  Verify that the changes are applied by running the following command

    ``` bash
    NAME            ALIAS    OWNER   SYSTEM  UPDATED     APPLICATIONS  LAST SEEN      LABELS
    <device1_name>  <none>   <none>  Online  Up-to-date  <none>        3 minutes ago  some_key=some_value,some_other_key=some_other_value
    <device2_name>  <none>   <none>  Online  Up-to-date  <none>        4 minutes ago  region=eu-west-1,site=factory-madrid
    ```

### Field selectors

Field selectors filter a list of Red Hat Edge Manager resources,
including individual devices, fleets and any other resources, based on
specific resource field values.

Field selectors follow the same syntax, principles, and operators as
Kubernetes field and label selectors with additional operators available
for more advanced search use cases.

#### Supported fields

The Red Hat Edge Manager resources give a set of metadata fields that
you can select.

Each resource supports the following metadata fields:

- `metadata.name`

- `metadata.owner`

- `metadata.creationTimestamp`

**Note:** To query labels, use label selectors for advanced and flexible
label filtering.

For more information, see Labels and label selectors.

#### List of additional supported fields

In addition to the metadata fields, each resource has its own unique set
of fields that you can select, offering further flexibility in filtering
and selection based on resource-specific attributes.

The following table lists the fields supported for filtering for each
resource kind:

- Kind - Fields

- Certificate Signing Request - status.certificate

- Device -
  status.summary.statusstatus.applicationsSummary.statusstatus.updated.statusstatus.lastSeenstatus.lifecycle.status

- Enrollment Request - status.approval.approvedstatus.certificate

- Fleet - spec.template.spec.os.image

- Repository - spec.typespec.url

- Resource Sync - spec.repository

#### Field discovery

Some Red Hat Edge Manager resources might expose additional supported
fields. You can discover the supported fields by using the `flightctl`
command with the `--field-selector` option. If you try to use an
unsupported field, the error message lists the available supported
fields.

See the following examples:

``` bash
flightctl get device --field-selector='text'
```

``` bash
Error: listing devices: 400, message: unknown or unsupported selector: unable to resolve selector name "text". Supported selectors are: [metadata.alias metadata.creationTimestamp metadata.name metadata.nameoralias metadata.owner status.applicationsSummary.status status.lastSeen status.summary.status status.updated.status]
```

The field `text` is not a valid field for filtering. The error message
provides a list of supported fields that you can use with
`--field-selector` for the `Device` resource.

You can then use one of the supported fields:

``` bash
flightctl get devices --field-selector 'metadata.alias contains cluster'
```

The `metadata.alias` field is checked with the containment operator
`contains` to see if it has the value `cluster`.

##### Examples

<div class="formalpara">

<div class="title">

Excluding a specific device by name

</div>

The following command filters out a specific device by its name:

</div>

``` bash
flightctl get devices --field-selector 'metadata.name!=<device_name>'
```

<div class="formalpara">

<div class="title">

Filter by owner, labels, and creation timestamp

</div>

The following command retrieves devices that are owned by
`Fleet/pos-fleet`, are located in the `us` region, and are created in
`2024`:

</div>

``` bash
flightctl get devices --field-selector 'metadata.owner=Fleet/pos-fleet, metadata.creationTimestamp >= 2024-01-01T00:00:00Z, metadata.creationTimestamp < 2025-01-01T00:00:00Z' -l 'region=us'
```

<div class="formalpara">

<div class="title">

Filter by owner, labels, and device status

</div>

The following command retrieves devices that are owned by
`Fleet/pos-fleet`, are located in the `us` region, and have a
`status.updated.status` of either `Unknown` or `OutOfDate`:

</div>

``` bash
flightctl get devices --field-selector 'metadata.owner=Fleet/pos-fleet, status.updated.status in (Unknown, OutOfDate)' -l 'region=us'
```

#### Supported operators

- Operator - Symbol - Description

- Exists - --field-selector \<field\> - Checks if a field exists. For
  example, the --field-selector 'metadata.owner' field selector returns
  resources that have the metadata.owner field.

- DoesNotExist - ! - Checks if a field does not exist.

- Equals - = - Checks if a field is equal to a value.

- DoubleEquals - == - Another form of equality check.

- NotEquals - != - Checks if a field is not equal to a value.

- GreaterThan - \> - Checks if a field is greater than a value.

- GreaterThanOrEquals - \>= - Checks if a field is greater than or equal
  to a value.

- LessThan - \< - Checks if a field is less than a value.

- LessThanOrEquals - ⇐ - Checks if a field is less than or equal to a
  value.

- In - in - Checks if a field is within a list of values.

- NotIn - notin - Checks if a field is not in a list of values.

- Contains - contains - Checks if a field has a value.

- NotContains - notcontains - Checks if a field does not contain a
  value.

#### Operators usage by field type

Each field type supports a specific subset of operators:

- Field Type - Supported Operators - Value

- String - Equals: Matches if the field value is an exact match to the
  specified string.DoubleEquals: Matches if the field value is an exact
  match to the specified string. Alternative to Equals.NotEquals:
  Matches if the field value is not an exact match to the specified
  string.In: Matches if the field value matches at least one string in
  the list.NotIn: Matches if the field value does not match any of the
  strings in the list.Contains: Matches if the field value has the
  specified substring.NotContains: Matches if the field value does not
  contain the specified substring.Exists: Matches if the field is
  present.DoesNotExist: Matches if the field is not present. - Text
  string

- Timestamp - Equals: Matches if the field value is an exact match to
  the specified timestamp.DoubleEquals: Matches if the field value is an
  exact match to the specified timestamp. Alternative to
  Equals.NotEquals: Matches if the field value is not an exact match to
  the specified timestamp.GreaterThan: Matches if the field value is
  after the specified timestamp.GreaterThanOrEquals: Matches if the
  field value is after or equal to the specified timestamp.LessThan:
  Matches if the field value is before the specified
  timestamp.LessThanOrEquals: Matches if the field value is before or
  equal to the specified timestamp.In: Matches if the field value
  matches at least one timestamp in the list.NotIn: Matches if the field
  value does not match any of the timestamps in the list.Exists: Matches
  if the field is present.DoesNotExist: Matches if the field is not
  present. - RFC 3339 format

- Number - Equals: Matches if the field value equals the specified
  number.DoubleEquals: Matches if the field value equals the specified
  number. Alternative to Equals.NotEquals: Matches if the field value
  does not equal to the specified number.GreaterThan: Matches if the
  field value is greater than the specified number.GreaterThanOrEquals:
  Matches if the field value is greater than or equal to the specified
  number.LessThan: Matches if the field value is less than the specified
  number.LessThanOrEquals: Matches if the field value is less than or
  equal to the specified number.In: Matches if the field value equals at
  least one number in the list.NotIn: Matches if the field value does
  not equal any numbers in the list.Exists: Matches if the field is
  present.DoesNotExist: Matches if the field is not present. - Number
  format

- Boolean - Equals: Matches if the value is true or false.DoubleEquals:
  Matches if the value is true or false. Alternative to
  Equals.NotEquals: Matches if the value is the opposite of the
  specified value.In: Matches if the value, true or false, is in the
  list. The list can only contain true or false, so this operator is
  limited in use.NotIn: Matches if the value is not in the list.Exists:
  Matches if the field is present.DoesNotExist: Matches if the field is
  not present. - Boolean format (true, false)

- Array - Contains: Matches if the array has the specified
  value.NotContains: Matches if the array does not contain the specified
  value.In: Matches if the array overlaps with the specified
  values.NotIn: Matches if the array does not overlap with the specified
  values. Exists: Matches if the field is present.DoesNotExist: Matches
  if the field is not present. - Array element

### Updating the operating system

**Technology Preview:** You can update the operating system of a device
by updating the target operating system image name or version in the
device specification.

When the Red Hat Edge Manager agent communicates with the service, the
agent detects the requested update. Then, the agent automatically starts
downloading and verifying the new operating system version in the
background.

The Red Hat Edge Manager agent schedules the actual system update
according to the update policy. At the scheduled update time, the agent
installs the new version without disrupting the currently running
operating system.

Finally, the device reboots into the new version.

The Red Hat Edge Manager currently supports the following image type and
image reference format:

- Image Type - Image Reference

- bootc - An OCI image reference to a container registry. Example:
  quay.io/flightctl-example/rhel:9.5

During the process, the agent sends status updates to the service. You
can monitor the update process by viewing the device status. For more
information, see Viewing devices.

#### Updating the operating system on the CLI

Update a device using the CLI. Complete the following steps:

1.  Get the current resource manifest of the device by running the
    following command:

    ``` bash
    flightctl get device/<device_name> -o yaml > my_device.yaml
    ```

2.  Edit the `Device` resource to specify the new operating system name
    and version target.

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Device
    metadata:
      name: <device_name>
    spec:
    [...]
      os:
        image: quay.io/flightctl/rhel:9.5
    [...]
    ```

3.  Apply the updated `Device` resource by running the following
    command:

    ``` bash
    flightctl apply -f <device_name>.yaml
    ```

### Operating system configuration for edge devices

**Technology Preview:** You can include an operating system-level host
configuration in the image to provide maximum consistency and
repeatability.

To update the configuration, you create a new operating system image and
update devices with the new image.

However, updating devices with a new image can be impractical in the
following cases:

- The configuration is missing in the image.

- The configuration needs to be specific to a device.

- The configuration needs to be updateable at runtime without updating
  the operating system image and rebooting.

For these cases, you can declare a set of configuration files that is
present on the file system of the device. The Red Hat Edge Manager agent
applies updates to the configuration files while ensuring that either
all files are successfully updated in the file system, or rolled back to
their pre-update state. If the user updates both an operating system and
configuration set of a device at the same time, the Red Hat Edge Manager
agent updates the operating system first, then applies the specified set
of configuration files.

You can also specify a list of configuration sets that the Red Hat Edge
Manager agent applies in sequence. In case of a conflict, the last
applied configuration set is valid.

**Important:** After the Red Hat Edge Manager agent updates the
configuration on the disk, the running applications need to reload the
new configuration into memory for the configuration to become effective.
If the update involves a reboot, `systemd` automatically restarts the
applications with the new configuration and in the correct order. If the
update does not involve a reboot, many application can detect changes to
their configuration files and automatically reload the files. When an
application does not support change detection, you can use device
lifecycle hooks to run scripts or commands if certain conditions are
met.

#### Configuration providers

You can provide configuration from multiple sources, called
configuration providers, in Red Hat Edge Manager. The Red Hat Edge
Manager currently supports the following configuration providers:

Git Config Provider  
Fetches device configuration files from a Git repository.

Kubernetes Secret Provider  
Fetches a secret from a Kubernetes cluster and writes the content to the
file system of the device.

HTTP Config Provider  
Fetches device configuration files from an HTTP(S) endpoint.

Inline Config Provider  
Allows specifying device configuration files inline in the device
manifest without querying external systems.

##### Configuration from a Git repository

You can store device configuration in a Git repository such as GitHub or
GitLab. You can then add a Git Config Provider so that the Red Hat Edge
Manager synchronizes the configuration from the repository to the file
system of the device.

The Git Config Provider takes the following parameters:

- Parameter - Description

- Repository - The name of a Repository resource defined in the Red Hat
  Edge Manager.

- TargetRevision - The branch, tag, or commit of the repository to
  checkout.

- Path - The absolute path to the directory in the repository from which
  files and subdirectories are synchronized to the file system of the
  device. The Path directory corresponds to the root directory (/) on
  the device, unless the MountPath parameter is specified.

- MountPath - Optional. The absolute path to the directory in the file
  system of the device to write the content of the repository to. By
  default, the value is the file system root (/).

The `Repository` resource defines the Git repository, the protocol and
access credentials that the Red Hat Edge Manager must use. The
repository needs to be set up only once. After setting up, the
repository can be used to configure individual devices or device fleets.

##### Secrets from a Kubernetes cluster

The Red Hat Edge Manager can query only the Kubernetes cluster that the
Red Hat Edge Manager is running on for a Kubernetes secret. The content
of that secret can be written to a path on the device file system.

The Kubernetes Secret Provider takes the following parameters:

- Parameter - Description

- Name - The name of the secret.

- NameSpace - The namespace of the secret.

- MountPath - The directory in the file system of the device to write
  the secret contents to.

**Note:** The Red Hat Edge Manager needs permission to access secrets in
the defined namespace. For example, creating a `ClusterRole` and
`ClusterRoleBinding` allows the `flightctl-worker` service account to
get and list secrets in that namespace.

##### Configuration from an HTTP server

The Red Hat Edge Manager can query an HTTP server for configuration. The
HTTP server can serve static or dynamically generated configuration for
a device.

The HTTP Config Provider takes the following parameters:

- Parameter - Description

- Repository - The name of a Repository resource defined in the Red Hat
  Edge Manager.

- Suffix - The suffix to append to the base URL defined in the
  Repository resource. The suffix can include path and query parameters,
  for example /path/to/endpoint?query=param.

- FilePath - The absolute path to the file in the file system of the
  device to write the response of the HTTP server to.

The `Repository` resource specifies the HTTP server for the Red Hat Edge
Manager to connect to, and the protocol and access credentials to use.
The repository needs to be set up once and then, the repository can be
used to configure multiple devices or device fleets.

##### Configuration inline in the device specification

You can specify configuration inline in a device specification. When
using the inline device specification, the Red Hat Edge Manager does not
need to connect to external systems to fetch the configuration.

The Inline Config Provider takes a list of file specifications, where
each file specification takes the following parameters:

- Parameter - Description

- Path - The absolute path to the file in the file system of the device
  to write the content to. If a file already exists in the specified
  path, the file is overwritten.

- Content - The UTF-8 or base64-encoded content of the file.

- ContentEncoding - Defines how the contents are encoded. Must be either
  plain or base64. Default value is set to plain.

- Mode - Optional. The permission mode of the file. You can specify the
  octal with a leading zero, for example 0644, or as a decimal without a
  leading zero, for example 420. The setuid, setgid, and sticky bits are
  supported. If not specified, the permission mode for files defaults to
  0644.

- User - Optional. The owner of the file. Specified either as a name or
  numeric ID. Default value is set to root.

- Group - Optional. The group of the file. Specified either as a name or
  numeric ID.

### Configuring fleets to auto-register MicroShift clusters

**Technology Preview:** If you have fleets of devices that are running
an operating system image that includes MicroShift, you can configure
your fleets to auto-register MicroShift clusters with Red Hat Advanced
Cluster Management.

#### Configuring your device template

To enable auto-registration in a fleet, add configuration to the device
template. Complete the following steps:

1.  Add the `acm-crd` resource configuration, which includes the
    `filePath` for your `crd.yaml` file, your `repository`, and `suffix`
    to your `Fleet` resource. See the following example:

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Fleet
    metadata:
     name: fleet-acm
    spec:
     selector:
      matchLabels:
       fleet: acm
     template:
      spec:
       os:
        image: <your os image>
    config:
       - name: acm-crd
        httpRef:
         filePath: /var/local/acm-import/crd.yaml
         repository: acm-registration
         suffix: /agent-registration/crds/v1
    ```

2.  Add the `acm-import` resource configuration with the `filePath`,
    `repository`, and `suffix`, as you see in the following example:

    ``` yaml
    - name: acm-import
        httpRef:
         filePath: /var/local/acm-import/import.yaml
         repository: acm-registration
         suffix: /agent-registration/manifests/{{.metadata.name}}
    ```

3.  **Optional:** If your MicroShift cluster did not pull the Red Hat
    Advanced Cluster Management images, add the `pull-secret` resource,
    as you see in the following addition to the template:

    ``` yaml
    - name: pull-secret
        inline:
        - path: "/etc/crio/openshift-pull-secret"
         content: "{\"auths\":{...}}"
    ```

4.  Add the `apply-acm-manifests` resource with the following
    conditional `if` requirements to run `kubectl apply -f` on your
    `crd.yaml` file, and your `import.yaml` file:

    ``` yaml
    - name: apply-acm-manifests
        inline:
        - path: "/etc/flightctl/hooks.d/afterupdating/50-acm-registration.yaml"
         content: |
          - if:
           - path: /var/local/acm-import/crd.yaml
            op: [created]
           run: kubectl apply -f /var/local/acm-import/crd.yaml
           envVars:
            KUBECONFIG: /var/lib/microshift/resources/kubeadmin/kubeconfig
          - if:
           - path: /var/local/acm-import/import.yaml
            op: [created]
           run: kubectl apply -f /var/local/acm-import/import.yaml
           envVars:
            KUBECONFIG: /var/lib/microshift/resources/kubeadmin/kubeconfig
    ```

5.  In the console, label the device `fleet:acm` and click **Approve**,
    which automatically selects the `fleet-acm` fleet. See Managing
    device fleets for information about managing devices with labels.

### Managing the device configuration from a Git repository on the CLI

**Technology Preview:** Create and apply a device configuration in a Git
repository.

Complete the following steps:

1.  Create a file, for example `site-settings-repo.yaml`, that contains
    the following definition for a `Repository` resource, named
    `site-settings`:

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Repository
    metadata:
      name: site-settings
    spec:
      type: git
      url: https://github.com/<your_org>/<your_repo>.git
    ```

2.  Create the `Repository` resource by running the following command:

    ``` bash
    flightctl apply -f site-settings-repo.yaml
    ```

3.  Verify that the resource has been correctly created and is
    accessible by Red Hat Edge Manager by running the following command:

    ``` bash
    flightctl get repository/site-settings
    ```

    See the following example output:

    ``` bash
    NAME           TYPE  REPOSITORY URL                                 ACCESSIBLE
    site-settings  git   https://github.com/<your_org>/<your_repo>.git  True
    ```

4.  Apply the `example-site` configuration to a device by update the
    device specification:

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Device
    metadata:
      name: <device_name>
    spec:
    [...]
      config: 
      - name: example-site
        configType: GitConfigProviderSpec
        gitRef:
          repository: site-settings
          targetRevision: production
          path: /etc/example-site 
    [...]
    ```

    - The example configuration takes all the files from the
      `example-site` directory from the `production` branch of the
      `site-settings` repository and places the files in the root
      directory (`/`).

    - Ensure that the target path is writeable by creating your
      directory structure. The root directory (`/`) is not writeable in
      `bootc` systems.

### Device lifecycle hooks

**Technology Preview:** The Red Hat Edge Manager agent can run
user-defined commands at specific points in the device lifecycle by
using device lifecycle hooks. For example, you can add a shell script to
your operating system images that backs up your application data. You
can then specify that the script must run and complete successfully
before the agent can start updating the operating system.

As another example, certain applications or system services do not
automatically reload their configuration file when the file changes on
the disk. You can manually reload the configuration file by specifying a
command as another hook, which is called after the agent completes the
update process.

The following device lifecycle hooks are supported:

- Lifecycle hook - Description

- beforeUpdating - The hook is called after the agent completes
  preparing for the update, but before changing the operating system. If
  an action in this hook returns with a failure, the agent cancels the
  update.

- afterUpdating - The hook is called after the agent writes the update
  to disk. If an action in this hook returns with a failure, the agent
  cancels and rolls back the update.

- beforeRebooting - The hook is called before the system reboots. The
  agent blocks the reboot until the action completes or times out. If
  any action in this hook returns with a failure, the agent cancels and
  rolls back the update.

- afterRebooting - The hook is called when the agent first starts after
  a reboot. If any action in this hook returns with a failure, the agent
  reports the failure but continues starting up.

#### Rule files

You can define device lifecycle hooks by adding rule files to one of the
following locations in the device file system:

- Rules in the `/usr/lib/flightctl/hooks.d/<lifecycle_hook_name>/`
  drop-in directory are read-only. To add rules to the `/usr` directory,
  you must add them to the operating system image during image building.

- Rules in the `/etc/flightctl/hooks.d/<lifecycle_hook_name>/` drop-in
  directory are read-writable. You can update the rules at runtime by
  using several methods.

When creating and placing the files, you must consider the following
practices:

- The name of the rule must be all lower case.

- If you define rules in both locations, the rules are merged.

- If you add more than one rule files to a lifecycle hook directory, the
  files are processed in lexical order of the file names.

- If you define files with identical file names in both locations, the
  file in the `/etc` folder takes precedence over the file of the same
  name in the `/usr` folder.

A rule file is written in YAML format and contains a list of one or more
actions. An action can be an instruction to run an external command.

When you specify many actions for a hook, the actions are performed in
sequence, finishing one action before starting the next.

If an action returns with a failure, the following actions are skipped.

A `run` action takes the following parameters:

- Parameter - Description

- Run - The absolute path to the command to run, followed by any flags
  or arguments, for example /usr/bin/nmcli connection reload. The
  command is not executed in a shell, so you cannot use shell variables,
  such as \$PATH or \$HOME, or chain commands, such as \| or ;. If
  necessary, you can start a shell by specifying the shell as command to
  run, for example /usr/bin/bash -c 'echo \$SHELL \$HOME \$USER'.

- EnvVars - Optional. A list of key-value pairs to set as environment
  variables for the command.

- WorkDir - Optional. The directory the command is run from.

- Timeout - Optional. The maximum duration that is allowed for the
  action to complete. Specify the duration as a single positive integer
  followed by a time unit. The s, m, and h units are supported for
  seconds, minutes, and hours, respectively.

- If - Optional. A list of conditions that must be true for the action
  to be run. If not provided, actions run unconditionally.

By default, actions are performed every time the hook is triggered.
However, for the `afterUpdating` hook, you can use the `If` parameter to
add conditions that must be true for an action to be performed.
Otherwise, the action is skipped.

For example, to run an action only if a given file or directory changes
during the update, you can define a path condition that takes the
following parameters:

- Parameter - Description

- Path - An absolute path to a file or directory that must change during
  the update as condition for the action to be performed. Specify paths
  by using forward slashes (/). If the path is to a directory, it must
  end with a forward slash (/). If you specify a path to a file, the
  file must have changed to satisfy the condition. If you specify a path
  to a directory, a file in that directory or any of its subdirectories
  must have changed to satisfy the condition.

- Op - A list of file operations, such as created, updated, and removed,
  to limit the type of changes to the specified path as condition for
  the action to be performed.

If you specify a path condition for an action in the `afterUpdating`
hook, you have the following variables that you can include in arguments
to your command and are replaced with the absolute paths to the changed
files:

- Variable - Description

- \${ Path } - The absolute path to the file or directory specified in
  the path condition.

- \${ Files } - A space-separated list of absolute paths of the files
  that changed during the update and are covered by the path condition.

- \${ CreatedFiles } - A space-separated list of absolute paths of the
  files that were created during the update and are covered by the path
  condition.

- \${ UpdatedFiles } - A space-separated list of absolute paths of the
  files that were updated during the update and are covered by the path
  condition.

- \${ RemovedFiles } - A space-separated list of absolute paths of the
  files that were removed during the update and are covered by the path
  condition.

The Red Hat Edge Manager agent includes a built-in set of rules defined
in `/usr/lib/flightctl/hooks.d/afterupdating/00-default.yaml`. The
following commands are executed if certain files are changed:

- File - Command - Description

- /etc/systemd/system/ - systemctl daemon-reload - Changes to systemd
  units are activated by signaling the systemd daemon to reload the
  systemd manager configuration. This reruns all generators, reloads all
  unit files, and re-creates the entire dependency tree.

- /etc/NetworkManager/system-connections/ - nmcli conn reload - Changes
  to NetworkManager system connections are activated by signaling the
  NetworkManager daemon to reload all connections. For more information,
  see the Additional resources section.

- /etc/firewalld/ - firewall-cmd --reload - Changes to the permanent
  configuration of firewalld are activated by signaling firewalld to
  reload firewall rules as new runtime configuration.

### Monitoring device resources

**Technology Preview:** You can set up resource monitors for device
resources and create alerts when the utilization of resources crosses a
defined threshold. When the agent alerts the Red Hat Edge Manager
service, the service sets the device status to `degraded` or `error`,
depending on the severity level.

Resource monitors take the following parameters:

- Parameter - Description

- MonitorType - The resource to monitor. The CPU, Memory, and Disk
  resources are currently supported.

- SamplingInterval - The interval in which the monitor samples usage,
  specified as a positive integer followed by a time unit: s for
  seconds, m for minutes, h for hours.

- AlertRules - A list of alert rules.

- Path - For Disk monitor only. The absolute path to the directory to
  monitor. Utilization reflects the file system that contains the path,
  even if the defined path is not a mount point.

Alert rules take the following parameters:

- Parameter - Description

- Severity - The severity of the alert rule can be Info, Warning, or
  Critical. Only one alert rule is allowed for each severity level and
  monitor.

- Duration - The duration that resource usage is measured and averaged
  over when sampling, specified as a positive integer followed by a time
  unit: s for seconds, m for minutes, h for hours. The duration must be
  smaller than the sampling interval.

- Percentage - The usage threshold that triggers the alert, as
  percentage value. The value ranges from 0 to 100 without the % sign.

- Description - A human-readable description of the alert. Add details
  about the alert to help with debugging. By default, the alert
  description is load is above \>% for more than.

#### Monitoring device resources using the CLI

Monitor the resources of your device through the CLI, providing you with
the tools and commands to track performance and troubleshoot issues.

Complete the following steps:

- Add resource monitors in the `spec.resources` section of the device
  specification. For example, add the following monitor for your disk:

  ``` yaml
  apiVersion: flightctl.io/v1alpha1
  kind: Device
  metadata:
    name: <device_name>
  spec:
  [...]
    resources:
    - monitorType: Disk
      samplingInterval: 5s 
      path: /application_data 
      alertRules:
      - severity: Warning 
        duration: 30m
        percentage: 75
        description: Disk space for application data is >75% full for over 30m.
      - severity: Critical 
        duration: 10m
        percentage: 90
        description: Disk space for application data is >90% full over 10m.
  [...]
  ```

  - Samples usage every 5 seconds.

  - Checks disk usage on the file system that is associated with the
    `/applications_data` path.

  - Initiates a warning if the average usage exceeds 75% for more than
    30 minutes.

  - Initiates a critical alert if the average usage exceeds 90% for over
    10 minutes.

## Managing applications on an edge device

**Technology Preview:** You can deploy, update, or remove applications
on a device by updating the list of applications in the device
specification. When the Red Hat Edge Manager agent checks in and detects
the change in the specification, the agent downloads any new or updated
application packages and images from an Open Container Initiative
(OCI)-compatible registry. Then, the agent deploys the packages to the
appropriate application runtime or removes them from that runtime.

The Red Hat Edge Manager supports the `podman-compose` tool as the
application runtime and format.

### Prerequisites

- You must install the Red Hat Edge Manager CLI.

- You must log in to the Red Hat Edge Manager service.

- Your device must run an operating system image with the
  `podman-compose` tool installed. See Building a bootc operating system
  image for use with the Red Hat Edge Manager

### Building an application package image

The Red Hat Edge Manager can download application packages from an Open
Container Initiative (OCI) compatible registry. You can build an OCI
container image that includes your application package in the
`podman-compose` format and push the image to your OCI registry.

Complete the following steps:

1.  Define the functionality of the application in a file called
    `podman-compose.yaml` that follows the Podman Compose specification.

    1.  Create a file called `Containerfile` with the following content:

    ``` bash
    FROM scratch 
    COPY podman-compose.yaml /podman-compose.yaml
    LABEL appType="compose" 
    ```

    - Embed the compose file in a `scratch` container.

    - Add the `appType=compose` label.

2.  Build and push he container image to your OCI registry.

    1.  Define the image repository that you have permissions to write
        to by running the following command:

        ``` bash
        OCI_IMAGE_REPO=quai.io/<your_org>/<your_image>
        ```

    2.  Define the image tag by running the following command:

        ``` bash
        OCI_IMAGE_TAG=v1
        ```

    3.  Build the application container image. Run the following
        command:

        ``` bash
        podman build -t ${OCI_IMAGE_REPO}:${OCI_IMAGE_TAG} .
        ```

    4.  Push the container image.

    ``` bash
    podman push ${OCI_IMAGE_REPO}:${OCI_IMAGE_TAG} .
    ```

### Deploying applications to a device using the CLI

Deploy an application package to a device from an OCI registry by using
the CLI.

Complete the following steps:

1.  Specify the application package that you want to deploy in the
    `spec.applications` field in the `Device` resource:

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Device
    metadata:
      name: <device_name>
    spec:
    [...]
      applications:
      - name: wordpress 
        image: quay.io/rhem-demos/wordpress-app:latest 
        envVars: 
          WORDPRESS_DB_HOST: <database_host>
          WORDPRESS_DB_USER: <user_name>
          WORDPRESS_DB_PASSWORD: <password>
    [...]
    ```

    - A user-defined name for the application that is used when the web
      console and the CLI list applications.

    - A reference to an application package in an OCI registry.

    - Optional. A list of key-value pairs that are passed to the
      deployment tool as environment variables or command line flags.

    **Note:** For each application in the `applications` section of the
    device specification, you can find the corresponding device status
    information.

2.  Verify the status of an application deployment on a device by
    inspecting the device status information. Run the following command:

    ``` bash
    flightctl get device/<your_device_id> -o yaml
    ```

    See the following example output:

    ``` yaml
    [...]
    spec:
      applications:
      - name: example-app
        image: quay.io/flightctl-demos/example-app:v1
    status:
      applications:
      - name: example-app
        ready: 3/3
        restarts: 0
        status: Running
      applicationsSummary:
        info: All application workloads are healthy.
        status: Healthy
    [...]
    ```

## Managing device fleets

**Technology Preview:** The Red Hat Edge Manager simplifies the
management of a large number of devices and workloads through *device
fleets*. A fleet is a resource that defines a group of devices governed
by a common device template and management policies.

When you make a change to the device template, all devices in the fleet
receive the changes when the Red Hat Edge Manager agent detects the new
target specification.

Device monitoring in a fleet is also simplified because you can check
the status summary of the whole fleet.

Fleet-level management offers the following advantages:

- Scales your operations because you perform operations only once for
  each fleet instead of once for each device.

- Minimizes the risk of configuration mistakes and configuration drift.

- Automatically applies the target configuration when you add devices to
  the fleet or replace devices in the fleet.

The fleet specification consists of the following features:

Label selector  
Determines which devices are part of the fleet.

Device template  
Defines the configuration that the Red Hat Edge Manager enforces on
devices in the fleet.

Policies  
Govern how devices are managed, for example, how changes to the device
template are rolled out to the devices.

You can have both individually managed and fleet-managed devices at the
same time. When a device is selected into a fleet, the Red Hat Edge
Manager creates the device specification for the new device based on the
device template. If you update the device template for a fleet or a new
device joins the fleet, the Red Hat Edge Manager enforces the new
specification in the fleet.

If a device is not selected into any fleets, the device is considered
user-managed or unmanaged. For user-managed devices, you must update the
device specification either manually or through an external automation.

**Important:** A device cannot be member of more than one fleet at the
same time.

For more information, see Labels and label selectors.

### Device selection into a fleet

By default, devices are not assigned to a fleet. Instead, each fleet
uses a selector that defines which labels a device must have to be added
to the fleet.

To understand how to use labels in a fleet, see the following example:

The following list shows point-of-sales terminal devices and their
labels:

- Device - Labels

- A - type: pos-terminal, region: east, stage: production

- B - type: pos-terminal, region: east, stage: development

- C - type: pos-terminal, region: west, stage: production

- D - type: pos-terminal, region: west, stage: development

If all point-of-sales terminals uses the same configuration and are
managed by the same operations team, you can define a single fleet
called `pos-terminals` with the `type=pos-terminal` label selector.
Then, the fleet contains devices A, B, C, and D.

However, you might want to create separate fleets for the different
organizations for development or production. You can define a fleet for
development with the `type=pos-terminal, stage=development` label
selector, which selects devices C and D. Then, you can define another
fleet for production with the `type=pos-terminal, stage=production`
label selector. By using the correct label selectors, you can manage
both fleets independently.

**Important:** You must define selectors in a way that two fleets do not
select the same device. For example, if one fleet selects `region=east`,
and another fleet selects `stage=production`, both fleets try to select
device A. If two fleets try to select the same device, the Red Hat Edge
Manager keeps the device in the currently assigned fleet, if any, and
sets the `OverlappingSelectors` condition on the affected fleets to
`true`.

### Device templates

A device template of a fleet contains a device specification that is
applied to all devices in the fleet when the template is updated.

For example, you can specify in the device template of a fleet that all
devices in the fleet must run the `quay.io/flightctl/rhel:9.5` operating
system image.

The Red Hat Edge Manager service then rolls out the target specification
to all devices in the fleet and the Red Hat Edge Manager agents update
each devices accordingly.

You can change other specification items in the device template and the
Red Hat Edge Manager apply the changes in the same way.

However, sometimes not all of the devices in the fleet need to have the
exact same specification. The Red Hat Edge Manager allows templates to
contain placeholders that are populated based on the device name or
label values.

The syntax of the placeholders matches that of Go templates. However,
you can only use simple text and actions.

The use of conditionals or loops in the placeholders is not supported.

You can reference anything from the metadata of a device, such as
`{{ .metadata.labels.key }}` or `{{ .metadata.name }}`.

You can also use the following functions in your placeholders:

- The `upper` function changes the value to uppercase. For example, the
  function is `{{ upper .metadata.name }}`.

- The `lower` function changes the value to lowercase. For example, the
  function is `{{ lower .metadata.labels.key }}`.

- The `replace` function replaces all occurrences of a substring with
  another string. For example, the function is
  `{{ replace "old" "new" .metadata.labels.key }}`.

- The `getOrDefault` function returns a default value if accessing a
  missing label. For example, he function is
  `{{ getOrDefault .metadata.labels "key" "default" }}`.

You can combine the functions in pipelines, for example, a combined
function is
`{{ getOrDefault .metadata.labels "key" "default" | upper | replace " " "-" }}`.

**Note:** Ensure using proper Go template syntax. For example,
`{{ .metadata.labels.target-revision }}` is not valid because of the
hyphen. Instead, you must refer to the field as
`{{ index .metadata.labels "target-revision" }}`.

You can use the placeholders in device templates in the following ways:

- You can label devices by deployment stage, for example, stage labels
  are `stage: testing` and `stage: production`. Then, you can use the
  label with the `stage` key as placeholder when referencing the
  operating system image to use, for example, use
  `quay.io/myorg/myimage:latest-{{ .metadata.labels.stage }}` or when
  referencing a configuration folder in a Git repository.

- You can label devices by deployment site, for example, deployment
  sites are `site: factory-berlin` and `site: factory-madrid`.

- Then, you can use the label with the `site` key as parameter when
  referencing the secret with network access credentials in Kubernetes.

The following fields in device templates support placeholders:

- Field - Placeholders supported in

- Operating System Image - repository name, image name, image tag

- Git Config Provider - target revision, path

- HTTP Config Provider - URL suffix, path

- Inline Config Provider - content, path

### Selecting devices into a fleet by using the CLI

**Technology Preview:** Define label selector to add devices into a
fleet.

Complete the following tasks:

1.  Run the following command to verify that the label selector returns
    the devices that you want to add to the fleet:

    ``` bash
    flightctl get devices -l type=pos-terminal -l stage=development
    ```

2.  If running the command returns the expected list of devices, you can
    define a fleet that selects the devices by using the following YAML
    file:

    ``` yaml
    apiVersion: flightctl.io/v1alpha1
    kind: Fleet
    metadata:
      name: my_fleet
    spec:
      selector:
        matchLabels:
          type: pos-terminal
          stage: development
    [...]
    ```

3.  Apply the change by running the following command:

    ``` bash
    flightctl apply -f my_fleet.yaml
    ```

4.  Check for any overlaps with the selector of other fleets by running
    the following command:

    ``` bash
    flightctl get fleets/my_fleet -o json | jq -r '.status.conditions[] | select(.type=="OverlappingSelectors").status'
    ```

    See the following example output:

    ``` bash
    False
    ```
