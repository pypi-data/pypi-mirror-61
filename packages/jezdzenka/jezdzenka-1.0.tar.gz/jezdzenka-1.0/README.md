# jězdźenka
jězdźenka (Upper Sorbian word for *ticket*) is a handy wallet in your terminal, no strings attached. It can be used for tagging and keeping important things like tickets, discount cards etc.

```
usage: jezdzenka [-h] [-a] [-n file] [-o id [id ...]] [-m id] [-i id] [-r id [id ...]] [-t id [id ...]] [-y id [id ...]] [-e EXPORT] [-v] [id]

Handy wallet in your terminal, no strings attached.

positional arguments:
  id                    an identifier of the object to be viewed using the external viewer

optional arguments:
  -h, --help            show this help message and exit
  -a, --all             get all objects in the wallet
  -n file, --new file   add a new object
  -o id [id ...], --outdated id [id ...]
                        archive the object
  -m id, --modify id    modify the parameters
  -i id, --info id      show all information about the card/coupon/ticket
  -r id [id ...], --remove id [id ...]
                        remove the object
  -t id [id ...], --tag id [id ...]
                        get objects with specific tag(s)
  -y id [id ...], --year id [id ...]
                        get objects from specific year
  -e EXPORT, --export EXPORT
                        export the data instead of showing it
  -v, --verbose         get a little bit more information sometimes
```
