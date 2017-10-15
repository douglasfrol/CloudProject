# Skapa stack och kalla på webhooks
## 1. Skapa stack
För att skapa stacken i terminalen från en VM (måste först köra `source SNIC\ 2017-13-45-openrc.sh`):
```
heat stack-create <StackName> -f CloudProject/Heat\ Autoscale/autoscale.yaml -e CloudProject/Heat\ Autoscale/environment.yaml
```

## 2. Nödvändig behörighet för att använda en webhook
För att kunna göra en HTTP request på webhooken (som ändrats från `alarm_url` till `signal_url` i den template som används) krävs rätt behörighet, vilket fås via en token genererad av OpenStack.

1. Om inte redan gjort, exportera rätt miljövariabler med `source SNIC\ 2017-13-45-openrc.sh`
2. Kör följande kommando som generarar en token:
```
curl -v -s -X POST $OS_AUTH_URL/auth/tokens?nocatalog   -H "Content-Type: application/json"   -d '{ "auth": { "identity": { "methods": ["password"],"password": {"user": {"domain": {"name": "'"$OS_USER_DOMAIN_NAME"'"},"name": "'"$OS_USERNAME"'", "password": "'"$OS_PASSWORD"'"} } }, "scope": { "project": { "domain": { "name": "'"$OS_PROJECT_DOMAIN_NAME"'" }, "name":  "'"$OS_PROJECT_NAME"'" } } }}' \
| python -m json.tool
```
3. Kopiera infon från `X-Subject-Token` variabeln i det returnerade resultatet.
4. Med den token som fås från steg 3 kan man nu kalla på en webhook-URL enligt :
```
curl -i -H "X-Auth-Token: <X-Subject-Token-Resultatet>" -X POST "webhook_url"
```

