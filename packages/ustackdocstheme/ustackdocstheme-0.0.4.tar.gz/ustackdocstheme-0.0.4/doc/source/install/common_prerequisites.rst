Prerequisites
-------------

Before you install and configure the replace with the service it implements service,
you must create a database, service credentials, and API endpoints.

#. To create the database, complete these steps:

   * Use the database access client to connect to the database
     server as the ``root`` user:

     .. code-block:: console

        $ mysql -u root -p

   * Create the ``ustackdocstheme`` database:

     .. code-block:: none

        CREATE DATABASE ustackdocstheme;

   * Grant proper access to the ``ustackdocstheme`` database:

     .. code-block:: none

        GRANT ALL PRIVILEGES ON ustackdocstheme.* TO 'ustackdocstheme'@'localhost' \
          IDENTIFIED BY 'USTACKDOCSTHEME_DBPASS';
        GRANT ALL PRIVILEGES ON ustackdocstheme.* TO 'ustackdocstheme'@'%' \
          IDENTIFIED BY 'USTACKDOCSTHEME_DBPASS';

     Replace ``USTACKDOCSTHEME_DBPASS`` with a suitable password.

   * Exit the database access client.

     .. code-block:: none

        exit;

#. Source the ``admin`` credentials to gain access to
   admin-only CLI commands:

   .. code-block:: console

      $ . admin-openrc

#. To create the service credentials, complete these steps:

   * Create the ``ustackdocstheme`` user:

     .. code-block:: console

        $ openstack user create --domain default --password-prompt ustackdocstheme

   * Add the ``admin`` role to the ``ustackdocstheme`` user:

     .. code-block:: console

        $ openstack role add --project service --user ustackdocstheme admin

   * Create the ustackdocstheme service entities:

     .. code-block:: console

        $ openstack service create --name ustackdocstheme --description "replace with the service it implements" replace with the service it implements

#. Create the replace with the service it implements service API endpoints:

   .. code-block:: console

      $ openstack endpoint create --region RegionOne \
        replace with the service it implements public http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements internal http://controller:XXXX/vY/%\(tenant_id\)s
      $ openstack endpoint create --region RegionOne \
        replace with the service it implements admin http://controller:XXXX/vY/%\(tenant_id\)s
