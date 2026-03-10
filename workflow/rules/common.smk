

def get_samples(wildcards): # TODO: move to a common.smk
  loc = Path(config["pathvars"]["samples_loc"])
  path = loc / "{sample}" / "results/eplusout.sql" 
  # print(path)
  # TODO: can us loguru here as well, if want this to be part of the reporting. 
  # TODO: need to consider that there are many paths => data is in buckets... but can keep in buckets? 

  samples, = glob_wildcards(path)

  # print(samp
  return samples

