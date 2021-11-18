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
When running this as a docker container, the path to configuration files should be mounted to `/config`. This container 
expects `mq_config.json` to contain service `neon_email_proxy` and `ngi_auth_vars.yml` to contain dict `emails`.

For example, if your configuration resides in `~/.config`:
```shell
export CONFIG_PATH="/home/${USER}/.config"
docker run -v ${CONFIG_PATH}:/config neon_email_proxy
```
