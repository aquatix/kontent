kontent CMS
===========

kontent, Python/Django based weblog/CMS software

## Requirements

kontent CMS needs the PostgreSQL database:

```
apt install postgresql
```

If you're new to PostgreSQL and are for example running Ubuntu, check this [PostgreSQL howto](https://help.ubuntu.com/community/PostgreSQL).

To run the pip install, first some debian/ubuntu packages are needed:

```
apt install libpq-dev libjpeg-dev python-dev
```

These are needed for the PostgreSQL library and Pillow (imaging). pg_config is in postgresql-devel (libpq-dev in Debian/Ubuntu)


## Acknowledgements

The default kontent install uses the excellent and minimalistic [Skeleton](http://getskeleton.com/) theme/framework.
