# CTJ storefront production promotion

DCS authorized deployment of the approved storefront and subsequent ESCD update.

{
  "task_id": "SC-CTJ-PROMOTION-20261019-01",
  "status": "DEPLOYED",
  "production_url": "https://sonlyconsulting.com/ctj/",
  "netlify_deploy_id": "6ad6b7cfb4adc6e92d314ca8",
  "site_id": "23a265c1-6ba1-4e82-aeaa-e39084842c40",
  "source_commit": "ec50ba0569546b1acc22ebc4eaf97698f8c7c9d7",
  "artifact_sha256": "4f2eedc1bd206712ac8e589d34a8e71bff02dc3518893e13f897c81550c41a1a",
  "verified": "Netlify published success and live browser hero/navigation/product-price readback",
  "preserved_files": 124,
  "package_changes": [
    "ctj/index.html",
    "netlify.toml publish path corrected to ."
  ],
  "commerce_status": "INCOMPLETE: SCA and bundle links, purchase return/delivery/email acceptance remain open in SC-CTJ issue 21"
}

ESCD deployment source is based on current production commit 601f35099530e51beea2409c062687976dbed419, preserving the verified chat-persistence and ambiance repair. This branch updates only the two catalog copies, the bounded canonical knowledge record and this receipt. Runtime consumption is pending the ESCD deployment readback, and must not be inferred from the commit. The original Voter Matrix canvas and historical deliverables remain available; they are not represented as the whole CTJ family.
