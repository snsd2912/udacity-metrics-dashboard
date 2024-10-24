## Verify the monitoring installation

### Application

![pplication_resources](./answer-img/application_resources.PNG)

### Monitoring

![monitoring_resources](./answer-img/monitoring_resources.PNG)

### Observability

![observability_resources](./answer-img/observability_resources.PNG)


## Setup the Jaeger and Prometheus source

- Expose Grafana to the internet and then setup Prometheus as a data source.

![grafana_homepage](./answer-img/grafana_home.PNG)

## Create a Basic Dashboard

- Create a dashboard in Grafana that shows Prometheus as a source.

![grafana_prometheus](./answer-img/grafana_dashboard.PNG)

## Describe SLO/SLI

Based on an SLO of *monthly uptime* and *request response time*:

1. 99.99% uptime monthly.
2. Response time of 95% of requests is less than 200 ms.

The SLIs are:

1. Got 99.98% uptime in May.
2. Response time of 96% of the requests is less than 200 ms.

## Creating SLI metrics

| Order | SLIs | Meaning |
|:-----------|:------------:|------------:|
| 1 | Uptime in a period of time | Measure health of the services |
| 2 | Average request response time | Performance of the services |
| 3 | Used CPU and memory | How much resources is used by the services |
| 4 | Count of error responses in a period of time | Identify possible bugs |
| 5 | Average recover time when a service goes down | Identify when incidents start to materially harm the business |

## Create a Dashboard to measure our SLIs

- Create a dashboard to measure the uptime of the frontend and backend services. We will also want to measure 40x and 50x errors. 

- PromQL to create dashboard:
    - Measure 4xx and 5xx errors:
```
sum(flask_http_request_total{status=~"4.."}) by (service)
```
    - Measure uptime for each service:
```
(sum(up{job=~"backend-service|frontend-service"}) by (job)) / (count(up{job=~"backend-service|frontend-service"}) by(job))
```

![grafana_dashboard](./answer-img/grafana_dashboard_2.PNG)

## Tracing our Flask App

Create a Jaeger span to measure the processes on the backend.

- Dashboard:
![jaeger-2](./answer-img/jaeger-2.PNG)

- Process details:
![jaeger](./answer-img/jaeger.PNG)

## Jaeger in Dashboards

- Now that the trace is running, let's add the metric to our current Grafana dashboard.



## Report Error

- write a trouble ticket for the developers, to explain the errors that you are seeing (400, 500, latency) and to let them know the file that is causing the issue also include a screenshot of the tracer span to demonstrate how we can user a tracer to locate errors easily.

```
TROUBLE TICKET

Name: Sang Le

Date: 10/24/2024 00:55:09 AM

Subject: Many 5xx errors created by Backend Service

Affected Area: API Requests

Severity: High

Description: The error logs is shown with database connection failed.
```

## Creating SLIs and SLOs

- We want to create an SLO guaranteeing that our application has a 99.95% uptime per month. Name four SLIs that you would use to measure the success of this SLO.


| Order | SLOs | SLIs |
|:-----------|:------------:|------------:|
| 1 | 99.95% uptime per month | Uptime is 99.96% |
| 2 | 99.95% response time is under 200ms | Response time under 200ms is 99.95% |
| 3 | The percentage of successful HTTP requests (e.g., 2xx and 3xx status codes) over total requests >= 99.95% | Proportion is 99.97% |
| 4 | The percentage of failed HTTP requests (e.g., 4xx and 5xx status codes) over total requests <= 0.05%  | Proportion is 0.03% |

## Building KPIs for our plan

- Create a list of 2-3 KPIs to accurately measure these metrics as well as a description of why those KPIs were chosen.

| Order | KPIs | Descriptions |
|:-----------|:------------:|------------:|
| 1 | Uptime | Monitors whether your application components (pods/services) are up and running continuously without interruption |
| 2 | Latency | Ensures that the application responds to requests in a timely manner, contributing to user experience |
| 3 | Error Rate | Tracks the number of erroneous responses, helping to monitor the reliability of the application |

## Final Dashboard

- Create a Dashboard containing graphs that capture all the metrics of your KPIs and adequately representing your SLIs and SLOs.



