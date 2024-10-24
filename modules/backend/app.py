from flask import Flask, render_template, request, jsonify

import pymongo
from flask_pymongo import PyMongo

from prometheus_flask_exporter import PrometheusMetrics

from flask_opentracing import FlaskTracing
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

import json
import logging
import opentracing

def init_tracer(service):

    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
        },
        service_name=service,
        validate=True,
        metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()



app = Flask(__name__)
app.config["MONGO_DBNAME"] = "example-mongodb"
app.config["MONGO_URI"] = "mongodb://my-user:YWRtaW4%3D@example-mongodb-1.example-mongodb-svc.default.svc.cluster.local:27017"
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

mongo = PyMongo(app)

metrics = PrometheusMetrics(app)
metrics.info("app_info", "Backend Application", version="1.0.3")

tracer = init_tracer("backend")
flask_tracer = FlaskTracing(tracer, True, app)
flask_tracer_span = flask_tracer.get_span()

@app.route("/")
def homepage():
    with tracer.start_span("homepage-endpoint", child_of=flask_tracer_span) as span:
        response = {"message": "Hello World"}
        span.set_tag("message", response)

        return response

@app.route("/api")
def my_api():
    with tracer.start_span("api-endpoint", child_of=flask_tracer_span) as span:
        response = {"message": "API endpoint"}
        span.set_tag("message", response)

        return jsonify(response)

@app.route("/star", methods=["POST"])
def add_star():
    with tracer.start_span("star-endpoint", child_of=flask_tracer_span) as span:
        try:
            star = mongo.db.stars
            name = request.json["name"]
            distance = request.json["distance"]
            star_id = star.insert({"name": name, "distance": distance})
            new_star = star.find_one({"_id": star_id})
            output = {"name": new_star["name"], "distance": new_star["distance"]}

            response = jsonify({"result": output})
            span.set_tag("message", json.dumps(response))

            return response
        except:
            span.set_tag("response", "Can't retrieve from database.")
            raise

if __name__ == "__main__":
    app.run()
