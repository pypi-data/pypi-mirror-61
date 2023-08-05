import os
import yaml
import pkg_resources
import glob


class Config(object):
    @property
    def default_run_backend(self):
        return os.environ.get('RECAST_DEFAULT_RUN_BACKEND','docker')

    def default_build_backend(self):
        return os.environ.get('RECAST_DEFAULT_BUILD_BACKEND','docker')

    @property
    def backends(self):
        return {
            "local": {
                "metadata": {
                    "short_description": "runs locally with natively installed tools"
                },
                "fromstring": "multiproc:auto",
            },
            "docker": {
                "metadata": {"short_description": "runs with containerized tools"},
                "image": os.environ.get("RECAST_IMAGE", "recast/recastatlas:v0.1.0"),
                "cvmfs": {"location": "/cvmfs", "propagation": "rprivate"},
                "reg": {
                    "user": os.environ.get("RECAST_REGISTRY_USERNAME"),
                    "pass": os.environ.get("RECAST_REGISTRY_PASSWORD"),
                    "host": os.environ.get("RECAST_REGISTRY_HOST"),
                },
                "schema_load_token": os.environ.get("YADAGE_SCHEMA_LOAD_TOKEN"),
                "init_token": os.environ.get("YADAGE_SCHEMA_LOAD_TOKEN"),
                "auth_location": os.environ.get("PACKTIVITY_AUTH_LOCATION"),
            },
            "kubernetes": {
                "metadata": {"short_description": "runs on a Kubernetes cluster"},
                "buildkit_addr": os.environ.get("RECAST_KUBERNETES_BUILDKIT_ADDR",'kube-pod://buildkitd'),
            },
        }

    def catalogue_paths(self,include_default = True):
        paths = [pkg_resources.resource_filename("recastatlas", "data/catalogue")] if include_default else []
        configpath = os.environ.get("RECAST_ATLAS_CATALOGUE")

        if configpath:
            for p in configpath.split(":"):
                paths.append(p)
        return paths

    @property
    def catalogue(self):
        paths = self.catalogue_paths()

        cfg = {}
        files = [x for p in paths for x in glob.glob("{}/*.yml".format(p))]
        for f in files:
            d = yaml.safe_load(open(f))
            if not validate_catalogue_entry(d):
                continue
            name = d.pop("name")
            if not "toplevel" in d["spec"]:
                d["spec"]["toplevel"] = os.path.realpath(
                    os.path.join(os.path.dirname(f), "specs")
                )
            cfg[name] = d
        return cfg


config = Config()


def validate_catalogue_entry(entry):
    for x in ['name','metadata','spec']:
        if not x in entry:
            return False
    return True
