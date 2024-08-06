#!/bin/bash

# Function to check if required utilities are installed
check_required_utils() {
    for util in wget tar; do
        if ! command -v $util &> /dev/null; then
            echo "$util could not be found, please install $util."
            exit 1
        fi
    done
}

# Main function to install CNI plugins
install_cni_plugins() {
    CNI_DOWNLOAD_ADDR=${CNI_DOWNLOAD_ADDR:-"https://github.com/containernetworking/plugins/releases/download/v1.1.1/cni-plugins-linux-amd64-v1.1.1.tgz"}
    CNI_PKG=${CNI_DOWNLOAD_ADDR##*/}
    CNI_CONF_OVERWRITE=${CNI_CONF_OVERWRITE:-"true"}

    echo -e "The installation of the CNI plugin will overwrite the CNI config file. Use export CNI_CONF_OVERWRITE=false to disable it."

    # Check if the loopback plugin exists
    if [ ! -f "/opt/cni/bin/loopback" ]; then
        echo -e "Start installing CNI plugins..."
        sudo mkdir -p /opt/cni/bin
        wget ${CNI_DOWNLOAD_ADDR}
        if [ ! -f ${CNI_PKG} ]; then
            echo -e "CNI plugins package does not exist"
            exit 1
        fi
        sudo tar -C /opt/cni/bin -xzvf ${CNI_PKG}
        sudo rm -rf ${CNI_PKG}
        if [ ! -f "/opt/cni/bin/loopback" ]; then
            echo -e "The ${CNI_PKG} package does not contain a loopback file."
            exit 1
        fi

        # Manage CNI configuration file
        CNI_CONFIG_FILE="/etc/cni/net.d/10-containerd-net.conflist"
        if [ -f ${CNI_CONFIG_FILE} ]; then
            if [ "${CNI_CONF_OVERWRITE}" == "false" ]; then
                echo -e "CNI netconf file already exists and will not be overwritten"
                return
            fi
            echo -e "Configuring CNI, ${CNI_CONFIG_FILE} already exists, will be backup as ${CNI_CONFIG_FILE}-bak ..."
            sudo mv ${CNI_CONFIG_FILE} ${CNI_CONFIG_FILE}-bak
        fi
        sudo mkdir -p "/etc/cni/net.d/"
        sudo sh -c "cat > ${CNI_CONFIG_FILE} <<EOF
{
  \"cniVersion\": \"1.0.0\",
  \"name\": \"containerd-net\",
  \"plugins\": [
    {
      \"type\": \"bridge\",
      \"bridge\": \"cni0\",
      \"isGateway\": true,
      \"ipMasq\": true,
      \"promiscMode\": true,
      \"ipam\": {
        \"type\": \"host-local\",
        \"ranges\": [
          [{\"subnet\": \"10.88.0.0/16\"}],
          [{\"subnet\": \"2001:db8:4860::/64\"}]
        ],
        \"routes\": [
          {\"dst\": \"0.0.0.0/0\"},
          {\"dst\": \"::/0\"}
        ]
      }
    },
    {
      \"type\": \"portmap\",
      \"capabilities\": {\"portMappings\": true}
    }
  ]
}
EOF"
    else
        echo "CNI plugins already installed and no need to install."
    fi
}

# Check for required utilities before proceeding
check_required_utils

# Run the main installation function
install_cni_plugins
