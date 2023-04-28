# NeonAI Email Proxy
Proxies outgoing emails so a central account configuration can be used.

## Request Format
API requests should be in the form of a dictionary. The email subject and body should be passed as strings and an optional 
dict of attachments should map string attachment names to string base-64 encoded file contents.

>Example Request:
>```json
>{
>  "subject": "Email Subject",
>  "body": "string email contents\noptionally with newlines",
>  "attachments": {"att_name":  "<b64-encoded contents>"}
>}
>```

## Docker Configuration
When running this as a docker container, the `XDG_CONFIG_HOME` envvar is set to `/config`.
A configuration file at `/config/neon/diana.yaml` is required and should look like:
```yaml
MQ:
  port: <MQ Port>
  server: <MQ Hostname or IP>
  users:
    neon_email_proxy:
      password: <neon_email user's password>
      user: neon_email
keys:
  emails:
    host: <smtp hostname>
    mail: <email address>
    pass: <email password>
    port: <string smtp port>
```

For example, if your configuration resides in `~/.config`:
```shell
export CONFIG_PATH="/home/${USER}/.config"
docker run -v ${CONFIG_PATH}:/config neon_email_proxy
```
> Note: If connecting to a local MQ server, you may need to specify `--network host`
