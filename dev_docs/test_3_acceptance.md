# Acceptance testing of a version

**See below for what RUN CHECKS means**

1. RUN CHECKS on the proposed application locally as a docker container before pushing to docker hub or github main
2. Upload to docker hub and then RUN CHECKS on that docker image FROM ANOTHER MACHINE
3. Upload to the public webserver and then RUN CHECKS from a non ICR laptop or at least not inside the ICR and not on the VPN
4. RUN CHECKS from a mobile


RUN CHECKS means:
- The app is accessible
- The app is responsive
- The app runs
  - beauti-box: test you can create a beauti xml file and download it
  - pisca-box: test you can upload a beauti xml file and it is displayed
  - tree-annotator: test you can annotate the previous trees file and download it
  - plot-box: you can produce the plot from the above (or other files)
- The app is performant
  - all the above is not too slow

