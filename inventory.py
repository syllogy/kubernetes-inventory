#!/usr/bin/env python3

import os
from kubernetes import client, config, dynamic
from kubernetes.dynamic.exceptions import ResourceNotFoundError
import json
from invoke import run
import yaml
import datetime
import re

now =  datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

try:
    config.load_incluster_config()
except config.ConfigException:
    try:
        config.load_kube_config()
    except config.ConfigException:
        raise Exception("Could not configure kubernetes python client")

api_core_v1 = client.CoreV1Api()
api_apps_v1 = client.AppsV1Api()
api_batchs_v1_beta_1 = client.BatchV1beta1Api()
api_networking_v1_beta_1 = client.NetworkingV1beta1Api()
api_version = client.VersionApi()
api_custom_object = client.CustomObjectsApi()

def get_cluster_version():
    return api_version.get_code().to_dict()

def get_helm(namespace):
    ret = []
    infos = run(f"helm list -n {namespace} -o yaml", warn=True, hide=True)
    if infos.ok:
        releases = yaml.safe_load(infos.stdout)
        for release in releases:
            data = {k:v for k,v in release.items()
                    if k in ['app_version', 'chart', 'name', 'revision', 'status']}
            ret.append(data)
    return ret


def get_deployments(namespace):
    data = api_apps_v1.list_namespaced_deployment(namespace=namespace)
    return data.to_dict()

def get_daemonsets(namespace):
    data = api_apps_v1.list_namespaced_daemon_set(namespace=namespace)
    return data.to_dict()

def get_statefulsets(namespace):
    data = api_apps_v1.list_namespaced_stateful_set(namespace=namespace)
    return data.to_dict()

def get_cronjobs(namespace):
    data = api_batchs_v1_beta_1.list_namespaced_cron_job(namespace=namespace)
    return data.to_dict()

def get_ingresses(namespace):
    data = api_networking_v1_beta_1.list_namespaced_ingress(namespace=namespace)
    return data.to_dict()

def get_namespaces():
    data = api_core_v1.list_namespace()
    namespaces = [ns.metadata.name for ns in data.items]
    ret = []
    for ns in namespaces:
        ret.append({'name': ns,
                    'deployments': get_deployments(ns),
                    'daemonsets': get_daemonsets(ns),
                    'statefulsets': get_statefulsets(ns),
                    'cronjobs': get_cronjobs(ns),
                    'ingresses': get_ingresses(ns),
                    'helm': get_helm(ns)
                   })
    return ret

def get_nodes():
    nodelist = api_core_v1.list_node()
    return nodelist.to_dict()
       
def get_velero_backups():
    try:
        api_velero_backup = api_custom_object.list_cluster_custom_object("velero.io","v1","backups")
        return api_velero_backup
    except ResourceNotFoundError:
        return []

def get_velero_schedules():
    try:
        api_velero_schedules = api_custom_object.list_cluster_custom_object("velero.io","v1","schedules")
        return api_velero_schedules
    except ResourceNotFoundError:
        return []


allinone = {
            'cluster_name': os.getenv('CLUSTER', ''),
            'cluster_version': get_cluster_version(),
            'lbnref': os.getenv('LBNREF', ''),
            'date': now,
            'nodes': get_nodes(),
            'namespaces': get_namespaces(),
            'velero_backups': get_velero_backups(),
            'velero_schedules': get_velero_schedules(),
            }

jsondata =  json.dumps(allinone, indent=4, default=str)

with open('inventory.json', 'w') as output:
    output.write(jsondata)
