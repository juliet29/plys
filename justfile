
push-tag end:
  git tag -a s0.1.{{end}} -m s0.1.{{end}}
  git push --tag


publish-tag end:
  @echo "Have you updated the version number for pushing to pypi?" 
  @read status;


  @echo "Have you pushed the code with this new version number?" 
  @read status;

  git tag -a v0.1.{{end}} -m v0.1.{{end}}
  git push --tag
  sleep 2
  gh run list
  #TODO: read from the tags automatically using sed / awk 
  #
  #


#### ======== TESTING SMK  ===============
run-qoi:
  uv run snakemake -c 1 qoi_create_target
  uv run snakemake -c 1 qoi_consolidate_target

run-jpg:
  uv run snakemake -c 1 jpg_create_target
  uv run snakemake -c 1 jpg_consolidate_target

clear-smk:
  rm -rIv static/4_temp/smk/test/*

