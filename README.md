A sample Flask app

In order to publish it, you need the following:
1. Modify the values in deployment folders to your desired microservice
2. Just commit & push
   2.1 Side branch: Builds image and tagging it with branch release, after that deploys to dev environment
   2.2 Main branch: Builds image and tagging it with main release, after that deploys to qa and then to prod environment
   2.3 Wait for Slack notification of the build result
   2.4 If pipeline succeeded, you'll be able to launch the service from within the cluster by typing the URL:
       http://<microservice-name>.flask-sample-<dev/qa/prod>.svc:<microservice-port>
       E.G: http://stav-poc.flask-sample-qa.svc:3000
   2.4 If using ingress.enabled: true, you'll be able to launch it from the internet by typing the URL:
       https://<microservice-name>-<dev/qa/prod>.k8s.stavco9.com
       E.G: https://stav-poc-qa.k8s.stavco9.com
3. On the Elastic Cloud, you'll be able to see the microservice logs
4. On the Grafana: https://grafana.k8s.stavco9.com you'll be able to see the service metrics