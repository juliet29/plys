
def make_eplus_inputs(wildcards):

    loc = Path(config["pathvars"]["samples_loc"])
    idf = loc / "{wildcards.sample}/out.idf".format(wildcards=wildcards),
    sql = loc / "{wildcards.sample}/results/eplusout.sql".format(wildcards=wildcards)
    return {"idf": idf, "sql": sql}

def get_eplus_samples(wildcards): 
  loc = Path(config["pathvars"]["samples_loc"])
  path = loc /  "{sample}" / "results/eplusout.sql" 
  samples, = glob_wildcards(path)

  return samples

def get_qoi_samples(wildcards): 
  loc = Path(config["pathvars"]["qoi_loc"])
  path = loc /  "{sample}" / "{subfolder}/out.parquet" 
  results = glob_wildcards(path)

  return results.sample

def get_jpg_samples(wildcards): 
  loc = Path(config["pathvars"]["jpg_loc"])
  path = loc / "metrics"/  "{sample}" / "out.json" 
  results = glob_wildcards(path)

  return results.sample

