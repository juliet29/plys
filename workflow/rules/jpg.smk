
from pathlib import Path 

configfile: "config/test.yaml"

def get_samples(wildcards):
  loc = Path(config["pathvars"]["samples_loc"])
  path = loc / "{sample}" / "out.idf" 
  print(path)
  # TODO: need to consider that there are many paths => data is in buckets... but can keep in buckets? 

  samples, = glob_wildcards(path)

  print(samples)
  return samples



rule all:
    input:
        "<shared_loc>/metrics/out.csv"

rule create_jpg_all:
    input:
      expand("<jpg_loc>/graphs/{sample}/out.json", sample=get_samples)

rule create_jpg:
    input:
        idf = "<samples_loc>/{sample}/out.idf",
        sql = "<samples_loc>/{sample}/eplusout.sql"
    output:
        jpg = "<jpg_loc>/graphs/{sample}/out.json" 
    params:
        dt = config["date_time"],
        name = lambda wildcards: wildcards.sample 
    shell:
        """
        uv run plys jpg create \
            --graph_name {params.name} \
            --idf-path {input.idf} \
            --sql-path {input.sql} \
            --date-time {params.dt} \
            --jpg-path {output.jpg}
        """

rule create_jpg_metrics:
    input:
        jpg = "<jpg_loc>/graphs/{sample}/out.json"
    output:
        metrics = "<jpg_loc>/metrics/{sample}/out.json"
    shell:
        """
        uv run plys jpg create-metrics \
            --jpg-path {input.jpg} \
            --metrics-path {output.metrics}
        """

rule consolidate_metrics:
    input:
        metrics = expand("<jpg_loc>/metrics/{sample}/out.json", sample=get_samples)
    output:
        csv = "<shared_loc>/metrics/out.csv"
    shell:
        """
        uv run plys jpg consolidate \
            --metrics-paths {input.metrics} \
            --csv-path {output.csv}
        """
