Configuration
=============

You can configure Django Audit Events by overriding the variables below in your ``settings.py``

.. glossary::
    ``AUDIT_EVENT_MODEL`` - default: ``django_audit_events.AuditEvent``
        The event model in use, in the form of ``"app.Model"``

    ``AUDIT_INCLUDE_QUERY_PARAMS`` - default: ``False``
        Configuration flag to store query params from requests in the audit context and eventually in audit events.

    ``AUDIT_INCLUDE_POST_DATA`` - default: ``False``
        Configuration flag to store post data from requests in the audit context and eventually in audit events.

    ``AUDIT_MASK_POST_FIELDS`` - default: ``("password",)``
        Post data may contain PII or any other sensitive information such as credit card numbers which you may want to avoid storing in your database. Define the names of the fields that contain sensitive information.
