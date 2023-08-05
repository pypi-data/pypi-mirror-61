# certbot-bigip-plugin

# Requirements
see certbot rquirements: https://certbot.eff.org/docs/install.html#system-requirements

* F5
    * LE Chain needs to be at /Common/chain_Letsencrypt and in every other folder that uses this plugin. ( f.e.: /Internal/chain_Letsencrypt)
      At the moment, the plugin checks if a corresponding certificate/chain is located in the same partition/folder as the profile that uses it
      This is eligible to change in future versions
    * clientssl profile needs to be attached to the virtual server (DOMAIN_clientssl)
      At the moment, the plugin only updates the client profile but does not attach it to the virtual server

# Install

# Usage

# Contribute
If you find errors please add a ticket
If you fix errors please create a new branch and then a merge request 
- to the master branch if it is a bugfix
- to the development branch if it is a feature
- docker run --volume $PWD:/src -it registry.ong.at:5555/infra/certbot-plugins/environments/certbot_docker_image:master sh
- /src/python setup.py develop

use the docker image for local development