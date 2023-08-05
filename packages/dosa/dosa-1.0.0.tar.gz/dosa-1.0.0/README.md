Python wrapper for Digital Ocean [API V2](https://developers.digitalocean.com).

[![Latest Version](https://badge.fury.io/py/dosa.svg)](http://badge.fury.io/py/dosa)

[![Number of PyPI downloads](https://pypip.in/d/dosa/badge.png)](https://crate.io/packages/dosa/)

[![Travis Build](https://img.shields.io/travis/shon/dosa.svg)](https://travis-ci.org/shon/dosa)


Installation
============

``` {.sourceCode .bash}
pip install dosa
```

Usage
=====

``` {.sourceCode .python}
import dosa

API_KEY = 'Your API Key'
dosa.set_debug()  # enables debug logs

client = dosa.Client(api_key=API_KEY)

# Droplets
client.droplets.list()
status, result = client.droplets.create(name='terminator', region='nyc2',\
    size='512mb', image='ubuntu-14-04-x32', ssh_keys=[12345])
new_droplet_id = result['id']

# Droplet
new_droplet = client.Droplet(new_droplet_id)
print(new_droplet.info())
## shortcuts
new_droplet.status()
new_droplet.ip_addresses()
client.droplets.delete(new_droplet_id)


# Get all available size configs
client.sizes.list()

# SSH Keys
pub_key = open('~/.ssh/id_rsa.pub').read()
client.keys.create(name='RSA key', public_key=pub_key)
client.keys.list()

# Images
client.images.list()
client.images.all()
client.images.search('ubuntu', 'sgp1', show_op=True)

# Domains
client.domains.list()
client.domains.all()
client.domains.create(name='example.com', ip_address='1.2.3.4')
client.domains.delete(id='example.com')

### Get specific domain
domain = client.Domain(domain='example.com')
domain.info()

# Domain Records
dr = client.DomainRecords(domain='example.com')
dr.list()
dr.create(type='A', name='example.com', data='162.10.66.0')

### Get specific domain record for a domain
record = dr.Record(record_id='7976006')
record.info()
record.update(name='new.example.com')

# Firewalls
## Create a firewall
params = {
 'inbound_rules': [{'ports': '22',
   'protocol': 'tcp',
   'sources': {'addresses': ['0.0.0.0/0', '::/0']}},
  {'ports': '80',
   'protocol': 'tcp',
   'sources': {'addresses': ['0.0.0.0/0', '::/0']}}],
 'name': 'firewall',
 'outbound_rules': [{'destinations': {'addresses': ['0.0.0.0/0', '::/0']},
   'ports': 'all',
   'protocol': 'tcp'}],
 'tags': []}
firewall = client.firewalls.create(**params)

# search firewall by name
firewall = client.firewalls.get_by_name('firewall')

## add a droplet to a firewall
firewall.add_droplet(new_droplet_id)

## remove a droplet from a firewall
firewall.remove_droplet(new_droplet_id)

## delete a firewall
client.firewalls.delete(id=firewall.id)

# Extras
# $ ls keys/
# rsa_pub1.id  rsa_pub2.key  rsa_pub3.key
keys_dir = 'keys'
client.sync_ssh_keys(keys_dir)
```

Notes
=====

Image search:

    >>> client.images.search('ubuntu', region='sgp1', show_op=True)

Above code snippets searches for images containing ubuntu in description
or slug. Since region is specified (sgp1), only images in sgp1 region
would be considered. If no region is specified all regions are included.

Tests:

    >>> tox

To run tests, run `tox` in the root directory of the repo. It will create
virtual environments specified in `tox.ini`, install dependancies, and
run pytest.

Credits
=======

Created while working on [Scroll.in](http://scroll.in)'s project.

Dosa?
=====

[!["Paper Masala Dosa" by SteveR- -
<http://www.flickr.com/photos/git/3936135033/>. Licensed under Creative
Commons Attribution 2.0 via Wikimedia
Commons](http://upload.wikimedia.org/wikipedia/commons/thumb/3/34/Paper_Masala_Dosa.jpg/640px-Paper_Masala_Dosa.jpg)](http://commons.wikimedia.org/wiki/File:Paper_Masala_Dosa.jpg#mediaviewer/File:Paper_Masala_Dosa.jpg)
