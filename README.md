# Fabric Release Guardian

An original Azure DevOps companion for Microsoft Fabric CI/CD. It turns a deployment manifest into a release-readiness report, applies policy-as-code checks, and recommends an approval gate for high-risk releases.

## Why it is different

Fabric deployment automation is valuable, but enterprise delivery also needs evidence: what changed, whether the target is ready, whether a connection or capacity is missing, and whether a human approval is warranted. Release Guardian adds that control plane without deploying or mutating Fabric resources itself.

```text
Fabric item manifest + target environment config
                    |
                    v
             Release Guardian
       policy checks + risk classification
                    |
                    v
 Azure DevOps pipeline summary + approval decision
```

## Checks included

- target workspace and capacity exist
- required connections are mapped for the target environment
- production deployment has an approved change reference
- semantic-model changes and high-impact item types raise the release risk
- policy failures block the deployment stage before Fabric automation runs

## Run locally

```bash
python src/release_guardian.py \
  --manifest sample_data/release_manifest.json \
  --environment sample_data/prod_environment.json \
  --output release_readiness.md
```

## Azure DevOps integration

[`pipelines/fabric-release.yml`](pipelines/fabric-release.yml) validates a release before the deployment job. It is designed to sit in front of the Microsoft Fabric Azure DevOps extension or `fabric-cicd`; those tools perform the actual deployment after the gate passes.

This design follows Fabric's current CI/CD guidance: source control versions workspace definitions, while deployment pipelines or code-driven automation move changes through environments. [Microsoft Learn](https://learn.microsoft.com/en-us/fabric/fundamentals/understand-best-practices-fabric-cicd)

## Portfolio note

This is an independent demonstration project. It uses fictional environment and item data, and contains no employer, client, tenant, or production configuration.
