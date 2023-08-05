=====
Usage
=====

Verify Slack signature::

    from slack_utils.signature import verify


    verify(
        request_headers['X-Slack-Signature'],
        request_headers['X-Slack-Request-Timestamp'],
        request_body,
        slack_signing_secret
    )

If signature is valid ``verify`` method will return True. Otherwise ``SlackException`` will be thrown.

Apart from signature ``verify`` method will validate request timestamp. Requests older than 60 seconds will trigger error.
